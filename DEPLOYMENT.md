# Deployment Guide -- Streamlit Community Cloud

Step-by-step guide to deploy the UPI Analytics Platform on Streamlit Community Cloud (100% free).

---

## Prerequisites

Before you start, make sure you have:

1. A **GitHub account** with this repository pushed to it
2. The repository must be **public** (Streamlit Community Cloud free tier requires public repos)
3. All gold export parquet files committed to `data/gold/exports/` (they already are)

---

## Step 1: Push Your Code to GitHub

If you have not already pushed to GitHub:

```bash
# Add your GitHub remote (replace with your username/repo)
git remote add origin https://github.com/YOUR_USERNAME/UPI_DS_Project.git

# Push to main branch
git push -u origin main
```

Verify on GitHub that these files exist:
- `src/visualization/app.py` (the Streamlit entry point)
- `requirements.txt` (Python dependencies)
- `.streamlit/config.toml` (theme and server config)
- `data/gold/exports/*.parquet` (28 parquet files)

---

## Step 2: Sign Up for Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign in with GitHub"**
3. Authorize Streamlit to access your GitHub account
4. You will land on the Streamlit Cloud dashboard

---

## Step 3: Deploy the App

1. Click **"New app"** (top right corner)
2. Fill in the deployment form:

| Field | Value |
|-------|-------|
| **Repository** | `YOUR_USERNAME/UPI_DS_Project` |
| **Branch** | `main` |
| **Main file path** | `src/visualization/app.py` |

3. Click **"Advanced settings"** (optional):
   - Python version: `3.11` (recommended -- Prophet works best here)
   - You do not need to add any secrets for this app

4. Click **"Deploy!"**

---

## Step 4: Wait for Build

The first deployment takes 5--10 minutes because Streamlit Cloud needs to:
1. Clone your repository
2. Install all packages from `requirements.txt`
3. Build Prophet (this is the slowest dependency -- it compiles C++ code)

You will see a build log in real time. Common issues:

| Issue | Solution |
|-------|----------|
| Build fails on `prophet` | Make sure `requirements.txt` has `prophet>=1.1.5` (not `fbprophet`) |
| Memory error during build | Remove unused packages from `requirements.txt` to reduce install footprint |
| App crashes on start | Check the Streamlit Cloud logs for the error traceback |

---

## Step 5: Verify the Deployment

Once deployed, your app will be live at:

```
https://YOUR_USERNAME-upi-ds-project-srcvisualizationapp-XXXXX.streamlit.app
```

Check all 11 tabs:
- [ ] Overview -- Hero section, key insights, project scale cards
- [ ] Executive Summary -- KPIs, yearly charts, category breakdown
- [ ] Market Concentration -- HHI gauge, trend line, market share visuals
- [ ] Geographic Insights -- Choropleth map, state rankings, treemap
- [ ] Forecasting -- Actual vs forecast chart, seasonal factors
- [ ] Cash Displacement -- Dual-axis chart, ratio trend, ATM data
- [ ] Growth & Trends -- CAGR, heatmap, festival impact
- [ ] App Dynamics -- Individual app trajectories, Paytm collapse analysis
- [ ] District Deep Dive -- Scatter plot, Gini bars, underserved table
- [ ] Users & Devices -- Registration growth, device brands, insurance
- [ ] Methodology -- Pipeline architecture, data quality, tech stack

---

## Step 6: Set a Custom URL (Optional)

1. Go to your Streamlit Cloud dashboard
2. Click the three-dot menu next to your app
3. Click **"Settings"**
4. Under **"General"**, you can set a custom subdomain:
   - Example: `upi-analytics.streamlit.app`
   - This makes the URL cleaner for sharing in applications and CVs

---

## Step 7: Set Up Automatic Data Refresh (Optional)

The repository includes a GitHub Actions workflow (`.github/workflows/data_refresh.yml`) that runs the full data pipeline monthly and commits updated parquet files. When new data is pushed to `main`, Streamlit Cloud automatically redeploys.

To enable this:
1. Go to your GitHub repo → **Settings** → **Actions** → **General**
2. Ensure "Allow all actions" is selected
3. The workflow runs on the 5th of every month via cron
4. It re-ingests data from NPCI and PhonePe Pulse, re-runs the pipeline, and commits updated exports

This means your dashboard stays current without manual intervention.

---

## Troubleshooting

### App shows "No data found"

The parquet files in `data/gold/exports/` are not being found. Check:
- Are the parquet files committed to git? Run `git ls-files data/gold/exports/` -- you should see 28+ files
- Is the `.gitignore` correctly configured? It must have `!data/gold/exports/*.parquet`

### Build fails with memory errors

Streamlit Cloud free tier has 1GB memory limit. If Prophet causes issues:
- Try pinning `prophet==1.1.5` (smaller build)
- Or temporarily remove `prophet` from requirements if you do not need the forecasting tab

### App is slow on first load

Normal. The first visitor after a cold start triggers data loading (~5 seconds). Subsequent loads are cached for 1 hour. Streamlit Cloud also puts apps to sleep after inactivity -- the next visitor triggers a cold start.

### Maps do not render

The India choropleth map loads GeoJSON from a public GitHub Gist URL. If that URL is down, the app falls back to a bar chart. This is handled automatically.

### Prophet import fails on Cloud

If you see `ModuleNotFoundError: No module named 'prophet'`:
- Make sure `requirements.txt` lists `prophet>=1.1.5` (not `fbprophet`)
- Prophet requires `pystan` which is installed automatically
- If it still fails, try adding `pystan==2.19.1.1` to requirements.txt

---

## Architecture on Streamlit Cloud

```
GitHub Repository (main branch)
    │
    ├── src/visualization/app.py        ← Streamlit entry point
    ├── src/visualization/pages/        ← 11 tab modules
    ├── src/visualization/components/   ← Charts, KPIs, styles, data loader
    ├── data/gold/exports/*.parquet     ← Pre-computed analytics data (committed)
    ├── .streamlit/config.toml          ← Theme and server settings
    └── requirements.txt                ← Python dependencies
            │
            ▼
    Streamlit Community Cloud
    - Clones repo on deploy
    - Installs requirements.txt
    - Runs: streamlit run src/visualization/app.py
    - Auto-redeploys on push to main
    - Free tier: 1GB RAM, public repos only
```

The app reads parquet files directly from the committed `data/gold/exports/` directory. No database server or external storage is needed.

---

## Cost

Streamlit Community Cloud is **100% free** for public repositories. There are no usage limits on visitors or uptime for public apps. The only constraint is:
- 1GB memory limit per app
- Apps sleep after extended inactivity (wake on next visit)
- Repository must be public
