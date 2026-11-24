import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Global Superstore | Sales & Profit",
    page_icon="📊",
    layout="wide",
)

DATA_FILE = Path(__file__).parent / "Global Superstore.xlsx"

@st.cache_data
def load_data():
    orders = pd.read_excel(DATA_FILE, sheet_name="Orders")
    returns = pd.read_excel(DATA_FILE, sheet_name="Returns")
    people = pd.read_excel(DATA_FILE, sheet_name="People")

    orders["Order Date"] = pd.to_datetime(orders["Order Date"], errors="coerce")
    orders["Ship Date"] = pd.to_datetime(orders["Ship Date"], errors="coerce")
    orders["Year"] = orders["Order Date"].dt.year
    orders["Month"] = orders["Order Date"].dt.to_period("M").astype(str)

    returned_ids = set(returns["Order ID"].dropna().astype(str))
    orders["Returned"] = orders["Order ID"].astype(str).isin(returned_ids)

    # Add regional manager where the region names match the People sheet.
    orders = orders.merge(people, on="Region", how="left")
    return orders, returns, people

try:
    df, returns_df, people_df = load_data()
except Exception as exc:
    st.error("Dataset tidak berhasil dibaca. Pastikan file 'Global Superstore.xlsx' berada satu folder dengan app.py.")
    st.exception(exc)
    st.stop()

st.title("🌎 Global Superstore")
st.subheader("Sales & Profit Analysis Dashboard")
st.caption("Analisis transaksi, keuntungan, kategori produk, dan persebaran penjualan.")

# Sidebar filters
st.sidebar.header("🔎 Filter Data")
years = sorted(df["Year"].dropna().astype(int).unique().tolist())
markets = sorted(df["Market"].dropna().astype(str).unique().tolist())
segments = sorted(df["Segment"].dropna().astype(str).unique().tolist())
categories = sorted(df["Category"].dropna().astype(str).unique().tolist())

selected_years = st.sidebar.multiselect("Tahun", years, default=years)
selected_markets = st.sidebar.multiselect("Market", markets, default=markets)
selected_segments = st.sidebar.multiselect("Segment", segments, default=segments)
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)

filtered = df[
    df["Year"].isin(selected_years)
    & df["Market"].isin(selected_markets)
    & df["Segment"].isin(selected_segments)
    & df["Category"].isin(selected_categories)
].copy()

if filtered.empty:
    st.warning("Tidak ada data untuk kombinasi filter ini. Silakan ubah filter di sebelah kiri.")
    st.stop()

sales = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
quantity = filtered["Quantity"].sum()
orders = filtered["Order ID"].nunique()
returned_orders = filtered.loc[filtered["Returned"], "Order ID"].nunique()
return_rate = returned_orders / orders * 100 if orders else 0
profit_margin = profit / sales * 100 if sales else 0

def money(value):
    return f"${value:,.2f}"

# Dashboard overview
st.markdown("## Dashboard — Global Sales Overview")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Sales", money(sales))
k2.metric("Total Profit", money(profit))
k3.metric("Quantity Sold", f"{quantity:,.0f}")
k4.metric("Unique Orders", f"{orders:,.0f}")

k5, k6 = st.columns(2)
k5.metric("Profit Margin", f"{profit_margin:.2f}%")
k6.metric("Returned Orders", f"{returned_orders:,.0f}", f"{return_rate:.2f}% dari order")

left, right = st.columns(2)
with left:
    cat_summary = filtered.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    fig = px.bar(cat_summary, x="Category", y="Sales", color="Category",
                 title="Sales by Category", labels={"Sales": "Sales (USD)"})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
with right:
    market_summary = filtered.groupby("Market", as_index=False)["Profit"].sum().sort_values("Profit", ascending=False)
    fig = px.bar(market_summary, x="Market", y="Profit", color="Market",
                 title="Profit by Market", labels={"Profit": "Profit (USD)"})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("## 3 Worksheets")
tab1, tab2, tab3 = st.tabs([
    "Worksheet 1 · Sales Trend",
    "Worksheet 2 · Profit by Category",
    "Worksheet 3 · Sales by Country",
])

