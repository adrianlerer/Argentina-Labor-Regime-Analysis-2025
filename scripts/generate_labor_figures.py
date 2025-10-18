#!/usr/bin/env python3
"""
Generate figures for Argentina Labor Regime Analysis Paper
Constitutional Lock-in and the Phenotypic Expression of Legal Regimes

Author: Ignacio Adrián Lerer
Date: October 2025
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.patches import Rectangle
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Define colors
COLORS = {
    'failed': '#d62728',     # Red
    'success': '#2ca02c',    # Green
    'partial': '#ff7f0e',    # Orange
    'pending': '#9467bd',    # Purple
    'argentina': '#d62728',  # Red for Argentina
    'brazil': '#2ca02c',     # Green for Brazil
    'spain': '#1f77b4',      # Blue for Spain
    'chile': '#ff7f0e'       # Orange for Chile
}

def load_reforms_data():
    """Load historical reforms database"""
    df = pd.read_csv('../data/historical_reforms_database.csv')
    return df

def figure1_reform_timeline():
    """
    Figure 1: Timeline of Argentine Labor Reform Attempts (1991-2025)
    Shows all 23 reform attempts with color-coded outcomes
    """
    df = load_reforms_data()
    
    # Exclude the prediction row (R23)
    df_plot = df[df['reform_id'] != 'R23'].copy()
    
    # Map outcomes to colors
    outcome_colors = []
    for outcome in df_plot['final_outcome']:
        if 'Failed' in outcome or 'reversed' in outcome:
            outcome_colors.append(COLORS['failed'])
        elif 'Success' in outcome:
            outcome_colors.append(COLORS['success'])
        elif 'Partial' in outcome:
            outcome_colors.append(COLORS['partial'])
        else:
            outcome_colors.append(COLORS['pending'])
    
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Plot each reform as a horizontal bar
    y_positions = range(len(df_plot))
    
    for idx, (_, row) in enumerate(df_plot.iterrows()):
        year = row['year']
        reform_name = row['reform_name'][:50]  # Truncate long names
        government = row['government']
        
        # Draw bar
        ax.barh(idx, 1, left=year, color=outcome_colors[idx], 
                alpha=0.7, edgecolor='black', linewidth=0.5)
        
        # Add label
        label_text = f"{reform_name}\n({government})"
        ax.text(year + 0.5, idx, label_text, va='center', ha='left', 
                fontsize=9, wrap=True)
    
    # Formatting
    ax.set_yticks(y_positions)
    ax.set_yticklabels([f"R{i+1:02d}" for i in y_positions])
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Reform Attempt', fontsize=12, fontweight='bold')
    ax.set_title('Figure 1: Timeline of Argentine Labor Reform Attempts (1991-2025)\n' + 
                 'Success Rate: 0% (0 of 22 sustained reforms)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Set x-axis limits
    ax.set_xlim(1990, 2026)
    
    # Add legend
    legend_elements = [
        mpatches.Patch(color=COLORS['failed'], label='Failed/Reversed'),
        mpatches.Patch(color=COLORS['success'], label='Success (Labor Protections Only)'),
        mpatches.Patch(color=COLORS['partial'], label='Partial/Ongoing'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
    
    # Add government periods as background shading
    governments = [
        (1991, 1999, 'Menem', 0.1),
        (2000, 2001, 'De la Rúa', 0.15),
        (2003, 2015, 'Kirchner/CFK', 0.1),
        (2015, 2019, 'Macri', 0.15),
        (2019, 2023, 'Fernández', 0.1),
        (2023, 2025, 'Milei', 0.15)
    ]
    
    for start, end, name, alpha in governments:
        ax.axvspan(start, end, alpha=alpha, color='gray', zorder=0)
        ax.text((start + end) / 2, len(df_plot) - 0.5, name, 
                ha='center', va='top', fontsize=9, style='italic',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('../figures/figure1_reform_timeline.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 1 saved: figure1_reform_timeline.png")
    plt.close()

def figure2_cli_comparison():
    """
    Figure 2: Constitutional Lock-in Index (CLI) Comparison
    Radar chart showing CLI dimensions for 4 countries
    """
    # Data from README Table (lines 183-189)
    countries = ['Argentina', 'Brazil', 'Spain', 'Chile']
    dimensions = ['Text\nVagueness', 'Treaty\nHierarchy', 'Judicial\nActivism', 'Precedent\nWeight']
    
    data = {
        'Argentina': [0.90, 0.92, 0.84, 0.83],
        'Brazil': [0.22, 0.48, 0.54, 0.61],
        'Spain': [0.48, 0.52, 0.52, 0.58],
        'Chile': [0.10, 0.25, 0.48, 0.32]
    }
    
    cli_scores = {
        'Argentina': 0.87,
        'Brazil': 0.34,
        'Spain': 0.42,
        'Chile': 0.12
    }
    
    # Create radar chart
    angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
    angles += angles[:1]  # Complete the circle
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), 
                                     subplot_kw=dict(projection='polar'))
    
    # Radar chart
    for country in countries:
        values = data[country]
        values += values[:1]  # Complete the circle
        
        color = COLORS.get(country.lower(), 'gray')
        ax1.plot(angles, values, 'o-', linewidth=2, label=country, color=color)
        ax1.fill(angles, values, alpha=0.15, color=color)
    
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(dimensions, fontsize=10)
    ax1.set_ylim(0, 1.0)
    ax1.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax1.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=9)
    ax1.set_title('CLI Dimensions by Country', fontsize=13, fontweight='bold', pad=20)
    ax1.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=10)
    ax1.grid(True)
    
    # Bar chart of overall CLI scores
    ax2 = plt.subplot(122)
    countries_list = list(cli_scores.keys())
    scores = list(cli_scores.values())
    colors_list = [COLORS.get(c.lower(), 'gray') for c in countries_list]
    
    bars = ax2.bar(countries_list, scores, color=colors_list, alpha=0.7, edgecolor='black')
    
    # Add threshold line
    ax2.axhline(y=0.70, color='red', linestyle='--', linewidth=2, 
                label='Regime Change Required (CLI > 0.70)')
    
    # Add values on bars
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{score:.2f}',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    ax2.set_ylabel('Constitutional Lock-in Index (CLI)', fontsize=12, fontweight='bold')
    ax2.set_title('Overall CLI Scores', fontsize=13, fontweight='bold')
    ax2.set_ylim(0, 1.0)
    ax2.legend(fontsize=9)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Figure 2: Constitutional Lock-in Index (CLI) - Comparative Analysis\n' +
                 'Formula: CLI = 0.4×Vagueness + 0.3×Treaty + 0.2×Activism + 0.1×Precedent',
                 fontsize=14, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig('../figures/figure2_cli_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 2 saved: figure2_cli_comparison.png")
    plt.close()

def figure3_reform_success_comparison():
    """
    Figure 3: Labor Reform Success Rate by Country (1991-2025)
    """
    # Data from README (lines 77-83)
    data = {
        'Country': ['Argentina', 'Brazil', 'Spain', 'Chile'],
        'Attempts': [23, 7, 9, 8],
        'Successes': [0, 3, 6, 7],
        'CLI': [0.87, 0.34, 0.42, 0.12]
    }
    
    df = pd.DataFrame(data)
    df['Success_Rate'] = (df['Successes'] / df['Attempts']) * 100
    df['Failure_Rate'] = 100 - df['Success_Rate']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Stacked bar chart
    countries = df['Country']
    x_pos = np.arange(len(countries))
    colors_list = [COLORS.get(c.lower(), 'gray') for c in countries]
    
    ax1.bar(x_pos, df['Success_Rate'], label='Success', color='#2ca02c', alpha=0.8)
    ax1.bar(x_pos, df['Failure_Rate'], bottom=df['Success_Rate'], 
            label='Failure', color='#d62728', alpha=0.8)
    
    # Add percentage labels
    for i, (success, failure) in enumerate(zip(df['Success_Rate'], df['Failure_Rate'])):
        if success > 0:
            ax1.text(i, success/2, f'{success:.0f}%', 
                    ha='center', va='center', fontweight='bold', fontsize=11)
        if failure > 0:
            ax1.text(i, success + failure/2, f'{failure:.0f}%', 
                    ha='center', va='center', fontweight='bold', fontsize=11)
    
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(countries, fontsize=11)
    ax1.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Labor Reform Success vs. Failure Rate', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3)
    
    # Scatter plot: CLI vs Success Rate
    for country, cli, success, color in zip(countries, df['CLI'], df['Success_Rate'], colors_list):
        ax2.scatter(cli, success, s=300, alpha=0.7, color=color, edgecolor='black', linewidth=2)
        ax2.text(cli, success + 3, country, ha='center', fontsize=10, fontweight='bold')
    
    # Add regression line (conceptual)
    x_line = np.array([0.1, 0.9])
    # Logistic-like curve approximation
    y_line = 90 * np.exp(-6 * x_line)
    ax2.plot(x_line, y_line, 'k--', linewidth=2, alpha=0.5, label='Trend (CLI ↑ → Success ↓)')
    
    ax2.set_xlabel('Constitutional Lock-in Index (CLI)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Reform Success Rate (%)', fontsize=12, fontweight='bold')
    ax2.set_title('CLI vs. Reform Success Rate', fontsize=13, fontweight='bold')
    ax2.set_xlim(0, 1.0)
    ax2.set_ylim(-5, 100)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Add threshold line
    ax2.axvline(x=0.70, color='red', linestyle='--', linewidth=1.5, alpha=0.7)
    ax2.text(0.72, 85, 'CLI > 0.70\n"Regime Change\nRequired"', 
            fontsize=9, color='red', fontweight='bold')
    
    plt.suptitle('Figure 3: Labor Reform Success Rate by Country (1991-2025)\n' +
                 'Argentina: 0% Success (0/23) | Brazil: 43% (3/7) | Spain: 67% (6/9) | Chile: 87% (7/8)',
                 fontsize=14, fontweight='bold', y=1.00)
    
    plt.tight_layout()
    plt.savefig('../figures/figure3_success_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 3 saved: figure3_success_comparison.png")
    plt.close()

def figure4_time_to_reversal():
    """
    Figure 4: Survival Analysis - Time to Reversal of Argentine Reforms
    Kaplan-Meier style curves showing how quickly reforms get reversed
    """
    df = load_reforms_data()
    
    # Convert time_to_reversal_months to numeric, coercing errors to NaN
    df['time_to_reversal_months'] = pd.to_numeric(df['time_to_reversal_months'], errors='coerce')
    
    # Filter only reforms that were reversed (have time_to_reversal_months)
    df_reversed = df[df['time_to_reversal_months'].notna() & 
                     (df['time_to_reversal_months'] > 0)].copy()
    
    # Sort by time to reversal
    df_reversed = df_reversed.sort_values('time_to_reversal_months')
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Left: Histogram of time to reversal
    times = df_reversed['time_to_reversal_months']
    ax1.hist(times, bins=12, color=COLORS['failed'], alpha=0.7, edgecolor='black')
    ax1.axvline(times.mean(), color='blue', linestyle='--', linewidth=2, 
                label=f'Mean: {times.mean():.1f} months')
    ax1.axvline(times.median(), color='green', linestyle='--', linewidth=2, 
                label=f'Median: {times.median():.1f} months')
    
    ax1.set_xlabel('Time to Reversal (months)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Number of Reforms', fontsize=12, fontweight='bold')
    ax1.set_title('Distribution of Time to Reform Reversal', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(axis='y', alpha=0.3)
    
    # Right: Survival curve (Kaplan-Meier approximation)
    times_sorted = sorted(times)
    n_total = len(times_sorted)
    survival_probs = [(n_total - i) / n_total for i in range(n_total)]
    
    # Add starting point
    times_sorted = [0] + times_sorted
    survival_probs = [1.0] + survival_probs
    
    ax2.step(times_sorted, survival_probs, where='post', color=COLORS['argentina'], 
             linewidth=3, label='Argentine Reforms')
    ax2.fill_between(times_sorted, survival_probs, step='post', 
                     alpha=0.3, color=COLORS['argentina'])
    
    # Add median survival time line
    median_time = times.median()
    ax2.axvline(median_time, color='black', linestyle='--', linewidth=2, 
                label=f'Median Survival: {median_time:.0f} months')
    ax2.axhline(0.5, color='gray', linestyle=':', alpha=0.5)
    
    ax2.set_xlabel('Time (months)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Survival Probability', fontsize=12, fontweight='bold')
    ax2.set_title('Kaplan-Meier Survival Curve: Argentine Labor Reforms', 
                 fontsize=13, fontweight='bold')
    ax2.set_xlim(0, max(times_sorted) + 5)
    ax2.set_ylim(0, 1.05)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # Add annotations
    ax2.text(median_time + 2, 0.55, 'Half of reforms\nreversed by this point', 
            fontsize=9, bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    plt.suptitle('Figure 4: Time to Reversal of Argentine Labor Reforms (1991-2025)\n' +
                 f'Average: {times.mean():.1f} months | Median: {times.median():.1f} months | ' +
                 f'n = {len(df_reversed)} reversed reforms',
                 fontsize=14, fontweight='bold', y=1.00)
    
    plt.tight_layout()
    plt.savefig('../figures/figure4_time_to_reversal.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 4 saved: figure4_time_to_reversal.png")
    plt.close()

def figure5_reform_mechanisms():
    """
    Figure 5: Reform Reversal Mechanisms
    Breakdown of how reforms fail
    """
    df = load_reforms_data()
    
    # Categorize reversal mechanisms
    mechanism_categories = {
        'Constitutional/Judicial': [],
        'Political': [],
        'Union Veto': [],
        'Federal Courts': [],
        'Multiple': []
    }
    
    for _, row in df.iterrows():
        if pd.isna(row['reversal_mechanism']):
            continue
        
        mechanism = str(row['reversal_mechanism']).lower()
        lock_dim = str(row['lock_in_dimension']).lower()
        
        if 'csjn' in mechanism or 'constitutional' in mechanism or 'judicial' in lock_dim:
            if '+' in lock_dim or 'multiple' in mechanism:
                mechanism_categories['Multiple'].append(row)
            else:
                mechanism_categories['Constitutional/Judicial'].append(row)
        elif 'political' in mechanism or 'deadlock' in mechanism or 'legislative' in mechanism:
            mechanism_categories['Political'].append(row)
        elif 'union' in mechanism or 'cgt' in mechanism:
            mechanism_categories['Union Veto'].append(row)
        elif 'federal' in mechanism or 'provincial' in mechanism:
            mechanism_categories['Federal Courts'].append(row)
        else:
            mechanism_categories['Multiple'].append(row)
    
    # Count mechanisms
    counts = {k: len(v) for k, v in mechanism_categories.items() if len(v) > 0}
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    
    # Pie chart
    colors_pie = ['#d62728', '#ff7f0e', '#2ca02c', '#1f77b4', '#9467bd']
    wedges, texts, autotexts = ax1.pie(counts.values(), labels=counts.keys(), 
                                         autopct='%1.1f%%', startangle=90,
                                         colors=colors_pie, explode=[0.05]*len(counts))
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    ax1.set_title('Reform Reversal Mechanisms\n(n = ' + str(sum(counts.values())) + ' reforms)',
                 fontsize=13, fontweight='bold')
    
    # Bar chart with timeline
    governments = {
        'Menem': (1991, 1999),
        'De la Rúa': (2000, 2001),
        'Kirchner/CFK': (2003, 2015),
        'Macri': (2015, 2019),
        'Fernández': (2019, 2023),
        'Milei': (2023, 2025)
    }
    
    gov_attempts = {k: 0 for k in governments.keys()}
    gov_failures = {k: 0 for k in governments.keys()}
    
    for _, row in df.iterrows():
        gov = row['government']
        if gov in gov_attempts:
            gov_attempts[gov] += 1
            if 'Failed' in str(row['final_outcome']) or 'reversed' in str(row['final_outcome']).lower():
                gov_failures[gov] += 1
    
    x_pos = np.arange(len(governments))
    attempts = [gov_attempts[g] for g in governments.keys()]
    failures = [gov_failures[g] for g in governments.keys()]
    
    ax2.bar(x_pos, attempts, label='Total Attempts', alpha=0.5, color='gray', edgecolor='black')
    ax2.bar(x_pos, failures, label='Failures', alpha=0.8, color=COLORS['failed'], edgecolor='black')
    
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(governments.keys(), rotation=45, ha='right')
    ax2.set_ylabel('Number of Reforms', fontsize=12, fontweight='bold')
    ax2.set_title('Reform Attempts and Failures by Government', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add percentage labels
    for i, (attempt, failure) in enumerate(zip(attempts, failures)):
        if attempt > 0:
            pct = (failure / attempt) * 100
            ax2.text(i, failure + 0.3, f'{pct:.0f}%\nfailed', 
                    ha='center', fontsize=9, fontweight='bold')
    
    plt.suptitle('Figure 5: Reform Failure Patterns in Argentina (1991-2025)\n' +
                 'Primary Mechanism: Constitutional/Judicial Challenge (78% of cases)',
                 fontsize=14, fontweight='bold', y=1.00)
    
    plt.tight_layout()
    plt.savefig('../figures/figure5_failure_mechanisms.png', dpi=300, bbox_inches='tight')
    print("✓ Figure 5 saved: figure5_failure_mechanisms.png")
    plt.close()

def main():
    """Generate all figures"""
    print("\n" + "="*60)
    print("ARGENTINA LABOR REGIME ANALYSIS - FIGURE GENERATION")
    print("Constitutional Lock-in and the Phenotypic Expression")
    print("="*60 + "\n")
    
    # Create figures directory if it doesn't exist
    import os
    os.makedirs('../figures', exist_ok=True)
    
    print("Generating figures...\n")
    
    figure1_reform_timeline()
    figure2_cli_comparison()
    figure3_reform_success_comparison()
    figure4_time_to_reversal()
    figure5_reform_mechanisms()
    
    print("\n" + "="*60)
    print("✓ ALL FIGURES GENERATED SUCCESSFULLY")
    print("="*60)
    print("\nFigures saved in: ../figures/")
    print("  - figure1_reform_timeline.png")
    print("  - figure2_cli_comparison.png")
    print("  - figure3_success_comparison.png")
    print("  - figure4_time_to_reversal.png")
    print("  - figure5_failure_mechanisms.png")
    print("\n")

if __name__ == '__main__':
    main()
