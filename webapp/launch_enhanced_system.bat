@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo 🛡️ Enhanced Ultimate Biometric Authentication System Launcher
echo ========================================================================
echo.

echo 🔍 Checking system requirements...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
)
echo ✅ Python is installed

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js 14+ and add it to PATH
    pause
    exit /b 1
)
echo ✅ Node.js is installed

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed or not in PATH
    echo Please install npm
    pause
    exit /b 1
)
echo ✅ npm is installed

echo.
echo 📦 Installing Python dependencies...
echo.

REM Install Python dependencies
pip install -r requirements_enhanced.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)
echo ✅ Python dependencies installed

echo.
echo 📦 Installing Node.js dependencies...
echo.

REM Install Node.js dependencies
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)
echo ✅ Node.js dependencies installed

echo.
echo 🗄️ Setting up database...
echo.

REM Initialize the enhanced database
python init_enhanced_db.py
if %errorlevel% neq 0 (
    echo ❌ Failed to initialize database
    echo Please check the error messages above
    pause
    exit /b 1
)
echo ✅ Database initialized

echo.
echo 🧪 Running system tests...
echo.

REM Run system tests
python test_enhanced_system.py
if %errorlevel% neq 0 (
    echo ⚠️  Some tests failed, but continuing with startup
    echo Check the test report for details
) else (
    echo ✅ All tests passed
)

echo.
echo 🚀 Starting Enhanced Ultimate Biometric Authentication System...
echo.

REM Create batch file to start backend
echo @echo off > start_backend.bat
echo echo 🔧 Starting Enhanced Backend Server... >> start_backend.bat
echo python app_enhanced_ultimate.py >> start_backend.bat
echo pause >> start_backend.bat

REM Create batch file to start frontend
echo @echo off > start_frontend.bat
echo echo 🌐 Starting React Frontend... >> start_frontend.bat
echo timeout /t 5 /nobreak >> start_frontend.bat
echo npm run dev >> start_frontend.bat
echo pause >> start_frontend.bat

REM Start backend in new window
echo 🔧 Starting backend server...
start "Enhanced Backend Server" start_backend.bat

REM Wait for backend to start
echo ⏳ Waiting for backend to initialize...
timeout /t 8 /nobreak

REM Start frontend in new window
echo 🌐 Starting frontend server...
start "React Frontend" start_frontend.bat

REM Wait for frontend to start
echo ⏳ Waiting for frontend to initialize...
timeout /t 5 /nobreak

echo.
echo ========================================================================
echo ✅ Enhanced Ultimate Biometric Authentication System Started!
echo ========================================================================
echo.
echo 🌐 Frontend Application: http://localhost:3000
echo 🔗 Backend API:          http://localhost:5000
echo 📊 System Status:        http://localhost:5000/api/system/status
echo.
echo 🔐 Security Levels Available:
echo    • LOW      - Basic authentication (70%% threshold)
echo    • MEDIUM   - Standard security (80%% threshold)
echo    • HIGH     - Advanced security (90%% threshold)
echo    • MAXIMUM  - Military-grade (95%% threshold)
echo.
echo 🧠 AI Algorithms Active:
echo    • Face Recognition: DeepFace, ResNet50, VGG16, InceptionV3
echo    • Fingerprint: HOG, LBP, Gabor, Minutiae
echo    • Fusion: Ensemble multi-algorithm combination
echo.
echo 📋 Usage Instructions:
echo    1. Open your web browser and go to http://localhost:3000
echo    2. Register a new user with face images and fingerprint
echo    3. Select your desired security level
echo    4. Test authentication with single or dual factor
echo    5. View real-time analytics and algorithm performance
echo.
echo 🔧 Troubleshooting:
echo    • If errors occur, check both console windows
echo    • Ensure camera permissions are granted
echo    • Use high-quality images for better accuracy
echo    • Check system requirements in README_ENHANCED.md
echo.
echo 🛑 To stop the system:
echo    • Close both console windows
echo    • Or press Ctrl+C in each window
echo.
echo 📄 For detailed documentation, see README_ENHANCED.md
echo.

REM Open browser automatically
echo 🌐 Opening browser...
timeout /t 3 /nobreak
start http://localhost:3000

echo.
echo 🎉 System is now running! Enjoy your enhanced biometric authentication!
echo.
echo Press any key to exit launcher (system will continue running)...
pause >nul

REM Cleanup temporary files
del start_backend.bat 2>nul
del start_frontend.bat 2>nul

echo.
echo 👋 Launcher exited. System is still running in background windows.
echo.