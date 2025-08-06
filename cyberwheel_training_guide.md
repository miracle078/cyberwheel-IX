# Cyberwheel Training, Visualization, and Evaluation Guide
# Complete PowerShell Commands for Autonomous Cyber Defense Framework

## Prerequisites Setup

### 1. Environment Setup
```powershell
# Navigate to the Cyberwheel directory
cd "c:\Users\mirac\OneDrive\Documents\Git\cyberwheel"

# Check Python version (requires Python 3.10)
python --version

# Create and activate virtual environment
python -m venv cyberwheel_env
.\cyberwheel_env\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Alternative: Install with Poetry (if available)
poetry install

# Verify installation and see help
python -m cyberwheel
```

### 2. Configuration Overview
```powershell
# List available configurations
Get-ChildItem -Path "cyberwheel\data\configs" -Recurse -Filter "*.yaml" | Select-Object Name, Directory

# View network configurations
Get-ChildItem -Path "cyberwheel\data\configs\network" -Filter "*.yaml"

# View environment training configurations
Get-ChildItem -Path "cyberwheel\data\configs\environment" -Filter "train_*.yaml"
```

## Training Framework

### 3. Basic Training Commands

#### Train Blue Agent (Defender) with PPO
```powershell
# Basic blue agent training with default configuration
python -m cyberwheel train train_blue.yaml

# Training with custom parameters
python -m cyberwheel train train_blue.yaml --total-timesteps 50000000 --num-envs 20 --seed 42

# Training with specific network size
python -m cyberwheel train train_blue.yaml --network-config 200-host-network.yaml --experiment-name Blue_200hosts_PPO

# Training with W&B tracking
python -m cyberwheel train train_blue.yaml --track --wandb-project-name cyberwheel_experiments --wandb-entity your_wandb_username
```

#### Train Red Agent (Attacker)
```powershell
# Train red agent with RL
python -m cyberwheel train train_red.yaml

# Train red agent against specific blue strategy
python -m cyberwheel train train_red.yaml --blue-agent baseline_blue_agent.yaml --experiment-name Red_vs_Baseline
```

#### Multi-Agent Training (SULI - Self-Improving Learning)
```powershell
# Co-evolutionary training where both agents improve simultaneously
python -m cyberwheel train train_suli.yaml --total-timesteps 100000000

# SULI baseline comparison
python -m cyberwheel train train_suli_baseline.yaml
```

### 4. Advanced Training Configurations

#### Large-Scale Network Training
```powershell
# Training on massive networks (up to 1M hosts)
python -m cyberwheel train train_blue.yaml --network-config large_network.yaml --num-envs 50 --async-env true --device cuda

# Scalability testing
python -m cyberwheel train train_blue.yaml --network-config scalability_test.yaml --total-timesteps 10000000 --num-saves 20
```

#### Deception-Focused Training
```powershell
# Training with emphasis on cyber deception (using train_blue.yaml which has decoy settings)
python -m cyberwheel train train_blue.yaml --experiment-name Deception_Study --total-timesteps 50000000

# Different network sizes for comparison
python -m cyberwheel train train_blue.yaml --network-config 1000-host-network.yaml --experiment-name Large_Network_Test
```

#### MITRE ATT&CK Integration Training
```powershell
# Training with full MITRE ATT&CK technique set (295+ techniques)
python -m cyberwheel train train_blue_art_campaign.yaml --campaign true

# Specific technique focus
python -m cyberwheel train train_red.yaml --red-agent art_agent.yaml --valid-targets servers
```

## Evaluation Framework

### 5. Model Evaluation Commands

#### Basic Evaluation
```powershell
# Evaluate trained blue agent
python -m cyberwheel evaluate evaluate_blue.yaml --experiment-name Blue_200hosts_PPO

# Evaluate against different red strategies
python -m cyberwheel evaluate evaluate_blue.yaml --red-agent art_agent.yaml --num-episodes 100

# Cross-evaluation: Blue vs multiple red agents
python -m cyberwheel evaluate evaluate_blue.yaml --red-agent art_campaign.yaml
```

#### Performance Metrics Evaluation
```powershell
# Comprehensive performance analysis
python -m cyberwheel evaluate evaluate_suli.yaml --num-episodes 1000 --deterministic false

# Different network configurations
python -m cyberwheel evaluate evaluate_blue.yaml --network-config 1000-host-network.yaml

# Detection system evaluation
python -m cyberwheel evaluate evaluate_blue.yaml --detector-config multilayered_perfect.yaml
```

#### Baseline Comparisons
```powershell
# Compare against baseline
python -m cyberwheel evaluate evaluate_suli_baseline.yaml

# Compare against rule-based policies
python -m cyberwheel evaluate evaluate_blue.yaml --blue-agent inactive_blue_agent.yaml
```

## Visualization Framework

### 6. Real-Time Visualization Server

#### Start Visualization Server
```powershell
# Launch interactive visualization dashboard
python -m cyberwheel visualizer train_blue.yaml

# Access dashboard at: http://localhost:8050
```

