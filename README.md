# Market Shift Detector

## Early Trend Intelligence Dashboard for FMCG

Market Shift Detector is a data analytics and AI-assisted dashboard designed to identify early market movement signals in FMCG products before they become obvious in standard sales reports. Instead of only forecasting future sales, this project focuses on detecting subtle shifts in consumer demand, category momentum, product acceleration, and potential market changes.

This project is built as a portfolio project for demonstrating business-oriented data analytics, AI application development, and decision support system thinking.

---

## 🚀 Quick Start

### Installation

1. **Clone or download this repository**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Generate initial data** (if not already present)
```bash
python src/data_generator.py
```

4. **Run the dashboard**
```bash
streamlit run app.py
```

5. **Open in browser**
The dashboard will automatically open at `http://localhost:8501`

### Requirements
- Python 3.8+
- Dependencies: streamlit, pandas, numpy, plotly, scikit-learn, openpyxl

---

## 📊 Dashboard Features

The dashboard consists of 5 main pages:

1. **📊 Executive Overview** - High-level KPIs, signal distribution, and top movers
2. **🔍 Early Signal Monitor** - Filterable product table with market shift signals
3. **🔬 Product Deep Dive** - Detailed analysis of individual products with trends
4. **🌍 Category & Region Analysis** - Comparative analysis across categories and regions
5. **📚 Methodology** - Explanation of the Market Shift Score and approach

---

## 1. Project Background

In FMCG businesses, companies need to respond quickly to changes in consumer behavior. A product category may start gaining traction before it becomes clearly visible in monthly reports. A competitor product may slowly gain market share. A previously stable product may begin declining due to changing preferences, pricing pressure, or reduced promotional effectiveness.

Most beginner data projects focus only on historical dashboarding or simple sales forecasting. This project takes a more strategic approach by answering:

> “Can we detect early signs of market change before the shift becomes obvious?”

The goal is to build a dashboard that helps business teams monitor weak signals, trend changes, and early demand shifts across products, categories, brands, and regions.

---

## 2. Main Objective

The main objective of this project is to develop an interactive dashboard that can:

1. Analyze historical sales and demand patterns.
2. Detect early signals of product or category growth.
3. Identify products with declining momentum.
4. Compare market movement across categories, brands, and regions.
5. Generate a Market Shift Score to rank products or categories based on trend movement.
6. Provide business-friendly insights that can support marketing, sales, and supply chain decisions.

---

## 3. Business Use Case

This project is designed for FMCG-related business problems such as:

* Identifying products that may become future growth drivers.
* Detecting products that are starting to lose demand.
* Monitoring category-level demand shifts.
* Supporting marketing teams in campaign planning.
* Supporting sales teams in regional product prioritization.
* Supporting supply chain teams in preparing inventory before demand changes become large.

Example business questions:

* Which product categories are gaining momentum?
* Which products show early signs of demand decline?
* Are there specific regions where product demand is shifting?
* Which products show abnormal acceleration in sales?
* Which categories should receive more marketing attention?
* Which products may need inventory adjustment?

---

## 4. Target Users

This dashboard is designed for:

* FMCG Business Analyst
* Data Analyst
* Marketing Analyst
* Sales Strategy Team
* Supply Chain Planning Team
* Category Management Team
* Management Trainee Candidate Portfolio

---

## 5. Key Features

### 5.1 Market Overview Dashboard

The dashboard should show high-level business metrics such as:

* Total sales
* Total units sold
* Number of active products
* Number of categories
* Best performing category
* Fastest growing category
* Products with strongest positive shift
* Products with strongest negative shift

Visualizations:

* Sales trend over time
* Category contribution chart
* Regional sales distribution
* Top products by revenue
* Top products by volume

---

### 5.2 Market Shift Detection

This is the core feature of the project.

The system should detect early market shifts by calculating indicators such as:

* Sales growth rate
* Rolling average trend
* Sales momentum
* Trend acceleration
* Category share movement
* Product rank movement
* Volatility change
* Demand consistency
* Sudden increase or decrease in product performance

