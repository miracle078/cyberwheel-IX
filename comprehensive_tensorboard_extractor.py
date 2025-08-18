#!/usr/bin/env python3
"""
Comprehensive TensorBoard Data Extractor for Cyberwheel Training Analysis
Extracts ALL metrics from verified experiments with detailed progress tracking
"""

from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import glob
import json
import warnings
from datetime import datetime
from pathlib import Path

warnings.filterwarnings('ignore')

class CyberwheelTensorBoardExtractor:
    def __init__(self, runs_dir=None):
        self.runs_dir = runs_dir or "C:/Users/mirac/Documents/Git/cyberwheel-IX/cyberwheel-complete/cyberwheel/data/runs"
        self.verified_experiments = [
            'Phase1_Validation_HPC',
            'Phase2_Blue_HighDecoy_HPC', 
            'Phase2_Blue_Medium_HPC',
            'Phase2_Blue_Small_HPC',
            'Phase2_Blue_PerfectDetection_HPC'
        ]
        self.all_metrics = {}
        self.summary_stats = {}
        
    def extract_metrics_from_event_file(self, event_file, experiment_name):
        """Extract all scalar metrics from a single event file"""
        print(f"  Processing: {os.path.basename(event_file)}")
        
        try:
            ea = EventAccumulator(event_file)
            ea.Reload()
            
            metrics = {}
            scalar_tags = ea.Tags()['scalars']
            print(f"    Found {len(scalar_tags)} scalar metrics")
            
            for tag in scalar_tags:
                try:
                    scalars = ea.Scalars(tag)
                    steps = [s.step for s in scalars]
                    values = [s.value for s in scalars]
                    wall_times = [s.wall_time for s in scalars]
                    
                    metrics[tag] = {
                        'steps': steps,
                        'values': values,
                        'wall_times': wall_times,
                        'count': len(steps)
                    }
                    print(f"      {tag}: {len(steps)} data points")
                except Exception as e:
                    print(f"      Error extracting {tag}: {e}")
                    continue
            
            return metrics
            
        except Exception as e:
            print(f"  ERROR processing {event_file}: {e}")
            return {}
    
    def process_experiment_directory(self, exp_dir, exp_name):
        """Process all event files in an experiment directory"""
        print(f"\nProcessing experiment: {exp_name}")
        exp_path = os.path.join(self.runs_dir, exp_dir)
        
        if not os.path.exists(exp_path):
            print(f"  Directory not found: {exp_path}")
            return {}
        
        # Find all tensorboard event files
        event_files = glob.glob(os.path.join(exp_path, "events.out.tfevents.*"))
        
        if not event_files:
            print(f"  No event files found in {exp_path}")
            return {}
        
        print(f"  Found {len(event_files)} event files")
        
        # Process each event file
        experiment_metrics = {}
        for i, event_file in enumerate(event_files):
            file_key = f"run_{i}" if len(event_files) > 1 else "main"
            metrics = self.extract_metrics_from_event_file(event_file, f"{exp_name}_{file_key}")
            if metrics:
                experiment_metrics[file_key] = {
                    'metrics': metrics,
                    'file_path': event_file,
                    'file_size': os.path.getsize(event_file),
                    'modification_time': datetime.fromtimestamp(os.path.getmtime(event_file))
                }
        
        return experiment_metrics
    
    def extract_all_metrics(self):
        """Extract metrics from all experiments"""
        print("="*80)
        print("COMPREHENSIVE TENSORBOARD METRICS EXTRACTION")
        print("="*80)
        
        # Process verified experiments first
        for exp_name in self.verified_experiments:
            if exp_name in os.listdir(self.runs_dir):
                self.all_metrics[exp_name] = self.process_experiment_directory(exp_name, exp_name)
        
        # Process any additional experiments
        for exp_dir in os.listdir(self.runs_dir):
            exp_path = os.path.join(self.runs_dir, exp_dir)
            if os.path.isdir(exp_path) and exp_dir not in self.verified_experiments and exp_dir != 'README.md':
                self.all_metrics[exp_dir] = self.process_experiment_directory(exp_dir, exp_dir)
        
        print(f"\nCompleted processing {len(self.all_metrics)} experiments")
        return self.all_metrics
    
    def generate_metrics_summary(self):
        """Generate comprehensive summary of all extracted metrics"""
        print("\n" + "="*80)
        print("GENERATING COMPREHENSIVE METRICS SUMMARY")
        print("="*80)
        
        summary = {}
        
        for exp_name, exp_data in self.all_metrics.items():
            if not exp_data:
                continue
                
            exp_summary = {
                'experiment': exp_name,
                'total_runs': len(exp_data),
                'metrics_per_run': {},
                'key_metrics': {}
            }
            
            # Process each run within the experiment
            for run_key, run_data in exp_data.items():
                metrics = run_data['metrics']
                run_summary = {
                    'total_metrics': len(metrics),
                    'file_size_mb': run_data['file_size'] / (1024*1024),
                    'last_modified': run_data['modification_time'].isoformat(),
                    'metrics_list': list(metrics.keys())
                }
                
                # Extract key training metrics
                key_metrics = {}
                
                # Common RL training metrics
                for metric_key in ['charts/episodic_return', 'charts/episodic_length', 
                                 'losses/value_loss', 'losses/policy_loss', 'losses/entropy_loss']:
                    if metric_key in metrics:
                        data = metrics[metric_key]
                        key_metrics[metric_key] = {
                            'final_value': data['values'][-1] if data['values'] else None,
                            'max_value': max(data['values']) if data['values'] else None,
                            'min_value': min(data['values']) if data['values'] else None,
                            'mean_value': np.mean(data['values']) if data['values'] else None,
                            'total_steps': max(data['steps']) if data['steps'] else None,
                            'data_points': len(data['values'])
                        }
                
                # SULI-specific metrics (defensive effectiveness)
                for metric_key in ['evaluation/time_step_till_impact_avg', 'evaluation/steps_delayed_avg',
                                 'evaluation/decoy_effectiveness', 'evaluation/detection_rate']:
                    if metric_key in metrics:
                        data = metrics[metric_key]
                        key_metrics[metric_key] = {
                            'final_value': data['values'][-1] if data['values'] else None,
                            'mean_value': np.mean(data['values']) if data['values'] else None,
                            'std_value': np.std(data['values']) if data['values'] else None,
                            'data_points': len(data['values'])
                        }
                
                run_summary['key_metrics'] = key_metrics
                exp_summary['metrics_per_run'][run_key] = run_summary
            
            summary[exp_name] = exp_summary
        
        self.summary_stats = summary
        return summary
    
    def create_comprehensive_visualizations(self):
        """Create comprehensive visualizations of training metrics"""
        print("\n" + "="*60)
        print("CREATING COMPREHENSIVE VISUALIZATIONS")
        print("="*60)
        
        # Set up the plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Episodic Returns Comparison
        ax1 = plt.subplot(3, 3, 1)
        self._plot_metric_comparison('charts/episodic_return', ax1, 'Episodic Returns', 'Training Steps', 'Return')
        
        # 2. Episode Length Trends  
        ax2 = plt.subplot(3, 3, 2)
        self._plot_metric_comparison('charts/episodic_length', ax2, 'Episode Length', 'Training Steps', 'Length')
        
        # 3. Value Loss
        ax3 = plt.subplot(3, 3, 3)
        self._plot_metric_comparison('losses/value_loss', ax3, 'Value Loss', 'Training Steps', 'Loss')
        
        # 4. Policy Loss
        ax4 = plt.subplot(3, 3, 4)
        self._plot_metric_comparison('losses/policy_loss', ax4, 'Policy Loss', 'Training Steps', 'Loss')
        
        # 5. Time to Impact (SULI metric)
        ax5 = plt.subplot(3, 3, 5)
        self._plot_metric_comparison('evaluation/time_step_till_impact_avg', ax5, 'Time to Impact', 'Evaluation Steps', 'Steps')
        
        # 6. Steps Delayed (Deception effectiveness)
        ax6 = plt.subplot(3, 3, 6)
        self._plot_metric_comparison('evaluation/steps_delayed_avg', ax6, 'Attack Delay', 'Evaluation Steps', 'Steps Delayed')
        
        # 7. Learning Rate
        ax7 = plt.subplot(3, 3, 7)
        self._plot_metric_comparison('charts/learning_rate', ax7, 'Learning Rate', 'Training Steps', 'LR')
        
        # 8. Entropy Loss
        ax8 = plt.subplot(3, 3, 8)
        self._plot_metric_comparison('losses/entropy_loss', ax8, 'Entropy Loss', 'Training Steps', 'Loss')
        
        # 9. Summary Statistics (Text)
        ax9 = plt.subplot(3, 3, 9)
        self._create_summary_text_plot(ax9)
        
        plt.tight_layout()
        plt.savefig('comprehensive_cyberwheel_analysis.png', dpi=300, bbox_inches='tight')
        print("  Saved: comprehensive_cyberwheel_analysis.png")
        
        return fig
    
    def _plot_metric_comparison(self, metric_name, ax, title, xlabel, ylabel):
        """Plot a specific metric across all experiments"""
        plotted = False
        
        for exp_name, exp_data in self.all_metrics.items():
            if not exp_data:
                continue
                
            for run_key, run_data in exp_data.items():
                if metric_name in run_data['metrics']:
                    data = run_data['metrics'][metric_name]
                    if data['values']:
                        label = f"{exp_name}" if run_key == 'main' else f"{exp_name}_{run_key}"
                        ax.plot(data['steps'], data['values'], label=label, alpha=0.8, linewidth=2)
                        plotted = True
        
        if plotted:
            ax.set_title(title, fontsize=12, fontweight='bold')
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.grid(True, alpha=0.3)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        else:
            ax.text(0.5, 0.5, f'No data for\n{metric_name}', 
                   horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            ax.set_title(title, fontsize=12, fontweight='bold')
    
    def _create_summary_text_plot(self, ax):
        """Create a text-based summary plot"""
        ax.axis('off')
        
        summary_text = "EXPERIMENT SUMMARY\n\n"
        
        for exp_name in self.verified_experiments:
            if exp_name in self.all_metrics and self.all_metrics[exp_name]:
                summary_text += f"✓ {exp_name}\n"
                
                # Get key stats if available
                for run_key, run_data in self.all_metrics[exp_name].items():
                    if 'charts/episodic_return' in run_data['metrics']:
                        final_return = run_data['metrics']['charts/episodic_return']['values'][-1]
                        summary_text += f"  Final Return: {final_return:.2f}\n"
                        break
            else:
                summary_text += f"✗ {exp_name} - No data\n"
        
        ax.text(0.1, 0.9, summary_text, transform=ax.transAxes, fontsize=10, 
                verticalalignment='top', fontfamily='monospace')
    
    def save_detailed_metrics(self):
        """Save detailed metrics to JSON and CSV files"""
        print("\n" + "="*60)
        print("SAVING DETAILED METRICS")
        print("="*60)
        
        # Save raw metrics to JSON
        with open('cyberwheel_raw_metrics.json', 'w') as f:
            # Convert numpy arrays to lists for JSON serialization
            json_data = {}
            for exp_name, exp_data in self.all_metrics.items():
                json_data[exp_name] = {}
                for run_key, run_data in exp_data.items():
                    json_data[exp_name][run_key] = {
                        'file_path': run_data['file_path'],
                        'file_size': run_data['file_size'],
                        'modification_time': run_data['modification_time'].isoformat(),
                        'metrics': {}
                    }
                    for metric_name, metric_data in run_data['metrics'].items():
                        json_data[exp_name][run_key]['metrics'][metric_name] = {
                            'steps': metric_data['steps'],
                            'values': metric_data['values'],
                            'count': metric_data['count']
                        }
            
            json.dump(json_data, f, indent=2)
        print("  Saved: cyberwheel_raw_metrics.json")
        
        # Save summary statistics to CSV
        summary_rows = []
        for exp_name, exp_summary in self.summary_stats.items():
            for run_key, run_data in exp_summary['metrics_per_run'].items():
                row = {
                    'experiment': exp_name,
                    'run': run_key,
                    'total_metrics': run_data['total_metrics'],
                    'file_size_mb': run_data['file_size_mb'],
                }
                
                # Add key metrics
                for metric_name, metric_stats in run_data['key_metrics'].items():
                    for stat_name, stat_value in metric_stats.items():
                        row[f"{metric_name}_{stat_name}"] = stat_value
                
                summary_rows.append(row)
        
        summary_df = pd.DataFrame(summary_rows)
        summary_df.to_csv('cyberwheel_metrics_summary.csv', index=False)
        print("  Saved: cyberwheel_metrics_summary.csv")
        
        return summary_df
    
    def print_comprehensive_report(self):
        """Print a comprehensive report of all findings"""
        print("\n" + "="*80)
        print("COMPREHENSIVE CYBERWHEEL TRAINING METRICS REPORT")
        print("="*80)
        
        print(f"\nDATA EXTRACTION SUMMARY:")
        print(f"  Total experiments processed: {len(self.all_metrics)}")
        print(f"  Verified experiments found: {len([e for e in self.verified_experiments if e in self.all_metrics])}")
        
        for exp_name in self.verified_experiments:
            if exp_name in self.all_metrics and self.all_metrics[exp_name]:
                print(f"\n{exp_name}:")
                exp_data = self.all_metrics[exp_name]
                
                for run_key, run_data in exp_data.items():
                    metrics = run_data['metrics']
                    print(f"  Run {run_key}:")
                    print(f"    File: {os.path.basename(run_data['file_path'])}")
                    print(f"    Size: {run_data['file_size'] / (1024*1024):.2f} MB")
                    print(f"    Metrics count: {len(metrics)}")
                    
                    # Show key metrics
                    if 'charts/episodic_return' in metrics:
                        returns = metrics['charts/episodic_return']['values']
                        if returns:
                            print(f"    Final return: {returns[-1]:.2f}")
                            print(f"    Max return: {max(returns):.2f}")
                            print(f"    Total training steps: {max(metrics['charts/episodic_return']['steps'])}")
                    
                    if 'evaluation/time_step_till_impact_avg' in metrics:
                        impact_times = metrics['evaluation/time_step_till_impact_avg']['values']
                        if impact_times:
                            print(f"    Avg time to impact: {np.mean(impact_times):.2f} steps")
                    
                    print(f"    Available metrics: {list(metrics.keys())[:5]}..." if len(metrics) > 5 else f"    Available metrics: {list(metrics.keys())}")
            else:
                print(f"\n{exp_name}: NO DATA FOUND")

def main():
    """Main execution function"""
    extractor = CyberwheelTensorBoardExtractor()
    
    # Extract all metrics
    all_metrics = extractor.extract_all_metrics()
    
    if not all_metrics:
        print("No metrics extracted. Exiting.")
        return
    
    # Generate comprehensive summary
    summary = extractor.generate_metrics_summary()
    
    # Create visualizations
    extractor.create_comprehensive_visualizations()
    
    # Save detailed data
    extractor.save_detailed_metrics()
    
    # Print comprehensive report
    extractor.print_comprehensive_report()
    
    print("\n" + "="*80)
    print("EXTRACTION COMPLETE!")
    print("Generated files:")
    print("  - comprehensive_cyberwheel_analysis.png")
    print("  - cyberwheel_raw_metrics.json")  
    print("  - cyberwheel_metrics_summary.csv")
    print("="*80)

if __name__ == "__main__":
    main()