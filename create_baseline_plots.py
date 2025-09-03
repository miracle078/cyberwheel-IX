#!/usr/bin/env python3
"""
Create Baseline Comparison Visualization Plots
Author: Miracle Akanmode
Date: August 2025

This script generates publication-ready plots from baseline comparison results
to be integrated into the comprehensive report.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from pathlib import Path

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_performance_comparison_plot(csv_file: str, output_dir: str = "plots"):
    """Create performance comparison bar plot"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    df = pd.read_csv(csv_file)
    
    # Create figure with subplots for each environment
    environments = df['Environment'].unique()
    fig, axes = plt.subplots(1, len(environments), figsize=(15, 6))
    
    if len(environments) == 1:
        axes = [axes]
    
    for i, env in enumerate(environments):
        env_data = df[df['Environment'] == env]
        
        # Sort by total reward
        env_data = env_data.sort_values('Total_Reward', ascending=False)
        
        bars = axes[i].bar(env_data['Agent'], env_data['Total_Reward'], 
                          color=['#2E8B57', '#FF6B35', '#4ECDC4', '#95A5A6'])
        
        # Add error bars using reward standard deviation
        axes[i].errorbar(env_data['Agent'], env_data['Total_Reward'], 
                        yerr=env_data['Reward_StdDev'], 
                        fmt='none', color='black', capsize=5, capthick=2)
        
        axes[i].set_title(f'{env.replace("_", " ").title()}', fontsize=14, fontweight='bold')
        axes[i].set_xlabel('Agent Type', fontsize=12)
        axes[i].set_ylabel('Total Reward', fontsize=12)
        axes[i].tick_params(axis='x', rotation=45)
        axes[i].grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for j, bar in enumerate(bars):
            height = bar.get_height()
            axes[i].text(bar.get_x() + bar.get_width()/2., height + env_data.iloc[j]['Reward_StdDev'],
                        f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, 'baseline_performance_comparison.png')
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"✅ Performance comparison plot saved: {plot_file}")
    plt.close()
    
    return plot_file


def create_action_distribution_plot(csv_file: str, output_dir: str = "plots"):
    """Create action distribution stacked bar chart"""
    
    df = pd.read_csv(csv_file)
    
    # Prepare data for stacking
    action_cols = ['Deploy_Actions', 'Remove_Actions', 'Nothing_Actions']
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    environments = df['Environment'].unique()
    
    for i, env in enumerate(environments):
        env_data = df[df['Environment'] == env]
        
        # Calculate percentages
        env_data_pct = env_data.copy()
        total_actions = env_data_pct[action_cols].sum(axis=1)
        for col in action_cols:
            env_data_pct[col] = env_data_pct[col] / total_actions * 100
        
        # Create stacked bar chart
        bottom = np.zeros(len(env_data_pct))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        labels = ['Deploy Decoy', 'Remove Decoy', 'No Action']
        
        for j, col in enumerate(action_cols):
            axes[i].bar(env_data_pct['Agent'], env_data_pct[col], 
                       bottom=bottom, color=colors[j], label=labels[j])
            bottom += env_data_pct[col]
        
        axes[i].set_title(f'Action Distribution - {env.replace("_", " ").title()}', 
                         fontsize=14, fontweight='bold')
        axes[i].set_xlabel('Agent Type', fontsize=12)
        axes[i].set_ylabel('Percentage of Actions (%)', fontsize=12)
        axes[i].tick_params(axis='x', rotation=45)
        axes[i].legend()
        axes[i].set_ylim(0, 100)
        
    plt.tight_layout()
    plot_file = os.path.join(output_dir, 'action_distribution_comparison.png')
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"✅ Action distribution plot saved: {plot_file}")
    plt.close()
    
    return plot_file


def create_performance_heatmap(csv_file: str, output_dir: str = "plots"):
    """Create performance heatmap showing agent performance across environments"""
    
    df = pd.read_csv(csv_file)
    
    # Create pivot table
    pivot_data = df.pivot(index='Agent', columns='Environment', values='Total_Reward')
    
    # Create heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot_data, annot=True, fmt='.1f', cmap='RdYlBu_r', 
                cbar_kws={'label': 'Total Reward'}, linewidths=0.5)
    
    plt.title('Agent Performance Heatmap Across Environments', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Environment', fontsize=12)
    plt.ylabel('Agent Type', fontsize=12)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, 'performance_heatmap.png')
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"✅ Performance heatmap saved: {plot_file}")
    plt.close()
    
    return plot_file


