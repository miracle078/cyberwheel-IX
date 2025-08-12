## 5. Environment Formulation

### 5.1 Mathematical Foundation

**Episodic RL Formulation**:
```
Environment: E = (S, A, P, R, γ, H)
Where:
S = State space (network configurations)
A = Action space (agent decisions)
P = Transition probability function
R = Reward function
γ = Discount factor
H = Episode horizon (finite length)
```

**Multi-Agent Extension**:
```
Agents: {Red, Blue} with individual state/action spaces
Red Agent: (S^(r), A^(r), π^(r))
Blue Agent: (S^(b), A^(b), π^(b))
```

**Theoretical Foundation**: This formulation extends standard single-agent MDPs to competitive multi-agent scenarios where agents have opposing objectives, creating a two-player zero-sum game embedded within the RL framework.

### 5.2 Network Representation Theory

**Graph-Theoretic Foundation**:
```
Network Graph: G = (V, E)
Vertices: V = H ∪ S ∪ R
  H = Hosts (computers/devices)
  S = Subnets (network segments)  
  R = Routers (network infrastructure)
Edges: E ⊆ V × V (directed connections)
```

**Implementation Details**:
```python
# NetworkX DiGraph implementation
G = nx.DiGraph()
# Supports 10 to 100,000+ hosts
# YAML-driven configuration system
```

**Host State Vector Mathematical Definition**:
```
h_i = ⟨IP_i, OS_i, S_i, V_i, compromised_i, decoy_i⟩
Where:
IP_i ∈ IPv4_address_space
OS_i ∈ {Windows, Linux, macOS, ...}
S_i ⊆ Services (running software)
V_i ⊆ Vulnerabilities (security weaknesses)
compromised_i ∈ {0,1}
decoy_i ∈ {0,1}
```

**Theoretical Significance**: Each host represents a complex state vector combining network configuration, security posture, and current compromise status, enabling realistic cyber attack/defense simulation.

### 5.3 State Space Mathematics

**Red Agent State Space Formulation**:
```
S^(r) ⊂ ℝ^(d_r)
d_r = 2|H| + |S| + 4 + |T| = 2|H| + |S| + 299

State Vector Components:
S^(r)_{t,h} = [position_{t,h}; knowledge_{t,h}; phase_{t,h}; capabilities_{t,h}]

Where:
position_{t,h} ∈ {0,1}^|H|     (one-hot current compromised host)
knowledge_{t,h} ∈ {0,1}^(|H|+|S|) (discovered network topology)
phase_{t,h} ∈ {0,1}^4          (kill-chain phase encoding)
capabilities_{t,h} ∈ {0,1}^|T|  (available MITRE ATT&CK techniques)
```

**Kill-Chain Phase Encoding**:
```
phase ∈ {0,1}^4 represents:
[discovery, reconnaissance, privilege-escalation, impact]
Only one phase active at a time (one-hot encoding)
```

**Blue Agent State Space Formulation**:
```
S^(b) ⊂ ℝ^(d_b)  
d_b = 3|H| + 2

State Vector Components:
S^(b)_{t,h} = [alerts_current; alerts_history; decoys; metadata]

Where:
alerts_current ∈ {0,1}^|H|    (immediate timestep alerts)
alerts_history ∈ {0,1}^|H|    (cumulative alert memory)
decoys ∈ {0,1}^|H|            (deployed honeypot locations)
metadata ∈ ℝ^2                (padding constant, total decoy count)
```

**Dual Observation Structure Theory**: The blue agent's state design implements both immediate response capability (current alerts) and strategic learning (historical patterns), enabling both reactive and proactive defensive strategies.

### 5.4 Action Space Formulation

