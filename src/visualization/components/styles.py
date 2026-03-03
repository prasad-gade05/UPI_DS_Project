"""Custom CSS and styled components for the dashboard."""

import streamlit as st

CUSTOM_CSS = """
<style>
/* Hide default sidebar completely */
[data-testid="stSidebar"] { display: none; }

/* Tighter top padding */
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    max-width: 100%;
}

/* KPI metrics */
[data-testid="stMetricValue"] {
    font-size: 1.8rem;
    font-weight: 700;
}
[data-testid="stMetricLabel"] {
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #555;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 600;
    font-size: 0.82rem;
}
.stTabs [aria-selected="true"] {
    background-color: #6C63FF !important;
    color: white !important;
}

/* Insight callout boxes */
.insight-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.2rem 1.5rem;
    border-radius: 12px;
    margin: 0.8rem 0;
    line-height: 1.6;
    font-size: 0.95rem;
}
.insight-warning {
    background: linear-gradient(135deg, #f5af19 0%, #f12711 100%);
    color: white;
    padding: 1.2rem 1.5rem;
    border-radius: 12px;
    margin: 0.8rem 0;
    line-height: 1.6;
}
.insight-success {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    color: white;
    padding: 1.2rem 1.5rem;
    border-radius: 12px;
    margin: 0.8rem 0;
    line-height: 1.6;
}

/* Gradient divider */
.gradient-divider {
    height: 3px;
    background: linear-gradient(90deg, #6C63FF 0%, #764ba2 50%, #f093fb 100%);
    border: none;
    border-radius: 2px;
    margin: 1.2rem 0;
}

/* Scale metric card */
.scale-card {
    text-align: center;
    padding: 1.2rem 0.8rem;
    background: #f8f9fa;
    border-radius: 12px;
    border-left: 4px solid #6C63FF;
}
.scale-card h2 {
    font-size: 1.8rem;
    font-weight: 700;
    color: #6C63FF;
    margin: 0 0 0.2rem 0;
}
.scale-card p {
    font-size: 0.85rem;
    color: #666;
    margin: 0;
}

/* Hero header */
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 0.1rem;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: #666;
    margin-top: 0;
}

/* About card */
.about-card {
    background: white;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}

/* DataFrames */
.stDataFrame { border-radius: 8px; }

/* Section headers */
.section-header {
    font-size: 1.3rem;
    font-weight: 600;
    color: #1a1a2e;
    border-bottom: 2px solid #6C63FF;
    padding-bottom: 0.3rem;
    margin: 1rem 0 0.5rem 0;
}
</style>
"""


def inject_custom_css():
    """Inject custom CSS into the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_insight(text: str, variant: str = "default"):
    """Render a styled insight callout box."""
    css_class = {
        "default": "insight-box",
        "warning": "insight-warning",
        "success": "insight-success",
    }.get(variant, "insight-box")
    st.markdown(f'<div class="{css_class}">{text}</div>', unsafe_allow_html=True)


def render_divider():
    """Render a gradient divider line."""
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


def render_scale_card(value: str, label: str):
    """Render a scale metric card."""
    st.markdown(
        f'<div class="scale-card"><h2>{value}</h2><p>{label}</p></div>',
        unsafe_allow_html=True,
    )


def render_section_header(text: str):
    """Render a styled section header."""
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)