def create_statistical_summary_plot(csv_file: str, output_dir: str = "plots"):
    """Create statistical summary with confidence intervals"""
    
    df = pd.read_csv(csv_file)
    
    # Calculate overall performance statistics
    agent_stats = df.groupby('Agent').agg({
        'Total_Reward': ['mean', 'std'],
        'Successful_Actions': 'mean',
        'Deploy_Actions': 'mean'
    }).reset_index()
    
    # Flatten column names
    agent_stats.columns = ['Agent', 'Mean_Reward', 'Reward_Std', 'Avg_Successful', 'Avg_Deploy']
    agent_stats = agent_stats.sort_values('Mean_Reward', ascending=True)
    
    # Create horizontal bar plot with confidence intervals
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Performance with confidence intervals
    bars1 = ax1.barh(agent_stats['Agent'], agent_stats['Mean_Reward'], 
                    xerr=agent_stats['Reward_Std'], capsize=5,
                    color=['#95A5A6', '#4ECDC4', '#FF6B35', '#2E8B57'])
    
    ax1.set_xlabel('Average Total Reward', fontsize=12)
    ax1.set_title('Average Performance with Standard Deviation', fontsize=14, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, mean, std) in enumerate(zip(bars1, agent_stats['Mean_Reward'], agent_stats['Reward_Std'])):
        ax1.text(bar.get_width() + std + 5, bar.get_y() + bar.get_height()/2,
                f'{mean:.1f}±{std:.1f}', va='center', fontweight='bold')
    
    # Success rate comparison
    success_rate = agent_stats['Avg_Successful'] / 1000 * 100  # Convert to percentage
    bars2 = ax2.barh(agent_stats['Agent'], success_rate,
                    color=['#95A5A6', '#4ECDC4', '#FF6B35', '#2E8B57'])
    
    ax2.set_xlabel('Success Rate (%)', fontsize=12)
    ax2.set_title('Action Success Rate', fontsize=14, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3)
    ax2.set_xlim(0, 105)
    
    # Add percentage labels
    for bar, rate in zip(bars2, success_rate):
        ax2.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{rate:.1f}%', va='center', fontweight='bold')
    
    plt.tight_layout()
    plot_file = os.path.join(output_dir, 'statistical_summary.png')
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    print(f"✅ Statistical summary plot saved: {plot_file}")
    plt.close()
    
    return plot_file


def main():
    """Generate all baseline comparison plots"""
    
    print("Creating Baseline Comparison Visualization Plots")
    print("="*50)
    
    # Check if results exist
    csv_file = "baseline_comparison_results/results.csv"
    if not os.path.exists(csv_file):
        print(f"❌ Results file not found: {csv_file}")
        print("Please run baseline comparison first:")
        print("  python run_baseline_comparison.py --quick")
        return False
    
    output_dir = "baseline_plots"
    
    try:
        # Generate all plots
        plot1 = create_performance_comparison_plot(csv_file, output_dir)
        plot2 = create_action_distribution_plot(csv_file, output_dir)
        plot3 = create_performance_heatmap(csv_file, output_dir)
        plot4 = create_statistical_summary_plot(csv_file, output_dir)
        
        print(f"\n🎨 All plots generated successfully!")
        print(f"Output directory: {output_dir}/")
        print(f"Files created:")
        print(f"  📊 {os.path.basename(plot1)}")
        print(f"  📊 {os.path.basename(plot2)}")
        print(f"  📊 {os.path.basename(plot3)}")
        print(f"  📊 {os.path.basename(plot4)}")
        
        print(f"\n✅ READY FOR INTEGRATION:")
        print(f"  • Copy plots to your report figures directory")
        print(f"  • Reference in comprehensive report experimental section")
        print(f"  • Use as evidence of baseline algorithm comparison")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating plots: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)