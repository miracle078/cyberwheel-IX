#!/usr/bin/env python3
"""
Comprehensive Training Data Analysis for Cyberwheel Research
Focus on cumulative returns, episodic performance, and SULI metrics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import os
import glob
import pickle
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality style
plt.style.use('default')
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 18,
    'figure.dpi': 300
})

class CyberwheelDataAnalyzer:
    def __init__(self, base_path="C:/Users/mirac/Documents/Git/cyberwheel-IX/cyberwheel-complete/cyberwheel"):
        self.base_path = base_path
        self.runs_path = os.path.join(base_path, "data", "runs")
        self.action_logs_path = os.path.join(base_path, "data", "action_logs")
        self.models_path = os.path.join(base_path, "data", "models")
        self.graphs_path = os.path.join(base_path, "data", "graphs")
        
        # Results storage
        self.tensorboard_data = {}
        self.action_data = {}
        self.cumulative_returns = {}
        self.suli_metrics = {}
        
    def extract_tensorboard_data(self):
        """Extract comprehensive data from all tensorboard logs"""
        print("Extracting TensorBoard data from all experiments...")
        
        for experiment in os.listdir(self.runs_path):
            exp_path = os.path.join(self.runs_path, experiment)
            if not os.path.isdir(exp_path):
                continue
                
            # Find tensorboard event files
            event_files = glob.glob(os.path.join(exp_path, "events.out.tfevents.*"))
            if not event_files:
                continue
                
            print(f"Processing experiment: {experiment}")
            
            # Use most recent event file
            event_file = max(event_files, key=os.path.getctime)
            
            try:
                ea = EventAccumulator(event_file)
                ea.Reload()
                
                exp_data = {}
                
                # Extract all scalar metrics
                for tag in ea.Tags()['scalars']:
                    scalars = ea.Scalars(tag)
                    steps = [s.step for s in scalars]
                    values = [s.value for s in scalars]
                    exp_data[tag] = {
                        'steps': steps,
                        'values': values,
                        'final_value': values[-1] if values else None,
                        'max_value': max(values) if values else None,
                        'min_value': min(values) if values else None,
                        'total_steps': len(values)
                    }
                
                self.tensorboard_data[experiment] = exp_data
                
                # Calculate cumulative returns if episodic return data exists
                if 'charts/episodic_return' in exp_data:
                    returns = exp_data['charts/episodic_return']['values']
                    self.cumulative_returns[experiment] = {
                        'episodic_returns': returns,
                        'cumulative_return': np.cumsum(returns),
                        'mean_return': np.mean(returns),
                        'std_return': np.std(returns),
                        'total_episodes': len(returns),
                        'final_cumulative': np.sum(returns)
                    }
                
                # Extract SULI-specific metrics
                suli_data = {}
                suli_metrics = [
                    'evaluation/impact_timestep_avg',
                    'evaluation/time_step_till_impact_avg', 
                    'evaluation/first_step_of_decoy_contact_avg',
                    'evaluation/impacted_decoys_avg',
                    'evaluation/delay_avg',
                    'evaluation/steps_delayed_avg'
                ]
                
                for metric in suli_metrics:
                    if metric in exp_data:
                        suli_data[metric.split('/')[-1]] = exp_data[metric]
                        
                if suli_data:
                    self.suli_metrics[experiment] = suli_data
                    
            except Exception as e:
                print(f"Error processing {experiment}: {e}")
                continue
        
        print(f"Successfully extracted data from {len(self.tensorboard_data)} experiments")
    
    def extract_action_log_data(self):
        """Extract detailed action and reward data from CSV logs"""
        print("Extracting action log data...")
        
        csv_files = glob.glob(os.path.join(self.action_logs_path, "*.csv"))
        
        for csv_file in csv_files:
            experiment_name = Path(csv_file).stem
            print(f"Processing action log: {experiment_name}")
            
            try:
                df = pd.read_csv(csv_file)
                
                # Calculate episode-wise statistics
                episode_stats = df.groupby('episode').agg({
                    'reward': ['sum', 'mean', 'count'],
                    'red_action_success': 'mean',
                    'step': 'max'
                }).round(3)
                
                # Flatten column names
                episode_stats.columns = ['_'.join(col).strip() for col in episode_stats.columns]
                
                # Calculate cumulative rewards
                episode_rewards = df.groupby('episode')['reward'].sum().values
                cumulative_rewards = np.cumsum(episode_rewards)
                
                self.action_data[experiment_name] = {
                    'raw_data': df,
                    'episode_stats': episode_stats,
                    'episode_rewards': episode_rewards,
                    'cumulative_rewards': cumulative_rewards,
                    'total_episodes': df['episode'].nunique(),
                    'total_steps': len(df),
                    'mean_episode_reward': np.mean(episode_rewards),
                    'final_cumulative_reward': cumulative_rewards[-1] if len(cumulative_rewards) > 0 else 0,
                    'red_success_rate': df['red_action_success'].mean()
                }
                
            except Exception as e:
                print(f"Error processing {csv_file}: {e}")
                continue
    
    def create_comprehensive_analysis(self):
        """Create comprehensive analysis of all data"""
        print("Creating comprehensive analysis...")
        
        # 1. Cumulative Returns Analysis
        self.create_cumulative_returns_analysis()
        
        # 2. SULI Metrics Analysis
        self.create_suli_analysis()
        
        # 3. Performance Comparison
        self.create_performance_comparison()
        
        # 4. Episode-wise Analysis
        self.create_episode_analysis()
        
        # 5. Comprehensive Summary
        self.create_comprehensive_summary()
    
    def create_cumulative_returns_analysis(self):
        """Focus on cumulative returns across all experiments"""
        print("Creating cumulative returns analysis...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Comprehensive Cumulative Returns Analysis', fontsize=20, fontweight='bold')
        
        # 1. Cumulative Returns Over Episodes
        ax1 = axes[0,0]
        for exp_name, data in self.cumulative_returns.items():
            if 'cumulative_return' in data:
                episodes = range(len(data['cumulative_return']))
                ax1.plot(episodes, data['cumulative_return'], label=exp_name.replace('_', ' '), linewidth=2)
        
        ax1.set_xlabel('Episode')
        ax1.set_ylabel('Cumulative Return')
        ax1.set_title('Cumulative Returns by Experiment')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # 2. Final Cumulative Returns Comparison
        ax2 = axes[0,1]
        exp_names = []
        final_returns = []
        
        for exp_name, data in self.cumulative_returns.items():
            if 'final_cumulative' in data:
                exp_names.append(exp_name.replace('_', ' '))
                final_returns.append(data['final_cumulative'])
        
        if exp_names:
            bars = ax2.bar(range(len(exp_names)), final_returns, alpha=0.7, color='skyblue')
            ax2.set_xlabel('Experiment')
            ax2.set_ylabel('Final Cumulative Return')
            ax2.set_title('Final Cumulative Returns Comparison')
            ax2.set_xticks(range(len(exp_names)))
            ax2.set_xticklabels(exp_names, rotation=45, ha='right')
            
            # Add value labels on bars
            for bar, value in zip(bars, final_returns):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{value:.0f}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Mean Episode Returns
        ax3 = axes[1,0]
        mean_returns = []
        std_returns = []
        
        for exp_name in exp_names:
            original_name = exp_name.replace(' ', '_')
            if original_name in self.cumulative_returns:
                data = self.cumulative_returns[original_name]
                mean_returns.append(data['mean_return'])
                std_returns.append(data['std_return'])
        
        if mean_returns:
            bars = ax3.bar(range(len(exp_names)), mean_returns, yerr=std_returns, 
                          alpha=0.7, color='lightcoral', capsize=5)
            ax3.set_xlabel('Experiment')
            ax3.set_ylabel('Mean Episode Return')
            ax3.set_title('Mean Episode Returns with Standard Deviation')
            ax3.set_xticks(range(len(exp_names)))
            ax3.set_xticklabels(exp_names, rotation=45, ha='right')
        
        # 4. Return Distribution Analysis
        ax4 = axes[1,1]
        return_data = []
        labels = []
        
        for exp_name, data in self.cumulative_returns.items():
            if 'episodic_returns' in data:
                return_data.extend(data['episodic_returns'])
                labels.extend([exp_name.replace('_', ' ')] * len(data['episodic_returns']))
        
        if return_data:
            df_returns = pd.DataFrame({'Returns': return_data, 'Experiment': labels})
            sns.boxplot(data=df_returns, x='Experiment', y='Returns', ax=ax4)
            ax4.set_title('Return Distribution by Experiment')
            ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig('Comprehensive_Cumulative_Returns_Analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_suli_analysis(self):
        """Analyze SULI methodology metrics"""
        print("Creating SULI analysis...")
        
        if not self.suli_metrics:
            print("No SULI metrics found")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('SULI Methodology Analysis', fontsize=20, fontweight='bold')
        
        # Extract metrics for analysis
        experiments = list(self.suli_metrics.keys())
        
        # 1. Impact Timestep Analysis
        ax1 = axes[0,0]
        impact_times = []
        exp_labels = []
        
        for exp in experiments:
            for metric_name, metric_data in self.suli_metrics[exp].items():
                if 'impact' in metric_name.lower() and 'timestep' in metric_name.lower():
                    if 'final_value' in metric_data:
                        impact_times.append(metric_data['final_value'])
                        exp_labels.append(exp.replace('_', ' '))
        
        if impact_times:
            bars = ax1.bar(range(len(exp_labels)), impact_times, alpha=0.7, color='gold')
            ax1.set_xlabel('Experiment')
            ax1.set_ylabel('Average Impact Timestep')
            ax1.set_title('SULI: Time to Impact Analysis')
            ax1.set_xticks(range(len(exp_labels)))
            ax1.set_xticklabels(exp_labels, rotation=45, ha='right')
        
        # 2. Steps Delayed Analysis
        ax2 = axes[0,1]
        delay_values = []
        delay_labels = []
        
        for exp in experiments:
            for metric_name, metric_data in self.suli_metrics[exp].items():
                if 'delay' in metric_name.lower():
                    if 'final_value' in metric_data:
                        delay_values.append(metric_data['final_value'])
                        delay_labels.append(exp.replace('_', ' '))
        
        if delay_values:
            bars = ax2.bar(range(len(delay_labels)), delay_values, alpha=0.7, color='lightgreen')
            ax2.set_xlabel('Experiment')
            ax2.set_ylabel('Average Steps Delayed')
            ax2.set_title('SULI: Attack Delay Effectiveness')
            ax2.set_xticks(range(len(delay_labels)))
            ax2.set_xticklabels(delay_labels, rotation=45, ha='right')
        
        # 3. Deception Effectiveness Over Time
        ax3 = axes[1,0]
        for exp in experiments:
            for metric_name, metric_data in self.suli_metrics[exp].items():
                if 'delay' in metric_name.lower() and 'values' in metric_data:
                    steps = metric_data['steps']
                    values = metric_data['values']
                    ax3.plot(steps, values, label=f"{exp.replace('_', ' ')} - {metric_name}", linewidth=2)
        
        ax3.set_xlabel('Training Steps')
        ax3.set_ylabel('Deception Effectiveness')
        ax3.set_title('SULI: Deception Effectiveness Over Training')
        ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax3.grid(True, alpha=0.3)
        
        # 4. SULI Metrics Summary Table (as text)
        ax4 = axes[1,1]
        ax4.axis('off')
        
        # Create summary table
        summary_data = []
        for exp in experiments:
            exp_summary = [exp.replace('_', ' ')]
            
            for metric_name, metric_data in self.suli_metrics[exp].items():
                if 'final_value' in metric_data:
                    exp_summary.append(f"{metric_data['final_value']:.2f}")
                else:
                    exp_summary.append("N/A")
            
            summary_data.append(exp_summary)
        
        if summary_data:
            headers = ['Experiment'] + [list(self.suli_metrics[experiments[0]].keys())[i].replace('_', ' ').title() 
                                       for i in range(len(self.suli_metrics[experiments[0]]))]
            
            table = ax4.table(cellText=summary_data, colLabels=headers, 
                             cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            table.scale(1.2, 1.5)
            ax4.set_title('SULI Metrics Summary', pad=20)
        
        plt.tight_layout()
        plt.savefig('SULI_Methodology_Analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_performance_comparison(self):
        """Create comprehensive performance comparison"""
        print("Creating performance comparison...")
        
        # Create comparison dataframe
        comparison_data = []
        
        for exp_name in self.tensorboard_data.keys():
            row = {'Experiment': exp_name.replace('_', ' ')}
            
            # Add tensorboard metrics
            tb_data = self.tensorboard_data[exp_name]
            if 'charts/episodic_return' in tb_data:
                ep_data = tb_data['charts/episodic_return']
                row['Final_Episodic_Return'] = ep_data['final_value']
                row['Best_Episodic_Return'] = ep_data['max_value']
                row['Worst_Episodic_Return'] = ep_data['min_value']
                row['Total_Episodes'] = ep_data['total_steps']
            
            # Add cumulative returns
            if exp_name in self.cumulative_returns:
                cum_data = self.cumulative_returns[exp_name]
                row['Mean_Episode_Return'] = cum_data['mean_return']
                row['Std_Episode_Return'] = cum_data['std_return']
                row['Final_Cumulative_Return'] = cum_data['final_cumulative']
            
            # Add action log data if available
            if exp_name in self.action_data:
                action_data = self.action_data[exp_name]
                row['Red_Success_Rate'] = action_data['red_success_rate']
                row['Total_Steps'] = action_data['total_steps']
            
            # Add SULI metrics
            if exp_name in self.suli_metrics:
                suli_data = self.suli_metrics[exp_name]
                for metric_name, metric_info in suli_data.items():
                    if 'final_value' in metric_info:
                        row[f'SULI_{metric_name}'] = metric_info['final_value']
            
            comparison_data.append(row)
        
        # Save comprehensive comparison
        if comparison_data:
            df = pd.DataFrame(comparison_data)
            df.to_csv('Comprehensive_Performance_Comparison.csv', index=False)
            
            # Create visualization
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_columns) > 1:
                fig, ax = plt.subplots(figsize=(14, 8))
                
                # Create correlation heatmap of performance metrics
                corr_matrix = df[numeric_columns].corr()
                sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
                ax.set_title('Performance Metrics Correlation Matrix')
                
                plt.tight_layout()
                plt.savefig('Performance_Metrics_Correlation.png', dpi=300, bbox_inches='tight')
                plt.close()
    
    def create_episode_analysis(self):
        """Analyze episode-wise performance"""
        print("Creating episode analysis...")
        
        if not self.action_data:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Episode-wise Performance Analysis', fontsize=20, fontweight='bold')
        
        # 1. Episode Rewards Progression
        ax1 = axes[0,0]
        for exp_name, data in self.action_data.items():
            episode_rewards = data['episode_rewards']
            episodes = range(len(episode_rewards))
            ax1.plot(episodes, episode_rewards, label=exp_name.replace('_', ' '), linewidth=2)
        
        ax1.set_xlabel('Episode')
        ax1.set_ylabel('Episode Reward')
        ax1.set_title('Episode Rewards Progression')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Cumulative Rewards from Action Logs
        ax2 = axes[0,1]
        for exp_name, data in self.action_data.items():
            cumulative_rewards = data['cumulative_rewards']
            episodes = range(len(cumulative_rewards))
            ax2.plot(episodes, cumulative_rewards, label=exp_name.replace('_', ' '), linewidth=2)
        
        ax2.set_xlabel('Episode')
        ax2.set_ylabel('Cumulative Reward')
        ax2.set_title('Cumulative Rewards (Action Logs)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Red Agent Success Rate
        ax3 = axes[1,0]
        exp_names = []
        success_rates = []
        
        for exp_name, data in self.action_data.items():
            exp_names.append(exp_name.replace('_', ' '))
            success_rates.append(data['red_success_rate'] * 100)
        
        if exp_names:
            bars = ax3.bar(range(len(exp_names)), success_rates, alpha=0.7, color='salmon')
            ax3.set_xlabel('Experiment')
            ax3.set_ylabel('Red Agent Success Rate (%)')
            ax3.set_title('Attack Success Rates by Configuration')
            ax3.set_xticks(range(len(exp_names)))
            ax3.set_xticklabels(exp_names, rotation=45, ha='right')
        
        # 4. Episode Length Distribution
        ax4 = axes[1,1]
        episode_lengths = []
        experiment_labels = []
        
        for exp_name, data in self.action_data.items():
            episode_stats = data['episode_stats']
            if 'step_max' in episode_stats.columns:
                lengths = episode_stats['step_max'].values
                episode_lengths.extend(lengths)
                experiment_labels.extend([exp_name.replace('_', ' ')] * len(lengths))
        
        if episode_lengths:
            df_lengths = pd.DataFrame({'Episode_Length': episode_lengths, 'Experiment': experiment_labels})
            sns.boxplot(data=df_lengths, x='Experiment', y='Episode_Length', ax=ax4)
            ax4.set_title('Episode Length Distribution')
            ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig('Episode_Performance_Analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_comprehensive_summary(self):
        """Create comprehensive summary report"""
        print("Creating comprehensive summary...")
        
        summary = {
            'total_experiments': len(self.tensorboard_data),
            'experiments_with_cumulative_data': len(self.cumulative_returns),
            'experiments_with_suli_data': len(self.suli_metrics),
            'experiments_with_action_data': len(self.action_data),
            'total_training_episodes': sum([data.get('total_episodes', 0) for data in self.cumulative_returns.values()]),
            'best_performing_experiment': None,
            'highest_cumulative_return': float('-inf'),
            'most_effective_deception': None,
            'lowest_attack_success': float('inf')
        }
        
        # Find best performing experiment
        for exp_name, data in self.cumulative_returns.items():
            if data['final_cumulative'] > summary['highest_cumulative_return']:
                summary['highest_cumulative_return'] = data['final_cumulative']
                summary['best_performing_experiment'] = exp_name
        
        # Find most effective deception
        for exp_name, data in self.action_data.items():
            if data['red_success_rate'] < summary['lowest_attack_success']:
                summary['lowest_attack_success'] = data['red_success_rate']
                summary['most_effective_deception'] = exp_name
        
        # Save summary
        with open('Comprehensive_Analysis_Summary.txt', 'w') as f:
            f.write("=== CYBERWHEEL COMPREHENSIVE DATA ANALYSIS SUMMARY ===\\n\\n")
            for key, value in summary.items():
                f.write(f"{key.replace('_', ' ').title()}: {value}\\n")
        
        print("Analysis complete!")
        print(f"Processed {summary['total_experiments']} experiments")
        print(f"Best performing: {summary['best_performing_experiment']}")
        print(f"Most effective deception: {summary['most_effective_deception']}")

def main():
    analyzer = CyberwheelDataAnalyzer()
    
    print("Starting comprehensive Cyberwheel data analysis...")
    
    # Extract all data
    analyzer.extract_tensorboard_data()
    analyzer.extract_action_log_data()
    
    # Create comprehensive analysis
    analyzer.create_comprehensive_analysis()
    
    print("\\nAnalysis complete! Generated files:")
    print("- Comprehensive_Cumulative_Returns_Analysis.png")
    print("- SULI_Methodology_Analysis.png") 
    print("- Performance_Metrics_Correlation.png")
    print("- Episode_Performance_Analysis.png")
    print("- Comprehensive_Performance_Comparison.csv")
    print("- Comprehensive_Analysis_Summary.txt")

if __name__ == "__main__":
    main()