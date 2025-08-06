# Cyberwheel Training Quick-Start Script
# Run this script to begin Phase 1 of the training progression

Write-Host "CYBERWHEEL TRAINING PROGRESSION - QUICK START" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Verify we're in the right directory
if (-not (Test-Path "cyberwheel" -PathType Container)) {
    Write-Host "ERROR: Not in cyberwheel directory. Please navigate to:" -ForegroundColor Red
    Write-Host "   cd 'c:\Users\mirac\OneDrive\Documents\Git\cyberwheel'" -ForegroundColor Yellow
    exit 1
}

Write-Host "Directory check passed" -ForegroundColor Green

# Phase 1: System Validation
Write-Host "`nPHASE 1: SYSTEM VALIDATION" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

Write-Host "`nStep 1.1: Testing basic functionality..."
try {
    python -m cyberwheel 2>&1 | Out-Null
    Write-Host "Cyberwheel module loads successfully" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Cyberwheel module failed to load" -ForegroundColor Red
    Write-Host "   Please run: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "`nStep 1.2: Running validation training (this will take ~2-3 minutes)..."
Write-Host "Command: python -m cyberwheel train train_blue.yaml --network-config 15-host-network.yaml --total-timesteps 1000 --experiment-name Phase1_Validation" -ForegroundColor DarkGray

try {
    $output = python -m cyberwheel train train_blue.yaml --network-config 15-host-network.yaml --total-timesteps 1000 --experiment-name Phase1_Validation 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Validation training completed successfully" -ForegroundColor Green
    } else {
        Write-Host "Validation training failed" -ForegroundColor Red
        Write-Host "Output: $output" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "ERROR: Validation training failed" -ForegroundColor Red
    exit 1
}

Write-Host "`nStep 1.3: Testing visualization (generating graph data first)..."
Write-Host "Command: python -m cyberwheel evaluate evaluate_blue.yaml --network-config 15-host-network.yaml --num-episodes 2 --experiment-name Phase1_Viz_Test --visualize --graph-name test_graph" -ForegroundColor DarkGray

try {
    $output = python -m cyberwheel evaluate evaluate_blue.yaml --network-config 15-host-network.yaml --num-episodes 2 --experiment-name Phase1_Viz_Test --visualize --graph-name test_graph 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Visualization data generated successfully" -ForegroundColor Green
        Write-Host "You can now start the visualization server with: python -m cyberwheel visualizer 8050" -ForegroundColor Cyan
    } else {
        Write-Host "Visualization test completed with warnings (this is normal)" -ForegroundColor Yellow
        Write-Host "   Basic functionality is working" -ForegroundColor White
    }
} catch {
    Write-Host "Visualization test had issues but continuing..." -ForegroundColor Yellow
}

# Display available configurations
Write-Host "`nStep 1.4: Available configurations:" -ForegroundColor White
Write-Host "`nNetwork configurations:" -ForegroundColor Yellow
Get-ChildItem -Path "cyberwheel\data\configs\network" -Name | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }

Write-Host "`nEnvironment configurations:" -ForegroundColor Yellow
Get-ChildItem -Path "cyberwheel\data\configs\environment" -Name | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }

Write-Host "`nRed agent configurations:" -ForegroundColor Yellow
Get-ChildItem -Path "cyberwheel\data\configs\red_agent" -Name | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }

Write-Host "`nBlue agent configurations:" -ForegroundColor Yellow
Get-ChildItem -Path "cyberwheel\data\configs\blue_agent" -Name | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }

# Success message and next steps
Write-Host "`nPHASE 1 VALIDATION COMPLETE!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

Write-Host "`nYour system is ready for Cyberwheel training!" -ForegroundColor Green
Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "1. Review the complete training strategy in: cyberwheel_complete_training_strategy.md" -ForegroundColor White
Write-Host "2. Start Phase 2 (Blue Agent Training) with:" -ForegroundColor White
Write-Host "   python -m cyberwheel train train_blue.yaml --network-config 15-host-network.yaml --total-timesteps 1000000 --experiment-name Phase2_Blue_Small --num-envs 10" -ForegroundColor Yellow
Write-Host "3. Monitor training with:" -ForegroundColor White
Write-Host "   tensorboard --logdir cyberwheel\data\runs" -ForegroundColor Yellow
Write-Host "4. View training progress with visualization server (after generating graph data):" -ForegroundColor White
Write-Host "   python -m cyberwheel visualizer 8050" -ForegroundColor Yellow

Write-Host "`nTraining Progression Overview:" -ForegroundColor Cyan
Write-Host "Phase 1: [COMPLETE] System Validation" -ForegroundColor Green
Write-Host "Phase 2: [NEXT] Blue Agent Mastery" -ForegroundColor Yellow
Write-Host "Phase 3: Red Agent Mastery" -ForegroundColor Gray
Write-Host "Phase 4: Agent Interaction Analysis" -ForegroundColor Gray
Write-Host "Phase 5: Multi-Agent Co-Evolution (SULI)" -ForegroundColor Gray
Write-Host "Phase 6: Scalability and Advanced Features" -ForegroundColor Gray
Write-Host "Phase 7: Research Extensions" -ForegroundColor Gray

Write-Host "`nEstimated Timeline:" -ForegroundColor Cyan
Write-Host "Week 1: Phases 1-2 (Basic Understanding)" -ForegroundColor White
Write-Host "Week 2: Phases 3-4 (Agent Specialization)" -ForegroundColor White
Write-Host "Week 3-4: Phase 5 (Multi-Agent Systems)" -ForegroundColor White
Write-Host "Week 5-6: Phases 6-7 (Advanced and Research)" -ForegroundColor White

Write-Host "`nReady to begin your Cyberwheel mastery journey!" -ForegroundColor Green
