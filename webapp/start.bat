@echo off
title Advanced Biometric Authentication System - God Mode
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║    🔐 Advanced Dual Biometric Authentication System          ║
echo ║                     GOD MODE LAUNCHER                       ║
echo ║                                                              ║
echo ║    🚀 Ultimate Security • 🎨 Modern UI • 📊 Analytics       ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔧 Initializing system components...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found! Please install Node.js 16+ first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

REM Create necessary directories
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups
if not exist "temp" mkdir temp

echo 📁 Directories created
echo.

echo 🐍 Starting Backend Server...
echo    Backend will be available at: http://localhost:5000
start "Biometric Auth Backend" cmd /k "python app_enhanced.py"

echo ⏳ Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

echo 📦 Starting Frontend Development Server...
echo    Frontend will be available at: http://localhost:5173
start "Biometric Auth Frontend" cmd /k "npm run dev"

echo.
echo 🎉 System startup initiated!
echo.
echo 🌐 Access URLs:
echo    Frontend: http://localhost:5173
echo    Backend:  http://localhost:5000
echo    API Docs: http://localhost:5000/api/health
echo.
echo 📊 Features Available:
echo    ✅ Dual Biometric Authentication (Face + Fingerprint)
echo    ✅ Real-time Security Monitoring
echo    ✅ Advanced Analytics Dashboard
echo    ✅ Document Management System
echo    ✅ Multi-level Security Settings
echo    ✅ Behavioral Analysis
echo    ✅ Device Fingerprinting
echo    ✅ Geolocation Tracking
echo    ✅ Session Management
echo    ✅ Audit Trail & Logging
echo.
echo 🔒 Security Levels:
echo    • Basic (60%% threshold)
echo    • Standard (75%% threshold)  
echo    • Enhanced (85%% threshold)
echo    • Maximum (95%% threshold)
echo.
echo 💡 Tips:
echo    • Use good lighting for face capture
echo    • Ensure high-quality fingerprint images (.bmp format)
echo    • Check browser permissions for camera access
echo    • Monitor security events in the dashboard
echo.
echo ⚠️  Important Notes:
echo    • Change default secrets in .env file for production
echo    • Configure SSL certificates for HTTPS
echo    • Review security settings in config.json
echo    • Backup database regularly
echo.
echo Press any key to open the application in your browser...
pause > nul

REM Open browser to the application
start http://localhost:5173

echo.
echo 🚀 Application launched successfully!
echo.
echo To stop the system:
echo    1. Close this window
echo    2. Close the Backend and Frontend windows
echo    3. Or press Ctrl+C in each terminal
echo.
echo 📚 For help and documentation, see README.md
echo.
pause