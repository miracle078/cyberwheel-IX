#!/usr/bin/env python3
"""
Create missing visualizations for comprehensive Cyberwheel analysis
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import os
import pickle

print('=== CREATING MISSING CYBERWHEEL VISUALIZATIONS ===')

# Load experimental data
df = pd.read_csv('COMPREHENSIVE_EXPERIMENTAL_RESULTS.csv')
runs_dir = r'C:\Users\mirac\Documents\Git\cyberwheel-IX\cyberwheel-complete\cyberwheel\data\runs'

# Set publication style
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'font.size': 10,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9
})

# 1. SULI EVALUATION METRICS COMPREHENSIVE ANALYSIS
print('Creating SULI Evaluation Metrics Analysis...')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('SULI Evaluation Metrics - Comprehensive Analysis', fontsize=16, fontweight='bold')

# Extract evaluation metrics from all experiments
eval_data = []
metric_names = [
    ('evaluation/time_step_till_impact_avg', 'Time to Impact (steps)'),
    ('evaluation/steps_delayed_avg', 'Steps Delayed'), 
    ('evaluation/first_step_of_decoy_contact_avg', 'First Decoy Contact'),
    ('evaluation/impacted_decoys_avg', 'Impacted Decoys')
]

for _, row in df.iterrows():
    exp_name = row['Experiment']
    run_path = os.path.join(runs_dir, exp_name)
    
    exp_metrics = {'Experiment': exp_name}
    try:
        ea = EventAccumulator(run_path)
        ea.Reload()
        
        for metric_key, metric_display in metric_names:
            if metric_key in ea.Tags()['scalars']:
                scalar_events = ea.Scalars(metric_key)
                if scalar_events:
                    exp_metrics[metric_display] = scalar_events[-1].value
                else:
                    exp_metrics[metric_display] = 0
            else:
                exp_metrics[metric_display] = 0
        
        eval_data.append(exp_metrics)
    except Exception as e:
        print(f"Error processing {exp_name}: {e}")
        continue

eval_df = pd.DataFrame(eval_data)

# Create individual metric plots
if not eval_df.empty:
    axes = [ax1, ax2, ax3, ax4]
    colors = plt.cm.Set3(np.linspace(0, 1, len(eval_df)))
    
    for i, (_, metric_display) in enumerate(metric_names):
        if i < 4 and metric_display in eval_df.columns:
            values = eval_df[metric_display].values
            exp_names = [name.replace('_', ' ') for name in eval_df['Experiment']]
            
            bars = axes[i].bar(range(len(values)), values, color=colors, alpha=0.7)
            axes[i].set_xticks(range(len(exp_names)))
            axes[i].set_xticklabels(exp_names, rotation=45, ha='right', fontsize=8)
            axes[i].set_ylabel(metric_display)
            axes[i].set_title(f'{metric_display} by Experiment')
            axes[i].grid(axis='y', alpha=0.3)
            
            # Add value labels
            for j, bar in enumerate(bars):
                height = bar.get_height()
                if height > 0:
                    axes[i].text(bar.get_x() + bar.get_width()/2., height + max(values) * 0.02,
                                f'{height:.1f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('SULI_EVALUATION_COMPREHENSIVE_ANALYSIS.png', dpi=300, bbox_inches='tight')
print('Created: SULI_EVALUATION_COMPREHENSIVE_ANALYSIS.png')
plt.close()

# 2. MULTI-AGENT INTERACTION DYNAMICS
print('Creating Multi-Agent Interaction Analysis...')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
fig.suptitle('Multi-Agent Interaction Dynamics Analysis', fontsize=16, fontweight='bold')

# Load action logs for behavioral analysis
action_logs_dir = r'C:\Users\mirac\Documents\Git\cyberwheel-IX\cyberwheel-complete\cyberwheel\data\action_logs'
interaction_data = []

if os.path.exists(action_logs_dir):
    csv_files = [f for f in os.listdir(action_logs_dir) if f.endswith('.csv')]
    
    for csv_file in csv_files:
        try:
            df_actions = pd.read_csv(os.path.join(action_logs_dir, csv_file))
            
            if len(df_actions) > 0:
                # Analyze red-blue interaction patterns
                red_success_rate = df_actions['red_action_success'].mean() if 'red_action_success' in df_actions.columns else 0
                avg_reward = df_actions['reward'].mean() if 'reward' in df_actions.columns else 0
                blue_actions = df_actions['blue_action'].value_counts() if 'blue_action' in df_actions.columns else {}
                
                interaction_data.append({
                    'Experiment': csv_file.replace('.csv', '').replace('_Interactive', ''),
                    'Red_Success_Rate': red_success_rate,
                    'Avg_Reward': avg_reward,
                    'Total_Steps': len(df_actions),
                    'Dominant_Blue_Action': blue_actions.index[0] if len(blue_actions) > 0 else 'unknown'
                })
        except Exception as e:
            print(f"Error processing {csv_file}: {e}")
            continue

if interaction_data:
    interaction_df = pd.DataFrame(interaction_data)
    
    # Red success rate comparison
    bars1 = ax1.bar(range(len(interaction_df)), interaction_df['Red_Success_Rate'], 
                   color=plt.cm.Reds(np.linspace(0.3, 0.8, len(interaction_df))), alpha=0.7)
    ax1.set_xticks(range(len(interaction_df)))
    ax1.set_xticklabels([name.replace('_', ' ') for name in interaction_df['Experiment']], 
                       rotation=45, ha='right')
    ax1.set_ylabel('Red Agent Success Rate')
    ax1.set_title('Red Agent Success Rate by Experiment')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, bar in enumerate(bars1):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.3f}', ha='center', va='bottom', fontsize=9)
    
    # Reward vs interaction complexity
    scatter = ax2.scatter(interaction_df['Total_Steps'], interaction_df['Avg_Reward'],
                         s=interaction_df['Red_Success_Rate']*200, 
                         c=range(len(interaction_df)), cmap='viridis', alpha=0.7)
    ax2.set_xlabel('Total Interaction Steps')
    ax2.set_ylabel('Average Reward')
    ax2.set_title('Reward vs Interaction Complexity')
    ax2.grid(True, alpha=0.3)
    
    # Add experiment labels
    for i, row in interaction_df.iterrows():
        ax2.annotate(row['Experiment'].replace('_', ' '), 
                    (row['Total_Steps'], row['Avg_Reward']),
                    xytext=(5, 5), textcoords='offset points', fontsize=8)

plt.tight_layout()
plt.savefig('MULTI_AGENT_INTERACTION_DYNAMICS.png', dpi=300, bbox_inches='tight')
print('Created: MULTI_AGENT_INTERACTION_DYNAMICS.png')
plt.close()

# 3. TRAINING EFFICIENCY AND SCALABILITY
print('Creating Training Efficiency Analysis...')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Training Efficiency and Scalability Analysis', fontsize=16, fontweight='bold')

# Steps vs Performance Efficiency
ax1.scatter(df['Total_Steps']/1000000, df['Improvement']/df['Total_Steps']*1000000, 
           s=df['Episodes']/50, alpha=0.7, c=range(len(df)), cmap='plasma')
ax1.set_xlabel('Training Steps (Millions)')
ax1.set_ylabel('Improvement per Million Steps')
ax1.set_title('Training Efficiency (Improvement/Steps)')
ax1.grid(True, alpha=0.3)

# Episodes vs Performance Relationship
ax2.scatter(df['Episodes']/1000, df['Final_Return'], 
           s=df['Total_Steps']/100000, alpha=0.7, c=df['Improvement'], cmap='RdYlGn')
ax2.set_xlabel('Episodes (Thousands)')
ax2.set_ylabel('Final Performance')
ax2.set_title('Episodes vs Final Performance')
ax2.grid(True, alpha=0.3)

# Scale category analysis
scale_categories = []
for _, row in df.iterrows():
    if row['Total_Steps'] <= 10000:
        scale_categories.append('Validation')
    elif row['Total_Steps'] <= 1000000:
        scale_categories.append('Small Scale')
    elif row['Total_Steps'] <= 5000000:
        scale_categories.append('Medium Scale')
    else:
        scale_categories.append('Large Scale')

df['Scale_Category'] = scale_categories

# Performance by scale category
scale_perf = df.groupby('Scale_Category')['Final_Return'].agg(['mean', 'std', 'count'])
categories = scale_perf.index
means = scale_perf['mean'].values
stds = scale_perf['std'].fillna(0).values

bars3 = ax3.bar(categories, means, yerr=stds, capsize=5, 
               color=plt.cm.Set2(np.linspace(0, 1, len(categories))), alpha=0.7)
ax3.set_ylabel('Average Final Return')
ax3.set_title('Performance by Training Scale')
ax3.grid(axis='y', alpha=0.3)

# Add value labels
for i, (bar, mean) in enumerate(zip(bars3, means)):
    ax3.text(bar.get_x() + bar.get_width()/2., mean + stds[i] + max(means) * 0.02,
            f'{mean:.1f}', ha='center', va='bottom', fontsize=9)

# Improvement distribution
ax4.hist(df['Improvement'], bins=6, color='lightblue', alpha=0.7, edgecolor='black')
ax4.axvline(df['Improvement'].mean(), color='red', linestyle='--', linewidth=2, 
           label=f'Mean: {df["Improvement"].mean():.1f}')
ax4.set_xlabel('Performance Improvement')
ax4.set_ylabel('Number of Experiments')
ax4.set_title('Performance Improvement Distribution')
ax4.legend()
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('TRAINING_EFFICIENCY_SCALABILITY.png', dpi=300, bbox_inches='tight')
print('Created: TRAINING_EFFICIENCY_SCALABILITY.png')
plt.close()

# 4. NETWORK TOPOLOGY IMPACT ANALYSIS
print('Creating Network Topology Analysis...')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
fig.suptitle('Network Topology and Deception Strategy Impact', fontsize=16, fontweight='bold')

# Extract agent configuration types from experiment names
config_analysis = []
for _, row in df.iterrows():
    exp_name = row['Experiment']
    
    # Determine configuration type
    if 'HighDecoy' in exp_name:
        config_type = 'High Decoy'
    elif 'LowDecoy' in exp_name:
        config_type = 'Low Decoy'
    elif 'PerfectDetection' in exp_name:
        config_type = 'Perfect Detection'
    elif 'Medium' in exp_name:
        config_type = 'Medium Detection'
    elif 'Small' in exp_name:
        config_type = 'Small Network'
    else:
        config_type = 'Standard'
    
    config_analysis.append({
        'Experiment': exp_name,
        'Config_Type': config_type,
        'Final_Return': row['Final_Return'],
        'Improvement': row['Improvement'],
        'Episodes': row['Episodes']
    })

config_df = pd.DataFrame(config_analysis)

# Performance by configuration type
config_perf = config_df.groupby('Config_Type')['Final_Return'].agg(['mean', 'count'])
config_types = config_perf.index
means = config_perf['mean'].values
counts = config_perf['count'].values

bars1 = ax1.bar(config_types, means, 
               color=plt.cm.Set1(np.linspace(0, 1, len(config_types))), alpha=0.7)
ax1.set_ylabel('Average Final Return')
ax1.set_title('Performance by Agent Configuration')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(axis='y', alpha=0.3)

# Add count labels
for bar, mean, count in zip(bars1, means, counts):
    ax1.text(bar.get_x() + bar.get_width()/2., mean + max(means) * 0.02,
            f'{mean:.1f}\n(n={count})', ha='center', va='bottom', fontsize=9)

# Configuration vs improvement
config_imp = config_df.groupby('Config_Type')['Improvement'].mean()
bars2 = ax2.bar(config_imp.index, config_imp.values,
               color=plt.cm.RdYlGn(np.linspace(0.2, 0.8, len(config_imp))), alpha=0.7)
ax2.set_ylabel('Average Improvement')
ax2.set_title('Learning Improvement by Configuration')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(axis='y', alpha=0.3)

# Add value labels
for bar, imp in zip(bars2, config_imp.values):
    ax2.text(bar.get_x() + bar.get_width()/2., imp + max(config_imp.values) * 0.02,
            f'{imp:.1f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('NETWORK_TOPOLOGY_IMPACT_ANALYSIS.png', dpi=300, bbox_inches='tight')
print('Created: NETWORK_TOPOLOGY_IMPACT_ANALYSIS.png')
plt.close()

print('\n=== MISSING VISUALIZATIONS CREATION COMPLETE ===')
print('Created 4 new comprehensive visualizations:')
print('1. SULI_EVALUATION_COMPREHENSIVE_ANALYSIS.png')
print('2. MULTI_AGENT_INTERACTION_DYNAMICS.png') 
print('3. TRAINING_EFFICIENCY_SCALABILITY.png')
print('4. NETWORK_TOPOLOGY_IMPACT_ANALYSIS.png')
print('\n=== TOTAL VISUALIZATION SUITE ===')
print('Existing files retained:')
print('- Accurate_Cyberwheel_Analysis.png (4-panel main analysis)')
print('- Figure2_Performance_Comparison.png (performance bars)')
print('- Training_Convergence.png (basic convergence)')
print('- Episode_Performance_Analysis.png (improvement analysis)')
print('- Comprehensive_Training_Curves_All_Metrics.png (detailed metrics)')