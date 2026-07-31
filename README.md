# 🍫 Chocolate Sales & Revenue Dashboard
# Thiranex Data Analytics Internship Third Project

An interactive data analytics dashboard built with **Streamlit**, **Pandas**, **Matplotlib**, and **Seaborn** to analyze chocolate sales data. The dashboard directly loads the dataset from `Chocolate Sales.csv` (no file upload required) and provides dynamic filters, KPIs, and visual insights.

![Dashboard Preview][http://localhost:8501/]
*(Replace with an actual screenshot of your running dashboard)*

## 📊 Key Features

- **Local Data Loading** – Reads `Chocolate Sales.csv` from the same folder as the script.
- **Key Performance Indicators (KPIs)** – Total revenue, total boxes shipped, average order value, transaction count.
- **Revenue Trend** – Interactive line chart with daily, weekly, or monthly aggregation.
- **Top Products** – Horizontal bar chart of best‑selling products by revenue.
- **Revenue by Country** – Bar chart of total sales per country.
- **Boxes vs Revenue** – Scatter plot to identify high‑value shipments.
- **Interactive Filters (Slicers)** – Filter by date range, country (multi‑select), product (multi‑select).
- **Data Export** – Download the filtered dataset as a CSV file.
- **Automated Insights** – Textual business recommendations based on current filters.

## 🛠️ Tech Stack

- **Python** 3.8+
- **Streamlit** – Dashboard framework
- **Pandas** – Data manipulation
- **NumPy** – Numerical operations
- **Matplotlib** & **Seaborn** – Visualization
