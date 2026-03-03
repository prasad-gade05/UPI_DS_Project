# Task 0: Download Execution Log

> **Status:** ✅ Completed  
> **Date:** 2026-02-26  
> **Environment:** PowerShell 7.5.4 on Windows  
> **Machine path:** `D:\AI_SLOP\`

---

## What Was Done

### 1. Created raw data directory

```powershell
New-Item -ItemType Directory -Force -Path "D:\AI_SLOP\data_raw"
```

### 2. Cloned PhonePe Pulse repository

```powershell
git clone --depth 1 https://github.com/PhonePe/pulse.git "D:\AI_SLOP\data_raw\phonepe-pulse"
```

- **Source:** https://github.com/PhonePe/pulse  
- **Clone type:** `--depth 1` (shallow clone — all files, latest commit only)  
- **Destination:** `D:\AI_SLOP\data_raw\phonepe-pulse\`
- **License:** CDLA-Permissive-2.0 (academically safe for research use)

---

## Verification Outputs

### Top-level data categories

```powershell
Get-ChildItem "D:\AI_SLOP\data_raw\phonepe-pulse\data" | Format-Table Name
```

```
Name
----
aggregated
map
top
```

✅ All 3 expected top-level categories present.

---

### Total JSON file count

```powershell
(Get-ChildItem "D:\AI_SLOP\data_raw\phonepe-pulse\data" -Recurse -Filter "*.json").Count
```

```
9026
```

✅ **9,026 JSON files** — well above the ~5,000 minimum expected. Full dataset confirmed.

---

### Aggregated transaction spot-check (2024 Q4, national level)

```powershell
Get-Content "D:\AI_SLOP\data_raw\phonepe-pulse\data\aggregated\transaction\country\india\2024\4.json" |
    ConvertFrom-Json |
    Select-Object -ExpandProperty data |
    Select-Object -ExpandProperty transactionData |
    Select-Object -First 3
```

```
name                     paymentInstruments
----                     ------------------
Merchant payments        {@{type=TOTAL; count=17419191808; amount=8081429560226}}
Peer-to-peer payments    {@{type=TOTAL; count=9368204284; amount=26633866936498}}
Recharge & bill payments {@{type=TOTAL; count=1392529171; amount=1255972669825}}
```

✅ JSON schema confirmed: `transactionData[]` array with `name` + `paymentInstruments[{type, count, amount}]` — exactly matches what the ingester code expects.

**Key data point from Q4 2024:**
| Category | Transactions | Amount (₹) |
|----------|-------------|-----------|
| Merchant payments | 17.4 billion | ₹8.08 lakh crore |
| Peer-to-peer payments | 9.4 billion | ₹26.6 lakh crore |
| Recharge & bill payments | 1.4 billion | ₹1.26 lakh crore |

---

### Full 9-category verification

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

```
Category               Exists JsonFiles
--------               ------ ---------
aggregated\transaction   True      1036
aggregated\user          True      1036
aggregated\insurance     True       703
map\transaction          True      1036
map\user                 True      1036
map\insurance            True      1404
top\transaction          True      1036
top\user                 True      1036
top\insurance            True       703
```

✅ All 9 categories present with substantial file counts.

**Total breakdown: 9,026 JSON files across:**
| Category Group | Files |
|---------------|-------|
| aggregated/* | 2,775 |
| map/* | 3,476 |
| top/* | 2,775 |

---

### Available years check

```powershell
Get-ChildItem "D:\AI_SLOP\data_raw\phonepe-pulse\data\aggregated\transaction\country\india" |
    Select-Object Name | Sort-Object Name
```

```
Name
----
2018
2019
2020
2021
2022
2023
2024
state
```

✅ **7 years of data: 2018–2024.** Covers the full UPI growth story from near-zero to 16+ billion monthly transactions.

> **Note:** The `state` directory contains state-level breakdowns (not a year). Expected.

---

## Summary of Downloaded Data

| Attribute | Value |
|-----------|-------|
| **Repository** | PhonePe/pulse |
| **Clone method** | `--depth 1` (shallow) |
| **Local path** | `D:\AI_SLOP\data_raw\phonepe-pulse\` |
| **Total JSON files** | 9,026 |
| **Years covered** | 2018, 2019, 2020, 2021, 2022, 2023, 2024 |
| **Quarters covered** | Q1–Q4 for each year (latest: Q4 2024) |
| **Data categories** | 9 (aggregated, map, top × transaction, user, insurance) |
| **Geographic depth** | National → State → District level |
| **License** | CDLA-Permissive-2.0 |

---

## NPCI & RBI Data

No download was required. Both datasets are pre-curated in the ingester code:

- **NPCI:** Monthly UPI volumes (2020–2025) + yearly aggregates (2017–2024) + app market share (3 months) hardcoded in `NPCIIngester`
- **RBI:** Quarterly currency-in-circulation (2020–2025) + ATM volumes (2021–2024) hardcoded in `RBIIngester`

These are written to `data/bronze/` as Parquet files when the pipeline runs.

---

## Next Step

**→ Task 1: Project Directory Structure Setup** *(pending instruction to begin)*

Will create: `src/`, `data/bronze/silver/gold/`, `config/`, `tests/`, `docs/` tree; initialize `pyproject.toml`, `requirements.txt`, config YAMLs, and base Python modules.
