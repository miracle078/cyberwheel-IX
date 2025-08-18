#!/usr/bin/env python3
"""
Comprehensive Network State Analysis for Cyberwheel Experiments
Analyzes all pickle files containing NetworkX graph data to understand network dynamics,
decoy deployment patterns, and structural evolution throughout training.
"""

import pickle
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from collections import defaultdict, Counter
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class CyberwheelNetworkAnalyzer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.graphs_path = self.base_path / "cyberwheel-complete" / "cyberwheel" / "data" / "graphs"
        self.results = defaultdict(list)
        self.network_metrics = []
        self.decoy_analysis = []
        self.temporal_analysis = []
        
    def find_all_pickle_files(self):
        """Find all pickle files in the graphs directory and subdirectories"""
        pickle_files = []
        for root, dirs, files in os.walk(self.graphs_path):
            for file in files:
                if file.endswith('.pickle') or file.endswith('.pkl'):
                    pickle_files.append(os.path.join(root, file))
        
        # Group files by experiment directory
        experiment_files = defaultdict(list)
        for file_path in pickle_files:
            # Extract experiment name from path
            rel_path = os.path.relpath(file_path, self.graphs_path)
            experiment = rel_path.split(os.sep)[0]
            experiment_files[experiment].append(file_path)
        
        print(f"Found {len(pickle_files)} pickle files across {len(experiment_files)} experiments:")
        for exp, files in experiment_files.items():
            print(f"  {exp}: {len(files)} files")
        
        return experiment_files
    
    def load_network_graph(self, file_path):
        """Load NetworkX graph from pickle file"""
        try:
            # Add cyberwheel to path for imports
            import sys
            sys.path.insert(0, str(self.base_path / "cyberwheel"))
            sys.path.insert(0, str(self.base_path / "cyberwheel-complete" / "cyberwheel"))
            
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
            
            # Handle different data types
            if isinstance(data, (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)):
                return data
            elif hasattr(data, 'graph') and isinstance(data.graph, (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)):
                return data.graph
            elif hasattr(data, 'network_graph'):
                return data.network_graph
            elif hasattr(data, '__dict__'):
                # Look for NetworkX graph in object attributes
                for attr_name, attr_value in data.__dict__.items():
                    if isinstance(attr_value, (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)):
                        return attr_value
            
            return None
        except Exception as e:
            if "cannot import name" not in str(e):
                print(f"Error loading {file_path}: {e}")
            return None
    
    def extract_network_metrics(self, graph, experiment, episode, step):
        """Extract comprehensive network metrics from NetworkX graph"""
        if graph is None or not isinstance(graph, (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)):
            return None
        
        # Convert directed graphs to undirected for connectivity analysis
        if isinstance(graph, (nx.DiGraph, nx.MultiDiGraph)):
            undirected_graph = graph.to_undirected()
        else:
            undirected_graph = graph
        
        metrics = {
            'experiment': experiment,
            'episode': episode,
            'step': step,
            'num_nodes': graph.number_of_nodes(),
            'num_edges': graph.number_of_edges(),
            'density': nx.density(graph),
            'is_directed': isinstance(graph, (nx.DiGraph, nx.MultiDiGraph)),
            'is_connected': nx.is_connected(undirected_graph) if undirected_graph.number_of_nodes() > 0 else False,
            'num_components': nx.number_connected_components(undirected_graph),
        }
        
        # Only compute expensive metrics for non-empty graphs
        if metrics['num_nodes'] > 0:
            # Centrality metrics (sample for large graphs)
            if metrics['num_nodes'] < 1000:
                degree_centrality = nx.degree_centrality(undirected_graph)
                betweenness_centrality = nx.betweenness_centrality(undirected_graph, k=min(100, metrics['num_nodes']))
                closeness_centrality = nx.closeness_centrality(undirected_graph)
                
                metrics.update({
                    'avg_degree_centrality': np.mean(list(degree_centrality.values())),
                    'max_degree_centrality': max(degree_centrality.values()),
                    'avg_betweenness_centrality': np.mean(list(betweenness_centrality.values())),
                    'max_betweenness_centrality': max(betweenness_centrality.values()),
                    'avg_closeness_centrality': np.mean(list(closeness_centrality.values())),
                })
            else:
                metrics.update({
                    'avg_degree_centrality': None,
                    'max_degree_centrality': None,
                    'avg_betweenness_centrality': None,
                    'max_betweenness_centrality': None,
                    'avg_closeness_centrality': None,
                })
            
            # Clustering coefficient
            if metrics['num_nodes'] < 5000:
                metrics['avg_clustering'] = nx.average_clustering(undirected_graph)
            else:
                metrics['avg_clustering'] = None
            
            # Degree distribution
            degrees = [d for n, d in graph.degree()]
            metrics.update({
                'avg_degree': np.mean(degrees),
                'max_degree': max(degrees) if degrees else 0,
                'degree_std': np.std(degrees) if len(degrees) > 1 else 0,
            })
            
            # Diameter and radius (for small connected graphs)
            if metrics['is_connected'] and metrics['num_nodes'] < 1000:
                try:
                    metrics['diameter'] = nx.diameter(undirected_graph)
                    metrics['radius'] = nx.radius(undirected_graph)
                except:
                    metrics['diameter'] = None
                    metrics['radius'] = None
            else:
                metrics['diameter'] = None
                metrics['radius'] = None
        
        return metrics
    
    def analyze_node_types(self, graph, experiment, episode, step):
        """Analyze different types of nodes (decoy, compromised, etc.)"""
        if graph is None or not isinstance(graph, (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph)):
            return None
        
        node_analysis = {
            'experiment': experiment,
            'episode': episode,
            'step': step,
            'total_nodes': graph.number_of_nodes(),
        }
        
        # Count different node types based on attributes
        decoy_nodes = 0
        compromised_nodes = 0
        isolated_nodes = 0
        server_nodes = 0
        user_nodes = 0
        
        for node, data in graph.nodes(data=True):
            if isinstance(data, dict):
                # Check for decoy indicators
                if any(key.lower().find('decoy') != -1 for key in data.keys() if isinstance(key, str)):
                    decoy_nodes += 1
                
                # Check for compromise status
                if any(key.lower() in ['compromised', 'infected', 'pwned'] for key in data.keys() if isinstance(key, str)):
                    compromised_nodes += 1
                
                # Check for isolation status
                if any(key.lower() in ['isolated', 'quarantined'] for key in data.keys() if isinstance(key, str)):
                    isolated_nodes += 1
                
                # Check node types
                node_type = data.get('type', '').lower()
                if 'server' in node_type:
                    server_nodes += 1
                elif 'user' in node_type or 'client' in node_type:
                    user_nodes += 1
        
        # Calculate isolated nodes by degree
        isolated_by_degree = len([n for n, d in graph.degree() if d == 0])
        
        node_analysis.update({
            'decoy_nodes': decoy_nodes,
            'compromised_nodes': compromised_nodes,
            'isolated_nodes': isolated_nodes,
            'isolated_by_degree': isolated_by_degree,
            'server_nodes': server_nodes,
            'user_nodes': user_nodes,
            'decoy_ratio': decoy_nodes / max(1, graph.number_of_nodes()),
            'compromise_ratio': compromised_nodes / max(1, graph.number_of_nodes()),
        })
        
        return node_analysis
    
    def parse_filename(self, file_path):
        """Parse episode and step from filename (format: episode_step.pickle)"""
        filename = os.path.basename(file_path)
        name_parts = filename.replace('.pickle', '').replace('.pkl', '').split('_')
        
        try:
            if len(name_parts) >= 2:
                episode = int(name_parts[0])
                step = int(name_parts[1])
                return episode, step
            else:
                return 0, 0
        except (ValueError, IndexError):
            return 0, 0
    
    def analyze_all_experiments(self):
        """Analyze all pickle files across all experiments"""
        experiment_files = self.find_all_pickle_files()
        
        print("\nAnalyzing network graphs...")
        
        for experiment, files in experiment_files.items():
            print(f"\nProcessing {experiment}...")
            
            # Sort files by episode and step
            files.sort(key=lambda x: self.parse_filename(x))
            
            for i, file_path in enumerate(files):
                if i % 50 == 0:
                    print(f"  Processed {i}/{len(files)} files...")
                
                episode, step = self.parse_filename(file_path)
                graph = self.load_network_graph(file_path)
                
                if graph is not None:
                    # Extract network metrics
                    metrics = self.extract_network_metrics(graph, experiment, episode, step)
                    if metrics:
                        self.network_metrics.append(metrics)
                    
                    # Analyze node types and decoys
                    node_analysis = self.analyze_node_types(graph, experiment, episode, step)
                    if node_analysis:
                        self.decoy_analysis.append(node_analysis)
        
        print(f"\nAnalysis complete! Processed {len(self.network_metrics)} network states.")
    
    def create_dataframes(self):
        """Convert analysis results to pandas DataFrames"""
        self.network_df = pd.DataFrame(self.network_metrics)
        self.decoy_df = pd.DataFrame(self.decoy_analysis)
        
        print(f"\nCreated DataFrames:")
        print(f"  Network metrics: {len(self.network_df)} records")
        print(f"  Decoy analysis: {len(self.decoy_df)} records")
    
    def analyze_temporal_patterns(self):
        """Analyze how networks evolve over time within episodes"""
        print("\nAnalyzing temporal patterns...")
        
        temporal_results = []
        
        for experiment in self.network_df['experiment'].unique():
            exp_data = self.network_df[self.network_df['experiment'] == experiment]
            
            for episode in exp_data['episode'].unique():
                episode_data = exp_data[exp_data['episode'] == episode].sort_values('step')
                
                if len(episode_data) > 1:
                    # Calculate changes over time
                    initial_nodes = episode_data['num_nodes'].iloc[0]
                    final_nodes = episode_data['num_nodes'].iloc[-1]
                    max_nodes = episode_data['num_nodes'].max()
                    
                    initial_edges = episode_data['num_edges'].iloc[0]
                    final_edges = episode_data['num_edges'].iloc[-1]
                    
                    temporal_results.append({
                        'experiment': experiment,
                        'episode': episode,
                        'initial_nodes': initial_nodes,
                        'final_nodes': final_nodes,
                        'max_nodes': max_nodes,
                        'node_growth': final_nodes - initial_nodes,
                        'initial_edges': initial_edges,
                        'final_edges': final_edges,
                        'edge_growth': final_edges - initial_edges,
                        'steps_recorded': len(episode_data),
                        'avg_density': episode_data['density'].mean(),
                        'density_change': episode_data['density'].iloc[-1] - episode_data['density'].iloc[0],
                    })
        
        self.temporal_df = pd.DataFrame(temporal_results)
        print(f"  Temporal analysis: {len(self.temporal_df)} episodes analyzed")
    
    def generate_visualizations(self):
        """Generate comprehensive visualizations of network dynamics"""
        print("\nGenerating visualizations...")
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        fig_size = (15, 10)
        
        # 1. Network size evolution across experiments
        plt.figure(figsize=fig_size)
        
        plt.subplot(2, 3, 1)
        for experiment in self.network_df['experiment'].unique():
            exp_data = self.network_df[self.network_df['experiment'] == experiment]
            # Sample data for cleaner plots
            if len(exp_data) > 1000:
                exp_data = exp_data.sample(n=1000).sort_values(['episode', 'step'])
            
            plt.plot(range(len(exp_data)), exp_data['num_nodes'], 
                    label=experiment.replace('_', ' '), alpha=0.7)
        plt.title('Network Size Evolution')
        plt.xlabel('Time Steps')
        plt.ylabel('Number of Nodes')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # 2. Network density comparison
        plt.subplot(2, 3, 2)
        self.network_df.boxplot(column='density', by='experiment', ax=plt.gca())
        plt.title('Network Density by Experiment')
        plt.xlabel('Experiment')
        plt.ylabel('Network Density')
        plt.xticks(rotation=45)
        
        # 3. Decoy deployment patterns
        plt.subplot(2, 3, 3)
        decoy_summary = self.decoy_df.groupby('experiment')['decoy_ratio'].mean()
        decoy_summary.plot(kind='bar')
        plt.title('Average Decoy Ratio by Experiment')
        plt.xlabel('Experiment')
        plt.ylabel('Decoy Ratio')
        plt.xticks(rotation=45)
        
        # 4. Network connectivity
        plt.subplot(2, 3, 4)
        connectivity = self.network_df.groupby('experiment')['is_connected'].mean()
        connectivity.plot(kind='bar', color='orange')
        plt.title('Network Connectivity Rate')
        plt.xlabel('Experiment')
        plt.ylabel('Fraction Connected')
        plt.xticks(rotation=45)
        
        # 5. Compromise patterns
        plt.subplot(2, 3, 5)
        if not self.decoy_df.empty and 'compromise_ratio' in self.decoy_df.columns:
            compromise_summary = self.decoy_df.groupby('experiment')['compromise_ratio'].mean()
            compromise_summary.plot(kind='bar', color='red', alpha=0.7)
            plt.title('Average Compromise Ratio')
            plt.xlabel('Experiment')
            plt.ylabel('Compromise Ratio')
            plt.xticks(rotation=45)
        
        # 6. Temporal network evolution
        plt.subplot(2, 3, 6)
        if hasattr(self, 'temporal_df') and not self.temporal_df.empty:
            for experiment in self.temporal_df['experiment'].unique():
                exp_temporal = self.temporal_df[self.temporal_df['experiment'] == experiment]
                plt.plot(exp_temporal['episode'], exp_temporal['node_growth'], 
                        'o-', label=experiment.replace('_', ' '), alpha=0.7)
            plt.title('Network Growth by Episode')
            plt.xlabel('Episode')
            plt.ylabel('Node Growth')
            plt.legend()
        
        plt.tight_layout()
        plt.savefig(self.base_path / 'Network_Dynamics_Analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Additional detailed visualizations
        self._create_detailed_visualizations()
    
    def _create_detailed_visualizations(self):
        """Create additional detailed visualizations"""
        
        # Degree distribution analysis
        plt.figure(figsize=(15, 5))
        
        plt.subplot(1, 3, 1)
        self.network_df.boxplot(column='avg_degree', by='experiment', ax=plt.gca())
        plt.title('Average Node Degree by Experiment')
        plt.xlabel('Experiment')
        plt.ylabel('Average Degree')
        plt.xticks(rotation=45)
        
        plt.subplot(1, 3, 2)
        if 'avg_clustering' in self.network_df.columns:
            clustering_data = self.network_df.dropna(subset=['avg_clustering'])
            if not clustering_data.empty:
                clustering_data.boxplot(column='avg_clustering', by='experiment', ax=plt.gca())
                plt.title('Network Clustering by Experiment')
                plt.xlabel('Experiment')
                plt.ylabel('Average Clustering Coefficient')
                plt.xticks(rotation=45)
        
        plt.subplot(1, 3, 3)
        # Network evolution over episodes
        if hasattr(self, 'temporal_df') and not self.temporal_df.empty:
            for experiment in self.temporal_df['experiment'].unique()[:3]:  # Limit to top 3
                exp_data = self.temporal_df[self.temporal_df['experiment'] == experiment]
                plt.scatter(exp_data['initial_nodes'], exp_data['final_nodes'], 
                          label=experiment.replace('_', ' '), alpha=0.6)
            plt.plot([0, plt.xlim()[1]], [0, plt.xlim()[1]], 'k--', alpha=0.5)
            plt.title('Initial vs Final Network Size')
            plt.xlabel('Initial Nodes')
            plt.ylabel('Final Nodes')
            plt.legend()
        
        plt.tight_layout()
        plt.savefig(self.base_path / 'Network_Detailed_Analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def generate_summary_statistics(self):
        """Generate comprehensive summary statistics"""
        print("\nGenerating summary statistics...")
        
        summary_stats = {}
        
        # Overall statistics
        summary_stats['total_network_states'] = len(self.network_df)
        summary_stats['experiments_analyzed'] = self.network_df['experiment'].nunique()
        summary_stats['episodes_analyzed'] = self.network_df.groupby('experiment')['episode'].nunique().to_dict()
        
        # Network size statistics
        summary_stats['network_size'] = {
            'min_nodes': self.network_df['num_nodes'].min(),
            'max_nodes': self.network_df['num_nodes'].max(),
            'avg_nodes': self.network_df['num_nodes'].mean(),
            'std_nodes': self.network_df['num_nodes'].std(),
        }
        
        # Network density statistics
        summary_stats['network_density'] = {
            'min_density': self.network_df['density'].min(),
            'max_density': self.network_df['density'].max(),
            'avg_density': self.network_df['density'].mean(),
            'std_density': self.network_df['density'].std(),
        }
        
        # Experiment-specific statistics
        exp_stats = {}
        for experiment in self.network_df['experiment'].unique():
            exp_data = self.network_df[self.network_df['experiment'] == experiment]
            decoy_data = self.decoy_df[self.decoy_df['experiment'] == experiment]
            
            exp_stats[experiment] = {
                'network_states': len(exp_data),
                'avg_nodes': exp_data['num_nodes'].mean(),
                'avg_edges': exp_data['num_edges'].mean(),
                'avg_density': exp_data['density'].mean(),
                'connectivity_rate': exp_data['is_connected'].mean(),
                'avg_decoy_ratio': decoy_data['decoy_ratio'].mean() if not decoy_data.empty else 0,
                'avg_compromise_ratio': decoy_data['compromise_ratio'].mean() if not decoy_data.empty else 0,
            }
        
        summary_stats['by_experiment'] = exp_stats
        
        # Save summary statistics
        with open(self.base_path / 'Network_Analysis_Summary.json', 'w') as f:
            json.dump(summary_stats, f, indent=2, default=str)
        
        return summary_stats
    
    def save_detailed_results(self):
        """Save all detailed analysis results"""
        print("\nSaving detailed results...")
        
        # Save main dataframes
        self.network_df.to_csv(self.base_path / 'Network_Metrics_Detailed.csv', index=False)
        self.decoy_df.to_csv(self.base_path / 'Decoy_Analysis_Detailed.csv', index=False)
        
        if hasattr(self, 'temporal_df'):
            self.temporal_df.to_csv(self.base_path / 'Temporal_Analysis_Detailed.csv', index=False)
        
        # Create summary tables
        network_summary = self.network_df.groupby('experiment').agg({
            'num_nodes': ['mean', 'std', 'min', 'max'],
            'num_edges': ['mean', 'std', 'min', 'max'],
            'density': ['mean', 'std', 'min', 'max'],
            'is_connected': 'mean',
            'avg_degree': ['mean', 'std'],
        }).round(4)
        
        network_summary.to_csv(self.base_path / 'Network_Summary_Statistics.csv')
        
        decoy_summary = self.decoy_df.groupby('experiment').agg({
            'decoy_ratio': ['mean', 'std', 'min', 'max'],
            'compromise_ratio': ['mean', 'std', 'min', 'max'],
            'decoy_nodes': ['mean', 'std', 'min', 'max'],
            'compromised_nodes': ['mean', 'std', 'min', 'max'],
        }).round(4)
        
        decoy_summary.to_csv(self.base_path / 'Decoy_Summary_Statistics.csv')
        
        print(f"Results saved to:")
        print(f"  - Network_Metrics_Detailed.csv")
        print(f"  - Decoy_Analysis_Detailed.csv")
        print(f"  - Network_Summary_Statistics.csv")
        print(f"  - Decoy_Summary_Statistics.csv")
        print(f"  - Network_Analysis_Summary.json")
    
    def run_comprehensive_analysis(self):
        """Run the complete network analysis pipeline"""
        print("=== Comprehensive Cyberwheel Network Analysis ===")
        print(f"Base path: {self.base_path}")
        print(f"Graphs path: {self.graphs_path}")
        
        # Main analysis pipeline
        self.analyze_all_experiments()
        self.create_dataframes()
        self.analyze_temporal_patterns()
        
        # Generate outputs
        summary_stats = self.generate_summary_statistics()
        self.generate_visualizations()
        self.save_detailed_results()
        
        # Print final summary
        print("\n=== ANALYSIS COMPLETE ===")
        print(f"Total network states analyzed: {summary_stats['total_network_states']}")
        print(f"Experiments: {summary_stats['experiments_analyzed']}")
        print(f"Average network size: {summary_stats['network_size']['avg_nodes']:.1f} nodes")
        print(f"Average network density: {summary_stats['network_density']['avg_density']:.4f}")
        
        return summary_stats

def main():
    """Main execution function"""
    base_path = Path(r"C:\Users\mirac\Documents\Git\cyberwheel-IX")
    
    analyzer = CyberwheelNetworkAnalyzer(base_path)
    results = analyzer.run_comprehensive_analysis()
    
    return analyzer, results

if __name__ == "__main__":
    analyzer, results = main()
    print("\nAnalysis completed successfully!")
    print("Check the generated files for detailed results and visualizations.")