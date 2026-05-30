import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="SEO Polaris | GSC Dashboard",
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
    </style>
""", unsafe_allow_html=True)

# ----------------- DATA INGESTION & PARSING -----------------

@st.cache_data
def load_gsc_data(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        data = {}
        for sheet in xls.sheet_names:
            # GSC can have lowercase/uppercase variants
            sheet_key = sheet.lower().replace(" ", "_")
            df = pd.read_excel(file_path, sheet_name=sheet)
            data[sheet_key] = df
        return data
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

# Load initial data
default_file = "Data/whistle_data.xlsx"
gsc_data = load_gsc_data(default_file)

if gsc_data is None:
    st.stop()

# ----------------- SIDEBAR CONTROLS -----------------

st.sidebar.title("🌌 SEO Polaris")
st.sidebar.markdown("*SEO Intelligence Engine v1.0*")
st.sidebar.write("---")

# File Upload Overrides
uploaded_file = st.sidebar.file_uploader("Upload GSC Excel Export", type=["xlsx"])
if uploaded_file is not None:
    # Save temp and override gsc_data
    with open("Data/temp_upload.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())
    gsc_data = load_gsc_data("Data/temp_upload.xlsx")
    st.sidebar.success("Loaded uploaded file!")

# Extract Chart data for date calculation
chart_df = gsc_data.get('chart')
if chart_df is not None:
    chart_df['Date'] = pd.to_datetime(chart_df['Date'])
    min_date = chart_df['Date'].min().to_pydatetime()
    max_date = chart_df['Date'].max().to_pydatetime()
    
    st.sidebar.subheader("📅 Date Filters")
    date_range = st.sidebar.date_input(
        "Select Timeframe",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
else:
    date_range = None

st.sidebar.subheader("⚙️ Analysis Settings")
brand_term = st.sidebar.text_input("Brand Keywords (comma-separated)", "whistle")

# ----------------- HELPER FUNCTIONS -----------------

def get_pop_metrics(df, start_d, end_d):
    """Calculates metrics for current period vs previous period of same duration."""
    df_sorted = df.sort_values('Date')
    
    # Filter current period
    curr_mask = (df_sorted['Date'] >= pd.Timestamp(start_d)) & (df_sorted['Date'] <= pd.Timestamp(end_d))
    curr_df = df_sorted[curr_mask]
    
    # Determine timeframe duration
    duration = (end_d - start_d).days + 1
    
    # Calculate previous period start/end
    prev_end = start_d - timedelta(days=1)
    prev_start = prev_end - timedelta(days=duration - 1)
    
    prev_mask = (df_sorted['Date'] >= pd.Timestamp(prev_start)) & (df_sorted['Date'] <= pd.Timestamp(prev_end))
    prev_df = df_sorted[prev_mask]
    
    # Fallback to splitting dataset if no previous period exists in GSC data
    if prev_df.empty or len(prev_df) < 2:
        half_len = len(curr_df) // 2
        if half_len > 0:
            prev_df = curr_df.iloc[:half_len]
            curr_df = curr_df.iloc[half_len:]
        else:
            prev_df = curr_df
            
    # Calculate totals
    c_clicks = curr_df['Clicks'].sum()
    p_clicks = prev_df['Clicks'].sum()
    c_imp = curr_df['Impressions'].sum()
    p_imp = prev_df['Impressions'].sum()
    
    # Avoid zero division
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

# Compute KPI metrics
if date_range and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

pop = get_pop_metrics(chart_df, start_date, end_date)

# Header title
st.title("🌌 SEO Polaris")
st.subheader("SEO Intelligence & Google Search Console Analytics")

# ----------------- METRIC CARDS GRID -----------------

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

col1, col2, col3, col4 = st.columns(4)

with col1:
    render_kpi_card("Total Clicks", f"{pop['clicks'][0]:,.0f}", pop['clicks'][1], "vs prev period")
with col2:
    render_kpi_card("Total Impressions", f"{pop['impressions'][0]:,.0f}", pop['impressions'][1], "vs prev period")
with col3:
    render_kpi_card("Average CTR", f"{pop['ctr'][0]:.2f}%", pop['ctr'][1], "vs prev period")
with col4:
    # Lower position is better
    render_kpi_card("Average Position", f"{pop['position'][0]:.2f}", pop['position'][1], "vs prev period")

st.write("---")

# ----------------- TABS CREATION -----------------

tab_overview, tab_queries, tab_pages, tab_intelligence = st.tabs([
    "📈 Overview Trends", 
    "🔍 Queries Explorer", 
    "📄 Pages Explorer", 
    "💡 Search Intelligence"
])

# ----------------- TAB 1: OVERVIEW TRENDS -----------------
with tab_overview:
    # Filtering Chart df based on dates
    mask = (chart_df['Date'] >= pd.Timestamp(start_date)) & (chart_df['Date'] <= pd.Timestamp(end_date))
    filtered_chart = chart_df[mask].sort_values('Date')
    
    st.markdown("### Search Performance Trends")
    
    # Dual Axis Trend using Plotly
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
            title=dict(
                text="Clicks",
                font=dict(color="#8a2be2")
            ),
            tickfont=dict(color="#8a2be2")
        ),
        yaxis2=dict(
            title=dict(
                text="Position (Rank)",
                font=dict(color="#ff007f")
            ),
            tickfont=dict(color="#ff007f"),
            overlaying="y",
            side="right",
            autorange="reversed" # Rank #1 at the top
        ),
        xaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Device and Countries Split Columns
    c_split1, c_split2 = st.columns(2)
    
    with c_split1:
        st.markdown("#### 📱 Device Share (Clicks)")
        device_df = gsc_data.get('devices')
        if device_df is not None:
            fig_dev = px.pie(
                device_df, 
                names='Device', 
                values='Clicks', 
                hole=0.5,
                color_discrete_sequence=px.colors.sequential.Purples_r
            )
            fig_dev.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)", 
                font=dict(color="white")
            )
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
            fig_cnt.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)", 
                font=dict(color="white")
            )
            st.plotly_chart(fig_cnt, use_container_width=True)
        else:
            st.info("No country data sheet found.")

# ----------------- TAB 2: QUERIES EXPLORER -----------------
with tab_queries:
    queries_df = gsc_data.get('queries')
    if queries_df is not None:
        st.markdown("### Search Queries Explorer")
        st.markdown("Analyze search terms driving impressions and clicks to your brand.")
        
        # Sidebar-styled filters inside tab for better UX
        f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
        
        with f_col1:
            q_search = st.text_input("🔍 Search Query Keyword", "")
        with f_col2:
            brand_filter = st.selectbox(
                "Segment Type",
                ["All Queries", "Brand Only", "Non-Brand Only"]
            )
        with f_col3:
            min_clicks = st.number_input("Min Clicks", min_value=0, value=0)
            
        # Segment and filter data
        filtered_q = queries_df.copy()
        
        # Brand filter logic
        brand_terms_list = [term.strip().lower() for term in brand_term.split(",") if term.strip()]
        
        def is_brand(query):
            query_str = str(query).lower()
            return any(bt in query_str for bt in brand_terms_list)
            
        if brand_filter == "Brand Only":
            filtered_q = filtered_q[filtered_q['Top queries'].apply(is_brand)]
        elif brand_filter == "Non-Brand Only":
            filtered_q = filtered_q[~filtered_q['Top queries'].apply(is_brand)]
            
        if q_search:
            filtered_q = filtered_q[filtered_q['Top queries'].astype(str).str.contains(q_search, case=False)]
            
        filtered_q = filtered_q[filtered_q['Clicks'] >= min_clicks]
        
        # Double format percentages
        formatted_q = filtered_q.copy()
        formatted_q['CTR'] = formatted_q['CTR'] * 100
        
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
    else:
        st.error("No queries dataset found.")

# ----------------- TAB 3: PAGES EXPLORER -----------------
with tab_pages:
    pages_df = gsc_data.get('pages')
    if pages_df is not None:
        st.markdown("### Landing Pages Explorer")
        
        p_search = st.text_input("🔍 Search Page URL", "")
        
        filtered_p = pages_df.copy()
        if p_search:
            filtered_p = filtered_p[filtered_p['Top pages'].astype(str).str.contains(p_search, case=False)]
            
        # Metrics enhancement: categorizing tiers
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
        
        # Format CTR
        formatted_p = filtered_p.copy()
        formatted_p['CTR'] = formatted_p['CTR'] * 100
        
        # Layout splitting: Categories and Table
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
    st.markdown("### Actionable Daily Search Insights")
    
    report_type = st.selectbox(
        "Select intelligence report",
        ["🎯 Striking Distance Optimization Report", "💡 Rich Snippet & Search Appearance Leaderboard"]
    )
    
    if report_type == "🎯 Striking Distance Optimization Report":
        st.markdown("#### Pages and Queries Ranking on Page 2 (Positions 11–20) or Striking Distance (4–10)")
        st.markdown("Optimize these queries/pages because they have search impressions, but just need a boost in ranking or CTR to generate substantial clicks.")
        
        col_sel1, col_sel2 = st.columns(2)
        with col_sel1:
            intel_type = st.radio("Target Metric Base", ["Queries", "Pages"])
        with col_sel2:
            rank_range = st.slider("Select Position Range", 4.0, 20.0, (4.0, 15.0))
            
        df_target = queries_df if intel_type == "Queries" else pages_df
        label_col = 'Top queries' if intel_type == "Queries" else 'Top pages'
        
        striking_df = df_target[
            (df_target['Position'] >= rank_range[0]) & 
            (df_target['Position'] <= rank_range[1])
        ].copy()
        
        # Sort by impressions to focus on search volume potential
        striking_df = striking_df.sort_values('Impressions', ascending=False)
        striking_df['CTR'] = striking_df['CTR'] * 100
        
        st.dataframe(
            striking_df.style.format({
                "Clicks": "{:,.0f}",
                "Impressions": "{:,.0f}",
                "CTR": "{:.2f}%",
                "Position": "{:.2f}"
            }),
            use_container_width=True
        )
        
    elif report_type == "💡 Rich Snippet & Search Appearance Leaderboard":
        sa_df = gsc_data.get('search_appearance')
        if sa_df is not None:
            st.markdown("#### Search Appearance Optimization")
            st.markdown("Identify which search features (snippets, video, review stars) are performing best.")
            
            # Format and display
            sa_formatted = sa_df.copy()
            sa_formatted['CTR'] = sa_formatted['CTR'] * 100
            
            st.dataframe(
                sa_formatted.style.format({
                    "Clicks": "{:,.0f}",
                    "Impressions": "{:,.0f}",
                    "CTR": "{:.2f}%",
                    "Position": "{:.2f}"
                }),
                use_container_width=True
            )
            
            # Plot
            fig_sa = px.bar(
                sa_df,
                x='Search Appearance',
                y='Clicks',
                color='CTR',
                title="Clicks generated by Special Search Appearances"
            )
            st.plotly_chart(fig_sa, use_container_width=True)
        else:
            st.info("No search appearance data found in the export sheet.")