"""
Data Loader for FMCG Market Shift Detector
Handles data loading with caching for Streamlit
"""

import pandas as pd
import streamlit as st
import os
from src.data_generator import generate_fmcg_data


@st.cache_data
def load_data(filepath='data/raw/fmcg_sales_data.csv', regenerate=False):
    """
    Load FMCG sales data with caching
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV file
    regenerate : bool
        If True, regenerate the data even if file exists
        
    Returns:
    --------
    pd.DataFrame
        Loaded sales data
    """
    if not os.path.exists(filepath) or regenerate:
        print("Generating new FMCG data...")
        df = generate_fmcg_data()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Save to file
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
    else:
        print(f"Loading data from {filepath}")
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'])
    
    return df


def get_data_summary(df):
    """
    Get summary statistics of the dataset
    
    Parameters:
    -----------
    df : pd.DataFrame
        Sales data
        
    Returns:
    --------
    dict
        Summary statistics
    """
    summary = {
        'total_records': len(df),
        'date_range': (df['date'].min(), df['date'].max()),
        'total_sales': df['sales'].sum(),
        'total_quantity': df['quantity'].sum(),
        'num_products': df['product_id'].nunique(),
        'num_categories': df['category'].nunique(),
        'num_regions': df['region'].nunique(),
        'products': df['product_name'].unique().tolist(),
        'categories': df['category'].unique().tolist(),
        'regions': df['region'].unique().tolist()
    }
    
    return summary


def filter_data(df, categories=None, regions=None, products=None, date_range=None):
    """
    Filter data based on various criteria
    
    Parameters:
    -----------
    df : pd.DataFrame
        Sales data
    categories : list, optional
        List of categories to include
    regions : list, optional
        List of regions to include
    products : list, optional
        List of products to include
    date_range : tuple, optional
        (start_date, end_date) tuple
        
    Returns:
    --------
    pd.DataFrame
        Filtered data
    """
    filtered_df = df.copy()
    
    if categories:
        filtered_df = filtered_df[filtered_df['category'].isin(categories)]
    
    if regions:
        filtered_df = filtered_df[filtered_df['region'].isin(regions)]
    
    if products:
        filtered_df = filtered_df[filtered_df['product_name'].isin(products)]
    
    if date_range:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['date'] >= pd.to_datetime(start_date)) &
            (filtered_df['date'] <= pd.to_datetime(end_date))
        ]
    
    return filtered_df
