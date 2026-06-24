"""
Page 4: Category & Region Analysis
Compare performance across categories and regions
"""

import streamlit as st
import pandas as pd
from src.visualization import (
    plot_regional_heatmap,
    plot_top_products_bar
)
from src.insights import generate_category_insight, generate_regional_insight


def render(df_latest):
    """
    Render Category & Region Analysis page
    
    Parameters:
    -----------
    df_latest : pd.DataFrame
        Latest period data with all features and scores
    """
    st.title("Category & Region Analysis")
    st.markdown("Compare market shifts across categories and geographic regions")
    
    st.divider()
    
    # Analysis type selector
    analysis_type = st.radio(
        "Select Analysis View",
        ["Category Analysis", "Regional Analysis", "Category-Region Matrix"],
        horizontal=True
    )
    
    st.divider()
    
    if analysis_type == "Category Analysis":
        render_category_analysis(df_latest)
    elif analysis_type == "Regional Analysis":
        render_regional_analysis(df_latest)
    else:
        render_matrix_analysis(df_latest)


def render_category_analysis(df_latest):
    """Render category comparison view"""
    st.subheader("Category Performance Comparison")
    
    # Category selector
    categories = sorted(df_latest['category'].unique().tolist())
    selected_category = st.selectbox("Select Category for Deep Dive", categories)
    
    st.divider()
    
    # Overall category comparison
    st.markdown("### All Categories Overview")
    
    cat_summary = df_latest.groupby('category').agg({
        'sales': 'sum',
        'quantity': 'sum',
        'market_shift_score': 'mean',
        'sales_growth_rate': 'mean',
        'product_id': 'nunique'
    }).reset_index()
    
    cat_summary.columns = ['Category', 'Total Sales', 'Total Quantity', 'Avg Score', 'Avg Growth', 'Num Products']
    cat_summary['Avg Growth'] = cat_summary['Avg Growth'] * 100
    cat_summary = cat_summary.sort_values('Avg Score', ascending=False)
    
    st.dataframe(
        cat_summary.style.format({
            'Total Sales': '${:,.0f}',
            'Total Quantity': '{:,.0f}',
            'Avg Score': '{:.1f}',
            'Avg Growth': '{:+.1f}%',
            'Num Products': '{:.0f}'
        }).background_gradient(subset=['Avg Score'], cmap='Blues'),
        use_container_width=True
    )
    
    st.divider()
    
    # Selected category deep dive
    st.markdown(f"### {selected_category} Deep Dive")
    
    cat_data = df_latest[df_latest['category'] == selected_category]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = cat_data['sales'].sum()
        st.metric("Total Sales", f"${total_sales:,.0f}")
    
    with col2:
        avg_score = cat_data['market_shift_score'].mean()
        st.metric("Avg Score", f"{avg_score:.1f}/100")
    
    with col3:
        avg_growth = cat_data['sales_growth_rate'].mean() * 100
        st.metric("Avg Growth", f"{avg_growth:+.1f}%")
    
    with col4:
        num_products = cat_data['product_id'].nunique()
        st.metric("Products", f"{num_products}")
    
    # Top products in category
    st.markdown("**Top Products by Market Shift Score**")
    fig = plot_top_products_bar(cat_data, n=10, metric='market_shift_score', 
                                 title=f"Top 10 Products in {selected_category}")
    st.plotly_chart(fig, use_container_width=True)
    
    # Category insights
    with st.expander("💡 Category Insights"):
        insight = generate_category_insight(df_latest, selected_category)
        st.markdown(insight)


