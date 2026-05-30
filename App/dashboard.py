import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os
import base64

# Page configuration
st.set_page_config(
    page_title="SEO Polaris | GSC Portfolio Dashboard",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling via CSS injection
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Outfit', sans-serif;
        }
        
        .main {
            background: linear-gradient(135deg, #0f0c1b 0%, #15102a 50%, #0c0817 100%);
            color: #f1f1f1;
        }
        
        /* Metric Card styling */
        .kpi-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(8px);
            transition: all 0.3s ease;
            width: 100%;
            min-height: 160px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        .kpi-card:hover {
            border-color: rgba(138, 43, 226, 0.4);
            transform: translateY(-2px);
            background: rgba(255, 255, 255, 0.05);
        }
        
        .kpi-label {
            font-size: 0.85rem;
            color: #a0aec0;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
            min-height: 40px;
            display: flex;
            align-items: flex-start;
        }
        
        .kpi-val {
            font-size: 2.2rem;
            font-weight: 800;
            color: #ffffff;
            margin: 8px 0;
        }
        
        .kpi-delta {
            font-size: 0.9rem;
            font-weight: 600;
            display: flex;
            align-items: center;
        }
        
        .delta-positive {
            color: #48bb78;
        }
        
        .delta-negative {
            color: #f56565;
        }
        
        .delta-neutral {
            color: #a0aec0;
        }
        
        /* Custom tab styles */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(255, 255, 255, 0.02);
            padding: 8px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 8px 16px;
            color: #a0aec0;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #6b46c1 !important;
            color: white !important;
        }
        
        /* API Badge styling */
        .api-badge {
            background: linear-gradient(90deg, #8a2be2 0%, #ff007f 100%);
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)


# ----------------- DYNAMIC BRAND DETECTION & PARSING -----------------

@st.cache_data
def load_gsc_data(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        data = {}
        for sheet in xls.sheet_names:
            sheet_key = sheet.lower().replace(" ", "_")
            df = pd.read_excel(file_path, sheet_name=sheet)
            data[sheet_key] = df
        return data
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

def detect_local_brands():
    brand_map = {}
    data_dir = "Data"
    if os.path.exists(data_dir):
        for f in os.listdir(data_dir):
            if f.endswith(".xlsx") and f != "temp_upload.xlsx" and not f.startswith("~$"):
                # "whistle_data.xlsx" -> "Whistle"
                # "saral_home.xlsx" -> "Saral Home"
                # "clove_dental.xlsx" -> "Clove Dental"
                name = f.replace("_data", "").replace(".xlsx", "").replace("_", " ").title()
                brand_map[name] = os.path.join(data_dir, f)
    return brand_map


# Load all detected brands initially
brand_files = detect_local_brands()
all_brands_data = {}
for name, path in brand_files.items():
    all_brands_data[name] = load_gsc_data(path)


# ----------------- SIDEBAR CONTROLS -----------------

with st.sidebar:
    logo_base64 = ""
    if os.path.exists("Unblogo.png"):
        with open("Unblogo.png", "rb") as f:
            logo_base64 = base64.b64encode(f.read()).decode()
            
    if logo_base64:
        logo_html = f"""
        <div style="display: flex; align-items: center; gap: 8px; margin-top: 8px; margin-bottom: 12px;">
            <img src="data:image/png;base64,{logo_base64}" width="30" style="vertical-align: middle;">
            <span style="font-weight: 800; font-size: 1.8rem; color: #ffffff; line-height: 1;">SEO Polaris</span>
        </div>
        """
        st.markdown(logo_html, unsafe_allow_html=True)
    else:
        st.title("🌌 SEO Polaris")
    st.markdown("*SEO Intelligence Engine v1.0*")
    st.write("---")

# Dynamic Brand / View Selector
st.sidebar.subheader("🏢 Active Portfolio/Brand")
view_options = ["📊 Polaris Command Center (Cross-Brand Comparison)"] + list(all_brands_data.keys())
selected_view = st.sidebar.selectbox("Select View", view_options)

# File Upload Overrides
uploaded_file = st.sidebar.file_uploader("Upload GSC Excel Export", type=["xlsx"])
if uploaded_file is not None:
    with open("Data/temp_upload.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())
    uploaded_data = load_gsc_data("Data/temp_upload.xlsx")
    if uploaded_data:
        all_brands_data["Uploaded Brand"] = uploaded_data
        brand_files["Uploaded Brand"] = "Data/temp_upload.xlsx"
        st.sidebar.success("Loaded uploaded file as 'Uploaded Brand'!")
        # Force re-rendering view option list
        st.rerun()

# ----------------- GENERAL DATA PREPARATION & DATE BOUNDS -----------------

# Compute absolute date bounds across all available brands
all_dates = []
for b_name, b_data in all_brands_data.items():
    c_df = b_data.get('chart')
    if c_df is not None and 'Date' in c_df.columns:
        c_df['Date'] = pd.to_datetime(c_df['Date'])
        all_dates.extend(c_df['Date'].tolist())

if all_dates:
    min_date = min(all_dates).to_pydatetime()
    max_date = max(all_dates).to_pydatetime()
else:
    min_date = datetime.now() - timedelta(days=90)
    max_date = datetime.now()

st.sidebar.subheader("📅 Date Filters")
date_range = st.sidebar.date_input(
    "Select Timeframe",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if date_range and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# ----------------- HELPER FUNCTIONS -----------------

def get_pop_metrics(df, start_d, end_d):
    df_sorted = df.sort_values('Date')
    curr_mask = (df_sorted['Date'] >= pd.Timestamp(start_d)) & (df_sorted['Date'] <= pd.Timestamp(end_d))
    curr_df = df_sorted[curr_mask]
    
    duration = (end_d - start_d).days + 1
    prev_end = start_d - timedelta(days=1)
    prev_start = prev_end - timedelta(days=duration - 1)
    
    prev_mask = (df_sorted['Date'] >= pd.Timestamp(prev_start)) & (df_sorted['Date'] <= pd.Timestamp(prev_end))
    prev_df = df_sorted[prev_mask]
    
    if prev_df.empty or len(prev_df) < 2:
        half_len = len(curr_df) // 2
        if half_len > 0:
            prev_df = curr_df.iloc[:half_len]
            curr_df = curr_df.iloc[half_len:]
        else:
            prev_df = curr_df
            
    c_clicks = curr_df['Clicks'].sum()
    p_clicks = prev_df['Clicks'].sum()
    c_imp = curr_df['Impressions'].sum()
    p_imp = prev_df['Impressions'].sum()
    
    c_ctr = (c_clicks / c_imp * 100) if c_imp > 0 else 0
    p_ctr = (p_clicks / p_imp * 100) if p_imp > 0 else 0
    
    c_pos = curr_df['Position'].mean() if not curr_df.empty else 0
    p_pos = prev_df['Position'].mean() if not prev_df.empty else 0
    
    def calc_delta(curr, prev, higher_is_better=True):
        if prev == 0:
            return 0.0
        diff = ((curr - prev) / prev) * 100
        return diff if higher_is_better else -diff
        
    return {
        "clicks": (c_clicks, calc_delta(c_clicks, p_clicks)),
        "impressions": (c_imp, calc_delta(c_imp, p_imp)),
        "ctr": (c_ctr, calc_delta(c_ctr, p_ctr)),
        "position": (c_pos, calc_delta(c_pos, p_pos, higher_is_better=False))
    }

def render_kpi_card(label, value_str, delta_val, suffix=""):
    delta_class = "delta-positive" if delta_val > 0 else ("delta-negative" if delta_val < 0 else "delta-neutral")
    delta_symbol = "▲" if delta_val > 0 else ("▼" if delta_val < 0 else "•")
    
    card_html = f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-val">{value_str}</div>
        <div class="kpi-delta {delta_class}">
            {delta_symbol} {abs(delta_val):.2f}% {suffix}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

# Google Algorithm Updates mapping
GOOGLE_UPDATES = [
    {"date": "2026-03-05", "name": "March 2026 Core Update"},
    {"date": "2026-05-06", "name": "May 2026 Reputation Abuse Update"}
]

# ----------------- VIEW RENDERING LOGIC -----------------

if selected_view == "📊 Polaris Command Center (Cross-Brand Comparison)":
    # ----------------- PORTFOLIO COMPARISON VIEW -----------------
    st.title("📊 Polaris Command Center")
    st.subheader("Cross-Brand Aggregated SEO Performance")
    
    # 1. Aggregate and prepare the data
    merged_charts = []
    brand_kpis = {}
    
    for b_name, b_data in all_brands_data.items():
        chart_df = b_data.get('chart')
        if chart_df is not None:
            chart_df['Date'] = pd.to_datetime(chart_df['Date'])
            pop = get_pop_metrics(chart_df, start_date, end_date)
            brand_kpis[b_name] = pop
            
            mask = (chart_df['Date'] >= pd.Timestamp(start_date)) & (chart_df['Date'] <= pd.Timestamp(end_date))
            f_chart = chart_df[mask].copy()
            f_chart['Brand'] = b_name
            merged_charts.append(f_chart)
            
    if merged_charts:
        portfolio_combined_df = pd.concat(merged_charts)
        
        # Group by Date to get consolidated metrics
        portfolio_agg_chart = portfolio_combined_df.groupby('Date').apply(lambda x: pd.Series({
            'Clicks': x['Clicks'].sum(),
            'Impressions': x['Impressions'].sum(),
            'CTR': (x['Clicks'].sum() / x['Impressions'].sum() * 100) if x['Impressions'].sum() > 0 else 0,
            'Position': np.average(x['Position'], weights=x['Impressions']) if x['Impressions'].sum() > 0 else x['Position'].mean()
        })).reset_index()
        
        # Calculate Blended Period-over-Period Performance
        total_clicks = 0
        total_prev_clicks = 0
        total_impressions = 0
        total_prev_impressions = 0
        total_weighted_pos = 0.0
        total_prev_weighted_pos = 0.0
        
        for b_name, pop in brand_kpis.items():
            c_clicks, d_clicks = pop['clicks']
            c_imp, d_imp = pop['impressions']
            c_pos, d_pos = pop['position']
            
            prev_clicks = c_clicks / (1 + d_clicks/100) if d_clicks != -100 else 0
            prev_imp = c_imp / (1 + d_imp/100) if d_imp != -100 else 0
            prev_pos = c_pos / (1 - d_pos/100) if d_pos != 100 else 10.0 # simple approximation
            
            total_clicks += c_clicks
            total_prev_clicks += prev_clicks
            total_impressions += c_imp
            total_prev_impressions += prev_imp
            
            total_weighted_pos += (c_pos * c_imp)
            total_prev_weighted_pos += (prev_pos * prev_imp)
            
        blended_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        blended_prev_ctr = (total_prev_clicks / total_prev_impressions * 100) if total_prev_impressions > 0 else 0
        blended_pos = (total_weighted_pos / total_impressions) if total_impressions > 0 else 0
        blended_prev_pos = (total_prev_weighted_pos / total_prev_impressions) if total_prev_impressions > 0 else 0
        
        def pct_diff(curr, prev, higher_is_better=True):
            if prev == 0:
                return 0.0
            diff = ((curr - prev) / prev) * 100
            return diff if higher_is_better else -diff
            
        portfolio_pop = {
            "clicks": (total_clicks, pct_diff(total_clicks, total_prev_clicks)),
            "impressions": (total_impressions, pct_diff(total_impressions, total_prev_impressions)),
            "ctr": (blended_ctr, pct_diff(blended_ctr, blended_prev_ctr)),
            "position": (blended_pos, pct_diff(blended_pos, blended_prev_pos, higher_is_better=False))
        }
        
        # ----------------- PORTFOLIO METRIC CARDS GRID -----------------
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            render_kpi_card("Portfolio Clicks", f"{portfolio_pop['clicks'][0]:,.0f}", portfolio_pop['clicks'][1], "vs prev period")
        with col2:
            render_kpi_card("Portfolio Impressions", f"{portfolio_pop['impressions'][0]:,.0f}", portfolio_pop['impressions'][1], "vs prev period")
        with col3:
            render_kpi_card("Portfolio Blended CTR", f"{portfolio_pop['ctr'][0]:.2f}%", portfolio_pop['ctr'][1], "vs prev period")
        with col4:
            render_kpi_card("Portfolio Blended Avg Position", f"{portfolio_pop['position'][0]:.2f}", portfolio_pop['position'][1], "vs prev period")
            
        st.write("---")
        
        # Create tabs for Portfolio Overview
        p_tab_overview, p_tab_keyword_gap, p_tab_device_geo = st.tabs([
            "📈 Portfolio Trends & Share",
            "⚔️ Competitive Keyword Gap",
            "📱 Device & Regional Share"
        ])
        
        with p_tab_overview:
            # Side-by-side: Share of Voice vs Absolute Trend
            c_so1, c_so2 = st.columns([1, 2])
            
            with c_so1:
                st.markdown("#### 🍩 Click Share of Voice")
                share_data = pd.DataFrame([
                    {"Brand": b_name, "Clicks": pop['clicks'][0], "Impressions": pop['impressions'][0]}
                    for b_name, pop in brand_kpis.items()
                ])
                fig_share = px.pie(
                    share_data,
                    names="Brand",
                    values="Clicks",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Prism
                )
                fig_share.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig_share, use_container_width=True)
                
            with c_so2:
                st.markdown("#### 📈 Multi-Brand Trend Synchronization")
                fig_sync = px.line(
                    portfolio_combined_df.sort_values('Date'),
                    x='Date',
                    y='Clicks',
                    color='Brand',
                    line_shape='spline',
                    color_discrete_sequence=px.colors.qualitative.Prism
                )
                
                # Add Google update vertical lines
                for update in GOOGLE_UPDATES:
                    u_date = pd.to_datetime(update['date'])
                    if start_date <= u_date.date() <= end_date:
                        fig_sync.add_vline(
                            x=u_date.timestamp() * 1000, # plotly handles datetimes as timestamps
                            line_dash="dash",
                            line_color="#ff3366",
                            annotation_text=update['name'],
                            annotation_position="top left"
                        )
                        
                fig_sync.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white"),
                    xaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig_sync, use_container_width=True)
                
            st.markdown("#### 🏢 Brand Metrics Comparison")
            comp_table = []
            for b_name, pop in brand_kpis.items():
                comp_table.append({
                    "Brand Name": b_name,
                    "Total Clicks": pop['clicks'][0],
                    "Clicks MoM Change": f"{pop['clicks'][1]:+.2f}%",
                    "Total Impressions": pop['impressions'][0],
                    "Impressions MoM Change": f"{pop['impressions'][1]:+.2f}%",
                    "Blended CTR": f"{pop['ctr'][0]:.2f}%",
                    "Avg Position": f"{pop['position'][0]:.2f}"
                })
            st.dataframe(pd.DataFrame(comp_table), use_container_width=True, hide_index=True)
            
        with p_tab_keyword_gap:
            st.markdown("### Competitive Keyword Gap & Synergy")
            st.markdown("Compare keyword rankings side-by-side across all portfolio brands to find keyword overlap or opportunities.")
            
            # Combine Queries from all brands
            queries_by_brand = {}
            all_queries_set = set()
            
            for b_name, b_data in all_brands_data.items():
                q_df = b_data.get('queries')
                if q_df is not None:
                    # Clean queries
                    q_df_clean = q_df.copy()
                    q_df_clean['Top queries'] = q_df_clean['Top queries'].astype(str).str.strip().str.lower()
                    queries_by_brand[b_name] = q_df_clean.set_index('Top queries')
                    all_queries_set.update(q_df_clean['Top queries'].tolist())
                    
            gap_data = []
            for query in all_queries_set:
                row_info = {"Query Keyword": query}
                total_clicks = 0
                total_impressions = 0
                ranks = []
                
                for b_name in all_brands_data.keys():
                    brand_q_df = queries_by_brand.get(b_name)
                    if brand_q_df is not None and query in brand_q_df.index:
                        q_row = brand_q_df.loc[query]
                        # Handle duplicate index if any
                        if isinstance(q_row, pd.DataFrame):
                            q_row = q_row.iloc[0]
                        row_info[f"{b_name} Rank"] = round(q_row['Position'], 2)
                        row_info[f"{b_name} Clicks"] = int(q_row['Clicks'])
                        total_clicks += q_row['Clicks']
                        total_impressions += q_row['Impressions']
                        ranks.append(q_row['Position'])
                    else:
                        row_info[f"{b_name} Rank"] = np.nan
                        row_info[f"{b_name} Clicks"] = 0
                        
                row_info["Combined Clicks"] = total_clicks
                row_info["Combined Impressions"] = total_impressions
                row_info["Best Rank"] = min(ranks) if ranks else np.nan
                gap_data.append(row_info)
                
            gap_df = pd.DataFrame(gap_data)
            
            # Advanced filters
            col_gf1, col_gf2 = st.columns([2, 1])
            with col_gf1:
                kw_search = st.text_input("🔍 Search Overlapping Keywords", "").strip().lower()
            with col_gf2:
                gap_mode = st.selectbox(
                    "View Filter",
                    ["Show All Keywords", "Keyword Gaps (One brand ranks, others don't)", "Keyword Cannibalization (Multiple brands rank in top 20)"]
                )
                
            if kw_search:
                gap_df = gap_df[gap_df['Query Keyword'].str.contains(kw_search, case=False)]
                
            # Filter definitions
            rank_cols = [f"{b_name} Rank" for b_name in all_brands_data.keys()]
            
            if gap_mode == "Keyword Gaps (One brand ranks, others don't)":
                # Find rows where exactly 1 rank col is not null
                non_null_count = gap_df[rank_cols].notnull().sum(axis=1)
                gap_df = gap_df[non_null_count == 1]
            elif gap_mode == "Keyword Cannibalization (Multiple brands rank in top 20)":
                # Find rows where at least two brands rank in position <= 20
                under_20_count = (gap_df[rank_cols] <= 20).sum(axis=1)
                gap_df = gap_df[under_20_count >= 2]
                
            gap_df_display = gap_df.sort_values('Combined Clicks', ascending=False)
            st.dataframe(
                gap_df_display.style.format({
                    "Combined Clicks": "{:,.0f}",
                    "Combined Impressions": "{:,.0f}",
                    "Best Rank": "{:.2f}"
                }).highlight_null(color="rgba(255,255,255,0.02)"),
                use_container_width=True,
                hide_index=True
            )
            
        with p_tab_device_geo:
            st.markdown("### Cross-Brand Devices & Regional Share")
            
            col_dg1, col_dg2 = st.columns(2)
            
            with col_dg1:
                st.markdown("#### 📱 Device Click Share Comparison")
                device_records = []
                for b_name, b_data in all_brands_data.items():
                    d_df = b_data.get('devices')
                    if d_df is not None:
                        temp = d_df.copy()
                        temp['Brand'] = b_name
                        device_records.append(temp)
                if device_records:
                    portfolio_dev = pd.concat(device_records)
                    fig_dev_share = px.bar(
                        portfolio_dev,
                        x='Device',
                        y='Clicks',
                        color='Brand',
                        barmode='group',
                        title="Clicks by Device & Brand",
                        color_discrete_sequence=px.colors.qualitative.Prism
                    )
                    fig_dev_share.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                    st.plotly_chart(fig_dev_share, use_container_width=True)
                    
            with col_dg2:
                st.markdown("#### 🌍 Top Traffic Countries Comparison")
                country_records = []
                for b_name, b_data in all_brands_data.items():
                    c_df = b_data.get('countries')
                    if c_df is not None:
                        temp = c_df.head(5).copy()
                        temp['Brand'] = b_name
                        country_records.append(temp)
                if country_records:
                    portfolio_cnt = pd.concat(country_records)
                    fig_cnt_share = px.bar(
                        portfolio_cnt,
                        x='Clicks',
                        y='Country',
                        color='Brand',
                        barmode='stack',
                        orientation='h',
                        title="Top Countries by Click Volume",
                        color_discrete_sequence=px.colors.qualitative.Prism
                    )
                    fig_cnt_share.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                    st.plotly_chart(fig_cnt_share, use_container_width=True)
                    
    else:
        st.info("No data sheets available for cross-brand overview.")

else:
    # ----------------- INDIVIDUAL BRAND VIEW (ORIGINAL DASHBOARD) -----------------
    gsc_data = all_brands_data[selected_view]
    
    # Advanced PM Insights Toggles in Sidebar
    st.sidebar.subheader("🛡️ Brand Segmentation")
    
    # Map brand name to default query matching patterns
    brand_keyword_defaults = {
        "Whistle": "whistle",
        "Saral Home": "saral",
        "Clove Dental": "clove"
    }
    
    default_brand_keyword = brand_keyword_defaults.get(selected_view, "")
    brand_term = st.sidebar.text_input("Brand Keywords (comma-separated)", default_brand_keyword)
    brand_filter = st.sidebar.selectbox(
        "Global Brand Mode",
        ["Show All Clicks", "Brand Queries Only", "Exclude Brand (Generic Only)"]
    )
    
    # Helper function for brand matching
    brand_terms_list = [term.strip().lower() for term in brand_term.split(",") if term.strip()]
    def is_brand(query):
        query_str = str(query).lower()
        return any(bt in query_str for bt in brand_terms_list)
        
    chart_df = gsc_data.get('chart')
    if chart_df is not None:
        chart_df['Date'] = pd.to_datetime(chart_df['Date'])
        pop = get_pop_metrics(chart_df, start_date, end_date)
    else:
        st.error(f"Chart data sheet missing for {selected_view}.")
        st.stop()
        
    if brand_filter != "Show All Clicks":
        st.sidebar.info("💡 Note: Brand filtering applies to queries. Pre-aggregated reports (e.g. Device splits) will reflect totals.")
        
    st.title(f"🌌 {selected_view}")
    st.subheader("SEO Intelligence & Google Search Console Analytics")
    
    # ----------------- METRIC CARDS GRID -----------------
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Clicks", f"{pop['clicks'][0]:,.0f}", pop['clicks'][1], "vs prev period")
    with col2:
        render_kpi_card("Total Impressions", f"{pop['impressions'][0]:,.0f}", pop['impressions'][1], "vs prev period")
    with col3:
        render_kpi_card("Average CTR", f"{pop['ctr'][0]:.2f}%", pop['ctr'][1], "vs prev period")
    with col4:
        render_kpi_card("Average Position", f"{pop['position'][0]:.2f}", pop['position'][1], "vs prev period")
        
    st.write("---")
    
    # ----------------- TABS CREATION -----------------
    tab_overview, tab_queries, tab_pages, tab_intelligence = st.tabs([
        "📈 Overview Trends", 
        "🔍 Queries Explorer", 
        "📄 Pages Explorer", 
        "💡 Search Intelligence Hub"
    ])
    
    # ----------------- TAB 1: OVERVIEW TRENDS -----------------
    with tab_overview:
        mask = (chart_df['Date'] >= pd.Timestamp(start_date)) & (chart_df['Date'] <= pd.Timestamp(end_date))
        filtered_chart = chart_df[mask].sort_values('Date')
        
        st.markdown("### Search Performance Trends")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=filtered_chart['Date'], y=filtered_chart['Clicks'],
            name="Clicks", mode='lines+markers', line=dict(color='#8a2be2', width=3),
            yaxis="y1"
        ))
        fig.add_trace(go.Scatter(
            x=filtered_chart['Date'], y=filtered_chart['Position'],
            name="Average Position", mode='lines', line=dict(color='#ff007f', width=2, dash='dot'),
            yaxis="y2"
        ))
        
        fig.update_layout(
            title="Daily Clicks vs. Average Rank Position",
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(
                title=dict(text="Clicks", font=dict(color="#8a2be2")),
                tickfont=dict(color="#8a2be2")
            ),
            yaxis2=dict(
                title=dict(text="Position (Rank)", font=dict(color="#ff007f")),
                tickfont=dict(color="#ff007f"),
                overlaying="y",
                side="right",
                autorange="reversed"
            ),
            xaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Device and Countries Split Columns
        c_split1, c_split2 = st.columns(2)
        
        with c_split1:
            st.markdown("#### 📱 Device Click Share & CTR")
            device_df = gsc_data.get('devices')
            if device_df is not None:
                dev_formatted = device_df.copy()
                dev_formatted['CTR'] = dev_formatted['CTR'] * 100
                
                fig_dev = px.bar(
                    dev_formatted,
                    x='Device',
                    y='Clicks',
                    color='CTR',
                    color_continuous_scale='Purples',
                    text_auto='.2s',
                    title="Clicks & CTR by Device Category"
                )
                fig_dev.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig_dev, use_container_width=True)
            else:
                st.info("No device data sheet found.")
                
        with c_split2:
            st.markdown("#### 🌍 Top Traffic Countries")
            country_df = gsc_data.get('countries')
            if country_df is not None:
                fig_cnt = px.bar(
                    country_df.head(10).sort_values('Clicks', ascending=True),
                    x='Clicks',
                    y='Country',
                    orientation='h',
                    color='CTR',
                    color_continuous_scale='Purples',
                    title="Top 10 Countries by Clicks & CTR"
                )
                fig_cnt.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
                st.plotly_chart(fig_cnt, use_container_width=True)
            else:
                st.info("No country data sheet found.")
                
    # ----------------- TAB 2: QUERIES EXPLORER -----------------
    with tab_queries:
        queries_df = gsc_data.get('queries')
        if queries_df is not None:
            st.markdown("### Search Queries Explorer")
            
            f_col1, f_col2 = st.columns([3, 1])
            with f_col1:
                q_search = st.text_input("🔍 Filter keywords", "")
            with f_col2:
                min_clicks = st.number_input("Min Clicks threshold", min_value=0, value=0, key="queries_min_clicks")
                
            filtered_q = queries_df.copy()
            
            # Apply the Brand filter
            if brand_filter == "Brand Queries Only":
                filtered_q = filtered_q[filtered_q['Top queries'].apply(is_brand)]
            elif brand_filter == "Exclude Brand (Generic Only)":
                filtered_q = filtered_q[~filtered_q['Top queries'].apply(is_brand)]
                
            if q_search:
                filtered_q = filtered_q[filtered_q['Top queries'].astype(str).str.contains(q_search, case=False)]
                
            filtered_q = filtered_q[filtered_q['Clicks'] >= min_clicks]
            formatted_q = filtered_q.copy()
            formatted_q['CTR'] = formatted_q['CTR'] * 100
            
            # Brand breakdown metrics
            br_clicks = queries_df[queries_df['Top queries'].apply(is_brand)]['Clicks'].sum()
            non_br_clicks = queries_df[~queries_df['Top queries'].apply(is_brand)]['Clicks'].sum()
            total_q_clicks = br_clicks + non_br_clicks if (br_clicks + non_br_clicks) > 0 else 1
            
            b_col1, b_col2 = st.columns([3, 1])
            with b_col1:
                st.markdown(f"**Found {len(formatted_q)} matching search queries**")
                st.dataframe(
                    formatted_q.style.format({
                        "Clicks": "{:,.0f}",
                        "Impressions": "{:,.0f}",
                        "CTR": "{:.2f}%",
                        "Position": "{:.2f}"
                    }),
                    use_container_width=True
                )
            with b_col2:
                st.markdown("#### 🏷️ Brand Traffic Split")
                brand_pie = pd.DataFrame({
                    "Segment": ["Branded", "Generic (Non-Brand)"],
                    "Clicks": [br_clicks, non_br_clicks]
                })
                fig_brand_pie = px.pie(
                    brand_pie, 
                    names="Segment", 
                    values="Clicks", 
                    hole=0.4,
                    color_discrete_sequence=["#8a2be2", "#ff007f"]
                )
                fig_brand_pie.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_brand_pie, use_container_width=True)
                st.metric("Branded Clicks", f"{br_clicks:,.0f}", f"{(br_clicks/total_q_clicks * 100):.1f}% of total")
                st.metric("Generic Clicks", f"{non_br_clicks:,.0f}", f"{(non_br_clicks/total_q_clicks * 100):.1f}% of total")
        else:
            st.error("No queries dataset found.")
            
    # ----------------- TAB 3: PAGES EXPLORER -----------------
    with tab_pages:
        pages_df = gsc_data.get('pages')
        if pages_df is not None:
            st.markdown("### Landing Pages Explorer")
            
            p_search = st.text_input("🔍 Search Page URL", "", key="page_search_input")
            
            filtered_p = pages_df.copy()
            if p_search:
                filtered_p = filtered_p[filtered_p['Top pages'].astype(str).str.contains(p_search, case=False)]
                
            def categorize_page(row):
                if row['Clicks'] > pages_df['Clicks'].quantile(0.9):
                    return "🌟 Star Performers (Top 10%)"
                elif row['Position'] <= 10 and row['CTR'] < pages_df['CTR'].median():
                    return "📈 High Rank, Low CTR (Needs Title Update)"
                elif row['Position'] > 10 and row['Position'] <= 20:
                    return "🎯 Striking Distance (Page 2)"
                else:
                    return "🔍 Longtail / Low Traffic"
                    
            filtered_p['Performance Category'] = filtered_p.apply(categorize_page, axis=1)
            formatted_p = filtered_p.copy()
            formatted_p['CTR'] = formatted_p['CTR'] * 100
            
            p_col1, p_col2 = st.columns([1, 3])
            
            with p_col1:
                st.markdown("#### Page Tier Distribution")
                cat_counts = filtered_p['Performance Category'].value_counts().reset_index()
                cat_counts.columns = ['Category', 'Count']
                fig_cat = px.pie(cat_counts, names='Category', values='Count', color_discrete_sequence=px.colors.sequential.Plotly3)
                fig_cat.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_cat, use_container_width=True)
                
            with p_col2:
                st.markdown(f"**Found {len(formatted_p)} landing pages**")
                st.dataframe(
                    formatted_p.style.format({
                        "Clicks": "{:,.0f}",
                        "Impressions": "{:,.0f}",
                        "CTR": "{:.2f}%",
                        "Position": "{:.2f}"
                    }),
                    use_container_width=True
                )
        else:
            st.error("No pages dataset found.")
            
    # ----------------- TAB 4: SEARCH INTELLIGENCE REPORTS -----------------
    with tab_intelligence:
        st.markdown("### Actionable Search Intelligence Hub")
        
        intel_mode = st.radio(
            "Choose Insights View",
            ["🎯 Striking Distance & Click Potential", "📉 Content Decay Alert (API Feature Simulation)", "📱 Device CTR Discrepancy Analysis"],
            horizontal=True
        )
        
        if intel_mode == "🎯 Striking Distance & Click Potential":
            st.markdown("#### Striking Distance Optimization Report")
            st.markdown("Keywords or pages ranking in positions 4–15. We compute the **Click Potential** using standard organic benchmark click curves (projecting CTR to 10% if optimized).")
            
            queries_df = gsc_data.get('queries')
            pages_df = gsc_data.get('pages')
            
            target_mode = st.radio("Target Element", ["Queries", "Pages"], horizontal=True)
            bench_ctr = st.slider("Projected Position Benchmarked CTR (%)", 1.0, 30.0, 10.0) / 100
            
            df_target = queries_df if target_mode == "Queries" else pages_df
            label_col = 'Top queries' if target_mode == "Queries" else 'Top pages'
            
            if df_target is not None:
                striking = df_target[(df_target['Position'] >= 4) & (df_target['Position'] <= 15)].copy()
                
                # Calculate potential clicks and uplift
                striking['Projected Clicks'] = striking['Impressions'] * bench_ctr
                striking['Uplift Potential (Clicks)'] = striking['Projected Clicks'] - striking['Clicks']
                
                # Format and display
                striking_out = striking.sort_values('Uplift Potential (Clicks)', ascending=False).copy()
                striking_out['CTR'] = striking_out['CTR'] * 100
                striking_out['Projected Clicks'] = striking_out['Projected Clicks'].apply(lambda x: max(0, x))
                striking_out['Uplift Potential (Clicks)'] = striking_out['Uplift Potential (Clicks)'].apply(lambda x: max(0, x))
                
                st.dataframe(
                    striking_out.style.format({
                        "Clicks": "{:,.0f}",
                        "Impressions": "{:,.0f}",
                        "CTR": "{:.2f}%",
                        "Position": "{:.2f}",
                        "Projected Clicks": "{:,.0f}",
                        "Uplift Potential (Clicks)": "{:,.0f}"
                    }),
                    use_container_width=True
                )
            else:
                st.error("Selected dataset sheet missing.")
                
        elif intel_mode == "📉 Content Decay Alert (API Feature Simulation)":
            st.markdown('<div class="api-badge">GSC API Integration Preview</div>', unsafe_allow_html=True)
            st.markdown("#### Page Traffic Loss Tracker (Content Decay)")
            st.markdown(
                "Detects pages whose performance has steadily declined in the second half of the date range compared to the first half."
            )
            
            pages_df = gsc_data.get('pages')
            if pages_df is not None:
                decay_data = []
                for idx, row in pages_df.head(15).iterrows():
                    np.random.seed(idx)
                    drift = np.random.uniform(-0.4, 0.15)
                    curr_clicks = row['Clicks']
                    prev_clicks = curr_clicks / (1 + drift)
                    loss = curr_clicks - prev_clicks
                    decay_data.append({
                        "Page URL": row['Top pages'],
                        "Current Period Clicks": int(curr_clicks),
                        "Previous Period Clicks": int(prev_clicks),
                        "Absolute Click Change": int(loss),
                        "Percentage Change": drift * 100
                    })
                    
                decay_df = pd.DataFrame(decay_data).sort_values("Absolute Click Change")
                decaying_only = decay_df[decay_df['Absolute Click Change'] < 0].copy()
                
                fig_decay = px.bar(
                    decaying_only,
                    x='Absolute Click Change',
                    y='Page URL',
                    orientation='h',
                    color='Percentage Change',
                    color_continuous_scale='Reds_r',
                    title="Top Decaying Landing Pages (Click Loss)"
                )
                st.plotly_chart(fig_decay, use_container_width=True)
                
                st.dataframe(
                    decaying_only.style.format({
                        "Current Period Clicks": "{:,.0f}",
                        "Previous Period Clicks": "{:,.0f}",
                        "Absolute Click Change": "{:,.0f}",
                        "Percentage Change": "{:.2f}%"
                    }),
                    use_container_width=True
                )
                
        elif intel_mode == "📱 Device CTR Discrepancy Analysis":
            st.markdown("#### Device CTR and Ranking Correlation")
            st.markdown("Analyze whether rankings correspond to identical CTR rates across Mobile, Desktop, and Tablet.")
            
            device_df = gsc_data.get('devices')
            if device_df is not None:
                dev_formatted = device_df.copy()
                dev_formatted['CTR'] = dev_formatted['CTR'] * 100
                
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.markdown("**Device Metrics Summary**")
                    st.dataframe(
                        dev_formatted.style.format({
                            "Clicks": "{:,.0f}",
                            "Impressions": "{:,.0f}",
                            "CTR": "{:.2f}%",
                            "Position": "{:.2f}"
                        }),
                        use_container_width=True
                    )
                with col_d2:
                    fig_dis = go.Figure()
                    fig_dis.add_trace(go.Bar(
                        x=dev_formatted['Device'],
                        y=dev_formatted['CTR'],
                        name="CTR (%)",
                        marker_color="#8a2be2"
                    ))
                    fig_dis.add_trace(go.Scatter(
                        x=dev_formatted['Device'],
                        y=dev_formatted['Position'],
                        name="Avg Position",
                        yaxis="y2",
                        line=dict(color="#ff007f", width=4)
                    ))
                    fig_dis.update_layout(
                        title="Device CTR vs Average Position",
                        yaxis=dict(title="CTR (%)"),
                        yaxis2=dict(title="Average Position", overlaying="y", side="right", autorange="reversed"),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="white")
                    )
                    st.plotly_chart(fig_dis, use_container_width=True)