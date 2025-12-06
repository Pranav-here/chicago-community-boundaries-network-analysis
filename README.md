# Data-Driven Community Boundaries in Chicago

**CS 579 Final Project | Network Science & Urban Informatics**

> **Key Finding:** We discovered that **27.3% of socioeconomic connections cross official Chicago Community Area boundaries** — revealing that administrative divisions don't match how neighborhoods actually function.

---

## The Discovery

We analyzed **83 census block groups** across 4 diverse Chicago neighborhoods and found that the city's official boundaries are outdated. Using network science and census data, we detected **3-4 natural communities** with strong internal structure (modularity Q=0.586) that completely ignore administrative lines.

**The numbers tell the story:**
- **396 total network connections** between socioeconomically similar neighborhoods
- **108 connections (27.3%)** cross official Community Area boundaries
- **74.7% median income growth** from 2014 to 2022
- **71.8% increase in Bachelor's+ education** over 8 years
- **3-4 data-driven communities** detected with Q>0.55 modularity

---

## What We Built

We extended individual neighborhood analyses into a **unified cross-city network** that reveals natural community patterns. Our system:

- **Integrated 4 Community Areas** spanning Northwest to Far South Chicago (Portage Park, Austin, West Pullman, West Elsdon)
- **Analyzed 10 socioeconomic variables** from U.S. Census Bureau data (race, education, income, housing, mobility)
- **Constructed k-nearest neighbor networks** (k=10) using cosine similarity on standardized features
- **Detected communities** with both Louvain and Leiden algorithms
- **Compared temporal patterns** across 2014 and 2022 to track neighborhood evolution
- **Generated interactive visualizations** including a Folium map showing detected communities on real Chicago geography

---

## Major Discoveries

### Cross-Boundary Connections
Nearly **1 in 3 social ties cross official boundaries**, proving that administrative divisions poorly reflect actual community structure. We found 108 cross-CA edges out of 396 total connections.

### Strong Natural Structure
Both algorithms detected clear community patterns with high modularity:
- **Louvain:** 3 communities, Q=0.551
- **Leiden:** 4 communities, Q=0.586

### Massive Economic Growth
The neighborhoods transformed dramatically in 8 years:
- **Median income:** $45,508 → $79,506 (+74.7%)
- **College graduates:** 15.2% → 26.1% (+71.8%)
- **Homeownership:** 74.1% → 76.8% (+3.6%)

### Multi-Dimensional Clustering
Communities formed based on complex patterns across demographics, housing, income, and mobility — not single characteristics.

---

## The Results

### Visualizations Generated
- **[01_temporal_analysis.png](final_figs/01_temporal_analysis.png)** — 2014 vs 2022 comparison showing dramatic socioeconomic shifts
- **[02_community_comparison.png](final_figs/02_community_comparison.png)** — Louvain vs Leiden algorithm comparison
- **[03_network_geographic.png](final_figs/03_network_geographic.png)** — Geographic visualization proving 27.3% cross-boundary connections
- **[04_feature_correlations.png](final_figs/04_feature_correlations.png)** — Correlation heatmap of 10 socioeconomic features
- **[05_ca_profiles.png](final_figs/05_ca_profiles.png)** — Socioeconomic profiles by Community Area

### Interactive Map
- **[interactive_map.html](final_figs/interactive_map.html)** — Folium-based interactive map with color-coded communities and detailed popups

### Data Outputs
- **[data_2022.csv](final_figs/data_2022.csv)** — 2022 block group data with computed features
- **[data_2014.csv](final_figs/data_2014.csv)** — 2014 block group data with computed features
- **[network_2022.gexf](final_figs/network_2022.gexf)** — Network file (compatible with Gephi)
- **[FINAL_REPORT.txt](final_figs/FINAL_REPORT.txt)** — Comprehensive analysis report with all findings

---

## The Stack

**Language:** Python 3

**Core Libraries:**
- `pandas`, `numpy` — Data processing and feature engineering
- `networkx` — Network construction and analysis
- `scikit-learn` — Similarity computation and standardization
- `matplotlib`, `seaborn` — Static visualizations
- `folium` — Interactive geographic maps
- `leidenalg`, `python-igraph` — Advanced community detection

**Data Source:** U.S. Census Bureau American Community Survey (ACS) 5-Year Estimates via Census API

---

## The Team

**Melissa Mey Y. Laiz** — CA 15 (Portage Park)
- Northwest Chicago data collection and analysis
- Quality control and validation

**Pranav Kuchibhotla** — CA 62 (West Elsdon)
- Network algorithm implementation
- Southwest visualization and mapping

**Chilla Sai Krishna Reddy** — CA 53 (West Pullman)
- Interactive Folium dashboard development
- Temporal analysis implementation

**Krystian Szczepankiewicz** — CA 25 (Austin)
- Performance optimization research
- Final report compilation and documentation

---

## Research Impact

### Why This Matters

**For Urban Planning:** Data-driven boundaries could inform more effective service delivery zones, aldermanic redistricting, and resource allocation.

**For Policy:** Understanding actual community structure helps target interventions where they'll have maximum impact.

**For Research:** Our methodology scales to all 77 Chicago Community Areas and could apply to any city with census data.

### Future Work

- Expand to all 77 Chicago Community Areas
- Integrate crime data, transit accessibility, and business patterns
- Track evolution across multiple time periods (2010, 2014, 2018, 2022)
- Compare with other network construction methods (geographic distance, mixed approaches)

---

## Quick Start

### Run the Analysis

```bash
# Install dependencies
pip install -r requirements.txt

# Set Census API key (get free key from https://api.census.gov/data/key_signup.html)
export CENSUS_API_KEY="your_key_here"

# Run complete analysis
python final_project_complete.py
```

The script fetches fresh data from Census API, builds networks, detects communities, and generates all visualizations and reports in `final_figs/`.

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
