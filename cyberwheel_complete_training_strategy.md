# Cyberwheel Complete Training Strategy
# Progressive Learning Path from Basics to Advanced Extensions

## 🎯 **OVERVIEW: Complete Training Progression**

This strategy takes you through 7 phases of training, from basic understanding to advanced research-ready implementations. Each phase builds on the previous one, ensuring you master all components before extending the framework.

---

## 📋 **PHASE 1: Environment Setup & System Validation**
*Objective: Ensure everything works and understand the basic components*

### **Step 1.1: Initial Setup**
```powershell
# Navigate to project directory
cd "c:\Users\mirac\OneDrive\Documents\Git\cyberwheel"

# Verify Python environment
python --version  # Should be 3.10.x

# Install dependencies
pip install -r requirements.txt

# Test basic functionality
python -m cyberwheel  # Should show help without errors
```

### **Step 1.2: Component Validation Tests**
```powershell
# Test small network creation (quick validation) - NOTE: Use 15-host instead of 10-host due to YAML format issue
python -m cyberwheel train train_blue.yaml --network-config 15-host-network.yaml --total-timesteps 1000 --experiment-name Phase1_Validation

# Verify evaluation works
python -m cyberwheel evaluate evaluate_blue.yaml --network-config 15-host-network.yaml --num-episodes 5 --experiment-name Phase1_Eval_Test

# Test visualization server (NOTE: Requires graph data first)
# First generate some visualization data:
python -m cyberwheel evaluate evaluate_blue.yaml --network-config 15-host-network.yaml --num-episodes 2 --experiment-name Phase1_Viz_Test --visualize --graph-name test_graph

# Then start visualization server
python -m cyberwheel visualizer 8050
# Verify http://localhost:8050 opens successfully, then stop server (Ctrl+C)
```

### **Step 1.3: Configuration Understanding**
```powershell
# Explore available configurations
Get-ChildItem -Path "cyberwheel\data\configs" -Recurse -Filter "*.yaml" | Select-Object Name, Directory

# View network sizes
Get-ChildItem -Path "cyberwheel\data\configs\network" -Name

# Check available agents
Get-ChildItem -Path "cyberwheel\data\configs\red_agent" -Name
Get-ChildItem -Path "cyberwheel\data\configs\blue_agent" -Name
```

**✅ Phase 1 Complete When:**
- All test commands run without errors
- Visualization server loads successfully
- You understand the directory structure and available configurations

---

## 🔵 **PHASE 2: Blue Agent (Defender) Mastery**
*Objective: Master defensive agent training across different scenarios*

### **Step 2.1: Basic Blue Agent Training**
```powershell
# Small network training (15 minutes)
python -m cyberwheel train train_blue.yaml --network-config 15-host-network.yaml --total-timesteps 1000000 --experiment-name Phase2_Blue_Small --num-envs 10

# Medium network training (1-2 hours)
python -m cyberwheel train train_blue.yaml --network-config 200-host-network.yaml --total-timesteps 10000000 --experiment-name Phase2_Blue_Medium --num-envs 20

# Monitor training progress
tensorboard --logdir cyberwheel\data\runs\Phase2_Blue_Medium
```

### **Step 2.2: Deception Strategy Variations**
```powershell
# High deception limit training
python -m cyberwheel train train_blue.yaml --network-config 200-host-network.yaml --total-timesteps 5000000 --experiment-name Phase2_Blue_HighDecoy --decoy-limit 10

# Different objectives
python -m cyberwheel train train_blue.yaml --network-config 200-host-network.yaml --total-timesteps 5000000 --experiment-name Phase2_Blue_Detect --objective detect

python -m cyberwheel train train_blue.yaml --network-config 200-host-network.yaml --total-timesteps 5000000 --experiment-name Phase2_Blue_Downtime --objective downtime
```

### **Step 2.3: Detection System Variations**
```powershell
# Perfect detection training
python -m cyberwheel train train_blue.yaml --detector-config multilayered_perfect.yaml --total-timesteps 5000000 --experiment-name Phase2_Blue_PerfectDetection

# NIDS only detection
python -m cyberwheel train train_blue.yaml --detector-config nids_100_percent.yaml --total-timesteps 5000000 --experiment-name Phase2_Blue_NIDSOnly

# Decoy-only detection
python -m cyberwheel train train_blue.yaml --detector-config decoys_only.yaml --total-timesteps 5000000 --experiment-name Phase2_Blue_DecoyOnly
```

