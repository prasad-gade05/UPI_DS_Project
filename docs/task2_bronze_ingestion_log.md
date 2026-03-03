# Task 2: Bronze Layer Ingestion — Log

**Date:** 2026-02-26
**Commit:** *(see below)*

## What Was Done

Implemented the full Bronze layer ingestion pipeline — 3 ingesters + config + utilities extracted from the plan document and wired into working Python code.

### Files Created (10 files)

| File | Purpose |
|------|---------|
| `config/settings.yaml` | Project-wide config (paths, DB, logging) |
| `config/sources.yaml` | Data source URLs, methods, local paths |
| `src/utils/logger.py` | Loguru setup with console + file sinks |
| `src/utils/config_loader.py` | YAML config reader |
| `src/ingestion/base_ingester.py` | Abstract base class (extract → validate → run) |
| `src/ingestion/phonepe_pulse_ingester.py` | Parses 9,026 JSON files into 5 Parquet outputs |
| `src/ingestion/npci_ingester.py` | 42 monthly + 8 yearly + 91 market share records |
| `src/ingestion/rbi_ingester.py` | 26 CIC + 26 ATM records |

### Bronze Layer Outputs (10 Parquet files, 22,011 total rows)

| File | Rows | Source |
|------|------|--------|
| `npci/monthly_upi_volumes.parquet` | 42 | NPCI curated (2022–2025) |
| `npci/yearly_upi_volumes.parquet` | 8 | NPCI curated (2017–2024) |
| `npci/app_market_share.parquet` | 91 | 13 snapshots × 7 apps |
| `phonepe_pulse/agg_transactions_country.parquet` | 140 | Country-level (2018–2024) |
| `phonepe_pulse/map_transactions_district.parquet` | 20,604 | District-level (KEY dataset) |
| `phonepe_pulse/agg_users_country.parquet` | 215 | User registrations + devices |
| `phonepe_pulse/aggregated_insurance.parquet` | 19 | Insurance transactions |
| `phonepe_pulse/top_transactions.parquet` | 840 | Top states/districts/pincodes |
| `rbi/currency_in_circulation.parquet` | 26 | Quarterly CIC (2019–2025) |
| `rbi/atm_transactions.parquet` | 26 | Quarterly ATM volumes (2019–2025) |

### Bugs Found & Fixed During Verification
1. **`state` directory crash** — PhonePe Pulse has a `state/` dir alongside year dirs. Fixed by extracting `_iter_year_quarter()` helper with `isdigit()` guard.
2. **`usersByDevice` is None** — Some quarters return `None` instead of empty list. Fixed with `or []` fallback.
3. **NPCI web scrape timeout** — Expected (no internet in this env). Graceful fallback to curated data works correctly.
