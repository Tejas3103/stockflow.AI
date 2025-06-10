# StockFlow.AI 🤖📈

> **Multi-Agent Stock Analysis & Recommendation System**

StockFlow.AI is an intelligent stock analysis platform that combines qualitative and quantitative analysis using advanced AI agents to provide comprehensive stock recommendations and market insights.

## ✨ Features

- **🤖 Multi-Agent Analysis**: Qualitative and quantitative agents working together
- **📊 Real-time Data**: Live stock prices, financial ratios, and market trends
- **📰 News Sentiment**: AI-powered news analysis and sentiment detection
- **🎯 Smart Recommendations**: Data-driven stock recommendations
- **💬 Interactive Chat**: Natural language interface for stock queries
- **📱 Modern UI**: Clean, responsive web interface

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Modern CSS** with responsive design

### Backend
- **FastAPI** for high-performance API
- **LangGraph** for multi-agent orchestration
- **Python** with async/await support

### AI & Data
- **OpenAI GPT** for natural language processing
- **Tavily Search** for real-time news and data
- **yfinance** for financial data
- **Pandas & NumPy** for data analysis

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- Python 3.8+
- API keys for OpenAI and Tavily

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/stockflow.AI.git
   cd stockflow.AI
   ```

2. **Set up the backend**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Run the application**
   ```bash
   # Terminal 1: Start backend
   cd backend
   uvicorn main:app --reload
   
   # Terminal 2: Start frontend
   cd frontend
   npm run dev
   ```

5. **Open your browser**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

## 📖 Usage

1. **Open the chat interface** at http://localhost:5173
2. **Enter your query** in the format: `STOCK_SYMBOL your question`
   - Example: `AAPL analyze the recent performance`
   - Example: `MSFT what are the analyst recommendations`
3. **Get AI-powered analysis** from both qualitative and quantitative agents

## 🏗️ Project Structure

```
stockflow.AI/
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx          # Main chat interface
│   │   └── App.css          # Styling
│   └── package.json
├── backend/                  # FastAPI backend
│   └── main.py              # API endpoints
├── Multi-Agent Stock Analysis recommendation/
│   ├── stock_analysis_graph.py    # LangGraph workflow
│   ├── qualitative_tools.py       # News & sentiment tools
│   └── quantitative_tools.py      # Financial analysis tools
└── README.md
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# OpenAI API
OPENAI_API_KEY=your_openai_api_key

# Azure OpenAI (alternative)
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint

# Tavily Search API
TAVILY_API_KEY=your_tavily_api_key
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) for multi-agent orchestration
- Powered by [OpenAI](https://openai.com/) for natural language processing
- Financial data from [yfinance](https://github.com/ranaroussi/yfinance)
- News search powered by [Tavily](https://tavily.com/)

## 📞 Support

If you have any questions or need help, please open an issue on GitHub.

---

**Made with ❤️ for intelligent stock analysis** 