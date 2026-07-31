"""
Chocolate Sales & Revenue Dashboard
Directly loads data from 'Chocolate Sales.csv' (no file upload).
Interactive analysis of sales, revenue, and product performance.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ---------------------------- PAGE CONFIG ---------------------------------
st.set_page_config(
    page_title="Chocolate Sales Dashboard",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------- STYLING -------------------------------------
sns.set_theme(style="whitegrid")
plt.rcParams['font.size'] = 12

# ---------------------------- DATA LOADING (LOCAL FILE) -------------------
@st.cache_data
def load_data():
    """Load the chocolate sales dataset from local CSV file."""
    df = pd.read_csv('Chocolate Sales.csv')
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Convert Date to datetime (format: dd-MMM-yy)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')
    
    # Clean Amount column: remove $, commas, convert to float
    df['Amount'] = df['Amount'].astype(str).str.replace('$', '').str.replace(',', '').str.strip()
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    
    # Ensure Boxes Shipped is numeric
    df['Boxes Shipped'] = pd.to_numeric(df['Boxes Shipped'], errors='coerce')
    
    # Drop rows with missing critical values
    df = df.dropna(subset=['Date', 'Amount', 'Product', 'Country'])
    
    return df

# ---------------------------- FILTERS --------------------------------------
def apply_filters(df, date_range, countries, products):
    """Apply date, country, and product filters."""
    mask = (
        (df['Date'] >= pd.to_datetime(date_range[0])) &
        (df['Date'] <= pd.to_datetime(date_range[1])) &
        (df['Country'].isin(countries)) &
        (df['Product'].isin(products))
    )
    return df.loc[mask].copy()

# ---------------------------- KPI CARDS ------------------------------------
def display_kpis(df):
    """Show key performance indicators."""
    total_revenue = df['Amount'].sum()
    total_boxes = df['Boxes Shipped'].sum()
    avg_order_value = df['Amount'].mean()
    total_transactions = len(df)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🍫 Total Revenue", f"{total_revenue:,.2f}")
    col2.metric("📦 Total Boxes Shipped", f"{total_boxes:,.0f}")
    col3.metric("💰 Avg Order Value", f"{avg_order_value:,.2f}")
    col4.metric("🧾 Transactions", f"{total_transactions:,}")

# ---------------------------- VISUALIZATIONS -------------------------------
def plot_revenue_trend(df, freq='M'):
    """Line chart: revenue over time."""
    if df.empty:
        return None
    if freq == 'D':
        trend = df.groupby(df['Date'].dt.date)['Amount'].sum()
        xlabel = "Date"
    elif freq == 'W':
        trend = df.groupby(df['Date'].dt.to_period('W').dt.start_time)['Amount'].sum()
        xlabel = "Week"
    else:
        trend = df.groupby(df['Date'].dt.to_period('M').dt.start_time)['Amount'].sum()
        xlabel = "Month"
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(trend.index, trend.values, marker='o', linestyle='-', color='#8B4513', linewidth=2)
    ax.fill_between(trend.index, trend.values, alpha=0.2, color='#D2691E')
    ax.set_title("Revenue Trend Over Time", fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Revenue (USD)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_top_products(df, top_n=10):
    """Horizontal bar chart: top products by revenue."""
    if df.empty:
        return None
    product_rev = df.groupby('Product')['Amount'].sum().sort_values(ascending=False).head(top_n)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(product_rev.index[::-1], product_rev.values[::-1], color='#A0522D')
    ax.set_title(f"Top {top_n} Products by Revenue", fontsize=14, fontweight='bold')
    ax.set_xlabel("Total Revenue (USD)")
    ax.bar_label(bars, fmt='{:,.0f}', padding=3)
    plt.tight_layout()
    return fig

def plot_sales_by_country(df):
    """Bar chart: revenue by country."""
    if df.empty:
        return None
    country_rev = df.groupby('Country')['Amount'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=country_rev.index, y=country_rev.values, palette='Oranges_r', ax=ax)
    ax.set_title("Revenue by Country", fontsize=14, fontweight='bold')
    ax.set_xlabel("Country")
    ax.set_ylabel("Revenue (USD)")
    ax.bar_label(ax.containers[0], fmt='{:,.0f}', rotation=45)
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig

def plot_boxes_vs_revenue(df):
    """Scatter plot: Boxes Shipped vs Revenue."""
    if df.empty:
        return None
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='Boxes Shipped', y='Amount', hue='Product', legend=False, alpha=0.6, ax=ax)
    ax.set_title("Boxes Shipped vs Revenue", fontsize=14)
    ax.set_xlabel("Boxes Shipped")
    ax.set_ylabel("Revenue")
    plt.tight_layout()
    return fig

# ---------------------------- INSIGHTS -------------------------------------
def generate_insights(df):
    """Generate textual business insights."""
    if df.empty:
        return "No data available for the selected filters."
    
    total_rev = df['Amount'].sum()
    top_product = df.groupby('Product')['Amount'].sum().idxmax()
    top_product_rev = df.groupby('Product')['Amount'].sum().max()
    best_country = df.groupby('Country')['Amount'].sum().idxmax()
    avg_boxes = df['Boxes Shipped'].mean()
    
    insights = f"""
    **🔍 Key Business Insights**
    - **Total Revenue**: {total_rev:,.2f}
    - **Best Selling Product**: {top_product} with {top_product_rev:,.2f}
    - **Top Performing Country**: {best_country}
    - **Average Boxes per Order**: {avg_boxes:.1f}
    - **Recommendation**: Focus marketing campaigns on {top_product} in {best_country} to maximize ROI.
    """
    return insights

# ---------------------------- MAIN DASHBOARD ------------------------------
def main():
    st.title("🍫 Chocolate Sales & Revenue Analytics Dashboard")
    st.markdown("Analyze sales performance, revenue trends, and product insights with interactive filters.")
    
    # Load data directly from local file
    df_raw = load_data()
    
    # Sidebar: Filters
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 Filters (Slicers)")
    
    # Date range
    min_date = df_raw['Date'].min().date()
    max_date = df_raw['Date'].max().date()
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    if len(date_range) == 1:
        date_range = (date_range[0], max_date)
    
    # Country multiselect
    all_countries = sorted(df_raw['Country'].unique())
    selected_countries = st.sidebar.multiselect(
        "Country", options=all_countries, default=all_countries
    )
    if not selected_countries:
        selected_countries = all_countries
    
    # Product multiselect
    all_products = sorted(df_raw['Product'].unique())
    selected_products = st.sidebar.multiselect(
        "Product", options=all_products, default=all_products[:5]
    )
    if not selected_products:
        selected_products = all_products
    
    # Time aggregation for trend
    time_freq = st.sidebar.radio("Revenue Trend Aggregation", ['Monthly (M)', 'Weekly (W)', 'Daily (D)'], index=0)
    freq_map = {'Monthly (M)': 'M', 'Weekly (W)': 'W', 'Daily (D)': 'D'}
    
    # Apply filters
    filtered_df = apply_filters(df_raw, date_range, selected_countries, selected_products)
    
    # KPIs
    st.subheader("📈 Key Performance Indicators")
    display_kpis(filtered_df)
    
    # Charts in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📉 Revenue Trend")
        fig_trend = plot_revenue_trend(filtered_df, freq=freq_map[time_freq])
        if fig_trend:
            st.pyplot(fig_trend)
            plt.close(fig_trend)
    with col2:
        st.subheader("🏆 Top Products")
        fig_top = plot_top_products(filtered_df, top_n=8)
        if fig_top:
            st.pyplot(fig_top)
            plt.close(fig_top)
    
    # Second row: two charts
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("🌍 Revenue by Country")
        fig_country = plot_sales_by_country(filtered_df)
        if fig_country:
            st.pyplot(fig_country)
            plt.close(fig_country)
    with col4:
        st.subheader("📦 Boxes vs Revenue")
        fig_scatter = plot_boxes_vs_revenue(filtered_df)
        if fig_scatter:
            st.pyplot(fig_scatter)
            plt.close(fig_scatter)
    
    # Data table & download
    with st.expander("🔎 View Filtered Data"):
        st.dataframe(filtered_df, use_container_width=True)
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_data,
            file_name="filtered_chocolate_sales.csv",
            mime="text/csv"
        )
    
    # Business insights
    st.markdown("---")
    st.subheader("💡 Automated Business Insights")
    insights = generate_insights(filtered_df)
    st.markdown(insights)
    
    st.markdown("---")
    st.caption("Built with 🍫 using Streamlit, Pandas, Matplotlib, Seaborn | Interactive Sales Dashboard")

if __name__ == "__main__":
    main()