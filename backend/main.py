import sys
import os
# Add the directory containing your LangGraph code to the Python path
# Using a path relative to the expected working directory (project root)
sys.path.insert(0, './Multi-Agent Stock Analysis recommendation')

# Import your LangGraph components (should be discoverable now)
from stock_analysis_graph import create_stock_analysis_graph, StockAnalysisState

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# Initialize the LangGraph (do this once when the app starts)
stock_analysis_graph = create_stock_analysis_graph()
print("LangGraph created successfully.")

# Define a request model for the chat message
class Message(BaseModel):
    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Modify the chat endpoint to use the LangGraph
@app.post("/chat")
async def chat(message: Message):
    user_query = message.content.strip()
    print(f"Received user query: {user_query}")

    # Basic parsing for stock symbol (assuming format "SYMBOL query...")
    parts = user_query.split(maxsplit=1)
    if len(parts) < 2:
        return {"response": "Please provide a stock symbol and your query (e.g., AAPL Analyze the stock)."}

    stock_symbol = parts[0].upper() # Assume first word is symbol
    query_text = parts[1] # The rest is the query input for the graph
    print(f"Parsed Symbol: {stock_symbol}, Query: {query_text}")

    try:
        # Create initial state for LangGraph
        initial_state = StockAnalysisState(input=user_query, stock_symbol=stock_symbol) # Pass both fields
        print(f"Initial state: {initial_state.model_dump_json()}")

        # Run the LangGraph (synchronously for now, can be made async)
        # You might need to adapt how you invoke your specific graph
        # Assuming invoke takes state and returns a final state with a 'result' field
        # If your graph streaming, you might need a different approach.
        final_state = stock_analysis_graph.invoke(initial_state)
        print(f"Final state: {final_state.model_dump_json()}")

        # Extract the result from the final state
        agent_response = final_state.result if final_state and final_state.result is not None else "Could not get a specific analysis result."

        print(f"Sending response: {agent_response}")
        return {"response": agent_response}

    except Exception as e:
        print(f"Error running LangGraph: {e}")
        return {"response": f"An error occurred during analysis: {e}"} 