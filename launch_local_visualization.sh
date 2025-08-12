#!/bin/bash
# Cyberwheel Local Visualization Launcher for Linux/Mac
# Run this from Z:/home/projects/cyberwheel (or equivalent mount)

echo "🎯 CYBERWHEEL LOCAL VISUALIZATION LAUNCHER"
echo "=========================================="

# Navigate to the cyberwheel directory
cd "$(dirname "$0")"

echo "📊 Checking data availability..."
if [ -d "cyberwheel/data/runs" ]; then
    echo "✅ Training data found"
    runs_count=$(find cyberwheel/data/runs -name "*.tfevents*" | wc -l)
    echo "   Found $runs_count TensorBoard files"
else
    echo "❌ Training data not found in cyberwheel/data/runs"
fi

if [ -d "cyberwheel/data/graphs" ]; then
    echo "✅ Visualization data found"
    viz_count=$(find cyberwheel/data/graphs -name "*.pickle" | wc -l)
    echo "   Found $viz_count visualization snapshots"
else
    echo "❌ Visualization data not found in cyberwheel/data/graphs"
fi

echo
echo "🚀 LAUNCHING SERVICES..."
echo "========================"

echo "Starting TensorBoard on port 6006..."
tensorboard --logdir=cyberwheel/data/runs --port=6006 &
TB_PID=$!

echo "Starting Cyberwheel Interactive Visualizer on port 8050..."
python -m cyberwheel visualizer 8050 &
VIZ_PID=$!

echo "Starting File Browser Dashboard on port 8051..."
python visualization_dashboard.py &
DASH_PID=$!

echo
echo "✅ ALL SERVICES STARTED!"
echo "========================="
echo "TensorBoard PID: $TB_PID"
echo "Visualizer PID: $VIZ_PID"
echo "Dashboard PID: $DASH_PID"
echo
echo "🌐 OPEN THESE URLS:"
echo "==================="
echo "TensorBoard (Training Metrics): http://localhost:6006"
echo "Interactive Visualizer (Network Views): http://localhost:8050"
echo "File Browser Dashboard: http://localhost:8051"
echo
echo "💡 Press Ctrl+C to stop all services"
echo "====================================="

# Wait for all background processes
wait
