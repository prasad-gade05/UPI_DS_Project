# 🇮🇳 UPI Analytics Platform

> A production-grade data engineering and analytics platform analyzing India's Unified Payments Interface (UPI) ecosystem — the world's largest real-time digital payments system.

## Overview

This project builds a complete data pipeline using the **Medallion Architecture** (Bronze → Silver → Gold) to ingest, clean, model, and analyze UPI transaction data from three authoritative sources:

- **PhonePe Pulse** — District-level transaction data across 700+ Indian districts
- **NPCI** — Official monthly UPI volumes and app-wise market share
- **RBI DBIE** — Currency in circulation and ATM transaction data

## Key Analyses

| Analysis | Description |
|----------|-------------|
| **Market Concentration (HHI)** | Quantifying duopoly risk (PhonePe ~48% + Google Pay ~37%) |
| **Cash Displacement** | Correlating UPI growth with declining ATM usage |
| **Geographic Digital Divide** | Identifying underserved districts using clustering |
| **Time-Series Forecasting** | Prophet + ARIMA models for UPI growth projection |
| **Seasonal Decomposition** | Diwali spikes, salary cycles, financial year-end effects |

## Tech Stack

| Layer | Tools |
|-------|-------|
| Ingestion | Python, requests, BeautifulSoup, GitPython |
| Processing | pandas, numpy, DuckDB |
| Analytics | Prophet, statsmodels, scikit-learn |
| Visualization | Power BI, Streamlit, Plotly |
| Orchestration | GitHub Actions (monthly cron) |

## Project Status

🚧 **Under active development** — Data pipeline being built.

---

*See `docs/planning/Project_Master_Context.md` for the full project specification.*
