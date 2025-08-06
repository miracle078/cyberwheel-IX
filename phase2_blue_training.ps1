# Phase 2: Blue Agent Training Script
# Advanced blue agent training with multiple network sizes and hyperparameter tuning

Write-Host "CYBERWHEEL PHASE 2: BLUE AGENT MASTERY" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green

# Verify setup
if (-not (Test-Path "cyberwheel" -PathType Container)) {
    Write-Host "ERROR: Not in cyberwheel directory" -ForegroundColor Red
    exit 1
}

Write-Host "`nSTEP 2.1: Small Network Training" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Training blue agent on 15-host network..."
Write-Host "Command: python -m cyberwheel train train_blue.yaml --network-config 15-host-network.yaml --total-timesteps 1000000 --experiment-name Phase2_Blue_Small --num-envs 10"

$result = python -m cyberwheel train train_blue.yaml --network-config 15-host-network.yaml --total-timesteps 1000000 --experiment-name Phase2_Blue_Small --num-envs 10
if ($LASTEXITCODE -eq 0) {
    Write-Host "Small network training completed successfully" -ForegroundColor Green
} else {
    Write-Host "Small network training failed" -ForegroundColor Red
    exit 1
}

Write-Host "`nSTEP 2.2: Medium Network Training" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Training blue agent on 50-host network..."
Write-Host "Command: python -m cyberwheel train train_blue.yaml --network-config 50-host-network.yaml --total-timesteps 2000000 --experiment-name Phase2_Blue_Medium --num-envs 8"

$result = python -m cyberwheel train train_blue.yaml --network-config 50-host-network.yaml --total-timesteps 2000000 --experiment-name Phase2_Blue_Medium --num-envs 8
if ($LASTEXITCODE -eq 0) {
    Write-Host "Medium network training completed successfully" -ForegroundColor Green
} else {
    Write-Host "Medium network training failed" -ForegroundColor Red
    exit 1
}

Write-Host "`nSTEP 2.3: Hyperparameter Optimization" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Learning rate experiments
$learningRates = @("1e-4", "2.5e-4", "5e-4")
foreach ($lr in $learningRates) {
    Write-Host "Testing learning rate: $lr"
    $expName = "Phase2_Hyperparam_LR_$($lr.Replace('-', '').Replace('.', ''))"
    Write-Host "Command: python -m cyberwheel train train_blue.yaml --network-config 15-host-network.yaml --total-timesteps 500000 --experiment-name $expName --learning-rate $lr --num-envs 6"
    
    $result = python -m cyberwheel train train_blue.yaml --network-config 15-host-network.yaml --total-timesteps 500000 --experiment-name $expName --learning-rate $lr --num-envs 6
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Learning rate $lr experiment completed" -ForegroundColor Green
    } else {
        Write-Host "Learning rate $lr experiment failed" -ForegroundColor Yellow
    }
}

Write-Host "`nPHASE 2 COMPLETE!" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green
Write-Host "Blue agent training completed. Ready for Phase 3 (Red Agent Training)" -ForegroundColor White
Write-Host "Run: .\phase3_red_training.ps1" -ForegroundColor Yellow