**Red Agent Action Space**:
```
A^(r) = A_discovery ∪ A_recon ∪ A_privesc ∪ A_impact
|A^(r)| = 12 × |H|

Parameterized by target host h ∈ H:
A_discovery: Network scanning, ping sweeps, port discovery
A_recon: Service enumeration, vulnerability identification
A_privesc: Exploitation, lateral movement, privilege escalation
A_impact: Data exfiltration, service disruption, persistence
```

**MITRE ATT&CK Integration**:
```
Total Techniques: |T| = 295 verified attack techniques
Kill-chain Mapping: Discovery → Reconnaissance → Privilege Escalation → Impact
Technique Success: Probability-based on target vulnerability profiles
```

**Blue Agent Action Space**:
```
A^(b) = A_deploy ∪ A_remove ∪ A_isolate ∪ {nothing}
|A^(b)| = 2|S||D| + |H| + 1

Action Categories:
A_deploy = {(deploy, s_j, d_k) : s_j ∈ S, d_k ∈ D}  (deploy decoy type d_k on subnet s_j)
A_remove = {(remove, s_j, d_k) : s_j ∈ S, d_k ∈ D}  (remove decoys)
A_isolate = {(isolate, h_i) : h_i ∈ H}               (isolate compromised hosts)
nothing = no defensive action taken
```

**Strategic Action Design**: The action space reflects realistic cybersecurity operations where defenders must balance resource allocation between detection, deception, and remediation activities.

### 5.5 Reward Function Theory

**Red Agent Reward Structure**:
```
R^(r)_{t,h} = Σᵢ αᵢ·𝟙[technique_i successful] 
              + β·|assets_compromised| 
              - λ·𝟙[detected]

Parameter Interpretation:
αᵢ > 0: Technique execution rewards (encourages attack progression)
β > 0: Asset compromise value (objective achievement)
λ > 0: Detection penalty (stealth incentive)
```

**Blue Agent Reward Structure**:
```
R^(b)_{t,h} = R_deception + R_protection + R_cost

Component Breakdown:
R_deception = 10·|R^(r)_base| if red attacks decoy successfully
R_protection = -|R^(r)_base| if red attacks real host successfully  
R_cost = -c_deploy·N_new_decoys - c_maintain·Σᵢ decoy_i
```

**Critical Design Decision - 10× Deception Multiplier**:
```
Theoretical Justification:
1. Creates strong incentive alignment toward honeypot effectiveness
2. Reflects real-world value of attack misdirection
3. Encourages sophisticated defensive strategies
4. Verified in implementation (rl_reward.py, lines 142-143)
```

**Adversarial Reward Structure**: The reward functions are designed to be zero-sum in the core attack/defense interaction while allowing for operational costs and strategic considerations.

### 5.6 State Transition Dynamics

**Transition Probability Formulation**:
```
P(S_{t,h+1}, S^(r)_{t,h+1}, S^(b)_{t,h+1} | S_{t,h}, S^(r)_{t,h}, S^(b)_{t,h}, A^(r)_{t,h}, A^(b)_{t,h})
```

**Decomposition**:
```
Network State Transition: P(N_{t,h+1} | N_{t,h}, A^(r)_{t,h}, A^(b)_{t,h})
Red State Update: P(S^(r)_{t,h+1} | N_{t,h+1}, S^(r)_{t,h}, A^(r)_{t,h})
Blue State Update: P(S^(b)_{t,h+1} | N_{t,h+1}, S^(b)_{t,h}, A^(r)_{t,h}, A^(b)_{t,h})
```

**Deterministic Network Rules**:
- Red actions modify host compromise status based on vulnerability exploitation
- Blue actions add/remove decoys and modify network isolation policies
- Alert generation follows probabilistic detection models

**Probabilistic Alert Generation**:
```
P(alert | technique, detector) = Π_j p_j^(detector)
Where j indexes technique components
```

---

## 6. Algorithmic Framework

### 6.1 Historical Context Formulation