with tab1:
    st.markdown("### Worksheet 1 — Sales Trend")
    trend = filtered.groupby("Month", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    trend = trend.sort_values("Month")
    fig = px.line(trend, x="Month", y="Sales", markers=True,
                  title="Monthly Sales Trend", labels={"Month": "Month", "Sales": "Sales (USD)"})
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Gunakan filter Tahun, Market, Segment, dan Category untuk melihat perubahan tren.")

with tab2:
    st.markdown("### Worksheet 2 — Profit by Category")
    category_profit = filtered.groupby("Category", as_index=False).agg(
        Profit=("Profit", "sum"), Sales=("Sales", "sum")
    ).sort_values("Profit", ascending=False)
    fig = px.bar(category_profit, x="Category", y="Profit", color="Category",
                 title="Total Profit by Product Category", labels={"Profit": "Profit (USD)"})
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(category_profit, use_container_width=True, hide_index=True)

with tab3:
    st.markdown("### Worksheet 3 — Sales by Country")
    country_sales = filtered.groupby("Country", as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique")
    ).sort_values("Sales", ascending=False).head(20)
    fig = px.bar(country_sales.sort_values("Sales"), x="Sales", y="Country",
                 orientation="h", color="Sales", title="Top 20 Countries by Sales",
                 labels={"Sales": "Sales (USD)"})
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(country_sales, use_container_width=True, hide_index=True)

st.divider()
st.markdown("## 2 Stories")

story1, story2 = st.tabs([
    "Story 1 · Sales Performance",
    "Story 2 · Profitability Analysis",
])

with story1:
    st.markdown("### Story 1 — Sales Performance Analysis")
    best_category = filtered.groupby("Category")["Sales"].sum().idxmax()
    best_market = filtered.groupby("Market")["Sales"].sum().idxmax()
    monthly = filtered.groupby("Month")["Sales"].sum()
    best_month = monthly.idxmax() if not monthly.empty else "N/A"
    st.write(
        f"Dalam data sesuai filter, kategori dengan penjualan tertinggi adalah **{best_category}**. "
        f"Market dengan penjualan tertinggi adalah **{best_market}**, sedangkan bulan dengan "
        f"penjualan tertinggi adalah **{best_month}**."
    )
    st.plotly_chart(
        px.line(filtered.groupby("Month", as_index=False)["Sales"].sum().sort_values("Month"),
                x="Month", y="Sales", markers=True, title="Story: Perkembangan Penjualan"),
        use_container_width=True,
    )
    st.info("Interpretasi: amati periode kenaikan dan penurunan penjualan, lalu bandingkan performa antar-market dan kategori.")

with story2:
    st.markdown("### Story 2 — Profitability Analysis")
    profit_by_cat = filtered.groupby("Category")["Profit"].sum().sort_values(ascending=False)
    best_profit_category = profit_by_cat.index[0]
    lowest_profit_category = profit_by_cat.index[-1]
    loss_rows = int((filtered["Profit"] < 0).sum())
    st.write(
        f"Kategori dengan total profit tertinggi adalah **{best_profit_category}**, sementara "
        f"kategori dengan total profit terendah adalah **{lowest_profit_category}**. "
        f"Terdapat **{loss_rows:,} baris transaksi** dengan profit negatif pada data terfilter."
    )
    st.plotly_chart(
        px.bar(profit_by_cat.rename_axis("Category").reset_index(name="Profit"),
               x="Category", y="Profit", color="Profit", title="Story: Perbandingan Profit Kategori"),
        use_container_width=True,
    )
    st.info("Interpretasi: penjualan tinggi tidak selalu berarti profit tinggi. Perhatikan kategori dengan profit rendah atau negatif.")

with st.expander("Lihat ringkasan data terfilter"):
    st.write(f"Jumlah baris: **{len(filtered):,}**")
    st.write(f"Jumlah negara: **{filtered['Country'].nunique():,}**")
    st.write(f"Jumlah pelanggan: **{filtered['Customer ID'].nunique():,}**")
    st.dataframe(filtered.head(100), use_container_width=True, hide_index=True)
    st.caption("Pratinjau dibatasi 100 baris agar tetap ringan di HP.")

st.caption("Sumber data: Global Superstore.xlsx (sheet Orders, Returns, dan People). Dibuat untuk proyek analisis data.")