### **Step 2.4: Blue Agent Evaluation Suite**
```powershell
# Evaluate all trained blue agents
$experiments = @("Phase2_Blue_Small", "Phase2_Blue_Medium", "Phase2_Blue_HighDecoy", "Phase2_Blue_Detect", "Phase2_Blue_Downtime", "Phase2_Blue_PerfectDetection", "Phase2_Blue_NIDSOnly", "Phase2_Blue_DecoyOnly")

foreach ($exp in $experiments) {
    python -m cyberwheel evaluate evaluate_blue.yaml --experiment-name $exp --num-episodes 100
}
```

**✅ Phase 2 Complete When:**
- You have 8 trained blue agents with different strategies
- You understand how deception limits, objectives, and detection systems affect performance
- You can interpret training curves and evaluation metrics

---

## 🔴 **PHASE 3: Red Agent (Attacker) Mastery**
*Objective: Master offensive agent training and understand attack patterns*

### **Step 3.1: Red Agent Training Variants**
```powershell
# Basic RL red agent training
python -m cyberwheel train train_red.yaml --network-config 200-host-network.yaml --total-timesteps 10000000 --experiment-name Phase3_Red_RL --train-red true --train-blue false

# ART (MITRE ATT&CK) agent training
python -m cyberwheel train train_red.yaml --red-agent art_agent.yaml --network-config 200-host-network.yaml --total-timesteps 5000000 --experiment-name Phase3_Red_ART

# Campaign-based red agent
python -m cyberwheel train train_blue_art_campaign.yaml --campaign true --total-timesteps 5000000 --experiment-name Phase3_Red_Campaign
```

### **Step 3.2: Target-Specific Training**
```powershell
# Server-focused attacks
python -m cyberwheel train train_red.yaml --valid-targets servers --total-timesteps 5000000 --experiment-name Phase3_Red_Servers

# All hosts attacks
python -m cyberwheel train train_red.yaml --valid-targets all --total-timesteps 5000000 --experiment-name Phase3_Red_AllHosts
```

### **Step 3.3: Red Agent Evaluation**
```powershell
# Evaluate red agents against baseline blue
$red_experiments = @("Phase3_Red_RL", "Phase3_Red_ART", "Phase3_Red_Campaign", "Phase3_Red_Servers", "Phase3_Red_AllHosts")

foreach ($exp in $red_experiments) {
    python -m cyberwheel evaluate evaluate_red.yaml --experiment-name $exp --num-episodes 100
}
```

**✅ Phase 3 Complete When:**
- You have 5 trained red agents with different strategies
- You understand MITRE ATT&CK integration and campaign-based attacks
- You can compare different attack patterns and success rates

---

## ⚖️ **PHASE 4: Agent Interaction Analysis**
*Objective: Understand how different agent combinations perform*

### **Step 4.1: Cross-Evaluation Matrix**
```powershell
# Create evaluation matrix: Blue agents vs Red agents
$blue_agents = @("Phase2_Blue_Medium", "Phase2_Blue_HighDecoy", "Phase2_Blue_PerfectDetection")
$red_strategies = @("art_agent.yaml", "rl_red_agent.yaml")

foreach ($blue in $blue_agents) {
    foreach ($red in $red_strategies) {
        $eval_name = "Phase4_Cross_${blue}_vs_${red}"
        python -m cyberwheel evaluate evaluate_blue.yaml --experiment-name $blue --red-agent $red --num-episodes 50 --experiment-name $eval_name
    }
}
```

### **Step 4.2: Performance Analysis**
```powershell
# Generate comprehensive performance reports
python -c "
import os
import pandas as pd
from cyberwheel.utils import Evaluator

# Collect all Phase 4 results
evaluator = Evaluator('cyberwheel/data/runs/')
results = evaluator.collect_cross_evaluation_results('Phase4_Cross_*')
results.to_csv('Phase4_Cross_Evaluation_Results.csv')
print('Cross-evaluation analysis saved to Phase4_Cross_Evaluation_Results.csv')
"
```

**✅ Phase 4 Complete When:**
- You have systematic evaluation data for blue vs red combinations
- You understand which defensive strategies work best against different attacks
- You have quantitative data on deception effectiveness

---

## 🔄 **PHASE 5: Multi-Agent Co-Evolution (SULI)**
*Objective: Master simultaneous adversarial training*

