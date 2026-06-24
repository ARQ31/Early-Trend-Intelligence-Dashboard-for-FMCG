"""
Page 5: Methodology
Explanation of the Market Shift Score and analysis approach
"""

import streamlit as st


def render():
    """Render Methodology page"""
    st.title("📚 Methodology")
    st.markdown("Understanding the Market Shift Detection System")
    
    st.divider()
    
    # Overview
    st.header("🎯 Overview")
    st.markdown("""
    The **Market Shift Detector** is designed to identify early signals of demand changes in FMCG products 
    before they become obvious in standard sales reports. Rather than simply forecasting future sales, 
    this system focuses on detecting subtle shifts in consumer demand, category momentum, product acceleration, 
    and potential market changes.
    """)
    
    st.divider()
    
    # Dataset
    st.header("📊 Dataset")
    st.markdown("""
    ### Data Source
    The dashboard analyzes synthetic FMCG sales data generated with realistic market patterns including:
    - **Time Period**: 24 months of weekly sales data (104 weeks)
    - **Products**: 80+ products across 6 FMCG categories
    - **Categories**: Personal Care, Home Care, Food & Beverage, Baby Care, Household Products, Health & Wellness
    - **Regions**: 5 geographic regions (North, South, East, West, Central)
    - **Patterns**: Seasonal trends, promotional spikes, product lifecycles, gradual growth/decline, sudden shifts
    
    ### Data Structure
    Each record contains:
    - Date, Product ID, Product Name, Category, Region
    - Sales (revenue), Quantity (units sold)
    - Various calculated features for analysis
    """)
    
    st.divider()
    
    # Feature Engineering
    st.header("🔧 Feature Engineering")
    
    with st.expander("📈 Growth Features", expanded=True):
        st.markdown("""
        **Period-over-Period Growth Rate**
        ```
        growth_rate = (current_sales - previous_sales) / previous_sales
        ```
        Measures the percentage change in sales compared to the previous period.
        """)
    
    with st.expander("📊 Rolling Features"):
        st.markdown("""
        **Rolling Averages**
        - **4-Week Rolling Average**: Short-term trend indicator
        - **8-Week Rolling Average**: Long-term trend indicator
        - **Rolling Standard Deviation**: Volatility measure
        
        These smooth out noise and help identify underlying trends.
        """)
    
    with st.expander("⚡ Momentum Features"):
        st.markdown("""
        **Momentum Calculation**
        ```
        momentum = rolling_4w_avg - rolling_8w_avg
        momentum_pct = (momentum / rolling_8w_avg) × 100
        ```
        
        Positive momentum indicates short-term sales are stronger than the long-term average, 
        suggesting accelerating demand. Negative momentum suggests weakening demand.
        """)
    
    with st.expander("🚀 Acceleration Features"):
        st.markdown("""
        **Acceleration Calculation**
        ```
        acceleration = current_growth_rate - previous_growth_rate
        ```
        
        Measures whether growth is speeding up or slowing down. Positive acceleration means 
        the growth rate is increasing (growth is accelerating).
        """)
    
    with st.expander("📍 Market Share Features"):
        st.markdown("""
        **Category Market Share**
        ```
        category_share = (product_sales / total_category_sales) × 100
        share_change = current_share - previous_share
        ```
        
        Tracks whether a product is gaining or losing share within its category.
        """)
    
    with st.expander("🏆 Ranking Features"):
        st.markdown("""
        **Category Rank Movement**
        
        Products are ranked by sales within their category each period. Tracking rank changes 
        helps identify products moving up (gaining competitiveness) or down (losing position).
        
        Rank improvement (moving from 8th to 4th) is a positive signal.
        """)
    
    st.divider()
    
    # Market Shift Score
    st.header("🎯 Market Shift Score")
    
    st.markdown("""
    The **Market Shift Score** combines multiple indicators into a single 0-100 score that represents 
    the strength and direction of market movement for each product.
    """)
    
    st.markdown("### Score Components & Weights")

    st.markdown("""
    | Component | Weight | Description |
    |-----------|--------|-------------|
    | Growth Rate | 30% | Recent sales growth performance |
    | Momentum | 25% | Short-term vs long-term trend |
    | Acceleration | 20% | Change in growth rate |
    | Market Share Movement | 15% | Category share change |
    | Rank Improvement | 10% | Category ranking change |
    """)

    col1, col2 = st.columns([1, 2.6])
    with col1:
        st.info("""
        **Formula**
        
        Market Shift Score = 
        - 0.30 × Growth Score
        - 0.25 × Momentum Score  
        - 0.20 × Acceleration Score
        - 0.15 × Market Share Score
        - 0.10 × Rank Score
        """)
    
    st.markdown("### Component Normalization")

    col1, col2 = st.columns([1, 2.6])
    with col1:
        st.info("""
        **Each component is normalized to a 0-100 scale:**
        - **Growth Score**: -100% growth → 0, 0% growth → 50, +300% growth → 100
        - **Momentum Score**: -50% momentum → 0, 0% → 50, +50% → 100
        - **Acceleration Score**: -100% accel → 0, 0% → 50, +100% → 100
        - **Market Share Score**: -10pp change → 0, 0pp → 50, +10pp → 100
        - **Rank Score**: +10 positions (decline) → 0, 0 → 50, -10 positions (improvement) → 100
        """)
    
    st.divider()
    
    # Signal Classification
    st.header("🚦 Signal Classification")
    
    st.markdown("""
    Products are classified based on their Market Shift Score and growth characteristics:
    """)
    
    signal_table = """
    | Signal | Score Range | Criteria | Meaning |
    |--------|-------------|----------|---------|
    | 🚀 **Emerging Growth** | 80-100 | High score + positive growth | Strong positive market shift |
    | 📈 **Positive Momentum** | 60-79 | Good score + positive growth | Moderate positive shift |
    | ➡️ **Stable** | 40-59 | Mid-range score | Neutral or stable performance |
    | ⚠️ **Declining Momentum** | 20-39 | Low score | Early warning of decline |
    | 🔴 **Strong Decline Warning** | 0-19 | Very low score | Concerning decline signals |
    """
    
    st.markdown(signal_table)
    
    st.warning("""
    **High Volatility Flag**: Products with high coefficient of variation (CV > 0.3) receive 
    a volatility warning, indicating patterns should be validated before major decisions.
    """)
    
    st.divider()
    
    # Limitations
    st.header("⚠️ Limitations & Disclaimers")
    
    st.error("""
    **Important Considerations:**
    
    1. **Proxy Indicator**: The Market Shift Score is a proxy indicator, not a guaranteed prediction. 
    It identifies patterns that *may* indicate market changes.
    
    2. **Data Quality Dependency**: Results depend heavily on data quality, completeness, and accuracy.
    
    3. **External Factors**: The system cannot fully capture external factors such as:
       - Competitor activities and new product launches
       - Pricing strategy changes
       - Distribution changes
       - Macroeconomic conditions
       - Seasonal events and holidays
       - Marketing campaign impacts
    
    4. **Validation Required**: Signals should be validated with business stakeholders, customer feedback, 
    and market research before making major decisions.
    
    5. **Historical Analysis**: The system analyzes historical patterns. Sudden market disruptions 
    or unprecedented events may not be accurately captured.
    
    6. **Context Matters**: A declining product may be intentionally being phased out. A growing product 
    may be benefiting from temporary factors. Always consider business context.
    """)
    
    st.divider()
    
    # Use Cases
    st.header("💼 Business Use Cases")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Marketing & Sales**
        - Identify products needing marketing support
        - Prioritize promotional campaigns
        - Adjust regional sales strategies
        - Plan product portfolio optimization
        """)
    
    with col2:
        st.markdown("""
        **Supply Chain & Planning**
        - Early inventory adjustments
        - Demand forecasting inputs
        - Production planning signals
        - Category management decisions
        """)
    
    st.divider()
    
    # Technical Stack
    st.header("🛠️ Technical Implementation")
    
    st.markdown("""
    ### Technology Stack
    - **Python**: Core programming language
    - **Streamlit**: Interactive dashboard framework
    - **Pandas**: Data manipulation and analysis
    - **NumPy**: Numerical computations
    - **Plotly**: Interactive visualizations
    - **Scikit-learn**: Normalization utilities
    
    ### Project Structure
    ```
    market-shift-detector/
    ├── app.py                      # Main Streamlit app
    ├── requirements.txt            # Python dependencies
    ├── data/                       # Data files
    ├── src/
    │   ├── data_generator.py       # Synthetic data generation
    │   ├── data_loader.py          # Data loading with caching
    │   ├── preprocessing.py        # Data cleaning and aggregation
    │   ├── feature_engineering.py  # Feature calculations
    │   ├── scoring.py              # Market Shift Score logic
    │   ├── insights.py             # Business insights generation
    │   ├── visualization.py        # Plotly chart functions
    │   └── pages/                  # Dashboard pages
    └── docs/                       # Documentation
    ```
    """)
    
    st.divider()
    
    # References
    st.header("📖 References & Further Reading")
    
    st.markdown("""
    This project demonstrates the application of:
    - **Time Series Analysis**: Rolling statistics, trend decomposition
    - **Business Analytics**: KPI design, signal detection
    - **Decision Support Systems**: Actionable insights from data
    - **FMCG Market Analysis**: Category management, demand sensing
    
    The methodology combines standard analytics techniques with domain-specific business logic 
    to create an interpretable early warning system for market changes.
    """)
