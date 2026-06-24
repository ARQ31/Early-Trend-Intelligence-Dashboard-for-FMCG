"""
Business Insights Generator for FMCG Market Shift Detector
Generates rule-based business-friendly insights
"""

import pandas as pd
import numpy as np


def generate_product_insight(row):
    """
    Generate business insight for a single product
    
    Parameters:
    -----------
    row : pd.Series
        Product data with features and scores
        
    Returns:
    --------
    str
        Business insight text
    """
    product_name = row['product_name']
    category = row['category']
    signal = row['signal']
    score = row['market_shift_score']
    growth_rate = row['sales_growth_rate'] * 100
    momentum_pct = row['momentum_pct']
    rank_change = row.get('rank_change', 0)
    
    insights = []
    
    # Opening statement based on signal
    if 'Emerging Growth' in signal:
        insights.append(f"**{product_name}** shows strong early positive market movement.")
    elif 'Positive Momentum' in signal:
        insights.append(f"**{product_name}** demonstrates positive momentum in the {category} category.")
    elif 'Stable' in signal:
        insights.append(f"**{product_name}** maintains stable performance in the {category} category.")
    elif 'Declining Momentum' in signal:
        insights.append(f"**{product_name}** shows early signs of weakening demand.")
    else:  # Strong Decline Warning
        insights.append(f"**{product_name}** shows concerning decline signals that may require attention.")
    
    # Add score context
    insights.append(f"Market Shift Score: **{score:.1f}/100**")
    
    # Add specific observations
    observations = []
    
    # Growth observation
    if growth_rate > 15:
        observations.append(f"sales increased by {abs(growth_rate):.1f}% compared to the previous period")
    elif growth_rate > 5:
        observations.append(f"sales grew by {abs(growth_rate):.1f}%")
    elif growth_rate > -5:
        observations.append(f"sales remained relatively flat with {growth_rate:+.1f}% change")
    elif growth_rate > -15:
        observations.append(f"sales declined by {abs(growth_rate):.1f}%")
    else:
        observations.append(f"sales dropped significantly by {abs(growth_rate):.1f}%")
    
    # Momentum observation
    if momentum_pct > 10:
        observations.append(f"rolling 4-week sales are {abs(momentum_pct):.1f}% above the 8-week average")
    elif momentum_pct < -10:
        observations.append(f"recent sales trend is {abs(momentum_pct):.1f}% below the longer-term average")
    
    # Rank observation
    if rank_change < -2:
        observations.append(f"category rank improved by {abs(int(rank_change))} positions")
    elif rank_change > 2:
        observations.append(f"category rank declined by {int(rank_change)} positions")
    
    if observations:
        insights.append("Key indicators: " + ", ".join(observations) + ".")
    
    # Add business recommendation
    recommendation = generate_recommendation(row)
    if recommendation:
        insights.append(f"\n**Business Implication:** {recommendation}")
    
    return "\n\n".join(insights)


def generate_recommendation(row):
    """
    Generate business recommendation based on signals
    
    Parameters:
    -----------
    row : pd.Series
        Product data with features and scores
        
    Returns:
    --------
    str
        Recommendation text
    """
    signal = row['signal']
    score = row['market_shift_score']
    growth_rate = row['sales_growth_rate']
    volatility = row.get('high_volatility', 0)
    
    if 'Emerging Growth' in signal:
        rec = "This product may indicate growing consumer demand. Consider increasing marketing support, ensuring adequate inventory levels, and monitoring for sustained growth patterns."
    
    elif 'Positive Momentum' in signal:
        rec = "The positive trend should be monitored to confirm sustained growth. This may be a good candidate for promotional activities or expanded distribution."
    
    elif 'Stable' in signal:
        rec = "This product shows steady performance. Continue current strategy while monitoring for any shifts in market dynamics or competitive pressure."
    
    elif 'Declining Momentum' in signal:
        rec = "Further investigation may be needed to understand whether this decline is due to pricing, promotion effectiveness, competition, or changing consumer preferences. Consider customer feedback and competitive analysis."
    
    else:  # Strong Decline Warning
        rec = "This product requires immediate attention. Conduct root cause analysis covering pricing strategy, competitive landscape, product quality issues, and distribution effectiveness. May need intervention or portfolio review."
    
    # Add volatility warning
    if volatility == 1:
        rec += " Note: High volatility detected - patterns should be validated over multiple periods before making major decisions."
    
    return rec


