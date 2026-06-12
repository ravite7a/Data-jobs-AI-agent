# Data Jobs Agent

An AI agent that monitors 35 top tech companies every morning and appends new Data Analyst, Analytics Engineer, and Data Engineer job openings directly to a Google Sheet.

## What it does

Every day at 7am ET, the agent scrapes all 35 company career pages, filters for relevant roles, deduplicates against previous days, and appends new jobs to your Google Sheet.

## Sheet columns

| Date | Job ID | Company | Title | Location | URL |
|------|--------|---------|-------|----------|-----|

## How to set it up

### 1. Fork this repo

### 2. Create a Google Sheet
- Go to sheets.google.com → create a blank sheet
- Copy the Sheet ID from the URL:
  `https://docs.google.com/spreadsheets/d/THIS_IS_YOUR_SHEET_ID/edit`

### 3. Set up a Google Service Account
1. Go to https://console.cloud.google.com
2. Create a new project (e.g. "data-jobs-agent")
3. Go to **APIs & Services → Enable APIs** → enable **Google Sheets API**
4. Go to **APIs & Services → Credentials → Create Credentials → Service Account**
5. Name it anything (e.g. "jobs-bot"), click Done
6. Click the service account → **Keys tab → Add Key → JSON**
7. Download the JSON file — keep it safe

### 4. Share your Google Sheet with the service account
- Open the downloaded JSON file
- Find the `client_email` field (looks like `jobs-bot@your-project.iam.gserviceaccount.com`)
- Open your Google Sheet → Share → paste that email → give it **Editor** access

### 5. Add GitHub Secrets
Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Value |
|-------------|-------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `GOOGLE_CREDENTIALS` | The entire contents of the JSON file downloaded in step 3 |
| `SHEET_ID` | The Sheet ID copied in step 2 |

For `GOOGLE_CREDENTIALS` — open the JSON file in a text editor, select all, copy, paste as the secret value.

### 6. Push to GitHub and test

First, replace the changed files in your repo. For each updated file (`main.py`, `sheets.py`, `requirements.txt`, `.github/workflows/daily_job_scan.yml`, `README.md`):
- Go to the file in your GitHub repo
- Click the pencil (edit) icon
- Paste the new contents
- Click **Commit changes**

Also delete `report.py` and `emailer.py` from your repo:
- Open the file → click the three-dot menu (⋯) → **Delete file** → Commit

Once all files are updated, test it immediately:
- Go to **Actions → Daily Data Jobs Scan → Run workflow → Run workflow**
- Watch the logs — if it succeeds, open your Google Sheet and you should see rows appearing

If you see a permissions error, double-check that you shared the Google Sheet with the service account email from the JSON file.

## Files

| File | Purpose |
|------|---------|
| `main.py` | Entrypoint |
| `scraper.py` | Scrapes 35 companies, filters, deduplicates |
| `sheets.py` | Appends new jobs to Google Sheet |
| `companies.md` | 35 company URLs and ATS types |
| `seen_jobs.csv` | Deduplication memory (grows daily) |
| `requirements.txt` | Python dependencies |
| `.github/workflows/daily_job_scan.yml` | GitHub Actions schedule |

## Cost

Essentially free — only cost is OpenAI API for 3 custom sites (~$0.01/day).
