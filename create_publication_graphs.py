#!/usr/bin/env python3
"""
Create publication-ready graphs from Cyberwheel training data
"""

import matplotlib.pyplot as plt
import numpy as np
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import pandas as pd

# Set publication-quality style
plt.style.use('seaborn-v0_8')
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 18
})

def extract_training_data(log_file, label):
    """Extract training data from tensorboard log"""
    ea = EventAccumulator(log_file)
    ea.Reload()
    
    # Extract episodic returns
    returns = ea.Scalars('charts/episodic_return')
    steps = [r.step for r in returns]
    values = [r.value for r in returns]
    
    return pd.DataFrame({
        'step': steps,
        'episodic_return': values,
        'experiment': label
    })

def create_figure_1_training_convergence():
    """Figure 1: Training Convergence Comparison"""
    
    # Load data from different experiments
    experiments = {
        'Blue Agent (High Decoy)': 'C:/Users/mirac/Documents/Git/cyberwheel-IX/cyberwheel-complete/cyberwheel/data/runs/Phase2_Blue_HighDecoy_HPC/events.out.tfevents.1754578964.cx3-12-23.cx3.hpc.ic.ac.uk.2455839.0',
        'Blue Agent (Medium)': 'C:/Users/mirac/Documents/Git/cyberwheel-IX/cyberwheel-complete/cyberwheel/data/runs/Phase2_Blue_Medium_HPC/events.out.tfevents.1754578964.cx3-12-23.cx3.hpc.ic.ac.uk.2455840.0',
        'Blue Agent (Perfect Detection)': 'C:/Users/mirac/Documents/Git/cyberwheel-IX/cyberwheel-complete/cyberwheel/data/runs/Phase2_Blue_PerfectDetection_HPC/events.out.tfevents.1754578978.cx3-12-24.cx3.hpc.ic.ac.uk.1368478.0'
    }
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    colors = ['#2E86AB', '#A23B72', '#F18F01']
    
    for i, (label, log_file) in enumerate(experiments.items()):
        try:
            data = extract_training_data(log_file, label)
            
            # Smooth the data for better visualization
            window_size = max(1, len(data) // 50)
            if len(data) > window_size:
                smoothed_returns = data['episodic_return'].rolling(window=window_size, center=True).mean()
                ax.plot(data['step'], smoothed_returns, 
                       label=label, color=colors[i], linewidth=2.5, alpha=0.8)
                
                # Add confidence interval (using rolling std)
                smoothed_std = data['episodic_return'].rolling(window=window_size, center=True).std()
                ax.fill_between(data['step'], 
                              smoothed_returns - smoothed_std, 
                              smoothed_returns + smoothed_std,
                              color=colors[i], alpha=0.2)
            else:
                ax.plot(data['step'], data['episodic_return'], 
                       label=label, color=colors[i], linewidth=2.5, alpha=0.8)
                
        except Exception as e:
            print(f"Could not load {label}: {e}")
    
    ax.set_xlabel('Training Steps', fontweight='bold')
    ax.set_ylabel('Episodic Return', fontweight='bold')
    ax.set_title('Training Convergence: Blue Agent Variants', fontweight='bold', pad=20)
    ax.legend(loc='lower right', frameon=True, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('Figure1_Training_Convergence.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig

def create_figure_2_performance_comparison():
    """Figure 2: Performance Comparison Bar Chart"""
    
    # Performance data extracted from our analysis
    experiments = ['High Decoy', 'Medium', 'Perfect Detection']
    final_returns = [-246.75, -259.31, None]  # Perfect Detection data pending
    best_returns = [-192.44, -185.44, None]
    training_steps = [6250, 10000, None]
    
    # Filter out None values
    valid_data = [(exp, final, best, steps) for exp, final, best, steps in 
                  zip(experiments, final_returns, best_returns, training_steps) 
                  if final is not None]
    
    if len(valid_data) < 2:
        print("Insufficient data for performance comparison")
        return None
    
    experiments, final_returns, best_returns, training_steps = zip(*valid_data)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Bar chart for final performance
    x_pos = np.arange(len(experiments))
    bars1 = ax1.bar(x_pos, final_returns, color=['#2E86AB', '#A23B72'], alpha=0.8)
    bars2 = ax1.bar(x_pos, best_returns, color=['#87CEEB', '#DDA0DD'], alpha=0.6, 
                    label='Best Performance')
    
    ax1.set_xlabel('Blue Agent Configuration', fontweight='bold')
    ax1.set_ylabel('Episodic Return', fontweight='bold')
    ax1.set_title('Final vs Best Performance', fontweight='bold')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(experiments)
    ax1.legend(['Final Performance', 'Best Performance'])
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, value in zip(bars1, final_returns):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
    
    # Training efficiency (steps to convergence)
    bars3 = ax2.bar(x_pos, training_steps, color=['#F18F01', '#C73E1D'], alpha=0.8)
    ax2.set_xlabel('Blue Agent Configuration', fontweight='bold')
    ax2.set_ylabel('Training Steps', fontweight='bold')
    ax2.set_title('Training Efficiency', fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(experiments)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, value in zip(bars3, training_steps):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 100,
                f'{value}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('Figure2_Performance_Comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig

def create_figure_3_action_analysis():
    """Figure 3: Action Analysis from CSV logs"""
    
    # Load action log data
    try:
        high_decoy_data = pd.read_csv('C:/Users/mirac/Documents/Git/cyberwheel-IX/cyberwheel-complete/cyberwheel/data/action_logs/Phase2_Blue_HighDecoy_HPC_Interactive.csv')
        medium_data = pd.read_csv('C:/Users/mirac/Documents/Git/cyberwheel-IX/cyberwheel-complete/cyberwheel/data/action_logs/Phase2_Blue_Medium_HPC_Interactive.csv')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Blue action frequency analysis
        high_decoy_actions = high_decoy_data['blue_action'].value_counts()
        medium_actions = medium_data['blue_action'].value_counts()
        
        # Plot action distributions
        actions = list(set(high_decoy_actions.index) | set(medium_actions.index))
        high_counts = [high_decoy_actions.get(action, 0) for action in actions]
        medium_counts = [medium_actions.get(action, 0) for action in actions]
        
        x = np.arange(len(actions))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, high_counts, width, label='High Decoy', color='#2E86AB', alpha=0.8)
        bars2 = ax1.bar(x + width/2, medium_counts, width, label='Medium', color='#A23B72', alpha=0.8)
        
        ax1.set_xlabel('Blue Agent Actions', fontweight='bold')
        ax1.set_ylabel('Action Frequency', fontweight='bold')
        ax1.set_title('Blue Agent Action Distribution', fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(actions, rotation=45)
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Red action success rate analysis
        high_success_rate = high_decoy_data['red_action_success'].mean() * 100
        medium_success_rate = medium_data['red_action_success'].mean() * 100
        
        success_rates = [high_success_rate, medium_success_rate]
        configs = ['High Decoy', 'Medium']
        
        bars3 = ax2.bar(configs, success_rates, color=['#F18F01', '#C73E1D'], alpha=0.8)
        ax2.set_ylabel('Red Agent Success Rate (%)', fontweight='bold')
        ax2.set_title('Red Agent Attack Success Rate', fontweight='bold')
        ax2.set_ylim(0, 100)
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, value in zip(bars3, success_rates):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{value:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('Figure3_Action_Analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
        
    except Exception as e:
        print(f"Could not create action analysis: {e}")
        return None

def create_summary_table():
    """Create a summary table of experimental results"""
    
    results = {
        'Configuration': ['High Decoy', 'Medium', 'Validation'],
        'Training Steps': [6250, 10000, 10],
        'Final Return': [-246.75, -259.31, -97.00],
        'Best Return': [-192.44, -185.44, 180.50],
        'Improvement': [47.31, 45.63, 'N/A'],  # Initial - Final
        'HPC Deployment': ['✓', '✓', '✓']
    }
    
    df = pd.DataFrame(results)
    print("\nExperimental Results Summary:")
    print("=" * 80)
    print(df.to_string(index=False))
    
    # Save to CSV for paper inclusion
    df.to_csv('Table1_Experimental_Results.csv', index=False)
    
    return df

if __name__ == "__main__":
    print("Creating publication-ready graphs from Cyberwheel data...")
    
    # Create figures
    fig1 = create_figure_1_training_convergence()
    fig2 = create_figure_2_performance_comparison()
    fig3 = create_figure_3_action_analysis()
    
    # Create summary table
    summary_df = create_summary_table()
    
    print("\nPublication-ready materials created:")
    print("- Figure1_Training_Convergence.png")
    print("- Figure2_Performance_Comparison.png") 
    print("- Figure3_Action_Analysis.png")
    print("- Table1_Experimental_Results.csv")
    print("\nThese can be directly included in your research paper.")