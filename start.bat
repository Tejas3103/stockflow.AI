@echo off
echo 🚀 Starting StockFlow.AI...

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  Warning: .env file not found!
    echo 📝 Please copy env.example to .env and configure your API keys:
    echo    copy env.example .env
    echo    # Then edit .env with your actual API keys
    echo.
)

REM Start backend
echo 🔧 Starting backend server...
cd backend
start "Backend Server" cmd /k "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
cd ..

REM Wait a moment for backend to start
timeout /t 2 /nobreak >nul

REM Start frontend
echo 🎨 Starting frontend server...
cd frontend
start "Frontend Server" cmd /k "npm run dev"
cd ..

echo.
echo ✅ StockFlow.AI is starting up!
echo 📊 Backend API: http://localhost:8000
echo 🎨 Frontend: http://localhost:5173
echo.
echo Close the terminal windows to stop the services
echo.
pause 