"""
Feature Engineering for FMCG Market Shift Detector
Calculates growth, momentum, acceleration, market share, and ranking features
"""

import pandas as pd
import numpy as np
import streamlit as st


@st.cache_data
def calculate_all_features(df):
    """
    Calculate all analytical features for market shift detection
    
    Parameters:
    -----------
    df : pd.DataFrame
        Preprocessed sales data (weekly or monthly)
        
    Returns:
    --------
    pd.DataFrame
        Data with all engineered features
    """
    df = df.copy()
    
    # Sort by product, region, and date
    df = df.sort_values(['product_id', 'region', 'date']).reset_index(drop=True)
    
    # Calculate features by product-region combination
    feature_dfs = []
    
    for (product_id, region), group in df.groupby(['product_id', 'region']):
        group = group.copy()
        
        # Growth features
        group = calculate_growth_features(group)
        
        # Rolling features
        group = calculate_rolling_features(group)
        
        # Momentum features
        group = calculate_momentum_features(group)
        
        # Acceleration features
        group = calculate_acceleration_features(group)
        
        # Volatility features
        group = calculate_volatility_features(group)
        
        feature_dfs.append(group)
    
    # Combine all groups
    df_with_features = pd.concat(feature_dfs, ignore_index=True)
    
    # Calculate market share features (requires all products)
    df_with_features = calculate_market_share_features(df_with_features)
    
    # Calculate ranking features (requires all products within category)
    df_with_features = calculate_ranking_features(df_with_features)
    
    return df_with_features


def calculate_growth_features(df):
    """Calculate period-over-period growth rates"""
    df = df.copy()
    
    # Previous period sales
    df['prev_sales'] = df['sales'].shift(1)
    df['prev_quantity'] = df['quantity'].shift(1)
    
    # Growth rate (handle division by zero)
    df['sales_growth_rate'] = np.where(
        df['prev_sales'] > 0,
        (df['sales'] - df['prev_sales']) / df['prev_sales'],
        0
    )
    
    df['quantity_growth_rate'] = np.where(
        df['prev_quantity'] > 0,
        (df['quantity'] - df['prev_quantity']) / df['prev_quantity'],
        0
    )
    
    # Absolute change
    df['sales_change'] = df['sales'] - df['prev_sales']
    df['quantity_change'] = df['quantity'] - df['prev_quantity']
    
    return df


def calculate_rolling_features(df, short_window=4, long_window=8):
    """Calculate rolling averages and statistics"""
    df = df.copy()
    
    # Rolling averages
    df['rolling_4w_sales'] = df['sales'].rolling(window=short_window, min_periods=1).mean()
    df['rolling_8w_sales'] = df['sales'].rolling(window=long_window, min_periods=1).mean()
    
    df['rolling_4w_quantity'] = df['quantity'].rolling(window=short_window, min_periods=1).mean()
    df['rolling_8w_quantity'] = df['quantity'].rolling(window=long_window, min_periods=1).mean()
    
    # Rolling standard deviation
    df['rolling_4w_std'] = df['sales'].rolling(window=short_window, min_periods=2).std()
    df['rolling_8w_std'] = df['sales'].rolling(window=long_window, min_periods=2).std()
    
    # Rolling min/max
    df['rolling_4w_min'] = df['sales'].rolling(window=short_window, min_periods=1).min()
    df['rolling_4w_max'] = df['sales'].rolling(window=short_window, min_periods=1).max()
    
    return df


def calculate_momentum_features(df):
    """Calculate momentum indicators"""
    df = df.copy()
    
    # Momentum = short-term avg - long-term avg
    df['momentum'] = df['rolling_4w_sales'] - df['rolling_8w_sales']
    
    # Momentum as percentage of long-term average
    df['momentum_pct'] = np.where(
        df['rolling_8w_sales'] > 0,
        (df['momentum'] / df['rolling_8w_sales']) * 100,
        0
    )
    
    # Trend direction: positive momentum = 1, negative = -1
    df['momentum_direction'] = np.sign(df['momentum'])
    
    # Momentum strength (absolute value)
    df['momentum_strength'] = df['momentum'].abs()
    
    return df


