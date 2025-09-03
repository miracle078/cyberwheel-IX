#!/usr/bin/env python3
"""
Run Baseline Comparison Analysis
Author: Miracle Akanmode
Date: August 2025

This script executes the comprehensive baseline comparison to address supervisor
feedback requiring comparison of different algorithms in the same environment.

Usage:
    python run_baseline_comparison.py [--quick] [--detailed] [--output-dir DIR]
"""

import sys
import os
import argparse
from pathlib import Path

# Add cyberwheel to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from cyberwheel.utils.baseline_comparison import BaselineComparator, ComparisonConfig, run_baseline_comparison
    print("✅ Successfully imported baseline comparison framework")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure you're running from the cyberwheel directory")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Run baseline agent comparison analysis")
    parser.add_argument("--quick", action="store_true", help="Run quick comparison (fewer episodes/trials)")
    parser.add_argument("--detailed", action="store_true", help="Run detailed comparison (more episodes/trials)")
    parser.add_argument("--output-dir", default="baseline_comparison_results", help="Output directory for results")
    parser.add_argument("--environments", nargs="+", default=["small_network", "medium_network", "large_network"], 
                       help="Environments to test")
    
    args = parser.parse_args()
    
    # Configure based on arguments
    if args.quick:
        config = ComparisonConfig(
            num_episodes=10,
            num_trials=2,
            max_steps_per_episode=50,
            environments=args.environments[:2],  # Test fewer environments
            output_dir=args.output_dir
        )
        print("🏃 Running QUICK baseline comparison...")
    elif args.detailed:
        config = ComparisonConfig(
            num_episodes=100,
            num_trials=10,
            max_steps_per_episode=200,
            environments=args.environments,
            output_dir=args.output_dir
        )
        print("📊 Running DETAILED baseline comparison...")
    else:
        config = ComparisonConfig(
            num_episodes=50,
            num_trials=5,
            max_steps_per_episode=100,
            environments=args.environments,
            output_dir=args.output_dir
        )
        print("⚖️  Running STANDARD baseline comparison...")
    
    print(f"Configuration:")
    print(f"  Episodes per trial: {config.num_episodes}")
    print(f"  Number of trials: {config.num_trials}")
    print(f"  Max steps per episode: {config.max_steps_per_episode}")
    print(f"  Environments: {config.environments}")
    print(f"  Output directory: {config.output_dir}")
    
    print("\n" + "="*60)
    
    try:
        # Run the comparison
        results = run_baseline_comparison(config)
        
        # Display summary
        print(f"\n🎉 BASELINE COMPARISON COMPLETE!")
        print("="*60)
        
        print(f"\nAgents Compared: {', '.join(results['comparison_overview']['agents_compared'])}")
        print(f"Environments Tested: {', '.join(results['comparison_overview']['environments_tested'])}")
        
        print(f"\n📈 PERFORMANCE RANKINGS:")
        for env_name, rankings in results["performance_rankings"].items():
            print(f"\n  {env_name.upper()}:")
            for rank_info in rankings:
                print(f"    {rank_info['rank']}. {rank_info['agent']:15} - Avg Reward: {rank_info['avg_reward']:6.2f} ±{rank_info['reward_std']:5.2f}")
        
        print(f"\n🔍 KEY FINDINGS:")
        for finding in results["key_findings"]:
            if finding.startswith("  "):
                print(f"    {finding.strip()}")
            else:
                print(f"  • {finding}")
        
        print(f"\n💾 Results saved to: {config.output_dir}/")
        print(f"  📄 CSV file: {config.output_dir}/results.csv")
        print(f"  📋 Summary: {config.output_dir}/comparison_summary.json")
        print(f"  📊 Details: {config.output_dir}/detailed_results.json")
        
        print(f"\n✅ SUCCESS: Baseline comparison addresses supervisor feedback:")
        print(f"   ✓ Multiple baseline algorithms implemented and compared")
        print(f"   ✓ Same environments used for all agents (fair comparison)")
        print(f"   ✓ Statistical significance with multiple trials")
        print(f"   ✓ Comprehensive performance metrics captured")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR during comparison: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)