**Complete History Definition**:
```
H_{t,h} = {(S^(r)_{t',h'}, A^(r)_{t',h'}, S^(b)_{t',h'}, A^(b)_{t',h'}, 
           R^(r)_{t',h'}, R^(b)_{t',h'})}_{(t',h') < (t,h)}
```

**Theoretical Significance**: This comprehensive history enables sophisticated strategy adaptation and opponent modeling, crucial for adversarial learning scenarios.

**Memory Complexity**: History grows linearly with episode length, requiring efficient storage and retrieval mechanisms for practical implementation.

### 6.2 Red Agent Algorithm Analysis

**Deterministic Baseline Algorithm**:
```
Algorithm: Deterministic Kill-Chain Policy
Input: State S^(r)_{t,h}, network knowledge
1. Extract phase φ and position p from state
2. Phase-based action selection:
   if φ = discovery: network_scan(current_subnet)
   elif φ = reconnaissance: vulnerability_identification(discovered_hosts)
   elif φ = privilege_escalation: lateral_movement(target_selection)
   elif φ = impact: data_exfiltration(high_value_assets)
3. Phase transition based on success criteria
4. Return action A^(r)_{t,h}
```

**Phase Transition Logic**:
```
discovery → reconnaissance: sufficient topology discovered
reconnaissance → privilege_escalation: exploitable vulnerability found
privilege_escalation → impact: critical server compromised
impact → [episode termination or persistence]
```

**Adaptive Enhancement Framework**:
```
π^(r)(a|s,H) = softmax(β·Q^(r)(s,a) + α·adaptation_bonus(a,H))

adaptation_bonus rewards actions that:
1. Counter observed blue defensive patterns
2. Exploit detected blue agent weaknesses
3. Adapt to blue agent behavioral changes
```

### 6.3 PPO Algorithm Deep Dive

**Proximal Policy Optimization Core Objective**:
```
L^PPO(θ) = 𝔼_t[min(r_t(θ)Â_t, clip(r_t(θ), 1-ε, 1+ε)Â_t)]

Where:
r_t(θ) = π_θ(A^(b)_{t,h}|S^(b)_{t,h}) / π_{θ_old}(A^(b)_{t,h}|S^(b)_{t,h})  (probability ratio)
Â_t = Generalized Advantage Estimate
ε = 0.2 (clipping parameter, verified in implementation)
```

**Theoretical Foundation of Clipping**:
- **Problem**: Large policy updates can destabilize training
- **Solution**: Clip probability ratios to [1-ε, 1+ε] range
- **Guarantee**: Monotonic policy improvement with bounded updates

**Generalized Advantage Estimation (GAE)**:
```
Â_{t,h} = Σˡ⁼⁰^{H-h} (γλ)ˡ δ_{t,h+l}

Where:
δ_{t,h} = R^(b)_{t,h} + γV(S^(b)_{t,h+1}) - V(S^(b)_{t,h})  (TD error)
λ = 0.95 (GAE parameter, bias-variance tradeoff)
γ = 0.95 (discount factor)
```

**GAE Theory**:
- **λ = 0**: High bias, low variance (TD(0))
- **λ = 1**: Low bias, high variance (Monte Carlo)
- **λ = 0.95**: Optimal bias-variance balance for most applications

### 6.4 PPO Training Algorithm Implementation

**Three-Phase Training Cycle**:

**Phase 1: Experience Collection**
```
Algorithm: Experience Collection
for episode t = 1 to T:
    for timestep h = 1 to H:
        observe state S^(b)_{t,h}
        sample action A^(b)_{t,h} ~ π_θ(S^(b)_{t,h})
        execute action in environment
        observe reward R^(b)_{t,h} and next state S^(b)_{t,h+1}
        store transition (S^(b)_{t,h}, A^(b)_{t,h}, R^(b)_{t,h}, S^(b)_{t,h+1})
```

