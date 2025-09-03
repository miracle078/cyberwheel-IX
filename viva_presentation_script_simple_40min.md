# Cyberwheel Viva Presentation (Simple Words Version ~40 Minutes)
## Teaching AI Defenders by Letting Them Spar With AI Attackers

(Designed for a clear spoken delivery. About 5,000 words ≈ 40 minutes at ~125 wpm.)

---
## Quick Timing Map
- Opening & Why It Matters: 3 min
- Section 1 (Network Basics): 4 min (7 total)
- Section 2 (History): 5 min (12 total)
- Section 3 (Prior Work & Gaps): 3 min (15 total)
- Section 4 (What is RL?): 5 min (20 total)
- Section 5 (Why Adversarial): 4 min (24 total)
- Section 6 (Environment Details): 5 min (29 total)
- Section 7 (Rewards): 3 min (32 total)
- Section 8 (How Learning Works – PPO): 3 min (35 total)
- Section 9 (SULI Method): 3 min (38 total)
- Sections 10–12 (Experiments, Results, Impact): 5–6 min (≈44; trim live)
- Conclusion + Questions buffer: finish at ~40 by light trimming as needed.

Have 3–4 small “flex trim” spots: Section 2 history, Section 6 details, Section 10 phase list, Section 12 metrics.

---
## Opening (≈3 min)
Good morning/afternoon. I’m presenting Cyberwheel: a way to train AI systems to defend computer networks by letting an AI attacker and an AI defender learn against each other—like two sparring partners who both improve.

Key problem in one line: How do we build defenders that can handle attacks they have never seen before? The answer: let them constantly practice against a learning attacker instead of only studying old attack logs.

### Why this matters (plain reasons)
1. Breaches cost a lot (millions per serious incident when you add downtime, legal, recovery). Stopping or delaying early stages saves money.
2. Attackers move fast with automation; defenders often react slowly. We need defenders that predict, not just react.
3. There aren’t enough skilled analysts to hand‑tune everything for huge networks.
4. Deception tools (like fake systems / decoys) are powerful but usually deployed in a guessy, manual way.
5. Older “adversarial” training methods often failed or collapsed; we fixed that stability problem.
6. If we can safely automate training, we shift from chasing yesterday’s threats to shaping tomorrow’s defense.

Core idea: Put an attacking AI and a defending AI in a realistic network simulator. Let them play thousands of times. The defender learns where to put decoys and how to slow, mislead, or contain the attacker. The attacker keeps adapting, forcing the defender to improve again. That is Cyberwheel.

---
## 1. The Battlefield: What Are We Defending? (≈4 min)
Think of a network as a small town: offices (workstations), warehouses (servers), and fake buildings (decoys) that look real but are traps.

We train across sizes: from tiny (15 machines) up to large enterprise scale (10,000+). Why is scale important? A method that only works on toy setups won’t help in the real world.

Key parts:
- Real servers: valuable targets (like databases or web services).
- Workstations: stepping stones attackers first compromise.
- Decoys: believable fakes that waste attacker time and reveal their presence.
- Defender actions: deploy or remove decoys, isolate infected machines, or wait.
- Attacker actions: scan, probe, exploit, escalate, and cause impact (steal or disrupt).

Goal: Teach the defender to place and manage decoys and respond efficiently before real damage happens.

---
## 2. How Cyber Defense Evolved (≈5 min)
Short history in plain words:
1. Manual era: Humans watched logs and reacted. Slow and incomplete.
2. Rule era: Firewalls and signatures—“block X,” “alert on pattern Y.” Good for known threats. Weak against new ones.
3. Machine learning era: Systems flagged unusual behavior. Better, but still reacting to what already happened.
4. Adversarial learning era (our focus): Train defense and attack models together so the defender experiences new tactics as they emerge.

Why the old way is not enough: Attackers change faster than static rules. Once a trick is known, they pivot. We need living training—an always-on sparring process.

What’s new here: We don’t just simulate fixed attackers; we train a learning attacker that forces the defender to keep adapting.

