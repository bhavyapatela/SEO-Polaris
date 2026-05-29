import pandas as pd
import streamlit as st

# Page title
st.set_page_config(page_title="SEO Polaris", layout = "wide")

st.title("SEO Polaris")
st.subheader("Whistle SEO Dashboard")

#Load Chart Sheet
df = pd.read_excel("Data/whistle_data.xlsx", sheet_name="Queries")

# Calculate KPIs
total_clicks = df['Clicks'].sum()
total_impressions = df['Impressions'].sum()
avg_ctr = df['CTR'].mean()
avg_position = df['Position'].mean()

# Create 4 KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Clicks", f"{total_clicks:,.0f}")
col2.metric("Total Impressions", f"{total_impressions:,.0f}")
col3.metric("Average CTR", f"{avg_ctr:.2f}%")
col4.metric("Average Position", f"{avg_position:.2f}")

#Date input
start_date = st.sidebar.date_input("Start date")