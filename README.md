**PyData Sri Lanka - UniConnect 2025 Case Study**

This project presents a comprehensive data analysis of wine brands from different countries. The aim was to prepare and clean data, derive insights, classify wine reviews using a Hugging Face NLP model, and visualize findings through an interactive dashboard.

The data consists of:
- 8 CSV files under `Wine_Stats/` — each representing a country's wine dataset.
- `wine_reviews.csv` — 500 customer reviews for *Merry Edwards Sauvignon Blanc 2023*.

Key features:
- `Name`, `Rating`, `Number of Ratings`, `Price`, `Region`, `Winery`, `Wine style`, `Alcohol content`, `Grapes`, `Food pairings`, `Bold`, `Tannin`, `Sweet`, `Acidic`.

Data Preparation
- Combined all 8 CSVs into a single DataFrame `wine_df`
- Cleaned nulls, removed duplicates
- Extracted:
  - `Country` and `Country_region` from `Region`
  - Expanded `Food pairings` into 21 binary columns (e.g., `Beef`, `Lamb`, `Pasta`)
- Removed irrelevant columns with reasoning

NLP with Hugging Face
- Used zero-shot classification to analyze 500 customer reviews
- Selected a suitable Hugging Face model with justification(facebook/bart-large-mnli)
- Labeled each review under:
  - Talks about food combinations
  - Talks about taste
  - Talks about value for money
  - Other
- Added classification as a new column `talks_about`
- Visualized category distribution using a chart

Dashboard Creation
- Developed an interactive dashboard using **Plotly Dash**
- Included multiple chart types (bar, line, pie, scatter, heatmap)
- Enabled interactive filters for dynamic storytelling
- Highlighted insights on wine preferences, pricing, food pairings, and regions

Tools & Technologies Used
- **Python** (Pandas, NumPy, Matplotlib, Seaborn, Plotly, Dash)
- **Hugging Face Transformers** (Zero-shot Classification)
- **Jupyter Notebook**
- **Git & GitHub**
