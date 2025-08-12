# Cyberwheel Training Progress Tracker
# Run this script to check your training progress and get next steps

Write-Host "CYBERWHEEL TRAINING PROGRESS TRACKER" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "cyberwheel" -PathType Container)) {
    Write-Host "ERROR: Not in cyberwheel directory. Please navigate to:" -ForegroundColor Red
    Write-Host "   cd 'c:\Users\mirac\OneDrive\Documents\Git\cyberwheel'" -ForegroundColor Yellow
    exit 1
}

# Function to check if experiment exists
function Test-ExperimentExists($experimentName) {
    $runsPath = "cyberwheel\data\runs"
    if (Test-Path $runsPath) {
        $experiments = Get-ChildItem -Path $runsPath -Directory -Name
        return $experiments -contains $experimentName
    }
    return $false
}

# Function to count experiments matching pattern
function Get-ExperimentCount($pattern) {
    $runsPath = "cyberwheel\data\runs"
    if (Test-Path $runsPath) {
        $experiments = Get-ChildItem -Path $runsPath -Directory -Name | Where-Object { $_ -like $pattern }
        return $experiments.Count
    }
    return 0
}

# Phase 1: System Validation
Write-Host "`nPHASE 1: SYSTEM VALIDATION" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

$phase1Complete = Test-ExperimentExists "Phase1_Validation"
if ($phase1Complete) {
    Write-Host "[COMPLETE] Phase 1" -ForegroundColor Green
    Write-Host "   System validation successful" -ForegroundColor White
} else {
    Write-Host "[INCOMPLETE] Phase 1" -ForegroundColor Red
    Write-Host "   Run: .\start_training_progression.ps1" -ForegroundColor Yellow
}

# Phase 2: Blue Agent Mastery
Write-Host "`nPHASE 2: BLUE AGENT MASTERY" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan

$phase2Count = Get-ExperimentCount "Phase2_*"
if ($phase2Count -gt 0) {
    Write-Host "[IN PROGRESS] Phase 2 - $phase2Count experiments completed" -ForegroundColor Yellow
    Write-Host "   Small network training: $(if (Test-ExperimentExists 'Phase2_Blue_Small') { 'COMPLETE' } else { 'PENDING' })" -ForegroundColor White
    Write-Host "   Medium network training: $(if (Test-ExperimentExists 'Phase2_Blue_Medium') { 'COMPLETE' } else { 'PENDING' })" -ForegroundColor White
    Write-Host "   Hyperparameter tuning: $(if ((Get-ExperimentCount 'Phase2_Hyperparam_*') -gt 0) { 'STARTED' } else { 'PENDING' })" -ForegroundColor White
} else {
    Write-Host "[NOT STARTED] Phase 2" -ForegroundColor Red
    Write-Host "   Next command:" -ForegroundColor Yellow
    Write-Host "   python -m cyberwheel train train_blue.yaml --network-config 15-host-network.yaml --total-timesteps 1000000 --experiment-name Phase2_Blue_Small --num-envs 10" -ForegroundColor White
}

# Phase 3: Red Agent Mastery
Write-Host "`nPHASE 3: RED AGENT MASTERY" -ForegroundColor Cyan
Write-Host "===========================" -ForegroundColor Cyan

$phase3Count = Get-ExperimentCount "Phase3_*"
if ($phase3Count -gt 0) {
    Write-Host "[IN PROGRESS] Phase 3 - $phase3Count experiments completed" -ForegroundColor Yellow
} else {
    Write-Host "[NOT STARTED] Phase 3" -ForegroundColor Gray
    Write-Host "   Complete Phase 2 first" -ForegroundColor Gray
}

# Phase 4: Agent Interaction Analysis
Write-Host "`nPHASE 4: AGENT INTERACTION ANALYSIS" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

$phase4Count = Get-ExperimentCount "Phase4_*"
if ($phase4Count -gt 0) {
    Write-Host "[IN PROGRESS] Phase 4 - $phase4Count experiments completed" -ForegroundColor Yellow
} else {
    Write-Host "[NOT STARTED] Phase 4" -ForegroundColor Gray
    Write-Host "   Complete Phases 2-3 first" -ForegroundColor Gray
}

# Phase 5: Multi-Agent Co-Evolution (SULI)
Write-Host "`nPHASE 5: MULTI-AGENT CO-EVOLUTION" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

$phase5Count = Get-ExperimentCount "Phase5_*"
if ($phase5Count -gt 0) {
    Write-Host "[IN PROGRESS] Phase 5 - $phase5Count experiments completed" -ForegroundColor Yellow
} else {
    Write-Host "[NOT STARTED] Phase 5 (SULI Specialization)" -ForegroundColor Gray
    Write-Host "   Complete Phases 2-4 first" -ForegroundColor Gray
}

# Phase 6: Scalability and Advanced Features
Write-Host "`nPHASE 6: SCALABILITY AND ADVANCED FEATURES" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

$phase6Count = Get-ExperimentCount "Phase6_*"
if ($phase6Count -gt 0) {
    Write-Host "[IN PROGRESS] Phase 6 - $phase6Count experiments completed" -ForegroundColor Yellow
} else {
    Write-Host "[NOT STARTED] Phase 6" -ForegroundColor Gray
    Write-Host "   Complete Phase 5 first" -ForegroundColor Gray
}