**Phase 2: Advantage Computation**
```
Algorithm: GAE Computation
compute value estimates V_θ(S^(b)_{t,h}) for all states
compute TD errors δ_{t,h} = R^(b)_{t,h} + γV_θ(S^(b)_{t,h+1}) - V_θ(S^(b)_{t,h})
compute advantages Â_{t,h} using GAE formula
compute returns R^total_{t,h} = Â_{t,h} + V_θ(S^(b)_{t,h})
normalize advantages: Â_{t,h} ← (Â_{t,h} - mean(Â)) / std(Â)
```

**Phase 3: Policy Update**
```
Algorithm: PPO Policy Update
for epoch k = 1 to K:
    for each minibatch in experience buffer:
        compute probability ratios r_t(θ)
        compute clipped objective L^PPO(θ)
        compute value loss L^value = ½(V_θ(s) - R^total)²
        compute entropy bonus L^entropy = -β_ent Σ_a π_θ(a|s)log π_θ(a|s)
        total loss L^total = L^PPO + 0.5·L^value + 0.01·L^entropy
        gradient update θ ← θ - α∇_θ L^total
```

**Loss Function Components**:
1. **PPO Loss**: Primary policy improvement objective
2. **Value Loss**: Critic network training (coefficient: 0.5)
3. **Entropy Bonus**: Exploration encouragement (coefficient: 0.01)

### 6.5 Detection and Alert Mechanisms

**Alert Structure Definition**:
```
Alert_{t,h} = ⟨src_host, techniques, timestamp, confidence⟩

Where:
src_host ∈ H ∪ {null}          (source of suspicious activity)
techniques ⊆ T                 (detected MITRE ATT&CK techniques)
timestamp ∈ ℕ                  (timestep of detection)
confidence ∈ [0,1]             (detection confidence score)
```

**Detection Probability Model**:
```
Multi-Component Technique Detection:
p_detect(technique_i, detector_d) = Π_{j=1}^{|technique_i.components|} p_j^(d)

Multi-Technique Detection (at least one detected):
P(detect ≥ 1) = 1 - Π_i (1 - p_detect(technique_i, detector_d))
```

**Detection Model Calibration**:
- **Simple Techniques**: p_detect ≈ 0.9 (high detection probability)
- **Sophisticated Techniques**: p_detect ≈ 0.3 (moderate detection)
- **Stealth Techniques**: p_detect ≈ 0.1 (low detection probability)

**False Positive Generation Model**:
```
P(false positive at time t) = 1 - e^{-λ_fp·Δt}

Where:
λ_fp = false positive rate parameter
Δt = time interval
```

**Exponential Distribution Rationale**: False positives often result from random system events, network noise, and operational activities, which follow Poisson processes leading to exponential inter-arrival times.

### 6.6 Blue Agent Observation Vector Construction

**Verified Implementation Algorithm**:
```
Algorithm: Blue Observation Construction
Input: Current alerts A_t, host mapping, active decoys
Output: Observation vector o_t ∈ ℝ^{d_b}

1. Initialize o_t ← 0^{d_b}
2. barrier ← |H|
3. Reset current alerts: o_t[0:barrier-1] ← 0
4. for each alert a ∈ A_t:
     if a.src_host ≠ null and mapping exists:
         o_t[mapping[a.src_host]] ← 1              (current alert)
         o_t[barrier + mapping[a.src_host]] ← 1    (sticky history)
5. Set metadata:
   o_t[d_b-2] ← -1                                (padding constant)
   o_t[d_b-1] ← |active_decoys|                   (decoy count)
6. return o_t
```

**Sticky Memory Design**: Once an alert is generated for a host, the historical alert bit remains set, providing the blue agent with persistent memory of past suspicious activity.

**Implementation Verification**: This algorithm is verified against the actual codebase implementation, ensuring accuracy of the mathematical description.

---

*This completes the technical analysis of sections 5-6. Would you like me to continue with sections 7-10 covering Evaluation Methodology, Experimental Design, Results Analysis, and Mathematical Foundations?*
