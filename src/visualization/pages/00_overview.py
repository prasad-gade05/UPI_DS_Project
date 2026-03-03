"""Tab 0: Overview — Hero landing section with project scale and data sources."""

import streamlit as st
import pandas as pd

from src.visualization.components.styles import (
    render_insight,
    render_divider,
    render_scale_card,
    render_section_header,
)
from src.visualization.components.kpi_cards import format_billions, format_lakh_crores


def render(data: dict[str, pd.DataFrame], year_range: tuple[int, int]) -> None:
    """Render the Overview / Hero landing tab."""

    # ── Hero Section ─────────────────────────────────────────────────
    st.markdown(
        '<div class="hero-title">🇮🇳 UPI Analytics Platform</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-subtitle">'
        "A production-grade data engineering &amp; analytics platform dissecting "
        "India's Unified Payments Interface — the world's largest real-time "
        "digital payment system processing 14 Bn+ transactions per month."
        "</div>",
        unsafe_allow_html=True,
    )

    render_divider()

    # ── Scale Metrics ────────────────────────────────────────────────
    render_section_header("📐 Project Scale")

    # Compute metrics from available data
    total_data_points = sum(len(df) for df in data.values())

    geo = data.get("dim_geography", pd.DataFrame())
    n_states = geo["state_name"].nunique() if "state_name" in geo.columns else 36
    n_districts = geo["district_name"].nunique() if "district_name" in geo.columns else 788

    apps = data.get("dim_app", pd.DataFrame())
    n_apps = len(apps) if not apps.empty else 7

    # Time span from multiple sources
    years_set: set[int] = set()
    for key in ("fact_upi_transactions", "v_monthly_summary", "npci_monthly_volumes"):
        df = data.get(key, pd.DataFrame())
        if "year" in df.columns:
            years_set.update(df["year"].dropna().astype(int).unique())
    if years_set:
        time_span = f"{min(years_set)}–{max(years_set)}"
    else:
        time_span = f"{year_range[0]}–{year_range[1]}"

    # Total transaction volume
    npci = data.get("npci_monthly_volumes", pd.DataFrame())
    if "transaction_volume_billions" in npci.columns:
        total_vol = npci["transaction_volume_billions"].sum()
        vol_label = f"{total_vol:.0f} Bn"
    else:
        fact = data.get("fact_upi_transactions", pd.DataFrame())
        total_vol = fact["txn_count"].sum() if "txn_count" in fact.columns else 0
        vol_label = format_billions(total_vol)

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        render_scale_card(f"{total_data_points:,}", "Total Data Points")
    with col2:
        render_scale_card(str(n_states), "States & UTs")
    with col3:
        render_scale_card(str(n_districts), "Districts Mapped")
    with col4:
        render_scale_card(str(n_apps), "UPI Apps Analyzed")
    with col5:
        render_scale_card(time_span, "Time Span")
    with col6:
        render_scale_card(vol_label, "Txn Volume Processed")

    st.markdown("")  # spacing

    # ── About This Project ───────────────────────────────────────────
    render_section_header("📖 About This Project")

    with st.expander("**Learn more about this project →**", expanded=False):
        st.markdown(
            """
**UPI Analytics Platform** is a production-grade data engineering and analytics
project that analyzes India's Unified Payments Interface (UPI) ecosystem — the
world's largest real-time digital payment system.

#### 🏗️ Architecture

Built on the **Medallion Architecture** (Bronze → Silver → Gold), the platform
ingests raw data from three authoritative sources, cleans and standardizes it
through a multi-stage pipeline, and produces analytics-ready datasets that power
this interactive dashboard.

| Layer | Purpose | Output |
|-------|---------|--------|
| **Bronze** | Raw ingestion — PhonePe Pulse API, NPCI CSVs, RBI DBIE exports | Raw Parquet files |
| **Silver** | Cleaning, deduplication, schema normalization, feature engineering | Standardized dimensions & facts |
| **Gold** | Analytical models, aggregations, forecasts, clustering | Dashboard-ready exports |

#### 📊 Scale & Coverage

- **20,000+** district-level transaction records across **788 districts** and **36 states/UTs**
- **42 months** of continuous monthly transaction data (2021–2024)
- **3 ML/statistical models**: Prophet time-series forecasting, ARIMA modeling,
  K-Means geographic clustering
- **7 UPI applications** tracked with market share decomposition
- **5 transaction categories** analyzed (P2P, P2M, bill payments, financial services, others)

#### 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Data Processing | **Python**, **Pandas**, **DuckDB** |
| Visualization | **Streamlit**, **Plotly** |
| Forecasting | **Prophet**, **statsmodels (ARIMA)** |
| Clustering | **scikit-learn (K-Means)** |
| Pipeline | **Make**, modular Python scripts |
| Data Format | **Apache Parquet** (columnar storage) |

#### 📚 Data Sources

1. **PhonePe Pulse** — Open-source repository with district-level UPI adoption
   data, user registrations, and app-open metrics.
2. **NPCI (National Payments Corporation of India)** — Official monthly
   transaction volumes and values for the entire UPI network.
3. **RBI DBIE (Database on Indian Economy)** — Macroeconomic indicators
   including currency-in-circulation for cash displacement analysis.
""",
            unsafe_allow_html=True,
        )

    # ── Why This Matters ─────────────────────────────────────────────
    render_section_header("🌍 Why This Matters")

    render_insight(
        "💡 <strong>UPI processed 14.04 Bn transactions worth ₹20.64 Lakh Crore "
        "in a single month (Dec 2024)</strong> — surpassing Visa and Mastercard "
        "combined in transaction volume. India's real-time payment system now "
        "accounts for over 80% of all retail digital payments in the country, "
        "reshaping a $3 trillion economy's relationship with money. Understanding "
        "this ecosystem through data isn't just an academic exercise — it's "
        "analyzing the infrastructure powering financial inclusion for 1.4 billion people."
    )

    st.markdown("")  # spacing

    # ── Data Sources ─────────────────────────────────────────────────
    render_section_header("📚 Data Sources")

    src1, src2, src3 = st.columns(3)

    with src1:
        st.markdown(
            """
<div class="about-card">
<h4>📱 PhonePe Pulse</h4>
<p style="font-size:0.9rem; color:#555;">
Open-source dataset with district-level UPI adoption data, quarterly user
registrations, and app-open metrics across all Indian states and districts.
</p>
<p style="font-size:0.8rem; color:#888;">
<a href="https://github.com/PhonePe/pulse" target="_blank">github.com/PhonePe/pulse</a>
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with src2:
        st.markdown(
            """
<div class="about-card">
<h4>🏦 NPCI Statistics</h4>
<p style="font-size:0.9rem; color:#555;">
Official monthly UPI transaction volumes and values published by the National
Payments Corporation of India — the umbrella organization operating UPI.
</p>
<p style="font-size:0.8rem; color:#888;">
<a href="https://www.npci.org.in/what-we-do/upi/upi-ecosystem-statistics" target="_blank">npci.org.in</a>
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with src3:
        st.markdown(
            """
<div class="about-card">
<h4>🇮🇳 RBI DBIE</h4>
<p style="font-size:0.9rem; color:#555;">
Reserve Bank of India's Database on Indian Economy — macroeconomic data
including currency-in-circulation used for cash displacement analysis.
</p>
<p style="font-size:0.8rem; color:#888;">
<a href="https://dbie.rbi.org.in" target="_blank">dbie.rbi.org.in</a>
</p>
</div>
""",
            unsafe_allow_html=True,
        )