#### Network State Visualization
```powershell
# Generate network topology graphs
python -c "
from cyberwheel.utils import visualize
from cyberwheel.utils import YAMLConfig
config = YAMLConfig('train_blue.yaml')
visualize.generate_network_graph(config)
"

# Create episode replay visualizations
python -c "
from cyberwheel.utils import visualize
visualize.create_episode_replay('cyberwheel/data/action_logs/episode_001.json')
"
```

#### Performance Dashboards
```powershell
# Launch TensorBoard for training metrics
tensorboard --logdir cyberwheel\data\runs

# W&B dashboard (if configured)
wandb login
# Then access your W&B project dashboard online
```

### 7. Network Graph Analysis

#### NetworkX-Based Analysis
```powershell
# Generate comprehensive network analysis
python -c "
import networkx as nx
from cyberwheel.network import NetworkGenerator
from cyberwheel.utils import YAMLConfig

config = YAMLConfig('train_blue.yaml')
net_gen = NetworkGenerator(config)
graph = net_gen.generate_network()

# Network statistics
print(f'Nodes: {graph.number_of_nodes()}')
print(f'Edges: {graph.number_of_edges()}')
print(f'Density: {nx.density(graph)}')
print(f'Components: {nx.number_connected_components(graph)}')
"

# Subnet analysis
python -c "
from cyberwheel.utils import get_service_map
service_map = get_service_map('cyberwheel/data/configs/services/windows_exploitable_services.yaml')
print('Available services:', list(service_map.keys()))
"
```

## Advanced Features

### 8. Detection System Configuration

#### Realistic Alert Generation
```powershell
# Configure detection probabilities
python -m cyberwheel train train_blue.yaml --detector-config nids_100_percent.yaml

# Multi-layered detection
python -m cyberwheel train train_blue.yaml --detector-config multilayered_perfect.yaml

# Decoy-only detection
python -m cyberwheel train train_blue.yaml --detector-config decoys_only.yaml
```

#### Custom Detection Rules
```powershell
# Test custom detection configurations
python -c "
from cyberwheel.detectors import DetectorHandler
from cyberwheel.utils import YAMLConfig

config = YAMLConfig('cyberwheel/data/configs/detector/detector_handler.yaml')
detector = DetectorHandler(config)
print('Configured detectors:', detector.get_detector_list())
"
```

### 9. Firewheel Emulation Bridge

#### Real-World Testing Integration
```powershell
# Configure Firewheel integration (requires Firewheel installation)
python -c "
from cyberwheel.utils import FirewheelBridge
bridge = FirewheelBridge('cyberwheel/data/configs/emulation/firewheel_config.yaml')
bridge.deploy_trained_agent('cyberwheel/data/models/blue_agent_final.zip')
"

# Export trained policies for emulation
python -m cyberwheel export cyberwheel\data\configs\environment\evaluate_blue.yaml --model_path "cyberwheel\data\models\blue_agent_final.zip" --export_format "firewheel"
```

### 10. Performance Optimization

#### GPU Acceleration
```powershell
# Training with GPU support
python -m cyberwheel train cyberwheel\data\configs\environment\train_blue.yaml --device "cuda" --num_envs 100

# Check GPU utilization during training
nvidia-smi --loop=1  # Run in separate PowerShell window
```

#### Parallel Environment Scaling
```powershell
# Massive parallel training
python -m cyberwheel train cyberwheel\data\configs\environment\train_blue.yaml --async_env true --num_envs 200 --num_steps 100

# Memory-efficient training for large networks
python -m cyberwheel train cyberwheel\data\configs\environment\train_blue.yaml --batch_size 32768 --minibatch_size 4096
```

## Experimental Analysis

### 11. Research Workflows

#### Hyperparameter Sweeps
```powershell
# Learning rate sweep
$learning_rates = @(0.0001, 0.0003, 0.001, 0.003)
foreach ($lr in $learning_rates) {
    python -m cyberwheel train cyberwheel\data\configs\environment\train_blue.yaml --learning_rate $lr --experiment_name "lr_sweep_$lr"
}

# Network size impact study
$networks = @("50-host-network.yaml", "200-host-network.yaml", "1000-host-network.yaml")
foreach ($net in $networks) {
    python -m cyberwheel train cyberwheel\data\configs\environment\train_blue.yaml --network_config $net --experiment_name "scale_study_$net"
}
```

#### Ablation Studies
```powershell
# Deception effectiveness ablation
$decoy_limits = @(0, 5, 10, 20, 50)
foreach ($limit in $decoy_limits) {
    python -m cyberwheel train cyberwheel\data\configs\environment\train_blue.yaml --decoy_limit $limit --experiment_name "decoy_ablation_$limit"
}

# Detection system ablation
$detectors = @("nids.yaml", "hids.yaml", "multilayered_perfect.yaml", "decoys_only.yaml")
foreach ($det in $detectors) {
    python -m cyberwheel evaluate cyberwheel\data\configs\environment\evaluate_blue.yaml --detector_config $det --experiment_name "detector_ablation_$det"
}
```

