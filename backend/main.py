import sys
import os
import logging
import time
from datetime import datetime

# Add the directory containing your LangGraph code to the Python path
# Using a path relative to the expected working directory (project root)
sys.path.insert(0, '../Multi-Agent Stock Analysis recommendation')

# Import your LangGraph components (should be discoverable now)
from stock_analysis_graph import create_stock_analysis_graph, StockAnalysisState

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.logger import get_logger

# Configure logging level
logging.basicConfig(level=logging.INFO)

# Set up different loggers for different purposes
app_logger = get_logger("app", log_type="application")
error_logger = get_logger("errors", log_type="errors", log_level=logging.ERROR)
audit_logger = get_logger("audit", log_type="audit", json_format=True)

# Log application startup
app_logger.info("Starting application", extra={
    "startup_time": datetime.now().isoformat(),
    "python_version": sys.version,
    "environment": os.getenv("ENVIRONMENT", "development")
})

app = FastAPI()

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

# Initialize the LangGraph (do this once when the app starts)
try:
    app_logger.info("Initializing LangGraph...")
    stock_analysis_graph = create_stock_analysis_graph()
    app_logger.info("LangGraph initialized successfully")
except Exception as e:
    error_logger.error("Failed to initialize LangGraph", exc_info=True, extra={
        "error_type": type(e).__name__,
        "error_message": str(e)
    })
    raise

# Define a request model for the chat message
class Message(BaseModel):
    content: str

@app.get("/")
async def read_root():
    app_logger.info("Root endpoint accessed")
    return {"Hello": "World", "status": "running", "timestamp": datetime.now().isoformat()}

# Modify the chat endpoint to use the LangGraph
@app.post("/chat")
async def chat(message: Message):
    request_id = str(time.time())  # Unique request ID
    user_query = message.content.strip()
    app_logger.info("Processing chat request", extra={
        "request_id": request_id,
        "query": user_query
    })

    # Basic parsing for stock symbol (assuming format "SYMBOL query...")
    parts = user_query.split(maxsplit=1)
    if len(parts) < 2:
        app_logger.warning("Invalid query format received", extra={
            "request_id": request_id,
            "query": user_query
        })
        return {"response": "Please provide a stock symbol and your query (e.g., AAPL Analyze the stock)."}

    stock_symbol = parts[0].upper() # Assume first word is symbol
    query_text = parts[1] # The rest is the query input for the graph
    app_logger.debug("Parsed query", extra={
        "request_id": request_id,
        "symbol": stock_symbol,
        "query": query_text
    })

    try:
        # Create initial state for LangGraph
        initial_state = StockAnalysisState(input=user_query, stock_symbol=stock_symbol) # Pass both fields
        app_logger.debug("Created initial state", extra={
            "request_id": request_id,
            "state": initial_state.model_dump_json()
        })

        # Run the LangGraph (synchronously for now, can be made async)
        # You might need to adapt how you invoke your specific graph
        # Assuming invoke takes state and returns a final state with a 'result' field
        # If your graph streaming, you might need a different approach.
        final_state = stock_analysis_graph.invoke(initial_state)
        app_logger.debug("Received final state", extra={
            "request_id": request_id,
            "state": final_state.model_dump_json()
        })

        # Extract the result from the final state
        agent_response = final_state.result if final_state and final_state.result is not None else "Could not get a specific analysis result."
        
        # Log successful analysis
        audit_logger.info("Stock analysis completed", extra={
            "request_id": request_id,
            "symbol": stock_symbol,
            "query": query_text,
            "response_length": len(agent_response)
        })

        return {"response": agent_response}

    except Exception as e:
        error_logger.error("Error during stock analysis", exc_info=True, extra={
            "request_id": request_id,
            "symbol": stock_symbol,
            "query": query_text,
            "error": str(e)
        })
        return {"response": f"An error occurred during analysis: {str(e)}"}

# Log application shutdown
@app.on_event("shutdown")
async def shutdown_event():
    app_logger.info("Application shutting down", extra={
        "shutdown_time": datetime.now().isoformat()
    }) 