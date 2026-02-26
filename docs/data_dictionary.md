# Data Dictionary — UPI Analytics Platform

> Star Schema built in DuckDB, exported as Parquet for Power BI / Streamlit.

---

## Dimension Tables

### dim_date (120 rows)

| Column | Type | Description |
|--------|------|-------------|
| `date_key` | INTEGER | Surrogate key, format YYYYMM (e.g., 202401) |
| `full_date` | DATE | First day of the month |
| `year` | INTEGER | Calendar year |
| `quarter` | INTEGER | Calendar quarter (1–4) |
| `month` | INTEGER | Calendar month (1–12) |
| `month_name` | VARCHAR | Full month name (e.g., "January") |
| `fiscal_year` | VARCHAR | Indian fiscal year, April–March (e.g., "FY2024-25") |
| `fiscal_quarter` | VARCHAR | Fiscal quarter (Q1 = Apr–Jun through Q4 = Jan–Mar) |
| `is_festival_month` | BOOLEAN | TRUE for Oct, Nov, Dec, Jan, Mar |
| `festival_name` | VARCHAR | Festival name if applicable (Diwali, Holi, etc.) |

### dim_geography (852 rows)

| Column | Type | Description |
|--------|------|-------------|
| `geo_key` | INTEGER | Surrogate key |
| `state_name` | VARCHAR | Standardized state name (Title Case, no hyphens) |
| `district_name` | VARCHAR | Standardized district name (trailing "district" removed) |
| `region` | VARCHAR | Geographic region: North, South, East, West, East & NE, Central, Other |
| `is_metro` | BOOLEAN | TRUE for top metros (Mumbai, Delhi, Bengaluru, etc.) |

### dim_app (7 rows)

| Column | Type | Description |
|--------|------|-------------|
| `app_key` | INTEGER | Surrogate key |
| `app_name` | VARCHAR | UPI app name |
| `parent_company` | VARCHAR | Parent/owning company |
| `launch_year` | INTEGER | Year the app launched UPI (NULL for "Others") |
| `is_major_player` | BOOLEAN | TRUE for PhonePe, Google Pay, Paytm |

### dim_category (5 rows)

| Column | Type | Description |
|--------|------|-------------|
| `category_key` | INTEGER | Surrogate key |
| `category_code` | VARCHAR | Snake_case code (e.g., "p2p_payments") |
| `category_name` | VARCHAR | Human-readable name |
| `is_p2p` | BOOLEAN | TRUE for peer-to-peer payments |
| `is_p2m` | BOOLEAN | TRUE for person-to-merchant payments |

---

## Fact Tables

### fact_upi_transactions (140 rows)

| Column | Type | Description |
|--------|------|-------------|
| `date_key` | INTEGER | FK → dim_date (YYYYMM of quarter start) |
| `category` | VARCHAR | Cleaned category code |
| `txn_count` | BIGINT | Number of transactions |
| `txn_amount_inr` | DOUBLE | Total transaction value in INR |
| `avg_txn_value` | DOUBLE | Average transaction value (amount / count) |
| `year` | INTEGER | Calendar year |
| `quarter` | INTEGER | Calendar quarter (1–4) |

**Source:** PhonePe Pulse aggregated transactions (country level, Q1 2018 – Q4 2024)

### fact_market_concentration (13 rows)

| Column | Type | Description |
|--------|------|-------------|
| `date_key` | INTEGER | FK → dim_date (YYYYMM) |
| `hhi_index` | DOUBLE | Herfindahl-Hirschman Index (sum of squared decimal shares) |
| `hhi_rounded` | DOUBLE | HHI rounded to 4 decimals |
| `top2_combined_share` | DOUBLE | PhonePe + Google Pay combined share (%) |
| `num_apps_above_1pct` | INTEGER | Number of apps with > 1% share |
| `concentration_category` | VARCHAR | "Highly Concentrated" (>0.25), "Moderately Concentrated" (0.15–0.25), or "Competitive" (<0.15) |
| `equivalent_firms` | DOUBLE | 1/HHI — hypothetical equal-sized firms count |

**Source:** NPCI app market share data (13 monthly snapshots, Mar 2023 – Jun 2025)

### fact_cash_displacement (34 rows)

| Column | Type | Description |
|--------|------|-------------|
| `date_key` | INTEGER | FK → dim_date (YYYYMM) |
| `upi_volume_bn` | DOUBLE | Monthly UPI transaction volume (billions) |
| `upi_value_lakh_cr` | DOUBLE | Monthly UPI transaction value (₹ lakh crore) |
| `cic_lakh_cr` | DOUBLE | Currency in circulation (₹ lakh crore, forward-filled from quarterly RBI data) |
| `digital_to_cash_ratio` | DOUBLE | UPI value / CIC — key displacement metric |
| `displacement_index` | DOUBLE | Unrounded ratio for trend analysis |

**Source:** NPCI monthly volumes + RBI CIC (quarterly → forward-filled). Only months where CIC data is available.

### fact_digital_divide (20,604 rows)

| Column | Type | Description |
|--------|------|-------------|
| `date_key` | INTEGER | FK → dim_date (YYYYMM of quarter start) |
| `state` | VARCHAR | Standardized state name |
| `district` | VARCHAR | Standardized district name |
| `total_txn_count` | BIGINT | Total transactions in the quarter |
| `total_txn_amount` | DOUBLE | Total transaction value in INR |
| `avg_txn_value` | DOUBLE | Average transaction value |
| `national_percentile` | DOUBLE | District's percentile rank nationally (0–100) |
| `adoption_tier` | VARCHAR | "Very Low Adoption" / "Low Adoption" / "Medium Adoption" / "High Adoption" |

**Source:** PhonePe Pulse district-level data (843 districts, Q1 2018 – Q4 2024)

---

## Analytical Views

### v_monthly_summary (28 rows)

Quarterly PhonePe transaction summary joined with date dimension for fiscal year and festival analysis.

| Column | Type | Description |
|--------|------|-------------|
| `year` | INTEGER | Calendar year |
| `month` | INTEGER | Month (quarter start month: 1, 4, 7, 10) |
| `month_name` | VARCHAR | Month name |
| `fiscal_year` | VARCHAR | Indian fiscal year |
| `is_festival_month` | BOOLEAN | Festival flag |
| `festival_name` | VARCHAR | Festival name |
| `total_transactions` | BIGINT | Sum of all transactions |
| `total_value_inr` | DOUBLE | Sum of all transaction values |
| `avg_transaction_value` | DOUBLE | Average transaction value |

### v_state_rankings (252 rows)

Annual state-level rankings by UPI adoption.

| Column | Type | Description |
|--------|------|-------------|
| `state` | VARCHAR | State name |
| `year` | INTEGER | Calendar year |
| `annual_transactions` | BIGINT | Total transactions in year |
| `annual_value` | DOUBLE | Total value in year |
| `num_districts` | INTEGER | Districts in state |
| `pct_underserved_districts` | DOUBLE | Fraction of districts in "Very Low Adoption" tier |
| `state_rank` | INTEGER | National rank by transaction count |

---

## Files

| Path | Description |
|------|-------------|
| `data/gold/upi_analytics.duckdb` | DuckDB database with all tables and views |
| `data/gold/exports/*.parquet` | 10 Parquet exports (8 tables + 2 views) |
