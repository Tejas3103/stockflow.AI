"""
Qualitative tools for stock analysis using external APIs for research.
"""

import os
import requests
from datetime import datetime
from langchain.tools import tool

@tool("research_company_fundamentals")
def research_company_fundamentals(ticker_or_company: str) -> str:
    """Research fundamental business information about a company beyond stock performance.
    
    Args:
        ticker_or_company: Stock ticker or company name (e.g., 'AAPL' or 'Apple Inc')
        
    Returns:
        In-depth business information including model, strategy, and competition
    """
    try:
        exa_api_key = os.getenv("EXA_API_KEY")
        if not exa_api_key:
            raise ValueError("EXA_API_KEY not found in environment variables")
        
        
        headers = {"x-api-key":exa_api_key}
        params = {
            "query": f"{ticker_or_company} business model strategy competition",
            "useAutoprompt": True,
            "numResults": 5
        }
        response = requests.post("https://api.exa.ai/search", headers=headers, json=params)
        response.raise_for_status()
        
        results = response.json().get("results", [])
        if not results:
            return f"No fundamental information found for {ticker_or_company}."
        
        # Format the research results
        insights = f"## Company Fundamentals: {ticker_or_company}\n\n"
        
        for i, result in enumerate(results[:5]):
            title = result.get("title", "Untitled")
            text = result.get("text", "No text available")
            url = result.get("url", "No URL available")
            date = result.get("publishedDate", "Unknown date")
            
            insights += f"### Source {i+1}: {title}\n"
            insights += f"{text[:500]}...\n"
            insights += f"Published: {date}\n"
            insights += f"Source: {url}\n\n"
        
        return insights
    except Exception as e:
        return f"Error researching company fundamentals for {ticker_or_company}: {str(e)}"

@tool("analyze_industry_trends")
def analyze_industry_trends(industry: str, region: str = "global") -> str:
    """Research current trends in a specific industry with regional focus.
    
    Args:
        industry: The industry to analyze (e.g., 'semiconductor', 'retail', 'banking')
        region: Optional regional focus (e.g., 'US', 'India', 'Europe')
        
    Returns:
        Analysis of industry trends, challenges, and opportunities
    """
    try:
        exa_api_key = os.getenv("EXA_API_KEY")
        if not exa_api_key:
            raise ValueError("EXA_API_KEY not found in environment variables.")
 
        headers = {"x-api-key": exa_api_key}
        params = {
            "query": f"latest trends in {industry} industry {region} market {datetime.now().strftime('%Y')}",
            "useAutoprompt": True,
            "numResults": 5
        }
        response = requests.post("https://api.exa.ai/search", headers=headers, json=params)
        response.raise_for_status()
        
        results = response.json().get("results", [])
        if not results:
            return f"No industry trend information found for {industry} in {region}."
        
        # Format the research results
        insights = f"## Industry Analysis: {industry} ({region})\n\n"
        
        for i, result in enumerate(results[:5]):
            title = result.get("title", "Untitled")
            text = result.get("text", "No text available")
            url = result.get("url", "No URL available")
            date = result.get("publishedDate", "Unknown date")
            
            insights += f"### Trend Source {i+1}: {title}\n"
            insights += f"{text[:500]}...\n"
            insights += f"Published: {date}\n"
            insights += f"Source: {url}\n\n"
        
        return insights
    except Exception as e:
        return f"Error analyzing industry trends for {industry} in {region}: {str(e)}"