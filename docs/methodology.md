# Market Shift Detector - Technical Methodology

## Overview

The Market Shift Detector uses a combination of time series analysis, rolling statistics, and custom scoring algorithms to identify early signals of market changes in FMCG products. This document explains the technical approach in detail.

---

## Data Pipeline

### 1. Data Generation
The system uses synthetic FMCG sales data generated with realistic characteristics:

- **Time Period**: 104 weeks (24 months) of weekly sales data
- **Products**: 72 products across 6 categories
- **Regions**: 5 geographic regions
- **Lifecycle Stages**: Products are assigned lifecycle stages (emerging growth, strong growth, stable, slow decline, sharp decline)
- **Patterns**: Seasonal variations, promotional spikes, regional differences, and random volatility

### 2. Data Preprocessing
Raw data is cleaned and aggregated:
- Date standardization
- Duplicate removal
- Missing value handling
- Weekly aggregation by product-region combination

---

## Feature Engineering

### Growth Features
```python
growth_rate = (current_sales - previous_sales) / previous_sales
```

Captures period-over-period percentage change in sales.

### Rolling Features
```python
rolling_4w_avg = sales.rolling(window=4).mean()
rolling_8w_avg = sales.rolling(window=8).mean()
rolling_std = sales.rolling(window=4).std()
```

Smooths out noise and identifies underlying trends.

### Momentum Features
```python
momentum = rolling_4w_avg - rolling_8w_avg
momentum_pct = (momentum / rolling_8w_avg) × 100
```

Positive momentum indicates short-term performance exceeds long-term average.

### Acceleration Features
```python
acceleration = current_growth_rate - previous_growth_rate
```

Measures whether growth is speeding up (positive) or slowing down (negative).

### Market Share Features
```python
category_share = (product_sales / total_category_sales) × 100
share_change = current_share - previous_share
```

Tracks competitive positioning within category.

### Ranking Features
Products are ranked by sales within their category each period. Rank changes indicate competitive shifts.

### Volatility Features
```python
cv = rolling_std / rolling_mean
high_volatility = (cv > 0.3)
```

Coefficient of variation identifies unstable products requiring cautious interpretation.

---

## Market Shift Score Algorithm

### Component Scoring

Each component is normalized to 0-100 scale using capped ranges:

**Growth Score**
```
growth_capped = clip(growth_rate, -1.0, 3.0)  # -100% to +300%
growth_score = ((growth_capped + 1) / 4) × 100
```

**Momentum Score**
```
momentum_capped = clip(momentum_pct, -50, 50)
momentum_score = ((momentum_capped + 50) / 100) × 100
```

**Acceleration Score**
```
accel_capped = clip(acceleration, -1.0, 1.0)
acceleration_score = ((accel_capped + 1) / 2) × 100
```

**Market Share Score**
```
share_change_capped = clip(share_change, -10, 10)  # -10pp to +10pp
market_share_score = ((share_change_capped + 10) / 20) × 100
```

**Rank Score**
```
rank_change_capped = clip(rank_change, -10, 10)
rank_score = ((-rank_change_capped + 10) / 20) × 100  # Inverted
```

### Weighted Combination

```python
market_shift_score = (
    0.30 × growth_score +
    0.25 × momentum_score +
    0.20 × acceleration_score +
    0.15 × market_share_score +
    0.10 × rank_score
)
```

Final score is clipped to [0, 100] range.

---

## Signal Classification Logic

```python
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

if high_volatility:
    signal += " (High Volatility)"
```

---

## Insight Generation

The system uses rule-based templates to generate business-friendly insights:

1. **Product Insights**: Combine score interpretation, growth metrics, momentum trends, and rank changes
2. **Category Insights**: Aggregate product signals and identify category-level patterns
3. **Regional Insights**: Compare regional performance and highlight geographic differences
4. **Executive Summary**: High-level overview of market movements

All insights use cautious language:
- "may indicate"
- "shows early signal"
- "should be monitored"
- "requires further validation"

---

## Visualization Approach

All charts use Plotly for interactivity:

- **Time Series**: Line charts with rolling averages overlay
- **Distributions**: Histograms and pie charts for signal types
- **Comparisons**: Bar charts and heatmaps for categories/regions
- **Relationships**: Scatter plots for growth vs momentum analysis
- **Breakdowns**: Waterfall charts for score components

Color scheme:
- Green (#10b981): Strong growth signals
- Blue (#3b82f6): Positive momentum
- Gray (#64748b): Stable
- Orange (#f59e0b): Declining momentum
- Red (#ef4444): Strong decline warnings

---

## Performance Optimizations

1. **Caching**: Streamlit `@st.cache_data` decorator on data loading and processing
2. **Vectorization**: NumPy/Pandas operations instead of loops
3. **Efficient Aggregation**: GroupBy operations for feature calculations
4. **Lazy Evaluation**: Features calculated only when needed

---

## Limitations and Considerations

### Technical Limitations
1. Rolling windows require minimum data points (first 8 weeks have incomplete features)
2. Rank calculations are relative within category (not absolute market position)
3. Normalization bounds are manually set based on expected ranges

### Business Limitations
1. External factors not captured (competitor actions, pricing, distribution)
2. Causation vs correlation - score shows patterns, not root causes
3. Synthetic data may not reflect real market complexity
4. Score interpretation requires business context

### Statistical Considerations
1. Serial correlation in time series not explicitly modeled
2. Seasonality adjusted through rolling averages, not decomposition
3. No confidence intervals or statistical significance tests
4. Outliers capped rather than removed

---

## Extensions and Future Work

Potential enhancements:
1. Change point detection (e.g., using PELT algorithm)
2. Forecasting integration (Prophet, ARIMA)
3. Anomaly detection (Isolation Forest)
4. Sentiment analysis from customer reviews
5. External signal integration (Google Trends, social media)
6. A/B testing framework for interventions
7. Automated alerting system
8. PDF report generation
9. Multi-level hierarchies (brand → product → SKU)
10. Bayesian updating for score confidence

---

## References

- **Time Series Analysis**: Rolling statistics, momentum indicators
- **Business Analytics**: KPI design, early warning systems
- **FMCG Domain**: Category management, demand sensing
- **Data Visualization**: Edward Tufte principles, interactive dashboards
- **Decision Support**: Interpretable AI, actionable insights

---

## Code Architecture

```
app.py
├── Data Loading (data_loader.py)
├── Preprocessing (preprocessing.py)
├── Feature Engineering (feature_engineering.py)
│   ├── Growth calculations
│   ├── Rolling statistics
│   ├── Momentum/acceleration
│   ├── Market share
│   └── Ranking
├── Scoring (scoring.py)
│   ├── Component normalization
│   ├── Weighted combination
│   └── Signal classification
├── Insights (insights.py)
│   └── Template-based generation
├── Visualization (visualization.py)
│   └── Plotly charts
└── Pages (pages/*.py)
    ├── Executive Overview
    ├── Signal Monitor
    ├── Product Deep Dive
    ├── Category & Region Analysis
    └── Methodology
```

All modules are designed to be:
- **Modular**: Each component has a single responsibility
- **Testable**: Pure functions with clear inputs/outputs
- **Scalable**: Vectorized operations for large datasets
- **Maintainable**: Clear naming, documentation, type hints

---

## Conclusion

The Market Shift Detector demonstrates how to build an end-to-end analytics system that:
1. Processes raw data into actionable intelligence
2. Combines multiple indicators into interpretable scores
3. Presents insights through an interactive dashboard
4. Maintains transparency in methodology

The system prioritizes interpretability and business relevance over algorithmic complexity, making it suitable for real-world decision support.