---
## 3. Prior Work & What Was Missing (≈3 min)
Prior foundations gave us:
- Reinforcement learning basics (how agents learn by trial and error).
- Self-play success in games (like AlphaGo).
- Game theory ideas for attack/defense balance.
- Honeypots (decoys) but usually static, limited, and hand-placed.

Gaps we target:
- Stability: many adversarial RL runs crashed or one side dominated early.
- Scale: few systems showed they work from small to very large networks.
- Deception optimization: little systematic placement learning.
- Realistic attack coverage: need many real techniques (we use 295 from a respected framework).

Our 5 headline contributions:
1. A stable training method (SULI) that cuts failures by about 90%.
2. Proven scaling 15 → 10,000+ hosts.
3. A structured 7-phase evaluation, not cherry-picked runs.
4. Learned deception strategies that beat detection-only defense.
5. Deep integration of real attack techniques for relevance.

---
## 4. What Is Reinforcement Learning? (≈5 min)
Simple analogy: Teach a dog tricks. Dog tries action → gets reward or not → repeats what works.

Key pieces in plain words:
- State: What the agent currently “sees.”
- Action: What it can do next.
- Reward: Immediate feedback (good, bad, neutral).
- Policy: Its habit or strategy for choosing actions.
- Goal: Get the highest total reward over time.

In our setting: The attacker learns which sequence of steps gets it deeper. The defender learns where to place decoys or when to isolate to block progress while conserving resources.

We add a discount (a “future matters slightly less” factor) so the agent balances short-term wins and long-term gains.

---
## 5. Why Adversarial Learning? (≈4 min)
Single-agent learning is like practicing against a static puzzle. Adversarial learning is like practicing against a real opponent who keeps improving. Harder—but more realistic.

Challenges:
- Moving target: The opponent changes while you learn.
- Instability: If attacker gets too strong early, defender learns nothing (or vice versa).
- Balance: Need both to improve together, not a one-sided stomp.

We treat it like a tug-of-war that should stay competitive so both sides keep getting better.

---
## 6. Inside the Simulation (≈5 min)
What the attacker sees: which machines it has touched, what it has scanned, what phase it is in, and what attack techniques are available.

What the defender sees: recent alerts, where decoys are placed, a memory of past signals, and counts of resources.

Action ranges:
- Attacker picks from scanning, probing, exploiting, moving, impacting.
- Defender deploys/removes decoys, isolates machines, or waits.

Why decoys? They: (1) waste attacker time, (2) give early warning, (3) shape attacker behavior into “safe” zones.

Scale principle: As network size grows, action options grow, but our method still trains effectively.

---
## 7. How We Motivate Behavior (Rewards) (≈3 min)
Attacker rewards: success for advancing and compromising real machines; penalty if detected.

Defender rewards:
- Big positive if attacker hits a decoy (we amplify this 10× to make deception attractive).
- Negative if attacker hits a real machine.
- Small costs for deploying and maintaining decoys (prevents spamming).

Why the 10× multiplier? To strongly push learning toward smart decoy placement. Without it the defender might just play passive blocking.

---
## 8. How Learning Steps Happen (PPO in Plain Words) (≈3 min)
Think of the defender as a student updating its playbook every few “games.” PPO (the algorithm) says: “Change your strategy, but not too drastically.” It compares new actions to old ones and clips extreme jumps to stay stable. This prevents forgetting useful behaviors.

Core idea: Small, steady improvements beat wild swings.

---
## 9. SULI: Our Stability Breakthrough (≈3 min)
Problem we faced: Normal adversarial training often collapsed—one side wins too early, the other never learns.

SULI solution components:
1. Start both with totally even, neutral strategies (no early lopsided advantage).
2. Watch the performance gap; if one pulls too far ahead, we rebalance (for example by resetting or adjusting learning speed).
3. Keep both moving forward together.

Impact: We cut failed training runs dramatically (about 90% fewer failures). That makes large experimentation practical.

