"""
Static Baseline Agent - Simplified Implementation for Comparative Analysis
Author: Miracle Akanmode
Date: August 2025

This implements a static decoy placement strategy as a baseline for comparison
with the RL-based PPO agent. Follows the exact Cyberwheel architecture pattern.
"""

import random
from cyberwheel.blue_agents.blue_agent import BlueAgent, BlueAgentResult
from cyberwheel.reward import RewardMap


class StaticBaselineAgent(BlueAgent):
    """
    Static Baseline Agent - Traditional Fixed Strategy
    
    Implements a simple static strategy for decoy placement:
    - Deploys decoys at regular intervals
    - Uses random subnet selection
    - Removes decoys when at capacity
    
    This represents traditional non-adaptive cybersecurity approaches.
    """
    
    def __init__(self, placement_interval: int = 5, max_decoys: int = 5, seed: int = 42):
        """
        Initialize Static Baseline Agent
        
        Args:
            placement_interval: Steps between placement decisions
            max_decoys: Maximum number of decoys to maintain
            seed: Random seed for reproducibility
        """
        super().__init__()
        self.placement_interval = placement_interval
        self.max_decoys = max_decoys
        self.step_count = 0
        self.deployed_count = 0
        
        random.seed(seed)
        
        # Define available subnets (this would be dynamic in real implementation)
        self.subnets = ['subnet1', 'subnet2', 'subnet3', 'subnet4']
    
    def act(self, action=None) -> BlueAgentResult:
        """
        Static placement decision logic
        
        Returns:
            BlueAgentResult following Cyberwheel convention
        """
        self.step_count += 1
        
        # Only act at specified intervals
        if self.step_count % self.placement_interval != 0:
            return BlueAgentResult("nothing", -1, True, 0)
        
        # Simple logic: deploy if under capacity, remove if at capacity
        if self.deployed_count < self.max_decoys:
            # Deploy decoy on random subnet
            target_subnet = random.choice(self.subnets)
            subnet_id = f"decoy_{self.step_count}_{target_subnet}"
            self.deployed_count += 1
            return BlueAgentResult("deploy_decoy_host", subnet_id, True, 1, target_subnet)
        else:
            # Remove oldest decoy (simulated)
            self.deployed_count -= 1
            return BlueAgentResult("remove_decoy_host", f"remove_{self.step_count}", True, -1)
    
    def get_reward_map(self) -> RewardMap:
        """
        Return reward mapping for static agent actions
        
        Returns:
            RewardMap compatible with Cyberwheel reward system
        """
        return {
            "deploy_decoy_host": (0, 5),   # Small positive for deployment
            "remove_decoy_host": (0, -2),  # Small negative for removal
            "nothing": (0, 0)               # Neutral for no action
        }
    
    def reset(self):
        """Reset agent state for new episode"""
        self.step_count = 0
        self.deployed_count = 0


class RandomBaselineAgent(BlueAgent):
    """
    Random Baseline Agent - Completely Random Actions
    
    This provides the simplest possible baseline by taking random actions.
    Used to establish lower bound for comparison.
    """
    
    def __init__(self, seed: int = 42):
        super().__init__()
        random.seed(seed)
        self.subnets = ['subnet1', 'subnet2', 'subnet3', 'subnet4']
        self.step_count = 0
    
    def act(self, action=None) -> BlueAgentResult:
        """Completely random action selection"""
        self.step_count += 1
        
        # Random choice between actions
        action_choice = random.choice(['deploy', 'remove', 'nothing', 'nothing'])  # Bias toward nothing
        
        if action_choice == 'deploy':
            target_subnet = random.choice(self.subnets)
            subnet_id = f"random_decoy_{self.step_count}_{target_subnet}"
            return BlueAgentResult("deploy_decoy_host", subnet_id, True, 1, target_subnet)
        elif action_choice == 'remove':
            return BlueAgentResult("remove_decoy_host", f"random_remove_{self.step_count}", True, -1)
        else:
            return BlueAgentResult("nothing", -1, True, 0)
    
    def get_reward_map(self) -> RewardMap:
        """Return reward mapping for random agent"""
        return {
            "deploy_decoy_host": (0, 5),
            "remove_decoy_host": (0, -2), 
            "nothing": (0, 0)
        }
    
    def reset(self):
        """Reset agent state"""
        self.step_count = 0


class RuleBaselineAgent(BlueAgent):
    """
    Rule-Based Baseline Agent - Simple IF-THEN Rules
    
    Implements basic rule-based logic similar to traditional cybersecurity systems:
    - Deploy decoys when step count indicates potential threat
    - Remove decoys when resources are scarce
    - Use simple threshold-based decisions
    """
    
    def __init__(self, alert_threshold: int = 3, max_decoys: int = 6):
        super().__init__()
        self.alert_threshold = alert_threshold
        self.max_decoys = max_decoys
        self.step_count = 0
        self.deployed_count = 0
        self.subnets = ['subnet1', 'subnet2', 'subnet3', 'subnet4']
    
    def act(self, action=None) -> BlueAgentResult:
        """Rule-based decision making"""
        self.step_count += 1
        
        # Rule 1: If early in episode, establish baseline defense
        if self.step_count <= 10 and self.deployed_count < 2:
            target_subnet = self.subnets[self.deployed_count % len(self.subnets)]
            subnet_id = f"rule_decoy_{self.step_count}_{target_subnet}"
            self.deployed_count += 1
            return BlueAgentResult("deploy_decoy_host", subnet_id, True, 1, target_subnet)
        
        # Rule 2: If step count suggests heightened activity, deploy more
        if self.step_count % 15 == 0 and self.deployed_count < self.max_decoys:
            target_subnet = random.choice(self.subnets)
            subnet_id = f"rule_decoy_{self.step_count}_{target_subnet}"
            self.deployed_count += 1
            return BlueAgentResult("deploy_decoy_host", subnet_id, True, 1, target_subnet)
        
        # Rule 3: If at capacity, occasionally remove and redeploy
        if self.deployed_count >= self.max_decoys and self.step_count % 20 == 0:
            self.deployed_count -= 1
            return BlueAgentResult("remove_decoy_host", f"rule_remove_{self.step_count}", True, -1)
        
        # Default: No action
        return BlueAgentResult("nothing", -1, True, 0)
    
    def get_reward_map(self) -> RewardMap:
        """Return reward mapping for rule-based agent"""
        return {
            "deploy_decoy_host": (0, 5),
            "remove_decoy_host": (0, -2),
            "nothing": (0, 0)
        }
    
    def reset(self):
        """Reset agent state"""
        self.step_count = 0
        self.deployed_count = 0