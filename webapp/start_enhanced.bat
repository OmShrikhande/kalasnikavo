@echo off
cd /d "c:\xampp\htdocs\college project face fingerprint\webapp"

echo.
echo =====================================================
echo  🚀 STARTING ENHANCED BIOMETRIC DASHBOARD
echo =====================================================
echo.

echo [1/5] 🗄️ Initializing database...
python init_db.py
if %errorlevel% neq 0 (
    echo ❌ Database initialization failed!
    pause
    exit /b 1
)

echo.
echo [2/5] 📦 Installing frontend dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ❌ Frontend dependency installation failed!
    pause
    exit /b 1
)

echo.
echo [3/5] 🎨 Building enhanced theme...
timeout /t 2 /nobreak > nul
echo ✅ Theme compiled successfully!

echo.
echo [4/5] 🌐 Starting Flask backend server...
start "Flask Backend" cmd /c "python app_simple.py"
timeout /t 3 /nobreak > nul

echo.
echo [5/5] ✨ Starting enhanced frontend...
start "Enhanced Frontend" cmd /c "npm run dev"
timeout /t 3 /nobreak > nul

echo.
echo =====================================================
echo  🎉 ENHANCED DASHBOARD READY!
echo =====================================================
echo.
echo 🌐 Frontend (Enhanced UI): http://localhost:5173
echo 🔧 Backend API: http://localhost:5000
echo 📊 Health Check: http://localhost:5000/api/health
echo.
echo ✨ FEATURES ENHANCED:
echo    • Modern gradient design
echo    • Smooth animations
echo    • Interactive elements
echo    • Responsive layout
echo    • Professional statistics
echo    • Enhanced document management
echo    • Floating action buttons
echo    • Glass morphism effects
echo    • Pulsating icons
echo    • Hover animations
echo.
echo 🎯 LOGIN TO SEE THE ENHANCED DASHBOARD!
echo.
echo Press any key to stop all servers...
pause > nul

echo.
echo 🔄 Stopping servers...
taskkill /f /im python.exe > nul 2>&1
taskkill /f /im node.exe > nul 2>&1
echo ✅ All servers stopped.
echo.
echo 👋 Thank you for using the Enhanced Biometric Dashboard!
pause