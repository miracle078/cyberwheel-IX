# Phase 4: Agent Interaction Analysis Script
# Analyze interactions between trained blue and red agents

Write-Host "CYBERWHEEL PHASE 4: AGENT INTERACTION ANALYSIS" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

# Verify setup
if (-not (Test-Path "cyberwheel" -PathType Container)) {
    Write-Host "ERROR: Not in cyberwheel directory" -ForegroundColor Red
    exit 1
}

Write-Host "`nSTEP 4.1: Head-to-Head Evaluation" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Running trained agents against each other..."
Write-Host "Command: python -m cyberwheel evaluate evaluate_interaction.yaml --network-config 15-host-network.yaml --num-episodes 100 --experiment-name Phase4_HeadToHead --visualize --graph-name interaction_analysis"

python -m cyberwheel evaluate evaluate_interaction.yaml --network-config 15-host-network.yaml --num-episodes 100 --experiment-name Phase4_HeadToHead --visualize --graph-name interaction_analysis
if ($LASTEXITCODE -eq 0) {
    Write-Host "Head-to-head evaluation completed successfully" -ForegroundColor Green
} else {
    Write-Host "Head-to-head evaluation failed" -ForegroundColor Red
    exit 1
}

Write-Host "`nSTEP 4.2: Performance Analysis" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host "Analyzing agent performance metrics..."

# Generate performance comparison reports
Write-Host "Command: python -m cyberwheel evaluate evaluate_blue.yaml --network-config 15-host-network.yaml --num-episodes 50 --experiment-name Phase4_Blue_Performance --model-path cyberwheel/data/runs/Phase2_Blue_Small"

python -m cyberwheel evaluate evaluate_blue.yaml --network-config 15-host-network.yaml --num-episodes 50 --experiment-name Phase4_Blue_Performance --model-path cyberwheel/data/runs/Phase2_Blue_Small
if ($LASTEXITCODE -eq 0) {
    Write-Host "Blue agent performance analysis completed" -ForegroundColor Green
} else {
    Write-Host "Blue agent performance analysis failed" -ForegroundColor Yellow
}

Write-Host "`nCommand: python -m cyberwheel evaluate evaluate_red.yaml --network-config 15-host-network.yaml --num-episodes 50 --experiment-name Phase4_Red_Performance --model-path cyberwheel/data/runs/Phase3_Red_Small"

python -m cyberwheel evaluate evaluate_red.yaml --network-config 15-host-network.yaml --num-episodes 50 --experiment-name Phase4_Red_Performance --model-path cyberwheel/data/runs/Phase3_Red_Small
if ($LASTEXITCODE -eq 0) {
    Write-Host "Red agent performance analysis completed" -ForegroundColor Green
} else {
    Write-Host "Red agent performance analysis failed" -ForegroundColor Yellow
}

Write-Host "`nSTEP 4.3: Network Size Scaling" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan
Write-Host "Testing agent performance on different network sizes..."

$networkSizes = @("15-host-network.yaml", "50-host-network.yaml")
foreach ($network in $networkSizes) {
    $networkName = $network.Replace("-host-network.yaml", "")
    $expName = "Phase4_Scaling_$networkName"
    Write-Host "Testing on $networkName hosts..."
    Write-Host "Command: python -m cyberwheel evaluate evaluate_interaction.yaml --network-config $network --num-episodes 25 --experiment-name $expName"
    
    python -m cyberwheel evaluate evaluate_interaction.yaml --network-config $network --num-episodes 25 --experiment-name $expName
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Scaling test on $networkName completed" -ForegroundColor Green
    } else {
        Write-Host "Scaling test on $networkName failed" -ForegroundColor Yellow
    }
}

Write-Host "`nSTEP 4.4: Visualization and Analysis" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "Generating comprehensive visualization data..."
Write-Host "Starting visualization server on port 8050..."
Write-Host "Command: python -m cyberwheel visualizer 8050"

Write-Host "`nVisualization server will start. Open your browser to:"
Write-Host "http://localhost:8050" -ForegroundColor Yellow
Write-Host "`nPress Ctrl+C to stop the server when done reviewing."

# Start visualization server (this will block until user stops it)
python -m cyberwheel visualizer 8050

Write-Host "`nPHASE 4 COMPLETE!" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green
Write-Host "Agent interaction analysis completed. Ready for Phase 5 (Multi-Agent Co-Evolution)" -ForegroundColor White
Write-Host "Run: .\phase5_coevolution.ps1" -ForegroundColor Yellow
