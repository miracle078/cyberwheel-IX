#!/usr/bin/env python3
"""
Cyberwheel Training Episode Analysis Script
Systematically analyzes and visualizes training episode data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class CyberwheelEpisodeAnalyzer:
    def __init__(self, data_dir="/rds/general/user/moa324/home/projects/cyberwheel/cyberwheel/data"):
        self.data_dir = Path(data_dir)
        self.action_logs_dir = self.data_dir / "action_logs"
        self.graphs_dir = self.data_dir / "graphs"
        self.runs_dir = self.data_dir / "runs"
        
    def load_episode_data(self, experiment_name):
        """Load action log data for a specific experiment"""
        log_file = self.action_logs_dir / f"{experiment_name}.csv"
        if log_file.exists():
            return pd.read_csv(log_file)
        else:
            print(f"No action log found for {experiment_name}")
            return None
    
    def analyze_episode_structure(self, df, experiment_name):
        """Analyze the structure and patterns in episode data"""
        print(f"\n=== EPISODE STRUCTURE ANALYSIS: {experiment_name} ===")
        
        # Basic statistics
        total_episodes = df['episode'].nunique()
        total_steps = len(df)
        avg_episode_length = df.groupby('episode').size().mean()
        
        print(f"Total Episodes: {total_episodes}")
        print(f"Total Steps: {total_steps}")
        print(f"Average Episode Length: {avg_episode_length:.1f} steps")
        
        # Episode length distribution
        episode_lengths = df.groupby('episode').size()
        print(f"Episode Length Range: {episode_lengths.min()} - {episode_lengths.max()} steps")
        
        return {
            'total_episodes': total_episodes,
            'total_steps': total_steps,
            'avg_episode_length': avg_episode_length,
            'episode_lengths': episode_lengths
        }
    
    def analyze_agent_actions(self, df):
        """Analyze red and blue agent action patterns"""
        print(f"\n=== AGENT ACTION ANALYSIS ===")
        
        # Red agent actions
        red_actions = df['red_action_type'].value_counts()
        red_success_rate = df['red_action_success'].mean()
        
        print(f"Red Agent Success Rate: {red_success_rate:.2%}")
        print("Red Agent Action Distribution:")
        for action, count in red_actions.items():
            pct = (count / len(df)) * 100
            print(f"  {action}: {count} ({pct:.1f}%)")
        
        # Blue agent actions
        blue_actions = df['blue_action'].value_counts()
        print("\nBlue Agent Action Distribution:")
        for action, count in blue_actions.items():
            pct = (count / len(df)) * 100
            print(f"  {action}: {count} ({pct:.1f}%)")
        
        # Action success by type
        print("\nRed Action Success Rates by Type:")
        for action_type in df['red_action_type'].unique():
            mask = df['red_action_type'] == action_type
            success_rate = df[mask]['red_action_success'].mean()
            print(f"  {action_type}: {success_rate:.2%}")
        
        return {
            'red_actions': red_actions,
            'blue_actions': blue_actions,
            'red_success_rate': red_success_rate
        }
    
    def analyze_rewards(self, df):
        """Analyze reward patterns and trends"""
        print(f"\n=== REWARD ANALYSIS ===")
        
        total_reward = df['reward'].sum()
        avg_reward = df['reward'].mean()
        reward_std = df['reward'].std()
        
        print(f"Total Cumulative Reward: {total_reward:.1f}")
        print(f"Average Step Reward: {avg_reward:.2f}")
        print(f"Reward Std Deviation: {reward_std:.2f}")
        
        # Episode-level rewards
        episode_rewards = df.groupby('episode')['reward'].sum()
        print(f"Average Episode Reward: {episode_rewards.mean():.1f}")
        print(f"Best Episode Reward: {episode_rewards.max():.1f}")
        print(f"Worst Episode Reward: {episode_rewards.min():.1f}")
        
        # Reward by action type
        print("\nAverage Rewards by Blue Action:")
        blue_action_rewards = df.groupby('blue_action')['reward'].mean().sort_values(ascending=False)
        for action, reward in blue_action_rewards.items():
            print(f"  {action}: {reward:.2f}")
        
        return {
            'total_reward': total_reward,
            'avg_reward': avg_reward,
            'episode_rewards': episode_rewards,
            'blue_action_rewards': blue_action_rewards
        }
    
    def analyze_network_progression(self, df):
        """Analyze how attacks progress through the network"""
        print(f"\n=== NETWORK PROGRESSION ANALYSIS ===")
        
        # Most targeted hosts
        red_targets = df['red_action_dest'].value_counts().head(10)
        print("Most Targeted Hosts (Red Agent):")
        for host, count in red_targets.items():
            print(f"  {host}: {count} attacks")
        
        # Most used attack sources
        red_sources = df['red_action_src'].value_counts().head(10)
        print("\nMost Used Attack Sources:")
        for host, count in red_sources.items():
            print(f"  {host}: {count} attacks launched")
        
        # Blue defense targets
        blue_targets = df['blue_action_target'].value_counts().head(10)
        print("\nMost Defended Subnets (Blue Agent):")
        for subnet, count in blue_targets.items():
            print(f"  {subnet}: {count} defensive actions")
        
        return {
            'red_targets': red_targets,
            'red_sources': red_sources,
            'blue_targets': blue_targets
        }
    
    def analyze_temporal_patterns(self, df):
        """Analyze how strategies evolve over time"""
        print(f"\n=== TEMPORAL PATTERN ANALYSIS ===")
        
        # Episode-by-episode trends
        episode_stats = df.groupby('episode').agg({
            'red_action_success': 'mean',
            'reward': 'sum',
            'step': 'count'
        }).rename(columns={'step': 'episode_length'})
        
        # Learning trends
        early_episodes = episode_stats.head(len(episode_stats)//3)
        late_episodes = episode_stats.tail(len(episode_stats)//3)
        
        print("Learning Progress (Early vs Late Episodes):")
        print(f"  Red Success Rate: {early_episodes['red_action_success'].mean():.2%} → {late_episodes['red_action_success'].mean():.2%}")
        print(f"  Average Episode Reward: {early_episodes['reward'].mean():.1f} → {late_episodes['reward'].mean():.1f}")
        print(f"  Average Episode Length: {early_episodes['episode_length'].mean():.1f} → {late_episodes['episode_length'].mean():.1f}")
        
        return episode_stats
    
    def create_visualizations(self, df, experiment_name, save_plots=True):
        """Create comprehensive visualizations"""
        print(f"\n=== CREATING VISUALIZATIONS ===")
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle(f'Cyberwheel Training Analysis: {experiment_name}', fontsize=16)
        
        # 1. Episode rewards over time
        episode_rewards = df.groupby('episode')['reward'].sum()
        axes[0,0].plot(episode_rewards.index, episode_rewards.values, 'b-', alpha=0.7)
        axes[0,0].set_title('Episode Rewards Over Time')
        axes[0,0].set_xlabel('Episode')
        axes[0,0].set_ylabel('Total Reward')
        axes[0,0].grid(True, alpha=0.3)
        
        # Add trend line
        z = np.polyfit(episode_rewards.index, episode_rewards.values, 1)
        p = np.poly1d(z)
        axes[0,0].plot(episode_rewards.index, p(episode_rewards.index), "r--", alpha=0.8, label=f'Trend: {z[0]:.2f}x + {z[1]:.2f}')
        axes[0,0].legend()
        
        # 2. Red action success over time
        episode_success = df.groupby('episode')['red_action_success'].mean()
        axes[0,1].plot(episode_success.index, episode_success.values, 'r-', alpha=0.7)
        axes[0,1].set_title('Red Agent Success Rate Over Time')
        axes[0,1].set_xlabel('Episode')
        axes[0,1].set_ylabel('Success Rate')
        axes[0,1].set_ylim(0, 1)
        axes[0,1].grid(True, alpha=0.3)
        
        # 3. Action type distributions
        red_actions = df['red_action_type'].value_counts()
        axes[0,2].pie(red_actions.values, labels=red_actions.index, autopct='%1.1f%%')
        axes[0,2].set_title('Red Agent Action Distribution')
        
        # 4. Blue action effectiveness
        blue_action_rewards = df.groupby('blue_action')['reward'].mean().sort_values()
        axes[1,0].barh(range(len(blue_action_rewards)), blue_action_rewards.values)
        axes[1,0].set_yticks(range(len(blue_action_rewards)))
        axes[1,0].set_yticklabels(blue_action_rewards.index)
        axes[1,0].set_title('Blue Action Average Rewards')
        axes[1,0].set_xlabel('Average Reward')
        
        # 5. Episode length distribution
        episode_lengths = df.groupby('episode').size()
        axes[1,1].hist(episode_lengths.values, bins=20, alpha=0.7, edgecolor='black')
        axes[1,1].set_title('Episode Length Distribution')
        axes[1,1].set_xlabel('Episode Length (steps)')
        axes[1,1].set_ylabel('Frequency')
        axes[1,1].grid(True, alpha=0.3)
        
        # 6. Reward distribution
        axes[1,2].hist(df['reward'].values, bins=30, alpha=0.7, edgecolor='black')
        axes[1,2].set_title('Step Reward Distribution')
        axes[1,2].set_xlabel('Reward')
        axes[1,2].set_ylabel('Frequency')
        axes[1,2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_plots:
            output_dir = Path(f"/rds/general/user/moa324/home/projects/cyberwheel/analysis_outputs")
            output_dir.mkdir(exist_ok=True)
            plt.savefig(output_dir / f"{experiment_name}_analysis.png", dpi=300, bbox_inches='tight')
            print(f"Saved visualization to: {output_dir / f'{experiment_name}_analysis.png'}")
        
        plt.show()
    
    def generate_comprehensive_report(self, experiment_name):
        """Generate a complete analysis report for an experiment"""
        print(f"\n{'='*60}")
        print(f"COMPREHENSIVE ANALYSIS: {experiment_name}")
        print(f"{'='*60}")
        
        # Load data
        df = self.load_episode_data(experiment_name)
        if df is None:
            return None
        
        # Run all analyses
        structure_stats = self.analyze_episode_structure(df, experiment_name)
        action_stats = self.analyze_agent_actions(df)
        reward_stats = self.analyze_rewards(df)
        network_stats = self.analyze_network_progression(df)
        temporal_stats = self.analyze_temporal_patterns(df)
        
        # Create visualizations
        self.create_visualizations(df, experiment_name)
        
        # Summary insights
        print(f"\n=== KEY INSIGHTS ===")
        
        # Learning assessment
        if len(temporal_stats) > 1:
            reward_trend = temporal_stats['reward'].corr(temporal_stats.index)
            success_trend = temporal_stats['red_action_success'].corr(temporal_stats.index)
            
            print(f"Learning Trends:")
            print(f"  Reward Correlation with Episode: {reward_trend:.3f}")
            print(f"  Success Rate Correlation with Episode: {success_trend:.3f}")
            
            if reward_trend > 0.1:
                print("  → Blue agent appears to be learning (improving rewards)")
            elif reward_trend < -0.1:
                print("  → Blue agent performance declining over time")
            else:
                print("  → Blue agent performance stable")
        
        # Strategy assessment
        dominant_red_action = action_stats['red_actions'].index[0]
        dominant_blue_action = action_stats['blue_actions'].index[0]
        
        print(f"\nDominant Strategies:")
        print(f"  Red Agent: {dominant_red_action} ({action_stats['red_actions'][dominant_red_action]} uses)")
        print(f"  Blue Agent: {dominant_blue_action} ({action_stats['blue_actions'][dominant_blue_action]} uses)")
        
        # Effectiveness assessment
        best_blue_action = reward_stats['blue_action_rewards'].index[0]
        best_reward = reward_stats['blue_action_rewards'].iloc[0]
        
        print(f"\nMost Effective Blue Action: {best_blue_action} (avg reward: {best_reward:.2f})")
        
        return {
            'structure': structure_stats,
            'actions': action_stats,
            'rewards': reward_stats,
            'network': network_stats,
            'temporal': temporal_stats
        }

def main():
    """Run analysis on available experiments"""
    analyzer = CyberwheelEpisodeAnalyzer()
    
    # Available experiments
    experiments = [
        "Phase1_Validation_HPC_Interactive",
        "Phase2_Blue_HighDecoy_HPC_Interactive", 
        "Phase2_Blue_Medium_HPC_Interactive"
    ]
    
    print("Available experiments for analysis:")
    for i, exp in enumerate(experiments, 1):
        print(f"{i}. {exp}")
    
    # Analyze each experiment
    for experiment in experiments:
        analyzer.generate_comprehensive_report(experiment)
        print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()
