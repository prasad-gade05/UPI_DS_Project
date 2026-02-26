# Task 0: Data Download Guide

> **Status:** ⏳ Pending execution  
> **Prerequisites:** Git, Python 3.x, ~2GB free disk space  
> **Next Task:** Task 1 — Project directory structure setup

---

## Overview

There are **3 data sources** for this project. Only **Source 1 (PhonePe Pulse)** requires an actual download. Sources 2 and 3 (NPCI + RBI) are **already fully curated** as Python dictionaries in the ingester code — the pipeline writes them to Parquet directly, no download needed.

| Source | Method | Size | Action |
|--------|--------|------|--------|
| PhonePe Pulse (GitHub) | `git clone` | ~600MB–1.2GB | ✅ Download required |
| NPCI Statistics | Hardcoded in `NPCIIngester` | — | ✅ Already curated |
| RBI DBIE | Hardcoded in `RBIIngester` | — | ✅ Already curated |

---

## SOURCE 1: PhonePe Pulse — Git Clone

This is the main data download. It is a public GitHub repository containing 7 years (2018–2024) of quarterly, district-level UPI transaction JSON files across all 36 Indian states/UTs.

### Step 1 — Create raw data directory and clone

Open **PowerShell** and run the following commands:

```powershell
# Create a dedicated raw data folder outside the project (raw data ≠ source code)
New-Item -ItemType Directory -Force -Path "D:\AI_SLOP\data_raw"

# Clone with --depth 1 to get all files but only the latest commit
# This saves ~200MB compared to a full clone with history
git clone --depth 1 https://github.com/PhonePe/pulse.git "D:\AI_SLOP\data_raw\phonepe-pulse"
```

> ⏱️ **Expected time:** 5–15 minutes depending on internet speed (thousands of JSON files).  
> 📁 **Location after clone:** `D:\AI_SLOP\data_raw\phonepe-pulse\`

---

### Step 2 — Verify the folder structure

After the clone finishes, run these commands to confirm the data is complete:

```powershell
# View top-level data categories
Get-ChildItem "D:\AI_SLOP\data_raw\phonepe-pulse\data" | Format-Table Name

# Count total JSON files — should be 3000+
(Get-ChildItem "D:\AI_SLOP\data_raw\phonepe-pulse\data" -Recurse -Filter "*.json").Count
```

**Expected top-level structure:**
```
data/
├── aggregated/
│   ├── transaction/    ← National + state-level, by payment type
│   ├── user/           ← Registered users + app opens
│   └── insurance/      ← Insurance transactions
├── map/
│   ├── transaction/    ← DISTRICT-LEVEL data (most valuable)
│   ├── user/
│   └── insurance/
└── top/
    ├── transaction/    ← Top states/districts/pincodes ranking
    ├── user/
    └── insurance/
```

---

### Step 3 — Spot-check a data file

Confirm the JSON schema matches what the pipeline expects:

```powershell
# Check aggregated transaction structure (national level, 2024 Q4)
Get-Content "D:\AI_SLOP\data_raw\phonepe-pulse\data\aggregated\transaction\country\india\2024\4.json" |
    ConvertFrom-Json |
    Select-Object -ExpandProperty data |
    Select-Object -ExpandProperty transactionData |
    Select-Object -First 3
```

**Expected output** — array of payment categories:
```
name                     paymentInstruments
----                     ------------------
Recharge & bill payments {…}
Financial Services       {…}
Merchant payments        {…}
```

```powershell
# Check district-level data structure (Karnataka, 2024 Q1)
Get-Content "D:\AI_SLOP\data_raw\phonepe-pulse\data\map\transaction\hover\country\india\state\karnataka\2024\1.json" |
    ConvertFrom-Json |
    Select-Object -ExpandProperty data |
    Select-Object -ExpandProperty hoverDataList |
    Select-Object -First 3
```

**Expected output** — array of districts (note: lowercase with " district" suffix):
```
name                    metric
----                    ------
bengaluru urban district {…}
mysuru district          {…}
tumakuru district        {…}
```

---

### Step 4 — Full verification checklist

Run this to confirm all 9 data categories are present:

```powershell
$base = "D:\AI_SLOP\data_raw\phonepe-pulse\data"

