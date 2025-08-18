#!/usr/bin/env python3
"""
Network Dynamics Analysis from 890 Pickle Files
"""

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the network analysis data
df = pd.read_csv('Network_States_Analysis.csv')

print('Creating comprehensive network dynamics visualizations...')

# Set style
plt.style.use('default')
plt.rcParams.update({'font.size': 10, 'figure.dpi': 300})

# Create comprehensive figure
fig = plt.figure(figsize=(20, 16))

# 1. Network Growth Over Time
ax1 = plt.subplot(3, 3, 1)
for exp in df['experiment'].unique():
    exp_data = df[df['experiment'] == exp].sort_values(['episode', 'step'])
    ax1.plot(range(len(exp_data)), exp_data['total_nodes'], 
            label=exp.replace('_', ' '), linewidth=2, alpha=0.8)
ax1.set_xlabel('Time Steps')
ax1.set_ylabel('Total Nodes')
ax1.set_title('Network Growth Dynamics')
ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax1.grid(True, alpha=0.3)

# 2. Decoy Deployment Strategy
ax2 = plt.subplot(3, 3, 2) 
for exp in df['experiment'].unique():
    exp_data = df[df['experiment'] == exp].sort_values(['episode', 'step'])
    ax2.plot(range(len(exp_data)), exp_data['decoy_nodes'], 
            label=exp.replace('_', ' '), linewidth=2, alpha=0.8)
ax2.set_xlabel('Time Steps')
ax2.set_ylabel('Decoy Nodes Deployed')
ax2.set_title('Deception Strategy Evolution')
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax2.grid(True, alpha=0.3)

# 3. Network Density Evolution
ax3 = plt.subplot(3, 3, 3)
for exp in df['experiment'].unique():
    exp_data = df[df['experiment'] == exp].sort_values(['episode', 'step'])
    ax3.plot(range(len(exp_data)), exp_data['density'], 
            label=exp.replace('_', ' '), linewidth=2, alpha=0.8)
ax3.set_xlabel('Time Steps')
ax3.set_ylabel('Network Density')
ax3.set_title('Topology Density Changes')
ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax3.grid(True, alpha=0.3)

# 4. Decoy Deployment Efficiency
ax4 = plt.subplot(3, 3, 4)
df['decoy_ratio'] = df['decoy_nodes'] / df['total_nodes']
exp_means = df.groupby('experiment')['decoy_ratio'].mean().sort_values(ascending=False)
bars = ax4.bar(range(len(exp_means)), exp_means.values, alpha=0.7, color='darkgreen')
ax4.set_xlabel('Experiment')
ax4.set_ylabel('Avg Decoy Ratio')
ax4.set_title('Deception Deployment Efficiency')
ax4.set_xticks(range(len(exp_means)))
ax4.set_xticklabels([exp.replace('_', '\n') for exp in exp_means.index], rotation=0, ha='center')

# Add value labels
for bar, value in zip(bars, exp_means.values):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
            f'{value:.2f}', ha='center', va='bottom', fontweight='bold')

# 5. Network Scale Comparison
ax5 = plt.subplot(3, 3, 5)
scale_data = df.groupby('experiment')['total_nodes'].agg(['mean', 'std']).sort_values('mean')
bars = ax5.bar(range(len(scale_data)), scale_data['mean'], 
              yerr=scale_data['std'], capsize=5, alpha=0.7, color='skyblue')
ax5.set_xlabel('Experiment')
ax5.set_ylabel('Average Network Size')
ax5.set_title('Network Scale Analysis')
ax5.set_xticks(range(len(scale_data)))
ax5.set_xticklabels([exp.replace('_', '\n') for exp in scale_data.index], rotation=0, ha='center')

# 6. Episode Analysis
ax6 = plt.subplot(3, 3, 6)
episode_coverage = df.groupby('experiment')['episode'].nunique()
bars = ax6.bar(range(len(episode_coverage)), episode_coverage.values, alpha=0.7, color='orange')
ax6.set_xlabel('Experiment')
ax6.set_ylabel('Number of Episodes')
ax6.set_title('Episode Coverage by Experiment')
ax6.set_xticks(range(len(episode_coverage)))
ax6.set_xticklabels([exp.replace('_', '\n') for exp in episode_coverage.index], rotation=0, ha='center')

# 7. Detailed Episode Progression
ax7 = plt.subplot(3, 3, 7)
max_episodes_exp = episode_coverage.idxmax()
exp_data = df[df['experiment'] == max_episodes_exp]

for episode in sorted(exp_data['episode'].unique()):
    ep_data = exp_data[exp_data['episode'] == episode].sort_values('step')
    ax7.plot(ep_data['step'], ep_data['decoy_nodes'], 
            label=f'Episode {episode}', linewidth=2, marker='o', markersize=4)

ax7.set_xlabel('Step within Episode')
ax7.set_ylabel('Decoy Nodes')
ax7.set_title(f'Episode Progression: {max_episodes_exp.replace("_", " ")}')
ax7.legend()
ax7.grid(True, alpha=0.3)

