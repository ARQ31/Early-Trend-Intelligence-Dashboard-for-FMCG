"""
Page 1: Executive Overview
High-level market metrics and top movers
"""

import streamlit as st
import pandas as pd
from src.visualization import (
    plot_category_distribution,
    plot_top_products_bar,
    plot_signal_distribution,
    plot_score_distribution
)
from src.insights import generate_executive_summary
from src.llm_insights import generate_ai_executive_brief


def render(df_latest):
    """
    Render Executive Overview page
    
    Parameters:
    -----------
    df_latest : pd.DataFrame
        Latest period data with all features and scores
    """
    st.title("📊 Executive Overview")
    st.markdown("High-level market intelligence and key performance indicators")
    
    st.divider()
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = df_latest['sales'].sum()
        st.metric("Total Sales", f"${total_sales:,.0f}")
    
    with col2:
        total_products = df_latest['product_id'].nunique()
        st.metric("Active Products", f"{total_products}")
    
    with col3:
        avg_score = df_latest['market_shift_score'].mean()
        st.metric("Avg Market Shift Score", f"{avg_score:.1f}/100")
    
    with col4:
        median_growth = df_latest['sales_growth_rate'].median() * 100
        st.metric("Median Growth Rate", f"{median_growth:+.1f}%")
    
    st.divider()

    # AI Executive Brief
    st.markdown("""
    <div style="
        padding: 22px 24px;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
        margin-bottom: 14px;
    ">
        <div style="font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">
            AI Executive Brief
        </div>
        <div style="font-size: 13px; line-height: 1.6; color: #475569; max-width: 920px;">
            Ringkasan naratif berbasis LLM untuk membantu membaca sinyal pasar secara cepat.
            Fitur ini memakai data dashboard yang sudah dihitung, bukan mengganti Market Shift Score.
            Tambahkan <code style="background:#eef2ff; color:#4f46e5; padding:2px 6px; border-radius:6px;">GROQ_API_KEY</code>
            di <code style="background:#eef2ff; color:#4f46e5; padding:2px 6px; border-radius:6px;">.streamlit/secrets.toml</code> sebelum generate.
        </div>
    </div>
    """, unsafe_allow_html=True)

    generate_ai = st.button("Generate AI Executive Brief", type="primary")

    if generate_ai:
        with st.spinner("Generating AI executive brief..."):
            ai_brief = generate_ai_executive_brief(df_latest)
        st.markdown(ai_brief)
    
    st.divider()
    
    # Signal Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Market Signal Distribution")
        fig = plot_signal_distribution(df_latest)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Score Distribution")
        fig = plot_score_distribution(df_latest)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Category Performance
    st.subheader("Category Performance")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = plot_category_distribution(df_latest, value_col='sales', title="Sales by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Category scores table
        cat_summary = df_latest.groupby('category').agg({
            'sales': 'sum',
            'market_shift_score': 'mean',
            'sales_growth_rate': 'mean'
        }).reset_index()
        cat_summary.columns = ['Category', 'Total Sales', 'Avg Score', 'Avg Growth']
        cat_summary['Avg Growth'] = cat_summary['Avg Growth'] * 100
        cat_summary = cat_summary.sort_values('Avg Score', ascending=False)
        
        st.markdown("**Category Rankings**")
        st.dataframe(
            cat_summary.style.format({
                'Total Sales': '${:,.0f}',
                'Avg Score': '{:.1f}',
                'Avg Growth': '{:+.1f}%'
            }).background_gradient(subset=['Avg Score'], cmap='Blues'),
            hide_index=True,
            use_container_width=True
        )
    
    st.divider()
    
    # Top Movers
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Positive Signals")
        top_positive = df_latest.nlargest(10, 'market_shift_score')[
            ['product_name', 'category', 'market_shift_score', 'sales_growth_rate']
        ].copy()
        top_positive['sales_growth_rate'] = top_positive['sales_growth_rate'] * 100
        st.dataframe(
            top_positive.style.format({
                'market_shift_score': '{:.1f}',
                'sales_growth_rate': '{:+.1f}%'
            }),
            hide_index=True,
            use_container_width=True,
            column_config={
                'product_name': 'Product',
                'category': 'Category',
                'market_shift_score': 'Score',
                'sales_growth_rate': 'Growth'
            }
        )
    
    with col2:
        st.subheader("Top Decline Warnings")
        top_negative = df_latest.nsmallest(10, 'market_shift_score')[
            ['product_name', 'category', 'market_shift_score', 'sales_growth_rate']
        ].copy()
        top_negative['sales_growth_rate'] = top_negative['sales_growth_rate'] * 100
        st.dataframe(
            top_negative.style.format({
                'market_shift_score': '{:.1f}',
                'sales_growth_rate': '{:+.1f}%'
            }),
            hide_index=True,
            use_container_width=True,
            column_config={
                'product_name': 'Product',
                'category': 'Category',
                'market_shift_score': 'Score',
                'sales_growth_rate': 'Growth'
            }
        )
    
    st.divider()
    
    # Executive Summary
    st.subheader("Executive Summary")
    with st.expander("View Detailed Summary", expanded=False):
        summary = generate_executive_summary(df_latest)
        st.markdown(summary)
