# Cyberwheel Training Episode Visualization Analysis Guide

## Overview
This guide helps you systematically understand and interpret the training episode visualizations in the cyberwheel multi-agent reinforcement learning framework.

## Data Structure Understanding

### 1. Data Organization
```
cyberwheel/data/
├── runs/           # TensorBoard training logs (23MB)
├── action_logs/    # Episode action sequences (130KB CSV files)
├── graphs/         # Network state snapshots (385MB pickle files)
├── models/         # Trained agent models (13MB)
├── configs/        # Configuration files
└── notebooks/      # Analysis notebooks
```

### 2. Key Experiments Available
- **Phase1_Validation**: Basic validation runs
- **Phase2_Blue_HighDecoy**: High decoy deployment strategy
- **Phase2_Blue_Medium**: Medium complexity scenarios
- **Phase2_Blue_PerfectDetection**: Perfect detection capability tests
- **Phase2_Blue_Small**: Small network scenarios

## Understanding Episode Data

### 3. Action Log Structure
Each CSV file contains:
- **episode**: Episode number (0-indexed)
- **step**: Time step within episode
- **red_action_success**: Whether red agent action succeeded
- **red_action_type**: Type of attack (pingsweep, portscan, discovery, lateral-movement)
- **red_action_src**: Source host for red action
- **red_action_dest**: Target host for red action
- **blue_action**: Blue agent defensive action type
- **blue_action_id**: Unique identifier for blue action
- **blue_action_target**: Target subnet/host for blue action
- **reward**: Immediate reward received

### 4. Network Graph Snapshots
- Files named `{episode}_{step}.pickle` contain network state at each step
- These capture:
  - Host compromise status
  - Decoy deployment locations
  - Network topology changes
  - Agent positions and capabilities

### 5. TensorBoard Metrics
Located in `runs/` directories, track:
- Episode rewards over time
- Action success rates
- Network compromise statistics
- Learning curves and convergence

## Interpretation Framework

### 6. Red Agent Behavior Analysis
**Attack Progression Patterns:**
1. **Reconnaissance Phase**: pingsweep, discovery actions
2. **Scanning Phase**: portscan actions to find vulnerabilities
3. **Exploitation Phase**: lateral-movement between compromised hosts

**Success Indicators:**
- High `red_action_success` rates indicate effective attack strategies
- Progression from outer network to internal hosts shows lateral movement success

### 7. Blue Agent Defensive Strategies
**Primary Actions:**
- **deploy_decoy**: Strategic placement of honeypots
- **isolate_host**: Network segmentation responses
- **restore_host**: Recovery operations

**Effectiveness Measures:**
- Reward trends (higher rewards = better defense)
- Decoy interaction rates (red agents caught by decoys)
- Time to contain attacks

### 8. SULI (Self-play Uniform Learning Initialization) Analysis
Key metrics to track:
- **Decoy compromise rates**: How often red agents interact with decoys
- **Learning convergence**: Both agents improving simultaneously
- **Strategy diversity**: Variety in action sequences

## Visualization Techniques

### 9. Episode Flow Analysis
For each episode, track:
1. **Initial network state** (step 0)
2. **Attack vector progression** (red actions sequence)
3. **Defensive responses** (blue actions timing)
4. **Network state evolution** (compromise spread)
5. **Episode outcome** (final rewards, containment success)

### 10. Temporal Patterns
Analyze across episodes:
- **Learning curves**: Reward improvements over episodes
- **Strategy evolution**: How action patterns change
- **Convergence indicators**: When strategies stabilize

### 11. Network Security Metrics
Track network-level statistics:
- **Compromise rate**: Percentage of hosts compromised per episode
- **Containment time**: Steps from first attack to successful defense
- **Decoy effectiveness**: Red agent deception success rate

## Key Analysis Questions

### 12. Performance Evaluation
- Are blue agents successfully learning to deploy decoys strategically?
- Do red agents adapt to blue defensive strategies?
- What network topologies favor defenders vs attackers?

### 13. Strategy Assessment
- Which attack paths are most successful?
- Where are decoys most effective?
- How does network size affect learning dynamics?

### 14. SULI Effectiveness
- Do both agents improve simultaneously?
- Is the self-play creating diverse, realistic scenarios?
- Are the learned strategies transferable to new networks?

## Analysis Workflow

### 15. Step-by-Step Analysis Process
1. **Load episode data** from action logs
2. **Visualize episode flows** (attack progression, defensive responses)
3. **Analyze reward trends** from TensorBoard logs
4. **Examine network states** from pickle files
5. **Correlate strategies** with outcomes
6. **Identify learning patterns** across episodes

### 16. Recommended Visualizations
- **Episode timeline plots**: Actions vs steps with color-coded success
- **Network topology views**: Host compromise status over time
- **Reward curve analysis**: Learning progress tracking
- **Heat maps**: Most targeted hosts/subnets
- **Strategy frequency plots**: Action type distributions

## Tools and Scripts

### 17. Available Analysis Tools
- **visualization_dashboard.py**: Interactive data browser
- **TensorBoard**: Built-in training metrics viewer
- **Network graph utilities**: In cyberwheel.network module
- **Custom analysis scripts**: Can be created for specific metrics

### 18. Getting Started Commands
```bash
# Start TensorBoard for training metrics
tensorboard --logdir cyberwheel/data/runs/

# Run visualization dashboard
python cyberwheel/visualization_dashboard.py

# Load episode data for custom analysis
import pandas as pd
df = pd.read_csv('cyberwheel/data/action_logs/Phase2_Blue_HighDecoy_HPC_Interactive.csv')
```

This framework provides a systematic approach to understanding your cyberwheel training results and extracting meaningful insights about multi-agent cybersecurity learning.
