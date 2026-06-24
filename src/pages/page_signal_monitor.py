"""
Page 2: Early Signal Monitor
Filterable table of products with market shift signals
"""

import streamlit as st
import pandas as pd
from src.visualization import plot_scatter_growth_vs_momentum


def render(df_latest):
    """
    Render Early Signal Monitor page
    
    Parameters:
    -----------
    df_latest : pd.DataFrame
        Latest period data with all features and scores
    """
    st.title("🔍 Early Signal Monitor")
    st.markdown("Monitor and filter products by market shift signals")
    
    st.divider()
    
    # Filters
    st.subheader("🎛️ Filters")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        categories = ['All'] + sorted(df_latest['category'].unique().tolist())
        selected_category = st.selectbox("Category", categories)
    
    with col2:
        regions = ['All'] + sorted(df_latest['region'].unique().tolist())
        selected_region = st.selectbox("Region", regions)
    
    with col3:
        # Extract base signals (without volatility suffix)
        all_signals = df_latest['signal'].str.split(' \(').str[0].unique()
        signals = ['All'] + sorted(all_signals.tolist())
        selected_signal = st.selectbox("Signal Type", signals)
    
    with col4:
        min_score = st.slider("Min Market Shift Score", 0, 100, 0)
    
    # Apply filters
    filtered_df = df_latest.copy()
    
    if selected_category != 'All':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    if selected_signal != 'All':
        filtered_df = filtered_df[filtered_df['signal'].str.contains(selected_signal)]
    
    filtered_df = filtered_df[filtered_df['market_shift_score'] >= min_score]
    
    st.info(f"Showing {len(filtered_df)} products matching criteria")
    
    st.divider()
    
    # Summary metrics for filtered data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Filtered Products", len(filtered_df))
    
    with col2:
        avg_score = filtered_df['market_shift_score'].mean()
        st.metric("Avg Score", f"{avg_score:.1f}")
    
    with col3:
        avg_growth = filtered_df['sales_growth_rate'].mean() * 100
        st.metric("Avg Growth", f"{avg_growth:+.1f}%")
    
    with col4:
        total_sales = filtered_df['sales'].sum()
        st.metric("Total Sales", f"${total_sales:,.0f}")
    
    st.divider()
    
    # Main data table
    st.subheader("📋 Product Rankings")
    
    # Prepare display dataframe
    display_df = filtered_df[[
        'product_name', 'category', 'region', 'sales', 'sales_growth_rate',
        'momentum_pct', 'acceleration', 'market_shift_score', 'signal'
    ]].copy()
    
    display_df.columns = [
        'Product', 'Category', 'Region', 'Sales', 'Growth Rate',
        'Momentum', 'Acceleration', 'Market Shift Score', 'Signal'
    ]
    
    # Convert to percentages
    display_df['Growth Rate'] = display_df['Growth Rate'] * 100
    
    # Sort by Market Shift Score
    display_df = display_df.sort_values('Market Shift Score', ascending=False).reset_index(drop=True)
    
    # Display with formatting
    st.dataframe(
        display_df.style.format({
            'Sales': '${:,.0f}',
            'Growth Rate': '{:+.1f}%',
            'Momentum': '{:+.1f}%',
            'Acceleration': '{:+.2f}',
            'Market Shift Score': '{:.1f}'
        }).background_gradient(subset=['Market Shift Score'], cmap='Blues'),
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="market_shift_signals.csv",
        mime="text/csv"
    )
    
    st.divider()
    
    # Visualization
    st.subheader("📊 Growth vs Momentum Analysis")
    st.markdown("Quadrant analysis to identify different product dynamics")
    
    if len(filtered_df) > 0:
        fig = plot_scatter_growth_vs_momentum(filtered_df)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Quadrant Interpretation:**
        - **Top Right**: High growth + positive momentum = Strong performers
        - **Top Left**: Negative growth + positive momentum = Early recovery signals
        - **Bottom Right**: High growth + negative momentum = Potential slowdown warning
        - **Bottom Left**: Negative growth + negative momentum = Decline warning
        """)
    else:
        st.warning("No data to display with current filters")