# Phase 7: Research Extensions
Write-Host "`nPHASE 7: RESEARCH EXTENSIONS" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

$phase7Count = Get-ExperimentCount "Phase7_*"
if ($phase7Count -gt 0) {
    Write-Host "[IN PROGRESS] Phase 7 - $phase7Count experiments completed" -ForegroundColor Yellow
} else {
    Write-Host "[NOT STARTED] Phase 7" -ForegroundColor Gray
    Write-Host "   Complete Phase 6 first" -ForegroundColor Gray
}

# Summary and Next Steps
Write-Host "`nTRAINING SUMMARY" -ForegroundColor Green
Write-Host "================" -ForegroundColor Green

$totalExperiments = Get-ExperimentCount "*"
Write-Host "`nTotal experiments: $totalExperiments" -ForegroundColor White

# Determine current phase and next action
if (-not $phase1Complete) {
    Write-Host "`nCURRENT STATUS: Setup Required" -ForegroundColor Red
    Write-Host "NEXT ACTION: Run .\start_training_progression.ps1" -ForegroundColor Yellow
} elseif ($phase2Count -eq 0) {
    Write-Host "`nCURRENT STATUS: Ready for Phase 2" -ForegroundColor Yellow
    Write-Host "NEXT ACTION: Start blue agent training" -ForegroundColor Yellow
    Write-Host "COMMAND: python -m cyberwheel train train_blue.yaml --network-config 15-host-network.yaml --total-timesteps 1000000 --experiment-name Phase2_Blue_Small --num-envs 10" -ForegroundColor White
} elseif ($phase3Count -eq 0 -and $phase2Count -ge 2) {
    Write-Host "`nCURRENT STATUS: Ready for Phase 3" -ForegroundColor Yellow
    Write-Host "NEXT ACTION: Start red agent training" -ForegroundColor Yellow
    Write-Host "COMMAND: python -m cyberwheel train train_red.yaml --network-config 15-host-network.yaml --total-timesteps 1000000 --experiment-name Phase3_Red_Small --num-envs 10" -ForegroundColor White
} elseif ($phase4Count -eq 0 -and $phase2Count -ge 2 -and $phase3Count -ge 2) {
    Write-Host "`nCURRENT STATUS: Ready for Phase 4" -ForegroundColor Yellow
    Write-Host "NEXT ACTION: Start agent interaction analysis" -ForegroundColor Yellow
} elseif ($phase5Count -eq 0 -and $phase4Count -ge 1) {
    Write-Host "`nCURRENT STATUS: Ready for Phase 5 (SULI)" -ForegroundColor Yellow
    Write-Host "NEXT ACTION: Start multi-agent co-evolution" -ForegroundColor Yellow
} else {
    Write-Host "`nCURRENT STATUS: Training in progress" -ForegroundColor Green
    Write-Host "Continue with current phase or proceed to next phase" -ForegroundColor White
}

# Recent experiments
Write-Host "`nRECENT EXPERIMENTS" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan

$runsPath = "cyberwheel\data\runs"
if (Test-Path $runsPath) {
    $recentExperiments = Get-ChildItem -Path $runsPath -Directory | Sort-Object LastWriteTime -Descending | Select-Object -First 5
    if ($recentExperiments.Count -gt 0) {
        foreach ($exp in $recentExperiments) {
            Write-Host "  $($exp.Name) ($(($exp.LastWriteTime).ToString('MM/dd HH:mm')))" -ForegroundColor White
        }
    } else {
        Write-Host "  No experiments found" -ForegroundColor Gray
    }
} else {
    Write-Host "  No runs directory found" -ForegroundColor Gray
}

# Available commands
Write-Host "`nUSEFUL COMMANDS" -ForegroundColor Cyan
Write-Host "===============" -ForegroundColor Cyan
Write-Host "Start training:         python -m cyberwheel train [config.yaml]" -ForegroundColor White
Write-Host "Evaluate model:         python -m cyberwheel evaluate [config.yaml]" -ForegroundColor White
Write-Host "Start visualization:    python -m cyberwheel visualizer 8050" -ForegroundColor White
Write-Host "Monitor with TensorBoard: tensorboard --logdir cyberwheel\data\runs" -ForegroundColor White
Write-Host "Check this progress:    .\check_training_progress.ps1" -ForegroundColor White

Write-Host "`nFor detailed strategy, see: cyberwheel_complete_training_strategy.md" -ForegroundColor Green

# System status check
Write-Host "`nSYSTEM STATUS" -ForegroundColor Cyan
Write-Host "=============" -ForegroundColor Cyan

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python: NOT FOUND" -ForegroundColor Red
}

# Check Cyberwheel
try {
    python -m cyberwheel 2>&1 | Out-Null
    Write-Host "Cyberwheel: Module loaded successfully" -ForegroundColor Green
} catch {
    Write-Host "Cyberwheel: Module load failed" -ForegroundColor Red
}

# Check TensorBoard
try {
    tensorboard --version 2>&1 | Out-Null
    Write-Host "TensorBoard: Available" -ForegroundColor Green
} catch {
    Write-Host "TensorBoard: Not available (optional)" -ForegroundColor Yellow
}

Write-Host "`nProgress check complete!" -ForegroundColor Green
