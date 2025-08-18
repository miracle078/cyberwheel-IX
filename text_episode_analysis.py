#!/usr/bin/env python3
"""
Simplified Cyberwheel Training Episode Analysis (Text Only)
"""

import pandas as pd
import numpy as np
from pathlib import Path

class CyberwheelTextAnalyzer:
    def __init__(self, data_dir="/rds/general/user/moa324/home/projects/cyberwheel/cyberwheel/data"):
        self.data_dir = Path(data_dir)
        self.action_logs_dir = self.data_dir / "action_logs"
    
    def analyze_experiment(self, experiment_name):
        """Comprehensive text-based analysis"""
        print(f"\n{'='*80}")
        print(f"CYBERWHEEL EPISODE ANALYSIS: {experiment_name}")
        print(f"{'='*80}")
        
        # Load data
        log_file = self.action_logs_dir / f"{experiment_name}.csv"
        if not log_file.exists():
            print(f"❌ No data found for {experiment_name}")
            return None
            
        df = pd.read_csv(log_file)
        
        # 1. DATASET OVERVIEW
        print(f"\n📊 DATASET OVERVIEW")
        print(f"{'─'*40}")
        total_episodes = df['episode'].nunique()
        total_steps = len(df)
        avg_episode_length = df.groupby('episode').size().mean()
        episode_lengths = df.groupby('episode').size()
        
        print(f"Episodes: {total_episodes}")
        print(f"Total Steps: {total_steps}")
        print(f"Avg Episode Length: {avg_episode_length:.1f} steps")
        print(f"Episode Length Range: {episode_lengths.min()} - {episode_lengths.max()} steps")
        
        # 2. RED AGENT ANALYSIS
        print(f"\n🔴 RED AGENT (ATTACKER) ANALYSIS")
        print(f"{'─'*40}")
        
        red_success_rate = df['red_action_success'].mean()
        print(f"Overall Success Rate: {red_success_rate:.1%}")
        
        # Action distribution with success rates
        print(f"\nAttack Actions:")
        red_actions = df['red_action_type'].value_counts()
        for action, count in red_actions.items():
            pct = (count / len(df)) * 100
            success_rate = df[df['red_action_type'] == action]['red_action_success'].mean()
            print(f"  {action:20} {count:3d} uses ({pct:4.1f}%) - {success_rate:.1%} success")
        
        # Most targeted hosts
        print(f"\nMost Targeted Hosts:")
        targets = df['red_action_dest'].value_counts().head(8)
        for host, count in targets.items():
            print(f"  {host:35} {count:2d} attacks")
        
        # Attack sources (lateral movement analysis)
        print(f"\nAttack Launch Points:")
        sources = df['red_action_src'].value_counts().head(6)
        for host, count in sources.items():
            print(f"  {host:35} {count:2d} attacks launched")
        
        # 3. BLUE AGENT ANALYSIS
        print(f"\n🔵 BLUE AGENT (DEFENDER) ANALYSIS")
        print(f"{'─'*40}")
        
        blue_actions = df['blue_action'].value_counts()
        print(f"Defensive Actions:")
        for action, count in blue_actions.items():
            pct = (count / len(df)) * 100
            avg_reward = df[df['blue_action'] == action]['reward'].mean()
            print(f"  {action:20} {count:3d} uses ({pct:4.1f}%) - avg reward: {avg_reward:6.2f}")
        
        # Defense targets
        print(f"\nMost Defended Locations:")
        def_targets = df['blue_action_target'].value_counts().head(8)
        for subnet, count in def_targets.items():
            print(f"  {subnet:25} {count:2d} defensive actions")
        
        # 4. REWARD ANALYSIS
        print(f"\n💰 REWARD ANALYSIS")
        print(f"{'─'*40}")
        
        total_reward = df['reward'].sum()
        avg_reward = df['reward'].mean()
        episode_rewards = df.groupby('episode')['reward'].sum()
        
        print(f"Total Cumulative Reward: {total_reward:8.1f}")
        print(f"Average Step Reward: {avg_reward:11.2f}")
        print(f"Average Episode Reward: {episode_rewards.mean():6.1f}")
        print(f"Best Episode: {episode_rewards.max():16.1f}")
        print(f"Worst Episode: {episode_rewards.min():15.1f}")
        
        # Reward trends
        if total_episodes > 2:
            early_rewards = episode_rewards.head(total_episodes//3).mean()
            late_rewards = episode_rewards.tail(total_episodes//3).mean()
            improvement = late_rewards - early_rewards
            print(f"Learning Trend: {early_rewards:.1f} → {late_rewards:.1f} ({improvement:+.1f})")
        
        # 5. STRATEGY PATTERNS
        print(f"\n🎯 STRATEGY PATTERNS")
        print(f"{'─'*40}")
        
        # Dominant strategies
        dominant_red = red_actions.index[0] if len(red_actions) > 0 else "None"
        dominant_blue = blue_actions.index[0] if len(blue_actions) > 0 else "None"
        
        print(f"Dominant Red Strategy: {dominant_red}")
        print(f"Dominant Blue Strategy: {dominant_blue}")
        
        # Check for specific patterns
        decoy_actions = df[df['blue_action'] == 'deploy_decoy']
        decoy_limit_exceeded = (df['blue_action_id'] == 'decoy_limit_exceeded').sum()
        lateral_moves = df[df['red_action_type'] == 'lateral-movement']
        
        if len(decoy_actions) > 0:
            print(f"Decoy Deployment: {len(decoy_actions)} attempts, {decoy_limit_exceeded} limit exceeded")
        
        if len(lateral_moves) > 0:
            lateral_success = lateral_moves['red_action_success'].mean()
            print(f"Lateral Movement Success: {lateral_success:.1%}")
        
        # 6. LEARNING ASSESSMENT
        print(f"\n🧠 LEARNING ASSESSMENT")
        print(f"{'─'*40}")
        
        if total_episodes > 1:
            # Calculate correlations with episode number
            episode_stats = df.groupby('episode').agg({
                'red_action_success': 'mean',
                'reward': 'sum',
                'step': 'count'
            })
            
            reward_trend = episode_stats['reward'].corr(pd.Series(episode_stats.index))
            success_trend = episode_stats['red_action_success'].corr(pd.Series(episode_stats.index))
            
            print(f"Reward Trend Correlation: {reward_trend:8.3f}")
            print(f"Red Success Trend: {success_trend:13.3f}")
            
            if reward_trend > 0.3:
                print("✅ Strong positive learning trend (Blue improving)")
            elif reward_trend > 0.1:
                print("📈 Moderate positive learning trend")
            elif reward_trend < -0.3:
                print("❌ Strong negative trend (Blue declining)")
            elif reward_trend < -0.1:
                print("📉 Moderate negative trend")
            else:
                print("➡️  Stable performance (no clear trend)")
        
        # 7. KEY INSIGHTS
        print(f"\n🔍 KEY INSIGHTS")
        print(f"{'─'*40}")
        
        insights = []
        
        # Red agent assessment
        if red_success_rate > 0.8:
            insights.append("🚨 Red agent highly successful - consider stronger defenses")
        elif red_success_rate < 0.5:
            insights.append("🛡️  Blue defenses effective against red attacks")
        
        # Blue agent assessment
        if avg_reward > 0:
            insights.append("💪 Blue agent achieving positive rewards overall")
        else:
            insights.append("⚠️  Blue agent struggling (negative average rewards)")
        
        # Episode length assessment
        if avg_episode_length < 20:
            insights.append("⚡ Short episodes - quick resolutions")
        elif avg_episode_length > 50:
            insights.append("🔄 Long episodes - extended engagements")
        
        # Decoy effectiveness
        if len(decoy_actions) > 0 and decoy_limit_exceeded < len(decoy_actions) * 0.5:
            insights.append("🎭 Decoy strategy appears well-managed")
        elif decoy_limit_exceeded > len(decoy_actions) * 0.7:
            insights.append("🚫 Frequent decoy limit exceeded - need better placement strategy")
        
        for insight in insights:
            print(f"  {insight}")
        
        return df

def main():
    """Run text-based analysis on all available experiments"""
    analyzer = CyberwheelTextAnalyzer()
    
    # Available experiments
    experiments = [
        "Phase1_Validation_HPC_Interactive",
        "Phase2_Blue_HighDecoy_HPC_Interactive", 
        "Phase2_Blue_Medium_HPC_Interactive"
    ]
    
    print("🎮 CYBERWHEEL TRAINING EPISODE ANALYSIS")
    print("="*80)
    
    results = {}
    for experiment in experiments:
        results[experiment] = analyzer.analyze_experiment(experiment)
    
    # Cross-experiment comparison
    print(f"\n🔄 CROSS-EXPERIMENT COMPARISON")
    print(f"{'='*80}")
    
    valid_results = {k: v for k, v in results.items() if v is not None}
    
    if len(valid_results) > 1:
        print(f"\nExperiment Performance Summary:")
        for exp_name, df in valid_results.items():
            if df is not None:
                total_reward = df['reward'].sum()
                red_success = df['red_action_success'].mean()
                episodes = df['episode'].nunique()
                print(f"  {exp_name:35} | Episodes: {episodes:2d} | Total Reward: {total_reward:8.1f} | Red Success: {red_success:.1%}")

if __name__ == "__main__":
    main()
