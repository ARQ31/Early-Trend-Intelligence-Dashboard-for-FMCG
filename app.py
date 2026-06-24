"""
Market Shift Detector - Early Trend Intelligence Dashboard for FMCG
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.data_loader import load_data
from src.preprocessing import prepare_for_analysis
from src.feature_engineering import calculate_all_features
from src.scoring import calculate_market_shift_score, add_signal_classification
from src.pages import (
    page_executive_overview,
    page_signal_monitor,
    page_product_deepdive,
    page_category_region,
    page_methodology
)


# Page configuration
st.set_page_config(
    page_title="Market Shift Detector",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding-top: 2rem;
    }
    
    /* Premium Metric Cards */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    
    /* Dataframes/Tables Styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 600;
    }
    
    /* Radio Buttons / Navigation */
    .stRadio [role="radiogroup"] {
        gap: 0.5rem;
    }
    div[role="radiogroup"] > label {
        padding: 10px 15px;
        border-radius: 8px;
        background-color: transparent;
        transition: all 0.2s;
    }
    div[role="radiogroup"] > label:hover {
        background-color: #f1f5f9;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        transition: all 0.2s;
        font-weight: 500;
    }
    .stButton > button:hover {
        border-color: #cbd5e1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_and_process_data():
    """Load and process all data with caching"""
    # Load raw data
    df_raw = load_data('data/raw/fmcg_sales_data.csv')
    
    # Preprocess
    df_clean = prepare_for_analysis(df_raw, aggregation='weekly')
    
    # Calculate features
    df_features = calculate_all_features(df_clean)
    
    # Calculate Market Shift Score
    df_scored = calculate_market_shift_score(df_features)
    
    # Add signal classification
    df_final = add_signal_classification(df_scored)
    
    return df_final


def main():
    """Main application"""
    
    # Sidebar
    with st.sidebar:
        st.title("📊 Market Shift Detector")
        st.markdown("---")
        
        # Navigation
        st.subheader("Navigation")
        page = st.radio(
            "Select Page",
            [
                "1. Executive Overview",
                "2. Early Signal Monitor",
                "3. Product Deep Dive",
                "4. Category & Region Analysis",
                "5. Methodology"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Data info
        st.subheader("About")
        st.info("""
        **Market Shift Detector** identifies early signals of demand changes 
        in FMCG products using advanced analytics and the Market Shift Score.
        
        Navigate through pages to explore market intelligence.
        """)
        
        st.markdown("---")
        
        # Data refresh
        if st.button("Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.caption("Built with Streamlit • Python • Plotly")
    
    # Load data
    try:
        with st.spinner("Loading and processing data..."):
            df_all = load_and_process_data()
        
        # Get latest period data
        latest_date = df_all['date'].max()
        df_latest = df_all[df_all['date'] == latest_date].copy()
        
        # Store in session state
        st.session_state['df_all'] = df_all
        st.session_state['df_latest'] = df_latest
        st.session_state['latest_date'] = latest_date
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.stop()
    
    # Display date info
    st.sidebar.markdown(f"**Latest Data:** {latest_date.strftime('%Y-%m-%d')}")
    st.sidebar.markdown(f"**Total Records:** {len(df_all):,}")
    st.sidebar.markdown(f"**Date Range:** {df_all['date'].min().strftime('%Y-%m-%d')} to {df_all['date'].max().strftime('%Y-%m-%d')}")
    
    # Route to selected page
    if page == "1. Executive Overview":
        page_executive_overview.render(df_latest)
    
    elif page == "2. Early Signal Monitor":
        page_signal_monitor.render(df_latest)
    
    elif page == "3. Product Deep Dive":
        page_product_deepdive.render(df_all, df_latest)
    
    elif page == "4. Category & Region Analysis":
        page_category_region.render(df_latest)
    
    elif page == "5. Methodology":
        page_methodology.render()


if __name__ == "__main__":
    main()
