# stock_analysis_graph.py

"""
Multi-agent system for stock analysis using LangGraph.

This system performs both qualitative and quantitative analysis of stocks:
- Supervisor Agent: Coordinates the overall analysis
- Qualitative Agent: Gathers news and sentiment using Tavily search
- Quantitative Agent: Analyzes price data using yfinance

"""

import os
from datetime import datetime
from typing import Dict, Any, Optional, List

# LangGraph imports
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent

# LangChain imports
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools import TavilySearchResults
from langgraph.graph import END

# Import the tools from separate files
from qualitative_tools import research_company_fundamentals, analyze_industry_trends
from quantitative_tools import (
    get_stock_prices, 
    get_price_extremes, 
    analyze_recent_trend,
    analyze_portfolio_risk,
    get_financial_ratios,
    get_earnings_calendar,
    get_analyst_recommendations
)
from dotenv import load_dotenv
import json
import pandas as pd
import numpy as np

# Load environment variables
load_dotenv()

def get_llm():
    """Get the appropriate LLM based on available API keys."""
    # Check for OpenAI API key
    if os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI API")
        return ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            streaming=True
        )
    
    # Check for Azure OpenAI API key and endpoint
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if azure_key and azure_endpoint and azure_key != "your-azure-openai-api-key":
        print("Using Azure OpenAI API")
        return AzureChatOpenAI(
            azure_deployment="gpt-3.5-turbo",
            openai_api_version="2024-02-15-preview",
            temperature=0,
            streaming=True
        )
    
    raise ValueError("No valid API key found. Please set either OPENAI_API_KEY or AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT")

def create_qualitative_agent():
    """Create the qualitative analysis agent.
    
    This agent is responsible for gathering and analyzing news, events, and sentiment
    about a stock using the Tavily search API, company fundamentals, and industry trends.
    
    Returns:
        A LangGraph agent that can perform qualitative analysis
    """
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    tavily_search = TavilySearchResults(
        max_results=5,
        api_key=os.getenv("TAVILY_API_KEY")
    )
    
    base_agent = create_react_agent(
        model=get_llm(),
        tools=[tavily_search, research_company_fundamentals, analyze_industry_trends],
        name="qualitative_agent",
        prompt=f"""You are an expert financial researcher specializing in qualitative stock analysis with deep knowledge of global markets, including emerging markets.

CRITICAL TIME AWARENESS: The current date is {current_date}. ALL your searches must include this date in your search queries when time-relevant.

IMPORTANT: Always format your final response as a message using the following structure:
[MARKET CONTEXT]
* Overall overview of relevant market/sector conditions
* Key economic indicators and policy influences
* Sources: [citations]

[KEY DEVELOPMENTS]
* Chronological list of significant news and events
* Impact assessment for each development
* Sources: [citations]

[SENTIMENT ANALYSIS]
* Analyst ratings and consensus
* Media sentiment trends
* Institutional investor activity
* Sources: [citations]

[RISKS AND OPPORTUNITIES]
* Identified threats to performance
* Growth catalysts and emerging opportunities
* Sources: [citations]

Remember to always end your analysis with a clear message that can be passed to the quantitative agent.
"""
    )
    
    def agent_wrapper(state):
        # Call the base agent with the state
        result = base_agent.invoke(state)
        # Append the result to the messages list
        messages = state.get("messages", [])
        if isinstance(result, dict) and "output" in result:
            messages.append(result["output"])
        else:
            messages.append(result)
        # Return the updated state
        return {**state, "messages": messages}
    return agent_wrapper

def create_quantitative_agent():
    """Create the quantitative analysis agent.
    
    This agent is responsible for analyzing stock price data using yfinance,
    identifying extremes, analyzing trends, portfolio risk, financial ratios,
    and earnings information.
    
    Returns:
        A LangGraph agent that can perform quantitative analysis
    """
    
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    base_agent = create_react_agent(
        model=get_llm(),
        tools=[
            get_stock_prices, 
            get_price_extremes, 
            analyze_recent_trend,
            analyze_portfolio_risk,
            get_financial_ratios,
            get_earnings_calendar,
            get_analyst_recommendations
        ],
        name="quantitative_agent",
        prompt=f"""You are an expert quantitative financial analyst specializing in technical analysis, risk assessment, and price pattern recognition across global markets.

CRITICAL TIME AWARENESS: The current date is {current_date}. All your analyses should be performed with this date as the reference point.

IMPORTANT: Always format your final response as a message using the following structure:
[PRICE SUMMARY]
* Current (as of {current_date}) and historical price data
* Key statistics and benchmark comparisons

[TREND ANALYSIS]
* Direction, strength, and duration of trends
* Support/resistance levels and pattern identification
* Volume confirmation analysis

[RISK ASSESSMENT]
* Volatility metrics with historical context
* Risk-adjusted performance metrics
* Liquidity and market depth analysis

[KEY DATES FOR INVESTIGATION]
* Specific dates where significant price/volume movements occurred
* Preliminary correlation with market-wide movements
* Questions for qualitative agent follow-up

Remember to always end your analysis with a clear message that can be passed to the qualitative agent.
"""
    )
    
    def agent_wrapper(state):
        result = base_agent.invoke(state)
        messages = state.get("messages", [])
        if isinstance(result, dict) and "output" in result:
            messages.append(result["output"])
        else:
            messages.append(result)
        return {**state, "messages": messages}
    return agent_wrapper

from pydantic import BaseModel, Field

class StockAnalysisState(BaseModel):
    input: str = Field(description="The user's query (e.g. 'Analyze the stock AAPL')")
    stock_symbol: str = Field(description="The stock symbol (e.g. 'AAPL')")
    result: Optional[str] = Field(default=None, description="The final analysis result (output)")

def create_stock_analysis_graph():
    """Create the multi-agent system for stock analysis.
    
    This function creates the complete graph with all agents:
    - Qualitative Agent: Handles news and sentiment
    - Quantitative Agent: Handles price analysis
    
    Returns:
        A compiled LangGraph that can be run
    """
    
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Create the specialized agents
    qualitative_agent = create_qualitative_agent()
    quantitative_agent = create_quantitative_agent()
    
    # Create a simple state graph instead of using supervisor
    workflow = StateGraph(state_schema=StockAnalysisState)
    
    # Add nodes for each agent
    workflow.add_node("qualitative_agent", qualitative_agent)
    workflow.add_node("quantitative_agent", quantitative_agent)
    
    # Define the edges - both agents can be called independently
    workflow.add_edge("qualitative_agent", "quantitative_agent")
    workflow.add_edge("quantitative_agent", "qualitative_agent")
    
    # Set the entry point
    workflow.set_entry_point("qualitative_agent")
    
    # Compile the graph
    return workflow.compile()

if __name__ == "__main__":
    # Create the graph
    graph = create_stock_analysis_graph()
    
    # Example usage
    stock_symbol = input("Enter stock symbol (e.g., AAPL, MSFT): ")
    
    # Run the analysis with proper message formatting
    result = graph.invoke({
        "input": f"Analyze the stock {stock_symbol}",
        "stock_symbol": stock_symbol,
        "messages": []  # Initialize empty messages list
    })
    
    print("\nAnalysis Results:")
    print(result["result"] if result.get("result") else result)