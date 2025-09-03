#!/usr/bin/env python3
"""
Baseline Comparison Visualization Generator
Author: Miracle Akanmode
Date: August 2025

Generate comprehensive graphical and numerical representations of baseline
comparison results for academic publication and analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality plotting parameters
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams.update({
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 16,
    'figure.figsize': (12, 8),
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})

class BaselineVisualizationGenerator:
    """Generate comprehensive baseline comparison visualizations"""
    
    def __init__(self, results_dir="baseline_comparison_results"):
        self.results_dir = Path(results_dir)
        self.output_dir = Path("baseline_comparison_visualizations")
        self.output_dir.mkdir(exist_ok=True)
        
        # Load data
        self.df = pd.read_csv(self.results_dir / "results.csv")
        with open(self.results_dir / "comparison_summary.json", 'r') as f:
            self.summary = json.load(f)
        
        # Color scheme for agents
        self.agent_colors = {
            'PPO_BestProduction': '#FF6B6B',      # Red - ML approach
            'StaticBaseline': '#4ECDC4',          # Teal - Rule-based
            'RandomBaseline': '#45B7D1',          # Blue - Stochastic
            'RuleBaseline': '#96CEB4',            # Green - Logic-based
            'InactiveBaseline': '#FFEAA7'         # Yellow - Control
        }
        
        print(f"📊 Loaded data: {len(self.df)} records across {self.df['Environment'].nunique()} environments")
        
    def generate_all_visualizations(self):
        """Generate complete set of baseline comparison visualizations"""
        print("🎨 Generating comprehensive baseline comparison visualizations...")
        
        # 1. Performance comparison plots
        self.plot_performance_comparison()
        self.plot_performance_by_environment()
        
        # 2. Statistical analysis
        self.plot_variance_analysis()
        self.plot_action_distribution()
        
        # 3. Comprehensive comparison
        self.plot_comprehensive_comparison()
        
        # 4. Publication-ready summary
        self.generate_publication_summary()
        
        print(f"✅ All visualizations saved to: {self.output_dir}")
        
    def plot_performance_comparison(self):
        """Generate performance comparison bar chart"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Small Network Performance
        small_data = self.df[self.df['Environment'] == 'small_network']
        bars1 = ax1.bar(range(len(small_data)), small_data['Total_Reward'], 
                       color=[self.agent_colors[agent] for agent in small_data['Agent']],
                       alpha=0.8, edgecolor='black', linewidth=0.5)
        
        ax1.set_title('Small Network Performance Comparison', fontweight='bold')
        ax1.set_xlabel('Baseline Agents')
        ax1.set_ylabel('Total Reward')
        ax1.set_xticks(range(len(small_data)))
        ax1.set_xticklabels(small_data['Agent'], rotation=45, ha='right')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, bar in enumerate(bars1):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # Medium Network Performance
        medium_data = self.df[self.df['Environment'] == 'medium_network']
        bars2 = ax2.bar(range(len(medium_data)), medium_data['Total_Reward'],
                       color=[self.agent_colors[agent] for agent in medium_data['Agent']],
                       alpha=0.8, edgecolor='black', linewidth=0.5)
        
        ax2.set_title('Medium Network Performance Comparison', fontweight='bold')
        ax2.set_xlabel('Baseline Agents')
        ax2.set_ylabel('Total Reward')
        ax2.set_xticks(range(len(medium_data)))
        ax2.set_xticklabels(medium_data['Agent'], rotation=45, ha='right')
        ax2.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for i, bar in enumerate(bars2):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
                    f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "baseline_performance_comparison.png")
        plt.savefig(self.output_dir / "baseline_performance_comparison.pdf")
        plt.close()
        
        print("✅ Generated: baseline_performance_comparison.png/pdf")
        
    def plot_performance_by_environment(self):
        """Generate grouped performance comparison"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Prepare data for grouped bar chart
        agents = self.df['Agent'].unique()
        environments = self.df['Environment'].unique()
        
        x = np.arange(len(agents))
        width = 0.35
        
        small_rewards = []
        medium_rewards = []
        
        for agent in agents:
            small_reward = self.df[(self.df['Agent'] == agent) & 
                                 (self.df['Environment'] == 'small_network')]['Total_Reward'].values[0]
            medium_reward = self.df[(self.df['Agent'] == agent) & 
                                  (self.df['Environment'] == 'medium_network')]['Total_Reward'].values[0]
            small_rewards.append(small_reward)
            medium_rewards.append(medium_reward)
        
        bars1 = ax.bar(x - width/2, small_rewards, width, label='Small Network', 
                      alpha=0.8, edgecolor='black', linewidth=0.5)
        bars2 = ax.bar(x + width/2, medium_rewards, width, label='Medium Network', 
                      alpha=0.8, edgecolor='black', linewidth=0.5)
        
        ax.set_title('Baseline Agent Performance Across Environments', fontweight='bold', fontsize=16)
        ax.set_xlabel('Baseline Agents', fontweight='bold')
        ax.set_ylabel('Total Reward', fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(agents, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                       f'{height:.0f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "performance_by_environment.png")
        plt.savefig(self.output_dir / "performance_by_environment.pdf")
        plt.close()
        
        print("✅ Generated: performance_by_environment.png/pdf")
        
    def plot_variance_analysis(self):
        """Generate variance and consistency analysis"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Performance vs Variance scatter plot
        ax1.scatter(self.df['Reward_StdDev'], self.df['Total_Reward'], 
                   c=[self.agent_colors[agent] for agent in self.df['Agent']], 
                   s=100, alpha=0.7, edgecolor='black', linewidth=0.5)
        
        # Add agent labels
        for i, row in self.df.iterrows():
            ax1.annotate(f"{row['Agent'][:8]}...", 
                        (row['Reward_StdDev'], row['Total_Reward']),
                        xytext=(5, 5), textcoords='offset points', fontsize=8)
        
        ax1.set_xlabel('Standard Deviation (Consistency)', fontweight='bold')
        ax1.set_ylabel('Total Reward (Performance)', fontweight='bold')
        ax1.set_title('Performance vs Consistency Trade-off', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # PPO vs Best Random performance comparison
        ppo_data = self.df[self.df['Agent'] == 'PPO_BestProduction']
        random_data = self.df[self.df['Agent'] == 'RandomBaseline']
        
        agents_comp = ['PPO_BestProduction', 'RandomBaseline']
        avg_performance = [ppo_data['Total_Reward'].mean(), random_data['Total_Reward'].mean()]
        avg_std = [ppo_data['Reward_StdDev'].mean(), random_data['Reward_StdDev'].mean()]
        
        bars = ax2.bar(agents_comp, avg_performance, 
                      color=[self.agent_colors[agent] for agent in agents_comp],
                      alpha=0.8, edgecolor='black', linewidth=0.5,
                      yerr=avg_std, capsize=5)
        
        ax2.set_title('PPO vs RandomBaseline: Performance & Consistency', fontweight='bold')
        ax2.set_ylabel('Average Total Reward', fontweight='bold')
        ax2.set_xticklabels(['PPO\n(Learned)', 'Random\n(Stochastic)'])
        
        # Add value labels
        for i, bar in enumerate(bars):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + avg_std[i] + 10,
                    f'{height:.1f}±{avg_std[i]:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / "variance_analysis.png")
        plt.savefig(self.output_dir / "variance_analysis.pdf")
        plt.close()
        
        print("✅ Generated: variance_analysis.png/pdf")
        
    def plot_action_distribution(self):
        """Generate action distribution analysis"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        agents = self.df['Agent'].unique()
        action_types = ['Deploy_Actions', 'Remove_Actions', 'Nothing_Actions']
        
        for i, agent in enumerate(agents):
            agent_data = self.df[self.df['Agent'] == agent]
            
            # Aggregate action data across environments
            total_deploy = agent_data['Deploy_Actions'].sum()
            total_remove = agent_data['Remove_Actions'].sum()
            total_nothing = agent_data['Nothing_Actions'].sum()
            total_actions = total_deploy + total_remove + total_nothing
            
            # Calculate percentages
            percentages = [
                (total_deploy / total_actions) * 100,
                (total_remove / total_actions) * 100,
                (total_nothing / total_actions) * 100
            ]
            
            # Create pie chart
            colors = ['#FF9999', '#66B2FF', '#99FF99']
            wedges, texts, autotexts = axes[i].pie(percentages, labels=action_types, autopct='%1.1f%%',
                                                  colors=colors, startangle=90)
            
            axes[i].set_title(f'{agent}\nAction Distribution', fontweight='bold', fontsize=10)
            
            # Make percentage text bold
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
        
        # Remove empty subplot
        if len(agents) < len(axes):
            axes[-1].remove()
        
        plt.suptitle('Agent Action Distribution Analysis', fontweight='bold', fontsize=16)
        plt.tight_layout()
        plt.savefig(self.output_dir / "action_distribution.png")
        plt.savefig(self.output_dir / "action_distribution.pdf")
        plt.close()
        
        print("✅ Generated: action_distribution.png/pdf")
        
    def plot_comprehensive_comparison(self):
        """Generate comprehensive comparison dashboard"""
        fig = plt.figure(figsize=(20, 12))
        
        # Create grid for subplots
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # 1. Overall Performance Ranking
        ax1 = fig.add_subplot(gs[0, :])
        overall_performance = self.df.groupby('Agent')['Total_Reward'].mean().sort_values(ascending=False)
        bars = ax1.bar(range(len(overall_performance)), overall_performance.values,
                      color=[self.agent_colors[agent] for agent in overall_performance.index],
                      alpha=0.8, edgecolor='black', linewidth=1)
        ax1.set_title('Overall Performance Ranking (Average Across Environments)', fontweight='bold', fontsize=14)
        ax1.set_xticks(range(len(overall_performance)))
        ax1.set_xticklabels(overall_performance.index, rotation=45, ha='right')
        ax1.set_ylabel('Average Total Reward')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add ranking numbers and values
        for i, (bar, value) in enumerate(zip(bars, overall_performance.values)):
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
                    f'#{i+1}\n{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # 2. PPO Focus Analysis
        ax2 = fig.add_subplot(gs[1, 0])
        ppo_vs_others = self.df.groupby('Agent')['Total_Reward'].mean()
        ppo_performance = ppo_vs_others['PPO_BestProduction']
        others_avg = ppo_vs_others.drop('PPO_BestProduction').mean()
        
        comparison_data = [ppo_performance, others_avg]
        comparison_labels = ['PPO\n(Our Approach)', 'Average\nBaselines']
        bars2 = ax2.bar(comparison_labels, comparison_data, 
                       color=['#FF6B6B', '#95A5A6'], alpha=0.8, edgecolor='black', linewidth=1)
        ax2.set_title('PPO vs Average Baselines', fontweight='bold')
        ax2.set_ylabel('Average Total Reward')
        
        for bar, value in zip(bars2, comparison_data):
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 5,
                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # 3. Consistency Analysis
        ax3 = fig.add_subplot(gs[1, 1])
        consistency_data = self.df.groupby('Agent')['Reward_StdDev'].mean().sort_values()
        bars3 = ax3.bar(range(len(consistency_data)), consistency_data.values,
                       color=[self.agent_colors[agent] for agent in consistency_data.index],
                       alpha=0.8, edgecolor='black', linewidth=1)
        ax3.set_title('Consistency Ranking\n(Lower = More Consistent)', fontweight='bold')
        ax3.set_xticks(range(len(consistency_data)))
        ax3.set_xticklabels(consistency_data.index, rotation=45, ha='right')
        ax3.set_ylabel('Average Std Dev')
        
        # 4. Success Rate Analysis
        ax4 = fig.add_subplot(gs[1, 2])
        success_rates = []
        for agent in self.df['Agent'].unique():
            agent_data = self.df[self.df['Agent'] == agent]
            total_successful = agent_data['Successful_Actions'].sum()
            total_actions = agent_data['Successful_Actions'].sum() + agent_data['Failed_Actions'].sum()
            success_rate = (total_successful / total_actions) * 100 if total_actions > 0 else 0
            success_rates.append(success_rate)
        
        bars4 = ax4.bar(self.df['Agent'].unique(), success_rates,
                       color=[self.agent_colors[agent] for agent in self.df['Agent'].unique()],
                       alpha=0.8, edgecolor='black', linewidth=1)
        ax4.set_title('Success Rate Analysis', fontweight='bold')
        ax4.set_ylabel('Success Rate (%)')
        ax4.set_xticklabels(self.df['Agent'].unique(), rotation=45, ha='right')
        ax4.set_ylim([95, 100.5])  # Focus on the small variations
        
        # 5. Statistical Summary Table
        ax5 = fig.add_subplot(gs[2, :])
        ax5.axis('tight')
        ax5.axis('off')
        
        # Create summary statistics table
        summary_stats = []
        for agent in self.df['Agent'].unique():
            agent_data = self.df[self.df['Agent'] == agent]
            stats = {
                'Agent': agent,
                'Avg Reward': f"{agent_data['Total_Reward'].mean():.1f}",
                'Std Dev': f"{agent_data['Reward_StdDev'].mean():.1f}",
                'Min Reward': f"{agent_data['Total_Reward'].min():.1f}",
                'Max Reward': f"{agent_data['Total_Reward'].max():.1f}",
                'Deploy %': f"{(agent_data['Deploy_Actions'].sum() / (agent_data['Deploy_Actions'].sum() + agent_data['Remove_Actions'].sum() + agent_data['Nothing_Actions'].sum()) * 100):.1f}%"
            }
            summary_stats.append(stats)
        
        summary_df = pd.DataFrame(summary_stats)
        table = ax5.table(cellText=summary_df.values, colLabels=summary_df.columns,
                         cellLoc='center', loc='center', bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 2)
        
        # Style the table
        for (row, col), cell in table.get_celld().items():
            if row == 0:  # Header
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#E8E8E8')
            else:
                agent_name = summary_df.iloc[row-1]['Agent']
                cell.set_facecolor(self.agent_colors.get(agent_name, '#FFFFFF'))
                cell.set_alpha(0.3)
        
        plt.suptitle('Comprehensive Baseline Comparison Analysis', fontweight='bold', fontsize=18)
        plt.savefig(self.output_dir / "comprehensive_comparison.png")
        plt.savefig(self.output_dir / "comprehensive_comparison.pdf")
        plt.close()
        
        print("✅ Generated: comprehensive_comparison.png/pdf")
        
    def generate_publication_summary(self):
        """Generate publication-ready summary statistics"""
        
        # Create LaTeX table for publication
        latex_table = self.generate_latex_table()
        
        with open(self.output_dir / "baseline_comparison_table.tex", 'w') as f:
            f.write(latex_table)
        
        # Create numerical summary
        summary_text = self.generate_numerical_summary()
        
        with open(self.output_dir / "numerical_summary.txt", 'w') as f:
            f.write(summary_text)
        
        print("✅ Generated: baseline_comparison_table.tex")
        print("✅ Generated: numerical_summary.txt")
        
    def generate_latex_table(self):
        """Generate LaTeX table for publication"""
        
        latex_content = """\\begin{table}[H]
\\centering
\\caption{Comprehensive Baseline Algorithm Performance Comparison}
\\label{tab:baseline_comparison}
\\begin{tabular}{|l|c|c|c|c|c|}
\\hline
\\textbf{Agent} & \\textbf{Avg Reward} & \\textbf{Std Dev} & \\textbf{Consistency Rank} & \\textbf{Deploy \\%} & \\textbf{Performance Rank} \\\\
\\hline
"""
        
        # Calculate rankings
        avg_rewards = self.df.groupby('Agent')['Total_Reward'].mean().sort_values(ascending=False)
        consistency_rank = self.df.groupby('Agent')['Reward_StdDev'].mean().sort_values()
        
        rank_counter = 1
        consistency_counter = 1
        
        for agent in avg_rewards.index:
            agent_data = self.df[self.df['Agent'] == agent]
            avg_reward = agent_data['Total_Reward'].mean()
            std_dev = agent_data['Reward_StdDev'].mean()
            
            # Calculate deployment percentage
            total_deploy = agent_data['Deploy_Actions'].sum()
            total_actions = agent_data['Deploy_Actions'].sum() + agent_data['Remove_Actions'].sum() + agent_data['Nothing_Actions'].sum()
            deploy_pct = (total_deploy / total_actions) * 100 if total_actions > 0 else 0
            
            # Find consistency rank
            cons_rank = list(consistency_rank.index).index(agent) + 1
            
            agent_latex = agent.replace('_', '\\_')
            latex_content += f"{agent_latex} & {avg_reward:.1f} & {std_dev:.1f} & {cons_rank} & {deploy_pct:.1f}\\% & {rank_counter} \\\\\n"
            rank_counter += 1
            
        latex_content += """\\hline
\\end{tabular}
\\end{table}

\\textbf{Key Findings:}
\\begin{itemize}
\\item PPO achieves 2nd place performance with superior consistency
\\item RandomBaseline shows highest average reward but with high variance
\\item PPO demonstrates learned strategic behavior vs random actions
\\item Performance gap between best and worst baseline: 423.6 points
\\end{itemize}
"""
        
        return latex_content
        
    def generate_numerical_summary(self):
        """Generate numerical summary for analysis"""
        
        summary = """BASELINE COMPARISON NUMERICAL SUMMARY
====================================

PERFORMANCE RANKINGS:
"""
        
        avg_rewards = self.df.groupby('Agent')['Total_Reward'].mean().sort_values(ascending=False)
        
        for i, (agent, reward) in enumerate(avg_rewards.items(), 1):
            agent_data = self.df[self.df['Agent'] == agent]
            std_dev = agent_data['Reward_StdDev'].mean()
            summary += f"{i}. {agent}: {reward:.2f} (±{std_dev:.2f})\n"
        
        summary += f"""
STATISTICAL ANALYSIS:
- Performance Gap (Best - Worst): {avg_rewards.iloc[0] - avg_rewards.iloc[-1]:.2f} points
- PPO Performance: {avg_rewards['PPO_BestProduction']:.2f} (Rank #2)
- PPO Consistency: {self.df[self.df['Agent'] == 'PPO_BestProduction']['Reward_StdDev'].mean():.2f} std dev
- Random Performance: {avg_rewards['RandomBaseline']:.2f} (Rank #1, High Variance)

ENVIRONMENT-SPECIFIC RESULTS:

Small Network:
"""
        
        small_data = self.df[self.df['Environment'] == 'small_network'].sort_values('Total_Reward', ascending=False)
        for i, (_, row) in enumerate(small_data.iterrows(), 1):
            summary += f"{i}. {row['Agent']}: {row['Total_Reward']:.2f}\n"
        
        summary += "\nMedium Network:\n"
        medium_data = self.df[self.df['Environment'] == 'medium_network'].sort_values('Total_Reward', ascending=False)
        for i, (_, row) in enumerate(medium_data.iterrows(), 1):
            summary += f"{i}. {row['Agent']}: {row['Total_Reward']:.2f}\n"
        
        summary += f"""
ACTION DISTRIBUTION ANALYSIS:
"""
        
        for agent in self.df['Agent'].unique():
            agent_data = self.df[self.df['Agent'] == agent]
            total_deploy = agent_data['Deploy_Actions'].sum()
            total_remove = agent_data['Remove_Actions'].sum()
            total_nothing = agent_data['Nothing_Actions'].sum()
            total = total_deploy + total_remove + total_nothing
            
            summary += f"\n{agent}:\n"
            summary += f"  Deploy: {(total_deploy/total)*100:.1f}% ({total_deploy} actions)\n"
            summary += f"  Remove: {(total_remove/total)*100:.1f}% ({total_remove} actions)\n"
            summary += f"  Nothing: {(total_nothing/total)*100:.1f}% ({total_nothing} actions)\n"
        
        return summary

def main():
    """Generate all baseline comparison visualizations"""
    print("🎨 Starting Baseline Comparison Visualization Generation...")
    
    generator = BaselineVisualizationGenerator()
    generator.generate_all_visualizations()
    
    print("\n✅ VISUALIZATION GENERATION COMPLETE!")
    print("📁 All files saved to: baseline_comparison_visualizations/")
    print("\n📊 Generated Files:")
    print("   • baseline_performance_comparison.png/pdf")
    print("   • performance_by_environment.png/pdf")
    print("   • variance_analysis.png/pdf")
    print("   • action_distribution.png/pdf")
    print("   • comprehensive_comparison.png/pdf")
    print("   • baseline_comparison_table.tex")
    print("   • numerical_summary.txt")

if __name__ == "__main__":
    main()