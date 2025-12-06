# presentation_outline.py
# Script to generate slide content for your progress video

def print_presentation_outline():
    """
    2-4 minute presentation outline
    Each team member speaks for ~30-60 seconds
    """
    
    slides = {
        "Slide 1 - Title": """
        DATA-DRIVEN COMMUNITY BOUNDARIES
        Rethinking Chicago's Neighborhood Structure
        
        Team Members:
        - Melissa Mey Y. Laiz - CA 15 (Portage Park)
        - Pranav Kuchibhotla - CA 62 (West Elsdon)  
        - Chilla Sai Krishna Reddy - CA 53 (West Pullman)
        - Krystian Szczepankiewicz - CA 25 (Austin)
        
        CS 579 - Fall 2025
        """,
        
        "Slide 2 - Project Overview": """
        FROM HW4 TO FINAL PROJECT: What Changed?
        
        HW4 (Individual):
        [X] Single CA analysis
        [X] ~35-70 block groups each
        [X] 6 basic variables
        [X] Local neighborhood patterns
        
        Final Project (Team):
        [X] 4 CAs combined (~63 BGs so far)
        [X] 10+ variables (added 3 NEW ones)
        [X] Cross-city similarity analysis
        [ ] Temporal comparison (2010 vs 2022) - IN PROGRESS
        [ ] Interactive visualization - PLANNED
        
        [SHOW: progress_figs/01_data_coverage.png]
        """,
        
        "Slide 3 - Progress: Data Integration": """
        PROGRESS UPDATE: What We've Built
        
        [X] Integrated 4 community areas:
          - Portage Park (NW), Austin (West)
          - West Elsdon (SW), West Pullman (South)
        
        [X] Extended feature set with NEW variables:
          - Housing vacancy rate  
          - Homeownership rate
          - Walk-to-work percentage
          (Note: Foreign-born had data issues, investigating)
        
        [SHOW: progress_figs/02_new_variables.png]
        
        This moves us beyond HW4's limited scope!
        """,
        
        "Slide 4 - Progress: Cross-City Network": """
        CROSS-CITY NETWORK ANALYSIS
        
        Built k-NN similarity graph across all 4 regions:
        - 63 block groups integrated
        - 10 socioeconomic features
        - Cosine similarity + k=10 neighbors
        - 310 total network connections
        
        KEY FINDING: 
        29.4% of edges cross CA boundaries!
        -> Official boundaries don't match lived communities
        
        [SHOW: progress_figs/03_network_structure.png]
        """,
        
        "Slide 5 - Progress: Community Detection": """
        PRELIMINARY COMMUNITY DETECTION
        
        Applied Louvain algorithm:
        - Detected 3 data-driven communities
        - Modularity Q = 0.587 (strong structure!)
        - Communities span multiple official CAs
        
        [SHOW: progress_figs/04_communities.png]
        
        Next: Add Leiden algorithm & compare results
        """,
        
        "Slide 6 - Completion Plan": """
        PATH TO COMPLETION
        
        DONE (HW4 foundation):
        [X] Individual CA networks
        [X] Basic similarity metrics
        [X] Census data pipeline
        
        COMPLETED THIS WEEK:
        [X] Data integration across 4 CAs
        [X] Extended variable set
        [X] Cross-city network building
        [X] Preliminary community detection
        
        REMAINING (Next 2 weeks):
        [ ] Temporal analysis (2010 vs 2022)
        [ ] Leiden algorithm implementation
        [ ] Add crime & transit data
        [ ] Interactive Folium dashboard
        [ ] Final report & visualizations
        
        [SHOW: progress_figs/05_summary_stats.png]
        
        Timeline: Week 1 - Analysis | Week 2 - Visualization & Report
        """
    }
    
    print("="*70)
    print("PRESENTATION SCRIPT (2-4 minutes)")
    print("="*70)
    print("\nTiming: ~30-45 seconds per slide\n")
    
    for slide_num, (title, content) in enumerate(slides.items(), 1):
        print("\n" + "-"*70)
        print(f"SLIDE {slide_num}: {title}")
        print("-"*70)
        print(content)
    
    print("\n" + "="*70)
    print("SPEAKER NOTES:")
    print("="*70)
    print("""
    Melissa: Introduce team & project (Slides 1-2)
    Pranav: Explain data integration & new variables (Slide 3)
    Chilla: Present network analysis results (Slide 4)
    Krystian: Show community detection & completion plan (Slides 5-6)
    
    Total time: 3-4 minutes with visualizations
    """)
    
    print("\n" + "="*70)
    print("ACTUAL RESULTS TO MENTION:")
    print("="*70)
    print("""
    KEY NUMBERS FOR YOUR VIDEO:
    - 63 block groups across 4 CAs
    - 310 network edges (connections)
    - 29.4% cross-CA edges (this is your main finding!)
    - 3 detected communities
    - Modularity Q = 0.587 (very good!)
    - 10 valid features used
    
    TALKING POINTS:
    1. "We integrated 4 diverse Chicago neighborhoods"
    2. "Added 3 new variables beyond our homework"
    3. "Built a cross-city similarity network"
    4. "Found nearly 30% of connections cross official boundaries"
    5. "Detected 3 data-driven communities that don't match the map"
    6. "High modularity shows strong community structure"
    """)

if __name__ == "__main__":
    print_presentation_outline()