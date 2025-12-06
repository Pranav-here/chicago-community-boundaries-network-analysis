# final_project_progress.py
# CS 579 Final Project - Progress Demo

import os
import time
import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns

# Configuration
STATE = "17"
COUNTY = "031"
API_KEY = os.getenv("CENSUS_API_KEY", "")

# Community areas to analyze
CAS = {
    "15": "Portage Park",
    "25": "Austin",
    "53": "West Pullman",
    "62": "West Elsdon"
}

ACS2022 = "https://api.census.gov/data/2022/acs/acs5"

# Census variables
VARIABLES = {
    # Demographics
    "B01003_001E": "total_pop",
    "B02001_002E": "white_alone",
    "B02001_003E": "black_alone",
    "B03003_003E": "hispanic",
    "B15003_001E": "edu_total",
    "B15003_022E": "ba_degree",
    "B15003_023E": "masters",
    "B15003_024E": "professional",
    "B15003_025E": "doctorate",
    "B25003_001E": "tenure_total",
    "B25003_003E": "renter_occupied",
    "B19013_001E": "median_hh_income",
    "B25064_001E": "median_gross_rent",
    "B05002_013E": "foreign_born",
    "B25002_001E": "housing_units_total",
    "B25002_003E": "vacant_units",
    "B25003_002E": "owner_occupied",
    "B08301_001E": "commute_total",
    "B08301_019E": "walk_to_work",
}

def get_ca_tracts(ca_id):
    """Get tracts for each community area"""
    ca_tracts = {
        "15": ["800100", "800200", "800300", "800400", "800500"],
        "25": ["250100", "250200", "250300", "250400", "250500"],
        "53": ["530100", "530200", "530300"],
        "62": ["620100", "620200", "620300", "620400"]
    }
    return ca_tracts.get(ca_id, [])

def census_api_get(url, params):
    """Fetch data from Census API with retry logic"""
    if API_KEY:
        params["key"] = API_KEY
    for _ in range(3):
        try:
            resp = requests.get(url, params=params, timeout=90)
            if resp.status_code == 200:
                return resp.json()
            time.sleep(1.0)
        except:
            time.sleep(1.0)
    return None

def fetch_ca_blockgroups(ca_id, tract_list):
    """Fetch ACS data for block groups in a CA"""
    var_list = list(VARIABLES.keys())
    records = []
    
    for tract in tract_list:
        params = {
            "get": ",".join(var_list + ["NAME"]),
            "for": "block group:*",
            "in": f"state:{STATE} county:{COUNTY} tract:{tract}"
        }
        data = census_api_get(ACS2022, params)
        if not data:
            continue
            
        header, *rows = data
        for row in rows:
            record = dict(zip(header, row))
            record["ca_id"] = ca_id
            record["ca_name"] = CAS[ca_id]
            record["geoid_bg"] = f"{record['state']}{record['county']}{record['tract']}{record['block group']}"
            records.append(record)
        time.sleep(0.3)
    
    return pd.DataFrame(records)

def compute_features(df):
    """Compute derived features"""
    # Convert to numeric
    for var in VARIABLES.keys():
        df[var] = pd.to_numeric(df[var], errors='coerce')
    
    # Replace Census suppression codes with NaN
    df = df.replace(-666666666, np.nan)
    df = df.replace(-999999999, np.nan)

    # Demographics
    df['share_white'] = df['B02001_002E'] / df['B01003_001E']
    df['share_black'] = df['B02001_003E'] / df['B01003_001E']
    df['share_hispanic'] = df['B03003_003E'] / df['B01003_001E']
    
    # Education
    ba_plus_cols = ['B15003_022E', 'B15003_023E', 'B15003_024E', 'B15003_025E']
    df['ba_plus_total'] = df[ba_plus_cols].sum(axis=1)
    df['share_ba_plus'] = df['ba_plus_total'] / df['B15003_001E']
    
    # Housing
    df['renter_share'] = df['B25003_003E'] / df['B25003_001E']
    df['med_income'] = df['B19013_001E']
    df['med_rent'] = df['B25064_001E']
    df['foreign_born_share'] = df['B05002_013E'] / df['B01003_001E']
    df['vacancy_rate'] = df['B25002_003E'] / df['B25002_001E']
    df['homeownership_rate'] = df['B25003_002E'] / df['B25003_001E']
    df['walk_to_work_share'] = df['B08301_019E'] / df['B08301_001E']
    
    return df