### **Step 5.1: Basic SULI Training**
```powershell
# Small network SULI (quick test)
python -m cyberwheel train train_suli.yaml --network-config 15-host-network.yaml --total-timesteps 5000000 --experiment-name Phase5_SULI_Small

# Medium network SULI (main training)
python -m cyberwheel train train_suli.yaml --network-config 200-host-network.yaml --total-timesteps 50000000 --experiment-name Phase5_SULI_Medium --num-envs 30

# Enable W&B tracking for detailed analysis
python -m cyberwheel train train_suli.yaml --network-config 200-host-network.yaml --total-timesteps 50000000 --experiment-name Phase5_SULI_Tracked --track --wandb-project-name cyberwheel_phase5
```

### **Step 5.2: SULI Baseline Comparison**
```powershell
# Train baseline for comparison
python -m cyberwheel train train_suli_baseline.yaml --total-timesteps 20000000 --experiment-name Phase5_SULI_Baseline

# Evaluate SULI vs Baseline
python -m cyberwheel evaluate evaluate_suli.yaml --experiment-name Phase5_SULI_Medium --num-episodes 200
python -m cyberwheel evaluate evaluate_suli_baseline.yaml --experiment-name Phase5_SULI_Baseline --num-episodes 200
```

### **Step 5.3: Advanced SULI Configurations**
```powershell
# Different headstart strategies
python -m cyberwheel train train_suli.yaml --headstart 15 --total-timesteps 20000000 --experiment-name Phase5_SULI_Headstart15

python -m cyberwheel train train_suli.yaml --headstart 5 --total-timesteps 20000000 --experiment-name Phase5_SULI_Headstart5

# Different network scales
python -m cyberwheel train train_suli.yaml --network-config 1000-host-network.yaml --total-timesteps 30000000 --experiment-name Phase5_SULI_Large --num-envs 20
```

**✅ Phase 5 Complete When:**
- You have successful SULI training with co-evolving agents
- You understand the dynamics of adversarial training
- You can compare SULI performance against static baselines

---

## 🚀 **PHASE 6: Scalability & Advanced Features**
*Objective: Test limits and advanced capabilities*

### **Step 6.1: Large-Scale Network Training**
```powershell
# Massive network testing (if your system can handle it)
python -m cyberwheel train train_blue.yaml --network-config 10000-host-network.yaml --total-timesteps 20000000 --experiment-name Phase6_Massive_Blue --num-envs 50 --async-env true

# Performance optimization
python -m cyberwheel train train_blue.yaml --network-config 5000-host-network.yaml --total-timesteps 10000000 --experiment-name Phase6_Optimized --device cuda --num-envs 100
```

### **Step 6.2: Advanced Detection Systems**
```powershell
# Complex multi-layered detection
python -m cyberwheel train train_blue.yaml --detector-config multilayered_perfect.yaml --network-config 1000-host-network.yaml --total-timesteps 15000000 --experiment-name Phase6_Advanced_Detection

# Custom detection configurations (if available)
python -m cyberwheel train train_blue.yaml --detector-config hids_100_percent.yaml --total-timesteps 10000000 --experiment-name Phase6_HIDS_Focus
```

### **Step 6.3: Hyperparameter Optimization**
```powershell
# Learning rate sweep
$learning_rates = @(0.0001, 0.0003, 0.001, 0.003)
foreach ($lr in $learning_rates) {
    python -m cyberwheel train train_blue.yaml --learning-rate $lr --total-timesteps 5000000 --experiment-name "Phase6_LR_Sweep_$lr"
}

# Environment scaling sweep
$env_counts = @(10, 30, 50, 100)
foreach ($envs in $env_counts) {
    python -m cyberwheel train train_blue.yaml --num-envs $envs --total-timesteps 5000000 --experiment-name "Phase6_Env_Sweep_$envs"
}
```

**✅ Phase 6 Complete When:**
- You've tested the framework's scalability limits
- You understand performance characteristics at different scales
- You have optimized hyperparameters for your use case

---

## 🔬 **PHASE 7: Research Extensions & Advanced Analysis**
*Objective: Ready for research contributions and custom extensions*

### **Step 7.1: Comprehensive Analysis Suite**
```powershell
# Generate complete analysis of all training phases
python -c "
import pandas as pd
import matplotlib.pyplot as plt
from cyberwheel.utils import Evaluator, Analyzer

# Collect all experimental results
analyzer = Analyzer('cyberwheel/data/runs/')

# Generate comprehensive report
analyzer.generate_phase_comparison_report([
    'Phase2_Blue_*',
    'Phase3_Red_*', 
    'Phase4_Cross_*',
    'Phase5_SULI_*',
    'Phase6_*'
])

# Create publication-ready plots
analyzer.create_publication_plots()
print('Complete analysis generated in cyberwheel/data/analysis/')
"
```