The result should be summarized into a single metric called:

## Market Shift Score

The Market Shift Score should help rank products or categories based on how strongly their market behavior is changing.

Example interpretation:

| Score Range | Meaning                      |
| ----------- | ---------------------------- |
| 80–100      | Strong positive market shift |
| 60–79       | Moderate positive shift      |
| 40–59       | Stable or neutral            |
| 20–39       | Early warning decline        |
| 0–19        | Strong negative shift        |

---

### 5.3 Early Signal Ranking

The dashboard should display a ranked list of products or categories based on their Market Shift Score.

Recommended table columns:

* Product name
* Category
* Region
* Current sales
* Previous period sales
* Growth rate
* Momentum score
* Acceleration score
* Market Shift Score
* Signal type

Signal types:

* Emerging Growth
* Stable Performer
* Declining Momentum
* High Volatility
* Potential Demand Spike
* Potential Demand Drop

---

### 5.4 Product and Category Deep Dive

Users should be able to select a product or category and view:

* Historical sales trend
* Rolling average trend
* Growth rate over time
* Sales contribution to category
* Rank movement over time
* Comparison with category average
* Detected shift signal explanation

Example insight:

> Product A shows early positive market movement with a 21% increase in rolling 4-week sales and a consistent rank improvement within its category. This may indicate growing consumer demand and potential opportunity for increased marketing support.

---

### 5.5 Regional Market Shift Analysis

If the dataset contains regional data, the system should allow users to compare market shifts across regions.

Possible analysis:

* Which regions are growing fastest?
* Which regions show declining demand?
* Which product category is gaining momentum in each region?
* Are there regional differences in consumer preference?

Visualizations:

* Region heatmap
* Regional trend line
* Product-category-region matrix
* Top growing products by region

---

### 5.6 Business Insight Generator

The dashboard should generate simple business insights automatically using rule-based logic.

Example insight templates:

* “This product shows early growth because its rolling sales increased by X% compared to the previous period.”
* “This category may require attention because its market share decreased for X consecutive periods.”
* “This region shows stronger demand acceleration than the national average.”
* “This product is volatile and should be monitored before making inventory decisions.”

The insight generator should not overclaim. It should use cautious wording such as:

* may indicate
* shows early signal
* should be monitored
* could suggest
* requires further validation

---

## 6. Dataset Requirements

The project should support a public retail or FMCG-like dataset.

Minimum required columns:

| Column       | Description               |
| ------------ | ------------------------- |
| date         | Transaction or sales date |
| product_id   | Unique product identifier |
| product_name | Product name              |
| category     | Product category          |
| sales        | Revenue or sales value    |
| quantity     | Number of units sold      |

Optional columns:

| Column      | Description                                               |
| ----------- | --------------------------------------------------------- |
| brand       | Product brand                                             |
| region      | Sales region                                              |
| store_id    | Store identifier                                          |
| price       | Product price                                             |
| promotion   | Promotion status                                          |
| customer_id | Customer identifier                                       |
| channel     | Sales channel such as online, offline, modern trade, etc. |

If the dataset does not contain FMCG-specific products, create a clean simulated FMCG product mapping such as:

* Personal Care
* Home Care
* Food & Beverage
* Baby Care
* Household Products
* Tobacco Alternative Category if relevant for business simulation

---

## 7. Suggested Dataset Options

The agent may use one of the following dataset types:

1. Retail transaction dataset
2. Supermarket sales dataset
3. Online retail dataset
4. FMCG sales dataset
5. Synthetic FMCG dataset generated from realistic business assumptions

If no suitable dataset is available, create a synthetic dataset with the following structure:

* 24 months of weekly sales data
* 50–100 products
* 5–8 categories
* 4–8 regions
* Seasonal demand patterns
* Random promotional spikes
* Gradual product growth
* Gradual product decline
* Sudden demand shifts
* Stable products for comparison

The synthetic dataset should be realistic enough to demonstrate the dashboard concept.

---

## 8. Methodology

