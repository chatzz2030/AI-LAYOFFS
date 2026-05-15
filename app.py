import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re
from collections import Counter

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Layoffs 2026 Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS for MNC Premium Look ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Clean white background and typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #fcfcfc;
        color: #1a1a1a;
    }

    /* KPI card styling */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 30px;
    }
    .kpi-card {
        flex: 1;
        background: #ffffff;
        border: 1px solid #eaebec;
        border-radius: 8px;
        padding: 20px 15px;
        text-align: left;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.08);
    }
    .kpi-value { 
        font-size: 2.2rem; 
        font-weight: 600; 
        color: #111827; 
        margin: 5px 0 0 0; 
        line-height: 1.2;
    }
    .kpi-label { 
        font-size: 0.85rem; 
        font-weight: 500;
        color: #6b7280; 
        margin: 0; 
        text-transform: uppercase; 
        letter-spacing: 0.5px;
    }

    /* Section headers */
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #111827;
        margin: 30px 0 15px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #eaebec;
    }

    /* Header styling */
    .dashboard-header {
        padding: 40px 0 20px 0;
        border-bottom: 1px solid #eaebec;
        margin-bottom: 30px;
    }
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #111827;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .dashboard-subtitle {
        font-size: 1.1rem;
        color: #6b7280;
        margin-top: 8px;
        font-weight: 400;
    }

    /* Hide streamlit branding and sidebar toggle */
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="collapsedControl"] { display: none; }
    .block-container { padding-top: 0rem; padding-bottom: 2rem; max-width: 1400px; }
    
    /* Table styling */
    .stDataFrame { border-radius: 8px; overflow: hidden; border: 1px solid #eaebec; }
</style>
""", unsafe_allow_html=True)

# ── Load Data ───────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("tech_layoffs_2026_tracker.csv")
    df['layoff_date'] = pd.to_datetime(df['layoff_date'])
    return df

df = load_data()

# ── Header ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dashboard-header">
    <h1 class="dashboard-title">Global Tech Layoffs & AI Impact Report</h1>
    <p class="dashboard-subtitle">Executive Summary · Q1 2026 · Comprehensive Industry Analysis</p>
</div>
""", unsafe_allow_html=True)

# ── Top-Level KPIs ──────────────────────────────────────────────────────────────
total_jobs = df['jobs_cut'].sum()
companies_count = len(df)
ai_ratio = round(df['ai_cited'].sum() / len(df) * 100) if len(df) > 0 else 0
avg_wf_cut = round(df['pct_workforce_cut'].mean(), 1) if len(df) > 0 else 0
total_ai_inv = df['simultaneous_ai_investment_bn'].sum()

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <p class="kpi-label">Total Jobs Displaced</p>
        <p class="kpi-value">{total_jobs:,}</p>
    </div>
    <div class="kpi-card">
        <p class="kpi-label">Companies Affected</p>
        <p class="kpi-value">{companies_count}</p>
    </div>
    <div class="kpi-card">
        <p class="kpi-label">AI-Driven Restructuring</p>
        <p class="kpi-value">{ai_ratio}%</p>
    </div>
    <div class="kpi-card">
        <p class="kpi-label">Avg. Workforce Reduction</p>
        <p class="kpi-value">{avg_wf_cut}%</p>
    </div>
    <div class="kpi-card">
        <p class="kpi-label">Simultaneous AI Investment</p>
        <p class="kpi-value">${total_ai_inv:.1f}B</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Define corporate color palette
