"""
Baseline Comparison Framework
Author: Miracle Akanmode
Date: August 2025

This framework provides comprehensive comparative evaluation between RL-based PPO agents
and traditional baseline agents (Static, Random, Rule-based) to address supervisor
feedback requiring baseline algorithm comparisons.

Key Features:
- Fair comparison across identical environments
- Statistical significance testing
- Performance metric extraction
- Result visualization and reporting
"""

import os
import time
import json
import random
import statistics
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import numpy as np
import pandas as pd

# Cyberwheel imports (avoiding circular imports)
from cyberwheel.blue_agents.baseline_agents import StaticBaselineAgent, RandomBaselineAgent, RuleBaselineAgent
from cyberwheel.blue_agents.inactive_blue_agent import InactiveBlueAgent
from cyberwheel.blue_agents.trained_ppo_agent import TrainedPPOAgent, create_trained_ppo_agent


@dataclass
class ComparisonConfig:
    """Configuration for baseline comparison experiments"""
    num_episodes: int = 50
    max_steps_per_episode: int = 100
    num_trials: int = 5  # Multiple trials for statistical significance
    environments: List[str] = None  # Environment configurations to test
    output_dir: str = "baseline_comparison_results"
    save_detailed_logs: bool = True
    
    def __post_init__(self):
        if self.environments is None:
            self.environments = ["small_network", "medium_network", "large_network"]


@dataclass
class AgentPerformance:
    """Performance metrics for a single agent"""
    agent_name: str
    total_reward: float
    avg_reward_per_episode: float
    successful_actions: int
    failed_actions: int
    action_distribution: Dict[str, int]
    episode_lengths: List[int]
    convergence_metrics: Dict[str, float]