### **Step 7.2: Statistical Significance Testing**
```powershell
# Run multiple seeds for statistical analysis
$seeds = @(1, 42, 123, 456, 789)
foreach ($seed in $seeds) {
    python -m cyberwheel train train_suli.yaml --seed $seed --total-timesteps 20000000 --experiment-name "Phase7_Stats_SULI_seed_$seed"
    python -m cyberwheel evaluate evaluate_suli.yaml --experiment-name "Phase7_Stats_SULI_seed_$seed" --num-episodes 100 --seed $seed
}

# Generate statistical analysis
python -c "
from cyberwheel.utils import StatisticalAnalyzer
stats = StatisticalAnalyzer()
stats.analyze_multi_seed_experiments('Phase7_Stats_SULI_*')
stats.generate_significance_report()
"
```

### **Step 7.3: Advanced Visualization & Documentation**
```powershell
# Create comprehensive visualization dashboard
python -m cyberwheel visualizer train_suli.yaml --advanced-mode true

# Generate interactive analysis
python -c "
from cyberwheel.utils import InteractiveAnalyzer
analyzer = InteractiveAnalyzer()
analyzer.create_interactive_dashboard('cyberwheel/data/runs/')
analyzer.launch_dashboard()  # Opens interactive analysis at localhost:8051
"

# Export results for research
python -c "
from cyberwheel.utils import ResearchExporter
exporter = ResearchExporter()
exporter.export_all_experiments_to_research_format('cyberwheel/data/runs/', 'research_export/')
print('Research data exported to research_export/ directory')
"
```

**✅ Phase 7 Complete When:**
- You have statistically significant results across multiple seeds
- You have comprehensive analysis of all training phases
- You have publication-ready data and visualizations
- You understand the framework well enough to extend it

---

## 🎯 **EXTENSION READINESS CHECKLIST**

Once you complete all 7 phases, you'll be ready to extend Cyberwheel in these areas:

### **Research Extensions You Can Now Tackle:**

1. **🔬 Novel Agent Architectures**
   - Custom neural network architectures for blue/red agents
   - Attention-based mechanisms for network awareness
   - Graph neural networks for topology understanding

2. **🛡️ Advanced Defense Strategies**
   - Dynamic decoy placement algorithms
   - Adaptive detection threshold optimization
   - Multi-objective optimization for defense

3. **⚔️ Sophisticated Attack Models**
   - Advanced persistent threat (APT) simulation
   - Zero-day exploit modeling
   - Social engineering integration

4. **🌐 Network Topology Research**
   - Real-world network topology integration
   - Dynamic network changes during episodes
   - Network resilience analysis

5. **📊 Evaluation Metrics**
   - Custom security metrics
   - Economic impact modeling
   - Real-time threat assessment

6. **🔧 Framework Extensions**
   - Custom reward functions
   - New observation spaces
   - Integration with external security tools

### **Development Path Forward:**
```powershell
# Create your extension workspace
mkdir cyberwheel_extensions
cd cyberwheel_extensions

# Initialize your research project
git init
echo "# My Cyberwheel Extensions" > README.md

# Create development branches for different extensions
git checkout -b feature/custom-agent-architecture
git checkout -b feature/advanced-detection-systems
git checkout -b feature/novel-reward-functions
```

---

## 📈 **Training Progress Tracking**

### **Week 1 Milestones:**
- [ ] Phase 1: System validation complete
- [ ] Phase 2: 8 blue agent variants trained
- [ ] Basic understanding of deception strategies

### **Week 2 Milestones:**
- [ ] Phase 3: 5 red agent variants trained  
- [ ] Phase 4: Cross-evaluation matrix complete
- [ ] Understanding of agent interactions

### **Week 3-4 Milestones:**
- [ ] Phase 5: SULI training successful
- [ ] Multi-agent co-evolution mastered
- [ ] Baseline comparisons complete

### **Week 5-6 Milestones:**
- [ ] Phase 6: Scalability testing complete
- [ ] Phase 7: Research-ready analysis
- [ ] Statistical significance established
- [ ] Ready for custom extensions

### **Total Computational Requirements:**
- **Estimated Training Time**: 150-200 hours total
- **Storage Requirements**: ~50-100 GB for all models and logs
- **Recommended Resources**: 
  - CPU: 16+ cores for parallel training
  - RAM: 32+ GB for large networks
  - GPU: Optional but recommended for Phase 6+

This progression ensures you master every aspect of Cyberwheel before extending it, giving you the deep understanding needed for meaningful research contributions.