# 8. Network Connectivity Analysis
ax8 = plt.subplot(3, 3, 8)
connectivity_stats = df.groupby('experiment')['is_connected'].mean()
bars = ax8.bar(range(len(connectivity_stats)), connectivity_stats.values, alpha=0.7, color='red')
ax8.set_xlabel('Experiment')
ax8.set_ylabel('Connectivity Rate')
ax8.set_title('Network Connectivity Stability')
ax8.set_xticks(range(len(connectivity_stats)))
ax8.set_xticklabels([exp.replace('_', '\n') for exp in connectivity_stats.index], rotation=0, ha='center')
ax8.set_ylim(0, 1.1)

# 9. Comprehensive Statistics Summary
ax9 = plt.subplot(3, 3, 9)
ax9.axis('off')

# Create summary statistics table
summary_text = 'NETWORK DYNAMICS SUMMARY\n\n'
summary_text += f'Total Network States Analyzed: {len(df)}\n'
summary_text += f'Experiments: {df["experiment"].nunique()}\n'
summary_text += f'Episodes Covered: {df["episode"].nunique()}\n'
summary_text += f'Max Steps in Episode: {df["step"].max()}\n\n'

summary_text += 'NETWORK SCALE RANGE:\n'
summary_text += f'Min Nodes: {df["total_nodes"].min()}\n'
summary_text += f'Max Nodes: {df["total_nodes"].max()}\n'
summary_text += f'Avg Nodes: {df["total_nodes"].mean():.1f}\n\n'

summary_text += 'DECOY DEPLOYMENT:\n'
summary_text += f'Max Decoys: {df["decoy_nodes"].max()}\n'
summary_text += f'Avg Decoys: {df["decoy_nodes"].mean():.1f}\n'
summary_text += f'Avg Decoy Ratio: {df["decoy_ratio"].mean():.2f}\n\n'

summary_text += 'TOPOLOGY CHARACTERISTICS:\n'
summary_text += f'Avg Density: {df["density"].mean():.3f}\n'
summary_text += f'Connectivity Rate: {df["is_connected"].mean():.1%}\n'

ax9.text(0.1, 0.9, summary_text, transform=ax9.transAxes, fontsize=10, 
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))

plt.suptitle('Comprehensive Network Dynamics Analysis: 890 Network States', 
             fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.subplots_adjust(top=0.95)
plt.savefig('Comprehensive_Network_Dynamics_Analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print('Created Comprehensive_Network_Dynamics_Analysis.png')

# Create detailed decoy analysis
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

# Decoy deployment heatmap by experiment and step
pivot_data = df.pivot_table(values='decoy_nodes', index='experiment', columns='step', aggfunc='mean')
sns.heatmap(pivot_data, ax=ax1, cmap='YlOrRd', cbar_kws={'label': 'Avg Decoy Nodes'})
ax1.set_title('Decoy Deployment Heatmap by Time')
ax1.set_xlabel('Step')
ax1.set_ylabel('Experiment')

# Network growth vs decoy deployment
scatter = ax2.scatter(df['total_nodes'], df['decoy_nodes'], alpha=0.6, c=df['density'], cmap='viridis')
ax2.set_xlabel('Total Nodes')
ax2.set_ylabel('Decoy Nodes')
ax2.set_title('Network Size vs Decoy Deployment')
plt.colorbar(scatter, ax=ax2, label='Network Density')

# Decoy efficiency by experiment
ax3.boxplot([df[df['experiment'] == exp]['decoy_ratio'].values for exp in df['experiment'].unique()],
           labels=[exp.replace('_', '\n') for exp in df['experiment'].unique()])
ax3.set_ylabel('Decoy Ratio (Decoys/Total Nodes)')
ax3.set_title('Decoy Deployment Efficiency Distribution')
ax3.tick_params(axis='x', rotation=45)

# Episode progression for validation experiment
validation_data = df[df['experiment'] == 'Phase1_Validation_HPC_Interactive']
for episode in sorted(validation_data['episode'].unique()):
    ep_data = validation_data[validation_data['episode'] == episode].sort_values('step')
    ax4.plot(ep_data['step'], ep_data['total_nodes'], 
            label=f'Episode {episode} - Nodes', linestyle='-', marker='o')
    ax4.plot(ep_data['step'], ep_data['decoy_nodes'], 
            label=f'Episode {episode} - Decoys', linestyle='--', marker='s')

ax4.set_xlabel('Step')
ax4.set_ylabel('Count')
ax4.set_title('Detailed Validation Episode Analysis')
ax4.legend()
ax4.grid(True, alpha=0.3)

plt.suptitle('Deep Decoy Strategy Analysis', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('Deep_Decoy_Strategy_Analysis.png', dpi=300, bbox_inches='tight')
plt.close()

print('Created Deep_Decoy_Strategy_Analysis.png')
print()
print('DEEP ANALYSIS COMPLETE:')
print('- Analyzed 890 network state snapshots')
print('- Tracked network growth from 20 to 213+ nodes')
print('- Massive decoy deployments (up to 204 decoys per state)')
print('- Multi-episode progression analysis')
print('- Topology evolution and connectivity patterns')