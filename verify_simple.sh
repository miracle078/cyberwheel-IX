#!/bin/bash
# Simple Implementation Verification Script
# Checks key files and extracts critical values

echo "CYBERWHEEL IMPLEMENTATION VERIFICATION"
echo "======================================"

echo
echo "=== FILE EXISTENCE CHECK ==="
files=(
    "cyberwheel/cyberwheel_envs/cyberwheel_rl.py"
    "cyberwheel/reward/rl_reward.py"
    "cyberwheel/blue_agents/rl_blue_agent.py"
    "cyberwheel/red_agents/rl_red_agent.py"
    "cyberwheel/data/configs/environment/train_blue.yaml"
    "cyberwheel/data/configs/red_agent/rl_red_agent.yaml"
    "cyberwheel/data/configs/blue_agent/rl_blue_agent.yaml"
    "cyberwheel/data/configs/network/15-host-network.yaml"
    "baseline_comparison_results/results.csv"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file"
    fi
done

echo
echo "=== HYPERPARAMETER EXTRACTION ==="
if [ -f "cyberwheel/data/configs/environment/train_blue.yaml" ]; then
    echo "Gamma value:"
    grep "gamma:" cyberwheel/data/configs/environment/train_blue.yaml || echo "Not found"
    echo "Learning rate:"
    grep "learning_rate:" cyberwheel/data/configs/environment/train_blue.yaml || echo "Not found"
    echo "Total timesteps:"
    grep "total_timesteps:" cyberwheel/data/configs/environment/train_blue.yaml || echo "Not found"
else
    echo "❌ Training config not found"
fi

echo
echo "=== REWARD VALUES EXTRACTION ==="
if [ -f "cyberwheel/data/configs/red_agent/rl_red_agent.yaml" ]; then
    echo "Red agent impact reward:"
    grep -A3 "impact:" cyberwheel/data/configs/red_agent/rl_red_agent.yaml | grep "immediate"
    echo "Red agent discovery reward:"
    grep -A3 "discovery:" cyberwheel/data/configs/red_agent/rl_red_agent.yaml | grep "immediate"
fi

if [ -f "cyberwheel/data/configs/blue_agent/rl_blue_agent.yaml" ]; then
    echo "Blue agent deploy_decoy cost:"
    grep -A3 "deploy_decoy:" cyberwheel/data/configs/blue_agent/rl_blue_agent.yaml | grep "immediate"
fi

echo
echo "=== NETWORK TOPOLOGY CHECK ==="
if [ -f "cyberwheel/data/configs/network/15-host-network.yaml" ]; then
    host_count=$(grep -c "^  [a-zA-Z].*:$" cyberwheel/data/configs/network/15-host-network.yaml)
    echo "Host count: $host_count"
    if [ "$host_count" -eq 15 ]; then
        echo "✅ Network has 15 hosts as claimed"
    else
        echo "⚠️  Expected 15 hosts, found $host_count"
    fi
fi

echo
echo "=== REWARD CALCULATION VERIFICATION ==="
if [ -f "cyberwheel/reward/rl_reward.py" ]; then
    echo "Deception multiplier (should be 10):"
    grep "* 10" cyberwheel/reward/rl_reward.py || echo "Not found in expected format"
    echo "Red success penalty:"
    grep "* -1" cyberwheel/reward/rl_reward.py || echo "Not found in expected format"
fi

echo
echo "=== BASELINE PERFORMANCE CHECK ==="
if [ -f "baseline_comparison_results/results.csv" ]; then
    echo "PPO Performance:"
    grep "PPO_BestProduction" baseline_comparison_results/results.csv | head -1
    echo "Random Performance:"
    grep "RandomBaseline" baseline_comparison_results/results.csv | head -1
else
    echo "❌ Results file not found"
fi

echo
echo "=== STEP FUNCTION VERIFICATION ==="
if [ -f "cyberwheel/cyberwheel_envs/cyberwheel_rl.py" ]; then
    echo "Blue acts first (line should show blue_agent_result first):"
    grep -n "blue_agent_result = self.blue_agent.act" cyberwheel/cyberwheel_envs/cyberwheel_rl.py
    echo "Red acts second:"
    grep -n "red_agent_result = self.red_agent.act" cyberwheel/cyberwheel_envs/cyberwheel_rl.py
    echo "Episode termination on impact:"
    grep -n "impact" cyberwheel/cyberwheel_envs/cyberwheel_rl.py
fi

echo
echo "VERIFICATION COMPLETE"
echo "Check any ⚠️ or ❌ items above for issues to address"