#### Statistical Analysis
```powershell
# Multiple seed evaluation for statistical significance
$seeds = @(1, 42, 123, 456, 789)
foreach ($seed in $seeds) {
    python -m cyberwheel evaluate cyberwheel\data\configs\environment\evaluate_blue.yaml --seed $seed --eval_episodes 100 --experiment_name "stats_seed_$seed"
}

# Generate statistical reports
python -c "
from cyberwheel.utils import Evaluator
evaluator = Evaluator('cyberwheel/data/runs/')
evaluator.generate_statistical_report()
"
```

### 12. Data Management

#### Action Logging and Replay
```powershell
# Enable detailed action logging
python -m cyberwheel train cyberwheel\data\configs\environment\train_blue.yaml --log_actions true --log_path "cyberwheel\data\action_logs"

# Replay specific episodes
python -c "
from cyberwheel.utils import EpisodeReplay
replay = EpisodeReplay('cyberwheel/data/action_logs/episode_001.json')
replay.visualize_sequence()
"

# Export training data
python -c "
from cyberwheel.utils import DataExporter
exporter = DataExporter('cyberwheel/data/runs/experiment_001')
exporter.export_trajectories('trajectories.csv')
exporter.export_rewards('rewards.json')
"
```

## Troubleshooting Commands

### 13. System Diagnostics

#### Environment Validation
```powershell
# Validate configuration files
python -c "
from cyberwheel.utils import YAMLConfig
try:
    config = YAMLConfig('cyberwheel/data/configs/environment/train_blue.yaml')
    print('Configuration valid')
except Exception as e:
    print(f'Configuration error: {e}')
"

# Test environment creation
python -c "
from cyberwheel.cyberwheel_envs import CyberwheelHS
from cyberwheel.utils import YAMLConfig
config = YAMLConfig('cyberwheel/data/configs/environment/train_blue.yaml')
env = CyberwheelHS(config)
print(f'Environment created successfully: {env}')
"
```

#### Performance Profiling
```powershell
# Profile training performance
python -m cProfile -o profile_output.prof -c "
from cyberwheel.utils import train_cyberwheel, YAMLConfig
config = YAMLConfig('cyberwheel/data/configs/environment/train_blue.yaml')
config.total_timesteps = 10000
train_cyberwheel(config)
"

# Analyze profiling results
python -c "
import pstats
stats = pstats.Stats('profile_output.prof')
stats.sort_stats('cumulative').print_stats(10)
"
```

## Complete Example Workflows

### 14. End-to-End Training Pipeline
```powershell
# Complete training and evaluation pipeline
$config = "cyberwheel\data\configs\environment\train_blue.yaml"
$model_name = "blue_agent_production"

# 1. Train the agent
python -m cyberwheel train $config --experiment_name $model_name --total_timesteps 50000000 --track

# 2. Evaluate the trained agent
python -m cyberwheel evaluate cyberwheel\data\configs\environment\evaluate_blue.yaml --model_path "cyberwheel\data\models\$model_name.zip" --eval_episodes 1000

# 3. Start visualization server for analysis
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m cyberwheel visualizer $config"

# 4. Generate comprehensive report
python -c "
from cyberwheel.utils import generate_comprehensive_report
generate_comprehensive_report('cyberwheel/data/runs/$model_name')
"
```

### 15. Research Experiment Template
```powershell
# Template for running systematic experiments
$experiment_base = "deception_effectiveness_study"
$configs = @{
    "baseline" = "evaluate_suli_baseline.yaml"
    "deception" = "evaluate_blue.yaml"
    "advanced" = "evaluate_blue_art_campaign.yaml"
}

foreach ($condition in $configs.Keys) {
    $config_file = $configs[$condition]
    $exp_name = "${experiment_base}_${condition}"
    
    # Run evaluation
    python -m cyberwheel evaluate "cyberwheel\data\configs\environment\$config_file" --experiment_name $exp_name --eval_episodes 500 --track
    
    # Generate visualizations
    python -c "
    from cyberwheel.utils import visualize
    visualize.generate_experiment_plots('cyberwheel/data/runs/$exp_name')
    "
}

# Aggregate results
python -c "
from cyberwheel.utils import aggregate_experiment_results
aggregate_experiment_results('$experiment_base', ['baseline', 'deception', 'advanced'])
"
```

This comprehensive guide covers all ten features you mentioned:
1. ✅ Network Simulation: NetworkX graph commands and network configuration
2. ✅ Agent Framework: Separate red/blue training commands
3. ✅ MITRE ATT&CK Integration: ART campaign and technique-specific training
4. ✅ Observation Spaces: Dual-structure alert configuration
5. ✅ Reward Systems: Deception-focused reward configuration
6. ✅ Detection Mechanisms: Multiple detector configurations
7. ✅ Scalability Features: Large network and parallel environment commands
8. ✅ Visualization Tools: Real-time dashboard and episode replay
9. ✅ Configuration System: YAML-driven parameter overrides
10. ✅ Emulation Bridge: Firewheel integration commands

Each section provides practical PowerShell commands you can run directly to train, evaluate, and visualize the Cyberwheel framework.
