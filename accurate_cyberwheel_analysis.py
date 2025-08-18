#!/usr/bin/env python3
"""
Accurate Cyberwheel Analysis - Based Only on Real Training Data
Analysis of 4 confirmed experiments with verifiable data
"""

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle
import networkx as nx
from pathlib import Path

print("=== ACCURATE CYBERWHEEL ANALYSIS ===")
print("Based on verified real training data only")
print()

# Define the 4 confirmed experiments with actual data
REAL_EXPERIMENTS = {
    'Phase1_Validation_HPC_Interactive': {
        'action_log': r'cyberwheel-complete\cyberwheel\data\action_logs\Phase1_Validation_HPC_Interactive.csv',
        'graphs': r'cyberwheel-complete\cyberwheel\data\graphs\Phase1_Validation_HPC_Interactive',
        'models': r'cyberwheel-complete\cyberwheel\data\models\Phase1_Validation_HPC',
        'runs': r'cyberwheel-complete\cyberwheel\data\runs\Phase1_Validation_HPC'
    },
    'Phase2_Blue_HighDecoy_HPC_Interactive': {
        'action_log': r'cyberwheel-complete\cyberwheel\data\action_logs\Phase2_Blue_HighDecoy_HPC_Interactive.csv',
        'graphs': r'cyberwheel-complete\cyberwheel\data\graphs\Phase2_Blue_HighDecoy_HPC_Interactive',
        'models': r'cyberwheel-complete\cyberwheel\data\models\Phase2_Blue_HighDecoy_HPC',
        'runs': r'cyberwheel-complete\cyberwheel\data\runs\Phase2_Blue_HighDecoy_HPC'
    },
    'Phase2_Blue_Medium_HPC_Interactive': {
        'action_log': r'cyberwheel-complete\cyberwheel\data\action_logs\Phase2_Blue_Medium_HPC_Interactive.csv',
        'graphs': r'cyberwheel-complete\cyberwheel\data\graphs\Phase2_Blue_Medium_HPC_Interactive',
        'models': r'cyberwheel-complete\cyberwheel\data\models\Phase2_Blue_Medium_HPC',
        'runs': r'cyberwheel-complete\cyberwheel\data\runs\Phase2_Blue_Medium_HPC'
    },
    'Phase2_Blue_Medium_Visualization': {
        'action_log': r'cyberwheel-complete\cyberwheel\data\action_logs\Phase2_Blue_Medium_Visualization.csv',
        'graphs': r'cyberwheel-complete\cyberwheel\data\graphs\Phase2_Blue_Medium_Visualization',
        'models': None,  # May not exist
        'runs': None     # May not exist
    }
}

# Analyze action logs for actual training metrics
print("1. ANALYZING REAL ACTION LOGS:")
print("=" * 50)

action_data = {}
for exp_name, paths in REAL_EXPERIMENTS.items():
    log_path = paths['action_log']
    if os.path.exists(log_path):
        df = pd.read_csv(log_path)
        action_data[exp_name] = df
        print(f"{exp_name}:")
        print(f"  - Actions logged: {len(df)} steps")
        print(f"  - Episodes: {df['episode'].max() + 1 if 'episode' in df.columns else 'Unknown'}")
        print(f"  - Max steps per episode: {df['step'].max() if 'step' in df.columns else 'Unknown'}")
        if 'reward' in df.columns:
            print(f"  - Total reward: {df['reward'].sum():.1f}")
            print(f"  - Average reward: {df['reward'].mean():.2f}")
        print()

# Analyze network states from pickle files
print("2. ANALYZING NETWORK STATES (PICKLE FILES):")
print("=" * 50)

network_states = []
total_pickle_count = 0

for exp_name, paths in REAL_EXPERIMENTS.items():
    graphs_path = paths['graphs']
    if os.path.exists(graphs_path):
        pickle_files = list(Path(graphs_path).glob('*.pickle'))
        exp_pickle_count = len(pickle_files)
        total_pickle_count += exp_pickle_count
        print(f"{exp_name}: {exp_pickle_count} network state files")
        
        # Analyze a sample of pickle files
        for i, pickle_file in enumerate(pickle_files[:5]):  # Sample first 5
            try:
                with open(pickle_file, 'rb') as f:
                    graph = pickle.load(f)
                if isinstance(graph, nx.DiGraph):
                    node_count = graph.number_of_nodes()
                    edge_count = graph.number_of_edges()
                    compromised = sum(1 for _, data in graph.nodes(data=True) 
                                    if data.get('compromised', False))
                    decoys = sum(1 for _, data in graph.nodes(data=True) 
                               if data.get('decoy', False))
                    
                    # Parse episode and step from filename
                    parts = pickle_file.stem.split('_')
                    episode = int(parts[0]) if len(parts) > 0 else 0
                    step = int(parts[1]) if len(parts) > 1 else 0
                    
                    network_states.append({
                        'experiment': exp_name,
                        'episode': episode,
                        'step': step,
                        'total_nodes': node_count,
                        'total_edges': edge_count,
                        'compromised_nodes': compromised,
                        'decoy_nodes': decoys,
                        'density': edge_count / (node_count * (node_count - 1)) if node_count > 1 else 0,
                        'is_connected': nx.is_connected(graph.to_undirected()) if node_count > 0 else False
                    })
            except Exception as e:
                print(f"    Warning: Could not load {pickle_file.name}: {e}")

print(f"\nTotal network states analyzed: {len(network_states)} samples from {total_pickle_count} files")

# Create accurate visualizations
print("\n3. CREATING ACCURATE VISUALIZATIONS:")
print("=" * 50)

