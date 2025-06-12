# 🛠️ Troubleshooting Guide

This guide helps you resolve common issues when setting up and running StockFlow.AI.

## 🚨 Common Issues

### 1. Missing Dependencies

**Problem:** `command not found: python3` or `command not found: node`

**Solution:**
```bash
# Install Python 3.8+
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# macOS (using Homebrew)
brew install python3

# Install Node.js 16+
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# macOS (using Homebrew)
brew install node
```

### 2. Virtual Environment Issues

**Problem:** `ModuleNotFoundError` or `No module named 'uvicorn'`

**Solution:**
```bash
# Make sure you're in the project root
cd /path/to/stockflow.AI

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Dependencies Issues

**Problem:** `npm ERR!` or missing frontend dependencies

**Solution:**
```bash
# Navigate to frontend directory
cd frontend

# Clear npm cache
npm cache clean --force

# Remove node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### 4. Environment Variables Issues

**Problem:** API errors or missing configuration

**Solution:**
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your API keys
nano .env  # or use your preferred editor

# Required keys:
# OPENAI_API_KEY=your_openai_api_key_here
# TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. Port Already in Use

**Problem:** `Address already in use` or port conflicts

**Solution:**
```bash
# Check what's using the ports
lsof -i :8000  # Backend port
lsof -i :5173  # Frontend port

# Kill processes using those ports
kill -9 <PID>

# Or use different ports
# Backend: uvicorn main:app --reload --port 8001
# Frontend: npm run dev -- --port 5174
```

### 6. CORS Issues

**Problem:** Frontend can't connect to backend

**Solution:**
- Make sure backend is running on `http://localhost:8000`
- Make sure frontend is running on `http://localhost:5173`
- Check that CORS is properly configured in `backend/main.py`

### 7. Git Issues

**Problem:** Missing files after cloning

**Solution:**
```bash
# Make sure you have the latest version
git pull origin main

# If package-lock.json is missing
cd frontend
npm install
```

## 🔧 Debug Mode

To run with more verbose output:

```bash
# Backend with debug
cd backend
python -m uvicorn main:app --reload --log-level debug

# Frontend with debug
cd frontend
npm run dev -- --debug
```

## 📋 Pre-flight Checklist

Before running the application, ensure:

- [ ] Python 3.8+ is installed
- [ ] Node.js 16+ is installed
- [ ] Virtual environment is created and activated
- [ ] Python dependencies are installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies are installed (`cd frontend && npm install`)
- [ ] `.env` file exists with valid API keys
- [ ] Ports 8000 and 5173 are available

## 🆘 Still Having Issues?

1. **Check the logs** - Look for error messages in the terminal
2. **Verify API keys** - Make sure your OpenAI and Tavily API keys are valid
3. **Check network** - Ensure you have internet access for API calls
4. **Restart everything** - Sometimes a fresh start helps:
   ```bash
   # Stop all processes
   pkill -f uvicorn
   pkill -f vite
   
   # Restart
   ./start.sh
   ```

## 📞 Getting Help

If you're still experiencing issues:

1. Check existing [GitHub Issues](https://github.com/YOUR_USERNAME/stockflow.AI/issues)
2. Create a new issue with:
   - Your operating system
   - Python and Node.js versions
   - Complete error messages
   - Steps to reproduce the issue

---

**Remember:** Most issues can be resolved by following the setup guide carefully and ensuring all prerequisites are met! 🚀 