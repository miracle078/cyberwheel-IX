# TikZ to PlantUML Conversion

This folder contains PlantUML equivalents of the TikZ figures from the Cyberwheel comprehensive report, converted for better maintainability and faster generation.

## Generated Diagrams

### 1. `adversarial_framework_new.puml/png`
- **Purpose**: Shows the adversarial learning framework with Red Agent, Blue Agent, and Environment interactions
- **Key Elements**: Attack actions, defense actions, observations, rewards, state changes
- **Use Case**: Illustrates the core PPO training loop

### 2. `agent_capabilities_comprehensive.puml/png`
- **Purpose**: Comprehensive view of Red and Blue agent capabilities across the MITRE ATT&CK kill chain
- **Key Elements**: Kill chain phases (Discovery → Reconnaissance → Access → Impact), Blue agent defensive actions
- **Use Case**: Shows the full scope of adversarial interactions

### 3. `agent_capabilities_new.puml` (source only)
- **Purpose**: Alternative version of agent capabilities diagram
- **Note**: PNG not generated for this version

### 4. `configuration_hierarchy_new.puml/png`
- **Purpose**: Shows the Cyberwheel configuration hierarchy and validation structure
- **Key Elements**: Environment config, Agent config, Mathematical mapping, Experimental controls, Implementation verification
- **Use Case**: Documents the system configuration architecture

### 5. `environment_interaction_new.puml/png`
- **Purpose**: Detailed view of environment-agent interactions with detection signals
- **Key Elements**: Red/Blue agents, Environment state, Detection signals, Reward feedback
- **Use Case**: Explains the reward computation and signal flow

### 6. `evolution_timeline_new.puml/png`
- **Purpose**: Timeline showing the evolution of cyber defense approaches
- **Key Elements**: Generation 1 (Rule-Based), Generation 2 (ML), Generation 3 (Adaptive), Generation 4 (Adversarial)
- **Use Case**: Historical context for the research contribution

### 7. `kill_chain_policy_new.puml/png`
- **Purpose**: Illustrates the deterministic Red agent policy through the MITRE ATT&CK kill chain
- **Key Elements**: Kill chain phases with transition logic and decision points
- **Use Case**: Shows how the fixed adversary progresses through attack phases

### 8. `network_topology_new.puml/png`
- **Purpose**: Network topology diagram showing DMZ, internal networks, and decoy placement
- **Key Elements**: Firewall, Web/Mail servers, Internal hosts, Database servers, Strategic decoys
- **Use Case**: Visualizes the experimental network environment

### 9. `observation_vector_new.puml/png`
- **Purpose**: Breakdown of the Blue agent's observation vector structure
- **Key Elements**: Current alerts (|H| dimensions), Historical alerts (|H| dimensions), Metadata (2 dimensions)
- **Use Case**: Documents the state space structure for the RL agent

### 10. `ppo_algorithm_phases_new.puml/png`
- **Purpose**: Shows the three phases of PPO algorithm execution
- **Key Elements**: Experience collection, Advantage estimation, Policy update
- **Use Case**: Explains the PPO training process

### 11. `ppo_architecture_new.puml/png`
- **Purpose**: Architecture diagram of PPO training for Cyberwheel
- **Key Elements**: Blue Agent (PPO), Red Agent (Fixed), Environment, Policy updates
- **Use Case**: High-level view of the training architecture

### 12. `reward_decomposition_new.puml/png`
- **Purpose**: Breakdown of the Blue agent's reward function components
- **Key Elements**: Deployment reward (α₁=5.0), Deception reward (α₂=15.0), Compromise penalty (α₃=-10.0), Removal cost (α₄=-2.0)
- **Use Case**: Documents the reward structure and incentives

## Benefits of PlantUML Conversion

1. **Text-based**: Easy to version control and modify
2. **Fast generation**: Much quicker than manual TikZ coding
3. **Consistent styling**: Professional appearance with minimal effort
4. **Multiple formats**: PNG, SVG, PDF, LaTeX output
5. **Maintainable**: Simple syntax for future updates

## Usage

To regenerate PNG files from PlantUML sources:
```bash
plantuml -tpng *.puml
```

To generate other formats:
```bash
plantuml -tsvg *.puml  # SVG format
plantuml -tlatex *.puml  # LaTeX format
plantuml -tpdf *.puml   # PDF format
```

## File Organization

- `*_new.puml`: PlantUML source files
- `*_new.png`: Generated PNG images
- `README.md`: This documentation file