corp_colors = ['#1f2937', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#6366f1']
ai_colors = {True: '#ef4444', False: '#3b82f6'}

# ── Row 1: Timeline & Sector Overview ───────────────────────────────────────────
st.markdown('<div class="section-title">Macro Trends & Industry Impact</div>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    timeline = df.groupby('layoff_date')['jobs_cut'].sum().reset_index()
    timeline['cumulative'] = timeline['jobs_cut'].cumsum()

    fig_time = make_subplots(specs=[[{"secondary_y": True}]])
    fig_time.add_trace(go.Bar(
        x=timeline['layoff_date'], y=timeline['jobs_cut'],
        name="Daily Job Reductions", marker_color="#cbd5e1", opacity=0.8
    ), secondary_y=False)
    fig_time.add_trace(go.Scatter(
        x=timeline['layoff_date'], y=timeline['cumulative'],
        name="Cumulative Reductions", line=dict(color="#1f2937", width=3), mode="lines"
    ), secondary_y=True)
    
    fig_time.update_layout(
        title=dict(text="Layoff Progression (Q1 2026)", font=dict(size=16, color="#111827")),
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=50, b=0),
        height=380,
        hovermode="x unified"
    )
    st.plotly_chart(fig_time, use_container_width=True)

with col2:
    sector_sum = df.groupby('sector')['jobs_cut'].sum().reset_index().sort_values('jobs_cut', ascending=False).head(6)
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=sector_sum['sector'], 
        values=sector_sum['jobs_cut'],
        hole=.4,
        marker_colors=corp_colors
    )])
    
    fig_pie.update_layout(
        title=dict(text="Impact by Tech Sector", font=dict(size=16, color="#111827")),
        template="plotly_white",
        margin=dict(l=0, r=0, t=50, b=0),
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent')
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Row 2: Company Spotlight & NLP Analysis ─────────────────────────────────────
st.markdown('<div class="section-title">Corporate Exposure & Restructuring Drivers</div>', unsafe_allow_html=True)
col3, col4 = st.columns([1, 1])

with col3:
    top10 = df.nlargest(10, 'jobs_cut').sort_values('jobs_cut', ascending=True)
    top10['color'] = top10['ai_cited'].map(ai_colors)
    
    fig_bar = go.Figure(go.Bar(
        y=top10['company'], x=top10['jobs_cut'],
        orientation='h',
        marker_color=top10['color'],
        text=top10['jobs_cut'].apply(lambda x: f"{x:,}"),
        textposition='outside',
        textfont=dict(size=11, color='#4b5563')
    ))
    
    fig_bar.update_layout(
        title=dict(text="Top 10 Entities by Absolute Job Loss", font=dict(size=16, color="#111827")),
        template="plotly_white",
        xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title="Jobs Cut"),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=40, t=50, b=0),
        height=400,
        annotations=[
            dict(x=1, y=1.05, xref='paper', yref='paper',
                 text="<span style='color:#ef4444'>● AI-Cited</span>  <span style='color:#3b82f6'>● Non-AI</span>",
                 showarrow=False, font=dict(size=12))
        ]
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col4:
    # Process text for Roles Most Affected
    def get_top_keywords(text_series, top_n=8):
        words = []
        for text in text_series.dropna():
            words.extend([w.lower().strip() for w in re.split(r'\\W+', str(text)) if len(w) > 3])
        # Filter some common generic words if needed
        stopwords = {'from', 'roles', 'with', 'teams', 'workers', 'across', 'related'}
        words = [w for w in words if w not in stopwords]
        return Counter(words).most_common(top_n)

    top_roles = get_top_keywords(df['roles_most_affected'], 8)
    roles_df = pd.DataFrame(top_roles, columns=['Keyword', 'Frequency']).sort_values('Frequency', ascending=True)

    fig_roles = go.Figure(go.Bar(
        y=roles_df['Keyword'].str.title(), x=roles_df['Frequency'],
        orientation='h',
        marker_color='#10b981',
        text=roles_df['Frequency'],
        textposition='outside'
    ))

    fig_roles.update_layout(
        title=dict(text="Most Disrupted Roles (Keyword Frequency)", font=dict(size=16, color="#111827")),
        template="plotly_white",
        xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title="Mentions"),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=40, t=50, b=0),
        height=400
    )
    st.plotly_chart(fig_roles, use_container_width=True)

# ── Row 3: Financial Correlation & Regional Distribution ─────────────────────────
st.markdown('<div class="section-title">Financial Indicators & Geographic Distribution</div>', unsafe_allow_html=True)
col5, col6 = st.columns([1, 1])

with col5:
    fig_scatter = px.scatter(
        df, x='pct_workforce_cut', y='stock_change_day_pct',
        size='jobs_cut', color='ai_cited',
        color_discrete_map=ai_colors,
        hover_name='company',
        labels={
            'pct_workforce_cut': 'Workforce Reduction (%)',
            'stock_change_day_pct': 'Market Reaction (Day 1 %)',
            'ai_cited': 'AI Cited'
        }
    )
    fig_scatter.add_hline(y=0, line_dash="dash", line_color="#9ca3af", opacity=0.5)
    
    fig_scatter.update_layout(
        title=dict(text="Market Reaction vs. Severity of Cuts", font=dict(size=16, color="#111827")),
        template="plotly_white",
        xaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
        yaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
        margin=dict(l=0, r=0, t=50, b=0),
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col6:
    region_data = df.groupby('region').agg(
        total_jobs=('jobs_cut', 'sum')
    ).reset_index().sort_values('total_jobs', ascending=True)

    fig_region = go.Figure(go.Bar(
        y=region_data['region'], x=region_data['total_jobs'],
        orientation='h', 
        marker_color='#6366f1',
        text=region_data['total_jobs'].apply(lambda x: f"{x:,}"),
        textposition='outside'
    ))
    
    fig_region.update_layout(
        title=dict(text="Geographic Distribution of Job Losses", font=dict(size=16, color="#111827")),
        template="plotly_white",
        xaxis=dict(showgrid=True, gridcolor='#f1f5f9', title="Jobs Cut"),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=40, t=50, b=0),
        height=380
    )
    st.plotly_chart(fig_region, use_container_width=True)

# ── Raw Data Table ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Comprehensive Data Extract</div>', unsafe_allow_html=True)

# Clean up column names for presentation
display_cols = ['company', 'layoff_date', 'jobs_cut', 'pct_workforce_cut', 'sector', 
                'region', 'ai_cited', 'simultaneous_ai_investment_bn', 'stock_reaction']
display_df = df[display_cols].sort_values('jobs_cut', ascending=False).reset_index(drop=True)
display_df.columns = ['Entity', 'Announcement Date', 'Jobs Affected', 'Workforce %', 'Sector', 
                      'Region', 'AI Driver', 'Concurrent AI Inv. ($B)', 'Market Consensus']

display_df['Announcement Date'] = display_df['Announcement Date'].dt.strftime('%Y-%m-%d')

st.dataframe(
    display_df,
    use_container_width=True,
    height=400,
    hide_index=True
)


