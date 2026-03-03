"""
UPI Analytics Platform — Streamlit Web Application

Production-grade interactive dashboard analyzing India's UPI ecosystem.
Deployed on Streamlit Community Cloud.
"""

import sys
from pathlib import Path

_project_root = str(Path(__file__).resolve().parents[2])
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st

from src.visualization.components.data_loader import load_all_data, get_available_years
from src.visualization.components.styles import inject_custom_css, render_divider
from src.visualization.pages import (
    overview,
    executive_summary,
    growth_trends,
    market_share,
    app_dynamics,
    geographic_insights,
    district_deep_dive,
    cash_displacement,
    forecasting,
    users_devices,
    methodology,
)

# ── Page Configuration ───────────────────────────────────────────────
st.set_page_config(
    page_title="UPI Analytics Platform",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_custom_css()

# ── Data Loading ─────────────────────────────────────────────────────
data = load_all_data()

if not data:
    st.error(
        "🚫 **No data found.** The Gold layer exports are not available.\n\n"
        "Run the data pipeline first:\n"
        "```bash\n"
        "make all   # or: python -m src.pipeline.run_pipeline --stage all\n"
        "```"
    )
    st.stop()

# ── Header Bar ───────────────────────────────────────────────────────
col_title, col_filter = st.columns([3, 1])

with col_title:
    st.markdown(
        '<h1 class="hero-title">🇮🇳 UPI Analytics Platform</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="hero-subtitle">'
        "Comprehensive Analysis of India's Digital Payments Ecosystem &nbsp;|&nbsp; "
        "3 Data Sources &nbsp;•&nbsp; 788 Districts &nbsp;•&nbsp; 42 Months"
        "</p>",
        unsafe_allow_html=True,
    )

with col_filter:
    years = get_available_years(data)
    year_range = st.slider(
        "📅 Year Range",
        min_value=min(years),
        max_value=max(years),
        value=(min(years), max(years)),
        key="global_year_filter",
    )

render_divider()

# ── Tab Navigation ───────────────────────────────────────────────────
TAB_LABELS = [
    "🇮🇳 Overview",
    "📊 Executive Summary",
    "📈 Growth & Trends",
    "🏢 Market Concentration",
    "📱 App Dynamics",
    "🗺️ Geographic Analysis",
    "📍 District Deep Dive",
    "💰 Cash vs Digital",
    "🔮 Forecasting",
    "👥 Users & Devices",
    "📋 Methodology",
]

TAB_PAGES = [
    overview,
    executive_summary,
    growth_trends,
    market_share,
    app_dynamics,
    geographic_insights,
    district_deep_dive,
    cash_displacement,
    forecasting,
    users_devices,
    methodology,
]

tabs = st.tabs(TAB_LABELS)

for tab, page in zip(tabs, TAB_PAGES):
    with tab:
        try:
            page.render(data, year_range)
        except Exception as e:
            st.error(f"⚠️ Error rendering this section: {e}")
            import traceback
            st.code(traceback.format_exc(), language="text")