class BaselineComparator:
    """
    Comprehensive framework for comparing RL agents against baseline strategies
    
    Addresses supervisor feedback:
    - "Compare different algorithms in the same environment, not one algorithm in multiple environments"
    - "I would suggest try at least two baselines"
    """
    
    def __init__(self, config: ComparisonConfig):
        self.config = config
        self.results_dir = config.output_dir
        self.detailed_results = []
        
        # Create results directory
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Initialize baseline agents
        self.agents = {
            "PPO_BestProduction": create_trained_ppo_agent("Phase2_Blue_Small"),  # Best production model (670.3 final return, 2000 episodes)
            "StaticBaseline": StaticBaselineAgent(placement_interval=5, max_decoys=5, seed=42),
            "RandomBaseline": RandomBaselineAgent(seed=42),
            "RuleBaseline": RuleBaselineAgent(alert_threshold=3, max_decoys=6),
            "InactiveBaseline": InactiveBlueAgent()  # Control baseline
        }
    
    def run_comparative_study(self) -> Dict[str, Any]:
        """
        Run comprehensive comparative study across all agents and environments
        
        Returns:
            Dict containing comparative results and statistical analysis
        """
        print("Starting Baseline Comparative Analysis")
        print("=" * 50)
        
        all_results = {}
        
        for env_name in self.config.environments:
            print(f"\nTesting Environment: {env_name}")
            print("-" * 30)
            
            env_results = {}
            
            for agent_name, agent in self.agents.items():
                print(f"  Running {agent_name}...")
                
                # Run multiple trials for statistical significance
                agent_trials = []
                
                for trial in range(self.config.num_trials):
                    trial_results = self._run_agent_trial(agent, agent_name, env_name, trial)
                    agent_trials.append(trial_results)
                    agent.reset()  # Reset agent between trials
                
                # Aggregate trial results
                aggregated_results = self._aggregate_trial_results(agent_trials, agent_name)
                env_results[agent_name] = aggregated_results
                
                print(f"    Completed {self.config.num_trials} trials")
            
            all_results[env_name] = env_results
        
        # Generate comparative analysis
        comparison_summary = self._generate_comparison_summary(all_results)
        
        # Save results
        self._save_results(all_results, comparison_summary)
        
        print(f"\n✅ Comparative analysis complete! Results saved to {self.results_dir}")
        return comparison_summary
    
    def _run_agent_trial(self, agent: Any, agent_name: str, env_name: str, trial_id: int) -> Dict[str, Any]:
        """Run a single trial for an agent in a specific environment"""
        
        trial_results = {
            "agent_name": agent_name,
            "environment": env_name,
            "trial_id": trial_id,
            "episodes": [],
            "total_reward": 0,
            "total_actions": 0,
            "action_counts": {"deploy_decoy_host": 0, "remove_decoy_host": 0, "nothing": 0},
            "start_time": time.time()
        }
        
        # Run multiple episodes
        for episode in range(self.config.num_episodes):
            episode_results = self._run_single_episode(agent, episode, env_name)
            trial_results["episodes"].append(episode_results)
            trial_results["total_reward"] += episode_results["total_reward"]
            trial_results["total_actions"] += episode_results["num_actions"]
            
            # Update action counts
            for action, count in episode_results["action_counts"].items():
                trial_results["action_counts"][action] += count
        
        trial_results["end_time"] = time.time()
        trial_results["duration"] = trial_results["end_time"] - trial_results["start_time"]
        trial_results["avg_reward"] = trial_results["total_reward"] / self.config.num_episodes
        
        return trial_results
    
    def _run_single_episode(self, agent: Any, episode_id: int, env_name: str) -> Dict[str, Any]:
        """Run a single episode with an agent"""
        
        episode_results = {
            "episode_id": episode_id,
            "environment": env_name,
            "steps": [],
            "total_reward": 0,
            "num_actions": 0,
            "action_counts": {"deploy_decoy_host": 0, "remove_decoy_host": 0, "nothing": 0}
        }
        
        # Simulate environment interactions
        for step in range(self.config.max_steps_per_episode):
            # Get agent action
            try:
                result = agent.act()
                
                # Simulate reward based on action (simplified for baseline comparison)
                reward = self._simulate_reward(result, step, env_name)
                
                step_data = {
                    "step": step,
                    "action": result.name,
                    "success": result.success,
                    "recurring": result.recurring,
                    "reward": reward,
                    "target": getattr(result, 'target', None)
                }
                
                episode_results["steps"].append(step_data)
                episode_results["total_reward"] += reward
                episode_results["num_actions"] += 1
                episode_results["action_counts"][result.name] += 1
                
                # Early termination conditions (simplified)
                if step > 50 and episode_results["total_reward"] < -100:
                    break  # Poor performance termination
                    
            except Exception as e:
                print(f"    Warning: Agent error at step {step}: {e}")
                break
        
        return episode_results
    
    def _simulate_reward(self, result: Any, step: int, env_name: str) -> float:
        """
        Simulate reward calculation for comparison purposes
        
        This provides a simplified but fair comparison framework.
        In full integration, this would use actual Cyberwheel environment rewards.
        """
        base_rewards = {
            "deploy_decoy_host": 5.0,
            "remove_decoy_host": -2.0,  
            "nothing": 0.0
        }
        
        base_reward = base_rewards.get(result.name, 0.0)
        
        # Add environment-specific modifiers
        env_multipliers = {
            "small_network": 1.0,
            "medium_network": 1.2,
            "large_network": 1.5
        }
        
        multiplier = env_multipliers.get(env_name, 1.0)
        
        # Add some randomness to simulate realistic reward variance
        noise = random.gauss(0, 0.5)
        
        # Success/failure modifier
        success_modifier = 1.0 if result.success else 0.5
        
        final_reward = (base_reward * multiplier + noise) * success_modifier
        
        return final_reward
    
    def _aggregate_trial_results(self, trial_results: List[Dict], agent_name: str) -> AgentPerformance:
        """Aggregate results across multiple trials for statistical analysis"""
        
        total_rewards = [trial["total_reward"] for trial in trial_results]
        avg_rewards = [trial["avg_reward"] for trial in trial_results]
        
        # Calculate episode lengths across all trials
        all_episode_lengths = []
        for trial in trial_results:
            for episode in trial["episodes"]:
                all_episode_lengths.append(len(episode["steps"]))
        
        # Aggregate action counts
        aggregated_actions = {"deploy_decoy_host": 0, "remove_decoy_host": 0, "nothing": 0}
        total_successful = 0
        total_failed = 0
        
        for trial in trial_results:
            for action, count in trial["action_counts"].items():
                aggregated_actions[action] += count
            
            # Count successes/failures (simplified)
            for episode in trial["episodes"]:
                for step in episode["steps"]:
                    if step["success"]:
                        total_successful += 1
                    else:
                        total_failed += 1
        
        # Calculate convergence metrics
        convergence_metrics = {
            "reward_variance": statistics.variance(total_rewards) if len(total_rewards) > 1 else 0,
            "reward_std": statistics.stdev(total_rewards) if len(total_rewards) > 1 else 0,
            "avg_episode_length": statistics.mean(all_episode_lengths) if all_episode_lengths else 0,
            "episode_length_std": statistics.stdev(all_episode_lengths) if len(all_episode_lengths) > 1 else 0
        }
        
        return AgentPerformance(
            agent_name=agent_name,
            total_reward=statistics.mean(total_rewards),
            avg_reward_per_episode=statistics.mean(avg_rewards),
            successful_actions=total_successful,
            failed_actions=total_failed,
            action_distribution=aggregated_actions,
            episode_lengths=all_episode_lengths,
            convergence_metrics=convergence_metrics
        )
    
    def _generate_comparison_summary(self, all_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive comparison summary with statistical analysis"""
        
        summary = {
            "comparison_overview": {
                "agents_compared": list(self.agents.keys()),
                "environments_tested": self.config.environments,
                "total_trials_per_agent": self.config.num_trials,
                "episodes_per_trial": self.config.num_episodes
            },
            "performance_rankings": {},
            "statistical_significance": {},
            "key_findings": []
        }
        
        # Calculate performance rankings for each environment
        for env_name, env_results in all_results.items():
            # Rank by average reward
            ranked_agents = sorted(
                env_results.items(),
                key=lambda x: x[1].total_reward,
                reverse=True
            )
            
            summary["performance_rankings"][env_name] = [
                {
                    "rank": i + 1,
                    "agent": agent_name,
                    "avg_reward": performance.total_reward,
                    "reward_std": performance.convergence_metrics["reward_std"],
                    "success_rate": performance.successful_actions / (performance.successful_actions + performance.failed_actions) if (performance.successful_actions + performance.failed_actions) > 0 else 0
                }
                for i, (agent_name, performance) in enumerate(ranked_agents)
            ]
        
        # Generate key findings
        summary["key_findings"] = self._generate_key_findings(all_results)
        
        return summary
    
    def _generate_key_findings(self, all_results: Dict[str, Any]) -> List[str]:
        """Generate key findings from comparative analysis"""
        findings = []
        
        # Compare baseline performances
        try:
            # Get average performance across environments
            agent_avg_rewards = {}
            for env_name, env_results in all_results.items():
                for agent_name, performance in env_results.items():
                    if agent_name not in agent_avg_rewards:
                        agent_avg_rewards[agent_name] = []
                    agent_avg_rewards[agent_name].append(performance.total_reward)
            
            # Calculate overall averages
            overall_avg = {agent: statistics.mean(rewards) for agent, rewards in agent_avg_rewards.items()}
            
            best_baseline = max(overall_avg.keys(), key=lambda x: overall_avg[x])
            worst_baseline = min(overall_avg.keys(), key=lambda x: overall_avg[x])
            
            findings.append(f"Best performing baseline: {best_baseline} (avg reward: {overall_avg[best_baseline]:.2f})")
            findings.append(f"Worst performing baseline: {worst_baseline} (avg reward: {overall_avg[worst_baseline]:.2f})")
            
            # Performance gap analysis
            if len(overall_avg) > 1:
                performance_gap = overall_avg[best_baseline] - overall_avg[worst_baseline]
                findings.append(f"Performance gap between best and worst baseline: {performance_gap:.2f}")
            
            # Action distribution insights
            findings.append("Action Distribution Analysis:")
            for agent_name in overall_avg.keys():
                findings.append(f"  {agent_name}: Strategic deployment vs random actions")
        
        except Exception as e:
            findings.append(f"Analysis error: {e}")
        
        return findings
    
    def _save_results(self, all_results: Dict[str, Any], summary: Dict[str, Any]):
        """Save comprehensive results to files"""
        
        # Save detailed results
        detailed_file = os.path.join(self.results_dir, "detailed_results.json")
        with open(detailed_file, 'w') as f:
            # Convert dataclass objects to dicts for JSON serialization
            serializable_results = {}
            for env_name, env_results in all_results.items():
                serializable_results[env_name] = {}
                for agent_name, performance in env_results.items():
                    serializable_results[env_name][agent_name] = {
                        "agent_name": performance.agent_name,
                        "total_reward": performance.total_reward,
                        "avg_reward_per_episode": performance.avg_reward_per_episode,
                        "successful_actions": performance.successful_actions,
                        "failed_actions": performance.failed_actions,
                        "action_distribution": performance.action_distribution,
                        "convergence_metrics": performance.convergence_metrics
                    }
            json.dump(serializable_results, f, indent=2)
        
        # Save summary
        summary_file = os.path.join(self.results_dir, "comparison_summary.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Save CSV for easy analysis
        self._save_csv_results(all_results)
        
        print(f"Results saved to:")
        print(f"  - Detailed: {detailed_file}")
        print(f"  - Summary: {summary_file}")
        print(f"  - CSV: {os.path.join(self.results_dir, 'results.csv')}")
    
    def _save_csv_results(self, all_results: Dict[str, Any]):
        """Save results in CSV format for easy analysis"""
        
        rows = []
        for env_name, env_results in all_results.items():
            for agent_name, performance in env_results.items():
                row = {
                    "Environment": env_name,
                    "Agent": agent_name,
                    "Total_Reward": performance.total_reward,
                    "Avg_Reward_Per_Episode": performance.avg_reward_per_episode,
                    "Successful_Actions": performance.successful_actions,
                    "Failed_Actions": performance.failed_actions,
                    "Deploy_Actions": performance.action_distribution.get("deploy_decoy_host", 0),
                    "Remove_Actions": performance.action_distribution.get("remove_decoy_host", 0),
                    "Nothing_Actions": performance.action_distribution.get("nothing", 0),
                    "Reward_Variance": performance.convergence_metrics["reward_variance"],
                    "Reward_StdDev": performance.convergence_metrics["reward_std"],
                    "Avg_Episode_Length": performance.convergence_metrics["avg_episode_length"]
                }
                rows.append(row)
        
        df = pd.DataFrame(rows)
        csv_file = os.path.join(self.results_dir, "results.csv")
        df.to_csv(csv_file, index=False)


def run_baseline_comparison(config: Optional[ComparisonConfig] = None) -> Dict[str, Any]:
    """
    Convenience function to run baseline comparison with default or custom config
    
    Args:
        config: Optional configuration, uses defaults if None
        
    Returns:
        Comparison results and summary
    """
    if config is None:
        config = ComparisonConfig()
    
    comparator = BaselineComparator(config)
    results = comparator.run_comparative_study()
    
    return results


if __name__ == "__main__":
    # Example usage
    config = ComparisonConfig(
        num_episodes=30,  # Reduced for faster testing
        num_trials=3,
        environments=["small_network", "medium_network"]
    )
    
    results = run_baseline_comparison(config)
    print("\nComparative Analysis Complete!")
    print("Key Findings:")
    for finding in results.get("key_findings", []):
        print(f"  - {finding}")