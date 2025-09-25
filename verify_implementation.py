#!/usr/bin/env python3
"""
Verification Script for Cyberwheel Implementation
Validates key claims from comprehensive report against actual implementation
"""

import yaml
import pandas as pd
import numpy as np
from pathlib import Path

def verify_hyperparameters():
    """Verify training hyperparameters match report claims"""
    print("=== HYPERPARAMETER VERIFICATION ===")
    
    config_path = Path("cyberwheel/data/configs/environment/train_blue.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        print(f"Gamma (discount factor): {config.get('gamma', 'NOT FOUND')}")
        print(f"Learning rate: {config.get('learning_rate', 'NOT FOUND')}")
        print(f"GAE lambda: {config.get('gae_lambda', 'NOT FOUND')}")
        print(f"Clip coefficient: {config.get('clip_coef', 'NOT FOUND')}")
        print(f"Number of environments: {config.get('num_envs', 'NOT FOUND')}")
        print(f"Total timesteps: {config.get('total_timesteps', 'NOT FOUND')}")
        
        # Check for discrepancies
        if config.get('gamma') != 0.95:
            print(f"⚠️  DISCREPANCY: Report claims γ=0.95, implementation uses γ={config.get('gamma')}")
        else:
            print("✅ Gamma value matches report")
    else:
        print("❌ Training config file not found")
    print()

def verify_reward_values():
    """Verify reward values in agent configurations"""
    print("=== REWARD VALUE VERIFICATION ===")
    
    # Red agent rewards
    red_config_path = Path("cyberwheel/data/configs/red_agent/rl_red_agent.yaml")
    if red_config_path.exists():
        with open(red_config_path, 'r') as f:
            red_config = yaml.safe_load(f)
        
        print("Red Agent Rewards:")
        for action, details in red_config.get('actions', {}).items():
            immediate = details.get('reward', {}).get('immediate', 0)
            recurring = details.get('reward', {}).get('recurring', 0)
            print(f"  {action}: immediate={immediate}, recurring={recurring}")
    
    # Blue agent rewards
    blue_config_path = Path("cyberwheel/data/configs/blue_agent/rl_blue_agent.yaml")
    if blue_config_path.exists():
        with open(blue_config_path, 'r') as f:
            blue_config = yaml.safe_load(f)
        
        print("\nBlue Agent Rewards:")
        for action, details in blue_config.get('actions', {}).items():
            immediate = details.get('reward', {}).get('immediate', 0)
            recurring = details.get('reward', {}).get('recurring', 0)
            print(f"  {action}: immediate={immediate}, recurring={recurring}")
    print()

def analyze_baseline_performance():
    """Analyze baseline comparison results"""
    print("=== BASELINE PERFORMANCE ANALYSIS ===")
    
    results_path = Path("baseline_comparison_results/results.csv")
    if results_path.exists():
        df = pd.read_csv(results_path)
        
        # Group by agent and calculate statistics
        stats = df.groupby('Agent')['Avg_Reward_Per_Episode'].agg(['mean', 'std', 'median']).round(2)
        
        print("Performance Summary (Avg Reward Per Episode):")
        print(stats)
        
        # Check for concerning patterns
        ppo_performance = stats.loc['PPO_BestProduction', 'mean']
        random_performance = stats.loc['RandomBaseline', 'mean']
        
        if random_performance > ppo_performance:
            print(f"\n⚠️  CONCERN: Random baseline ({random_performance:.2f}) outperforms PPO ({ppo_performance:.2f})")
            print(f"   Random std dev: {stats.loc['RandomBaseline', 'std']:.2f}")
            print(f"   PPO std dev: {stats.loc['PPO_BestProduction', 'std']:.2f}")
            print("   High variance in random agent may explain higher mean")
        else:
            print(f"\n✅ PPO ({ppo_performance:.2f}) outperforms Random ({random_performance:.2f})")
            
    else:
        print("❌ Baseline results file not found")
    print()

def verify_network_configuration():
    """Verify network topology claims"""
    print("=== NETWORK TOPOLOGY VERIFICATION ===")
    
    network_config_path = Path("cyberwheel/data/configs/network/15-host-network.yaml")
    if network_config_path.exists():
        with open(network_config_path, 'r') as f:
            network_config = yaml.safe_load(f)
        
        host_count = len(network_config.get('hosts', {}))
        print(f"Total hosts in network: {host_count}")
        
        if host_count == 15:
            print("✅ Network topology matches 15-host claim")
        else:
            print(f"⚠️  DISCREPANCY: Expected 15 hosts, found {host_count}")
            
        # Count by type
        host_types = {}
        for host_name, host_config in network_config.get('hosts', {}).items():
            host_type = host_config.get('type', 'unknown')
            host_types[host_type] = host_types.get(host_type, 0) + 1
        
        print("Host distribution by type:")
        for host_type, count in host_types.items():
            print(f"  {host_type}: {count}")
    else:
        print("❌ Network config file not found")
    print()

def check_implementation_completeness():
    """Check if key implementation files exist"""
    print("=== IMPLEMENTATION COMPLETENESS CHECK ===")
    
    key_files = [
        "cyberwheel/cyberwheel_envs/cyberwheel_rl.py",
        "cyberwheel/reward/rl_reward.py", 
        "cyberwheel/blue_agents/rl_blue_agent.py",
        "cyberwheel/red_agents/rl_red_agent.py",
        "cyberwheel/blue_agents/baseline_agents.py"
    ]
    
    for file_path in key_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
    print()

def main():
    """Run complete verification"""
    print("CYBERWHEEL IMPLEMENTATION VERIFICATION")
    print("=" * 50)
    
    verify_hyperparameters()
    verify_reward_values()
    analyze_baseline_performance()
    verify_network_configuration()
    check_implementation_completeness()
    
    print("VERIFICATION COMPLETE")
    print("Review any ⚠️  or ❌ items above for viva preparation")

if __name__ == "__main__":
    main()
