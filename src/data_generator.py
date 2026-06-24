"""
Data Generator for FMCG Market Shift Detector
Generates realistic synthetic FMCG sales data with various market patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_fmcg_data(start_date='2024-01-01', weeks=104, random_seed=42):
    """
    Generate synthetic FMCG sales data with realistic patterns
    
    Parameters:
    -----------
    start_date : str
        Start date for the dataset
    weeks : int
        Number of weeks to generate (default 104 = 2 years)
    random_seed : int
        Random seed for reproducibility
        
    Returns:
    --------
    pd.DataFrame
        Generated FMCG sales data
    """
    np.random.seed(random_seed)
    random.seed(random_seed)
    
    # Define FMCG categories and products
    categories = {
        'Personal Care': [
            'Pantena Shampoo', 'Sunsleek Shampoo', 'Dovey Conditioner', 'Lifebuoya Body Wash', 'Luxura Body Wash',
            'Pepsodentia Toothpaste', 'Colgata Toothpaste', 'Pondsy Face Wash', 'Rexon Deodorant', 'Axel Deodorant',
            'Dettolia Hand Soap', 'Vaselinea Body Lotion', 'Olayia Facial Cream'
        ],
        'Home Care': [
            'Rinsha Detergent', 'Arielia Detergent', 'Downya Fabric Softener', 'Sunlightia Dish Soap', 'Mamma Lemonia Dish Soap',
            'Super Pellia Floor Cleaner', 'Harpica Bathroom Cleaner', 'Mr. Brawn Glass Cleaner', 'Gladia Air Freshener',
            'Bleachlin Bleach', 'Wipolia Multi-Surface Cleaner', 'Tidia Laundry Pods'
        ],
        'Food & Beverage': [
            'IndoNoodle', 'Mie Sedapicious', 'Nescoffee', 'Kapal Laut Coffee', 'Saritea',
            'Bimolia Cooking Oil', 'Filmia Cooking Oil', 'Bangun Soy Sauce', 'XYZ Chili Sauce', 'Hienz Ketchup',
            'Orea Biscuits', 'Romia Biscuits', 'Ritza Crackers', 'Red Cow Energy Drink', 'Buavida Juice'
        ],
        'Baby Care': [
            'Pamperia Diapers', 'MommyPoko Diapers', 'Cousins Baby Wipes', 'Jackson\'s Baby Powder',
            'Zwitsea Baby Shampoo', 'Dovelet Baby Lotion', 'Cousins Baby Oil', 'Jackson\'s Baby Soap',
            'Cerealac Baby Food', 'SGN Baby Formula'
        ],
        'Household Products': [
            'Passoa Tissue Paper', 'Nicely Tissue Paper', 'Plentiful Kitchen Towel', 'Bagoos Garbage Bags',
            'Clingy Plastic Wrap', 'Diamond Aluminum Foil', 'Tubberware Food Containers', 'Energic Batteries',
            'Philipes Light Bulbs', 'BugGone Insect Repellent'
        ],
        'Health & Wellness': [
            'Enerzon-C Vitamins', 'Whitemores Vitamins', 'Painadol Pain Relief', 'Headrex Cold Medicine',
            'OBH Combo Cough Syrup', 'Betacure First Aid Kit', 'AntiBac Hand Sanitizer', 'Sensia Face Mask',
            'Dettolia Antiseptic', 'Handiplast Bandages', 'Throatsils Lozenges', 'ProGast Digestive Aid'
        ]
    }
    
    # Define regions
    regions = ['North', 'South', 'East', 'West', 'Central']
    
    # Create product list with categories
    products_list = []
    for category, products in categories.items():
        for product in products:
            products_list.append({
                'product_name': product,
                'category': category,
                'product_id': f"P{len(products_list):03d}"
            })
    
    # Generate date range
    start = pd.to_datetime(start_date)
    dates = [start + timedelta(weeks=i) for i in range(weeks)]
    
    # Generate sales data
    records = []
    
    for product_info in products_list:
        product_id = product_info['product_id']
        product_name = product_info['product_name']
        category = product_info['category']
        
        # Determine product lifecycle stage
        lifecycle = np.random.choice(
            ['emerging_growth', 'strong_growth', 'stable', 'slow_decline', 'sharp_decline'],
            p=[0.15, 0.20, 0.40, 0.15, 0.10]
        )
        
        # Base sales parameters per category
        category_base_sales = {
            'Personal Care': (8000, 15000),
            'Home Care': (10000, 20000),
            'Food & Beverage': (15000, 30000),
            'Baby Care': (6000, 12000),
            'Household Products': (5000, 10000),
            'Health & Wellness': (7000, 14000)
        }
        
        base_sales = random.uniform(*category_base_sales[category])
        
        for week_idx, date in enumerate(dates):
            for region in regions:
                # Regional multiplier
                regional_factors = {
                    'North': random.uniform(0.9, 1.1),
                    'South': random.uniform(0.85, 1.15),
                    'East': random.uniform(0.95, 1.05),
                    'West': random.uniform(0.9, 1.2),
                    'Central': random.uniform(0.95, 1.1)
                }
                regional_mult = regional_factors[region]
                
                # Seasonal pattern (stronger in certain months)
                month = date.month
                seasonal_mult = 1.0
                if category in ['Personal Care', 'Home Care']:
                    # Peak during holiday seasons
                    if month in [11, 12, 6, 7]:
                        seasonal_mult = 1.15
                elif category == 'Food & Beverage':
                    # Peak during holidays and summer
                    if month in [12, 1, 6, 7, 8]:
                        seasonal_mult = 1.2
                elif category == 'Baby Care':
                    # More stable, slight peaks
                    if month in [3, 4, 9, 10]:
                        seasonal_mult = 1.08
                
                # Lifecycle trend
                time_progress = week_idx / weeks
                if lifecycle == 'emerging_growth':
                    # Start low, accelerate growth
                    trend_mult = 0.6 + (0.8 * time_progress) + (0.5 * time_progress**2)
                elif lifecycle == 'strong_growth':
                    # Steady growth
                    trend_mult = 0.8 + (0.6 * time_progress)
                elif lifecycle == 'stable':
                    # Slight growth or flat
                    trend_mult = 1.0 + (0.1 * np.sin(time_progress * np.pi))
                elif lifecycle == 'slow_decline':
                    # Gradual decline
                    trend_mult = 1.1 - (0.3 * time_progress)
                else:  # sharp_decline
                    # Accelerating decline
                    trend_mult = 1.2 - (0.5 * time_progress) - (0.3 * time_progress**2)
                
                # Add promotional spikes (10% chance each week)
                promo_mult = 1.0
                if random.random() < 0.10:
                    promo_mult = random.uniform(1.3, 1.8)
                
                # Add random volatility
                volatility = random.uniform(0.85, 1.15)
                
                # Calculate final sales
                sales = base_sales * regional_mult * seasonal_mult * trend_mult * promo_mult * volatility
                sales = max(0, sales)  # Ensure non-negative
                
                # Calculate quantity (assume average price varies by category)
                avg_prices = {
                    'Personal Care': 25,
                    'Home Care': 30,
                    'Food & Beverage': 15,
                    'Baby Care': 35,
                    'Household Products': 20,
                    'Health & Wellness': 40
                }
                quantity = int(sales / avg_prices[category])
                
                records.append({
                    'date': date,
                    'product_id': product_id,
                    'product_name': product_name,
                    'category': category,
                    'region': region,
                    'sales': round(sales, 2),
                    'quantity': quantity,
                    'lifecycle_stage': lifecycle
                })
    
    # Create DataFrame
    df = pd.DataFrame(records)
    
    # Sort by date and product
    df = df.sort_values(['date', 'product_id', 'region']).reset_index(drop=True)
    
    return df


def save_data(df, filepath='data/raw/fmcg_sales_data.csv'):
    """Save generated data to CSV"""
    df.to_csv(filepath, index=False)
    print(f"Data saved to {filepath}")
    print(f"Shape: {df.shape}")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Products: {df['product_id'].nunique()}")
    print(f"Categories: {df['category'].nunique()}")
    print(f"Regions: {df['region'].nunique()}")


if __name__ == "__main__":
    # Generate and save data
    df = generate_fmcg_data()
    save_data(df)
    
    # Display summary
    print("\n" + "="*50)
    print("Data Generation Summary")
    print("="*50)
    print(f"\nTotal records: {len(df):,}")
    print(f"\nCategories:")
    print(df['category'].value_counts())
    print(f"\nSample data:")
    print(df.head(10))
