"""Custom CSS and styled components for the dashboard."""

import streamlit as st

CUSTOM_CSS = """
<style>
/* ===================================================================
   UPI Analytics Platform — Professional Design System
   =================================================================== */

/* --- Reset & Foundation --- */
[data-testid="stSidebar"] { display: none; }

.main .block-container {
    padding-top: 0.75rem;
    padding-bottom: 2rem;
    max-width: 100%;
}

/* --- Dashboard Header Banner --- */
.dashboard-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #1e40af 100%);
    color: white;
    padding: 1.5rem 2rem;
    border-radius: 10px;
    margin-bottom: 0.75rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
}
.dashboard-title {
    font-size: 1.75rem;
    font-weight: 800;
    color: white;
    margin: 0 0 0.25rem 0;
    letter-spacing: -0.5px;
    line-height: 1.2;
}
.dashboard-subtitle {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.75);
    margin: 0;
    font-weight: 400;
    line-height: 1.4;
}
.header-badges {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.75rem;
    flex-wrap: wrap;
}
.header-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(4px);
    color: rgba(255, 255, 255, 0.9);
    padding: 0.3rem 0.75rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 500;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

/* --- Tab Navigation --- */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background-color: transparent;
    border-bottom: 2px solid #e2e8f0;
    padding: 0;
    border-radius: 0;
    overflow-x: auto;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0;
    padding: 0.6rem 0.9rem;
    font-weight: 500;
    font-size: 0.8rem;
    color: #64748b;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    white-space: nowrap;
    transition: color 0.15s ease, border-color 0.15s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #1e3a5f;
}
.stTabs [aria-selected="true"] {
    background-color: transparent !important;
    color: #0f172a !important;
    border-bottom-color: #2563eb !important;
    font-weight: 600;
}

/* --- KPI Metric Cards --- */
[data-testid="stMetricValue"] {
    font-size: 1.5rem;
    font-weight: 700;
    color: #0f172a;
}
[data-testid="stMetricLabel"] {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: #64748b;
}
[data-testid="stMetricDelta"] {
    font-size: 0.78rem;
}
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-top: 3px solid #2563eb;
    border-radius: 8px;
    padding: 0.85rem 1rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

/* --- Insight Callout Boxes --- */
.insight-box {
    background: #eff6ff;
    color: #1e3a5f;
    padding: 1rem 1.25rem;
    border-radius: 8px;
    margin: 0.75rem 0;
    line-height: 1.65;
    font-size: 0.9rem;
    border: 1px solid #bfdbfe;
    border-left: 4px solid #2563eb;
}
.insight-box b, .insight-box strong { color: #1e40af; }

.insight-warning {
    background: #fffbeb;
    color: #78350f;
    padding: 1rem 1.25rem;
    border-radius: 8px;
    margin: 0.75rem 0;
    line-height: 1.65;
    font-size: 0.9rem;
    border: 1px solid #fde68a;
    border-left: 4px solid #d97706;
}
.insight-warning b, .insight-warning strong { color: #92400e; }

.insight-success {
    background: #ecfdf5;
    color: #064e3b;
    padding: 1rem 1.25rem;
    border-radius: 8px;
    margin: 0.75rem 0;
    line-height: 1.65;
    font-size: 0.9rem;
    border: 1px solid #a7f3d0;
    border-left: 4px solid #059669;
}
.insight-success b, .insight-success strong { color: #065f46; }

/* --- Divider --- */
.gradient-divider {
    height: 1px;
    background: #e2e8f0;
    border: none;
    border-radius: 0;
    margin: 1.25rem 0;
}

/* --- Scale Metric Cards --- */
.scale-card {
    text-align: center;
    padding: 1.1rem 0.75rem;
    background: #ffffff;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    border-top: 3px solid #2563eb;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}
.scale-card h2 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 0.25rem 0;
}
.scale-card p {
    font-size: 0.72rem;
    color: #64748b;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    font-weight: 600;
}

/* --- Hero Header (used in tab pages) --- */
.hero-title {
    font-size: 1.75rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0.2rem;
    letter-spacing: -0.5px;
    line-height: 1.2;
}
.hero-subtitle {
    font-size: 0.92rem;
    color: #64748b;
    margin-top: 0;
    line-height: 1.5;
}

/* --- Page Header (tab-level title) --- */
.page-header {
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #e2e8f0;
}
.page-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 0.15rem 0;
    letter-spacing: -0.3px;
}
.page-subtitle {
    font-size: 0.88rem;
    color: #64748b;
    margin: 0;
    font-weight: 400;
}

/* --- Section Headers --- */
.section-header {
    font-size: 1.05rem;
    font-weight: 700;
    color: #0f172a;
    border-bottom: none;
    border-left: 3px solid #2563eb;
    padding: 0.25rem 0 0.25rem 0.75rem;
    margin: 1.25rem 0 0.6rem 0;
    letter-spacing: -0.2px;
}

/* --- About / Info Cards --- */
.about-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 1.25rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    margin-bottom: 0.75rem;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
    height: 100%;
}
.about-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transform: translateY(-1px);
}
.about-card h4 {
    color: #0f172a;
    margin: 0 0 0.5rem 0;
    font-size: 0.95rem;
    font-weight: 700;
}
.about-card p {
    margin: 0 0 0.4rem 0;
}

/* --- Chart & Visualization Containers --- */
[data-testid="stPlotlyChart"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.75rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.03);
    margin-bottom: 0.5rem;
}

[data-testid="stVegaLiteChart"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.75rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.03);
    margin-bottom: 0.5rem;
}

/* --- Data Tables --- */
.stDataFrame {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.03);
    overflow: hidden;
}

/* --- Expander --- */
[data-testid="stExpander"] {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
}

/* --- Footer --- */
.footer-text {
    text-align: center;
    color: #94a3b8;
    font-size: 0.8rem;
    padding: 1.25rem 0 0.5rem 0;
    border-top: 1px solid #e2e8f0;
    margin-top: 1.5rem;
}
.footer-text a {
    color: #2563eb;
    text-decoration: none;
    font-weight: 500;
}
.footer-text a:hover {
    text-decoration: underline;
}

/* --- Form Labels --- */
[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label,
[data-testid="stSlider"] label,
[data-testid="stRadio"] label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

/* --- Pipeline Visualization --- */
.pipeline-flow {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    flex-wrap: wrap;
    margin: 1rem 0;
}
.pipeline-stage {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 0.6rem 1.2rem;
    font-size: 0.85rem;
    font-weight: 600;
    color: #1e293b;
    text-align: center;
}
.pipeline-arrow {
    color: #94a3b8;
    font-size: 1.2rem;
    padding: 0 0.5rem;
}
.pipeline-stage.active {
    background: #2563eb;
    color: white;
    border-color: #2563eb;
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
    """Render a styled section header with left accent."""
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = ""):
    """Render a professional page-level header."""
    html = f'<div class="page-header"><h2 class="page-title">{title}</h2>'
    if subtitle:
        html += f'<p class="page-subtitle">{subtitle}</p>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
