# StockFlow.AI – Project Overview

## 🚀 Elevator Pitch
StockFlow.AI is an intelligent, multi-agent stock analysis and recommendation platform. It combines real-time financial data, AI-powered qualitative and quantitative analysis, and a modern, interactive dashboard to help users make smarter investment decisions. Imagine ChatGPT meets Bloomberg Terminal, but accessible and user-friendly!

---

## 🧐 What is StockFlow.AI?
StockFlow.AI is a web application that allows users to:
- **Chat** with AI agents about stocks, market trends, and investment strategies
- **Get real-time stock data** and news
- **Receive actionable recommendations** based on both numbers (quantitative) and news/sentiment (qualitative)
- **Explore a modern, glassmorphic dashboard** with a professional look and feel

---

## 🏗️ How Does It Work? (High-Level)
1. **User enters a stock-related question** in the chat (e.g., "AAPL recent performance?").
2. **Frontend (React + Vite)** sends the query to the backend.
3. **Backend (FastAPI)** routes the query to:
   - **Tavily** for real-time news/search
   - **OpenAI** for natural language analysis (if API key provided)
   - **yfinance** for live stock data (or demo data)
4. **AI agents** (qualitative & quantitative) analyze the data and generate a response.
5. **Frontend displays** the answer in a chat interface, alongside top stocks and market news.

---

## 🛠️ Tech Stack (Summary)
- **Frontend:** React 19, Vite, TypeScript, styled-components
- **Backend:** FastAPI, Python, LangGraph, yfinance, Tavily, OpenAI
- **Other:** Modern UI/UX, glassmorphic dashboard, modular codebase

---

## 🗺️ Architecture (Simple Diagram)

User (Browser)
   │
   ▼
Frontend (React Dashboard)
   │
   ▼
Backend (FastAPI API)
   ├──> Tavily (News/Search)
   ├──> yfinance (Stock Data)
   └──> OpenAI (AI Analysis)

---

## 🗣️ How to Explain in an Interview
- "I built StockFlow.AI, a full-stack web app for intelligent stock analysis. It uses a multi-agent backend (FastAPI + LangGraph) to combine real-time financial data, news sentiment, and AI-powered recommendations. The frontend is a modern, glassmorphic dashboard where users can chat with AI agents, view top stocks, and get actionable insights. I handled everything from backend API design and AI integration to frontend architecture and UI/UX."

---

## 👥 For Friends/Collaborators
- **It's like having a smart financial advisor you can chat with.**
- You ask about any stock, and the app gives you both the numbers and the story behind them.
- The dashboard is clean, modern, and easy to use.
- All code is modular and well-documented for easy collaboration.

---

## 📚 Want to Dive Deeper?
- See the README for setup and usage.
- Explore the `frontend/src/components` and `backend/` folders for code.
- Open an issue or PR if you want to contribute! 