"""
Market Shift Score Calculation and Signal Classification
Combines multiple indicators into a single actionable score
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def normalize_to_100(series, inverse=False):
    """
    Normalize a series to 0-100 scale
    
    Parameters:
    -----------
    series : pd.Series
        Values to normalize
    inverse : bool
        If True, invert the scale (high values become low)
        
    Returns:
    --------
    pd.Series
        Normalized values (0-100)
    """
    if len(series) == 0 or series.isna().all():
        return series
    
    # Remove infinities
    series = series.replace([np.inf, -np.inf], np.nan)
    
    # Get min and max
    min_val = series.min()
    max_val = series.max()
    
    # Handle case where all values are the same
    if max_val == min_val:
        return pd.Series([50] * len(series), index=series.index)
    
    # Normalize to 0-100
    normalized = ((series - min_val) / (max_val - min_val)) * 100
    
    # Invert if needed
    if inverse:
        normalized = 100 - normalized
    
    # Fill NaN with 50 (neutral)
    normalized = normalized.fillna(50)
    
    return normalized


def calculate_growth_score(df):
    """
    Calculate growth rate component score (0-100)
    Higher growth = higher score
    """
    df = df.copy()
    
    # Use sales growth rate
    # Cap extreme values for normalization
    growth = df['sales_growth_rate'].clip(-1, 3)  # Cap at -100% to +300%
    
    # Shift to positive range and normalize
    # -100% growth = 0 score, 0% growth = 50 score, +300% growth = 100 score
    df['growth_score'] = ((growth + 1) / 4) * 100
    df['growth_score'] = df['growth_score'].clip(0, 100)
    
    return df


def calculate_momentum_score(df):
    """
    Calculate momentum component score (0-100)
    Positive momentum = higher score
    """
    df = df.copy()
    
    # Use momentum percentage
    # Cap extreme values
    momentum = df['momentum_pct'].clip(-50, 50)  # Cap at ±50%
    
    # Normalize: -50% = 0, 0% = 50, +50% = 100
    df['momentum_score'] = ((momentum + 50) / 100) * 100
    df['momentum_score'] = df['momentum_score'].clip(0, 100)
    
    return df


def calculate_acceleration_score(df):
    """
    Calculate acceleration component score (0-100)
    Positive acceleration = higher score
    """
    df = df.copy()
    
    # Use acceleration
    # Cap extreme values
    accel = df['acceleration'].clip(-1, 1)  # Cap at ±100%
    
    # Normalize: -100% = 0, 0% = 50, +100% = 100
    df['acceleration_score'] = ((accel + 1) / 2) * 100
    df['acceleration_score'] = df['acceleration_score'].clip(0, 100)
    
    return df


def calculate_market_share_score(df):
    """
    Calculate market share movement score (0-100)
    Increasing share = higher score
    """
    df = df.copy()
    
    # Use category share change
    # Cap extreme values
    share_change = df['category_share_change'].clip(-10, 10)  # Cap at ±10 percentage points
    
    # Normalize: -10pp = 0, 0pp = 50, +10pp = 100
    df['market_share_score'] = ((share_change + 10) / 20) * 100
    df['market_share_score'] = df['market_share_score'].clip(0, 100)
    
    # Handle missing values (first period has no change)
    df['market_share_score'] = df['market_share_score'].fillna(50)
    
    return df


def calculate_rank_score(df):
    """
    Calculate rank improvement score (0-100)
    Rank improvement = higher score
    """
    df = df.copy()
    
    # Use rank change (negative = improvement)
    # Cap extreme values
    rank_change = df['rank_change'].clip(-10, 10)  # Cap at ±10 positions
    
    # Normalize and invert: -10 = 100 (big improvement), 0 = 50, +10 = 0 (big decline)
    df['rank_score'] = ((-rank_change + 10) / 20) * 100
    df['rank_score'] = df['rank_score'].clip(0, 100)
    
    # Handle missing values (first period has no change)
    df['rank_score'] = df['rank_score'].fillna(50)
    
    return df


def calculate_market_shift_score(df, weights=None):
    """
    Calculate Market Shift Score combining all components
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data with features
    weights : dict, optional
        Custom weights for each component
        Default: {'growth': 0.30, 'momentum': 0.25, 'acceleration': 0.20, 
                 'market_share': 0.15, 'rank': 0.10}
        
    Returns:
    --------
    pd.DataFrame
        Data with Market Shift Score
    """
    df = df.copy()
    
    # Default weights from README
    if weights is None:
        weights = {
            'growth': 0.30,
            'momentum': 0.25,
            'acceleration': 0.20,
            'market_share': 0.15,
            'rank': 0.10
        }
    
    # Calculate component scores
    df = calculate_growth_score(df)
    df = calculate_momentum_score(df)
    df = calculate_acceleration_score(df)
    df = calculate_market_share_score(df)
    df = calculate_rank_score(df)
    
    # Calculate weighted Market Shift Score
    df['market_shift_score'] = (
        weights['growth'] * df['growth_score'] +
        weights['momentum'] * df['momentum_score'] +
        weights['acceleration'] * df['acceleration_score'] +
        weights['market_share'] * df['market_share_score'] +
        weights['rank'] * df['rank_score']
    )
    
    # Ensure score is between 0 and 100
    df['market_shift_score'] = df['market_shift_score'].clip(0, 100)
    
    return df


def classify_signal(row):
    """
    Classify product signal based on Market Shift Score and other indicators
    
    Parameters:
    -----------
    row : pd.Series
        Row with market shift score and features
        
    Returns:
    --------
    str
        Signal classification
    """
    score = row['market_shift_score']
    growth_rate = row['sales_growth_rate']
    volatility = row.get('high_volatility', 0)
    
    # Base classification on score
    if score >= 80 and growth_rate > 0:
        signal = "Emerging Growth"
    elif score >= 60 and growth_rate > 0:
        signal = "Positive Momentum"
    elif score >= 40:
        signal = "Stable"
    elif score >= 20:
        signal = "Declining Momentum"
    else:
        signal = "Strong Decline Warning"
    
    # Add volatility warning
    if volatility == 1:
        signal = signal + " (High Volatility)"
    
    return signal


def add_signal_classification(df):
    """
    Add signal classification to dataframe
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data with Market Shift Score
        
    Returns:
    --------
    pd.DataFrame
        Data with signal classification
    """
    df = df.copy()
    
    df['signal'] = df.apply(classify_signal, axis=1)
    
    return df


def get_top_movers(df, n=10, direction='positive'):
    """
    Get top market movers
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data with Market Shift Score
    n : int
        Number of top movers to return
    direction : str
        'positive' for top gainers, 'negative' for top decliners
        
    Returns:
    --------
    pd.DataFrame
        Top movers
    """
    if direction == 'positive':
        top = df.nlargest(n, 'market_shift_score')
    else:
        top = df.nsmallest(n, 'market_shift_score')
    
    return top


def get_signal_summary(df):
    """
    Get summary statistics by signal type
    
    Parameters:
    -----------
    df : pd.DataFrame
        Data with signals
        
    Returns:
    --------
    pd.DataFrame
        Summary by signal type
    """
    summary = df.groupby('signal').agg({
        'product_id': 'count',
        'sales': 'sum',
        'market_shift_score': 'mean',
        'sales_growth_rate': 'mean'
    }).reset_index()
    
    summary = summary.rename(columns={
        'product_id': 'count',
        'sales': 'total_sales',
        'market_shift_score': 'avg_score',
        'sales_growth_rate': 'avg_growth_rate'
    })
    
    return summary
