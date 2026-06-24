"""
Visualization Functions for FMCG Market Shift Detector
Creates Plotly charts for dashboard
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Premium layout base configuration
def apply_premium_layout(fig, title, height=400, show_x_grid=False, show_y_grid=True):
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family="Inter", size=18, color="#0f172a", weight="bold")
        ),
        font=dict(family="Inter", color="#64748b", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=show_x_grid, 
            gridcolor='#f1f5f9', 
            zeroline=False, 
            showline=True, 
            linecolor='#e2e8f0',
            tickfont=dict(color='#64748b')
        ),
        yaxis=dict(
            showgrid=show_y_grid, 
            gridcolor='#f1f5f9', 
            zeroline=False, 
            showline=False,
            tickfont=dict(color='#64748b')
        ),
        margin=dict(l=20, r=20, t=60, b=20),
        hovermode='x unified',
        height=height,
        colorway=['#4f46e5', '#0ea5e9', '#8b5cf6', '#10b981', '#f59e0b', '#f43f5e', '#64748b']
    )
    return fig


def plot_sales_trend(df, title="Sales Trend Over Time"):
    fig = go.Figure()
    
    # Actual sales with smooth line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['sales'],
        mode='lines+markers',
        name='Actual Sales',
        line=dict(color='#4f46e5', width=3, shape='spline'),
        marker=dict(size=6, color='#4f46e5', line=dict(color='white', width=1)),
        fill='tozeroy',
        fillcolor='rgba(79, 70, 229, 0.08)'
    ))
    
    # Rolling averages
    if 'rolling_4w_sales' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['rolling_4w_sales'],
            mode='lines',
            name='4-Week Avg',
            line=dict(color='#0ea5e9', width=2, dash='dash', shape='spline')
        ))
    
    if 'rolling_8w_sales' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['rolling_8w_sales'],
            mode='lines',
            name='8-Week Avg',
            line=dict(color='#8b5cf6', width=2, dash='dot', shape='spline')
        ))
    
    apply_premium_layout(fig, title)
    fig.update_layout(yaxis_title="Sales ($)")
    
    return fig


def plot_growth_rate_trend(df, title="Growth Rate Over Time"):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['sales_growth_rate'] * 100,
        mode='lines',
        name='Growth Rate',
        line=dict(color='#4f46e5', width=3, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(79, 70, 229, 0.1)'
    ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="#cbd5e1", opacity=1)
    
    apply_premium_layout(fig, title, height=350)
    fig.update_layout(yaxis_title="Growth Rate (%)")
    
    return fig


def plot_momentum_acceleration(df, title="Momentum & Acceleration"):
    fig = go.Figure()
    
    # Momentum
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['momentum_pct'],
        mode='lines',
        name='Momentum (%)',
        line=dict(color='#0ea5e9', width=2, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(14, 165, 233, 0.1)',
        yaxis='y'
    ))
    
    # Acceleration
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['acceleration'] * 100,
        mode='lines',
        name='Acceleration (%)',
        line=dict(color='#8b5cf6', width=2, shape='spline'),
        yaxis='y2'
    ))
    
    apply_premium_layout(fig, title, height=350)
    
    fig.update_layout(
        yaxis=dict(title="Momentum (%)", side='left', showgrid=True, gridcolor='#f1f5f9'),
        yaxis2=dict(title="Acceleration (%)", side='right', overlaying='y', showgrid=False),
    )
    
    return fig


def plot_market_shift_score_trend(df, title="Market Shift Score Over Time"):
    fig = go.Figure()
    
    # Clean unified color instead of a rainbow
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['market_shift_score'],
        mode='lines+markers',
        name='Score',
        line=dict(color='#4f46e5', width=2, shape='spline'),
        marker=dict(size=8, color='#4f46e5', line=dict(color='white', width=1.5)),
        fill='tozeroy',
        fillcolor='rgba(79, 70, 229, 0.05)'
    ))
    
    # Add subtle threshold lines, using grayscale/slate for a cleaner look
    fig.add_hline(y=80, line_dash="dash", line_color="#cbd5e1", opacity=0.8, annotation_text="Strong Growth", annotation_font_color="#64748b")
    fig.add_hline(y=60, line_dash="dash", line_color="#e2e8f0", opacity=0.8)
    fig.add_hline(y=40, line_dash="dash", line_color="#e2e8f0", opacity=0.8)
    fig.add_hline(y=20, line_dash="dash", line_color="#cbd5e1", opacity=0.8, annotation_text="Declining", annotation_font_color="#64748b")
    
    apply_premium_layout(fig, title)
    fig.update_layout(yaxis_title="Score (0-100)", yaxis_range=[0, 105])
    
    return fig


def plot_score_components_waterfall(row):
    components = [
        ('Growth', row['growth_score'] * 0.30),
        ('Momentum', row['momentum_score'] * 0.25),
        ('Acceleration', row['acceleration_score'] * 0.20),
        ('Market Share', row['market_share_score'] * 0.15),
        ('Rank', row['rank_score'] * 0.10)
    ]
    
    x = [c[0] for c in components] + ['Total']
    y = [c[1] for c in components] + [row['market_shift_score']]
    
    fig = go.Figure(go.Waterfall(
        x=x,
        y=y,
        measure=['relative'] * 5 + ['total'],
        text=[f"{v:.1f}" for v in y],
        textposition="outside",
        connector={"line": {"color": "#e2e8f0", "width": 2, "dash": "dot"}},
        decreasing={"marker": {"color": "#f43f5e", "line": {"color": "white", "width": 1}}},
        increasing={"marker": {"color": "#10b981", "line": {"color": "white", "width": 1}}},
        totals={"marker": {"color": "#4f46e5", "line": {"color": "white", "width": 1}}},
        hoverinfo="x+y"
    ))
    
    apply_premium_layout(fig, "Market Shift Score Components", show_x_grid=False, show_y_grid=True)
    fig.update_layout(yaxis_title="Weighted Score")
    
    return fig


def plot_category_distribution(df, value_col='sales', title="Category Distribution"):
    cat_data = df.groupby('category')[value_col].sum().reset_index()
    cat_data = cat_data.sort_values(value_col, ascending=False)
    
    # Modern sequential color scale
    fig = px.treemap(
        cat_data,
        path=['category'],
        values=value_col,
        title=title,
        color=value_col,
        color_continuous_scale=['#f8fafc', '#c7d2fe', '#818cf8', '#4f46e5', '#312e81']
    )
    
    fig.update_traces(
        textinfo="label+value+percent parent",
        hovertemplate="<b>%{label}</b><br>Sales: $%{value:,.0f}<br>Share: %{percentParent:.1%}",
        marker=dict(line=dict(color='white', width=2))
    )
    
    apply_premium_layout(fig, title)
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    
    return fig


def plot_top_products_bar(df, n=10, metric='market_shift_score', title="Top Products"):
    top = df.nlargest(n, metric).copy()
    top = top.sort_values(metric, ascending=True) # Sort ascending so largest is on top
    
    # Use a clean unified color for bars, e.g., Indigo
    fig = go.Figure(go.Bar(
        x=top[metric],
        y=top['product_name'],
        orientation='h',
        marker=dict(color='#4f46e5', line=dict(color='white', width=0)),
        text=top[metric].round(1),
        textposition='auto',
        textfont=dict(color='white', family='Inter')
    ))
    
    apply_premium_layout(fig, title, show_x_grid=True, show_y_grid=False)
    fig.update_layout(
        xaxis_title=metric.replace('_', ' ').title(),
        yaxis=dict(title="", categoryorder='total ascending'),
        margin=dict(l=10, r=20, t=50, b=20),
        bargap=0.2
    )
    
    return fig


def plot_signal_distribution(df, title="Signal Distribution"):
    signal_counts = df['signal'].value_counts().reset_index()
    signal_counts.columns = ['signal', 'count']
    
    # Unified Indigo Theme
    color_map = {
        'Emerging Growth': '#312e81',      # Darkest Indigo
        'Positive Momentum': '#4f46e5',    # Primary Indigo
        'Stable': '#818cf8',               # Light Indigo
        'Declining Momentum': '#c7d2fe',   # Lighter Indigo
        'Strong Decline Warning': '#e0e7ff'# Palest Indigo
    }
    
    colors = [color_map.get(s.split(' (')[0], '#cbd5e1') for s in signal_counts['signal']]
    
    fig = go.Figure(go.Pie(
        labels=signal_counts['signal'],
        values=signal_counts['count'],
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        hole=0.6,
        textinfo='percent',
        hoverinfo='label+value+percent'
    ))
    
    # Add center text
    fig.add_annotation(
        x=0.5, y=0.5,
        text=f"<span style='font-size:24px; font-weight:bold; color:#0f172a;'>{len(df)}</span><br><span style='color:#64748b;'>Products</span>",
        showarrow=False
    )
    
    apply_premium_layout(fig, title)
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20), 
        showlegend=True, 
        legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5, font=dict(color="#475569"))
    )
    
    return fig


def plot_regional_heatmap(df, metric='market_shift_score', title="Regional Performance Heatmap"):
    pivot = df.pivot_table(
        values=metric,
        index='category',
        columns='region',
        aggfunc='mean'
    )
    
    # Modern continuous scale, unified theme
    custom_colorscale = [
        [0.0, '#f8fafc'],
        [0.5, '#a5b4fc'],
        [1.0, '#4f46e5']
    ]
    
    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale=custom_colorscale,
        text=pivot.values.round(1),
        texttemplate='%{text}',
        textfont={"size": 12, "family": "Inter", "color": "#0f172a"},
        colorbar=dict(
            title=metric.replace('_', ' ').title(),
            thickness=10,
            outlinewidth=0,
            tickfont=dict(family="Inter", color="#64748b")
        ),
        xgap=4,
        ygap=4
    ))
    
    apply_premium_layout(fig, title, show_x_grid=False, show_y_grid=False)
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        margin=dict(l=10, r=10, t=50, b=20)
    )
    
    return fig


def plot_scatter_growth_vs_momentum(df, title="Growth vs Momentum Analysis"):
    fig = px.scatter(
        df,
        x='sales_growth_rate',
        y='momentum_pct',
        size='sales',
        color='category',
        hover_data=['product_name', 'market_shift_score'],
        title=title,
        labels={
            'sales_growth_rate': 'Growth Rate (%)',
            'momentum_pct': 'Momentum (%)',
            'sales': 'Sales'
        },
        color_discrete_sequence=['#4f46e5', '#0ea5e9', '#8b5cf6', '#10b981', '#f59e0b', '#06b6d4']
    )
    
    fig.update_traces(
        marker=dict(line=dict(width=1, color='white'), opacity=0.7)
    )
    
    # Add quadrant lines
    fig.add_hline(y=0, line_dash="dash", line_color="#cbd5e1", opacity=1)
    fig.add_vline(x=0, line_dash="dash", line_color="#cbd5e1", opacity=1)
    
    # Add quadrant annotations
    fig.add_annotation(x=df['sales_growth_rate'].max()*0.8, y=df['momentum_pct'].max()*0.8, text="Strong Growth", showarrow=False, font=dict(color="#64748b", size=14, family="Inter"))
    fig.add_annotation(x=df['sales_growth_rate'].min()*0.8, y=df['momentum_pct'].min()*0.8, text="Decline", showarrow=False, font=dict(color="#64748b", size=14, family="Inter"))
    
    apply_premium_layout(fig, title, height=500)
    
    return fig


def plot_score_distribution(df, title="Market Shift Score Distribution"):
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df['market_shift_score'],
        nbinsx=15,
        marker=dict(
            color='#4f46e5',
            line=dict(color='white', width=1.5)
        ),
        showlegend=False,
        opacity=0.85
    ))
    
    # Add vertical lines for thresholds
    fig.add_vline(x=80, line_dash="dot", line_color="#10b981", opacity=0.8, annotation_text="Strong", annotation_position="top left", annotation_font_color="#10b981")
    fig.add_vline(x=60, line_dash="dot", line_color="#0ea5e9", opacity=0.8)
    fig.add_vline(x=40, line_dash="dot", line_color="#94a3b8", opacity=0.8)
    fig.add_vline(x=20, line_dash="dot", line_color="#f59e0b", opacity=0.8, annotation_text="Decline", annotation_position="top right", annotation_font_color="#f59e0b")
    
    apply_premium_layout(fig, title, show_x_grid=False, show_y_grid=True)
    fig.update_layout(
        xaxis_title="Market Shift Score",
        yaxis_title="Number of Products",
        bargap=0.1
    )
    
    return fig
