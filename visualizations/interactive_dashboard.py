#!/usr/bin/env python3
"""
Interactive Dashboard for Labor Reform Lock-in Visualization

Provides interactive visualizations of:
1. System interrelations network
2. Feedback loop dynamics
3. Historical reform timeline
4. Comparative country analysis
5. Predictive scenarios

Author: Adrian Lerer
Date: 2025-10-17
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

class LaborReformDashboard:
    """
    Interactive dashboard for visualizing labor reform lock-in mechanisms.
    """
    
    def __init__(self):
        """Initialize dashboard with data and network structure."""
        self.setup_network()
        self.load_historical_data()
        self.load_comparative_data()
        
    def setup_network(self):
        """Define system interrelations network."""
        
        # Nodes
        self.nodes = {
            'N1': {'name': 'Constitutional\nLock-in', 'index': 0.87, 'color': '#d32f2f'},
            'N2': {'name': 'Judicial\nActivism', 'index': 2.4/3, 'color': '#c62828'},
            'N3': {'name': 'Ultraactivity\nRatchet', 'index': 0.93, 'color': '#f44336'},
            'N4': {'name': 'Union\nVeto Power', 'index': 0.78, 'color': '#e53935'},
            'N5': {'name': 'Labor Cost\nRigidity', 'index': 0.83, 'color': '#ff5722'},
            'N6': {'name': 'Informality\nRate', 'index': 0.48, 'color': '#ff7043'},
            'N7': {'name': 'Reform\nFailure', 'index': 1.00, 'color': '#b71c1c'}
        }
        
        # Edges (causal pathways)
        self.edges = [
            # Constitutional pathways
            ('N1', 'N2', 0.89, 'Constitutional → Judicial'),
            ('N1', 'N3', 0.76, 'Constitutional → Ultraactivity'),
            ('N1', 'N7', 0.78, 'Constitutional → Reform Failure'),
            
            # Judicial pathways
            ('N2', 'N3', 0.71, 'Judicial → Ultraactivity'),
            ('N2', 'N7', 0.84, 'Judicial → Reform Failure'),
            
            # Ultraactivity pathways
            ('N3', 'N5', 0.91, 'Ultraactivity → Cost Rigidity'),
            ('N3', 'N7', 0.67, 'Ultraactivity → Reform Failure'),
            
            # Union veto pathways
            ('N4', 'N7', 0.81, 'Union → Reform Failure'),
            ('N4', 'N5', 0.52, 'Union → Cost Rigidity'),
            
            # Economic pathways
            ('N5', 'N6', 0.79, 'Cost → Informality'),
            ('N6', 'N4', -0.23, 'Informality → Union (weak negative)'),
            
            # Feedback pathways
            ('N7', 'N2', 0.76, 'Reform Failure → Judicial Strengthening'),
            ('N7', 'N1', 0.73, 'Reform Failure → Constitutional Strengthening'),
            ('N7', 'N4', 0.68, 'Reform Failure → Union Strengthening'),
        ]
        
        # Feedback loops
        self.feedback_loops = {
            'R1': {'name': 'Constitutional-Judicial Amplification', 
                   'type': 'reinforcing', 'gain': 1.7, 
                   'path': ['N1', 'N2', 'N1']},
            'R2': {'name': 'Ultraactivity Peak-Lock', 
                   'type': 'reinforcing', 'gain': 2.3, 
                   'path': ['N3', 'N5', 'N3']},
            'R3': {'name': 'Reform Failure → Stronger Veto', 
                   'type': 'reinforcing', 'gain': 1.5, 
                   'path': ['N7', 'N4', 'N7']},
            'R6': {'name': 'Master Lock-in Loop', 
                   'type': 'reinforcing', 'gain': 2.8, 
                   'path': ['N1', 'N7', 'N1']},
            'B1': {'name': 'Crisis → Reform (weak)', 
                   'type': 'balancing', 'gain': 0.3, 
                   'path': ['N5', 'N7', 'N5']},
        }
        
    def load_historical_data(self):
        """Load historical reform attempts data."""
        
        self.reform_attempts = pd.DataFrame({
            'year': [1991, 1995, 1998, 2000, 2004, 2006, 2009, 2012, 2016, 2017, 2017, 2018, 2020, 2023, 2024, 2025],
            'government': ['Menem', 'Menem', 'Menem', 'De la Rúa', 'Kirchner', 'Provincial', 
                          'CFK', 'CFK', 'Macri', 'Macri', 'Macri', 'Macri', 'Fernández', 
                          'Milei', 'Milei', 'Milei'],
            'reform_name': ['Ley Empleo', 'PyMEs Exemption', 'Flexibilization', 'Reforma Laboral',
                           'Reversion', 'Córdoba', 'ART Re-close', 'ART Limit', 'DNU 267', 
                           'Comprehensive', 'Diluted', 'Emergency', 'COVID-19', 'DNU 70', 
                           'Ley Bases', 'Post-Election'],
            'outcome': ['Failed', 'Failed', 'Failed', 'Failed', 'Anti-reform', 'Failed',
                       'Failed', 'Failed', 'Failed', 'Failed', 'Failed', 'Failed', 'Failed',
                       'Partial', 'Partial', 'Predicted: Failed'],
            'reversal_months': [24, 36, 0, 48, 0, 6, 0, 0, 2, 12, 6, 8, 12, 15, 6, 18],
            'cli_after': [0.72, 0.74, 0.75, 0.77, 0.79, 0.79, 0.80, 0.81, 0.82, 0.83, 0.84, 0.84, 0.85, 0.86, 0.87, 0.88]
        })
        
    def load_comparative_data(self):
        """Load comparative country data."""
        
        self.country_data = pd.DataFrame({
            'country': ['Argentina', 'Brazil', 'Spain', 'Chile'],
            'cli': [0.87, 0.34, 0.42, 0.12],
            'jam': [2.4, 1.2, 1.3, 1.0],
            'uvi': [0.78, 0.31, 0.38, 0.15],
            'cls': [0.85, 0.32, 0.39, 0.14],
            'reform_success_rate': [0.0, 0.43, 0.67, 0.87],
            'informality': [48.1, 38.2, 23.4, 19.7],
            'labor_cost_rigidity': [83, 42, 38, 21]
        })
        
    def plot_network(self, output_file='network_diagram.png'):
        """Plot system interrelations network."""
        
        fig, ax = plt.subplots(figsize=(16, 12))
        
        # Create networkx graph
        G = nx.DiGraph()
        
        # Add nodes
        for node_id, node_data in self.nodes.items():
            G.add_node(node_id, **node_data)
        
        # Add edges
        for source, target, weight, label in self.edges:
            G.add_edge(source, target, weight=weight, label=label)
        
        # Layout
        pos = {
            'N1': (0.5, 0.9),   # Constitutional (top center)
            'N2': (0.3, 0.7),   # Judicial (top left)
            'N3': (0.7, 0.7),   # Ultraactivity (top right)
            'N4': (0.2, 0.4),   # Union (left)
            'N5': (0.5, 0.4),   # Cost (center)
            'N6': (0.8, 0.4),   # Informality (right)
            'N7': (0.5, 0.1),   # Reform Failure (bottom)
        }
        
        # Draw nodes
        for node_id, (x, y) in pos.items():
            node_data = self.nodes[node_id]
            index = node_data['index']
            color = node_data['color']
            size = 3000 + 2000 * index
            
            # Node circle
            circle = plt.Circle((x, y), 0.08, color=color, alpha=0.7, zorder=10)
            ax.add_patch(circle)
            
            # Node label
            ax.text(x, y, node_data['name'], ha='center', va='center', 
                   fontsize=11, fontweight='bold', color='white', zorder=11)
            
            # Index value
            ax.text(x, y - 0.11, f'Index: {index:.2f}', ha='center', va='top',
                   fontsize=9, color='#333', zorder=11)
        
        # Draw edges
        for source, target, weight, label in self.edges:
            x1, y1 = pos[source]
            x2, y2 = pos[target]
            
            # Edge color based on weight
            if weight > 0:
                edge_color = '#d32f2f' if weight > 0.75 else '#ff5722'
                alpha = 0.3 + 0.5 * abs(weight)
            else:
                edge_color = '#2196f3'
                alpha = 0.3
            
            # Edge width based on weight
            linewidth = 1 + 4 * abs(weight)
            
            # Arrow
            arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                   arrowstyle='->', mutation_scale=20,
                                   linewidth=linewidth, color=edge_color,
                                   alpha=alpha, zorder=5,
                                   connectionstyle="arc3,rad=0.1")
            ax.add_patch(arrow)
            
            # Weight label
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x, mid_y, f'{weight:.2f}', ha='center', va='center',
                   fontsize=8, bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                                        edgecolor=edge_color, alpha=0.8), zorder=6)
        
        # Title and legend
        ax.set_title('Labor Reform Lock-in: System Interrelations Network\n' +
                    'Node Size = Lock-in Index | Edge Width = Pathway Strength | Red = Reinforcing',
                    fontsize=16, fontweight='bold', pad=20)
        
        # Legend
        legend_elements = [
            Line2D([0], [0], color='#d32f2f', linewidth=3, label='Strong Pathway (β > 0.75)'),
            Line2D([0], [0], color='#ff5722', linewidth=2, label='Moderate Pathway (β < 0.75)'),
            Line2D([0], [0], color='#2196f3', linewidth=2, label='Negative Pathway (weak)'),
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
        
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Network diagram saved to: {output_file}")
        plt.show()
        
    def plot_feedback_loops(self, output_file='feedback_loops.png'):
        """Plot feedback loop dynamics."""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Loop gains
        loop_names = list(self.feedback_loops.keys())
        loop_gains = [self.feedback_loops[l]['gain'] for l in loop_names]
        loop_types = [self.feedback_loops[l]['type'] for l in loop_names]
        
        colors = ['#d32f2f' if t == 'reinforcing' else '#2196f3' for t in loop_types]
        
        bars = ax1.barh(loop_names, loop_gains, color=colors, alpha=0.7)
        ax1.axvline(x=1.0, color='black', linestyle='--', linewidth=2, label='Stability Threshold')
        ax1.set_xlabel('Loop Gain', fontsize=12, fontweight='bold')
        ax1.set_title('Feedback Loop Strength\n(Gain > 1 = Unstable/Explosive)', 
                     fontsize=13, fontweight='bold')
        ax1.legend()
        ax1.grid(axis='x', alpha=0.3)
        
        # Add gain values
        for i, (bar, gain) in enumerate(zip(bars, loop_gains)):
            ax1.text(gain + 0.05, i, f'{gain:.1f}', va='center', fontweight='bold')
        
        # Net loop gain over time
        years = np.arange(1990, 2051)
        reinforcing_gain = np.array([sum([self.feedback_loops[l]['gain'] 
                                         for l in loop_names if loop_types[loop_names.index(l)] == 'reinforcing'])
                                    for _ in years])
        balancing_gain = np.array([sum([self.feedback_loops[l]['gain'] 
                                       for l in loop_names if loop_types[loop_names.index(l)] == 'balancing'])
                                  for _ in years])
        net_gain = reinforcing_gain - balancing_gain
        
        ax2.plot(years, reinforcing_gain, 'r-', linewidth=2, label='Reinforcing Loops (Total)', alpha=0.7)
        ax2.plot(years, balancing_gain, 'b-', linewidth=2, label='Balancing Loops (Total)', alpha=0.7)
        ax2.plot(years, net_gain, 'k-', linewidth=3, label='Net Loop Gain', alpha=0.9)
        ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        ax2.fill_between(years, 0, net_gain, alpha=0.2, color='red')
        
        ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Loop Gain', fontsize=12, fontweight='bold')
        ax2.set_title('Net Feedback Loop Dynamics\n(Net > 0 = System Unstable Toward Lock-in)', 
                     fontsize=13, fontweight='bold')
        ax2.legend(loc='upper left')
        ax2.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Feedback loops plot saved to: {output_file}")
        plt.show()
        
    def plot_historical_timeline(self, output_file='historical_timeline.png'):
        """Plot historical reform attempts timeline."""
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), 
                                       gridspec_kw={'height_ratios': [2, 1]})
        
        # Timeline
        years = self.reform_attempts['year'].values
        cli_values = self.reform_attempts['cli_after'].values
        outcomes = self.reform_attempts['outcome'].values
        
        # Color code by outcome
        colors = ['red' if 'Failed' in o else 'orange' if 'Partial' in o else 'green' 
                 for o in outcomes]
        
        # Plot reform attempts
        for i, (year, cli, outcome, color) in enumerate(zip(years, cli_values, outcomes, colors)):
            ax1.scatter(year, cli, s=300, color=color, alpha=0.7, edgecolor='black', 
                       linewidth=2, zorder=10)
            ax1.text(year, cli + 0.015, outcome.split(':')[0], ha='center', va='bottom',
                    fontsize=8, fontweight='bold')
        
        # Trend line
        ax1.plot(years, cli_values, 'k--', linewidth=2, alpha=0.5, label='CLI Trajectory')
        
        # Shaded regions
        ax1.axhspan(0.7, 0.85, alpha=0.1, color='orange', label='Hard Reform Zone (0.7-0.85)')
        ax1.axhspan(0.85, 1.0, alpha=0.1, color='red', label='Impossible Zone (>0.85)')
        
        ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Constitutional Lock-in Index (CLI)', fontsize=12, fontweight='bold')
        ax1.set_title('Historical Labor Reform Attempts & Lock-in Evolution (1991-2025)', 
                     fontsize=14, fontweight='bold')
        ax1.legend(loc='upper left')
        ax1.grid(alpha=0.3)
        ax1.set_xlim(1989, 2027)
        ax1.set_ylim(0.65, 0.92)
        
        # Success rate over time
        window = 5
        success_rate = []
        for i in range(len(self.reform_attempts) - window + 1):
            window_data = self.reform_attempts.iloc[i:i+window]
            failures = sum('Failed' in o for o in window_data['outcome'])
            rate = (window - failures) / window
            success_rate.append(rate)
        
        mid_years = [self.reform_attempts.iloc[i + window // 2]['year'] 
                    for i in range(len(success_rate))]
        
        ax2.plot(mid_years, success_rate, 'b-', linewidth=3, marker='o', markersize=8)
        ax2.fill_between(mid_years, 0, success_rate, alpha=0.2, color='blue')
        ax2.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='50% Success')
        ax2.axhline(y=0.0, color='red', linestyle='--', alpha=0.7, label='0% Success (Reality)')
        
        ax2.set_xlabel('Year (5-year rolling window)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Reform Success Rate', fontsize=12, fontweight='bold')
        ax2.set_title('Rolling Reform Success Rate\n(Learning Effect: Each Failure Reduces Future Attempts)', 
                     fontsize=13, fontweight='bold')
        ax2.legend()
        ax2.grid(alpha=0.3)
        ax2.set_ylim(-0.05, 0.6)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Historical timeline saved to: {output_file}")
        plt.show()
        
    def plot_comparative_analysis(self, output_file='comparative_analysis.png'):
        """Plot comparative country analysis."""
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Constitutional Lock-in Index (CLI)',
                          'Combined Lock-in Score (CLS)',
                          'Reform Success Rate',
                          'Informality Rate'),
            specs=[[{'type': 'bar'}, {'type': 'bar'}],
                   [{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        countries = self.country_data['country'].values
        colors_map = {'Argentina': '#d32f2f', 'Brazil': '#4caf50', 
                     'Spain': '#ff9800', 'Chile': '#2196f3'}
        colors = [colors_map[c] for c in countries]
        
        # CLI
        fig.add_trace(go.Bar(x=countries, y=self.country_data['cli'], 
                            marker_color=colors, name='CLI',
                            text=self.country_data['cli'].round(2),
                            textposition='outside'),
                     row=1, col=1)
        fig.add_hline(y=0.68, line_dash="dash", line_color="red", 
                     annotation_text="Reformable Threshold", row=1, col=1)
        
        # CLS
        fig.add_trace(go.Bar(x=countries, y=self.country_data['cls'], 
                            marker_color=colors, name='CLS',
                            text=self.country_data['cls'].round(2),
                            textposition='outside'),
                     row=1, col=2)
        
        # Reform Success Rate
        fig.add_trace(go.Bar(x=countries, y=self.country_data['reform_success_rate'] * 100, 
                            marker_color=colors, name='Success %',
                            text=[f"{v:.0f}%" for v in self.country_data['reform_success_rate'] * 100],
                            textposition='outside'),
                     row=2, col=1)
        
        # Informality
        fig.add_trace(go.Bar(x=countries, y=self.country_data['informality'], 
                            marker_color=colors, name='Informality %',
                            text=[f"{v:.1f}%" for v in self.country_data['informality']],
                            textposition='outside'),
                     row=2, col=2)
        
        fig.update_xaxes(title_text="Country", row=2, col=1)
        fig.update_xaxes(title_text="Country", row=2, col=2)
        fig.update_yaxes(title_text="CLI Index", row=1, col=1)
        fig.update_yaxes(title_text="CLS Index", row=1, col=2)
        fig.update_yaxes(title_text="Success Rate (%)", row=2, col=1)
        fig.update_yaxes(title_text="Informality Rate (%)", row=2, col=2)
        
        fig.update_layout(height=800, showlegend=False,
                         title_text="Comparative Country Analysis: Lock-in Indices & Outcomes",
                         title_font_size=18)
        
        fig.write_html(output_file.replace('.png', '.html'))
        print(f"✓ Comparative analysis saved to: {output_file.replace('.png', '.html')}")
        fig.show()
        
    def generate_full_dashboard(self, output_dir='dashboard_outputs'):
        """Generate all dashboard visualizations."""
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print("\n" + "="*80)
        print("GENERATING LABOR REFORM LOCK-IN DASHBOARD")
        print("="*80 + "\n")
        
        # Network diagram
        print("1. Generating system interrelations network...")
        self.plot_network(f'{output_dir}/network_diagram.png')
        
        # Feedback loops
        print("\n2. Generating feedback loop analysis...")
        self.plot_feedback_loops(f'{output_dir}/feedback_loops.png')
        
        # Historical timeline
        print("\n3. Generating historical reform timeline...")
        self.plot_historical_timeline(f'{output_dir}/historical_timeline.png')
        
        # Comparative analysis
        print("\n4. Generating comparative country analysis...")
        self.plot_comparative_analysis(f'{output_dir}/comparative_analysis.png')
        
        print("\n" + "="*80)
        print("DASHBOARD GENERATION COMPLETE")
        print("="*80)
        print(f"\nAll visualizations saved to: {output_dir}/")
        print("\nFiles generated:")
        print(f"  • network_diagram.png")
        print(f"  • feedback_loops.png")
        print(f"  • historical_timeline.png")
        print(f"  • comparative_analysis.html (interactive)")
        print()


def main():
    """Run dashboard generation."""
    
    dashboard = LaborReformDashboard()
    dashboard.generate_full_dashboard()


if __name__ == "__main__":
    main()