def render_regional_analysis(df_latest):
    """Render regional comparison view"""
    st.subheader("Regional Performance Comparison")
    
    # Region selector
    regions = sorted(df_latest['region'].unique().tolist())
    selected_region = st.selectbox("Select Region for Deep Dive", regions)
    
    st.divider()
    
    # Overall regional comparison
    st.markdown("### All Regions Overview")
    
    reg_summary = df_latest.groupby('region').agg({
        'sales': 'sum',
        'quantity': 'sum',
        'market_shift_score': 'mean',
        'sales_growth_rate': 'mean',
        'product_id': 'nunique'
    }).reset_index()
    
    reg_summary.columns = ['Region', 'Total Sales', 'Total Quantity', 'Avg Score', 'Avg Growth', 'Num Products']
    reg_summary['Avg Growth'] = reg_summary['Avg Growth'] * 100
    reg_summary = reg_summary.sort_values('Avg Score', ascending=False)
    
    st.dataframe(
        reg_summary.style.format({
            'Total Sales': '${:,.0f}',
            'Total Quantity': '{:,.0f}',
            'Avg Score': '{:.1f}',
            'Avg Growth': '{:+.1f}%',
            'Num Products': '{:.0f}'
        }).background_gradient(subset=['Avg Score'], cmap='Blues'),
        use_container_width=True
    )
    
    st.divider()
    
    # Selected region deep dive
    st.markdown(f"### {selected_region} Region Deep Dive")
    
    reg_data = df_latest[df_latest['region'] == selected_region]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = reg_data['sales'].sum()
        st.metric("Total Sales", f"${total_sales:,.0f}")
    
    with col2:
        avg_score = reg_data['market_shift_score'].mean()
        st.metric("Avg Score", f"{avg_score:.1f}/100")
    
    with col3:
        avg_growth = reg_data['sales_growth_rate'].mean() * 100
        st.metric("Avg Growth", f"{avg_growth:+.1f}%")
    
    with col4:
        num_categories = reg_data['category'].nunique()
        st.metric("Categories", f"{num_categories}")
    
    # Category performance in region
    st.markdown("**Category Performance in Region**")
    cat_in_region = reg_data.groupby('category').agg({
        'sales': 'sum',
        'market_shift_score': 'mean'
    }).reset_index().sort_values('market_shift_score', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(
            cat_in_region.style.format({
                'sales': '${:,.0f}',
                'market_shift_score': '{:.1f}'
            }),
            use_container_width=True,
            column_config={
                'category': 'Category',
                'sales': 'Sales',
                'market_shift_score': 'Avg Score'
            }
        )
    
    with col2:
        # Top products in region
        top_products = reg_data.nlargest(10, 'market_shift_score')[
            ['product_name', 'category', 'market_shift_score']
        ]
        st.markdown("**Top Products in Region**")
        st.dataframe(
            top_products.style.format({'market_shift_score': '{:.1f}'}),
            hide_index=True,
            use_container_width=True
        )
    
    # Regional insights
    with st.expander("Regional Insights"):
        insight = generate_regional_insight(df_latest, selected_region)
        st.markdown(insight)


def render_matrix_analysis(df_latest):
    """Render category-region matrix heatmap"""
    st.subheader("Category-Region Performance Matrix")
    
    st.markdown("""
    This heatmap shows average Market Shift Score for each category-region combination.
    Darker green indicates stronger positive market shifts, while red indicates declining momentum.
    """)
    
    # Metric selector
    metric_options = {
        'Market Shift Score': 'market_shift_score',
        'Growth Rate (%)': 'sales_growth_rate',
        'Total Sales': 'sales'
    }
    
    selected_metric = st.selectbox("Select Metric", list(metric_options.keys()))
    metric_col = metric_options[selected_metric]
    
    # Generate heatmap
    fig = plot_regional_heatmap(
        df_latest,
        metric=metric_col,
        title=f"{selected_metric} by Category and Region"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Detailed table
    st.markdown("### Detailed Matrix Data")
    
    pivot = df_latest.pivot_table(
        values=metric_col,
        index='category',
        columns='region',
        aggfunc='mean'
    )
    
    if metric_col == 'sales_growth_rate':
        pivot = pivot * 100
        format_str = '{:+.1f}%'
    elif metric_col == 'sales':
        format_str = '${:,.0f}'
    else:
        format_str = '{:.1f}'
    
    st.dataframe(
        pivot.style.format(format_str).background_gradient(cmap='Blues', axis=None),
        use_container_width=True
    )
