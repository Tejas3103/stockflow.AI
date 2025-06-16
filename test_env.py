import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This assumes .env is in the same directory as test_env.py
load_dotenv()

tavily_key = os.getenv("TAVILY_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")
exa_key = os.getenv("EXA_API_KEY") # Include Exa key for testing all

print(f"Loaded TAVILY_API_KEY: {tavily_key is not None}")
print(f"Loaded OPENAI_API_KEY: {openai_key is not None}")
print(f"Loaded EXA_API_KEY: {exa_key is not None}")

if tavily_key:
    print(f"TAVILY_API_KEY value length: {len(tavily_key)} (first 5 chars: {tavily_key[:5]}... )")
if openai_key:
    print(f"OPENAI_API_KEY value length: {len(openai_key)} (first 5 chars: {openai_key[:5]}... )")
if exa_key:
    print(f"EXA_API_KEY value length: {len(exa_key)} (first 5 chars: {exa_key[:5]}... )")

# If you want to see the actual values (for debugging, be careful not to share sensitive info)
# print(f"TAVILY_API_KEY value: {tavily_key}")
# print(f"OPENAI_API_KEY value: {openai_key}")
# print(f"EXA_API_KEY value: {exa_key}")