def calculate_acceleration_features(df):
    """Calculate acceleration (change in growth rate)"""
    df = df.copy()
    
    # Previous growth rate
    df['prev_growth_rate'] = df['sales_growth_rate'].shift(1)
    
    # Acceleration = current growth - previous growth
    df['acceleration'] = df['sales_growth_rate'] - df['prev_growth_rate']
    
    # Acceleration direction
    df['acceleration_direction'] = np.sign(df['acceleration'])
    
    # Is growth accelerating?
    df['is_accelerating'] = (df['acceleration'] > 0).astype(int)
    
    return df


def calculate_volatility_features(df):
    """Calculate volatility indicators"""
    df = df.copy()
    
    # Coefficient of variation (CV) = std / mean
    df['cv_4w'] = np.where(
        df['rolling_4w_sales'] > 0,
        df['rolling_4w_std'] / df['rolling_4w_sales'],
        0
    )
    
    df['cv_8w'] = np.where(
        df['rolling_8w_sales'] > 0,
        df['rolling_8w_std'] / df['rolling_8w_sales'],
        0
    )
    
    # High volatility flag (CV > 0.3 is considered high)
    df['high_volatility'] = (df['cv_4w'] > 0.3).astype(int)
    
    return df


def calculate_market_share_features(df):
    """Calculate market share within category and overall"""
    df = df.copy()
    
    # Total sales by date and category
    category_totals = df.groupby(['date', 'category'])['sales'].sum().reset_index()
    category_totals = category_totals.rename(columns={'sales': 'category_total_sales'})
    
    # Total overall sales by date
    overall_totals = df.groupby('date')['sales'].sum().reset_index()
    overall_totals = overall_totals.rename(columns={'sales': 'overall_total_sales'})
    
    # Merge totals
    df = df.merge(category_totals, on=['date', 'category'], how='left')
    df = df.merge(overall_totals, on='date', how='left')
    
    # Calculate market share
    df['category_market_share'] = np.where(
        df['category_total_sales'] > 0,
        (df['sales'] / df['category_total_sales']) * 100,
        0
    )
    
    df['overall_market_share'] = np.where(
        df['overall_total_sales'] > 0,
        (df['sales'] / df['overall_total_sales']) * 100,
        0
    )
    
    # Market share change
    df['prev_category_share'] = df.groupby(['product_id', 'region'])['category_market_share'].shift(1)
    df['category_share_change'] = df['category_market_share'] - df['prev_category_share']
    
    return df


def calculate_ranking_features(df):
    """Calculate product ranking within category over time"""
    df = df.copy()
    
    # Rank products by sales within each category and date
    df['category_rank'] = df.groupby(['date', 'category', 'region'])['sales'].rank(
        method='dense', ascending=False
    )
    
    # Previous rank
    df['prev_category_rank'] = df.groupby(['product_id', 'region'])['category_rank'].shift(1)
    
    # Rank change (negative means improvement, positive means decline)
    df['rank_change'] = df['category_rank'] - df['prev_category_rank']
    
    # Rank improvement flag
    df['rank_improved'] = (df['rank_change'] < 0).astype(int)
    df['rank_declined'] = (df['rank_change'] > 0).astype(int)
    
    return df


def get_latest_features(df, n_periods=1):
    """
    Get features for the most recent period(s)
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data with features
    n_periods : int
        Number of recent periods to return
        
    Returns:
    --------
    pd.DataFrame
        Latest period features
    """
    # Get unique dates sorted
    dates = sorted(df['date'].unique())
    latest_dates = dates[-n_periods:]
    
    # Filter to latest dates
    latest_df = df[df['date'].isin(latest_dates)].copy()
    
    return latest_df


def aggregate_features_by_product(df):
    """
    Aggregate features across regions to get product-level view
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data with features (by product-region)
        
    Returns:
    --------
    pd.DataFrame
        Product-level aggregated features
    """
    # Aggregate numeric features
    agg_dict = {
        'sales': 'sum',
        'quantity': 'sum',
        'sales_growth_rate': 'mean',
        'momentum': 'mean',
        'momentum_pct': 'mean',
        'acceleration': 'mean',
        'cv_4w': 'mean',
        'high_volatility': 'max',
        'category_market_share': 'sum',
        'category_rank': 'mean',
        'rank_change': 'mean'
    }
    
    # Group by date, product, category
    product_features = df.groupby(['date', 'product_id', 'product_name', 'category']).agg(
        agg_dict
    ).reset_index()
    
    return product_features
