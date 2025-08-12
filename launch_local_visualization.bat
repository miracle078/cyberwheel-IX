@echo off
REM Cyberwheel Local Visualization Launcher for Windows
REM Run this from Z:\home\projects\cyberwheel

echo 🎯 CYBERWHEEL LOCAL VISUALIZATION LAUNCHER
echo ==========================================

cd /d Z:\home\projects\cyberwheel

echo 📊 Checking data availability...
if exist cyberwheel\data\runs (
    echo ✅ Training data found
) else (
    echo ❌ Training data not found in cyberwheel\data\runs
)

if exist cyberwheel\data\graphs (
    echo ✅ Visualization data found
) else (
    echo ❌ Visualization data not found in cyberwheel\data\graphs
)

echo.
echo 🚀 LAUNCHING SERVICES...
echo ========================

echo Starting TensorBoard on port 6006...
start "TensorBoard" cmd /k "tensorboard --logdir=cyberwheel/data/runs --port=6006"

timeout /t 3 /nobreak > nul

echo Starting Cyberwheel Interactive Visualizer on port 8050...
start "Cyberwheel Visualizer" cmd /k "python -m cyberwheel visualizer 8050"

timeout /t 3 /nobreak > nul

echo Starting File Browser Dashboard on port 8051...
start "File Browser" cmd /k "python visualization_dashboard.py"

echo.
echo ✅ ALL SERVICES STARTED!
echo =========================
echo.
echo 🌐 OPEN THESE URLS:
echo ===================
echo TensorBoard (Training Metrics): http://localhost:6006
echo Interactive Visualizer (Network Views): http://localhost:8050  
echo File Browser Dashboard: http://localhost:8051
echo.
echo 💡 All services are running in separate windows
echo Close the command windows to stop the services
echo.
pause
