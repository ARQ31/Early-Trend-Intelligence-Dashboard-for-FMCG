"""
Data Preprocessing for FMCG Market Shift Detector
Handles data cleaning, aggregation, and preparation
"""

import pandas as pd
import numpy as np


def clean_data(df):
    """
    Clean and standardize the dataset
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw sales data
        
    Returns:
    --------
    pd.DataFrame
        Cleaned data
    """
    df = df.copy()
    
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    df = df.dropna(subset=['date', 'product_id', 'sales'])
    df['quantity'] = df['quantity'].fillna(0)
    
    # Standardize text columns
    df['product_name'] = df['product_name'].str.strip()
    df['category'] = df['category'].str.strip()
    df['region'] = df['region'].str.strip()
    
    # Ensure non-negative sales
    df['sales'] = df['sales'].clip(lower=0)
    df['quantity'] = df['quantity'].clip(lower=0)
    
    return df


def aggregate_weekly(df):
    """
    Aggregate data by week, product, category, and region
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned sales data
        
    Returns:
    --------
    pd.DataFrame
        Weekly aggregated data
    """
    df = df.copy()
    
    # Add week number
    df['year'] = df['date'].dt.year
    df['week'] = df['date'].dt.isocalendar().week
    df['year_week'] = df['year'].astype(str) + '-W' + df['week'].astype(str).str.zfill(2)
    
    # Aggregate by week, product, and region
    weekly = df.groupby([
        'date', 'year_week', 'product_id', 'product_name', 
        'category', 'region'
    ]).agg({
        'sales': 'sum',
        'quantity': 'sum'
    }).reset_index()
    
    return weekly


def aggregate_monthly(df):
    """
    Aggregate data by month, product, category, and region
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned sales data
        
    Returns:
    --------
    pd.DataFrame
        Monthly aggregated data
    """
    df = df.copy()
    
    # Add month
    df['year_month'] = df['date'].dt.to_period('M').astype(str)
    df['month_start'] = df['date'].dt.to_period('M').dt.to_timestamp()
    
    # Aggregate by month, product, and region
    monthly = df.groupby([
        'month_start', 'year_month', 'product_id', 'product_name',
        'category', 'region'
    ]).agg({
        'sales': 'sum',
        'quantity': 'sum'
    }).reset_index()
    
    monthly = monthly.rename(columns={'month_start': 'date'})
    
    return monthly


def create_product_region_series(df, freq='W'):
    """
    Create complete time series for each product-region combination
    filling missing periods with zeros
    
    Parameters:
    -----------
    df : pd.DataFrame
        Sales data
    freq : str
        Frequency: 'W' for weekly, 'M' for monthly
        
    Returns:
    --------
    pd.DataFrame
        Complete time series
    """
    # Get all unique combinations
    all_dates = pd.date_range(df['date'].min(), df['date'].max(), freq=freq)
    all_products = df[['product_id', 'product_name', 'category']].drop_duplicates()
    all_regions = df['region'].unique()
    
    # Create complete index
    index_data = []
    for date in all_dates:
        for _, product in all_products.iterrows():
            for region in all_regions:
                index_data.append({
                    'date': date,
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'category': product['category'],
                    'region': region
                })
    
    complete_index = pd.DataFrame(index_data)
    
    # Merge with actual data
    complete_df = complete_index.merge(
        df[['date', 'product_id', 'region', 'sales', 'quantity']],
        on=['date', 'product_id', 'region'],
        how='left'
    )
    
    # Fill missing with zero
    complete_df['sales'] = complete_df['sales'].fillna(0)
    complete_df['quantity'] = complete_df['quantity'].fillna(0)
    
    return complete_df


def prepare_for_analysis(df, aggregation='weekly'):
    """
    Complete preprocessing pipeline
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw sales data
    aggregation : str
        'weekly' or 'monthly'
        
    Returns:
    --------
    pd.DataFrame
        Preprocessed data ready for analysis
    """
    # Clean data
    df_clean = clean_data(df)
    
    # Aggregate
    if aggregation == 'weekly':
        df_agg = aggregate_weekly(df_clean)
    else:
        df_agg = aggregate_monthly(df_clean)
    
    # Sort by date and product
    df_agg = df_agg.sort_values(['product_id', 'region', 'date']).reset_index(drop=True)
    
    return df_agg
