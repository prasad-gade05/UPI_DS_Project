# Phase 5: Power BI Dashboard — Complete Build Guide

> **Project:** UPI Digital Payments Analytics Platform
> **Dashboard Name:** "India UPI Pulse — Digital Payments Intelligence"
> **Pages:** 14 (+ 2 hidden tooltip pages)
> **Total Visuals:** 120+
> **DAX Measures:** 65+

---

## Table of Contents

1. [Setup & Data Connection](#1-setup--data-connection)
2. [Data Model & Relationships](#2-data-model--relationships)
3. [Master DAX Measures](#3-master-dax-measures)
4. [Page 1: Cover & Navigation](#page-1-cover--navigation)
5. [Page 2: Executive Summary](#page-2-executive-summary)
6. [Page 3: UPI Growth Story](#page-3-upi-growth-story)
7. [Page 4: Transaction Deep Dive](#page-4-transaction-deep-dive)
8. [Page 5: Market Concentration (HHI)](#page-5-market-concentration-hhi)
9. [Page 6: App Market Share Dynamics](#page-6-app-market-share-dynamics)
10. [Page 7: Geographic Overview — State Level](#page-7-geographic-overview--state-level)
11. [Page 8: District-Level Drill Down](#page-8-district-level-drill-down)
12. [Page 9: Digital Divide Deep Dive](#page-9-digital-divide-deep-dive)
13. [Page 10: Cash vs Digital](#page-10-cash-vs-digital)
14. [Page 11: Forecasting & Predictions](#page-11-forecasting--predictions)
15. [Page 12: User & Device Analytics](#page-12-user--device-analytics)
16. [Page 13: Insurance via UPI](#page-13-insurance-via-upi)
17. [Page 14: Data Quality & Methodology](#page-14-data-quality--methodology)
18. [Tooltip Page T1: District Detail](#tooltip-page-t1-district-detail)
19. [Tooltip Page T2: App Detail](#tooltip-page-t2-app-detail)
20. [Bookmarks & Navigation Setup](#bookmarks--navigation-setup)
21. [Theme & Visual Polish](#theme--visual-polish)

---

## 1. Setup & Data Connection

### 1.1 Open Power BI Desktop

1. File → New Report
2. Save immediately as `UPI_Analytics_Dashboard.pbix` in `dashboards/`

### 1.2 Load Data (Get Data → Folder)

Use **Get Data → Parquet** (or Folder method) to load all 17 Gold layer exports.

**Method A — Individual Parquet files (Recommended):**

1. Home → Get Data → More → Parquet
2. Navigate to `data/gold/exports/`
3. Load each file individually (gives you control over naming):

| Table Name in Power BI | Source File | Rows |
|------------------------|-------------|------|
| `dim_date` | `dim_date.parquet` | ~3,653 |
| `dim_geography` | `dim_geography.parquet` | 852 |
| `dim_app` | `dim_app.parquet` | 7 |
| `dim_category` | `dim_category.parquet` | 5 |
| `fact_upi_transactions` | `fact_upi_transactions.parquet` | 140 |
| `fact_market_concentration` | `fact_market_concentration.parquet` | 13 |
| `fact_cash_displacement` | `fact_cash_displacement.parquet` | 34 |
| `fact_digital_divide` | `fact_digital_divide.parquet` | 20,604 |
| `v_monthly_summary` | `v_monthly_summary.parquet` | 28 |
| `v_state_rankings` | `v_state_rankings.parquet` | 252 |
| `hhi_analysis` | `hhi_analysis.parquet` | 13 |
| `arima_forecast` | `arima_forecast.parquet` | 12 |
| `forecast_combined` | `forecast_combined.parquet` | 54 |
| `seasonal_factors` | `seasonal_factors.parquet` | 12 |
| `state_analysis` | `state_analysis.parquet` | 36 |
| `district_clusters` | `district_clusters.parquet` | 788 |
| `underserved_districts` | `underserved_districts.parquet` | 50 |
| `cash_displacement_analysis` | `cash_displacement_analysis.parquet` | 34 |

4. Also load these **Silver** tables for additional richness:

| Table Name | Source File | Rows |
|------------|-------------|------|
| `silver_app_market_share` | `data/silver/market_share/app_market_share.parquet` | 91 |
| `silver_npci_monthly` | `data/silver/transactions/npci_monthly_volumes.parquet` | 42 |
| `silver_device_brands` | `data/silver/users/phonepe_device_brands.parquet` | 187 |
| `silver_user_aggregates` | `data/silver/users/phonepe_user_aggregates.parquet` | 28 |
| `silver_insurance` | `data/silver/transactions/phonepe_insurance.parquet` | 19 |
| `silver_state_transactions` | `data/silver/geographic/state_transactions.parquet` | 1,008 |
| `silver_rbi_atm` | `data/silver/transactions/rbi_atm_transactions.parquet` | 26 |
| `silver_top_transactions` | `data/silver/transactions/phonepe_top_transactions.parquet` | 840 |
| `bronze_yearly_volumes` | `data/bronze/npci/yearly_upi_volumes.parquet` | 8 |

### 1.3 Power Query Transformations

In Power Query Editor (Transform Data):

**For `dim_date`:**
1. Select `full_date` column → Change Type → Date
2. Select `date_key` column → Change Type → Whole Number
3. Right-click `dim_date` table → **Mark as Date Table** → Select `full_date` as the date column
4. This is CRITICAL — all time intelligence DAX functions require a marked date table
5. The `full_date` column contains contiguous daily dates (2017-01-01 to 2026-12-31) with no gaps, which is required for Power BI Date Table validation

**For `arima_forecast`:**
1. Change `date` column type to Date

**For `forecast_combined`** (pre-built — no manual append needed):
1. Change `date` column type to Date
2. This table already contains `date`, `volume_bn`, and `is_forecast` (true/false) combining silver_npci_monthly actuals with ARIMA forecasts — 54 rows total

**For `silver_npci_monthly`:**
1. Change `date` to Date type

**For all fact tables:**
- Ensure `date_key` columns are Integer type (not text)

Close & Apply.

---

## 2. Data Model & Relationships

### 2.1 Switch to Model View

Click the Model icon (3rd icon) on the left sidebar.

### 2.2 Create Relationships

Create these relationships by dragging fields between tables:

| From Table | From Column | To Table | To Column | Cardinality | Cross-filter |
|------------|-------------|----------|-----------|-------------|-------------|
| `fact_upi_transactions` | `date_key` | `dim_date` | `date_key` | Many-to-One | Both |
| `fact_upi_transactions` | `category` | `dim_category` | `category_code` | Many-to-One | Both |
| `fact_digital_divide` | `date_key` | `dim_date` | `date_key` | Many-to-One | Single |
| `fact_digital_divide` | `state` | `dim_geography` | `state_name` | Many-to-Many | Single |
| `fact_market_concentration` | `date_key` | `dim_date` | `date_key` | Many-to-One | Both |
| `fact_cash_displacement` | `date_key` | `dim_date` | `date_key` | Many-to-One | Both |
| `v_state_rankings` | `state` | `dim_geography` | `state_name` | Many-to-Many | Single |
| `silver_app_market_share` | `app_name` | `dim_app` | `app_name` | Many-to-One | Both |
| `district_clusters` | `state_clean` | `state_analysis` | `state_clean` | Many-to-One | Both |

**Important:** For the `fact_digital_divide` → `dim_geography` relationship, use Many-to-Many since `dim_geography` has district-level granularity and `fact_digital_divide` also has district-level. Set cross-filter to Single direction to avoid ambiguity.

### 2.3 Create a Disconnected Date Slicer Table (Optional but powerful)

This lets you have a slicer that doesn't filter dimensions directly:

```
DateSlicer = CALENDAR(DATE(2017,1,1), DATE(2026,12,31))
```

### 2.4 Hide Technical Columns

In Model View, right-click and "Hide in report view" for:
- All `date_key` columns (users interact via `dim_date`)
- `category_code` in `dim_category`
- `geo_key` in `dim_geography`
- `app_key` in `dim_app`
- All `_key` surrogate keys

---

## 3. Master DAX Measures

Create a dedicated Measures table: Modeling → New Table → `_Measures = ROW("x", 0)` then hide the `x` column.

### 3.1 Core Volume & Value Measures

```dax
// ═══════════════════════════════════════════
// VOLUME & VALUE MEASURES
// ═══════════════════════════════════════════

Total Transactions = 
SUM(fact_upi_transactions[txn_count])

Total Value INR = 
SUM(fact_upi_transactions[txn_amount_inr])

Total Value Lakh Cr = 
DIVIDE([Total Value INR], 1000000000000, 0)

Total Value Cr = 
DIVIDE([Total Value INR], 10000000, 0)

Avg Transaction Value = 
DIVIDE([Total Value INR], [Total Transactions], 0)

Transaction Count Billions = 
DIVIDE([Total Transactions], 1000000000, 0)
```

### 3.2 Growth Measures

```dax
// ═══════════════════════════════════════════
// GROWTH MEASURES
// ═══════════════════════════════════════════

YoY Transaction Growth = 
VAR CurrentYear = [Total Transactions]
VAR PrevYear = CALCULATE(
    [Total Transactions],
    DATEADD(dim_date[full_date], -1, YEAR)
)
RETURN DIVIDE(CurrentYear - PrevYear, PrevYear, 0)

QoQ Transaction Growth = 
VAR CurrentQ = [Total Transactions]
VAR PrevQ = CALCULATE(
    [Total Transactions],
    DATEADD(dim_date[full_date], -3, MONTH)
)
RETURN DIVIDE(CurrentQ - PrevQ, PrevQ, 0)

YoY Value Growth = 
VAR CurrentYear = [Total Value INR]
VAR PrevYear = CALCULATE(
    [Total Value INR],
    DATEADD(dim_date[full_date], -1, YEAR)
)
RETURN DIVIDE(CurrentYear - PrevYear, PrevYear, 0)

CAGR Volume = 
VAR FirstYear = CALCULATE(
    [Total Transactions],
    FIRSTNONBLANK(dim_date[full_date], [Total Transactions])
)
VAR LastYear = CALCULATE(
    [Total Transactions],
    LASTNONBLANK(dim_date[full_date], [Total Transactions])
)
VAR FirstDt = CALCULATE(
    MIN(dim_date[full_date]),
    FIRSTNONBLANK(dim_date[full_date], [Total Transactions])
)
VAR LastDt = CALCULATE(
    MAX(dim_date[full_date]),
    LASTNONBLANK(dim_date[full_date], [Total Transactions])
)
VAR Years = DATEDIFF(FirstDt, LastDt, YEAR)
RETURN IF(Years > 0 && FirstYear > 0,
    POWER(DIVIDE(LastYear, FirstYear), DIVIDE(1, Years)) - 1,
    BLANK()
)
```

### 3.3 Market Concentration Measures

```dax
// ═══════════════════════════════════════════
// MARKET CONCENTRATION (HHI) MEASURES
// ═══════════════════════════════════════════

Current HHI = 
CALCULATE(
    SELECTEDVALUE(hhi_analysis[hhi]),
    LASTNONBLANK(hhi_analysis[period], 1)
)

HHI Interpretation = 
VAR hhi = [Current HHI]
RETURN SWITCH(TRUE(),
    hhi > 0.25, "Highly Concentrated",
    hhi > 0.15, "Moderately Concentrated",
    hhi > 0, "Competitive",
    "N/A"
)

HHI Color = 
VAR hhi = [Current HHI]
RETURN SWITCH(TRUE(),
    hhi > 0.25, "#E74C3C",
    hhi > 0.15, "#F39C12",
    hhi > 0, "#2ECC71",
    "#95A5A6"
)

Equivalent Firms = 
CALCULATE(
    SELECTEDVALUE(hhi_analysis[equivalent_firms]),
    LASTNONBLANK(hhi_analysis[period], 1)
)

Top 2 Combined Share = 
CALCULATE(
    SELECTEDVALUE(hhi_analysis[top2_share]),
    LASTNONBLANK(hhi_analysis[period], 1)
)

PhonePe Share = 
CALCULATE(
    SELECTEDVALUE(silver_app_market_share[market_share_pct]),
    silver_app_market_share[app_name] = "PhonePe",
    LASTNONBLANK(silver_app_market_share[date], 1)
)

Google Pay Share = 
CALCULATE(
    SELECTEDVALUE(silver_app_market_share[market_share_pct]),
    silver_app_market_share[app_name] = "Google Pay",
    LASTNONBLANK(silver_app_market_share[date], 1)
)

Share Above 30pct Cap = 
VAR phonepe = [PhonePe Share]
RETURN IF(phonepe > 30, phonepe - 30, 0)

NPCI Cap Line = 30
```

### 3.4 Cash Displacement Measures

```dax
// ═══════════════════════════════════════════
// CASH DISPLACEMENT MEASURES
// ═══════════════════════════════════════════

Current Digital to Cash Ratio = 
CALCULATE(
    SELECTEDVALUE(cash_displacement_analysis[digital_to_cash_ratio]),
    LASTNONBLANK(cash_displacement_analysis[date], 1)
)

Starting Digital to Cash Ratio = 
CALCULATE(
    SELECTEDVALUE(cash_displacement_analysis[digital_to_cash_ratio]),
    FIRSTNONBLANK(cash_displacement_analysis[date], 1)
)

Ratio Change Pct = 
DIVIDE(
    [Current Digital to Cash Ratio] - [Starting Digital to Cash Ratio],
    [Starting Digital to Cash Ratio],
    0
)

Current CIC Lakh Cr = 
CALCULATE(
    SELECTEDVALUE(cash_displacement_analysis[cic_lakh_cr]),
    LASTNONBLANK(cash_displacement_analysis[date], 1)
)

Current UPI Value Lakh Cr = 
CALCULATE(
    SELECTEDVALUE(cash_displacement_analysis[upi_value_lakh_cr]),
    LASTNONBLANK(cash_displacement_analysis[date], 1)
)

Displacement Velocity = 
CALCULATE(
    SELECTEDVALUE(cash_displacement_analysis[displacement_velocity]),
    LASTNONBLANK(cash_displacement_analysis[date], 1)
)

Months to Parity = 
VAR ratio = [Current Digital to Cash Ratio]
VAR velocity = CALCULATE(
    AVERAGE(cash_displacement_analysis[displacement_velocity]),
    cash_displacement_analysis[displacement_velocity] > 0
)
RETURN IF(velocity > 0 && ratio < 1,
    DIVIDE(1 - ratio, velocity),
    BLANK()
)

Displacement Trend = 
CALCULATE(
    SELECTEDVALUE(cash_displacement_analysis[trend]),
    LASTNONBLANK(cash_displacement_analysis[date], 1)
)
```

### 3.5 Geographic & Digital Divide Measures

```dax
// ═══════════════════════════════════════════
// GEOGRAPHIC & DIGITAL DIVIDE MEASURES
// ═══════════════════════════════════════════

Total Districts = 
DISTINCTCOUNT(fact_digital_divide[district])

Underserved District Count = 
CALCULATE(
    DISTINCTCOUNT(fact_digital_divide[district]),
    fact_digital_divide[adoption_tier] = "Low Adoption"
) + CALCULATE(
    DISTINCTCOUNT(fact_digital_divide[district]),
    fact_digital_divide[adoption_tier] = "Very Low Adoption"
)

Pct Underserved = 
DIVIDE([Underserved District Count], [Total Districts], 0)

High Adoption District Count = 
CALCULATE(
    DISTINCTCOUNT(fact_digital_divide[district]),
    fact_digital_divide[adoption_tier] = "High Adoption"
)

State Gini Coefficient = 
SELECTEDVALUE(state_analysis[intra_state_gini])

National Avg Gini = 
AVERAGE(state_analysis[intra_state_gini])

District Transactions = 
SUM(fact_digital_divide[total_txn_count])

District Avg Txn Value = 
DIVIDE(
    SUM(fact_digital_divide[total_txn_amount]),
    SUM(fact_digital_divide[total_txn_count]),
    0
)

State Rank = 
SELECTEDVALUE(state_analysis[rank])

Top State Name = 
CALCULATE(
    SELECTEDVALUE(state_analysis[state_clean]),
    state_analysis[rank] = 1
)

Bottom State Name = 
CALCULATE(
    SELECTEDVALUE(state_analysis[state_clean]),
    state_analysis[rank] = MAX(state_analysis[rank])
)
```

### 3.6 Forecasting Measures

```dax
// ═══════════════════════════════════════════
// FORECASTING MEASURES
// ═══════════════════════════════════════════

ARIMA Forecast = 
SELECTEDVALUE(arima_forecast[arima_forecast_bn])

ARIMA Upper = 
SELECTEDVALUE(arima_forecast[arima_upper_bn])

ARIMA Lower = 
SELECTEDVALUE(arima_forecast[arima_lower_bn])

Forecast Confidence Width = 
[ARIMA Upper] - [ARIMA Lower]

Latest Actual Volume = 
CALCULATE(
    SELECTEDVALUE(silver_npci_monthly[transaction_volume_billions]),
    LASTNONBLANK(silver_npci_monthly[date], 1)
)

Seasonal Factor = 
SELECTEDVALUE(seasonal_factors[seasonal_factor])

Peak Season Month = 
CALCULATE(
    SELECTEDVALUE(seasonal_factors[month]),
    TOPN(1, seasonal_factors, seasonal_factors[seasonal_factor], DESC)
)

Trough Season Month = 
CALCULATE(
    SELECTEDVALUE(seasonal_factors[month]),
    TOPN(1, seasonal_factors, seasonal_factors[seasonal_factor], ASC)
)
```

### 3.7 User & Device Measures

```dax
// ═══════════════════════════════════════════
// USER & DEVICE MEASURES
// ═══════════════════════════════════════════

Total Registered Users = 
CALCULATE(
    SELECTEDVALUE(silver_user_aggregates[registered_users]),
    LASTNONBLANK(silver_user_aggregates[quarter_start_date], 1)
)

Registered Users Millions = 
DIVIDE([Total Registered Users], 1000000, 0)

Registered Users Cr = 
DIVIDE([Total Registered Users], 10000000, 0)

Top Device Brand = 
CALCULATE(
    SELECTEDVALUE(silver_device_brands[device_brand_clean]),
    TOPN(1,
        FILTER(silver_device_brands,
            silver_device_brands[quarter_start_date] = MAX(silver_device_brands[quarter_start_date])),
        silver_device_brands[device_percentage], DESC
    )
)

Device Brand Share = 
SUM(silver_device_brands[device_percentage])
```

### 3.8 Insurance Measures

```dax
// ═══════════════════════════════════════════
// INSURANCE MEASURES
// ═══════════════════════════════════════════

Insurance Policies = 
SUM(silver_insurance[count])

Insurance Premium INR = 
SUM(silver_insurance[amount])

Insurance Premium Cr = 
DIVIDE([Insurance Premium INR], 10000000, 0)

Avg Premium Per Policy = 
DIVIDE([Insurance Premium INR], [Insurance Policies], 0)

Insurance QoQ Growth = 
VAR LatestDate = MAX(silver_insurance[quarter_start_date])
VAR PrevDate = EDATE(LatestDate, -3)
VAR Current = CALCULATE(
    SUM(silver_insurance[count]),
    silver_insurance[quarter_start_date] = LatestDate
)
VAR Prev = CALCULATE(
    SUM(silver_insurance[count]),
    silver_insurance[quarter_start_date] = PrevDate
)
RETURN DIVIDE(Current - Prev, Prev, 0)
```

### 3.9 Conditional Formatting Measures

```dax
// ═══════════════════════════════════════════
// CONDITIONAL FORMATTING HELPERS
// ═══════════════════════════════════════════

Growth Color = 
VAR growth = [YoY Transaction Growth]
RETURN SWITCH(TRUE(),
    growth > 0.5, "#1ABC9C",
    growth > 0.2, "#2ECC71",
    growth > 0, "#F1C40F",
    growth > -0.1, "#E67E22",
    "#E74C3C"
)

Adoption Tier Color = 
SWITCH(
    SELECTEDVALUE(fact_digital_divide[adoption_tier]),
    "High Adoption", "#1ABC9C",
    "Medium Adoption", "#3498DB",
    "Low Adoption", "#F39C12",
    "Very Low Adoption", "#E74C3C",
    "#95A5A6"
)

Gini Alert = 
VAR gini = [State Gini Coefficient]
RETURN SWITCH(TRUE(),
    gini > 0.6, "🔴 Severe Inequality",
    gini > 0.4, "🟡 Moderate Inequality",
    gini > 0.2, "🟢 Relatively Equal",
    "🟢 Very Equal"
)

HHI Gauge Value = 
// Scale HHI (0-1) to gauge (0-100)
[Current HHI] * 100
```

### 3.10 Dynamic Title Measures

```dax
// ═══════════════════════════════════════════
// DYNAMIC TITLES
// ═══════════════════════════════════════════

Selected Year Label = 
"Data for " & SELECTEDVALUE(dim_date[year], "All Years")

Selected State Label = 
"State: " & SELECTEDVALUE(dim_geography[state_name], "All States")

Last Updated = 
"Data as of " & FORMAT(MAX(dim_date[full_date]), "MMMM YYYY")

Page Subtitle Exec = 
"Tracking India's ₹" & FORMAT([Total Value Lakh Cr], "#,0.0") & 
" Lakh Crore Digital Payments Revolution | " & [Last Updated]
```

---

## Page 1: Cover & Navigation

**Purpose:** Professional landing page with navigation buttons to all dashboard sections.

**Page Settings:**
- Page size: 16:9 (1280 × 720)
- Background color: `#1B2631` (dark navy)
- Page type: Normal

### Visual 1.1 — Title Text Box

| Property | Value |
|----------|-------|
| Type | Text Box |
| Position | Top center |
| Size | 900 × 100 px |
| Text | **"India UPI Pulse"** |
| Font | Segoe UI Bold, 42pt, White |
| Subtitle | "Digital Payments Intelligence Dashboard" |
| Subtitle font | Segoe UI Light, 18pt, `#BDC3C7` |

### Visual 1.2 — Subtitle Text Box

| Property | Value |
|----------|-------|
| Type | Text Box |
| Position | Below title |
| Text | "Analyzing ₹260+ Lakh Crore in UPI Transactions across 800+ Districts" |
| Font | Segoe UI, 14pt, `#95A5A6` |

### Visual 1.3 — Hero KPI Cards (4 cards in a row)

Create 4 **Card** visuals in a horizontal row:

**Card A — Total Transactions:**
- Field: `[Transaction Count Billions]`
- Format: `0.0 "Bn"`
- Title: "Total UPI Transactions"
- Icon: 📊
- Background: `#2C3E50` with `#1ABC9C` left border (4px)

**Card B — Total Value:**
- Field: `[Total Value Lakh Cr]`
- Format: `₹ #,0.0 " L Cr"`
- Title: "Total Value Processed"
- Background: `#2C3E50` with `#3498DB` left border

**Card C — Districts Covered:**
- Field: `[Total Districts]`
- Title: "Districts Analyzed"
- Background: `#2C3E50` with `#F39C12` left border

**Card D — Market HHI:**
- Field: `[Current HHI]`
- Format: `0.0000`
- Title: "Market Concentration (HHI)"
- Background: `#2C3E50` with `#E74C3C` left border

### Visual 1.4 — Navigation Buttons (Grid of 12)

Create **Buttons** (Insert → Buttons → Blank) arranged in a 4×3 grid:

| Button | Label | Icon | Action | Target Page |
|--------|-------|------|--------|-------------|
| 1 | Executive Summary | 📋 | Page Navigation | Page 2 |
| 2 | UPI Growth Story | 📈 | Page Navigation | Page 3 |
| 3 | Transaction Deep Dive | 🔍 | Page Navigation | Page 4 |
| 4 | Market Concentration | 🏢 | Page Navigation | Page 5 |
| 5 | App Market Share | 📱 | Page Navigation | Page 6 |
| 6 | Geographic Overview | 🗺️ | Page Navigation | Page 7 |
| 7 | District Analysis | 📍 | Page Navigation | Page 8 |
| 8 | Digital Divide | ⚖️ | Page Navigation | Page 9 |
| 9 | Cash vs Digital | 💰 | Page Navigation | Page 10 |
| 10 | Forecasting | 🔮 | Page Navigation | Page 11 |
| 11 | Users & Devices | 👤 | Page Navigation | Page 12 |
| 12 | Data Quality | ℹ️ | Page Navigation | Page 14 |

**Button Styling:**
- Size: 200 × 60 px each
- Default fill: `#2C3E50`, hover fill: `#34495E`
- Border: 1px `#1ABC9C`, radius: 8px
- Font: Segoe UI, 11pt, White
- Action: Type = Page Navigation → select target page

### Visual 1.5 — Data Sources Footer

| Property | Value |
|----------|-------|
| Type | Text Box |
| Position | Bottom |
| Text | "Sources: NPCI Official • RBI DBIE • PhonePe Pulse (GitHub) | Built with Medallion Architecture" |
| Font | 10pt, `#7F8C8D` |

---

## Page 2: Executive Summary

**Purpose:** One-page snapshot of everything — the page a CXO reads.

**Page Background:** White with subtle `#F8F9FA` gradient
**Header bar:** 60px tall, `#2C3E50` background, white text "Executive Summary"

### Global Slicers (top right, horizontal)

**Slicer 2.A — Year:**
- Field: `dim_date[year]`
- Style: Dropdown
- Default: All
- Size: 150 × 40 px

**Slicer 2.B — Quarter:**
- Field: `dim_date[quarter]`
- Style: Horizontal list (tiles)
- Default: All

### Visual 2.1 — KPI Card Row (6 cards)

Arrange 6 **Multi-row Card** or **Card** visuals horizontally:

| # | Measure | Format | Subtitle | Conditional Color |
|---|---------|--------|----------|-------------------|
| A | `[Total Transactions]` | `#,0` | "Total UPI Transactions" | — |
| B | `[Total Value Lakh Cr]` | `₹#,0.0 L Cr` | "Transaction Value" | — |
| C | `[YoY Transaction Growth]` | `+0.0%` | "YoY Volume Growth" | Green if >0, Red if <0 |
| D | `[Current HHI]` | `0.0000` | "Market HHI" | Red (always >0.25) |
| E | `[Current Digital to Cash Ratio]` | `0.00x` | "Digital-to-Cash Ratio" | — |
| F | `[Registered Users Cr]` | `#,0.0 Cr` | "Registered Users" | — |

**Styling:** Each card gets a thin colored top border (1px) using the project color palette.

### Visual 2.2 — UPI Volume Trend (Line Chart)

| Property | Value |
|----------|-------|
| Type | Line Chart |
| Position | Left half, below KPI row |
| Size | 580 × 280 px |
| X-Axis | `silver_npci_monthly[date]` |
| Y-Axis | `silver_npci_monthly[transaction_volume_billions]` |
| Title | "Monthly UPI Transaction Volume (Billions)" |
| Data labels | ON (last point only) |
| Trend line | ON (linear, dashed) |
| Reference line | Y-axis constant line at latest value, labeled "Current: XX Bn" |
| Color | `#1ABC9C` |

### Visual 2.3 — Category Breakdown (Donut Chart)

| Property | Value |
|----------|-------|
| Type | Donut Chart |
| Position | Right of line chart |
| Size | 300 × 280 px |
| Legend/Values | `dim_category[category_name]` |
| Values | `[Total Transactions]` |
| Title | "Transaction Mix by Category" |
| Colors | Merchant: `#1ABC9C`, P2P: `#3498DB`, Recharge: `#9B59B6`, Financial: `#F39C12`, Others: `#95A5A6` |
| Detail labels | Show category + percentage |
| Inner radius | 60% |

### Visual 2.4 — Top 5 States Bar Chart

| Property | Value |
|----------|-------|
| Type | Clustered Bar Chart |
| Position | Bottom left |
| Size | 400 × 220 px |
| Y-Axis | `v_state_rankings[state]` (Top N filter = 5 by `annual_transactions`) |
| X-Axis | `v_state_rankings[annual_transactions]` |
| Title | "Top 5 States by Transaction Volume" |
| Data labels | ON, format: `#,0.0 "Bn"` (divide by 1B in measure) |
| Colors | Gradient from `#1ABC9C` (darkest for #1) to `#BDC3C7` |
| Sort | Descending by value |

### Visual 2.5 — HHI Gauge

| Property | Value |
|----------|-------|
| Type | Gauge |
| Position | Bottom center |
| Size | 200 × 200 px |
| Value | `[HHI Gauge Value]` (HHI × 100) |
| Min | 0 |
| Max | 50 (since HHI max realistic ~0.5) |
| Target | 25 (the threshold for "Highly Concentrated") |
| Title | "Market Concentration Index" |
| Colors | Green (0-15), Yellow (15-25), Red (25-50) — use conditional formatting |
| Callout | Show `[HHI Interpretation]` below |

### Visual 2.6 — Cash Displacement Sparkline

| Property | Value |
|----------|-------|
| Type | Line & Stacked Column |
| Position | Bottom right |
| Size | 350 × 220 px |
| X-Axis | `cash_displacement_analysis[date]` |
| Column Y | `cash_displacement_analysis[upi_value_lakh_cr]` (UPI Value) |
| Line Y | `cash_displacement_analysis[cic_lakh_cr]` (CIC) |
| Title | "UPI Value vs Cash in Circulation (₹ Lakh Cr)" |
| Column color | `#1ABC9C` |
| Line color | `#E74C3C` |
| Legend | ON |

### Visual 2.7 — Key Insights Text Box

| Property | Value |
|----------|-------|
| Type | Text Box |
| Position | Bottom strip, full width |
| Background | `#FEF9E7` (light yellow) |
| Border | 1px `#F39C12` left |
| Text | Dynamic (use a measure for partial): "📌 Key Insight: India's UPI processes XX Billion transactions monthly, yet the market is controlled by a PhonePe-Google Pay duopoly (HHI: 0.XX). Cash in circulation continues to grow — India is becoming 'less cash-dependent' rather than 'cashless.'" |
| Font | 11pt, `#2C3E50` |

---

## Page 3: UPI Growth Story

**Purpose:** Deep dive into UPI's explosive growth from 2017 to present.

**Header:** "The UPI Growth Story — From ₹1L Cr to ₹260L Cr"

### Slicers

**Slicer 3.A — Fiscal Year:**
- Field: `dim_date[fiscal_year]`
- Style: Dropdown

### Visual 3.1 — Yearly Volume Growth (Column + Line Combo)

| Property | Value |
|----------|-------|
| Type | Line and Clustered Column |
| Size | Full width, 300 px tall |
| X-Axis | `bronze_yearly_volumes[year]` |
| Column Y | `bronze_yearly_volumes[transaction_volume_billions]` |
| Line Y | `bronze_yearly_volumes[yoy_volume_growth]` (format as %) |
| Title | "Annual UPI Transaction Volume & YoY Growth" |
| Column color | `#1ABC9C` |
| Line color | `#E74C3C` with markers |
| Data labels | ON for both series |
| Secondary Y-axis | ON for growth rate |

### Visual 3.2 — Monthly Volume Line with Moving Average

| Property | Value |
|----------|-------|
| Type | Line Chart |
| Size | Left half, 280 px |
| X-Axis | `silver_npci_monthly[date]` |
| Y-Axis (1) | `silver_npci_monthly[transaction_volume_billions]` |
| Y-Axis (2) | Add Analytics → Moving Average (3-month window) |
| Title | "Monthly UPI Volumes with 3-Month Moving Average" |
| Main line | `#1ABC9C`, 2px |
| Moving avg | `#E74C3C`, dashed, 1px |
| Reference lines | Add vertical reference lines for key events: "COVID Lockdown (Mar 2020)", "Paytm Crisis (Jan 2024)" |

### Visual 3.3 — Monthly Value Line

| Property | Value |
|----------|-------|
| Type | Area Chart |
| Size | Right half, 280 px |
| X-Axis | `silver_npci_monthly[date]` |
| Y-Axis | `silver_npci_monthly[transaction_value_lakh_crores]` |
| Title | "Monthly UPI Transaction Value (₹ Lakh Cr)" |
| Fill color | `#3498DB` with 30% opacity |
| Line | `#2980B9`, 2px |

### Visual 3.4 — Average Transaction Value Trend

| Property | Value |
|----------|-------|
| Type | Line Chart |
| Size | Left half, below |
| X-Axis | `silver_npci_monthly[date]` |
| Y-Axis | `silver_npci_monthly[avg_transaction_value_inr]` |
| Title | "Average Transaction Value (₹)" |
| Analytics | Add trend line (linear) |
| Insight | Value is declining = more small-value P2P transactions entering the system |

### Visual 3.5 — MoM Growth Heatmap (Matrix)

| Property | Value |
|----------|-------|
| Type | Matrix |
| Size | Right half, below |
| Rows | `silver_npci_monthly[year]` |
| Columns | `silver_npci_monthly[month]` (display as Jan, Feb...) |
| Values | `silver_npci_monthly[mom_volume_growth]` |
| Title | "Month-over-Month Growth Heatmap" |
| Conditional formatting | Background color: Red (#E74C3C) for negative, White for 0, Green (#1ABC9C) for positive. Scale: diverging. |
| Format values | As percentage (0.0%) |

### Visual 3.6 — Cumulative Growth Waterfall

| Property | Value |
|----------|-------|
| Type | Waterfall Chart |
| Size | Full width, bottom |
| Category | `bronze_yearly_volumes[year]` |
| Y-Axis | `bronze_yearly_volumes[transaction_volume_billions]` |
| Title | "Cumulative UPI Volume by Year (Waterfall)" |
| Increase color | `#1ABC9C` |
| Decrease color | `#E74C3C` |
| Total color | `#2C3E50` |
| Breakdown | Shows how each year added to the total |

### Visual 3.7 — Key Milestone Annotations (Text Box)

| Property | Value |
|----------|-------|
| Type | Text box |
| Content | Timeline of milestones: "2016: UPI Launched • 2018: 1 Bn txns • 2020: COVID accelerates digital • 2023: 10 Bn monthly • 2024: Paytm crisis" |

---

## Page 4: Transaction Deep Dive

**Purpose:** Category-level analysis — P2P vs P2M, Merchant vs Personal.

**Header:** "Transaction Anatomy — What India Pays For"

### Slicers

**Slicer 4.A — Category:**
- Field: `dim_category[category_name]`
- Style: Horizontal tile buttons
- Multi-select: ON

**Slicer 4.B — Year:**
- Field: `dim_date[year]`
- Style: Slider (range)

### Visual 4.1 — 100% Stacked Area (Category Share Over Time)

| Property | Value |
|----------|-------|
| Type | 100% Stacked Area Chart |
| Size | Full width, 300 px |
| X-Axis | `fact_upi_transactions[year]` + `fact_upi_transactions[quarter]` as hierarchy |
| Y-Axis | `[Total Transactions]` |
| Legend | `dim_category[category_name]` |
| Title | "Transaction Category Mix Over Time (% Share)" |
| Colors | Use distinct colors per category |
| **Drill-down** | Year → Quarter (click the drill-down arrows) |

### Visual 4.2 — P2P vs P2M Split (Donut)

First, create a calculated column on `dim_category`:
```dax
Payment Type = 
SWITCH(TRUE(),
    dim_category[is_p2p] = TRUE, "P2P",
    dim_category[is_p2m] = TRUE, "P2M",
    "Other"
)
```

| Property | Value |
|----------|-------|
| Type | Donut Chart |
| Size | 250 × 250 px |
| Legend | `dim_category[Payment Type]` |
| Values | `[Total Transactions]` |
| Title | "P2P vs P2M Transaction Split" |
| Colors | P2P: `#3498DB`, P2M: `#E67E22`, Other: `#95A5A6` |

### Visual 4.3 — P2P vs P2M Value Split (Donut)

| Property | Value |
|----------|-------|
| Type | Donut Chart |
| Size | 250 × 250 px, next to 4.2 |
| Legend | `dim_category[Payment Type]` |
| Values | `[Total Value INR]` |
| Title | "P2P vs P2M Value Split" |
| Insight | P2P has MORE volume but P2M has HIGHER value per transaction |

### Visual 4.4 — Category Volume Trend (Multi-line)

| Property | Value |
|----------|-------|
| Type | Line Chart |
| Size | Left half, 280 px |
| X-Axis | `fact_upi_transactions[year]` (or quarter start date) |
| Y-Axis | `[Total Transactions]` |
| Legend | `dim_category[category_name]` |
| Title | "Transaction Volume by Category Over Time" |
| Highlight | Merchant payments overtaking P2P = key story |

### Visual 4.5 — Avg Transaction Value by Category (Bar)

| Property | Value |
|----------|-------|
| Type | Clustered Bar Chart |
| Size | Right half |
| Y-Axis | `dim_category[category_name]` |
| X-Axis | `[Avg Transaction Value]` |
| Title | "Average Transaction Value by Category (₹)" |
| Data labels | ON, format ₹#,0 |
| Sort | Descending |
| Conditional formatting | Gradient bars (darker = higher value) |

### Visual 4.6 — Category Growth Matrix

| Property | Value |
|----------|-------|
| Type | Matrix |
| Rows | `dim_category[category_name]` |
| Columns | `dim_date[year]` |
| Values | `[Total Transactions]` |
| Title | "Category × Year Transaction Matrix" |
| Conditional formatting | Background scale from white to `#1ABC9C` |
| Totals | Row + Column totals ON |

### Visual 4.7 — Quarterly Seasonality by Category (Small Multiples)

| Property | Value |
|----------|-------|
| Type | Line Chart with **Small Multiples** |
| Small multiple field | `dim_category[category_name]` |
| X-Axis | Quarter (1-4) |
| Y-Axis | `[Total Transactions]` |
| Title | "Quarterly Patterns by Category" |
| Layout | 1 row × 5 columns |
| Insight | Merchant payments peak in Q4 (festivals), P2P peaks in Q1 (New Year gifting) |

### Visual 4.8 — Top 10 States by Category (Stacked Bar with Drill-through)

| Property | Value |
|----------|-------|
| Type | Stacked Bar Chart |
| Y-Axis | `silver_top_transactions[entity_name_clean]` (filter: `level` = "states", Top N = 10) |
| X-Axis | `silver_top_transactions[count]` |
| Title | "Top 10 States — Transaction Volume" |
| **Drill-through** | Right-click any bar → Drill through to Page 7 (Geographic Overview) filtered to that state |

---

## Page 5: Market Concentration (HHI)

**Purpose:** Antitrust-grade analysis of UPI market concentration.

**Header:** "Market Concentration — The PhonePe-Google Pay Duopoly"
**Sub-header:** Dynamic measure `[Page Subtitle HHI]`

### Visual 5.1 — HHI Gauge (Large, center-stage)

| Property | Value |
|----------|-------|
| Type | Gauge |
| Size | 300 × 300 px, top center |
| Value | `[HHI Gauge Value]` |
| Min | 0, Max | 50 |
| Target | 25 (DOJ threshold) |
| Title | "Herfindahl-Hirschman Index" |
| Color bands | 0-15: `#2ECC71`, 15-25: `#F39C12`, 25-50: `#E74C3C` |
| Callout text below | `[HHI Interpretation]` + `[Equivalent Firms]` |

### Visual 5.2 — HHI Trend Line

| Property | Value |
|----------|-------|
| Type | Line Chart |
| Size | Left half, 280 px |
| X-Axis | `hhi_analysis[period]` |
| Y-Axis | `hhi_analysis[hhi]` |
| Title | "HHI Over Time" |
| Reference lines | Horizontal lines at 0.25 (labeled "Highly Concentrated") and 0.15 ("Moderately Concentrated") with different colors |
| Data point markers | ON |
| Color | `#E74C3C` |
| Annotation | Add text box noting "NPCI proposed 30% cap" |

### Visual 5.3 — Top 2 Share Trend

| Property | Value |
|----------|-------|
| Type | Line Chart |
| Size | Right half, 280 px |
| X-Axis | `hhi_analysis[period]` |
| Y-Axis | `hhi_analysis[top2_share]` |
| Title | "PhonePe + Google Pay Combined Share (%)" |
| Reference line | Y-axis at 60% labeled "Duopoly Threshold" |
| Color | `#8E44AD` |
| Data labels | ON for last point |
| Analytics | Add a constant line at 30% labeled "NPCI Cap (per app)" |

### Visual 5.4 — Equivalent Firms Bar

| Property | Value |
|----------|-------|
| Type | Clustered Column Chart |
| X-Axis | `hhi_analysis[period]` |
| Y-Axis | `hhi_analysis[equivalent_firms]` |
| Title | "Equivalent Number of Competitors" |
| Reference line | Y = 3 (labeled "Minimum healthy competition") |
| Color | `#3498DB` |
| Insight | Market has never had more than 2.8 equivalent firms |

### Visual 5.5 — Latest Period App Share (Treemap)

| Property | Value |
|----------|-------|
| Type | Treemap |
| Size | Left half, 280 px |
| Group | `silver_app_market_share[app_name]` |
| Values | `silver_app_market_share[market_share_pct]` |
| Filter | Latest period only (filter pane: `date` = max date) |
| Title | "Current Market Share Distribution" |
| Data labels | Show app name + percentage |
| Colors | PhonePe: `#5F259F` (PhonePe brand), Google Pay: `#4285F4` (Google brand), Paytm: `#00BAF2`, others: shades of gray |

### Visual 5.6 — App Share Stacked Area Over Time

| Property | Value |
|----------|-------|
| Type | 100% Stacked Area |
| X-Axis | `silver_app_market_share[date]` |
| Y-Axis | `silver_app_market_share[market_share_pct]` |
| Legend | `silver_app_market_share[app_name]` |
| Title | "Market Share Evolution Over Time" |
| Highlight | PhonePe growing, Paytm shrinking visible in the visualization |

### Visual 5.7 — NPCI 30% Cap Compliance Table

| Property | Value |
|----------|-------|
| Type | Table |
| Size | Full width, bottom |
| Columns | App Name, Latest Share (%), Above 30% Cap?, Excess Share to Shed |
| Data | From `silver_app_market_share` filtered to latest period |
| Conditional formatting | Red background for any app > 30% |
| Title | "NPCI 30% Market Share Cap Compliance" |

Create a calculated table or use measures:
```dax
Cap Excess = 
VAR share = SELECTEDVALUE(silver_app_market_share[market_share_pct])
RETURN IF(share > 30, share - 30, 0)

Above Cap Flag = 
IF(SELECTEDVALUE(silver_app_market_share[market_share_pct]) > 30, "⚠️ YES", "✅ No")
```

### Visual 5.8 — Policy Implications Card

| Property | Value |
|----------|-------|
| Type | Text Box |
| Background | `#FDEDEC` (light red) |
| Border | 2px left `#E74C3C` |
| Content | Bullet list: "• PhonePe must shed ~XX pp under 30% cap • Only 2.7 effective competitors • Systemic risk: single point of failure • New entrants need regulatory support" |

---

## Page 6: App Market Share Dynamics

**Purpose:** Individual app trajectories, competitive landscape, Paytm collapse analysis.

**Header:** "App Battlefield — Who Wins India's Payments War"

### Slicers

**Slicer 6.A — App Selector:**
- Field: `silver_app_market_share[app_name]`
- Style: Vertical list with checkboxes
- Default: All selected

### Visual 6.1 — Multi-Line App Share Trend

| Property | Value |
|----------|-------|
| Type | Line Chart |
| Size | Full width, 300 px |
| X-Axis | `silver_app_market_share[date]` |
| Y-Axis | `silver_app_market_share[market_share_pct]` |
| Legend | `silver_app_market_share[app_name]` |
| Title | "Individual App Market Share Trajectories (%)" |
| Reference line | Horizontal at 30% (NPCI Cap), dashed red |
| Colors | PhonePe: `#5F259F`, Google Pay: `#4285F4`, Paytm: `#00BAF2`, CRED: `#000000`, WhatsApp Pay: `#25D366`, Others: `#95A5A6`, Amazon Pay: `#FF9900` |
| Markers | ON for all series |
| **Tooltip** | Use Tooltip Page T2 (App Detail) |

### Visual 6.2 — App Share Change (Dumbbell/Dot Plot via Scatter)

| Property | Value |
|----------|-------|
| Type | Scatter Chart (simulating dumbbell) |
| Details | `silver_app_market_share[app_name]` |
| X-Axis | First period share vs Last period share (create 2 measures) |
| Y-Axis | App name |
| Title | "Market Share: Start vs Current" |
| Insight | Shows who gained and who lost |

Create measures:
```dax
First Period Share = 
CALCULATE(
    SELECTEDVALUE(silver_app_market_share[market_share_pct]),
    FIRSTNONBLANK(silver_app_market_share[date], 1)
)

Latest Period Share = 
CALCULATE(
    SELECTEDVALUE(silver_app_market_share[market_share_pct]),
    LASTNONBLANK(silver_app_market_share[date], 1)
)

Share Change pp = [Latest Period Share] - [First Period Share]
```

### Visual 6.3 — Share Change Waterfall

| Property | Value |
|----------|-------|
| Type | Waterfall Chart |
| Category | `silver_app_market_share[app_name]` |
| Values | `[Share Change pp]` |
| Title | "Market Share Change (Percentage Points)" |
| Increase | `#2ECC71` (gained share) |
| Decrease | `#E74C3C` (lost share) |

### Visual 6.4 — Parent Company View (Stacked Bar)

| Property | Value |
|----------|-------|
| Type | Stacked Bar Chart |
| Y-Axis | `dim_app[parent_company]` |
| X-Axis | Latest share (via measure) |
| Legend | `dim_app[app_name]` |
| Title | "Market Share by Parent Company" |
| Insight | Walmart (PhonePe) vs Alphabet (GPay) vs others |

### Visual 6.5 — Paytm Collapse Focus (Bookmarked view)

Create a **Bookmark** called "Paytm Collapse Story" that:
1. Filters date range to Jan 2024 – Dec 2024
2. Highlights Paytm line in Visual 6.1
3. Shows a text annotation: "RBI barred Paytm Payments Bank in Jan 2024. Share dropped from 11.4% to ~6.5%. Market redistributed to PhonePe/GPay rather than smaller players — HHI barely changed."

**How to create:**
1. Set the filters as described
2. View → Bookmarks pane → Add bookmark
3. Name it "Paytm Collapse"
4. Create a button on the page: "📖 Show Paytm Collapse Story" → Action: Bookmark → select this bookmark

### Visual 6.6 — Competitive Dynamics Table

| Property | Value |
|----------|-------|
| Type | Table |
| Columns | App Name | Parent Company | Current Share | Share 1Y Ago | Change | Status |
| Conditional formatting | Green/red arrows for change column |
| Title | "Competitive Landscape Summary" |

---

## Page 7: Geographic Overview — State Level

**Purpose:** India-wide map visualization, state rankings, regional disparities. This is one of the richest pages.

**Header:** "India's Digital Map — 36 States, 800+ Districts"

### Slicers

**Slicer 7.A — Year:**
- Field: `v_state_rankings[year]`
- Style: Slider
- Default: Latest year

**Slicer 7.B — Region:**
- Field: `dim_geography[region]`
- Style: Horizontal tile buttons (North, South, East, West, Central, Northeast, Other)
- Multi-select: ON

### Visual 7.1 — India Filled Map (Choropleth)

| Property | Value |
|----------|-------|
| Type | **Filled Map** (or ArcGIS/Azure Map) |
| Size | Left half, 400 px tall (dominant visual) |
| Location | `v_state_rankings[state]` |
| Color saturation | `v_state_rankings[annual_transactions]` |
| Title | "UPI Adoption Intensity by State" |
| Color scale | Sequential: `#FEF9E7` (low) → `#F39C12` (medium) → `#E74C3C` (high) |
| **Tooltip** | Custom tooltip page T1 — shows state details on hover |
| **Drill-through** | Enable drill-through to Page 8 (District Level) |

**How to set up Drill-through:**
1. Go to Page 8
2. In Visualizations pane → Drill-through section → Add `v_state_rankings[state]` as drill-through field
3. Now on Page 7, right-clicking a state on the map → "Drill through → District Analysis" will navigate to Page 8 filtered to that state

### Visual 7.2 — State Rankings Table (Sortable)

| Property | Value |
|----------|-------|
| Type | Table |
| Size | Right half, 400 px |
| Columns (in order): |
| | `v_state_rankings[state_rank]` — format as rank icon (1st, 2nd...) |
| | `v_state_rankings[state]` |
| | `v_state_rankings[annual_transactions]` — format: `#,0.0 M` (divide by 1M) |
| | `v_state_rankings[annual_value]` — format: `₹#,0 Cr` |
| | `v_state_rankings[num_districts]` |
| | `v_state_rankings[pct_underserved_districts]` — format as % |
| Title | "State Rankings — Annual Performance" |
| Conditional formatting on `annual_transactions` | Data bars (green gradient) |
| Conditional formatting on `pct_underserved_districts` | Background: white to red scale |
| Sort | By `state_rank` ascending (default) |
| Row count | Show all 36 with scroll |

### Visual 7.3 — Top 10 vs Bottom 10 States (Diverging Bar)

| Property | Value |
|----------|-------|
| Type | Clustered Bar Chart |
| Size | Left bottom, 400 × 250 px |

Create TWO bar charts side by side or use a single chart with a calculated column:

**Top 10 chart:**
- Y-Axis: `v_state_rankings[state]` (Top N = 10 by transactions)
- X-Axis: `v_state_rankings[annual_transactions]`
- Color: `#1ABC9C`
- Title: "Top 10 Digital States"

**Bottom 10 chart:**
- Y-Axis: `v_state_rankings[state]` (Bottom N = 10 by transactions)
- X-Axis: `v_state_rankings[annual_transactions]`
- Color: `#E74C3C`
- Title: "Bottom 10 States (Needs Attention)"

### Visual 7.4 — Region Breakdown (Donut)

| Property | Value |
|----------|-------|
| Type | Donut Chart |
| Size | 250 × 250 px |
| Legend | `dim_geography[region]` |
| Values | Transaction count from `fact_digital_divide` (create measure) |
| Title | "Transaction Share by Region" |
| Colors | North: `#3498DB`, South: `#1ABC9C`, West: `#F39C12`, East: `#9B59B6`, Central: `#E67E22`, Northeast: `#E74C3C`, Other: `#95A5A6` |

### Visual 7.5 — State Growth Over Years (Line Chart with Small Multiples)

| Property | Value |
|----------|-------|
| Type | Line Chart with **Small Multiples** |
| Small Multiple Field | `silver_state_transactions[state_clean]` (filter to Top 9 states) |
| X-Axis | `silver_state_transactions[quarter_start_date]` |
| Y-Axis | `silver_state_transactions[total_txn_count]` |
| Title | "Growth Trajectories — Top 9 States" |
| Layout | 3×3 grid |
| Each mini-chart | Shows the quarterly trend for one state |

### Visual 7.6 — Metro vs Non-Metro Split

| Property | Value |
|----------|-------|
| Type | Clustered Bar Chart |
| Y-Axis | Two categories: "Metro" and "Non-Metro" |
| X-Axis | District transaction sum (grouped by `dim_geography[is_metro]`) |
| Title | "Metro vs Non-Metro UPI Transactions" |
| Data labels | Show percentage of total |

Create measure:
```dax
Metro Transactions = 
CALCULATE(
    SUM(fact_digital_divide[total_txn_count]),
    dim_geography[is_metro] = TRUE
)

Non-Metro Transactions = 
CALCULATE(
    SUM(fact_digital_divide[total_txn_count]),
    dim_geography[is_metro] = FALSE
)

Metro Pct = DIVIDE([Metro Transactions], [Metro Transactions] + [Non-Metro Transactions], 0)
```

### Visual 7.7 — Avg Transaction Value by State (Heat-colored bar)

| Property | Value |
|----------|-------|
| Type | Clustered Bar Chart |
| Y-Axis | `silver_state_transactions[state_clean]` (Top N = 15) |
| X-Axis | `silver_state_transactions[avg_txn_value]` |
| Title | "Average Transaction Value by State (₹)" |
| Conditional formatting | Color by value: low value = `#3498DB`, high = `#E74C3C` |
| Sort | Descending |
| Insight | High avg value = more P2M/commercial; Low avg = more P2P/micro-payments |

---

## Page 8: District-Level Drill Down

**Purpose:** Granular district-level analysis with clustering, drill-down from state maps. This is the data-richest page (20,604 rows).

**Header:** Dynamic title using measure `[Selected State Label]`

### Slicers

**Slicer 8.A — State:**
- Field: `fact_digital_divide[state]`
- Style: Dropdown
- Default: All (or filled by drill-through from Page 7)

**Slicer 8.B — Adoption Tier:**
- Field: `fact_digital_divide[adoption_tier]`
- Style: Horizontal tile buttons
- Colors: Match `[Adoption Tier Color]` measure

**Slicer 8.C — Year-Quarter:**
- Field: `dim_date[year]` + `dim_date[quarter]` hierarchy
- Style: Dropdown

### Visual 8.1 — District Map (Shape Map or ArcGIS)

| Property | Value |
|----------|-------|
| Type | **Shape Map** (if India district TopoJSON available) or **ArcGIS Map** |
| Size | Left half, 400 px |
| Location | `fact_digital_divide[district]` (with state context) |
| Color | `fact_digital_divide[adoption_tier]` → color by tier |
| Bubble size (if using ArcGIS) | `fact_digital_divide[total_txn_count]` |
| Title | "District UPI Adoption Map" |
| Colors | Very Low: `#E74C3C`, Low: `#F39C12`, Medium: `#3498DB`, High: `#1ABC9C` |
| **Tooltip** | Tooltip Page T1 (District Detail) |

**Alternative if Shape Map unavailable:** Use a **Scatter Chart** with state on Y-axis, district on details, and size = transaction count, color = adoption tier.

### Visual 8.2 — District Cluster Scatter Plot

| Property | Value |
|----------|-------|
| Type | Scatter Chart |
| Size | Right half, 350 px |
| X-Axis | `district_clusters[total_txn]` (log scale ON) |
| Y-Axis | `district_clusters[avg_txn_value]` |
| Size | `district_clusters[total_value]` |
| Color | `district_clusters[adoption_tier]` |
| Details | `district_clusters[district_clean]` |
| Title | "District Adoption Clusters (K-Means)" |
| Legend | Show 4 clusters with tier names |
| **Play axis** (optional) | If using quarterly data, animate through quarters |

### Visual 8.3 — Adoption Tier Distribution (Donut)

| Property | Value |
|----------|-------|
| Type | Donut Chart |
| Size | 250 × 250 px |
| Legend | `district_clusters[adoption_tier]` |
| Values | Count of districts (COUNTROWS) |
| Title | "Districts by Adoption Tier" |
| Data labels | Count + percentage |
| Colors | Tier colors as defined above |
| Inner text | Total district count |

Create measure:
```dax
Districts in Tier = 
COUNTROWS(district_clusters)
```

### Visual 8.4 — District Ranking Table

| Property | Value |
|----------|-------|
| Type | Table |
| Size | Full width bottom, 300 px |
| Columns: |
| | `district_clusters[state_clean]` |
| | `district_clusters[district_clean]` |
| | `district_clusters[total_txn]` — format: `#,0` |
| | `district_clusters[total_value]` — format: `₹#,0.0 Cr` |
| | `district_clusters[avg_txn_value]` — format: `₹#,0` |
| | `district_clusters[adoption_tier]` |
| Title | "District Performance Table" |
| Conditional formatting on `adoption_tier` | Background color matching tier colors |
| Conditional formatting on `total_txn` | Data bars |
| Sort | By `total_txn` descending (default) |
| Row count | Paginated, 20 per page |
| Search | Enable search on district name |

### Visual 8.5 — Top Districts Within Selected State (Bar)

| Property | Value |
|----------|-------|
| Type | Clustered Bar Chart |
| Size | Left bottom, 350 × 250 px |
| Y-Axis | `district_clusters[district_clean]` (Top N = 15) |
| X-Axis | `district_clusters[total_txn]` |
| Title | "Top 15 Districts by Transaction Volume" |
| Data labels | ON |
| Color | `#1ABC9C` |

### Visual 8.6 — Bottom Districts Within Selected State (Bar)

| Property | Value |
|----------|-------|
| Type | Clustered Bar Chart |
| Size | Right bottom, 350 × 250 px |
| Y-Axis | `district_clusters[district_clean]` (Bottom N = 15) |
| X-Axis | `district_clusters[total_txn]` |
| Title | "Bottom 15 Districts (Underserved)" |
| Color | `#E74C3C` |
| Insight | These are the districts needing digital payment infrastructure investment |

### Visual 8.7 — District Volume Distribution (Histogram)

| Property | Value |
|----------|-------|
| Type | Clustered Column Chart (acting as histogram) |
| X-Axis | Create bins for `total_txn` (use Power Query: Right-click column → New Group → Bin size = auto) |
| Y-Axis | Count of districts |
| Title | "Distribution of District Transaction Volumes" |
| Color | `#3498DB` |
| Analytics | Add normal distribution line |
| Insight | Expect a right-skewed distribution (few high-volume districts, many low-volume) |

### Visual 8.8 — District Quarterly Trend (for selected district)

| Property | Value |
|----------|-------|
| Type | Line Chart |
| Size | Appears on selection (or use conditional visibility with bookmarks) |
| X-Axis | `fact_digital_divide[date_key]` |
| Y-Axis | `fact_digital_divide[total_txn_count]` |
| Filter | Selected district from table/map interaction |
| Title | Dynamic: "Quarterly Trend — [Selected District]" |

---

## Page 9: Digital Divide Deep Dive

**Purpose:** Inequality analysis using Gini coefficients, identifying where India needs investment.

**Header:** "The Digital Divide — Who's Left Behind?"
**Color scheme:** Red-amber for this page (inequality theme)

### Visual 9.1 — National Gini Overview Card

| Property | Value |
|----------|-------|
| Type | Card |
| Size | 200 × 100 px |
| Value | `[National Avg Gini]` |
| Format | `0.000` |
| Title | "National Average Intra-State Gini" |
| Conditional color | Text color by `[Gini Alert]` measure |

### Visual 9.2 — State Gini Coefficient Bar Chart (Sorted)

| Property | Value |
|----------|-------|
| Type | Clustered Bar Chart |
| Size | Left half, 450 px (tall — show all 36 states) |
| Y-Axis | `state_analysis[state_clean]` |
| X-Axis | `state_analysis[intra_state_gini]` |
| Title | "Intra-State Digital Inequality (Gini Coefficient)" |
| Sort | Descending by Gini |
| Conditional formatting | Gradient: `#2ECC71` (low Gini, equal) → `#F39C12` → `#E74C3C` (high Gini, unequal) |
| Reference line | X = 0.5 labeled "High Inequality Threshold" |
| Data labels | ON |

**Insight:** States with high Gini (like Nagaland 0.704) have extreme disparity between their best and worst districts.

### Visual 9.3 — State Scatter: Gini vs Total Transactions

| Property | Value |
|----------|-------|
| Type | Scatter Chart |
| Size | Right half, 300 px |
| X-Axis | `state_analysis[total_transactions]` (log scale) |
| Y-Axis | `state_analysis[intra_state_gini]` |
| Size | `state_analysis[num_districts]` |
| Details | `state_analysis[state_clean]` |
| Title | "Transaction Volume vs Internal Inequality" |
| Quadrant lines | X median + Y = 0.5 → creates 4 quadrants |
| Labels | "High Volume, Low Inequality" (best), "High Volume, High Inequality" (need redistribution), etc. |

Create reference lines:
- X-axis: Median line (Analytics pane → Median line)
- Y-axis: Constant at 0.5

### Visual 9.4 — Underserved Districts Table

| Property | Value |
|----------|-------|
| Type | Table |
| Size | Full width, 250 px |
| Source | `underserved_districts` |
| Columns: |
| | Row number (1-50) |
| | `underserved_districts[state_clean]` |
| | `underserved_districts[district_clean]` |
| | `underserved_districts[total_txn]` — format: `#,0` |
| Title | "🚨 Bottom 50 Underserved Districts in India" |
| Conditional formatting | Entire row: Red background with increasing intensity for lower-ranked districts |
| Header | Bold, dark red background |

### Visual 9.5 — Underserved by State (Stacked Bar)

| Property | Value |
|----------|-------|
| Type | Stacked Bar Chart |
| Y-Axis | `underserved_districts[state_clean]` |
| X-Axis | Count of districts (from underserved_districts) |
| Title | "Which States Have the Most Underserved Districts?" |
| Color | `#E74C3C` |
| Sort | Descending |
| Insight | Northeastern states dominate the underserved list |

### Visual 9.6 — State Internal Range (Min-Max Bar)

| Property | Value |
|----------|-------|
| Type | Clustered Bar Chart |
| Y-Axis | `state_analysis[state_clean]` (Top 15 by `max_district_txn`) |
| X-Axis | Show both `min_district_txn` and `max_district_txn` as two series |
| Title | "District Transaction Range Within States (Min vs Max)" |
| Min color | `#E74C3C`, Max color | `#1ABC9C` |
| Insight | States like Maharashtra have enormous spread (Mumbai vs rural districts) |

### Visual 9.7 — Adoption Tier Transition Matrix (If multi-period data)

| Property | Value |
|----------|-------|
| Type | Matrix |
| Rows | State name |
| Columns | `fact_digital_divide[adoption_tier]` |
| Values | Count of districts |
| Title | "District Count by State × Adoption Tier" |
| Conditional formatting | Heat map coloring |
| Size | Full width |

### Visual 9.8 — Digital Inclusion Score Card (Custom KPI)

Create a composite score:
```dax
Digital Inclusion Score = 
VAR gini = AVERAGE(state_analysis[intra_state_gini])
VAR underserved_pct = [Pct Underserved]
VAR high_pct = DIVIDE([High Adoption District Count], [Total Districts], 0)
RETURN (1 - gini) * 0.4 + (1 - underserved_pct) * 0.3 + high_pct * 0.3
```

| Property | Value |
|----------|-------|
| Type | KPI Card |
| Value | `[Digital Inclusion Score]` |
| Format | `0.0%` |
| Title | "National Digital Inclusion Score" |
| Target | 0.7 (70%) |

---

## Page 10: Cash vs Digital

**Purpose:** Answer the billion-dollar question: "Is India going cashless?"

**Header:** "Cash vs Digital — Is India Really Going Cashless?"
**Subheader:** "Spoiler: No. India is becoming *less cash-dependent*, not cashless."

### Visual 10.1 — Hero KPI Row (4 cards)

| Card | Measure | Format | Color |
|------|---------|--------|-------|
| A | `[Current Digital to Cash Ratio]` | `0.00x` | `#1ABC9C` |
| B | `[Ratio Change Pct]` | `+0.0%` | `#2ECC71` |
| C | `[Current CIC Lakh Cr]` | `₹#,0.0 L Cr` | `#E74C3C` |
| D | `[Months to Parity]` | `~#,0 months` | `#3498DB` |

### Visual 10.2 — Dual Axis: UPI Value vs CIC (The Headline Chart)

| Property | Value |
|----------|-------|
| Type | Line and Clustered Column |
| Size | Full width, 300 px |
| X-Axis | `cash_displacement_analysis[date]` |
| Column Y | `cash_displacement_analysis[upi_value_lakh_cr]` |
| Line Y | `cash_displacement_analysis[cic_lakh_cr]` (secondary axis) |
| Title | "UPI Transaction Value vs Currency in Circulation (₹ Lakh Cr)" |
| Column color | `#1ABC9C` (UPI — growing fast) |
| Line color | `#E74C3C` (Cash — also growing!) |
| Line style | Thick (3px), with markers |
| Data labels | Last point on line only |
| Legend | ON, positioned top-right |
| **KEY INSIGHT annotation:** | Add a text box: "💡 Both lines go UP. Cash hasn't decreased — UPI is additive, not substitutive." |

### Visual 10.3 — Digital-to-Cash Ratio Trend

| Property | Value |
|----------|-------|
| Type | Area Chart |
| Size | Left half, 280 px |
| X-Axis | `cash_displacement_analysis[date]` |
| Y-Axis | `cash_displacement_analysis[digital_to_cash_ratio]` |
| Title | "Digital-to-Cash Ratio (UPI Value / CIC)" |
| Fill | `#1ABC9C`, 30% opacity |
| Line | `#16A085`, 2px |
| Reference lines | Y = 1.0 (labeled "Parity — UPI = Cash", dashed) |
| Reference lines | Y = 0.5 (labeled "Halfway", dotted) |
| Analytics | Trend line (linear), extrapolated |

### Visual 10.4 — Displacement Velocity (Speed of Change)

| Property | Value |
|----------|-------|
| Type | Combo: Column + Line |
| Size | Right half, 280 px |
| X-Axis | `cash_displacement_analysis[date]` |
| Column Y | `cash_displacement_analysis[displacement_velocity]` |
| Line Y | `cash_displacement_analysis[velocity_3m_avg]` (3-month moving avg) |
| Title | "Displacement Velocity (Monthly Change in Ratio)" |
| Column color | Green if positive, red if negative → use conditional formatting |
| Line | `#8E44AD`, dashed |
| Reference line | Y = 0 (zero line) |

### Visual 10.5 — Trend Classification (Donut)

| Property | Value |
|----------|-------|
| Type | Donut Chart |
| Size | 200 × 200 px |
| Legend | `cash_displacement_analysis[trend]` |
| Values | Count of months |
| Title | "Monthly Trend Distribution" |
| Colors | Accelerating: `#2ECC71`, Stable: `#F39C12`, Decelerating: `#E74C3C` |

### Visual 10.6 — UPI Volume Growth vs CIC Growth (Comparison)

| Property | Value |
|----------|-------|
| Type | Clustered Bar Chart |
| Category | Two bars: "UPI Volume Growth" and "CIC Growth" |
| Values | Latest growth rates from `cash_displacement_analysis` |
| Title | "Growth Rate Comparison: UPI vs Cash" |
| Colors | UPI: `#1ABC9C`, CIC: `#E74C3C` |
| Insight | UPI grows 20-40% while CIC grows 5-8% — UPI is outpacing but not replacing |

### Visual 10.7 — ATM Transactions Trend

| Property | Value |
|----------|-------|
| Type | Line Chart |
| Size | Left bottom, 350 × 220 px |
| X-Axis | `silver_rbi_atm[quarter_start_date]` |
| Y-Axis | `silver_rbi_atm[atm_transactions_millions]` |
| Title | "ATM Transactions (Millions per Quarter)" |
| Color | `#E67E22` |
| Analytics | Trend line |
| Insight | ATM usage is plateauing or declining — THIS is the clearest displacement signal |

### Visual 10.8 — Ratio 3-Month Moving Average vs Raw

| Property | Value |
|----------|-------|
| Type | Line Chart |
| Size | Right bottom |
| X-Axis | `cash_displacement_analysis[date]` |
| Line 1 | `digital_to_cash_ratio` (raw) — thin, light |
| Line 2 | `ratio_3m_avg` (smoothed) — thick, bold |
| Title | "Smoothed Displacement Trend (3-Month Average)" |

### Visual 10.9 — Insight Summary Box

| Property | Value |
|----------|-------|
| Type | Text Box |
| Background | `#E8F8F5` (light teal) |
| Border | 3px left `#1ABC9C` |
| Content | Multi-line insight: |
| | "**Finding:** India is NOT going cashless. Currency in circulation grew from ₹31.33L Cr to ₹38.24L Cr (+22%) even as UPI grew 122%. |
| | **What's happening:** UPI is digitizing previously informal cash transactions (chai, auto, vegetables) rather than replacing formal cash usage. |
| | **The real story:** India is becoming *less cash-dependent* — the digital-to-cash ratio nearly doubled from 0.31 to 0.68." |

---

## Page 11: Forecasting & Predictions

**Purpose:** Forward-looking analytics with ARIMA model results and seasonal patterns.

**Header:** "Looking Ahead — UPI Volume Forecasting"

### Visual 11.1 — Actual + Forecast Combo Chart (THE showcase visual)

| Property | Value |
|----------|-------|
| Type | Line Chart |
| Size | Full width, 350 px (hero visual) |

**This visual uses the pre-built `forecast_combined` table** (loaded from `forecast_combined.parquet`):

The table contains `date`, `volume_bn`, and `is_forecast` (true = ARIMA forecast, false = actual).
For confidence bands, also bring in `arima_forecast[arima_upper_bn]` and `arima_forecast[arima_lower_bn]`.

**In the Line Chart:**
| Field | Source |
|-------|--------|
| X-Axis | `forecast_combined[date]` |
| Y-Axis Line 1 | Actual values (filter: `is_forecast` = FALSE) |
| Y-Axis Line 2 | Forecast values (filter: `is_forecast` = TRUE) |
| Y-Axis Line 3 | Upper confidence bound (`arima_forecast[arima_upper_bn]`) |
| Y-Axis Line 4 | Lower confidence bound (`arima_forecast[arima_lower_bn]`) |

**Alternative (simpler):** Use TWO line charts overlaid, or use the **Area between lines** feature:
- Actual line: solid `#1ABC9C`, 2px
- Forecast line: dashed `#E74C3C`, 2px  
- Confidence band: Area between upper/lower, filled `#E74C3C` at 15% opacity

| Title | "UPI Monthly Volume: Actual + 12-Month ARIMA Forecast" |
| Reference line | Vertical line at the actual/forecast boundary, labeled "Forecast starts here →" |

**DAX for combined visual (alternative to using forecast_combined table directly):**
```dax
Combined Volume = 
VAR actual = SELECTEDVALUE(forecast_combined[volume_bn])
RETURN actual

Is Forecast Period = 
IF(SELECTEDVALUE(forecast_combined[is_forecast]) = TRUE(), "Forecast", "Actual")
```

### Visual 11.2 — Forecast Summary Cards (3 cards)

| Card | Measure | Format |
|------|---------|--------|
| A | ARIMA forecast for month +12 | `#,0.0 "Bn"` with title "12-Month Forecast" |
| B | Confidence interval width | `±#,0.0 "Bn"` with title "Confidence Range" |
| C | Latest actual | `#,0.0 "Bn"` with title "Current Monthly Volume" |

### Visual 11.3 — Seasonal Factors Bar Chart

| Property | Value |
|----------|-------|
| Type | Clustered Column Chart |
| Size | Left half, 280 px |
| X-Axis | `seasonal_factors[month]` (display as month names — create calculated column: `MonthName = FORMAT(DATE(2020, [month], 1), "MMM")`) |
| Y-Axis | `seasonal_factors[seasonal_factor]` |
| Title | "Monthly Seasonal Factors (Multiplicative)" |
| Reference line | Y = 1.0 (labeled "Baseline") |
| Conditional formatting | Above 1.0: `#1ABC9C`, Below 1.0: `#E74C3C` |
| Data labels | ON, format `0.000` |

**Insight annotations:**
- October bar: "🎆 Diwali Effect" (label)
- February bar: "📉 Shortest Month + Post-Holiday Lull"

### Visual 11.4 — Seasonal Radar/Spider Chart

| Property | Value |
|----------|-------|
| Type | Use a **custom visual** from AppSource: "Radar Chart" |
| Category | Month names (Jan-Dec) |
| Values | `seasonal_factors[seasonal_factor]` |
| Title | "Seasonal Profile — Radar View" |
| Fill | `#1ABC9C`, 20% opacity |
| Outline | `#16A085` |

If Radar chart isn't available, use a **Line Chart** with months on X-axis as a circular-looking alternative.

### Visual 11.5 — Forecast Accuracy Table

| Property | Value |
|----------|-------|
| Type | Table |
| Columns | Month | Forecast (Bn) | Lower Bound | Upper Bound | Confidence Width |
| Source | `arima_forecast` |
| Format | 2 decimal places |
| Title | "12-Month ARIMA Forecast Detail" |
| Conditional formatting | Width column: data bars (wider = less certain) |

### Visual 11.6 — YoY Growth Rate Trend

| Property | Value |
|----------|-------|
| Type | Column Chart |
| X-Axis | `silver_npci_monthly[date]` |
| Y-Axis | `silver_npci_monthly[yoy_volume_growth]` |
| Title | "Year-over-Year Volume Growth Rate" |
| Conditional formatting | Positive: `#2ECC71`, Negative: `#E74C3C` |
| Reference line | Y = 0 |
| Analytics | Trend line |
| Insight | Growth rate is decelerating (law of large numbers) but still 20%+ |

### Visual 11.7 — Methodology Note

| Property | Value |
|----------|-------|
| Type | Text Box |
| Background | `#EBF5FB` |
| Content | "📊 **Methodology:** ARIMA(1,1,1) model trained on 42 monthly data points (Jan 2022 – Jun 2025). Confidence intervals are 95%. The model captures trend and autocorrelation but not external shocks (regulatory changes, new competitors). Seasonal decomposition uses multiplicative model with period=12. Prophet model planned for future enhancement (requires Python 3.12)." |

---

## Page 12: User & Device Analytics

**Purpose:** PhonePe registered users and device brand market share — the hardware side of digital payments.

**Header:** "Users & Devices — Who Pays Digitally and With What?"

### Slicers

**Slicer 12.A — Year-Quarter:**
- Field: `silver_user_aggregates[quarter_start_date]`
- Style: Slider (date range)

### Visual 12.1 — Registered Users Growth Line

| Property | Value |
|----------|-------|
| Type | Area Chart |
| Size | Full width, 280 px |
| X-Axis | `silver_user_aggregates[quarter_start_date]` |
| Y-Axis | `silver_user_aggregates[registered_users]` |
| Title | "PhonePe Registered Users Over Time" |
| Fill | `#5F259F` (PhonePe purple), 20% opacity |
| Line | `#5F259F`, 2px |
| Data labels | Last point only, format as Crores (÷ 10M) |
| Analytics | Add trend line (linear) |

Create measure for formatting:
```dax
Registered Users Label = 
FORMAT(
    SELECTEDVALUE(silver_user_aggregates[registered_users]) / 10000000,
    "#,0.0"
) & " Cr"
```

### Visual 12.2 — QoQ User Growth Rate (Column)

| Property | Value |
|----------|-------|
| Type | Clustered Column Chart |
| Size | Left half, 250 px |
| X-Axis | Quarter labels |
| Y-Axis | QoQ growth rate (calculated) |
| Title | "User Growth Rate (Quarter-over-Quarter)" |
| Conditional formatting | Green for positive, amber for slowing growth |

Create measure (in Power Query, add a column for QoQ growth):
```
QoQ_User_Growth = 
VAR prev = CALCULATE(
    SELECTEDVALUE(silver_user_aggregates[registered_users]),
    DATEADD(silver_user_aggregates[quarter_start_date], -3, MONTH)
)
VAR curr = SELECTEDVALUE(silver_user_aggregates[registered_users])
RETURN DIVIDE(curr - prev, prev, BLANK())
```

### Visual 12.3 — Device Brand Market Share (Latest Quarter — Donut)

| Property | Value |
|----------|-------|
| Type | Donut Chart |
| Size | Right half, 280 px |
| Filter | Latest quarter only |
| Legend | `silver_device_brands[device_brand_clean]` |
| Values | `silver_device_brands[device_percentage]` |
| Title | "Current Device Brand Distribution (PhonePe Users)" |
| Colors | Xiaomi: `#FF6900`, Samsung: `#1428A0`, Vivo: `#415FFF`, Oppo: `#1D8348`, Realme: `#F1C40F`, Others: `#95A5A6` |
| Data labels | Brand + percentage |
| Top N | Show top 8, group rest as "Others" |

### Visual 12.4 — Device Brand Evolution (100% Stacked Area)

| Property | Value |
|----------|-------|
| Type | 100% Stacked Area Chart |
| Size | Full width, 300 px |
| X-Axis | `silver_device_brands[quarter_start_date]` |
| Y-Axis | `silver_device_brands[device_percentage]` |
| Legend | `silver_device_brands[device_brand_clean]` (Top 6 brands) |
| Title | "Device Brand Share Evolution Over Time" |
| Insight | Chinese brands (Xiaomi, Vivo, Oppo, Realme) dominate UPI user base |

### Visual 12.5 — Device Brand Count Trend (Multi-line)

| Property | Value |
|----------|-------|
| Type | Line Chart |
| Size | Left half, 250 px |
| X-Axis | `silver_device_brands[quarter_start_date]` |
| Y-Axis | `silver_device_brands[device_count]` |
| Legend | `silver_device_brands[device_brand_clean]` (Top 5) |
| Title | "Device User Count by Brand (Absolute)" |
| Y-Axis format | Millions |

### Visual 12.6 — Brand Share Change Table

| Property | Value |
|----------|-------|
| Type | Table |
| Columns | Brand | First Quarter Share | Latest Share | Change (pp) | Trend Arrow |
| Title | "Device Brand Market Dynamics" |
| Conditional formatting | Green arrow ↑ for gaining, Red arrow ↓ for losing |
| Sort | By latest share descending |

### Visual 12.7 — Users per Transaction Ratio

| Property | Value |
|----------|-------|
| Type | Line Chart |
| X-Axis | Quarter |
| Y-Axis | Create measure: Transactions per registered user per quarter |
| Title | "Average Transactions per User per Quarter" |
| Insight | Shows engagement depth — are new users actively transacting? |

```dax
Txn Per User = 
DIVIDE(
    SUM(fact_upi_transactions[txn_count]),
    SELECTEDVALUE(silver_user_aggregates[registered_users]),
    BLANK()
)
```

### Visual 12.8 — Chinese vs Indian vs Korean Brand Split (Stacked Bar)

Create a calculated column in Power Query:
```
Brand_Origin = 
SWITCH(TRUE(),
    silver_device_brands[device_brand_clean] IN {"Xiaomi", "Vivo", "Oppo", "Realme", "OnePlus", "Huawei", "Tecno", "Itel"}, "Chinese",
    silver_device_brands[device_brand_clean] IN {"Samsung"}, "Korean",
    silver_device_brands[device_brand_clean] IN {"Apple", "Google", "Motorola"}, "American",
    silver_device_brands[device_brand_clean] IN {"Lava", "Micromax", "Karbonn", "Jio"}, "Indian",
    "Other"
)
```

| Property | Value |
|----------|-------|
| Type | Stacked Bar |
| Y-Axis | `Brand_Origin` |
| X-Axis | Sum of `device_count` |
| Title | "UPI Users by Device Origin Country" |
| Insight | Massive dependence on Chinese hardware for India's digital payment infrastructure |

---

## Page 13: Insurance via UPI

**Purpose:** PhonePe's insurance distribution — UPI as a platform beyond payments.

**Header:** "Beyond Payments — Insurance Distribution via UPI"

### Visual 13.1 — Insurance KPI Cards (3)

| Card | Value | Format |
|------|-------|--------|
| A | Total Policies Sold | `#,0` with title "Total Insurance Policies" |
| B | Total Premium Collected | `₹#,0.0 Cr` with title "Premium Volume" |
| C | Avg Premium per Policy | `₹#,0` with title "Average Premium" |

### Visual 13.2 — Insurance Volume Trend (Combo)

| Property | Value |
|----------|-------|
| Type | Line and Clustered Column |
| Size | Full width, 300 px |
| X-Axis | `silver_insurance[quarter_start_date]` |
| Column Y | `silver_insurance[count]` (policies) |
| Line Y | `silver_insurance[amount]` (premium value) |
| Title | "Insurance Policies & Premium Trend" |
| Column color | `#3498DB` |
| Line color | `#E74C3C` |
| Secondary Y-axis | ON for premium |

### Visual 13.3 — QoQ Insurance Growth

| Property | Value |
|----------|-------|
| Type | Clustered Column |
| X-Axis | Quarter labels |
| Y-Axis | QoQ growth in policy count |
| Title | "Insurance Adoption Growth Rate" |
| Conditional formatting | Green gradient |

### Visual 13.4 — Average Premium Trend Line

| Property | Value |
|----------|-------|
| Type | Line Chart |
| X-Axis | `silver_insurance[quarter_start_date]` |
| Y-Axis | Calculated: `amount / count` |
| Title | "Average Premium per Policy (₹)" |
| Analytics | Trend line |
| Insight | Declining avg premium = micro-insurance products becoming popular |

### Visual 13.5 — Insurance as % of Total UPI (Card)

| Property | Value |
|----------|-------|
| Type | Card |
| Measure | Insurance transactions / Total UPI transactions × 100 |
| Title | "Insurance % of Total UPI Volume" |
| Insight | Tiny fraction — massive growth runway |

### Visual 13.6 — Insurance Cumulative Growth (Area)

| Property | Value |
|----------|-------|
| Type | Area Chart |
| X-Axis | `silver_insurance[quarter_start_date]` |
| Y-Axis | Running total of policies (use DAX TOTALYTD or running sum) |
| Title | "Cumulative Insurance Policies Sold" |

```dax
Cumulative Policies = 
CALCULATE(
    SUM(silver_insurance[count]),
    FILTER(
        ALL(silver_insurance[quarter_start_date]),
        silver_insurance[quarter_start_date] <= MAX(silver_insurance[quarter_start_date])
    )
)
```

---

## Page 14: Data Quality & Methodology

**Purpose:** Transparency page — data sources, freshness, known limitations.

**Header:** "Data Sources & Methodology"

### Visual 14.1 — Data Source Table

| Property | Value |
|----------|-------|
| Type | Table (styled) |
| Columns: |
| | Source Name |
| | URL / Reference |
| | Data Type |
| | Frequency |
| | Date Range |
| | Record Count |

| Source | Reference | Type | Frequency | Range | Records |
|--------|-----------|------|-----------|-------|---------|
| NPCI Official | npci.org.in | Monthly UPI stats | Monthly | Jan 2022 – Jun 2025 | 42 |
| NPCI Official | npci.org.in | App market share | Monthly | Mar 2023 – Mar 2025 | 91 |
| NPCI Official | npci.org.in | Yearly volumes | Annual | 2017 – 2024 | 8 |
| RBI DBIE | rbi.org.in | Currency in Circulation | Quarterly | Mar 2019 – Jun 2025 | 26 |
| RBI DBIE | rbi.org.in | ATM Transactions | Quarterly | Q1 2019 – Q2 2025 | 26 |
| PhonePe Pulse | github.com/PhonePe/pulse | Transaction data | Quarterly | Q1 2018 – Q4 2024 | 20,604 |
| PhonePe Pulse | github.com/PhonePe/pulse | User/Device data | Quarterly | Q1 2018 – Q4 2024 | 215 |
| PhonePe Pulse | github.com/PhonePe/pulse | Insurance data | Quarterly | Q2 2020 – Q4 2024 | 19 |

### Visual 14.2 — Architecture Diagram (Image)

| Property | Value |
|----------|-------|
| Type | Image |
| Source | Embed a screenshot of the Medallion Architecture diagram |
| Content | Bronze → Silver → Gold → Analytics → Power BI |
| Size | Full width, 200 px |

### Visual 14.3 — Data Pipeline Card

| Property | Value |
|----------|-------|
| Type | Text Box |
| Content | |
| | **Pipeline Architecture:** Medallion (Bronze → Silver → Gold) |
| | **Storage:** Parquet files + DuckDB analytical database |
| | **Processing:** Python (pandas, numpy, scikit-learn, statsmodels) |
| | **Analytics:** 4 modules (HHI, Forecasting, Geographic, Cash Displacement) |
| | **Total Records Processed:** 23,000+ Gold layer rows from 22,011 Bronze records |

### Visual 14.4 — Known Limitations Text

| Property | Value |
|----------|-------|
| Type | Text Box |
| Background | `#FEF9E7` |
| Content | |
| | **⚠️ Known Limitations:** |
| | 1. PhonePe Pulse data covers PhonePe only (~48% market) — not all UPI apps |
| | 2. NPCI market share data available only from Mar 2023 (13 snapshots) |
| | 3. RBI CIC is quarterly — monthly gaps are forward-filled from last quarterly value |
| | 4. District names from PhonePe use lowercase + "district" suffix — cleaned but some may mismatch |
| | 5. ARIMA model has only 42 data points — wide confidence intervals expected |
| | 6. Insurance data is PhonePe-only, not industry-wide |
| | 7. No demographic data (age, income, gender) available in public datasets |

### Visual 14.5 — Glossary Table

| Property | Value |
|----------|-------|
| Type | Table |
| Columns | Term | Definition |

| Term | Definition |
|------|-----------|
| UPI | Unified Payments Interface — real-time inter-bank payment system by NPCI |
| HHI | Herfindahl-Hirschman Index — market concentration measure (sum of squared shares) |
| CIC | Currency in Circulation — total physical cash in the economy |
| P2P | Person-to-Person transfer |
| P2M | Person-to-Merchant payment |
| Gini Coefficient | Inequality measure (0 = perfect equality, 1 = maximum inequality) |
| ARIMA | AutoRegressive Integrated Moving Average — time series forecasting model |
| Lakh Crore | 1 Lakh Crore = ₹1 Trillion = ₹10^12 |
| NPCI | National Payments Corporation of India |
| RBI DBIE | Reserve Bank of India — Database on Indian Economy |
| Fiscal Year | India: April to March (e.g., FY2023-24 = Apr 2023 – Mar 2024) |
| Adoption Tier | K-Means cluster label: Very Low / Low / Medium / High |

---

## Tooltip Page T1: District Detail

**Purpose:** Custom tooltip that appears when hovering over any district visual.

### Setup

1. Create a new page named "TT_District"
2. Format → Page Information → Toggle "Allow use as tooltip" → ON
3. Format → Canvas Settings → Type: Tooltip (auto-resizes to 320 × 240 px)
4. Set page background to `#2C3E50`

### Tooltip Visuals

**T1.1 — District Name (Title)**

| Property | Value |
|----------|-------|
| Type | Card |
| Field | `fact_digital_divide[district]` |
| Font | 16pt, White, Bold |
| No border, transparent background |

**T1.2 — State Name**

| Property | Value |
|----------|-------|
| Type | Card |
| Field | `fact_digital_divide[state]` |
| Font | 12pt, `#BDC3C7` |

**T1.3 — Transaction Count**

| Property | Value |
|----------|-------|
| Type | Card |
| Field | `[District Transactions]` |
| Format | `#,0` |
| Title | "Transactions" |
| Font | 14pt, `#1ABC9C` |

**T1.4 — Average Transaction Value**

| Property | Value |
|----------|-------|
| Type | Card |
| Field | `[District Avg Txn Value]` |
| Format | `₹#,0` |
| Title | "Avg Value" |

**T1.5 — Adoption Tier Badge**

| Property | Value |
|----------|-------|
| Type | Card |
| Field | `fact_digital_divide[adoption_tier]` |
| Conditional formatting | Background color by tier |

**T1.6 — National Percentile**

| Property | Value |
|----------|-------|
| Type | Card |
| Field | `fact_digital_divide[national_percentile]` |
| Format | `0.0 "th percentile"` |

### How to Use

On any visual showing district data, go to:
- Format pane → Tooltip → Type: **Report page** → Page: **TT_District**

Now hovering over a district bar/point shows this rich tooltip instead of the default.

---

## Tooltip Page T2: App Detail

**Purpose:** Custom tooltip for app market share visuals.

### Setup

1. New page "TT_App"
2. Toggle "Allow use as tooltip" → ON
3. Canvas Settings → Type: Tooltip
4. Background: `#2C3E50`

### Tooltip Visuals

**T2.1 — App Name**

| Property | Value |
|----------|-------|
| Type | Card |
| Field | `dim_app[app_name]` |
| Font | 16pt, White, Bold |

**T2.2 — Parent Company**

| Property | Value |
|----------|-------|
| Type | Card |
| Field | `dim_app[parent_company]` |
| Font | 11pt, `#BDC3C7` |

**T2.3 — Current Market Share**

| Property | Value |
|----------|-------|
| Type | Card |
| Field | `silver_app_market_share[market_share_pct]` |
| Format | `0.0 "%"` |
| Title | "Market Share" |

**T2.4 — NPCI Cap Status**

| Property | Value |
|----------|-------|
| Type | Card |
| Field | `[Above Cap Flag]` measure |
| Conditional formatting | Red if above, green if below |

**T2.5 — Mini Sparkline (Share trend)**

| Property | Value |
|----------|-------|
| Type | Sparkline (Line Chart, tiny) |
| X-Axis | `silver_app_market_share[date]` |
| Y-Axis | `silver_app_market_share[market_share_pct]` |
| Size | 200 × 60 px |
| No axes, no labels, just the line |

---

## Bookmarks & Navigation Setup

### Bookmark 1: "Executive View"
- **What it does:** Resets all filters, navigates to Page 2
- **How to create:** Clear all slicers, go to Page 2, View → Bookmarks → Add → Name: "Executive View"

### Bookmark 2: "Paytm Collapse Analysis"
- **What it does:** Navigates to Page 6, filters date to 2024, highlights Paytm
- **Steps:** Go to Page 6, set date slicer to 2024, click Paytm in slicer, add annotation text box. Save bookmark.

### Bookmark 3: "Northeast Focus"
- **What it does:** Filters geographic pages to Northeast region
- **Steps:** Go to Page 7, select "Northeast" in region slicer. Save bookmark.

### Bookmark 4: "Underserved Districts Alert"
- **What it does:** Shows Page 9, filters to Very Low + Low adoption tiers
- **Steps:** Go to Page 9, select tier filters. Save bookmark.

### Bookmark 5: "Cashless Myth"
- **What it does:** Shows Page 10 with all visuals highlighting the key finding
- **Steps:** Go to Page 10, no filters needed (the page IS the story). Save bookmark.

### Bookmark 6: "Future Outlook"
- **What it does:** Shows Page 11 (Forecasting)
- **Steps:** Go to Page 11, save bookmark.

### Navigation Button Setup on ALL Pages

Add a **"← Back to Home"** button on every page (except Page 1):
1. Insert → Button → Back (or Blank)
2. Action → Page Navigation → Page 1
3. Position: Top-left corner, 100 × 30 px
4. Style: Transparent bg, White text, Segoe UI 10pt

Add a **page navigation bar** at the bottom of every page:
1. Use Shape → Rectangle (full width, 40px tall, `#2C3E50`)
2. Add 14 small buttons on it, one per page
3. Each button: Action → Page Navigation → respective page
4. Highlight current page button with `#1ABC9C` underline

---

## Theme & Visual Polish

### Custom Theme JSON

Create a file `dashboards/upi_theme.json`:

```json
{
  "name": "UPI Pulse Analytics",
  "dataColors": [
    "#1ABC9C", "#3498DB", "#9B59B6", "#E74C3C", "#F39C12",
    "#2ECC71", "#E67E22", "#1F77B4", "#5F259F", "#00BAF2"
  ],
  "background": "#FFFFFF",
  "foreground": "#2C3E50",
  "tableAccent": "#1ABC9C",
  "textClasses": {
    "callout": {
      "fontSize": 28,
      "fontFace": "Segoe UI Light",
      "color": "#2C3E50"
    },
    "title": {
      "fontSize": 14,
      "fontFace": "Segoe UI Semibold",
      "color": "#2C3E50"
    },
    "header": {
      "fontSize": 11,
      "fontFace": "Segoe UI",
      "color": "#2C3E50"
    },
    "label": {
      "fontSize": 10,
      "fontFace": "Segoe UI",
      "color": "#7F8C8D"
    }
  },
  "visualStyles": {
    "*": {
      "*": {
        "background": [{"color": {"solid": {"color": "#FFFFFF"}}}],
        "border": [{"show": false}],
        "dropShadow": [{"show": false}],
        "visualHeader": [{"show": false}],
        "padding": [{"top": 8, "bottom": 8, "left": 12, "right": 12}]
      }
    },
    "card": {
      "*": {
        "wordWrap": [{"show": true}]
      }
    }
  }
}
```

**To apply:** View → Themes → Browse for themes → Select `upi_theme.json`

### Color Palette Reference

| Use Case | Color | Hex |
|----------|-------|-----|
| Primary (UPI/Digital) | Teal/Turquoise | `#1ABC9C` |
| Secondary (Charts) | Blue | `#3498DB` |
| Accent (Highlights) | Purple | `#9B59B6` |
| Danger/Cash/Alert | Red | `#E74C3C` |
| Warning/Moderate | Amber | `#F39C12` |
| Success/Growth | Green | `#2ECC71` |
| Background (Dark) | Navy | `#2C3E50` |
| Background (Light) | Off-white | `#F8F9FA` |
| Text Primary | Dark gray | `#2C3E50` |
| Text Secondary | Medium gray | `#7F8C8D` |
| PhonePe Brand | Purple | `#5F259F` |
| Google Pay Brand | Blue | `#4285F4` |
| Paytm Brand | Cyan | `#00BAF2` |

### Typography Rules

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Page Title | Segoe UI | 22pt | Bold |
| Section Header | Segoe UI | 14pt | Semibold |
| Visual Title | Segoe UI | 12pt | Semibold |
| Data Label | Segoe UI | 10pt | Regular |
| Axis Label | Segoe UI | 9pt | Regular |
| Tooltip Text | Segoe UI | 10pt | Regular |
| KPI Value | Segoe UI Light | 28pt | Light |
| KPI Label | Segoe UI | 10pt | Regular |

### Global Formatting Rules

1. **No visual borders** — use white space to separate
2. **No drop shadows** — flat design only
3. **Visual headers hidden** — use text boxes for titles (cleaner)
4. **Consistent padding** — 12px on all sides
5. **Axis titles** — show Y-axis title only when unit is unclear
6. **Gridlines** — light gray, Y-axis only, X-axis gridlines OFF
7. **Legend position** — top-right for line charts, bottom for pie/donut
8. **Data labels** — ON for bar charts, OFF for dense line charts (use tooltip)
9. **Responsive layout** — test at 1280×720 AND 1920×1080

---

## Interactions Configuration

### Cross-filtering Rules

Set up visual interactions (Format → Edit Interactions) on key pages:

**Page 2 (Executive Summary):**
- Donut chart (category) → Cross-filters all other visuals
- State bar chart → Doesn't filter KPI cards (set to "None")

**Page 5 (Market Concentration):**
- HHI trend line → Cross-filters share table
- Treemap → Cross-highlights app share area chart

**Page 7 (Geographic):**
- Map clicks → Cross-filter ranking table + region donut
- Region donut → Cross-filters map + ranking table

**Page 8 (District):**
- Cluster scatter → Cross-filters district table
- Tier donut → Cross-filters scatter + table + maps

**Page 10 (Cash vs Digital):**
- DISABLE cross-filtering between all visuals (each tells its own story)
- How: Select each visual → Format → Edit Interactions → Click "None" (⊘) on every other visual

---

## Drill-Down & Drill-Through Configuration

### Drill-Down Hierarchies

**Hierarchy 1: Time**
- Year → Quarter → Month
- Used in: Pages 2, 3, 4, 11

**Hierarchy 2: Geography**
- Region → State → District
- Used in: Pages 7, 8, 9

**Hierarchy 3: Category**
- P2P/P2M → Category Name
- Used in: Page 4

### Drill-Through Pages

| Source Page | Target Page | Drill-Through Field | What Happens |
|------------|-------------|--------------------|-|
| Page 7 (State Map) | Page 8 (District) | `state` | Right-click state → "Drill through to District Analysis" — Page 8 opens filtered to that state |
| Page 5 (App Treemap) | Page 6 (App Dynamics) | `app_name` | Right-click app → See that app's full trajectory |
| Page 2 (Top 5 States) | Page 7 (Geographic) | `state` | Right-click state bar → Jump to full geographic view |
| Page 9 (Underserved Table) | Page 8 (District) | `state_clean` | Right-click underserved district → See all districts in that state |

**How to set up drill-through:**
1. Go to the TARGET page (e.g., Page 8)
2. In Visualizations pane → find "Drill through" section at the bottom
3. Drag the field (e.g., `fact_digital_divide[state]`) into the Drill through well
4. Power BI automatically adds a "← Back" button
5. Now on the SOURCE page, right-clicking a data point shows "Drill through → [Target Page]"

---

## Final Checklist

### Before Publishing

- [ ] All 14 pages + 2 tooltip pages created
- [ ] All 65+ DAX measures working (no errors in measure table)
- [ ] Theme applied consistently (import `upi_theme.json`)
- [ ] All slicers have sync groups configured (View → Sync Slicers)
- [ ] Drill-through works from Pages 7→8, 5→6, 2→7
- [ ] Bookmarks created and buttons linked
- [ ] Tooltip pages configured on district + app visuals
- [ ] Navigation bar on every page
- [ ] All visuals have titles
- [ ] Conditional formatting applied (HHI gauge, Gini bars, adoption tiers)
- [ ] Data labels clean (no overlapping)
- [ ] Mobile layout configured (View → Mobile Layout → arrange key visuals)
- [ ] Performance: Check Performance Analyzer (View → Performance Analyzer) — all visuals render in <3s

### Slicer Sync Groups

Sync slicers across pages so selecting a year on one page applies everywhere:

1. View → Sync Slicers
2. Create sync group "Year" — add year slicers from Pages 2, 3, 4, 7, 8
3. Create sync group "State" — add state slicers from Pages 7, 8, 9
4. For each slicer, check "Sync" (same value) and optionally "Visible" (show/hide per page)

---

## Visual Count Summary

| Page | # Visuals | Key Visual Types |
|------|-----------|-----------------|
| 1. Cover & Navigation | 7 | Cards, Buttons, Text |
| 2. Executive Summary | 9 | Cards, Line, Donut, Bar, Gauge, Combo |
| 3. UPI Growth Story | 8 | Column+Line, Area, Line, Matrix, Waterfall |
| 4. Transaction Deep Dive | 9 | Stacked Area, Donut×2, Line, Bar, Matrix, Small Multiples, Stacked Bar |
| 5. Market Concentration | 9 | Gauge, Line×2, Bar, Treemap, Stacked Area, Table, Text |
| 6. App Market Share | 7 | Multi-line, Scatter, Waterfall, Stacked Bar, Table, Bookmark Button |
| 7. Geographic Overview | 8 | Filled Map, Table, Bar×2, Donut, Small Multiples, Bar, Bar |
| 8. District Drill Down | 9 | Shape Map, Scatter, Donut, Table, Bar×2, Histogram, Line |
| 9. Digital Divide | 9 | Card, Bar, Scatter, Table, Stacked Bar, Bar, Matrix, KPI |
| 10. Cash vs Digital | 10 | Cards×4, Combo, Area, Combo, Donut, Bar, Line, Line, Text |
| 11. Forecasting | 8 | Line (hero), Cards×3, Column, Radar, Table, Column |
| 12. Users & Devices | 9 | Area, Column, Donut, Stacked Area, Line, Table, Line, Stacked Bar |
| 13. Insurance | 7 | Cards×3, Combo, Column, Line, Card, Area |
| 14. Data Quality | 5 | Table, Image, Text×3 |
| TT1: District Tooltip | 6 | Cards×6 |
| TT2: App Tooltip | 5 | Cards×4, Sparkline |
| **TOTAL** | **~125** | |

---

## DAX Measures Summary

| Category | Count | Examples |
|----------|-------|---------|
| Volume & Value | 6 | Total Transactions, Total Value, Avg Txn Value |
| Growth | 5 | YoY Growth, QoQ Growth, CAGR, MoM |
| Market Concentration | 8 | Current HHI, Equivalent Firms, PhonePe Share, Cap Excess |
| Cash Displacement | 7 | Ratio, Velocity, CIC, Months to Parity, Trend |
| Geographic | 10 | Total Districts, Underserved Count, Gini, Metro Split |
| Forecasting | 6 | ARIMA Forecast, Confidence Width, Seasonal Factor |
| Users & Devices | 5 | Registered Users, QoQ Growth, Txn Per User |
| Insurance | 5 | Policies, Premium, Avg Premium, QoQ Growth |
| Formatting | 8 | Growth Color, Tier Color, Gini Alert, Dynamic Titles |
| Navigation | 5 | Labels, Subtitles, Last Updated |
| **TOTAL** | **~65** | |

---

*This guide was generated from the UPI Analytics Platform Gold layer containing 23,000 rows across 17 Parquet files, enriched with Silver layer detail tables for maximum visual richness.*
