"""Tab 2: Market Concentration — HHI analysis, duopoly metrics, treemap."""

import pandas as pd
import streamlit as st

from src.visualization.components.kpi_cards import render_kpi_row
from src.visualization.components.charts import (
    APP_COLORS,
    PLOTLY_CONFIG,
    create_hhi_trend,
    create_stacked_area,
    create_horizontal_bar,
    create_gauge,
    create_treemap,
)
from src.visualization.components.styles import render_insight, render_divider, render_section_header


def render(data: dict[str, pd.DataFrame], year_range: tuple[int, int]) -> None:
    """Render the Market Concentration tab."""
    render_section_header("🏢 Market Concentration Analysis")

    if "fact_market_concentration" not in data or data["fact_market_concentration"].empty:
        st.warning("⚠️ Market concentration data not available. Run `make all` first.")
        return

    df = data["fact_market_concentration"].copy()
    df["year"] = df["date_key"] // 10000
    df["month"] = (df["date_key"] % 10000) // 100
    df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

    if df.empty:
        st.info("No data available for the selected year range.")
        return

    df = df.sort_values(["year", "month"])
    df["period"] = df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)

    # ── KPI Cards ────────────────────────────────────────────────
    latest = df.iloc[-1]
    hhi_val = latest["hhi_index"]
    classification = latest["concentration_category"]
    class_icon = "🔴" if hhi_val > 0.25 else ("🟡" if hhi_val > 0.15 else "🟢")

    render_kpi_row([
        {"label": "Current HHI", "value": f"{hhi_val:.4f}", "delta_color": "off"},
        {"label": "Top 2 Combined Share",
         "value": f"{latest['top2_combined_share']:.1f}%",
         "delta": "PhonePe + GPay", "delta_color": "off"},
        {"label": "Equivalent Firms",
         "value": f"{latest['equivalent_firms']:.1f}",
         "delta_color": "off"},
        {"label": "Classification",
         "value": f"{class_icon} {classification}",
         "delta_color": "off"},
    ])

    render_divider()

    # ── HHI Gauge + HHI Trend (side by side) ─────────────────────
    col1, col2 = st.columns([1, 2])

    with col1:
        fig_gauge = create_gauge(
            value=hhi_val,
            title="HHI Index (Current)",
            max_val=0.5,
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config=PLOTLY_CONFIG)

        # NPCI Cap Compliance
        st.markdown("##### 📋 NPCI 30% Cap Compliance")
        if "app_market_share" in data and not data["app_market_share"].empty:
            share_df = data["app_market_share"].copy()
            latest_month = share_df.loc[share_df["date"] == share_df["date"].max()]
            app_col = "app_name_clean" if "app_name_clean" in share_df.columns else "app_name"
            share_col = "market_share_pct"
            for _, row in latest_month.iterrows():
                app = row[app_col]
                share = row[share_col]
                status = "🔴 Over Cap" if share > 30 else "🟢 Compliant"
                st.markdown(f"**{app}**: {share:.1f}% — {status}")

    with col2:
        fig_hhi = create_hhi_trend(
            df, x="period", y="hhi_index",
            title="HHI Trend — Market Concentration Over Time (DOJ Thresholds)",
        )
        st.plotly_chart(fig_hhi, use_container_width=True, config=PLOTLY_CONFIG)

    render_divider()

    # ── Market Share Visuals ─────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        if "app_market_share" in data and not data["app_market_share"].empty:
            share_df = data["app_market_share"].copy()
            share_df = share_df[
                (share_df["year"] >= year_range[0]) & (share_df["year"] <= year_range[1])
            ]
            share_df = share_df.sort_values(["year", "month"])
            share_df["period"] = share_df["year"].astype(str) + "-" + share_df["month"].astype(str).str.zfill(2)
            app_col = "app_name_clean" if "app_name_clean" in share_df.columns else "app_name"

            fig_area = create_stacked_area(
                share_df, x="period", y="market_share_pct", color=app_col,
                title="📊 Market Share Evolution (100% Stacked)",
                color_discrete_map=APP_COLORS,
            )
            st.plotly_chart(fig_area, use_container_width=True, config=PLOTLY_CONFIG)
        else:
            st.info("App-level market share data not available.")

    with col2:
        if "app_market_share" in data and not data["app_market_share"].empty:
            share_df = data["app_market_share"].copy()
            app_col = "app_name_clean" if "app_name_clean" in share_df.columns else "app_name"
            max_year = share_df["year"].max()
            latest_month_df = share_df[share_df["year"] == max_year]
            max_month = latest_month_df["month"].max()
            latest_snap = latest_month_df[latest_month_df["month"] == max_month]

            fig_bar = create_horizontal_bar(
                latest_snap, x="market_share_pct", y=app_col,
                title=f"📊 Market Share Snapshot ({max_year}-{max_month:02d})",
                color=app_col, color_discrete_map=APP_COLORS,
            )
            fig_bar.add_vline(x=30, line_dash="dash", line_color="red", opacity=0.6,
                              annotation_text="NPCI 30% Cap")
            st.plotly_chart(fig_bar, use_container_width=True, config=PLOTLY_CONFIG)

    # ── Treemap of Market Share ──────────────────────────────────
    if "app_market_share" in data and not data["app_market_share"].empty:
        share_df = data["app_market_share"].copy()
        max_date = share_df["date"].max()
        latest = share_df[share_df["date"] == max_date].copy()
        app_col = "app_name_clean" if "app_name_clean" in latest.columns else "app_name"
        latest["market_label"] = "UPI Market"

        fig_tree = create_treemap(
            latest,
            path=["market_label", app_col],
            values="market_share_pct",
            title="🗂️ UPI Market Share Treemap (Latest Month)",
            color="market_share_pct",
            color_continuous_scale="Purples",
        )
        st.plotly_chart(fig_tree, use_container_width=True, config=PLOTLY_CONFIG)

    # ── Insight Box ──────────────────────────────────────────────
    if hhi_val > 0.25:
        render_insight(
            f"<b>⚠️ Highly Concentrated Market:</b> India's UPI market has an HHI of "
            f"<b>{hhi_val:.4f}</b>, classified as 'Highly Concentrated' by US DOJ standards. "
            f"PhonePe + Google Pay together control <b>~{latest['top2_combined_share']:.1f}%</b> "
            f"of all UPI transactions. The market effectively behaves as if it has only "
            f"<b>{latest['equivalent_firms']:.1f}</b> competing firms. "
            f"NPCI's proposed 30% market share cap could fundamentally reshape this landscape.",
            variant="warning",
        )
    else:
        render_insight(
            f"Market HHI of {hhi_val:.4f} indicates "
            f"{'moderate' if hhi_val > 0.15 else 'healthy'} competition.",
            variant="success",
        )
