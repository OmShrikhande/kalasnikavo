@echo off
echo 🚀 Starting Enhanced Ultimate Biometric Authentication System
echo.

echo 📦 Installing Python dependencies...
pip install flask flask-cors werkzeug numpy opencv-python scikit-learn scikit-image pandas matplotlib tensorflow deepface pillow scipy

echo.
echo 🗄️ Initializing database...
python init_db.py

echo.
echo 🔧 Starting Enhanced Backend...
start "Enhanced Backend" python app_enhanced_ultimate.py

echo.
echo ⏳ Waiting for backend to initialize...
timeout /t 5 /nobreak

echo.
echo 🌐 Starting Frontend...
start "Frontend" npm run dev

echo.
echo ✅ System started successfully!
echo.
echo 📍 Access the application at: http://localhost:3000
echo 🔗 Backend API at: http://localhost:5000
echo.
echo Press any key to exit...
pause