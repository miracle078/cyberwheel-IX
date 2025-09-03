"""
Statistical Analysis Framework for Cyberwheel Research
=====================================================

This module addresses the critical statistical validation gaps identified in the
comprehensive analysis. It provides proper statistical testing, confidence intervals,
effect size calculations, and multiple comparison corrections.

Key Features:
- Multi-seed experiment validation
- Confidence interval calculation (95%)
- Effect size analysis (Cohen's d)
- ANOVA for experimental conditions
- Multiple comparison correction (Bonferroni)
- Statistical significance testing

Author: Research Team
Date: August 2025
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
import scipy.stats as stats
from scipy.stats import f_oneway, ttest_ind, chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
import warnings
import json
from pathlib import Path

@dataclass
class StatisticalConfig:
    """Configuration for statistical analysis"""
    confidence_level: float = 0.95
    alpha: float = 0.05
    min_sample_size: int = 3
    effect_size_thresholds: Dict[str, float] = None
    
    def __post_init__(self):
        if self.effect_size_thresholds is None:
            self.effect_size_thresholds = {
                'small': 0.2,
                'medium': 0.5, 
                'large': 0.8
            }


class CyberwheelStatisticalAnalyzer:
    """
    Comprehensive statistical analysis for Cyberwheel experimental results
    
    Addresses critical gaps:
    1. Missing confidence intervals
    2. Lack of significance testing
    3. No effect size analysis
    4. Multiple comparison issues
    5. Inadequate sample size validation
    """
    
    def __init__(self, config: StatisticalConfig = None):
        self.config = config or StatisticalConfig()
        self.results = {}
        self.raw_data = {}
        
    def load_experimental_data(self, data_path: str) -> pd.DataFrame:
        """Load experimental data from CSV files"""
        
        try:
            if data_path.endswith('.csv'):
                df = pd.read_csv(data_path)
            else:
                # Try to load from multiple CSV files in directory
                path = Path(data_path)
                csv_files = list(path.glob("*.csv"))
                
                if not csv_files:
                    raise ValueError(f"No CSV files found in {data_path}")
                
                dfs = []
                for csv_file in csv_files:
                    df_temp = pd.read_csv(csv_file)
                    df_temp['source_file'] = csv_file.name
                    dfs.append(df_temp)
                
                df = pd.concat(dfs, ignore_index=True)
            
            self.raw_data['experimental_data'] = df
            return df
            
        except Exception as e:
            raise ValueError(f"Failed to load data from {data_path}: {e}")
    
    def validate_sample_sizes(self, data: pd.DataFrame, group_column: str) -> Dict[str, bool]:
        """Validate sample sizes for statistical power"""
        
        validation = {}
        
        for group in data[group_column].unique():
            group_data = data[data[group_column] == group]
            sample_size = len(group_data)
            
            validation[group] = {
                'sample_size': sample_size,
                'adequate': sample_size >= self.config.min_sample_size,
                'power_adequate': sample_size >= 20  # Rule of thumb for t-tests
            }
        
        return validation
    
    def calculate_confidence_intervals(self, data: np.ndarray, confidence: float = None) -> Tuple[float, float]:
        """Calculate confidence intervals for given data"""
        
        if confidence is None:
            confidence = self.config.confidence_level
        
        if len(data) < 2:
            return (np.nan, np.nan)
        
        mean = np.mean(data)
        sem = stats.sem(data)  # Standard error of mean
        
        # Use t-distribution for small samples
        df = len(data) - 1
        t_critical = stats.t.ppf((1 + confidence) / 2, df)
        margin_error = t_critical * sem
        
        return (mean - margin_error, mean + margin_error)
    
    def calculate_effect_size(self, group1: np.ndarray, group2: np.ndarray) -> Dict[str, float]:
        """Calculate Cohen's d effect size"""
        
        if len(group1) < 2 or len(group2) < 2:
            return {'cohens_d': np.nan, 'interpretation': 'insufficient_data'}
        
        # Cohen's d calculation
        mean1, mean2 = np.mean(group1), np.mean(group2)
        std1, std2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
        n1, n2 = len(group1), len(group2)
        
        # Pooled standard deviation
        pooled_std = np.sqrt(((n1 - 1) * std1**2 + (n2 - 1) * std2**2) / (n1 + n2 - 2))
        
        if pooled_std == 0:
            cohens_d = 0
        else:
            cohens_d = (mean1 - mean2) / pooled_std
        
        # Interpret effect size
        abs_d = abs(cohens_d)
        if abs_d < self.config.effect_size_thresholds['small']:
            interpretation = 'negligible'
        elif abs_d < self.config.effect_size_thresholds['medium']:
            interpretation = 'small'
        elif abs_d < self.config.effect_size_thresholds['large']:
            interpretation = 'medium'
        else:
            interpretation = 'large'
        
        return {
            'cohens_d': cohens_d,
            'interpretation': interpretation,
            'magnitude': abs_d
        }
    
    def perform_anova(self, data: pd.DataFrame, dependent_var: str, 
                     independent_var: str) -> Dict[str, Any]:
        """Perform one-way ANOVA analysis"""
        
        groups = []
        group_names = []
        
        for group_name in data[independent_var].unique():
            group_data = data[data[independent_var] == group_name][dependent_var].dropna()
            if len(group_data) >= 2:  # Need at least 2 observations
                groups.append(group_data.values)
                group_names.append(group_name)
        
        if len(groups) < 2:
            return {
                'error': 'Insufficient groups for ANOVA',
                'groups_found': len(groups)
            }
        
        # Perform ANOVA
        f_statistic, p_value = f_oneway(*groups)
        
        # Calculate effect size (eta-squared)
        total_n = sum(len(group) for group in groups)
        ss_between = sum(len(group) * (np.mean(group) - np.mean(np.concatenate(groups)))**2 
                        for group in groups)
        ss_total = sum((x - np.mean(np.concatenate(groups)))**2 for group in groups for x in group)
        eta_squared = ss_between / ss_total if ss_total > 0 else 0
        
        return {
            'f_statistic': f_statistic,
            'p_value': p_value,
            'significant': p_value < self.config.alpha,
            'eta_squared': eta_squared,
            'groups_tested': group_names,
            'total_observations': total_n,
            'degrees_freedom_between': len(groups) - 1,
            'degrees_freedom_within': total_n - len(groups)
        }
    
    def perform_pairwise_comparisons(self, data: pd.DataFrame, dependent_var: str,
                                   independent_var: str, correction: str = 'bonferroni') -> Dict:
        """Perform pairwise t-tests with multiple comparison correction"""
        
        groups = data[independent_var].unique()
        n_comparisons = len(groups) * (len(groups) - 1) // 2
        
        if correction == 'bonferroni':
            adjusted_alpha = self.config.alpha / n_comparisons
        else:
            adjusted_alpha = self.config.alpha
        
        comparisons = []
        
        for i, group1 in enumerate(groups):
            for j, group2 in enumerate(groups):
                if i < j:  # Avoid duplicate comparisons
                    data1 = data[data[independent_var] == group1][dependent_var].dropna()
                    data2 = data[data[independent_var] == group2][dependent_var].dropna()
                    
                    if len(data1) >= 2 and len(data2) >= 2:
                        # Perform t-test
                        t_stat, p_value = ttest_ind(data1, data2)
                        
                        # Calculate effect size
                        effect_size = self.calculate_effect_size(data1.values, data2.values)
                        
                        # Calculate confidence intervals
                        ci1 = self.calculate_confidence_intervals(data1.values)
                        ci2 = self.calculate_confidence_intervals(data2.values)
                        
                        comparisons.append({
                            'group1': group1,
                            'group2': group2,
                            'group1_mean': np.mean(data1),
                            'group2_mean': np.mean(data2),
                            'group1_ci': ci1,
                            'group2_ci': ci2,
                            't_statistic': t_stat,
                            'p_value': p_value,
                            'p_value_adjusted': min(p_value * n_comparisons, 1.0) if correction == 'bonferroni' else p_value,
                            'significant': p_value < adjusted_alpha,
                            'effect_size': effect_size,
                            'sample_sizes': (len(data1), len(data2))
                        })
        
        return {
            'comparisons': comparisons,
            'correction_method': correction,
            'n_comparisons': n_comparisons,
            'adjusted_alpha': adjusted_alpha,
            'original_alpha': self.config.alpha
        }
    
    def analyze_suli_claims(self, suli_data: pd.DataFrame, baseline_data: pd.DataFrame) -> Dict:
        """
        Analyze specific SULI methodology claims with statistical rigor
        
        Claims to validate:
        1. 90% reduction in training failures
        2. 30% faster convergence
        3. Improved performance balance
        """
        
        analysis = {}
        
        # Claim 1: Training failure reduction
        if 'training_failed' in suli_data.columns and 'training_failed' in baseline_data.columns:
            suli_failures = suli_data['training_failed'].sum()
            suli_total = len(suli_data)
            baseline_failures = baseline_data['training_failed'].sum()
            baseline_total = len(baseline_data)
            
            suli_failure_rate = suli_failures / suli_total if suli_total > 0 else 0
            baseline_failure_rate = baseline_failures / baseline_total if baseline_total > 0 else 0
            
            # Chi-square test for independence
            contingency_table = [
                [suli_failures, suli_total - suli_failures],
                [baseline_failures, baseline_total - baseline_failures]
            ]
            
            chi2, p_value, _, _ = chi2_contingency(contingency_table)
            
            reduction_percent = ((baseline_failure_rate - suli_failure_rate) / baseline_failure_rate * 100 
                               if baseline_failure_rate > 0 else 0)
            
            analysis['failure_rate_analysis'] = {
                'suli_failure_rate': suli_failure_rate,
                'baseline_failure_rate': baseline_failure_rate,
                'reduction_percent': reduction_percent,
                'claim_90_percent_validated': reduction_percent >= 85,  # Allow 5% tolerance
                'chi2_statistic': chi2,
                'p_value': p_value,
                'significant': p_value < self.config.alpha
            }
        
        # Claim 2: Convergence speed improvement
        if 'convergence_episodes' in suli_data.columns and 'convergence_episodes' in baseline_data.columns:
            suli_convergence = suli_data['convergence_episodes'].dropna()
            baseline_convergence = baseline_data['convergence_episodes'].dropna()
            
            if len(suli_convergence) > 0 and len(baseline_convergence) > 0:
                # t-test for convergence speed
                t_stat, p_value = ttest_ind(baseline_convergence, suli_convergence)  # baseline - suli (expect positive)
                
                speed_improvement = ((np.mean(baseline_convergence) - np.mean(suli_convergence)) / 
                                   np.mean(baseline_convergence) * 100)
                
                effect_size = self.calculate_effect_size(baseline_convergence.values, suli_convergence.values)
                
                analysis['convergence_speed_analysis'] = {
                    'suli_mean_episodes': np.mean(suli_convergence),
                    'baseline_mean_episodes': np.mean(baseline_convergence),
                    'improvement_percent': speed_improvement,
                    'claim_30_percent_validated': speed_improvement >= 25,  # Allow 5% tolerance
                    't_statistic': t_stat,
                    'p_value': p_value,
                    'significant': p_value < self.config.alpha,
                    'effect_size': effect_size
                }
        
        # Claim 3: Performance balance
        if 'balance_metric' in suli_data.columns and 'balance_metric' in baseline_data.columns:
            suli_balance = suli_data['balance_metric'].dropna()
            baseline_balance = baseline_data['balance_metric'].dropna()
            
            if len(suli_balance) > 0 and len(baseline_balance) > 0:
                # t-test for balance improvement (lower is better)
                t_stat, p_value = ttest_ind(suli_balance, baseline_balance)
                
                balance_improvement = ((np.mean(baseline_balance) - np.mean(suli_balance)) / 
                                     np.mean(baseline_balance) * 100)
                
                effect_size = self.calculate_effect_size(suli_balance.values, baseline_balance.values)
                
                analysis['balance_analysis'] = {
                    'suli_mean_balance': np.mean(suli_balance),
                    'baseline_mean_balance': np.mean(baseline_balance),
                    'improvement_percent': balance_improvement,
                    't_statistic': t_stat,
                    'p_value': p_value,
                    'significant': p_value < self.config.alpha,
                    'effect_size': effect_size
                }
        
        return analysis
    
    def generate_comprehensive_report(self, data: pd.DataFrame, 
                                    experiment_column: str = 'Experiment',
                                    performance_column: str = 'Final_Return') -> Dict:
        """Generate comprehensive statistical report for all experiments"""
        
        report = {
            'data_summary': {
                'total_experiments': len(data),
                'unique_conditions': data[experiment_column].nunique(),
                'conditions': list(data[experiment_column].unique())
            },
            'sample_size_validation': self.validate_sample_sizes(data, experiment_column),
            'descriptive_statistics': {},
            'inferential_statistics': {},
            'effect_size_analysis': {},
            'confidence_intervals': {},
            'multiple_comparisons': {}
        }
        
        # Descriptive statistics for each experiment
        for experiment in data[experiment_column].unique():
            exp_data = data[data[experiment_column] == experiment][performance_column].dropna()
            
            if len(exp_data) > 0:
                ci_lower, ci_upper = self.calculate_confidence_intervals(exp_data.values)
                
                report['descriptive_statistics'][experiment] = {
                    'n': len(exp_data),
                    'mean': np.mean(exp_data),
                    'std': np.std(exp_data, ddof=1),
                    'min': np.min(exp_data),
                    'max': np.max(exp_data),
                    'median': np.median(exp_data),
                    'q25': np.percentile(exp_data, 25),
                    'q75': np.percentile(exp_data, 75)
                }
                
                report['confidence_intervals'][experiment] = {
                    'lower': ci_lower,
                    'upper': ci_upper,
                    'confidence_level': self.config.confidence_level
                }
        
        # ANOVA analysis
        anova_result = self.perform_anova(data, performance_column, experiment_column)
        report['inferential_statistics']['anova'] = anova_result
        
        # Pairwise comparisons
        pairwise_result = self.perform_pairwise_comparisons(data, performance_column, experiment_column)
        report['multiple_comparisons'] = pairwise_result
        
        # Overall statistical summary
        report['statistical_summary'] = {
            'significant_anova': anova_result.get('significant', False),
            'significant_pairwise_comparisons': sum(
                1 for comp in pairwise_result.get('comparisons', []) if comp['significant']
            ),
            'total_pairwise_comparisons': len(pairwise_result.get('comparisons', [])),
            'multiple_comparison_correction': pairwise_result.get('correction_method'),
            'statistical_power': 'adequate' if all(
                val['power_adequate'] for val in report['sample_size_validation'].values()
            ) else 'inadequate'
        }
        
        return report
    
    def create_statistical_visualizations(self, data: pd.DataFrame, 
                                        experiment_column: str = 'Experiment',
                                        performance_column: str = 'Final_Return',
                                        save_path: str = None) -> None:
        """Create comprehensive statistical visualizations"""
        
        # Set up the plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Cyberwheel Statistical Analysis', fontsize=16, fontweight='bold')
        
        # 1. Box plot with confidence intervals
        ax1 = axes[0, 0]
        sns.boxplot(data=data, x=experiment_column, y=performance_column, ax=ax1)
        ax1.set_title('Performance Distribution by Experiment')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add confidence intervals as error bars
        for i, experiment in enumerate(data[experiment_column].unique()):
            exp_data = data[data[experiment_column] == experiment][performance_column].dropna()
            if len(exp_data) > 1:
                ci_lower, ci_upper = self.calculate_confidence_intervals(exp_data.values)
                mean_val = np.mean(exp_data)
                ax1.errorbar(i, mean_val, yerr=[[mean_val - ci_lower], [ci_upper - mean_val]], 
                           fmt='ro', capsize=5, capthick=2)
        
        # 2. Performance comparison with effect sizes
        ax2 = axes[0, 1]
        means = []
        errors = []
        labels = []
        
        for experiment in data[experiment_column].unique():
            exp_data = data[data[experiment_column] == experiment][performance_column].dropna()
            if len(exp_data) > 0:
                mean_val = np.mean(exp_data)
                ci_lower, ci_upper = self.calculate_confidence_intervals(exp_data.values)
                
                means.append(mean_val)
                errors.append([mean_val - ci_lower, ci_upper - mean_val])
                labels.append(experiment.replace('_', '\n'))
        
        if means:
            x_pos = np.arange(len(labels))
            bars = ax2.bar(x_pos, means, yerr=np.array(errors).T, capsize=5)
            ax2.set_xlabel('Experiments')
            ax2.set_ylabel('Performance (with 95% CI)')
            ax2.set_title('Performance Comparison with Confidence Intervals')
            ax2.set_xticks(x_pos)
            ax2.set_xticklabels(labels, rotation=45, ha='right')
        
        # 3. Statistical significance heatmap
        ax3 = axes[1, 0]
        experiments = data[experiment_column].unique()
        n_exp = len(experiments)
        p_value_matrix = np.ones((n_exp, n_exp))
        
        for i, exp1 in enumerate(experiments):
            for j, exp2 in enumerate(experiments):
                if i != j:
                    data1 = data[data[experiment_column] == exp1][performance_column].dropna()
                    data2 = data[data[experiment_column] == exp2][performance_column].dropna()
                    
                    if len(data1) >= 2 and len(data2) >= 2:
                        _, p_value = ttest_ind(data1, data2)
                        p_value_matrix[i, j] = p_value
        
        im = ax3.imshow(p_value_matrix, cmap='RdYlBu', vmin=0, vmax=0.1)
        ax3.set_xticks(range(n_exp))
        ax3.set_yticks(range(n_exp))
        ax3.set_xticklabels([exp.replace('_', '\n') for exp in experiments], rotation=45, ha='right')
        ax3.set_yticklabels([exp.replace('_', '\n') for exp in experiments])
        ax3.set_title('P-value Matrix (Pairwise T-tests)')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax3)
        cbar.set_label('P-value')
        
        # 4. Effect size visualization
        ax4 = axes[1, 1]
        
        # Calculate effect sizes against first experiment (baseline)
        if len(experiments) > 1:
            baseline_data = data[data[experiment_column] == experiments[0]][performance_column].dropna()
            effect_sizes = []
            effect_labels = []
            
            for exp in experiments[1:]:
                exp_data = data[data[experiment_column] == exp][performance_column].dropna()
                if len(exp_data) >= 2 and len(baseline_data) >= 2:
                    effect_size = self.calculate_effect_size(exp_data.values, baseline_data.values)
                    effect_sizes.append(effect_size['cohens_d'])
                    effect_labels.append(exp.replace('_', '\n'))
            
            if effect_sizes:
                colors = ['red' if abs(es) < 0.2 else 'orange' if abs(es) < 0.5 else 'green' 
                         for es in effect_sizes]
                bars = ax4.barh(range(len(effect_sizes)), effect_sizes, color=colors)
                ax4.set_yticks(range(len(effect_sizes)))
                ax4.set_yticklabels(effect_labels)
                ax4.set_xlabel("Cohen's d (Effect Size)")
                ax4.set_title(f'Effect Sizes vs {experiments[0]}')
                ax4.axvline(x=0, color='black', linestyle='-', alpha=0.3)
                ax4.axvline(x=0.2, color='gray', linestyle='--', alpha=0.5, label='Small')
                ax4.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5, label='Medium')
                ax4.axvline(x=0.8, color='gray', linestyle='--', alpha=0.5, label='Large')
                ax4.axvline(x=-0.2, color='gray', linestyle='--', alpha=0.5)
                ax4.axvline(x=-0.5, color='gray', linestyle='--', alpha=0.5)
                ax4.axvline(x=-0.8, color='gray', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Statistical visualization saved to {save_path}")
        else:
            plt.savefig('/rds/general/user/moa324/home/projects/cyberwheel/Statistical_Analysis_Report.png', 
                       dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def save_report(self, report: Dict, filepath: str) -> None:
        """Save statistical report to JSON file"""
        
        # Convert numpy types to Python types for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {key: convert_numpy(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy(item) for item in obj]
            else:
                return obj
        
        converted_report = convert_numpy(report)
        
        with open(filepath, 'w') as f:
            json.dump(converted_report, f, indent=2)
        
        print(f"Statistical report saved to {filepath}")


def run_comprehensive_statistical_analysis():
    """
    Run comprehensive statistical analysis on Cyberwheel experimental data
    This addresses the critical gaps identified in the research analysis.
    """
    
    print("Starting Comprehensive Statistical Analysis...")
    
    # Initialize analyzer
    analyzer = CyberwheelStatisticalAnalyzer()
    
    # Load experimental data
    try:
        data_path = "/rds/general/user/moa324/home/projects/cyberwheel/COMPREHENSIVE_EXPERIMENTAL_RESULTS.csv"
        data = analyzer.load_experimental_data(data_path)
        print(f"Loaded {len(data)} experimental records")
        
        # Generate comprehensive report
        report = analyzer.generate_comprehensive_report(data)
        
        # Create visualizations
        analyzer.create_statistical_visualizations(data)
        
        # Save report
        report_path = "/rds/general/user/moa324/home/projects/cyberwheel/comprehensive_statistical_report.json"
        analyzer.save_report(report, report_path)
        
        # Print key findings
        print("\n" + "="*60)
        print("KEY STATISTICAL FINDINGS:")
        print("="*60)
        
        if 'anova' in report['inferential_statistics']:
            anova = report['inferential_statistics']['anova']
            print(f"ANOVA Results:")
            print(f"  F-statistic: {anova.get('f_statistic', 'N/A'):.4f}")
            print(f"  P-value: {anova.get('p_value', 'N/A'):.6f}")
            print(f"  Significant: {anova.get('significant', 'N/A')}")
            print(f"  Effect size (η²): {anova.get('eta_squared', 'N/A'):.4f}")
        
        print(f"\nSample Size Validation:")
        for exp, validation in report['sample_size_validation'].items():
            print(f"  {exp}: n={validation['sample_size']}, adequate={validation['adequate']}")
        
        print(f"\nMultiple Comparisons:")
        comparisons = report['multiple_comparisons'].get('comparisons', [])
        significant_comparisons = [c for c in comparisons if c['significant']]
        print(f"  Total comparisons: {len(comparisons)}")
        print(f"  Significant comparisons: {len(significant_comparisons)}")
        print(f"  Correction method: {report['multiple_comparisons'].get('correction_method', 'N/A')}")
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)
        
        return report
        
    except Exception as e:
        print(f"Error in statistical analysis: {e}")
        return None


if __name__ == "__main__":
    # Run the comprehensive analysis
    result = run_comprehensive_statistical_analysis()
    
    if result:
        print("Statistical analysis completed successfully!")
        print("Files generated:")
        print("- comprehensive_statistical_report.json")
        print("- Statistical_Analysis_Report.png")
    else:
        print("Statistical analysis failed. Check data paths and format.")
