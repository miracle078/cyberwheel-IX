# Phase 3: Red Agent Training Script
# Comprehensive red agent training with different attack strategies

Write-Host "CYBERWHEEL PHASE 3: RED AGENT MASTERY" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green

# Verify setup
if (-not (Test-Path "cyberwheel" -PathType Container)) {
    Write-Host "ERROR: Not in cyberwheel directory" -ForegroundColor Red
    exit 1
}

Write-Host "`nSTEP 3.1: Basic Red Agent Training" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Training red agent on 15-host network..."
Write-Host "Command: python -m cyberwheel train train_red.yaml --network-config 15-host-network.yaml --total-timesteps 1000000 --experiment-name Phase3_Red_Small --num-envs 10"

python -m cyberwheel train train_red.yaml --network-config 15-host-network.yaml --total-timesteps 1000000 --experiment-name Phase3_Red_Small --num-envs 10
if ($LASTEXITCODE -eq 0) {
    Write-Host "Basic red agent training completed successfully" -ForegroundColor Green
} else {
    Write-Host "Basic red agent training failed" -ForegroundColor Red
    exit 1
}

Write-Host "`nSTEP 3.2: Advanced Red Agent Training" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Training red agent on larger network..."
Write-Host "Command: python -m cyberwheel train train_red.yaml --network-config 50-host-network.yaml --total-timesteps 2000000 --experiment-name Phase3_Red_Medium --num-envs 8"

python -m cyberwheel train train_red.yaml --network-config 50-host-network.yaml --total-timesteps 2000000 --experiment-name Phase3_Red_Medium --num-envs 8
if ($LASTEXITCODE -eq 0) {
    Write-Host "Advanced red agent training completed successfully" -ForegroundColor Green
} else {
    Write-Host "Advanced red agent training failed" -ForegroundColor Red
    exit 1
}

Write-Host "`nSTEP 3.3: Red Agent Strategy Analysis" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Evaluating different red agent strategies..."

# Test different red agent configs if available
$redConfigs = Get-ChildItem -Path "cyberwheel\data\configs\red_agent" -Name "*.yaml"
foreach ($config in $redConfigs) {
    if ($config -ne "art_agent.yaml") {
        $configName = $config.Replace(".yaml", "")
        $expName = "Phase3_Strategy_$configName"
        Write-Host "Testing strategy: $configName"
        Write-Host "Command: python -m cyberwheel train train_red.yaml --network-config 15-host-network.yaml --red-agent $config --total-timesteps 500000 --experiment-name $expName --num-envs 6"
        
        python -m cyberwheel train train_red.yaml --network-config 15-host-network.yaml --red-agent $config --total-timesteps 500000 --experiment-name $expName --num-envs 6
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Strategy $configName completed" -ForegroundColor Green
        } else {
            Write-Host "Strategy $configName failed" -ForegroundColor Yellow
        }
    }
}

Write-Host "`nPHASE 3 COMPLETE!" -ForegroundColor Green
Write-Host "=================" -ForegroundColor Green
Write-Host "Red agent training completed. Ready for Phase 4 (Agent Interaction Analysis)" -ForegroundColor White
Write-Host "Run: .\phase4_interaction_analysis.ps1" -ForegroundColor Yellow