### 8.1 Data Cleaning

The system should:

* Convert date columns into datetime format.
* Handle missing values.
* Remove duplicate records.
* Standardize product and category names.
* Aggregate sales by date, product, category, and region.
* Create weekly or monthly time periods.

Recommended aggregation level:

* Weekly data for more detailed movement detection.
* Monthly data for simpler business summary.

---

### 8.2 Feature Engineering

Create the following features:

#### Growth Features

* Current period sales
* Previous period sales
* Sales growth rate
* Quantity growth rate

Formula example:

```text
growth_rate = (current_sales - previous_sales) / previous_sales
```

#### Rolling Features

* Rolling 4-week sales average
* Rolling 8-week sales average
* Rolling standard deviation
* Rolling market share

#### Momentum Features

Momentum measures whether product performance is improving or weakening.

Example:

```text
momentum = rolling_4_week_avg - rolling_8_week_avg
```

Positive momentum means short-term sales are stronger than longer-term average.

#### Acceleration Features

Acceleration measures whether growth is getting faster.

Example:

```text
acceleration = current_growth_rate - previous_growth_rate
```

#### Market Share Features

Calculate product or category share within total sales.

Example:

```text
market_share = product_sales / total_category_sales
```

Track whether product share is increasing or decreasing over time.

#### Rank Movement Features

Track product ranking within category over time.

Example:

* Current rank
* Previous rank
* Rank change
* Rank improvement flag

---

## 9. Market Shift Score Design

The Market Shift Score should combine several indicators into one score.

Recommended components:

| Component                   | Weight |
| --------------------------- | ------ |
| Growth rate score           | 30%    |
| Momentum score              | 25%    |
| Acceleration score          | 20%    |
| Market share movement score | 15%    |
| Rank improvement score      | 10%    |

Example formula:

```text
Market Shift Score =
0.30 * Growth Score +
0.25 * Momentum Score +
0.20 * Acceleration Score +
0.15 * Market Share Movement Score +
0.10 * Rank Improvement Score
```

Each component should be normalized to a 0–100 scale.

The final score should also be between 0 and 100.

Important:

* Avoid making the score overly complex.
* Prioritize interpretability.
* Make the scoring logic easy to explain in the README and dashboard.

---

## 10. Signal Classification Logic

After calculating the Market Shift Score, classify each product or category.

Example logic:

```text
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
```

Add volatility-based warning:

```text
if volatility is high:
    add label = "High Volatility"
```

---

## 11. Dashboard Requirements

The project should use Streamlit.

Recommended pages or sections:

### Page 1: Executive Overview

Show:

* Key metrics
* Top growing categories
* Top declining categories
* Market Shift Score distribution
* Overall market trend

### Page 2: Early Signal Monitor

Show:

* Ranked product table
* Filters by category, region, and time period
* Signal type filter
* Market Shift Score chart

### Page 3: Product Deep Dive

Show:

* Product sales trend
* Rolling average
* Growth rate
* Momentum and acceleration
* Business insight explanation

### Page 4: Category and Region Analysis

Show:

* Category comparison
* Region comparison
* Heatmap of market shift by region and category

### Page 5: Methodology

Explain:

* Dataset used
* Feature engineering process
* Market Shift Score logic
* Limitations

---

## 12. Recommended Tech Stack

Use the following technology:

* Python
* Pandas
* NumPy
* Streamlit
* Plotly
* Scikit-learn
* Matplotlib optional
* Seaborn optional

Optional advanced packages:

* ruptures for change point detection
* prophet for forecasting comparison
* statsmodels for trend analysis

However, the MVP should not depend on too many advanced packages.

---

## 13. Project Folder Structure

Recommended structure:

```text
market-shift-detector/
│
├── app.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   ├── scoring.py
│   ├── insights.py
│   └── visualization.py
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── assets/
│   ├── screenshots/
│   └── dashboard_preview.png
│
└── docs/
    └── methodology.md
```

---

## 14. Minimum Viable Product

The first version should include:

* Data loading
* Data cleaning
* Weekly or monthly aggregation
* Growth rate calculation
* Rolling average calculation
* Momentum calculation
* Market Shift Score
* Signal classification
* Streamlit dashboard
* Product/category filter
* Ranked signal table
* Basic business insights

---

## 15. Advanced Version

After the MVP is complete, improve the project with:

* Change point detection
* Forecasting comparison
* Region-level market shift
* Promotion impact analysis
* External signal integration such as Google Trends or social media trend data
* AI-generated summary using LLM
* PDF report export
* Automated weekly insight generation

---

## 16. Example Dashboard Insight

The dashboard should be able to generate insights like:

```text
Product: Shampoo A
Category: Personal Care
Signal: Emerging Growth
Market Shift Score: 84/100

Insight:
Shampoo A shows an early positive market shift. Its rolling 4-week sales increased by 18.5% compared to the previous period, while its category rank improved from 8th to 4th. This may indicate growing consumer demand and should be monitored for potential marketing or inventory planning.
```

Another example:

```text
Product: Detergent B
Category: Home Care
Signal: Declining Momentum
Market Shift Score: 28/100

Insight:
Detergent B shows early signs of weakening demand. Its sales growth has declined for three consecutive periods, and its market share within the Home Care category has decreased. Further investigation may be needed to understand whether this is caused by pricing, promotion, competition, or seasonal demand changes.
```

---

## 17. Success Criteria

The project is considered successful if:

* The dashboard can clearly identify top positive and negative market shifts.
* The Market Shift Score is interpretable.
* The user can filter results by category, product, region, and time period.
* The dashboard provides business-friendly explanations.
* The project can be explained easily in an interview.
* The README clearly communicates the business value, methodology, and technical approach.

---

## 18. Expected Business Value

This project should demonstrate the ability to:

* Move beyond descriptive analytics.
* Detect early market signals.
* Convert raw data into business insights.
* Build interactive decision-support tools.
* Think from both technical and business perspectives.

The project is especially relevant for FMCG companies because it connects data analytics with real business problems such as demand movement, category growth, product decline, marketing focus, and inventory planning.

---

## 19. Limitations

The dashboard should clearly state the following limitations:

* The Market Shift Score is a proxy indicator, not a guaranteed prediction.
* The result depends heavily on dataset quality.
* External factors such as competitor activity, pricing strategy, macroeconomic conditions, and distribution changes may not be fully captured.
* Further validation with real business stakeholders would be required before using the system for actual decision-making.

---

## 20. Suggested GitHub Repository Description

Early trend intelligence dashboard for detecting market shifts in FMCG sales using Python, Streamlit, rolling analytics, momentum scoring, and business insight generation.

---

## 21. Suggested CV Description

Market Shift Detector (2026) | Python, Streamlit, Pandas, Plotly
Developed an early trend intelligence dashboard for FMCG sales analysis. The system detects product and category market shifts using rolling trends, momentum indicators, acceleration analysis, and a custom Market Shift Score to support business decision-making.

---

## 22. Development Instructions for AI Agent

The AI agent should build this project step by step:

1. Create the project folder structure.
2. Prepare or generate a suitable FMCG-like dataset.
3. Build the data preprocessing pipeline.
4. Create feature engineering functions.
5. Build Market Shift Score logic.
6. Create signal classification logic.
7. Build business insight generator.
8. Build Streamlit dashboard.
9. Add charts and filters.
10. Add documentation and methodology explanation.
11. Create requirements.txt.
12. Ensure the project can run locally with:

```bash
streamlit run app.py
```

The final output should be a complete GitHub-ready project with clean code, clear README, and a functional dashboard.

---

## 23. Final Project Positioning

This project is not just a sales dashboard.

It is designed as a strategic analytics system that helps detect early changes in market behavior. The project shows the ability to combine data analysis, business understanding, AI-assisted thinking, and dashboard development into one practical decision-support tool.

The main value of this project is:

> Helping businesses detect market movement earlier, respond faster, and make more data-driven decisions.
