import os
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Patch

def create_visualizations(df, G, communities, stats, valid_cols):
    os.makedirs("progress_figs", exist_ok=True)

    # Data coverage
    fig, ax = plt.subplots(figsize=(10, 6))
    ca_counts = df.groupby('ca_name').size()
    colors = plt.cm.Set3(range(len(ca_counts)))
    bars = ax.bar(ca_counts.index, ca_counts.values, color=colors)
    ax.set_ylabel('Number of Block Groups', fontsize=12)
    ax.set_title('Block Groups by Community Area', fontsize=14, fontweight='bold')
    ax.set_xlabel('Community Area', fontsize=12)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')

    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.savefig('progress_figs/01_data_coverage.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    01_data_coverage.png")

    # Additional variables
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Variables by Community Area', fontsize=14, fontweight='bold')

    new_vars = [
        ('foreign_born_share', 'Foreign-Born Share'),
        ('vacancy_rate', 'Vacancy Rate'),
        ('homeownership_rate', 'Homeownership Rate'),
        ('walk_to_work_share', 'Walk to Work Share')
    ]

    for idx, (var, title) in enumerate(new_vars):
        ax = axes[idx//2, idx%2]
        if var in df.columns:
            for ca_name in df['ca_name'].unique():
                ca_data = df[df['ca_name'] == ca_name][var].dropna()
                if len(ca_data) > 0:
                    ax.hist(ca_data, alpha=0.5, label=ca_name, bins=15)
        ax.set_title(title, fontweight='bold')
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.savefig('progress_figs/02_new_variables.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    02_new_variables.png")

    # Network structure
    fig, ax = plt.subplots(figsize=(10, 8))

    ca_names = sorted(df['ca_name'].unique())
    ca_colors = {ca: plt.cm.Set2(i) for i, ca in enumerate(ca_names)}

    node_colors = [ca_colors[G.nodes[node]['ca_name']] for node in G.nodes()]

    pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)

    nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                          node_size=50, alpha=0.7, ax=ax)

    cross_edges = [(u,v) for u,v in G.edges()
                   if G.nodes[u]['ca_id'] != G.nodes[v]['ca_id']]
    nx.draw_networkx_edges(G, pos, edgelist=cross_edges,
                          edge_color='red', alpha=0.2, width=0.5, ax=ax)

    within_edges = [(u,v) for u,v in G.edges()
                    if G.nodes[u]['ca_id'] == G.nodes[v]['ca_id']]
    nx.draw_networkx_edges(G, pos, edgelist=within_edges,
                          edge_color='gray', alpha=0.1, width=0.3, ax=ax)

    legend_elements = [Patch(facecolor=ca_colors[ca], label=ca)
                      for ca in ca_names]
    legend_elements.append(Patch(facecolor='red', alpha=0.5, label='Cross-CA connections'))
    ax.legend(handles=legend_elements, loc='upper right')

    ax.set_title(f'Network Structure - {stats["cross_ca_percentage"]:.1f}% cross-CA edges',
                fontsize=14, fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('progress_figs/03_network_structure.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    03_network_structure.png")

    # Community detection
    fig, ax = plt.subplots(figsize=(10, 8))

    node_to_comm = {}
    for i, comm in enumerate(communities):
        for node in comm:
            node_to_comm[node] = i

    comm_colors = [plt.cm.tab10(node_to_comm[node] % 10) for node in G.nodes()]

    nx.draw_networkx_nodes(G, pos, node_color=comm_colors,
                          node_size=50, alpha=0.8, ax=ax)
    nx.draw_networkx_edges(G, pos, alpha=0.1, width=0.5, ax=ax)

    ax.set_title(f'Communities (Q = {stats["modularity"]:.3f})',
                fontsize=14, fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('progress_figs/04_communities.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    04_communities.png")

    # Summary stats
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')

    summary_text = f"""
Network Statistics
==================

Data: {len(df['ca_id'].unique())} CAs, {stats['total_nodes']} block groups
Network: {stats['total_edges']} edges (k=10)
Within-CA: {stats['within_ca_edges']}
Cross-CA: {stats['cross_ca_edges']} ({stats['cross_ca_percentage']:.1f}%)
Density: {stats['density']:.4f}

Communities: {stats['n_communities']} detected
Modularity: {stats['modularity']:.3f}
Features: {len(valid_cols)} variables
    """

    ax.text(0.1, 0.95, summary_text, transform=ax.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))

    plt.tight_layout()
    plt.savefig('progress_figs/05_summary_stats.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    05_summary_stats.png")
