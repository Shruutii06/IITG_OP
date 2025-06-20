import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Inventory Dashboard", layout="wide")
st.title("📦 Urban Retail Inventory Dashboard")
st.markdown("A unified view to monitor stock health, supply-demand gaps, and product performance.")

# ------------------ LOAD DATA ------------------
@st.cache_data

def load_data():
    return (
        pd.read_csv("InventoryHealth.csv"),
        pd.read_csv("ReorderStatus.csv"),
        pd.read_csv("TurnoverByProduct.csv"),
        pd.read_csv("Top5SKUs.csv"),
        pd.read_csv("Bottom5SKUs.csv"),
        pd.read_csv("AgingInventory.csv"),
        pd.read_csv("ChronicUnderstock.csv"),
        pd.read_csv("TurnoverByRegionCategory.csv"),
        pd.read_csv("WeatherImpact.csv"),
        pd.read_csv("SeasonalCategorySales.csv"),
        pd.read_csv("SupplyDemandGap.csv"),
    )

(inventory_health, reorder_status, turnover, top5, bottom5, aging, understock,
 turnover_region_cat, weather, seasonal, gap) = load_data()

# ------------------ KPI METRICS ------------------
st.markdown("### 🔹 Key Inventory KPIs")
k1, k2, k3, k4 = st.columns(4)

k1.metric("🔻 Below Threshold SKUs", inventory_health.query("InventoryStatus == 'Below Threshold'").shape[0])
k2.metric("🟢 Safe SKUs", inventory_health.query("InventoryStatus == 'Safe'").shape[0])
k3.metric("🔁 Reorder Now", reorder_status.query("Status == 'Reorder Now'").shape[0])
k4.metric("🪊 Aging Inventory", aging.query("DaysHighStock > 14").shape[0])

# ------------------ PERFORMANCE CHARTS ------------------
st.markdown("### 📊 Product Performance")
c1, c2 = st.columns(2)

with c1:
    st.markdown("#### 🔝 Top 5 SKUs")
    fig_top5 = px.bar(top5, x="ProductID", y="TotalSold", color="TotalSold", title="Top 5 SKUs")
    st.plotly_chart(fig_top5, use_container_width=True)

with c2:
    st.markdown("#### 🔻 Bottom 5 SKUs")
    fig_bottom5 = px.bar(bottom5, x="ProductID", y="TotalSold", color="TotalSold", title="Bottom 5 SKUs")
    st.plotly_chart(fig_bottom5, use_container_width=True)

# ------------------ INVENTORY STATUS PIE CHART ------------------
st.markdown("### 🥧 Inventory Status Distribution")
region_filter = st.selectbox("Filter by Region", ["All"] + sorted(inventory_health['Region'].unique())) if "Region" in inventory_health.columns else "All"

if region_filter != "All":
    filtered_data = inventory_health[inventory_health["Region"] == region_filter]
else:
    filtered_data = inventory_health

status_counts = filtered_data["InventoryStatus"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]
fig_status = px.pie(status_counts, names="Status", values="Count", title=f"Inventory Status Breakdown{' - ' + region_filter if region_filter != 'All' else ''}")
st.plotly_chart(fig_status, use_container_width=True)

# ------------------ EXPANDERS ------------------
with st.expander("🔀 Inventory Turnover by Region & Category"):
    st.markdown("Average inventory turnover across store regions and product categories.")
    pivot_data = turnover_region_cat.pivot(index="Region", columns="Category", values="TurnoverRatio")
    fig_tc = px.imshow(pivot_data, text_auto=True, aspect="auto", color_continuous_scale="Blues")
    st.plotly_chart(fig_tc, use_container_width=True)

with st.expander("🌦️ Weather Impact on Sales"):
    fig_weather = px.bar(weather, x="WeatherCondition", y="AvgUnitsSold", color="AvgUnitsSold",
                         title="Avg Units Sold by Weather", labels={"AvgUnitsSold": "Avg Units Sold"})
    st.plotly_chart(fig_weather, use_container_width=True)

with st.expander("🗓️ Seasonal Demand by Product Category"):
    fig_seasonal = px.bar(seasonal, x="Seasonality", y="TotalSales", color="Category", barmode="group",
                          title="Seasonal Sales by Category")
    st.plotly_chart(fig_seasonal, use_container_width=True)

with st.expander("⚖️ Supply vs. Forecast Gap Distribution"):
    gap['GapType'] = gap['AvgSupplyGap'].apply(lambda x: 'Overstock' if x < 0 else 'Understock')
    gap_filter = st.selectbox("Select Gap Type", ["All"] + gap["GapType"].unique().tolist())

    if gap_filter != "All":
        filtered_gap = gap[gap["GapType"] == gap_filter]
    else:
        filtered_gap = gap

    if not filtered_gap.empty:
        fig_gap = px.histogram(
            filtered_gap,
            x="AvgSupplyGap",
            color="GapType",
            nbins=30,
            marginal="box",
            title=f"Supply Gap Distribution ({gap_filter})" if gap_filter != "All" else "Supply Gap Distribution",
            color_discrete_map={"Overstock": "blue", "Understock": "red"}
        )
        st.plotly_chart(fig_gap, use_container_width=True)
    else:
        st.info("No data available for the selected Gap Type.")

# ------------------ TABLES ------------------
with st.expander("⚠️ Chronic Understock (7+ Days)"):
    st.dataframe(understock.sort_values("DaysBelowForecast", ascending=False).reset_index(drop=True))

with st.expander("🪊 Aging Inventory (High Stock > 14 Days)"):
    st.dataframe(aging[aging['DaysHighStock'] > 14].sort_values("DaysHighStock", ascending=False).reset_index(drop=True))

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit by YourName")