def build_cross_ca_network(df, feature_cols, k=10):
    """Build similarity network across multiple CAs"""
    # Prepare feature matrix
    X = df[feature_cols].copy()
    
    # Check which columns have any valid data
    valid_cols = []
    for col in feature_cols:
        if X[col].notna().sum() > 0:  # Has at least some valid values
            valid_cols.append(col)
        else:
            print(f"  Warning: Dropping column '{col}' (all NaN)")
    
    # Use only valid columns
    X = X[valid_cols].copy()
    
    # Impute missing values with column median (proper pandas way)
    for col in valid_cols:
        median_val = X[col].median()
        if pd.isna(median_val):
            median_val = 0.0  # If all values are NaN, use 0
        X[col] = X[col].fillna(median_val)
    
    # Convert to numpy and check for remaining NaNs
    X_array = X.to_numpy()
    
    # Replace any remaining NaNs with 0 (safety)
    X_array = np.nan_to_num(X_array, nan=0.0, posinf=0.0, neginf=0.0)
    
    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_array)
    
    # Replace any NaNs that might have been created during scaling
    X_scaled = np.nan_to_num(X_scaled, nan=0.0, posinf=0.0, neginf=0.0)
    
    # Compute cosine similarity
    sim_matrix = cosine_similarity(X_scaled)
    
    # Build k-NN graph
    G = nx.Graph()
    n_nodes = len(df)
    
    for i in range(n_nodes):
        G.add_node(i, 
                  geoid=df.iloc[i]['geoid_bg'],
                  ca_id=df.iloc[i]['ca_id'],
                  ca_name=df.iloc[i]['ca_name'])
    
    # Add edges (k nearest neighbors)
    for i in range(n_nodes):
        # Get k nearest neighbors (excluding self)
        neighbors = np.argsort(sim_matrix[i])[::-1][1:k+1]
        for j in neighbors:
            if i < j:  # Avoid duplicates
                G.add_edge(i, j, weight=float(sim_matrix[i,j]))
    
    return G, sim_matrix, valid_cols

def analyze_network(G, df):
    """Analyze cross-CA connectivity"""
    stats = {
        'total_nodes': G.number_of_nodes(),
        'total_edges': G.number_of_edges(),
        'density': nx.density(G)
    }
    
    # Count within-CA vs cross-CA edges
    within_ca = 0
    cross_ca = 0
    
    for u, v in G.edges():
        ca_u = G.nodes[u]['ca_id']
        ca_v = G.nodes[v]['ca_id']
        if ca_u == ca_v:
            within_ca += 1
        else:
            cross_ca += 1
    
    stats['within_ca_edges'] = within_ca
    stats['cross_ca_edges'] = cross_ca
    stats['cross_ca_percentage'] = 100 * cross_ca / max(within_ca + cross_ca, 1)
    
    # Community detection
    communities = list(nx.community.greedy_modularity_communities(G, weight='weight'))
    stats['n_communities'] = len(communities)
    stats['modularity'] = nx.community.modularity(G, communities, weight='weight')
    
    return stats, communities

