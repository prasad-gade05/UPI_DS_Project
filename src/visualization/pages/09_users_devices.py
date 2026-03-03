"""👥 Users & Devices — UPI user adoption, device brand analysis, and insurance trends."""

import streamlit as st
import pandas as pd
import numpy as np
from src.visualization.components.charts import (
    create_line_chart, create_bar_chart, create_donut_chart, create_stacked_area,
    APP_COLORS, PLOTLY_CONFIG, apply_common_layout,
)
from src.visualization.components.kpi_cards import render_kpi_row, format_billions, format_percentage
from src.visualization.components.styles import render_insight, render_divider, render_section_header


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _filter_year(df: pd.DataFrame, year_range: tuple[int, int]) -> pd.DataFrame:
    """Filter dataframe to the selected year range."""
    return df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])].copy()


def _qoq_growth(series: pd.Series) -> pd.Series:
    """Quarter-over-quarter percentage growth."""
    return series.pct_change() * 100


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render(data: dict[str, pd.DataFrame], year_range: tuple[int, int]) -> None:
    st.header("👥 Users & Devices")
    st.markdown("Deep-dive into PhonePe user adoption, device brand landscape, and insurance trends.")

    # --- Validate required data -------------------------------------------------
    users_df = data.get("phonepe_user_aggregates")
    devices_df = data.get("phonepe_device_brands")

    if users_df is None or users_df.empty:
        st.warning("User aggregate data is not available.")
        return

    users = _filter_year(users_df, year_range).sort_values("quarter_start_date")
    devices = _filter_year(devices_df, year_range).sort_values("quarter_start_date") if devices_df is not None and not devices_df.empty else pd.DataFrame()

    if users.empty:
        st.info("No user data available for the selected year range.")
        return

    # --- KPI row ----------------------------------------------------------------
    latest = users.iloc[-1]
    prev = users.iloc[-2] if len(users) > 1 else None

    qoq_user_growth = (
        (latest["registered_users"] - prev["registered_users"]) / prev["registered_users"] * 100
        if prev is not None and prev["registered_users"] > 0
        else 0.0
    )

    brand_count = devices["device_brand_clean"].nunique() if not devices.empty and "device_brand_clean" in devices.columns else 0

    render_kpi_row([
        {"label": "Registered Users", "value": format_billions(latest["registered_users"])},
        {"label": "App Opens (Latest Q)", "value": format_billions(latest["app_opens"])},
        {
            "label": "QoQ User Growth",
            "value": format_percentage(qoq_user_growth),
            "delta": format_percentage(qoq_user_growth),
            "delta_color": "normal",
        },
        {"label": "Device Brands Tracked", "value": str(brand_count)},
    ])

    render_divider()

    # ── Section 1: User Registration Growth ─────────────────────────────────────
    render_section_header("📈 User Registration Growth")

    fig_users = create_line_chart(
        users,
        x="quarter_start_date",
        y="registered_users",
        title="Registered Users Over Time",
        area_fill=True,
    )
    st.plotly_chart(fig_users, use_container_width=True, config=PLOTLY_CONFIG)

    # ── Section 2: App Opens Trend ──────────────────────────────────────────────
    render_section_header("📱 App Opens Trend")

    fig_opens = create_line_chart(
        users,
        x="quarter_start_date",
        y="app_opens",
        title="Quarterly App Opens",
        markers=True,
    )
    st.plotly_chart(fig_opens, use_container_width=True, config=PLOTLY_CONFIG)

    # ── Section 3: QoQ User Growth Rate ─────────────────────────────────────────
    render_section_header("📊 Quarter-over-Quarter User Growth Rate")

    growth_df = users[["quarter_start_date", "registered_users"]].copy()
    growth_df["qoq_growth"] = _qoq_growth(growth_df["registered_users"])
    growth_df = growth_df.dropna(subset=["qoq_growth"])

    if not growth_df.empty:
        fig_growth = create_bar_chart(
            growth_df,
            x="quarter_start_date",
            y="qoq_growth",
            title="QoQ Registered-User Growth (%)",
        )
        st.plotly_chart(fig_growth, use_container_width=True, config=PLOTLY_CONFIG)

    render_divider()

    # ── Section 4 & 5: Device Analysis (side-by-side) ───────────────────────────
    if not devices.empty:
        render_section_header("📲 Device Brand Analysis")

        col_donut, col_evolution = st.columns(2)

        # -- Donut: latest quarter, top 6 + Others --
        with col_donut:
            latest_q = devices["quarter_start_date"].max()
            latest_dev = devices[devices["quarter_start_date"] == latest_q].copy()

            brand_col = "device_brand_clean" if "device_brand_clean" in latest_dev.columns else "device_brand"
            top_brands = (
                latest_dev.groupby(brand_col)["device_percentage"]
                .sum()
                .sort_values(ascending=False)
            )
            top6 = top_brands.head(6)
            others = top_brands.iloc[6:].sum() if len(top_brands) > 6 else 0

            donut_df = pd.DataFrame({
                "brand": list(top6.index) + (["Others"] if others > 0 else []),
                "percentage": list(top6.values) + ([others] if others > 0 else []),
            })

            fig_donut = create_donut_chart(
                donut_df,
                values="percentage",
                names="brand",
                title="Device Brand Market Share (Latest Quarter)",
            )
            st.plotly_chart(fig_donut, use_container_width=True, config=PLOTLY_CONFIG)

        # -- Stacked area: top 5 brands over time --
        with col_evolution:
            brand_col = "device_brand_clean" if "device_brand_clean" in devices.columns else "device_brand"
            top5_brands = (
                devices.groupby(brand_col)["device_count"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .index.tolist()
            )
            evo_df = devices[devices[brand_col].isin(top5_brands)].copy()

            if not evo_df.empty:
                fig_evo = create_stacked_area(
                    evo_df,
                    x="quarter_start_date",
                    y="device_percentage",
                    color=brand_col,
                    title="Top 5 Device Brands Over Time",
                )
                st.plotly_chart(fig_evo, use_container_width=True, config=PLOTLY_CONFIG)

        render_divider()

    # ── Section 6 & 7: Insurance Adoption ───────────────────────────────────────
    insurance_df = data.get("phonepe_insurance")
    if insurance_df is not None and not insurance_df.empty:
        ins = _filter_year(insurance_df, year_range).sort_values("quarter_start_date")

        if not ins.empty:
            render_section_header("🛡️ Insurance Adoption")

            col_bar, col_area = st.columns(2)

            with col_bar:
                ins_q = ins.groupby("quarter_start_date", as_index=False).agg(
                    total_count=("count", "sum"),
                    total_amount=("amount", "sum"),
                )

                fig_ins_bar = create_bar_chart(
                    ins_q,
                    x="quarter_start_date",
                    y="total_count",
                    title="Insurance Policy Count by Quarter",
                )
                st.plotly_chart(fig_ins_bar, use_container_width=True, config=PLOTLY_CONFIG)

            with col_area:
                fig_ins_area = create_line_chart(
                    ins_q,
                    x="quarter_start_date",
                    y="total_count",
                    title="Insurance Count Growth Trend",
                    area_fill=True,
                )
                st.plotly_chart(fig_ins_area, use_container_width=True, config=PLOTLY_CONFIG)

            render_divider()

    # ── Insight ─────────────────────────────────────────────────────────────────
    render_insight(
        "PhonePe's registered user base has scaled from ~47 million to over 600 million users, "
        "reflecting India's rapid digital-payments adoption. Device diversity continues to widen, "
        "with Xiaomi, Samsung, and Vivo leading the ecosystem — underscoring the importance of "
        "optimising for affordable Android devices.",
        variant="success",
    )
