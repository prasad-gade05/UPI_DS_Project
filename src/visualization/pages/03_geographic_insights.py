"""Tab 3: Geographic Insights — Digital divide, state rankings, interactive maps."""

import pandas as pd
import streamlit as st

from src.visualization.components.kpi_cards import render_kpi_row, format_billions
from src.visualization.components.charts import (
    create_bar_chart,
    create_donut_chart,
    CLUSTER_COLORS,
    REGION_COLORS,
    PLOTLY_CONFIG,
)
from src.visualization.components.maps import (
    create_india_choropleth,
    create_state_bar_map_fallback,
)
from src.visualization.components.styles import render_insight, render_divider, render_section_header


def render(data: dict[str, pd.DataFrame], year_range: tuple[int, int]) -> None:
    """Render the Geographic Insights tab."""
    render_section_header("🗺️ Geographic Analysis — State-Level Insights")

    # ── KPI Cards ────────────────────────────────────────────────
    num_states = 0
    num_districts = 0
    if "state_analysis" in data:
        num_states = len(data["state_analysis"])
    if "district_clusters" in data:
        num_districts = len(data["district_clusters"])

    underserved_count = 0
    if "underserved_districts" in data:
        underserved_count = len(data["underserved_districts"])

    avg_gini = 0
    if "state_analysis" in data and "intra_state_gini" in data["state_analysis"].columns:
        avg_gini = data["state_analysis"]["intra_state_gini"].mean()

    render_kpi_row([
        {"label": "States Analyzed", "value": str(num_states), "delta_color": "off"},
        {"label": "Districts Mapped", "value": f"{num_districts:,}", "delta_color": "off"},
        {"label": "Underserved Districts", "value": str(underserved_count),
         "delta": "Bottom 50 by adoption", "delta_color": "off"},
        {"label": "Avg State Gini", "value": f"{avg_gini:.3f}",
         "delta": "Intra-state inequality", "delta_color": "off"},
    ])

    render_divider()

    # ── Interactive India Map ────────────────────────────────────
    if "state_analysis" in data and not data["state_analysis"].empty:
        sa = data["state_analysis"].copy()
        sa["txn_billions"] = sa["total_transactions"] / 1e9

        fig_map = create_india_choropleth(
            sa,
            locations_col="state_clean",
            color_col="txn_billions",
            title="🗺️ State-wise UPI Transaction Volume (Billions)",
            color_scale="YlOrRd",
            hover_data=["num_districts", "intra_state_gini", "rank"],
        )
        if fig_map is not None:
            st.plotly_chart(fig_map, use_container_width=True, config=PLOTLY_CONFIG)
        else:
            fig_fallback = create_state_bar_map_fallback(
                sa, state_col="state_clean", value_col="txn_billions",
                title="Top 15 States by UPI Transaction Volume (Bn)",
            )
            st.plotly_chart(fig_fallback, use_container_width=True, config=PLOTLY_CONFIG)
            st.caption("📌 GeoJSON loading — showing bar chart. Map will render when GeoJSON is available.")

    render_divider()

    # ── State Rankings Table + Regional Breakdown ────────────────
    col1, col2 = st.columns([3, 2])

    with col1:
        if "v_state_rankings" in data and not data["v_state_rankings"].empty:
            rankings = data["v_state_rankings"].copy()
            rankings = rankings[
                (rankings["year"] >= year_range[0]) & (rankings["year"] <= year_range[1])
            ]
            state_agg = (
                rankings.groupby("state", as_index=False)
                .agg(
                    total_txns=("annual_transactions", "sum"),
                    total_value=("annual_value", "sum"),
                    num_districts=("num_districts", "max"),
                    pct_underserved=("pct_underserved_districts", "mean"),
                )
                .sort_values("total_txns", ascending=False)
            )
            state_agg.insert(0, "Rank", range(1, len(state_agg) + 1))
            state_agg["total_txns_bn"] = state_agg["total_txns"] / 1e9
            state_agg["pct_underserved"] = state_agg["pct_underserved"] * 100

            st.markdown("##### 📋 State Rankings by UPI Adoption")
            st.dataframe(
                state_agg[["Rank", "state", "total_txns_bn", "num_districts", "pct_underserved"]]
                .rename(columns={
                    "state": "State",
                    "total_txns_bn": "Txns (Bn)",
                    "num_districts": "Districts",
                    "pct_underserved": "% Underserved",
                }),
                use_container_width=True, hide_index=True, height=400,
                column_config={
                    "Txns (Bn)": st.column_config.NumberColumn(format="%.2f"),
                    "% Underserved": st.column_config.ProgressColumn(
                        min_value=0, max_value=100, format="%.1f%%",
                    ),
                },
            )

    with col2:
        # Regional breakdown donut chart
        if "dim_geography" in data and "state_analysis" in data:
            geo = data["dim_geography"][["state_name", "region"]].drop_duplicates("state_name")
            sa = data["state_analysis"].copy()
            merged = sa.merge(geo, left_on="state_clean", right_on="state_name", how="left")
            merged["region"] = merged["region"].fillna("Other")
            regional = merged.groupby("region", as_index=False)["total_transactions"].sum()

            fig_region = create_donut_chart(
                regional, values="total_transactions", names="region",
                title="🌍 Regional Distribution of UPI Transactions",
                color_discrete_map=REGION_COLORS,
            )
            st.plotly_chart(fig_region, use_container_width=True, config=PLOTLY_CONFIG)

    # ── Cluster Distribution + Top/Bottom ────────────────────────
    render_divider()
    col1, col2 = st.columns(2)

    with col1:
        if "district_clusters" in data and not data["district_clusters"].empty:
            dc = data["district_clusters"].copy()
            cluster_counts = dc.groupby("adoption_tier", as_index=False).size()
            cluster_counts.columns = ["adoption_tier", "count"]
            tier_order = ["Very Low Adoption", "Low Adoption", "Medium Adoption", "High Adoption"]
            cluster_counts["adoption_tier"] = pd.Categorical(
                cluster_counts["adoption_tier"], categories=tier_order, ordered=True,
            )
            cluster_counts = cluster_counts.sort_values("adoption_tier")

            fig_cluster = create_bar_chart(
                cluster_counts, x="adoption_tier", y="count",
                title="📊 Districts by Adoption Tier",
                color="adoption_tier", color_discrete_map=CLUSTER_COLORS,
            )
            st.plotly_chart(fig_cluster, use_container_width=True, config=PLOTLY_CONFIG)

    with col2:
        if "fact_digital_divide" in data and not data["fact_digital_divide"].empty:
            dd = data["fact_digital_divide"].copy()
            dd["year"] = dd["date_key"] // 10000
            latest_year = dd["year"].max()
            latest_dd = dd[dd["year"] == latest_year]
            district_agg = (
                latest_dd.groupby(["state", "district"], as_index=False)
                .agg(total_txns=("total_txn_count", "sum"))
                .sort_values("total_txns", ascending=False)
            )

            top_tab, bottom_tab = st.tabs(["🟢 Top 10 Districts", "🔴 Bottom 10 Districts"])
            with top_tab:
                top_10 = district_agg.head(10).reset_index(drop=True)
                top_10.insert(0, "#", range(1, 11))
                st.dataframe(
                    top_10[["#", "state", "district", "total_txns"]].rename(columns={
                        "state": "State", "district": "District", "total_txns": "Transactions",
                    }),
                    use_container_width=True, hide_index=True,
                )
            with bottom_tab:
                bottom_10 = district_agg.tail(10).sort_values("total_txns").reset_index(drop=True)
                bottom_10.insert(0, "#", range(1, 11))
                st.dataframe(
                    bottom_10[["#", "state", "district", "total_txns"]].rename(columns={
                        "state": "State", "district": "District", "total_txns": "Transactions",
                    }),
                    use_container_width=True, hide_index=True,
                )

    render_insight(
        f"<b>🗺️ Geographic Divide:</b> India's UPI adoption shows significant geographic disparity. "
        f"<b>{num_states}</b> states and <b>{num_districts}</b> districts analyzed reveal "
        f"<b>{underserved_count}</b> critically underserved districts. "
        f"The average intra-state Gini coefficient of <b>{avg_gini:.3f}</b> indicates substantial "
        f"inequality even within states — urban hubs dominate while rural districts lag behind."
    )