def generate_category_insight(df, category):
    """
    Generate insights for an entire category
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data with features and scores
    category : str
        Category name
        
    Returns:
    --------
    str
        Category insight text
    """
    cat_data = df[df['category'] == category].copy()
    
    if len(cat_data) == 0:
        return f"No data available for {category}."
    
    insights = []
    insights.append(f"## {category} Category Overview")
    
    # Summary statistics
    total_sales = cat_data['sales'].sum()
    avg_growth = cat_data['sales_growth_rate'].mean() * 100
    avg_score = cat_data['market_shift_score'].mean()
    
    insights.append(f"Total Sales: ${total_sales:,.0f}")
    insights.append(f"Average Growth Rate: {avg_growth:+.1f}%")
    insights.append(f"Average Market Shift Score: {avg_score:.1f}/100")
    
    # Signal distribution
    signal_counts = cat_data['signal'].value_counts()
    insights.append("\n**Signal Distribution:**")
    for signal, count in signal_counts.items():
        insights.append(f"- {signal}: {count} products")
    
    # Top performers
    top_3 = cat_data.nlargest(3, 'market_shift_score')[['product_name', 'market_shift_score']]
    insights.append("\n**Top Performers:**")
    for _, row in top_3.iterrows():
        insights.append(f"- {row['product_name']}: {row['market_shift_score']:.1f}")
    
    # Category-level recommendation
    if avg_score > 60:
        rec = "This category shows strong overall momentum and may warrant increased investment."
    elif avg_score > 40:
        rec = "This category shows stable performance. Monitor for emerging sub-trends."
    else:
        rec = "This category shows declining momentum. Review product portfolio and competitive positioning."
    
    insights.append(f"\n**Category Assessment:** {rec}")
    
    return "\n\n".join(insights)


def generate_regional_insight(df, region):
    """
    Generate insights for a specific region
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data with features and scores
    region : str
        Region name
        
    Returns:
    --------
    str
        Regional insight text
    """
    reg_data = df[df['region'] == region].copy()
    
    if len(reg_data) == 0:
        return f"No data available for {region} region."
    
    insights = []
    insights.append(f"## {region} Region Overview")
    
    # Summary statistics
    total_sales = reg_data['sales'].sum()
    avg_growth = reg_data['sales_growth_rate'].mean() * 100
    avg_score = reg_data['market_shift_score'].mean()
    
    insights.append(f"Total Sales: ${total_sales:,.0f}")
    insights.append(f"Average Growth Rate: {avg_growth:+.1f}%")
    insights.append(f"Average Market Shift Score: {avg_score:.1f}/100")
    
    # Top categories in this region
    cat_sales = reg_data.groupby('category')['sales'].sum().sort_values(ascending=False)
    insights.append("\n**Top Categories by Sales:**")
    for cat, sales in cat_sales.head(5).items():
        insights.append(f"- {cat}: ${sales:,.0f}")
    
    # Regional assessment
    if avg_growth > 10:
        rec = "This region demonstrates strong growth momentum. Consider it for expansion or test marketing."
    elif avg_growth > 0:
        rec = "This region shows positive but moderate growth. Continue monitoring performance trends."
    else:
        rec = "This region shows declining performance. Investigate local competition, distribution, or market factors."
    
    insights.append(f"\n**Regional Assessment:** {rec}")
    
    return "\n\n".join(insights)


def generate_executive_summary(df):
    """
    Generate executive summary of market shifts
    
    Parameters:
    -----------
    df : pd.DataFrame
        Latest period data with scores
        
    Returns:
    --------
    str
        Executive summary text
    """
    insights = []
    insights.append("# Market Shift Executive Summary")
    
    # Overall metrics
    total_products = len(df)
    avg_score = df['market_shift_score'].mean()
    median_growth = df['sales_growth_rate'].median() * 100
    
    # Signal distribution
    strong_growth = len(df[df['signal'].str.contains('Emerging Growth')])
    positive = len(df[df['signal'].str.contains('Positive Momentum')])
    declining = len(df[df['signal'].str.contains('Declining')])
    strong_decline = len(df[df['signal'].str.contains('Strong Decline')])
    
    insights.append(f"Analyzing {total_products} products across all categories and regions.")
    insights.append(f"Average Market Shift Score: **{avg_score:.1f}/100**")
    insights.append(f"Median Growth Rate: **{median_growth:+.1f}%**")
    
    insights.append("\n## Key Findings")
    insights.append(f"- **{strong_growth}** products showing strong emerging growth signals")
    insights.append(f"- **{positive}** products with positive momentum")
    insights.append(f"- **{declining}** products showing early decline warnings")
    insights.append(f"- **{strong_decline}** products with strong decline signals")
    
    # Top movers
    top_gainer = df.nlargest(1, 'market_shift_score').iloc[0]
    top_decliner = df.nsmallest(1, 'market_shift_score').iloc[0]
    
    insights.append("\n## Notable Movements")
    insights.append(f"**Strongest Positive Signal:** {top_gainer['product_name']} ({top_gainer['category']}) - Score: {top_gainer['market_shift_score']:.1f}")
    insights.append(f"**Strongest Negative Signal:** {top_decliner['product_name']} ({top_decliner['category']}) - Score: {top_decliner['market_shift_score']:.1f}")
    
    # Category highlights
    cat_scores = df.groupby('category')['market_shift_score'].mean().sort_values(ascending=False)
    best_cat = cat_scores.index[0]
    worst_cat = cat_scores.index[-1]
    
    insights.append("\n## Category Highlights")
    insights.append(f"**Strongest Category:** {best_cat} (Avg Score: {cat_scores.iloc[0]:.1f})")
    insights.append(f"**Weakest Category:** {worst_cat} (Avg Score: {cat_scores.iloc[-1]:.1f})")
    
    return "\n\n".join(insights)
