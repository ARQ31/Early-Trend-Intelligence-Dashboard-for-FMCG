"""
Page 3: Product Deep Dive
Detailed analysis of individual products
"""

import streamlit as st
import pandas as pd
from src.visualization import (
    plot_sales_trend,
    plot_growth_rate_trend,
    plot_momentum_acceleration,
    plot_market_shift_score_trend,
    plot_score_components_waterfall
)
from src.insights import generate_product_insight


def render(df_all, df_latest):
    """
    Render Product Deep Dive page
    
    Parameters:
    -----------
    df_all : pd.DataFrame
        All historical data with features
    df_latest : pd.DataFrame
        Latest period data
    """
    st.title("Product Deep Dive")
    st.markdown("Detailed analysis of individual product performance and trends")
    
    st.divider()
    
    # Product selector
    col1, col2 = st.columns([2, 1])
    
    with col1:
        products = sorted(df_latest['product_name'].unique().tolist())
        selected_product = st.selectbox("Select Product", products)
    
    with col2:
        regions = sorted(df_all['region'].unique().tolist())
        selected_region = st.selectbox("Select Region", regions)
    
    # Filter data for selected product and region
    product_data = df_all[
        (df_all['product_name'] == selected_product) &
        (df_all['region'] == selected_region)
    ].sort_values('date').copy()
    
    if len(product_data) == 0:
        st.error("No data available for this product-region combination")
        return
    
    # Get latest data point
    latest_row = product_data.iloc[-1]
    
    st.divider()
    
    # Key metrics
    st.subheader("Current Performance")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Market Shift Score",
            f"{latest_row['market_shift_score']:.1f}/100"
        )
    
    with col2:
        growth = latest_row['sales_growth_rate'] * 100
        st.metric("Growth Rate", f"{growth:+.1f}%")
    
    with col3:
        momentum = latest_row['momentum_pct']
        st.metric("Momentum", f"{momentum:+.1f}%")
    
    with col4:
        rank = int(latest_row['category_rank'])
        rank_change = int(latest_row.get('rank_change', 0))
        st.metric(
            "Category Rank",
            f"#{rank}",
            delta=f"{-rank_change}" if rank_change != 0 else None,
            delta_color="normal"
        )
    
    with col5:
        share = latest_row['category_market_share']
        st.metric("Market Share", f"{share:.2f}%")
    
    # Signal badge
    signal = latest_row['signal']
    if 'Emerging Growth' in signal:
        st.success(f"Signal: {signal}")
    elif 'Positive' in signal:
        st.info(f"Signal: {signal}")
    elif 'Stable' in signal:
        st.info(f"Signal: {signal}")
    elif 'Declining' in signal:
        st.warning(f"Signal: {signal}")
    else:
        st.error(f"Signal: {signal}")
    
    st.divider()
    
    # Time series charts
    st.subheader("Historical Trends")
    
    # Sales trend
    fig = plot_sales_trend(product_data, title=f"{selected_product} - Sales Trend")
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Growth rate trend
        fig = plot_growth_rate_trend(product_data, title="Growth Rate Trend")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Momentum and acceleration
        fig = plot_momentum_acceleration(product_data, title="Momentum & Acceleration")
        st.plotly_chart(fig, use_container_width=True)
    
    # Market Shift Score trend
    fig = plot_market_shift_score_trend(product_data, title="Market Shift Score Evolution")
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Score component breakdown
    st.subheader("Score Component Breakdown")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = plot_score_components_waterfall(latest_row)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Component Scores:**")
        components = {
            'Growth': latest_row['growth_score'],
            'Momentum': latest_row['momentum_score'],
            'Acceleration': latest_row['acceleration_score'],
            'Market Share': latest_row['market_share_score'],
            'Rank': latest_row['rank_score']
        }
        
        for name, score in components.items():
            st.metric(name, f"{score:.1f}/100")
    
    st.divider()
    
    # Business insights
    st.subheader("Business Insights")
    
    insight = generate_product_insight(latest_row)
    st.markdown(insight)
    
    st.divider()
    
    # Detailed statistics
    with st.expander("View Detailed Statistics"):
        st.markdown("**Recent Performance (Last 8 Weeks)**")
        
        recent = product_data.tail(8)[[
            'date', 'sales', 'quantity', 'sales_growth_rate', 'momentum_pct',
            'acceleration', 'market_shift_score'
        ]].copy()
        
        recent['sales_growth_rate'] = recent['sales_growth_rate'] * 100
        
        st.dataframe(
            recent.style.format({
                'date': lambda x: x.strftime('%Y-%m-%d'),
                'sales': '${:,.0f}',
                'quantity': '{:,.0f}',
                'sales_growth_rate': '{:+.1f}%',
                'momentum_pct': '{:+.1f}%',
                'acceleration': '{:+.3f}',
                'market_shift_score': '{:.1f}'
            }),
            use_container_width=True
        )
