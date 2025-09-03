#!/usr/bin/env python3
"""
Extract and analyze tensorboard data from Cyberwheel training experiments
"""

from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

def extract_data_from_log(log_file, experiment_name):
    """Extract scalar data from a tensorboard log file"""
    try:
        ea = EventAccumulator(log_file)
        ea.Reload()
        
        data = {}
        for tag in ea.Tags()['scalars']:
            scalars = ea.Scalars(tag)
            steps = [s.step for s in scalars]
            values = [s.value for s in scalars]
            data[tag] = pd.DataFrame({'step': steps, 'value': values, 'experiment': experiment_name})
        
        return data
    except Exception as e:
        print(f"Error processing {log_file}: {e}")
        return {}

def analyze_all_experiments():
    """Analyze all available tensorboard logs"""
    runs_dir = "C:/Users/mirac/Documents/Git/cyberwheel-IX/cyberwheel-complete/cyberwheel/data/runs"
    
    experiments = {}
    
    # Find all experiment directories
    for exp_dir in os.listdir(runs_dir):
        exp_path = os.path.join(runs_dir, exp_dir)
        if os.path.isdir(exp_path) and exp_dir != 'README.md':
            # Look for tensorboard files
            tb_files = glob.glob(os.path.join(exp_path, "events.out.tfevents.*"))
            if tb_files:
                print(f"Processing experiment: {exp_dir}")
                # Take the most recent file if multiple
                log_file = max(tb_files, key=os.path.getctime)
                exp_data = extract_data_from_log(log_file, exp_dir)
                if exp_data:
                    experiments[exp_dir] = exp_data
    
    return experiments

def create_training_curves(experiments):
    """Create training curve plots"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Cyberwheel Training Results Analysis', fontsize=16)
    
    # Plot 1: Episodic Returns
    ax1 = axes[0,0]
    for exp_name, exp_data in experiments.items():
        if 'charts/episodic_return' in exp_data:
            data = exp_data['charts/episodic_return']
            ax1.plot(data['step'], data['value'], label=exp_name, alpha=0.8)
    ax1.set_xlabel('Training Steps')
    ax1.set_ylabel('Episodic Return')
    ax1.set_title('Training Progress: Episodic Returns')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Value Loss
    ax2 = axes[0,1]
    for exp_name, exp_data in experiments.items():
        if 'losses/value_loss' in exp_data:
            data = exp_data['losses/value_loss']
            # Smooth the data for better visualization
            if len(data) > 100:
                window = len(data) // 50
                smoothed = data['value'].rolling(window=window).mean()
                ax2.plot(data['step'], smoothed, label=exp_name, alpha=0.8)
    ax2.set_xlabel('Training Steps')
    ax2.set_ylabel('Value Loss')
    ax2.set_title('Training Stability: Value Loss')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: SULI Metrics - Time to Impact
    ax3 = axes[1,0]
    for exp_name, exp_data in experiments.items():
        if 'evaluation/time_step_till_impact_avg' in exp_data:
            data = exp_data['evaluation/time_step_till_impact_avg']
            ax3.plot(data['step'], data['value'], label=exp_name, alpha=0.8, marker='o', markersize=4)
    ax3.set_xlabel('Training Steps')
    ax3.set_ylabel('Average Steps to Impact')
    ax3.set_title('Defensive Effectiveness: Time to Impact')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Deception Effectiveness - Steps Delayed
    ax4 = axes[1,1]
    for exp_name, exp_data in experiments.items():
        if 'evaluation/steps_delayed_avg' in exp_data:
            data = exp_data['evaluation/steps_delayed_avg']
            ax4.plot(data['step'], data['value'], label=exp_name, alpha=0.8, marker='s', markersize=4)
    ax4.set_xlabel('Training Steps')
    ax4.set_ylabel('Average Steps Delayed')
    ax4.set_title('Deception Effectiveness: Attack Delay')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('cyberwheel_training_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig

def generate_summary_statistics(experiments):
    """Generate summary statistics for the experiments"""
    summary_data = []
    
    for exp_name, exp_data in experiments.items():
        stats = {'experiment': exp_name}
        
        # Final episodic return
        if 'charts/episodic_return' in exp_data:
            returns = exp_data['charts/episodic_return']['value']
            stats['final_return'] = returns.iloc[-1] if len(returns) > 0 else None
            stats['max_return'] = returns.max() if len(returns) > 0 else None
            stats['training_steps'] = len(returns)
        
        # SULI metrics
        if 'evaluation/time_step_till_impact_avg' in exp_data:
            impact_times = exp_data['evaluation/time_step_till_impact_avg']['value']
            stats['avg_time_to_impact'] = impact_times.mean() if len(impact_times) > 0 else None
            
        if 'evaluation/steps_delayed_avg' in exp_data:
            delays = exp_data['evaluation/steps_delayed_avg']['value']
            stats['avg_steps_delayed'] = delays.mean() if len(delays) > 0 else None
        
        summary_data.append(stats)
    
    summary_df = pd.DataFrame(summary_data)
    print("\nExperiment Summary Statistics:")
    print("=" * 80)
    print(summary_df.to_string(index=False))
    
    return summary_df

if __name__ == "__main__":
    print("Extracting Cyberwheel training data...")
    experiments = analyze_all_experiments()
    
    if experiments:
        print(f"\nFound {len(experiments)} experiments with data")
        
        # Create visualizations
        create_training_curves(experiments)
        
        # Generate summary statistics
        summary_df = generate_summary_statistics(experiments)
        
        # Save summary to CSV
        summary_df.to_csv('cyberwheel_experiment_summary.csv', index=False)
        print(f"\nResults saved to 'cyberwheel_training_analysis.png' and 'cyberwheel_experiment_summary.csv'")
        
    else:
        print("No valid experiment data found")