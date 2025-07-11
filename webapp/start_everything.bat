@echo off
cd /d "c:\xampp\htdocs\college project face fingerprint\webapp"

echo =====================================================
echo  STARTING BIOMETRIC AUTHENTICATION SYSTEM
echo =====================================================

echo.
echo [1/4] Initializing database...
python init_db.py
if %errorlevel% neq 0 (
    echo Database initialization failed!
    pause
    exit /b 1
)

echo.
echo [2/4] Installing frontend dependencies...
npm install
if %errorlevel% neq 0 (
    echo Frontend dependency installation failed!
    pause
    exit /b 1
)

echo.
echo [3/4] Starting Flask backend server...
start "Flask Backend" python app_simple.py

echo.
echo [4/4] Starting frontend development server...
timeout /t 3 /nobreak > nul
start "Frontend" npm run dev

echo.
echo =====================================================
echo  SYSTEM STARTED SUCCESSFULLY!
echo =====================================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Press any key to stop all servers...
pause > nul

echo.
echo Stopping servers...
taskkill /f /im python.exe > nul 2>&1
taskkill /f /im node.exe > nul 2>&1
echo All servers stopped.
pause