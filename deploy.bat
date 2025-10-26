@echo off
REM GradStat Deployment Script for Windows
REM Version: 1.0
REM Date: October 23, 2025

echo.
echo ========================================
echo    GradStat Deployment Script
echo ========================================
echo.

REM Check if running in correct directory
if not exist "frontend" (
    echo ERROR: frontend directory not found
    echo Please run this script from the gradstat root directory
    pause
    exit /b 1
)

if not exist "backend" (
    echo ERROR: backend directory not found
    pause
    exit /b 1
)

if not exist "worker" (
    echo ERROR: worker directory not found
    pause
    exit /b 1
)

REM Step 1: Check prerequisites
echo [Step 1/7] Checking prerequisites...
echo.

where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Node.js is not installed
    pause
    exit /b 1
)
echo [OK] Node.js found

where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: npm is not installed
    pause
    exit /b 1
)
echo [OK] npm found

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not installed
    pause
    exit /b 1
)
echo [OK] Python found

echo.

REM Step 2: Install dependencies
echo [Step 2/7] Installing dependencies...
echo.

echo Installing frontend dependencies...
cd frontend
call npm install --legacy-peer-deps
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Frontend dependency installation failed
    cd ..
    pause
    exit /b 1
)
echo [OK] Frontend dependencies installed
cd ..

echo Installing backend dependencies...
cd backend
call npm install
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Backend dependency installation failed
    cd ..
    pause
    exit /b 1
)
echo [OK] Backend dependencies installed
cd ..

echo Installing worker dependencies...
cd worker
python -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Worker dependency installation failed
    cd ..
    pause
    exit /b 1
)
echo [OK] Worker dependencies installed
cd ..

echo.

REM Step 3: Build frontend
echo [Step 3/7] Building frontend...
echo.

cd frontend
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Frontend build failed
    cd ..
    pause
    exit /b 1
)
echo [OK] Frontend built successfully
cd ..

echo.

REM Step 4: Check for PM2
echo [Step 4/7] Checking process manager...
echo.

where pm2 >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo PM2 not found. Installing PM2...
    call npm install -g pm2
    echo [OK] PM2 installed
) else (
    echo [OK] PM2 found
)

echo.

REM Step 5: Stop existing services
echo [Step 5/7] Stopping existing services...
echo.

call pm2 delete worker 2>nul
call pm2 delete backend 2>nul
call pm2 delete frontend 2>nul
echo [OK] Existing services stopped

echo.

REM Step 6: Start services
echo [Step 6/7] Starting services...
echo.

REM Start worker
cd worker
call pm2 start main.py --name worker --interpreter python
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Worker failed to start
    cd ..
    pause
    exit /b 1
)
echo [OK] Worker started
cd ..

REM Start backend
cd backend
call pm2 start server.js --name backend
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Backend failed to start
    cd ..
    pause
    exit /b 1
)
echo [OK] Backend started
cd ..

REM Serve frontend
cd frontend
call pm2 serve build 3000 --name frontend --spa
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Frontend failed to start
    cd ..
    pause
    exit /b 1
)
echo [OK] Frontend started
cd ..

REM Save PM2 configuration
call pm2 save

echo.

REM Step 7: Verify deployment
echo [Step 7/7] Verifying deployment...
echo.

timeout /t 5 /nobreak >nul

call pm2 list

echo.
echo ========================================
echo    Deployment Complete!
echo ========================================
echo.
echo Next Steps:
echo   1. Access the application at: http://localhost:3000
echo   2. Backend API available at: http://localhost:3001
echo   3. Worker API available at: http://localhost:8001
echo.
echo Useful Commands:
echo   - View logs: pm2 logs
echo   - Restart all: pm2 restart all
echo   - Stop all: pm2 stop all
echo   - Monitor: pm2 monit
echo.
echo Documentation: See DEPLOYMENT_GUIDE.md for more details
echo.

pause
