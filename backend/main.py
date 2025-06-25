import sys
import os
import logging
import time
from datetime import datetime
import requests
import yfinance as yf

# Add the directory containing your LangGraph code to the Python path
# Using a path relative to the expected working directory (project root)
sys.path.insert(0, '../Multi-Agent Stock Analysis recommendation')

# ---
# LLM/Agent features temporarily disabled for Tavily-only mode.
# To re-enable, uncomment the import and LangGraph initialization below, and ensure the module exists.
# from stock_analysis_graph import create_stock_analysis_graph, StockAnalysisState
# ---

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


# Configure logging at the beginning of your application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Define different logger instances for specific purposes
error_logger = logging.getLogger("error_log")   # For critical errors
app_logger = logging.getLogger("app_log")       # For general application info/debug messages
audit_logger = logging.getLogger("audit_log")   # For request auditing and tracing

app = FastAPI() #this app object is what uvicorn runs and handles api routes

# Configure CORS
origins = [
    "http://localhost:5173",  # Allow your frontend origin
    # Add other origins if needed (e.g., production domain)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, PUT, DELETE, etc)
    allow_headers=["*"], # Allows all headers
)

# Middleware for request logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    request_id = str(time.time())  # Simple request ID for tracking
    
    # Log the incoming request
    audit_logger.info("Incoming request", extra={
        "request_id": request_id,
        "method": request.method,
        "url": str(request.url),
        "client_host": request.client.host if request.client else None,
        "headers": dict(request.headers)
    })
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log the response
        audit_logger.info("Request completed", extra={
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "process_time_ms": round(process_time * 1000, 2)
        })
        
        return response
    except Exception as e:
        error_logger.error("Request failed", exc_info=True, extra={
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "error": str(e)
        })
        raise

# ---
# LLM/Agent features temporarily disabled for Tavily-only mode.
# To re-enable, uncomment the LangGraph initialization below, and ensure the module exists.
# try:
#     app_logger.info("Initializing LangGraph...")
#     stock_analysis_graph = create_stock_analysis_graph()
#     app_logger.info("LangGraph initialized successfully")
# except Exception as e:
#     error_logger.error("Failed to initialize LangGraph", exc_info=True, extra={
#         "error_type": type(e).__name__,
#         "error_message": str(e)
#     })
#     raise
# ---

# Define a request model for the chat message
class Message(BaseModel):
    content: str

class TavilySearchRequest(BaseModel):
    query: str

@app.get("/")
async def read_root():
    app_logger.info("Root endpoint accessed")
    return {"Hello": "World", "status": "running", "timestamp": datetime.now().isoformat()}

# ---
# LLM/Agent chat endpoint temporarily disabled for Tavily-only mode.
# To re-enable, uncomment the /chat endpoint below, and ensure the module exists.
# @app.post("/chat")
# async def chat(message: Message):
#     ...
# ---

@app.post("/tavily_search")
async def tavily_search(request: TavilySearchRequest):
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        raise HTTPException(status_code=500, detail="Tavily API key not configured.")
    
    url = "https://api.tavily.com/search"
    headers = {"Authorization": f"Bearer {tavily_key}", "Content-Type": "application/json"}
    payload = {"query": request.query, "search_depth": "advanced", "include_answer": True}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        # Return the answer and top sources if available
        return {
            "answer": data.get("answer"),
            "sources": data.get("sources", []),
            "raw": data
        }
    except Exception as e:
        error_logger.error("Tavily search failed", exc_info=True, extra={"error": str(e)})
        raise HTTPException(status_code=500, detail=f"Tavily search failed: {str(e)}")

@app.get("/top_stocks")
async def top_stocks():
    # ---
    # LIVE DATA (yfinance) - Uncomment to enable real-time fetching
    # tickers = ["AAPL", "MSFT", "NVDA"]
    # stocks = []
    # try:
    #     data = yf.download(tickers, period="1d", group_by='ticker', threads=True, progress=False)
    #     for ticker in tickers:
    #         try:
    #             info = yf.Ticker(ticker).info
    #             name = info.get("shortName") or info.get("longName") or ticker
    #             price = data[ticker]["Close"][0] if ticker in data and "Close" in data[ticker] else None
    #             prev_close = data[ticker]["Open"][0] if ticker in data and "Open" in data[ticker] else None
    #             change = round(((price - prev_close) / prev_close) * 100, 2) if price and prev_close else 0
    #             recommendation = info.get("recommendationKey", "No data available.")
    #             stocks.append({
    #                 "name": name,
    #                 "ticker": ticker,
    #                 "price": round(price, 2) if price else None,
    #                 "change": change,
    #                 "recommendation": recommendation.capitalize() if isinstance(recommendation, str) else "No data available."
    #             })
    #         except Exception as e:
    #             stocks.append({
    #                 "name": ticker,
    #                 "ticker": ticker,
    #                 "price": None,
    #                 "change": 0,
    #                 "recommendation": "No data available."
    #             })
    #     return {"stocks": stocks}
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Failed to fetch top stocks: {str(e)}")
    # ---
    # STATIC DEMO DATA (for reliability)
    stocks = [
        {"name": "Apple Inc.", "ticker": "AAPL", "price": 212.45, "change": 1.23, "recommendation": "Buy - Strong brand, solid growth."},
        {"name": "Microsoft Corp.", "ticker": "MSFT", "price": 345.67, "change": -0.56, "recommendation": "Hold - Stable earnings, watch for tech trends."},
        {"name": "NVIDIA Corp.", "ticker": "NVDA", "price": 123.45, "change": 2.78, "recommendation": "Buy - AI leader, high growth potential."},
        {"name": "Tesla Inc.", "ticker": "TSLA", "price": 789.01, "change": -1.12, "recommendation": "Sell - Volatile, recent pullbacks."},
        {"name": "Amazon.com Inc.", "ticker": "AMZN", "price": 134.56, "change": 0.89, "recommendation": "Buy - E-commerce and cloud strength."}
    ]
    return {"stocks": stocks}

# Log application shutdown
@app.on_event("shutdown")
async def shutdown_event():
    app_logger.info("Application shutting down", extra={
        "shutdown_time": datetime.now().isoformat()
    }) 