@(
    "aggregated\transaction",
    "aggregated\user",
    "aggregated\insurance",
    "map\transaction",
    "map\user",
    "map\insurance",
    "top\transaction",
    "top\user",
    "top\insurance"
) | ForEach-Object {
    $path = Join-Path $base $_
    $exists = Test-Path $path
    $count = if ($exists) {
        (Get-ChildItem $path -Recurse -Filter "*.json").Count
    } else { 0 }
    [PSCustomObject]@{
        Category  = $_
        Exists    = $exists
        JsonFiles = $count
    }
} | Format-Table -AutoSize
```

**Expected output** — all 9 rows with `Exists = True` and non-zero `JsonFiles`:
```
Category                  Exists JsonFiles
--------                  ------ ---------
aggregated\transaction      True       56
aggregated\user             True       56
aggregated\insurance        True       28
map\transaction             True     2016
map\user                    True     2016
map\insurance               True      448
top\transaction             True       56
top\user                    True       56
top\insurance               True       28
```

> The exact counts may vary; what matters is that all 9 are non-zero.

---

### Step 5 — Check available years

```powershell
# Confirm years 2018–2024 are present
Get-ChildItem "D:\AI_SLOP\data_raw\phonepe-pulse\data\aggregated\transaction\country\india" |
    Select-Object Name | Sort-Object Name
```

**Expected:** Directories named `2018`, `2019`, `2020`, `2021`, `2022`, `2023`, `2024`.

---

## SOURCE 2: NPCI Statistics — No Download Needed ✅

All NPCI data is **already hardcoded** in the plan's `NPCIIngester` class as Python dictionaries. This covers:

- **Monthly UPI volumes** (2020–2025): Transaction count (billions) + value (₹ lakh crore) per month
- **Yearly UPI aggregates** (2017–2024): Long-term trend data
- **App market share** (Dec 2024, Jan 2025, Mar 2025): PhonePe, GPay, Paytm, CRED, Amazon Pay, WhatsApp Pay

The ingester writes all of this to `data/bronze/npci/` as Parquet files automatically when the pipeline runs.

### Optional: Extend market share data

The curated data currently covers only 3 months. For a stronger HHI trend analysis, manually add historical months:

1. Go to: https://www.npci.org.in/what-we-do/upi/product-statistics
2. Scroll to the **"UPI App-wise Transaction Volume"** section
3. The site is JS-rendered — use **Chrome DevTools** (F12 → Elements) to read the table
4. Add entries to `UPI_APP_MARKET_SHARE` in the `NPCIIngester` class

---

## SOURCE 3: RBI DBIE — No Download Needed ✅

All RBI data is **already hardcoded** in the plan's `RBIIngester` class:

- **Currency in Circulation** (quarterly, 2020–2025): End-of-quarter CIC in ₹ lakh crore
- **ATM transaction volumes** (quarterly, 2021–2024): Millions of ATM transactions per quarter

The ingester writes these to `data/bronze/rbi/` automatically.

### Optional: Verify/extend RBI numbers

If you want to validate or add more history:

1. Go to: https://dbie.rbi.org.in
2. Navigate: **Statistics → Currency → Currency in Circulation**
3. Download Excel → Cross-check with values in `CURRENCY_IN_CIRCULATION` dict

---

## Important Notes

> **⚠️ PhonePe Pulse = PhonePe transactions only**  
> The Pulse dataset covers ~48% of the UPI market (PhonePe's transactions only). It is used for **geographic district-level granularity**. NPCI data is used for **total market volumes and market share**. All dashboards and visualizations should attribute the source clearly.

> **⚠️ Latest data is Q4 2024**  
> As of March 2025, the PhonePe Pulse repo contains data through Q4 2024. No 2025 quarterly data has been published yet. The pipeline handles this gracefully — it will log "no new data found" and use existing data.

> **⚠️ District name format**  
> District names in the JSON files are **lowercase with a " district" suffix** (e.g., `"mysuru district"`, `"bengaluru urban district"`). The Silver layer cleaning code strips this suffix and applies title case. Do not manually rename or transform the raw files.

---

## After Successful Download

Once the PhonePe Pulse clone is verified, proceed to:

**→ Task 1: Project Directory Structure Setup**

This will create the full `src/`, `data/bronze/silver/gold/`, `config/`, `tests/`, and `docs/` directory tree, initialize the Python project (`pyproject.toml`, `requirements.txt`), write all config YAMLs, and push the scaffold to GitHub.