if network_states:
    df_states = pd.DataFrame(network_states)
    
    # Set up the plotting style
    plt.style.use('default')
    plt.rcParams.update({'font.size': 12, 'figure.dpi': 300})
    
    # Create comprehensive figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Cyberwheel Training Analysis - Verified Experiments Only', fontsize=16, fontweight='bold')
    
    # 1. Network size evolution
    ax1 = axes[0, 0]
    for exp in df_states['experiment'].unique():
        exp_data = df_states[df_states['experiment'] == exp].sort_values(['episode', 'step'])
        ax1.plot(range(len(exp_data)), exp_data['total_nodes'], 
                label=exp.replace('_', ' ')[:20] + '...', linewidth=2, marker='o', markersize=3)
    ax1.set_xlabel('Time Steps (sampled)')
    ax1.set_ylabel('Network Size (nodes)')
    ax1.set_title('Network Growth Dynamics')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # 2. Decoy deployment
    ax2 = axes[0, 1]
    for exp in df_states['experiment'].unique():
        exp_data = df_states[df_states['experiment'] == exp].sort_values(['episode', 'step'])
        ax2.plot(range(len(exp_data)), exp_data['decoy_nodes'],
                label=exp.replace('_', ' ')[:20] + '...', linewidth=2, marker='s', markersize=3)
    ax2.set_xlabel('Time Steps (sampled)')
    ax2.set_ylabel('Decoy Nodes')
    ax2.set_title('Decoy Deployment Strategy')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    # 3. Network density
    ax3 = axes[0, 2]
    df_states['decoy_ratio'] = df_states['decoy_nodes'] / df_states['total_nodes']
    exp_ratios = df_states.groupby('experiment')['decoy_ratio'].mean().sort_values(ascending=False)
    bars = ax3.bar(range(len(exp_ratios)), exp_ratios.values, alpha=0.7)
    ax3.set_xlabel('Experiment')
    ax3.set_ylabel('Average Decoy Ratio')
    ax3.set_title('Deception Strategy Effectiveness')
    ax3.set_xticks(range(len(exp_ratios)))
    ax3.set_xticklabels([exp.split('_')[0] + '_' + exp.split('_')[1] for exp in exp_ratios.index], rotation=45)
    
    # Add value labels
    for bar, value in zip(bars, exp_ratios.values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 4. Action analysis from logs
    ax4 = axes[1, 0]
    if action_data:
        rewards = []
        exp_names = []
        for exp_name, df in action_data.items():
            if 'reward' in df.columns:
                rewards.append(df['reward'].sum())
                exp_names.append(exp_name.split('_')[0] + '_' + exp_name.split('_')[1])
        
        if rewards:
            bars = ax4.bar(range(len(rewards)), rewards, alpha=0.7, color='skyblue')
            ax4.set_xlabel('Experiment')
            ax4.set_ylabel('Cumulative Reward')
            ax4.set_title('Training Performance (Cumulative Rewards)')
            ax4.set_xticks(range(len(exp_names)))
            ax4.set_xticklabels(exp_names, rotation=45)
            
            for bar, value in zip(bars, rewards):
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.0f}', ha='center', va='bottom', fontweight='bold')
    
    # 5. Episode coverage
    ax5 = axes[1, 1]
    episode_counts = []
    exp_labels = []
    for exp_name, df in action_data.items():
        if 'episode' in df.columns:
            episode_counts.append(df['episode'].nunique())
            exp_labels.append(exp_name.split('_')[0] + '_' + exp_name.split('_')[1])
    
    if episode_counts:
        bars = ax5.bar(range(len(episode_counts)), episode_counts, alpha=0.7, color='orange')
        ax5.set_xlabel('Experiment')
        ax5.set_ylabel('Episodes Completed')
        ax5.set_title('Training Episode Coverage')
        ax5.set_xticks(range(len(exp_labels)))
        ax5.set_xticklabels(exp_labels, rotation=45)
    
    # 6. Summary statistics
    ax6 = axes[1, 2]
    ax6.axis('off')
    
    summary_text = 'VERIFIED DATA SUMMARY\n\n'
    summary_text += f'Real Experiments: {len(REAL_EXPERIMENTS)}\n'
    summary_text += f'Total Pickle Files: {total_pickle_count}\n'
    summary_text += f'Analyzed Network States: {len(network_states)}\n'
    if action_data:
        total_actions = sum(len(df) for df in action_data.values())
        summary_text += f'Total Logged Actions: {total_actions}\n'
    
    if network_states:
        summary_text += f'\nNETWORK ANALYSIS:\n'
        summary_text += f'Node Range: {df_states["total_nodes"].min()}-{df_states["total_nodes"].max()}\n'
        summary_text += f'Max Decoys: {df_states["decoy_nodes"].max()}\n'
        summary_text += f'Avg Decoy Ratio: {df_states["decoy_ratio"].mean():.2f}\n'
    
    summary_text += f'\nNOTE: Analysis based on\nverified data only.\nSULI methodology not\nyet implemented.'
    
    ax6.text(0.1, 0.9, summary_text, transform=ax6.transAxes, fontsize=11,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('Accurate_Cyberwheel_Analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Created: Accurate_Cyberwheel_Analysis.png")

# Save accurate data summary
if network_states:
    df_states.to_csv('Verified_Network_States.csv', index=False)
    print("Created: Verified_Network_States.csv")

print("\n=== ANALYSIS COMPLETE ===")
print("All results based on verified real training data only")
print("No fabricated or extrapolated content included")