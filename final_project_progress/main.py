from data_fetch import fetch_all_cas
from features import compute_features, get_feature_cols
from network import build_cross_ca_network, analyze_network
from visualizations import create_visualizations

def main():
    print("\nCS 579 Final Project - Progress Demo")
    print("Cross-city network analysis\n")

    print("\n[1/5] Fetching block group data...")
    df_combined = fetch_all_cas()

    if df_combined is None:
        print("\nNo data fetched. Check Census API key and tract numbers.")
        return

    print(f"\n  Total: {len(df_combined)} block groups")
    print(f"  CAs: {list(df_combined['ca_name'].unique())}")

    print("\n[2/5] Computing features...")
    df_combined = compute_features(df_combined)

    feature_cols = get_feature_cols()
    print(f"  Features: {len(feature_cols)} variables")

    print("\n[3/5] Building network...")
    G, sim_matrix, valid_cols = build_cross_ca_network(df_combined, feature_cols, k=10)
    print(f"  Network: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"  Valid features: {len(valid_cols)}")

    print("\n[4/5] Analyzing network...")
    stats, communities = analyze_network(G, df_combined)

    print(f"\n  Stats:")
    print(f"    Within-CA edges: {stats['within_ca_edges']}")
    print(f"    Cross-CA edges: {stats['cross_ca_edges']} ({stats['cross_ca_percentage']:.1f}%)")
    print(f"    Communities: {stats['n_communities']}")
    print(f"    Modularity: {stats['modularity']:.3f}")

    print("\n[5/5] Creating visualizations...")
    create_visualizations(df_combined, G, communities, stats, valid_cols)

    df_combined.to_csv('progress_integrated_data.csv', index=False)

    print("\nDone! Files created:")
    print("  - progress_figs/*.png")
    print("  - progress_integrated_data.csv")

if __name__ == "__main__":
    main()
