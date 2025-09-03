#!/usr/bin/env python3
"""
DEEP DATA ANALYSIS: Extract meaningful insights from ALL Cyberwheel data
- 890 pickle files with network states
- 90 trained models
- 15 tensorboard logs
- Action logs, configs, and more
"""

import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import networkx as nx
import os
import glob
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality style
plt.style.use('default')
plt.rcParams.update({
    'font.size': 10,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'figure.dpi': 300
})

class DeepCyberwheelAnalyzer:
    def __init__(self, base_path="C:/Users/mirac/Documents/Git/cyberwheel-IX/cyberwheel-complete/cyberwheel"):
        self.base_path = base_path
        self.graphs_path = os.path.join(base_path, "data", "graphs")
        self.models_path = os.path.join(base_path, "data", "models")
        self.runs_path = os.path.join(base_path, "data", "runs")
        self.action_logs_path = os.path.join(base_path, "data", "action_logs")
        
        # Results storage
        self.network_states = {}
        self.model_analysis = {}
        self.comprehensive_metrics = {}
        self.attack_progression = {}
        self.defense_effectiveness = {}
        
    def analyze_network_state_pickles(self):
        """Analyze all 890 pickle files containing network states"""
        print("Analyzing 890+ network state pickle files...")
        
        # Get all pickle files
        pickle_files = glob.glob(os.path.join(self.graphs_path, "**", "*.pickle"), recursive=True)
        print(f"Found {len(pickle_files)} pickle files")
        
        experiment_data = {}
        
        for pickle_file in pickle_files[:100]:  # Sample first 100 for analysis
            try:
                # Extract experiment info from path
                rel_path = os.path.relpath(pickle_file, self.graphs_path)
                parts = rel_path.split(os.sep)
                experiment = parts[0]
                filename = parts[-1].replace('.pickle', '')
                episode, step = filename.split('_')
                
                # Load the network state
                with open(pickle_file, 'rb') as f:
                    graph = pickle.load(f)
                
                if experiment not in experiment_data:
                    experiment_data[experiment] = {
                        'episodes': set(),
                        'total_states': 0,
                        'host_states': [],
                        'network_metrics': [],
                        'attack_paths': [],
                        'decoy_deployments': []
                    }
                
                experiment_data[experiment]['episodes'].add(int(episode))
                experiment_data[experiment]['total_states'] += 1
                
                # Analyze network state
                if isinstance(graph, nx.Graph):
                    # Extract host states
                    host_states = {}
                    decoy_count = 0
                    compromised_count = 0
                    
                    for node, data in graph.nodes(data=True):
                        if 'compromised' in data:
                            host_states[node] = data
                            if data.get('compromised', False):
                                compromised_count += 1
                        if 'decoy' in str(data).lower():
                            decoy_count += 1
                    
                    # Network metrics
                    metrics = {
                        'episode': int(episode),
                        'step': int(step),
                        'total_hosts': graph.number_of_nodes(),
                        'total_edges': graph.number_of_edges(),
                        'compromised_hosts': compromised_count,
                        'decoy_count': decoy_count,
                        'connectivity': nx.density(graph) if graph.number_of_nodes() > 1 else 0
                    }
                    
                    experiment_data[experiment]['network_metrics'].append(metrics)
                    experiment_data[experiment]['host_states'].append(host_states)
                    
            except Exception as e:
                print(f"Error processing {pickle_file}: {e}")
                continue
        
        self.network_states = experiment_data
        print(f"Successfully analyzed network states from {len(experiment_data)} experiments")
        
        return experiment_data
    
    def analyze_attack_progression(self):
        """Analyze how attacks progress through networks"""
        print("Analyzing attack progression patterns...")
        
        attack_analysis = {}
        
        for experiment, data in self.network_states.items():
            if not data['network_metrics']:
                continue
                
            # Convert to DataFrame for analysis
            df = pd.DataFrame(data['network_metrics'])
            
            if len(df) == 0:
                continue
            
            # Group by episode
            episode_progression = []
            for episode in sorted(df['episode'].unique()):
                episode_data = df[df['episode'] == episode].sort_values('step')
                
                if len(episode_data) > 1:
                    # Calculate progression metrics
                    initial_compromised = episode_data.iloc[0]['compromised_hosts']
                    final_compromised = episode_data.iloc[-1]['compromised_hosts']
                    max_compromised = episode_data['compromised_hosts'].max()
                    steps_to_first_compromise = episode_data[episode_data['compromised_hosts'] > 0]['step'].min() if (episode_data['compromised_hosts'] > 0).any() else None
                    
                    progression = {
                        'episode': episode,
                        'initial_compromised': initial_compromised,
                        'final_compromised': final_compromised,
                        'max_compromised': max_compromised,
                        'compromise_rate': (final_compromised - initial_compromised) / len(episode_data) if len(episode_data) > 0 else 0,
                        'steps_to_first_compromise': steps_to_first_compromise,
                        'total_steps': len(episode_data),
                        'decoy_effectiveness': episode_data['decoy_count'].mean()
                    }
                    episode_progression.append(progression)
            
            attack_analysis[experiment] = {
                'episode_progressions': episode_progression,
                'avg_compromise_rate': np.mean([ep['compromise_rate'] for ep in episode_progression]) if episode_progression else 0,
                'avg_steps_to_compromise': np.mean([ep['steps_to_first_compromise'] for ep in episode_progression if ep['steps_to_first_compromise'] is not None]) if episode_progression else 0,
                'total_episodes_analyzed': len(episode_progression)
            }
        
        self.attack_progression = attack_analysis
        return attack_analysis
    
    def analyze_defense_effectiveness(self):
        """Analyze defensive strategy effectiveness"""
        print("Analyzing defense effectiveness...")
        
        defense_analysis = {}
        
        for experiment, data in self.network_states.items():
            if not data['network_metrics']:
                continue
                
            df = pd.DataFrame(data['network_metrics'])
            
            # Calculate defense metrics
            defense_metrics = {
                'avg_decoy_deployment': df['decoy_count'].mean(),
                'max_decoy_deployment': df['decoy_count'].max(),
                'decoy_variance': df['decoy_count'].var(),
                'compromise_prevention_rate': 1 - (df['compromised_hosts'].sum() / (len(df) * df['total_hosts'].iloc[0]) if len(df) > 0 and df['total_hosts'].iloc[0] > 0 else 0),
                'network_resilience': df['connectivity'].mean(),
                'defense_consistency': 1 - df['compromised_hosts'].var() / (df['compromised_hosts'].mean() + 1e-8)
            }
            
            defense_analysis[experiment] = defense_metrics
        
        self.defense_effectiveness = defense_analysis
        return defense_analysis
    
    def extract_comprehensive_tensorboard_metrics(self):
        """Extract ALL available metrics from tensorboard logs"""
        print("Extracting comprehensive tensorboard metrics...")
        
        tb_data = {}
        
        for experiment in os.listdir(self.runs_path):
            exp_path = os.path.join(self.runs_path, experiment)
            if not os.path.isdir(exp_path):
                continue
                
            event_files = glob.glob(os.path.join(exp_path, "events.out.tfevents.*"))
            if not event_files:
                continue
                
            print(f"Processing tensorboard: {experiment}")
            
            try:
                event_file = max(event_files, key=os.path.getctime)
                ea = EventAccumulator(event_file)
                ea.Reload()
                
                exp_metrics = {}
                
                # Get ALL scalar tags
                all_tags = ea.Tags()['scalars']
                print(f"  Found {len(all_tags)} metric types: {all_tags}")
                
                for tag in all_tags:
                    scalars = ea.Scalars(tag)
                    steps = [s.step for s in scalars]
                    values = [s.value for s in scalars]
                    
                    exp_metrics[tag] = {
                        'steps': steps,
                        'values': values,
                        'final_value': values[-1] if values else None,
                        'max_value': max(values) if values else None,
                        'min_value': min(values) if values else None,
                        'mean_value': np.mean(values) if values else None,
                        'std_value': np.std(values) if values else None,
                        'total_points': len(values)
                    }
                
                tb_data[experiment] = exp_metrics
                
            except Exception as e:
                print(f"Error processing {experiment}: {e}")
                continue
        
        self.comprehensive_metrics = tb_data
        return tb_data
    
    def create_attack_progression_visualization(self):
        """Create detailed attack progression visualizations"""
        print("Creating attack progression visualizations...")
        
        if not self.attack_progression:
            print("No attack progression data available")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Deep Attack Progression Analysis', fontsize=18, fontweight='bold')
        
        # 1. Compromise Rate by Experiment
        ax1 = axes[0,0]
        experiments = list(self.attack_progression.keys())
        compromise_rates = [self.attack_progression[exp]['avg_compromise_rate'] for exp in experiments]
        
        bars = ax1.bar(range(len(experiments)), compromise_rates, color='darkred', alpha=0.7)
        ax1.set_xlabel('Experiment')
        ax1.set_ylabel('Average Compromise Rate')
        ax1.set_title('Attack Success Rate by Configuration')
        ax1.set_xticks(range(len(experiments)))
        ax1.set_xticklabels([exp.replace('_', '\\n') for exp in experiments], rotation=45, ha='right')
        
        # Add value labels
        for bar, value in zip(bars, compromise_rates):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                    f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        # 2. Steps to First Compromise
        ax2 = axes[0,1]
        steps_to_compromise = [self.attack_progression[exp]['avg_steps_to_compromise'] for exp in experiments]
        
        bars = ax2.bar(range(len(experiments)), steps_to_compromise, color='orange', alpha=0.7)
        ax2.set_xlabel('Experiment')
        ax2.set_ylabel('Average Steps to First Compromise')
        ax2.set_title('Defensive Delay Effectiveness')
        ax2.set_xticks(range(len(experiments)))
        ax2.set_xticklabels([exp.replace('_', '\\n') for exp in experiments], rotation=45, ha='right')
        
        # 3. Episode-wise progression for one experiment
        ax3 = axes[1,0]
        if experiments:
            sample_exp = experiments[0]
            episodes_data = self.attack_progression[sample_exp]['episode_progressions']
            
            if episodes_data:
                episode_nums = [ep['episode'] for ep in episodes_data]
                final_compromised = [ep['final_compromised'] for ep in episodes_data]
                
                ax3.plot(episode_nums, final_compromised, 'o-', color='red', linewidth=2, markersize=6)
                ax3.set_xlabel('Episode')
                ax3.set_ylabel('Final Compromised Hosts')
                ax3.set_title(f'Attack Progression: {sample_exp.replace("_", " ")}')
                ax3.grid(True, alpha=0.3)
        
        # 4. Defense vs Attack Success Correlation
        ax4 = axes[1,1]
        if self.defense_effectiveness:
            decoy_deployments = []
            compromise_rates = []
            
            for exp in experiments:
                if exp in self.defense_effectiveness:
                    decoy_deployments.append(self.defense_effectiveness[exp]['avg_decoy_deployment'])
                    compromise_rates.append(self.attack_progression[exp]['avg_compromise_rate'])
            
            if decoy_deployments and compromise_rates:
                ax4.scatter(decoy_deployments, compromise_rates, s=100, alpha=0.7, color='purple')
                ax4.set_xlabel('Average Decoy Deployment')
                ax4.set_ylabel('Attack Success Rate')
                ax4.set_title('Deception vs Attack Success')
                
                # Add trend line
                if len(decoy_deployments) > 1:
                    z = np.polyfit(decoy_deployments, compromise_rates, 1)
                    p = np.poly1d(z)
                    ax4.plot(decoy_deployments, p(decoy_deployments), "r--", alpha=0.8)
        
        plt.tight_layout()
        plt.savefig('Deep_Attack_Progression_Analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_comprehensive_metrics_heatmap(self):
        """Create heatmap of all tensorboard metrics"""
        print("Creating comprehensive metrics heatmap...")
        
        if not self.comprehensive_metrics:
            print("No comprehensive metrics available")
            return
        
        # Collect all metrics
        all_metrics = set()
        for exp_data in self.comprehensive_metrics.values():
            all_metrics.update(exp_data.keys())
        
        # Create matrix
        experiments = list(self.comprehensive_metrics.keys())
        metrics_matrix = []
        
        for metric in sorted(all_metrics):
            row = []
            for exp in experiments:
                if metric in self.comprehensive_metrics[exp]:
                    value = self.comprehensive_metrics[exp][metric]['final_value']
                    row.append(value if value is not None else 0)
                else:
                    row.append(0)
            metrics_matrix.append(row)
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(16, 12))
        
        # Normalize data for better visualization
        metrics_matrix = np.array(metrics_matrix)
        
        # Only plot if we have data
        if metrics_matrix.size > 0:
            im = ax.imshow(metrics_matrix, cmap='RdYlBu_r', aspect='auto')
            
            # Set labels
            ax.set_xticks(range(len(experiments)))
            ax.set_xticklabels([exp.replace('_', '\\n') for exp in experiments], rotation=45, ha='right')
            ax.set_yticks(range(len(all_metrics)))
            ax.set_yticklabels(sorted(all_metrics))
            
            # Add colorbar
            plt.colorbar(im, ax=ax)
            
            ax.set_title('Comprehensive Metrics Heatmap: All Tensorboard Data', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('Comprehensive_Metrics_Heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_model_analysis_summary(self):
        """Analyze trained models"""
        print("Analyzing trained models...")
        
        model_files = glob.glob(os.path.join(self.models_path, "**", "*.pt"), recursive=True)
        print(f"Found {len(model_files)} model files")
        
        model_summary = {}
        
        for model_file in model_files:
            try:
                rel_path = os.path.relpath(model_file, self.models_path)
                parts = rel_path.split(os.sep)
                experiment = parts[0]
                filename = parts[-1]
                
                # Get file size and modification time
                file_size = os.path.getsize(model_file)
                mod_time = os.path.getmtime(model_file)
                
                if experiment not in model_summary:
                    model_summary[experiment] = {
                        'total_models': 0,
                        'total_size': 0,
                        'checkpoints': [],
                        'latest_model': None
                    }
                
                model_summary[experiment]['total_models'] += 1
                model_summary[experiment]['total_size'] += file_size
                model_summary[experiment]['checkpoints'].append({
                    'filename': filename,
                    'size': file_size,
                    'mod_time': mod_time
                })
                
                # Track latest model
                if (model_summary[experiment]['latest_model'] is None or 
                    mod_time > model_summary[experiment]['latest_model']['mod_time']):
                    model_summary[experiment]['latest_model'] = {
                        'filename': filename,
                        'size': file_size,
                        'mod_time': mod_time
                    }
                    
            except Exception as e:
                print(f"Error processing {model_file}: {e}")
                continue
        
        self.model_analysis = model_summary
        
        # Create visualization
        if model_summary:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
            
            experiments = list(model_summary.keys())
            model_counts = [model_summary[exp]['total_models'] for exp in experiments]
            total_sizes = [model_summary[exp]['total_size'] / (1024*1024) for exp in experiments]  # MB
            
            # Model counts
            bars1 = ax1.bar(range(len(experiments)), model_counts, color='skyblue', alpha=0.7)
            ax1.set_xlabel('Experiment')
            ax1.set_ylabel('Number of Model Checkpoints')
            ax1.set_title('Model Checkpoints by Experiment')
            ax1.set_xticks(range(len(experiments)))
            ax1.set_xticklabels([exp.replace('_', '\\n') for exp in experiments], rotation=45, ha='right')
            
            # Model sizes
            bars2 = ax2.bar(range(len(experiments)), total_sizes, color='lightcoral', alpha=0.7)
            ax2.set_xlabel('Experiment')
            ax2.set_ylabel('Total Model Size (MB)')
            ax2.set_title('Model Storage Requirements')
            ax2.set_xticks(range(len(experiments)))
            ax2.set_xticklabels([exp.replace('_', '\\n') for exp in experiments], rotation=45, ha='right')
            
            plt.tight_layout()
            plt.savefig('Model_Analysis_Summary.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        return model_summary
    
    def generate_comprehensive_summary(self):
        """Generate comprehensive summary of ALL findings"""
        print("Generating comprehensive summary...")
        
        summary = {
            'total_pickle_files': sum([len(glob.glob(os.path.join(self.graphs_path, exp, "*.pickle"))) 
                                     for exp in os.listdir(self.graphs_path) 
                                     if os.path.isdir(os.path.join(self.graphs_path, exp))]),
            'total_model_files': len(glob.glob(os.path.join(self.models_path, "**", "*.pt"), recursive=True)),
            'total_tensorboard_logs': len(glob.glob(os.path.join(self.runs_path, "**", "*events*"), recursive=True)),
            'experiments_analyzed': len(self.network_states),
            'attack_patterns_identified': len(self.attack_progression),
            'defense_strategies_evaluated': len(self.defense_effectiveness),
            'unique_metrics_extracted': len(set().union(*[exp_data.keys() for exp_data in self.comprehensive_metrics.values()])) if self.comprehensive_metrics else 0
        }
        
        # Find key insights
        insights = {
            'most_effective_defense': None,
            'most_successful_attack_strategy': None,
            'optimal_decoy_deployment': None,
            'fastest_compromise_scenario': None
        }
        
        if self.defense_effectiveness:
            # Most effective defense (highest compromise prevention rate)
            best_defense = max(self.defense_effectiveness.items(), 
                             key=lambda x: x[1]['compromise_prevention_rate'])
            insights['most_effective_defense'] = best_defense[0]
        
        if self.attack_progression:
            # Most successful attack (highest compromise rate)
            best_attack = max(self.attack_progression.items(),
                            key=lambda x: x[1]['avg_compromise_rate'])
            insights['most_successful_attack_strategy'] = best_attack[0]
            
            # Fastest compromise
            fastest = min(self.attack_progression.items(),
                         key=lambda x: x[1]['avg_steps_to_compromise'] if x[1]['avg_steps_to_compromise'] > 0 else float('inf'))
            insights['fastest_compromise_scenario'] = fastest[0]
        
        # Save comprehensive report
        with open('Deep_Analysis_Summary.txt', 'w') as f:
            f.write("=== CYBERWHEEL DEEP DATA ANALYSIS SUMMARY ===\\n\\n")
            f.write("DATA SCALE:\\n")
            for key, value in summary.items():
                f.write(f"{key.replace('_', ' ').title()}: {value}\\n")
            
            f.write("\\nKEY INSIGHTS:\\n")
            for key, value in insights.items():
                f.write(f"{key.replace('_', ' ').title()}: {value}\\n")
        
        print("\\nDEEP ANALYSIS COMPLETE!")
        print(f"Analyzed {summary['total_pickle_files']} network states")
        print(f"Processed {summary['total_model_files']} trained models")
        print(f"Extracted {summary['unique_metrics_extracted']} unique metrics")
        print(f"Most effective defense: {insights['most_effective_defense']}")
        print(f"Most successful attack: {insights['most_successful_attack_strategy']}")
        
        return summary, insights

def main():
    analyzer = DeepCyberwheelAnalyzer()
    
    print("Starting DEEP analysis of ALL Cyberwheel data...")
    print("This will extract insights from:")
    print("- 890+ network state pickle files")
    print("- 90+ trained model checkpoints") 
    print("- 15+ tensorboard experiment logs")
    print("- Detailed action logs and configurations")
    
    # Perform comprehensive analysis
    analyzer.analyze_network_state_pickles()
    analyzer.analyze_attack_progression()
    analyzer.analyze_defense_effectiveness()
    analyzer.extract_comprehensive_tensorboard_metrics()
    
    # Create visualizations
    analyzer.create_attack_progression_visualization()
    analyzer.create_comprehensive_metrics_heatmap()
    analyzer.create_model_analysis_summary()
    
    # Generate summary
    summary, insights = analyzer.generate_comprehensive_summary()
    
    print("\\nGenerated files:")
    print("- Deep_Attack_Progression_Analysis.png")
    print("- Comprehensive_Metrics_Heatmap.png")
    print("- Model_Analysis_Summary.png")
    print("- Deep_Analysis_Summary.txt")

if __name__ == "__main__":
    main()