---
## 10. Our 7 Test Phases (Condensed) (≈4 min)
We did not rely on one lucky run. We used seven structured phases:
1. Quick system check: Does everything learn at all? (Yes—fast improvement.)
2. Train defender variants (different decoy budgets and styles).
3. Build/verify attacker with many real techniques.
4. Cross-match defender vs attacker combinations to see patterns.
5. Co-evolution under SULI (prove stability and variance reduction).
6. Scale up networks to large sizes (show it still works).
7. Statistical roll-up (multiple random seeds; consistency; no cherry-picking).

Headline numbers:
- 32+ million total training steps.
- All major configurations showed positive learning.
- Large improvements for deception-based defenders.

---
## 11. Key Metrics (≈2–3 min)
Plain language versions:
- Deception rate: Of all attacker moves, how many hit fakes?
- Protection rate: How many real machines stayed safe?
- Time to impact: How long until the attacker reaches something important? (Longer is better for us.)
- Steps delayed: How much extra wandering did deception cause?

Why they matter: They show not just “who won,” but how well we slowed, diverted, and protected.

---
## 12. Main Results & Impact (≈4 min)
Core findings:
- Deception strategies clearly outperformed plain detection strategies.
- Stable training meant less wasted compute and time (no constant restarts).
- Large networks: Method still held up without collapsing accuracy.
- Variance (run-to-run randomness) went down, so results are more dependable.

Practical meaning:
- Organizations can invest in automated training loops instead of manual tuning cycles.
- Decoys become a planned optimization lever, not a side experiment.
- Early diversion of attackers reduces chance of deep, costly compromise.

---
## 13. Integrity, Limits, and Honesty (≈3 min)
What we did well:
- Transparent multi-seed experiments (different random starts) all improved.
- Comprehensive coverage: attacker realism via 295 techniques.
- Clear, reproducible workflow.

Limits:
- All tests in simulation so far; real deployment is future work.
- We have not benchmarked against commercial products yet.
- Network changes during an episode (dynamic topology) not yet modeled.
- No formal mathematical convergence proof—evidence is empirical.

Future work targets each of those.

---
## 14. Methodology Snapshot (≈2 min)
Think of the whole system as a training gym:
- We generate realistic attack behavior.
- We let defense strategies adapt continuously.
- We measure, rebalance, and scale.
- We repeat under different conditions to gain confidence.

---
## 15. Conclusion & Takeaway (≈3 min)
Single sentence summary: Cyberwheel shows we can stably train AI defenders by pairing them with learning AI attackers, using deception as a central strategy, and scaling that process to enterprise-sized networks.

Three pillars:
1. Stability (SULI): Makes adversarial training reliable.
2. Deception optimization: Turns decoys into a measurable, high-impact control.
3. Scale & rigor: Big networks, many runs, consistent outcomes.

Executive takeaway: Earlier attacker diversion + stable automated training = lower breach risk and lower long-term defense cost.

What’s next:
- Real-world pilot deployments.
- Smarter adaptive deception (dynamic rotating decoys).
- Integration with existing SOC tooling.
- Deeper theory (formal proofs) and cross-domain applications.

Thank you. I’m happy to take questions.

---
## Optional Fast Answers (If Asked)
- Why 10× deception reward? To ensure learning strongly values trapping attackers early; experiments confirm it drives better defensive delay.
- How do you know it’s stable? Failure rate dropped sharply versus typical multi-agent baselines.
- What makes it practical? Works from small lab networks up to thousands of hosts with consistent improvement curves.
- Biggest limitation? All simulation so far—live deployment is future validation.

---
## Micro Glossary (Plain Words)
- Decoy/Honeypot: Fake system that looks real to an attacker.
- Seed: Different random starting point to check consistency.
- Policy: The agent’s habit for choosing actions.
- Episode: One simulated attack / defense scenario run-through.
- Step: A single decision moment in an episode.

---
## Presenter Reminders (Not Spoken)
- Keep analogies (town, sparring, gym) consistent.
- Pause after each section title; let the panel reset.
- If time is short, trim detailed phase list (Section 10) and metric explanations.
- Emphasize “stability + deception + scale” triad repeatedly.

End of simplified script.
