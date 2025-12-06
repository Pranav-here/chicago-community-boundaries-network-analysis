# Data-Driven Community Boundaries in Chicago

**CS 579 Final Project**

Network analysis of socioeconomic boundaries across 4 Chicago Community Areas.

## Key Findings

Analysis of 83 census block groups revealed:
- **27.3%** of network connections cross official Community Area boundaries
- **3-4 natural communities** detected with modularity Q>0.55
- **74.7%** median income growth from 2014 to 2022
- **71.8%** increase in Bachelor's degree attainment from 2014 to 2022

## Approach

Analyzed 4 Community Areas (Portage Park, Austin, West Pullman, West Elsdon) using:
- Census data from ACS 5-year estimates (2014, 2022)
- 10 socioeconomic variables (demographics, education, income, housing, mobility)
- k-NN similarity networks (k=10) with cosine similarity on standardized features
- Louvain and Leiden community detection algorithms
- Temporal comparison and interactive visualizations

## Results

**Network Statistics:**
- 396 total connections between block groups
- 108 (27.3%) cross-CA connections
- Network density: 0.116

**Community Detection:**
- Louvain: 3 communities, Q=0.551
- Leiden: 4 communities, Q=0.586

**Temporal Changes (2014-2022):**
- Median income: $45,508 → $79,506 (+74.7%)
- College graduates: 15.2% → 26.1% (+71.8%)
- Homeownership: 74.1% → 76.8% (+3.6%)

**Visualizations:**
- [01_temporal_analysis.png](final_figs/01_temporal_analysis.png) - 2014 vs 2022 comparison
- [02_community_comparison.png](final_figs/02_community_comparison.png) - Louvain vs Leiden
- [03_network_geographic.png](final_figs/03_network_geographic.png) - Cross-boundary connections
- [04_feature_correlations.png](final_figs/04_feature_correlations.png) - Feature correlation matrix
- [05_ca_profiles.png](final_figs/05_ca_profiles.png) - CA socioeconomic profiles
- [interactive_map.html](final_figs/interactive_map.html) - Interactive Folium map

**Data Outputs:**
- [data_2022.csv](final_figs/data_2022.csv), [data_2014.csv](final_figs/data_2014.csv) - Processed datasets
- [network_2022.gexf](final_figs/network_2022.gexf) - Network file for Gephi

## Stack

**Language:** Python 3

**Libraries:**
- `pandas`, `numpy` - Data processing
- `networkx` - Network analysis
- `scikit-learn` - Similarity computation
- `matplotlib`, `seaborn` - Visualizations
- `folium` - Interactive maps
- `leidenalg`, `python-igraph` - Community detection

**Data Source:** U.S. Census Bureau ACS 5-Year Estimates

---

## Team

- **Melissa Mey Y. Laiz** - CA 15 (Portage Park)
- **Pranav Kuchibhotla** - CA 62 (West Elsdon)
- **Chilla Sai Krishna Reddy** - CA 53 (West Pullman)
- **Krystian Szczepankiewicz** - CA 25 (Austin)

## Future Work

- Expand to all 77 Chicago Community Areas
- Integrate crime data and transit accessibility
- Track evolution across multiple time periods
- Compare with geographic distance-based networks

---

## Project Structure

```
final_project/
├── config.py              # Configuration and constants
├── data_fetcher.py        # Census API data collection
├── features.py            # Feature engineering and temporal analysis
├── network.py             # Network construction and analysis
├── communities.py         # Community detection algorithms
├── visualizations.py      # Visualization generation
└── main.py               # Main analysis script
```

### Quick Start

```bash
# Install dependencies
pip install pandas numpy networkx scikit-learn matplotlib seaborn folium leidenalg python-igraph

# Set Census API key
export CENSUS_API_KEY="your_key_here"

# Run analysis
cd final_project
python main.py
```

Outputs saved to `final_figs/`

---

## Citation

```
Laiz, M., Kuchibhotla, P., Reddy, C., & Szczepankiewicz, K. (2025).
Data-Driven Community Boundaries in Chicago: A Network Analysis Approach.
CS 579 Final Project, Illinois Institute of Technology.
```

---

## References

1. U.S. Census Bureau. *American Community Survey*. https://www.census.gov/programs-surveys/acs
2. City of Chicago Data Portal. https://data.cityofchicago.org/
3. Blondel, V. D., et al. (2008). Fast unfolding of communities in large networks. *Journal of Statistical Mechanics: Theory and Experiment*.
4. Traag, V. A., Waltman, L., & Van Eck, N. J. (2019). From Louvain to Leiden: guaranteeing well-connected communities. *Scientific Reports*.

---

**License:** Educational use only | CS 579 Coursework | Illinois Institute of Technology

**Contact:** For questions or collaboration opportunities, contact the team members or Dr. Cindy Hood.
