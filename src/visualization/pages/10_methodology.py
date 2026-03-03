"""Tab 10: Methodology & Data Quality — Project architecture, data sources,
analytical models, technology stack, limitations, and glossary."""

import streamlit as st
import pandas as pd

from src.visualization.components.styles import (
    render_insight,
    render_divider,
    render_section_header,
)


# ── Helper ───────────────────────────────────────────────────────────────────

def _null_pct(df: pd.DataFrame, columns: list[str]) -> dict[str, float]:
    """Return null percentage for each column present in *df*."""
    result: dict[str, float] = {}
    for col in columns:
        if col in df.columns:
            result[col] = round(df[col].isna().sum() / max(len(df), 1) * 100, 2)
    return result


# ── Main render ──────────────────────────────────────────────────────────────

def render(data: dict[str, pd.DataFrame], year_range: tuple[int, int]) -> None:
    """Render the Methodology & Data Quality page."""

    st.markdown(
        '<div class="hero-title">📋 Methodology & Data Quality</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hero-subtitle">'
        "Project architecture, analytical framework, data provenance, "
        "and known limitations — everything needed to evaluate this work."
        "</div>",
        unsafe_allow_html=True,
    )

    render_divider()

    # ════════════════════════════════════════════════════════════════════
    # 1. Data Pipeline Architecture
    # ════════════════════════════════════════════════════════════════════
    render_section_header("🏗️ Data Pipeline Architecture")

    st.markdown(
        """
This platform follows the **Medallion Architecture** — a proven pattern for
progressive data refinement used in modern lakehouse systems.
"""
    )

    st.code(
        "  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────────┐\n"
        "  │  🥉 Bronze   │───▶│  🥈 Silver    │───▶│  🥇 Gold     │───▶│  📊 Dashboard│\n"
        "  │  (Raw Data)  │    │  (Cleaned)    │    │  (Analytics) │    │  (Streamlit) │\n"
        "  └─────────────┘    └──────────────┘    └──────────────┘    └─────────────┘",
        language=None,
    )

    layer1, layer2, layer3, layer4 = st.columns(4)

    with layer1:
        st.markdown(
            """
<div class="about-card">
<h4>🥉 Bronze Layer</h4>
<p style="font-size:0.88rem; color:#555;">
Raw ingestion from PhonePe Pulse GitHub API, NPCI web-scraped CSVs, and
RBI DBIE exports. Data is stored as-is in Parquet format with full lineage
metadata.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with layer2:
        st.markdown(
            """
<div class="about-card">
<h4>🥈 Silver Layer</h4>
<p style="font-size:0.88rem; color:#555;">
Schema normalization, deduplication, null handling, type casting, and
date standardization. Dimensional modeling produces star-schema facts
and dimensions.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with layer3:
        st.markdown(
            """
<div class="about-card">
<h4>🥇 Gold Layer</h4>
<p style="font-size:0.88rem; color:#555;">
Analytical models, aggregations, forecasts (Prophet + ARIMA), clustering
(K-Means), market concentration (HHI), and cash displacement analysis.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with layer4:
        st.markdown(
            """
<div class="about-card">
<h4>📊 Dashboard</h4>
<p style="font-size:0.88rem; color:#555;">
Interactive Streamlit application with Plotly visualizations. Reads
Gold-layer Parquet files and renders 10+ analytical views with
real-time filtering.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    render_divider()

    # ════════════════════════════════════════════════════════════════════
    # 2. Data Sources
    # ════════════════════════════════════════════════════════════════════
    render_section_header("📚 Data Sources")

    pp_records = sum(
        len(data.get(k, pd.DataFrame()))
        for k in (
            "phonepe_user_aggregates",
            "phonepe_device_brands",
            "phonepe_insurance",
            "phonepe_top_transactions",
        )
    )
    npci_records = len(data.get("npci_monthly_volumes", pd.DataFrame()))
    rbi_records = sum(
        len(data.get(k, pd.DataFrame()))
        for k in ("rbi_atm_transactions", "rbi_currency_circulation")
    )

    sources_df = pd.DataFrame(
        {
            "Source": [
                "PhonePe Pulse",
                "NPCI (National Payments Corporation)",
                "RBI DBIE (Database on Indian Economy)",
            ],
            "Description": [
                "District-level UPI transaction aggregates, user registrations, device analytics, and insurance data",
                "Official monthly UPI transaction volumes and values for the entire network",
                "Currency-in-circulation, ATM transaction data, and macroeconomic indicators",
            ],
            "Update Frequency": ["Quarterly", "Monthly", "Quarterly"],
            "Ingestion Method": ["GitHub API", "Web Scraping", "API / Manual Download"],
            "Records": [
                f"{pp_records:,}" if pp_records else "—",
                f"{npci_records:,}" if npci_records else "—",
                f"{rbi_records:,}" if rbi_records else "—",
            ],
        }
    )

    st.dataframe(sources_df, use_container_width=True, hide_index=True)

    render_divider()

    # ════════════════════════════════════════════════════════════════════
    # 3. Data Quality Metrics
    # ════════════════════════════════════════════════════════════════════
    render_section_header("🔍 Data Quality Metrics")

    total_tables = len(data)
    total_records = sum(len(df) for df in data.values())

    # Derive date range from data
    years_set: set[int] = set()
    for key in ("fact_upi_transactions", "v_monthly_summary", "npci_monthly_volumes", "dim_date"):
        df = data.get(key, pd.DataFrame())
        if "year" in df.columns:
            years_set.update(df["year"].dropna().astype(int).unique())
    date_coverage = (
        f"{min(years_set)}–{max(years_set)}" if years_set else f"{year_range[0]}–{year_range[1]}"
    )

    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Tables Loaded", f"{total_tables}")
    q2.metric("Total Records", f"{total_records:,}")
    q3.metric("Date Range", date_coverage)

    # Null analysis on fact table
    fact_df = data.get("fact_upi_transactions", pd.DataFrame())
    if not fact_df.empty:
        key_cols = ["txn_count", "txn_value", "year", "quarter", "state_name"]
        nulls = _null_pct(fact_df, key_cols)
        avg_null = round(sum(nulls.values()) / max(len(nulls), 1), 2) if nulls else 0.0
        q4.metric("Avg Null % (Fact Table)", f"{avg_null}%")

        st.markdown("**Column-level null analysis** — `fact_upi_transactions`:")
        null_df = pd.DataFrame(
            [
                {"Column": col, "Null %": pct, "Status": "✅ Clean" if pct < 1 else "⚠️ Review"}
                for col, pct in nulls.items()
            ]
        )
        st.dataframe(null_df, use_container_width=True, hide_index=True)
    else:
        q4.metric("Avg Null % (Fact Table)", "N/A")

    # Table inventory
    with st.expander("📦 **Full table inventory**", expanded=False):
        inventory = pd.DataFrame(
            [
                {"Table": name, "Rows": f"{len(df):,}", "Columns": len(df.columns)}
                for name, df in sorted(data.items())
            ]
        )
        st.dataframe(inventory, use_container_width=True, hide_index=True)

    render_insight(
        f"📊 The pipeline successfully loaded <strong>{total_tables} tables</strong> "
        f"comprising <strong>{total_records:,} records</strong> spanning "
        f"<strong>{date_coverage}</strong>. All datasets pass through automated "
        "schema validation and null-checking before reaching the dashboard.",
        variant="success",
    )

    render_divider()

    # ════════════════════════════════════════════════════════════════════
    # 4. Analytics Models
    # ════════════════════════════════════════════════════════════════════
    render_section_header("🧮 Analytical Models")

    st.markdown(
        "The Gold layer produces three families of analytical output, each "
        "implemented as an independent, reproducible Python module."
    )

    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(
            """
<div class="about-card">
<h4>📈 Market Concentration</h4>
<p style="font-size:0.88rem; color:#555;">
<strong>Herfindahl-Hirschman Index (HHI)</strong> computed from app-level
market shares. Tracks equivalent number of firms, identifies concentration
thresholds, and evaluates the impact of NPCI's 30% volume cap on
competitive dynamics.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with m2:
        st.markdown(
            """
<div class="about-card">
<h4>🔮 Forecasting</h4>
<p style="font-size:0.88rem; color:#555;">
Dual-model approach: <strong>Facebook Prophet</strong> for trend + seasonality
decomposition and <strong>ARIMA</strong> for classical time-series modeling.
Includes seasonal factor extraction and 12-month forward projections with
confidence intervals.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    with m3:
        st.markdown(
            """
<div class="about-card">
<h4>💵 Cash Displacement</h4>
<p style="font-size:0.88rem; color:#555;">
Quantifies the shift from cash to digital payments using the
<strong>digital-to-cash ratio</strong>, currency velocity analysis, and
ATM transaction trends. Tracks RBI currency-in-circulation against UPI
growth to measure real displacement.
</p>
</div>
""",
            unsafe_allow_html=True,
        )

    render_divider()

    # ════════════════════════════════════════════════════════════════════
    # 5. Technology Stack
    # ════════════════════════════════════════════════════════════════════
    render_section_header("🛠️ Technology Stack")

    t1, t2, t3, t4 = st.columns(4)

    with t1:
        st.markdown(
            """
<div class="about-card">
<h4>⚙️ Data Engineering</h4>
<ul style="font-size:0.88rem; color:#555; padding-left:1.2rem;">
<li><strong>Python 3.11+</strong></li>
<li><strong>DuckDB</strong> — in-process OLAP</li>
<li><strong>Pandas</strong> — data wrangling</li>
<li><strong>PyArrow</strong> — Parquet I/O</li>
<li><strong>Make</strong> — pipeline orchestration</li>
</ul>
</div>
""",
            unsafe_allow_html=True,
        )

    with t2:
        st.markdown(
            """
<div class="about-card">
<h4>📐 Analytics</h4>
<ul style="font-size:0.88rem; color:#555; padding-left:1.2rem;">
<li><strong>Prophet</strong> — time-series</li>
<li><strong>statsmodels</strong> — ARIMA</li>
<li><strong>scikit-learn</strong> — K-Means clustering</li>
<li><strong>SciPy</strong> — statistical tests</li>
</ul>
</div>
""",
            unsafe_allow_html=True,
        )

    with t3:
        st.markdown(
            """
<div class="about-card">
<h4>📊 Visualization</h4>
<ul style="font-size:0.88rem; color:#555; padding-left:1.2rem;">
<li><strong>Streamlit</strong> — app framework</li>
<li><strong>Plotly</strong> — interactive charts</li>
<li><strong>Custom CSS</strong> — styled components</li>
</ul>
</div>
""",
            unsafe_allow_html=True,
        )

    with t4:
        st.markdown(
            """
<div class="about-card">
<h4>🚀 CI/CD & Deployment</h4>
<ul style="font-size:0.88rem; color:#555; padding-left:1.2rem;">
<li><strong>GitHub Actions</strong> — CI pipeline</li>
<li><strong>Streamlit Cloud</strong> — hosting</li>
<li><strong>Apache Parquet</strong> — storage format</li>
</ul>
</div>
""",
            unsafe_allow_html=True,
        )

    render_divider()

    # ════════════════════════════════════════════════════════════════════
    # 6. Limitations & Caveats
    # ════════════════════════════════════════════════════════════════════
    render_section_header("⚠️ Limitations & Caveats")

    render_insight(
        "Transparency about limitations is a hallmark of rigorous research. "
        "The following caveats should be considered when interpreting results.",
        variant="warning",
    )

    st.markdown(
        """
- **PhonePe Pulse coverage**: Transaction data is sourced from PhonePe's
  open-source repository, which represents PhonePe's view of the ecosystem.
  It may not capture the full UPI network volume reported by NPCI.
- **Temporal granularity**: PhonePe data is available at *quarterly*
  granularity while NPCI data is *monthly*. Joining these requires
  temporal alignment assumptions.
- **Geographic mapping**: District-level data relies on PhonePe's internal
  geographic classification, which may not perfectly align with Census 2011
  or administrative boundary changes.
- **Forecasting horizon**: Prophet and ARIMA models are trained on ~42 months
  of data. Forecasts beyond 6–12 months should be treated as directional
  indicators, not precise predictions.
- **Cash displacement proxy**: Currency-in-circulation (CIC) is an imperfect
  proxy for cash usage — CIC includes hoarded currency and does not
  distinguish between transactional and precautionary cash holdings.
- **Market share calculation**: App-level market shares are derived from
  PhonePe Pulse data, not NPCI's official per-app breakdowns, which are
  not publicly available at district granularity.
- **No real-time data**: All data is batch-processed. The dashboard reflects
  the last pipeline run, not live transaction feeds.
"""
    )

    render_divider()

    # ════════════════════════════════════════════════════════════════════
    # 7. Glossary
    # ════════════════════════════════════════════════════════════════════
    render_section_header("📖 Glossary of Key Terms")

    with st.expander("**Click to expand the full glossary →**", expanded=False):
        st.markdown(
            """
| Term | Full Form | Definition |
|------|-----------|------------|
| **UPI** | Unified Payments Interface | Real-time interbank payment system operated by NPCI enabling instant money transfers via mobile devices |
| **NPCI** | National Payments Corporation of India | Umbrella organization operating retail payment systems in India including UPI, IMPS, and RuPay |
| **P2P** | Person-to-Person | UPI transactions between individuals (e.g., splitting a bill, sending money to family) |
| **P2M** | Person-to-Merchant | UPI transactions from individuals to businesses (e.g., paying at a shop, online purchases) |
| **HHI** | Herfindahl-Hirschman Index | Market concentration metric calculated as the sum of squared market shares (0–10,000 scale). Higher values indicate greater concentration |
| **CIC** | Currency in Circulation | Total value of banknotes and coins in public circulation, published by RBI. Used as a proxy for cash economy size |
| **ARIMA** | Auto-Regressive Integrated Moving Average | Classical statistical model for time-series forecasting combining autoregression, differencing, and moving averages |
| **Prophet** | — | Open-source forecasting library by Meta that decomposes time series into trend, seasonality, and holiday components |
| **CAGR** | Compound Annual Growth Rate | Smoothed annualized growth rate over a period, used to compare growth across different time spans |
| **Lakh Crore** | — | Indian numbering unit equal to 10 trillion (10¹³). ₹1 Lakh Crore = ₹10 trillion ≈ US$120 billion |
| **PSP** | Payment Service Provider | Entity that provides the UPI app interface to end users (e.g., PhonePe, Google Pay, Paytm) |
| **TPAP** | Third Party Application Provider | Non-bank entity authorized by NPCI to offer UPI services through a sponsor bank |
| **VPA** | Virtual Payment Address | UPI identifier (e.g., user@upi) that maps to a bank account without exposing account details |
| **K-Means** | — | Unsupervised machine learning algorithm that partitions data points into K clusters based on feature similarity |
| **Star Schema** | — | Dimensional modeling pattern with a central fact table connected to dimension tables, optimized for analytical queries |
| **Parquet** | — | Columnar storage file format optimized for analytical workloads with efficient compression and encoding |
"""
        )

    st.markdown("")

    render_insight(
        "📬 <strong>Questions or feedback?</strong> This project is open-source "
        "and welcomes contributions. Review the full source code, pipeline logic, "
        "and documentation in the project repository.",
    )