def create_progress_visualizations(df, G, communities, stats, valid_cols):
    """Create visualizations"""
    os.makedirs("progress_figs", exist_ok=True)
    
    # 1. Data Coverage Map
    fig, ax = plt.subplots(figsize=(10, 6))
    ca_counts = df.groupby('ca_name').size()
    colors = plt.cm.Set3(range(len(ca_counts)))
    bars = ax.bar(ca_counts.index, ca_counts.values, color=colors)
    ax.set_ylabel('Number of Block Groups', fontsize=12)
    ax.set_title('Integrated Dataset: Block Groups by Community Area', fontsize=14, fontweight='bold')
    ax.set_xlabel('Community Area', fontsize=12)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom')
    
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.savefig('progress_figs/01_data_coverage.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    [DONE] 01_data_coverage.png")
    
    # 2. Additional Variables
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Additional Variables Distribution by Community Area',
                 fontsize=14, fontweight='bold')
    
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
    print("    [DONE] 02_new_variables.png")
    
    # 3. Cross-CA Network Structure
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
    
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=ca_colors[ca], label=ca) 
                      for ca in ca_names]
    legend_elements.append(Patch(facecolor='red', alpha=0.5, label='Cross-CA connections'))
    ax.legend(handles=legend_elements, loc='upper right')
    
    ax.set_title(f'Cross-City Network Structure\n{stats["cross_ca_percentage"]:.1f}% of edges connect different CAs', 
                fontsize=14, fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('progress_figs/03_network_structure.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    [DONE] 03_network_structure.png")
    
    # 4. Community Detection Results
    fig, ax = plt.subplots(figsize=(10, 8))
    
    node_to_comm = {}
    for i, comm in enumerate(communities):
        for node in comm:
            node_to_comm[node] = i
    
    comm_colors = [plt.cm.tab10(node_to_comm[node] % 10) for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, node_color=comm_colors, 
                          node_size=50, alpha=0.8, ax=ax)
    nx.draw_networkx_edges(G, pos, alpha=0.1, width=0.5, ax=ax)
    
    ax.set_title(f'Detected Communities (Modularity Q = {stats["modularity"]:.3f})\n{stats["n_communities"]} data-driven neighborhoods found', 
                fontsize=14, fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('progress_figs/04_communities.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    [DONE] 04_communities.png")
    
    # 5. Network Statistics Summary
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    summary_text = f"""
    Cross-City Network Analysis Summary
    ====================================

    Data:
    - Community Areas: {len(df['ca_id'].unique())}
    - Block groups: {stats['total_nodes']}
    - Regions: Northwest, Southwest, West Side, Far South

    Network:
    - Edges (k=10): {stats['total_edges']}
    - Within-CA: {stats['within_ca_edges']}
    - Cross-CA: {stats['cross_ca_edges']} ({stats['cross_ca_percentage']:.1f}%)
    - Density: {stats['density']:.4f}

    Communities:
    - Algorithm: Greedy Modularity
    - Detected: {stats['n_communities']}
    - Modularity: {stats['modularity']:.3f}

    Features:
    - Variables: {len(valid_cols)}
    - Includes: demographics, education, housing,
      foreign-born share, vacancy, homeownership, commute
    """
    
    ax.text(0.1, 0.95, summary_text, transform=ax.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('progress_figs/05_summary_stats.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("    [DONE] 05_summary_stats.png")

def main():
    print("\nCS 579 Final Project - Progress Demo")
    print("Cross-city network analysis\n")
    
    # Collect data from multiple CAs
    print("\n[1/5] Fetching block group data from multiple CAs...")
    all_dfs = []
    
    for ca_id, ca_name in CAS.items():
        print(f"  Processing CA {ca_id} ({ca_name})...")
        tracts = get_ca_tracts(ca_id)
        if tracts:
            df_ca = fetch_ca_blockgroups(ca_id, tracts)
            if not df_ca.empty:
                all_dfs.append(df_ca)
                print(f"    [OK] Got {len(df_ca)} block groups")
    
    if not all_dfs:
        print("\nNo data fetched. Check Census API key and tract numbers.")
        return
    
    df_combined = pd.concat(all_dfs, ignore_index=True)
    print(f"\n  Total block groups collected: {len(df_combined)}")
    print(f"  CAs represented: {list(df_combined['ca_name'].unique())}")
    
    # Compute features
    print("\n[2/5] Computing features (including NEW variables)...")
    df_combined = compute_features(df_combined)
    
    # Define feature set
    feature_cols = [
        'share_white', 'share_black', 'share_hispanic',
        'share_ba_plus', 'renter_share', 'med_income', 'med_rent',
        'foreign_born_share', 'vacancy_rate', 'homeownership_rate', 'walk_to_work_share'
    ]
    
    print(f"  Features: {len(feature_cols)} variables")
    
    # Build network
    print("\n[3/5] Building cross-CA similarity network...")
    G, sim_matrix, valid_cols = build_cross_ca_network(df_combined, feature_cols, k=10)
    print(f"  Network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"  Valid features used: {len(valid_cols)}")
    
    # Analyze
    print("\n[4/5] Analyzing network structure and detecting communities...")
    stats, communities = analyze_network(G, df_combined)
    
    print(f"\n  Network Statistics:")
    print(f"    - Within-CA edges: {stats['within_ca_edges']}")
    print(f"    - Cross-CA edges: {stats['cross_ca_edges']} ({stats['cross_ca_percentage']:.1f}%)")
    print(f"    - Communities detected: {stats['n_communities']}")
    print(f"    - Modularity: {stats['modularity']:.3f}")
    
    # Create visualizations
    print("\n[5/5] Creating progress visualizations...")
    create_progress_visualizations(df_combined, G, communities, stats, valid_cols)
    
    # Save data
    df_combined.to_csv('progress_integrated_data.csv', index=False)

    print("\nDone! Files created:")
    print("  - progress_figs/*.png (5 visualizations)")
    print("  - progress_integrated_data.csv")

if __name__ == "__main__":
    main()