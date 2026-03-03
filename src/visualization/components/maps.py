"""India choropleth and geographic map components using Plotly."""

import json
from pathlib import Path

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

from src.visualization.components.charts import apply_common_layout


STATE_NAME_MAP = {
    "Andaman And Nicobar Islands": "Andaman & Nicobar Island",
    "Dadra And Nagar Haveli And Daman And Diu": "Dadra and Nagar Haveli and Daman and Diu",
    "Jammu And Kashmir": "Jammu & Kashmir",
    "Nct Of Delhi": "NCT of Delhi",
    "Delhi": "NCT of Delhi",
    "Telangana": "Telangana",
    "Ladakh": "Ladakh",
    "Lakshadweep": "Lakshadweep",
    "The Government Of Nct Of Delhi": "NCT of Delhi",
}


@st.cache_data(ttl=86400)
def load_india_geojson() -> dict | None:
    """Load India states GeoJSON — local file or public URL fallback."""
    local_paths = [
        Path("data/geojson/india_states.geojson"),
        Path("data/geojson/india_state_geo.geojson"),
    ]
    for p in local_paths:
        if p.exists():
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    try:
        import urllib.request
        url = (
            "https://gist.githubusercontent.com/jbrobst/"
            "56c13bbbf9d97d187fea01ca62ea5112/raw/"
            "e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        )
        with urllib.request.urlopen(url, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def normalize_state_name(name: str) -> str:
    """Normalize state name to match GeoJSON properties."""
    return STATE_NAME_MAP.get(name, name)


def _detect_feature_key(geojson: dict) -> str:
    """Auto-detect the GeoJSON property key for state names."""
    props = geojson["features"][0]["properties"]
    for key in ["ST_NM", "state", "NAME_1", "name", "NAME"]:
        if key in props:
            return f"properties.{key}"
    return f"properties.{list(props.keys())[0]}"


def create_india_choropleth(
    df: pd.DataFrame,
    locations_col: str,
    color_col: str,
    title: str,
    color_scale: str = "YlOrRd",
    hover_data: list[str] | None = None,
    height: int = 550,
) -> go.Figure | None:
    """Create an India state-level choropleth map. Returns None if GeoJSON unavailable."""
    geojson = load_india_geojson()
    if geojson is None:
        return None

    df = df.copy()
    df["_geo_state"] = df[locations_col].apply(normalize_state_name)

    feature_key = _detect_feature_key(geojson)

    fig = px.choropleth(
        df,
        geojson=geojson,
        locations="_geo_state",
        featureidkey=feature_key,
        color=color_col,
        color_continuous_scale=color_scale,
        title=title,
        hover_name=locations_col,
        hover_data=hover_data,
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=height, margin=dict(l=0, r=0, t=50, b=0))
    return apply_common_layout(fig, height)


def create_india_bubble_map(
    df: pd.DataFrame,
    lat_col: str,
    lon_col: str,
    size_col: str,
    color_col: str | None = None,
    title: str = "",
    hover_name: str | None = None,
    height: int = 550,
) -> go.Figure:
    """Create a scatter map of India with bubble sizes."""
    fig = px.scatter_geo(
        df,
        lat=lat_col,
        lon=lon_col,
        size=size_col,
        color=color_col,
        hover_name=hover_name,
        title=title,
        scope="asia",
    )
    fig.update_geos(
        center=dict(lat=22, lon=82),
        projection_scale=4,
        visible=True,
        showland=True,
        landcolor="rgb(243, 243, 243)",
    )
    fig.update_layout(height=height, margin=dict(l=0, r=0, t=50, b=0))
    return apply_common_layout(fig, height)


def create_state_bar_map_fallback(
    df: pd.DataFrame,
    state_col: str,
    value_col: str,
    title: str,
    top_n: int = 15,
    height: int | None = None,
) -> go.Figure:
    """Fallback bar chart when GeoJSON is unavailable."""
    top = df.nlargest(top_n, value_col)
    fig = px.bar(
        top, x=value_col, y=state_col, orientation="h",
        title=title, text_auto=".2s",
        color=value_col, color_continuous_scale="YlOrRd",
    )
    fig.update_layout(yaxis=dict(categoryorder="total ascending"))
    fig.update_traces(textposition="outside")
    return apply_common_layout(fig, height)
