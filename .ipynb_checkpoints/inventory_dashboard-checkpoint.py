
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ PAGE SETUP ------------------
st.set_page_config(page_title="Inventory Dashboard", layout="wide")

st.title("📦 Urban Retail Inventory Dashboard")
st.markdown("Track SKU performance, stock health, and supply-demand balance.")

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    inventory_health = pd.read_csv("InventoryHealth.csv")
    reorder_status = pd.read_csv("ReorderStatus.csv")
    turnover = pd.read_csv("TurnoverByProduct.csv")
    top5 = pd.read_csv("Top5SKUs.csv")
    bottom5 = pd.read_csv("Bottom5SKUs.csv")
    aging = pd.read_csv("AgingInventory.csv")
    understock = pd.read_csv("ChronicUnderstock.csv")
    return inventory_health, reorder_status, turnover, top5, bottom5, aging, understock

# Load all CSVs
inventory_health, reorder_status, turnover, top5, bottom5, aging, understock = load_data()

# ------------------ KPI SECTION ------------------
st.markdown("### 🔹 Key Inventory KPIs")
col1, col2, col3, col4 = st.columns(4)

with col1:
    below_threshold = inventory_health[inventory_health['InventoryStatus'] == 'Below Threshold']
    st.metric("Below Threshold SKUs", len(below_threshold))

with col2:
    safe_skus = inventory_health[inventory_health['InventoryStatus'] == 'Safe']
    st.metric("Safe SKUs", len(safe_skus))

with col3:
    reorder_now = reorder_status[reorder_status['Status'] == 'Reorder Now']
    st.metric("Reorder Now SKUs", len(reorder_now))

with col4:
    aging_critical = aging[aging['DaysHighStock'] > 14]
    st.metric("Aging Inventory SKUs", len(aging_critical))

# ------------------ CHART SECTION ------------------
st.markdown("### 📊 Top and Bottom Product Performance")

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### 🔝 Top 5 SKUs")
    st.bar_chart(top5.set_index("ProductID")["TotalSold"])

with c2:
    st.markdown("#### 🔻 Bottom 5 SKUs")
    st.bar_chart(bottom5.set_index("ProductID")["TotalSold"])

# ------------------ INVENTORY HEALTH PIE CHART ------------------
st.markdown("### 🥧 Inventory Status Distribution")
status_counts = inventory_health['InventoryStatus'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90, colors=["red", "green"])
ax1.axis('equal')
st.pyplot(fig1)

# ------------------ UNDERSTOCK TABLE ------------------
st.markdown("### ⚠️ Chronic Understock (7+ Days)")
st.dataframe(understock.sort_values("DaysBelowForecast", ascending=False).reset_index(drop=True))

# ------------------ AGING INVENTORY TABLE ------------------
st.markdown("### 🧊 Aging Inventory (High Stock > 14 Days)")
st.dataframe(aging_critical.sort_values("DaysHighStock", ascending=False).reset_index(drop=True))

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit by YourName")
