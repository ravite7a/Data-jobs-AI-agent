import os
import csv
import json
import time
import logging
import re
import requests
from datetime import date
from pathlib import Path
from openai import OpenAI

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
COMPANIES_FILE = "companies.md"
SEEN_JOBS_FILE = "seen_jobs.csv"
OUTPUT_DIR = "output"

TITLE_KEYWORDS = [
    "data analyst", "analytics engineer", "data engineer",
    "bi engineer", "business intelligence engineer",
    "data scientist", "analytics engineer",
]

INCLUDE_LEVELS = ["mid", "senior", "sr.", "sr ", "staff", "ii", "level 2", "l2", "2"]
EXCLUDE_LEVELS = [
    "junior", "jr.", "associate", "entry", "intern", "new grad",
    "principal", "director", "manager", "head of", "vp ", "vice president",
    "lead ", "iii", "level 3", "l3", "iv", "level 4",
]

def _get_client():
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ── Helpers ───────────────────────────────────────────────────────────────────
def load_companies():
    """Parse companies.md and return list of (name, url, ats) tuples."""
    companies = []
    with open(COMPANIES_FILE) as f:
        for line in f:
            m = re.match(r"\|\s*\d+\s*\|\s*(.+?)\s*\|\s*(https?://\S+?)\s*\|\s*(\w[\w\s]*?)\s*\|", line)
            if m:
                companies.append((m.group(1).strip(), m.group(2).strip(), m.group(3).strip()))
    return companies


def load_seen_jobs():
    """Return set of seen job IDs."""
    seen = set()
    if Path(SEEN_JOBS_FILE).exists():
        with open(SEEN_JOBS_FILE) as f:
            for row in csv.DictReader(f):
                seen.add(row["job_id"])
    return seen


def save_seen_jobs(new_jobs, seen):
    """Append new jobs to seen_jobs.csv."""
    file_exists = Path(SEEN_JOBS_FILE).exists()
    with open(SEEN_JOBS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["job_id", "company", "title", "date_seen"])
        if not file_exists:
            writer.writeheader()
        for job in new_jobs:
            if job["job_id"] not in seen:
                writer.writerow({
                    "job_id": job["job_id"],
                    "company": job["company"],
                    "title": job["title"],
                    "date_seen": str(date.today()),
                })


def is_relevant_title(title: str) -> bool:
    """Return True if the job title matches keywords and seniority rules."""
    t = title.lower()

    # Must contain at least one data-related keyword
    if not any(kw in t for kw in TITLE_KEYWORDS):
        return False

    # Exclude unwanted levels
    if any(ex in t for ex in EXCLUDE_LEVELS):
        return False

    # If a level keyword is present, it must be an included level
    level_found = any(inc in t for inc in INCLUDE_LEVELS)
    explicit_level = any(
        kw in t for kw in INCLUDE_LEVELS + EXCLUDE_LEVELS +
        ["engineer i ", "analyst i ", " i ", "level 1", "l1"]
    )
    if explicit_level and not level_found:
        return False

    return True


def is_usa_location(location: str) -> bool:
    """Rough check: accept US states, Remote, USA mentions; reject foreign."""
    if not location:
        return True  # unknown — include and let user filter
    loc = location.lower()
    foreign = ["canada", "uk", "united kingdom", "london", "india", "bangalore",
               "germany", "france", "australia", "singapore", "ireland", "amsterdam"]
    if any(f in loc for f in foreign):
        return False
    usa_hints = [
        "remote", "usa", "united states", "u.s.", ", ca", ", ny", ", wa",
        ", tx", ", il", ", ma", ", co", ", ga", ", fl", ", nc", ", va",
        "san francisco", "new york", "seattle", "chicago", "austin",
        "boston", "denver", "atlanta", "los angeles", "menlo park",
    ]
    return any(h in loc for h in usa_hints) or True  # default include if ambiguous


# ── Scrapers ──────────────────────────────────────────────────────────────────
def scrape_greenhouse(company_name: str, url: str) -> list[dict]:
    """Hit the Greenhouse public API directly."""
    # Extract board token from URL
    m = re.search(r"greenhouse\.io/([^/?\s]+)", url)
    if not m:
        log.warning(f"Could not parse Greenhouse token from {url}")
        return []
    token = m.group(1)
    api_url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"

    try:
        resp = requests.get(api_url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        log.error(f"Greenhouse API error for {company_name}: {e}")
        return []

    jobs = []
    for job in data.get("jobs", []):
        title = job.get("title", "")
        location = job.get("location", {}).get("name", "")
        job_id = str(job.get("id", ""))
        job_url = job.get("absolute_url", "")
        dept = job.get("departments", [{}])[0].get("name", "") if job.get("departments") else ""

        if not is_relevant_title(title):
            continue
        if not is_usa_location(location):
            continue

        jobs.append({
            "job_id": f"gh_{token}_{job_id}",
            "company": company_name,
            "title": title,
            "location": location,
            "department": dept,
            "url": job_url,
            "date_found": str(date.today()),
        })
    return jobs


def scrape_lever(company_name: str, url: str) -> list[dict]:
    """Hit the Lever postings API."""
    m = re.search(r"lever\.co/([^/?\s]+)", url)
    if not m:
        return []
    token = m.group(1)
    api_url = f"https://api.lever.co/v0/postings/{token}?mode=json"

    try:
        resp = requests.get(api_url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        log.error(f"Lever API error for {company_name}: {e}")
        return []

    jobs = []
    for job in data:
        title = job.get("text", "")
        location = job.get("categories", {}).get("location", "")
        job_id = job.get("id", "")
        job_url = job.get("hostedUrl", "")
        dept = job.get("categories", {}).get("team", "")

        if not is_relevant_title(title):
            continue
        if not is_usa_location(location):
            continue

        jobs.append({
            "job_id": f"lv_{token}_{job_id}",
            "company": company_name,
            "title": title,
            "location": location,
            "department": dept,
            "url": job_url,
            "date_found": str(date.today()),
        })
    return jobs


def scrape_workday(company_name: str, url: str) -> list[dict]:
    """Scrape Workday via their search API (best-effort)."""
    try:
        # Derive base API URL from careers page
        base = re.sub(r"/search-results.*", "", url)
        api_url = base + "/fs/searchJob?limit=50&offset=0&searchText=data+engineer+OR+data+analyst+OR+analytics+engineer"
        headers = {"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
        resp = requests.get(api_url, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        log.error(f"Workday error for {company_name}: {e}")
        return []

    jobs = []
    for job in data.get("jobPostings", []):
        title = job.get("title", "")
        location = job.get("locationsText", "")
        job_id = job.get("bulletFields", [""])[0] if job.get("bulletFields") else job.get("externalPath", "")
        job_url = url.split("/fs/")[0] + job.get("externalPath", "")

        if not is_relevant_title(title):
            continue
        if not is_usa_location(location):
            continue

        jobs.append({
            "job_id": f"wd_{company_name.lower().replace(' ', '_')}_{job_id}",
            "company": company_name,
            "title": title,
            "location": location,
            "department": "",
            "url": job_url,
            "date_found": str(date.today()),
        })
    return jobs


def scrape_custom_claude(company_name: str, url: str) -> list[dict]:
    """Use Claude Haiku to extract jobs from custom career pages."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        html = resp.text[:40000]  # limit tokens
    except Exception as e:
        log.error(f"Fetch error for {company_name} ({url}): {e}")
        return []

    prompt = f"""Extract all job postings from this career page HTML for {company_name}.
Return ONLY a JSON array. Each object must have:
- title (string)
- location (string, empty string if not found)  
- url (string, full URL if available, else empty string)
- job_id (string, any unique identifier found, else empty string)

Only include roles related to: data analyst, analytics engineer, data engineer, BI engineer, data scientist.
Only include roles based in the USA or Remote.
Only include mid-level, senior, or staff roles (no junior, intern, principal, director, VP, manager).
Include roles with no explicit level.

HTML:
{html}

Return ONLY the JSON array, no other text."""

    try:
        response = _get_client().chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.choices[0].message.content.strip()
        raw = re.sub(r"^```json|^```|```$", "", raw, flags=re.MULTILINE).strip()
        listings = json.loads(raw)
    except Exception as e:
        log.error(f"OpenAI extraction error for {company_name}: {e}")
        return []

    jobs = []
    for i, job in enumerate(listings):
        title = job.get("title", "")
        if not is_relevant_title(title):
            continue
        uid = job.get("job_id") or f"{i}"
        jobs.append({
            "job_id": f"custom_{company_name.lower().replace(' ', '_')}_{uid}",
            "company": company_name,
            "title": title,
            "location": job.get("location", ""),
            "department": "",
            "url": job.get("url", url),
            "date_found": str(date.today()),
        })
    return jobs


# ── Main ──────────────────────────────────────────────────────────────────────
def run():
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    companies = load_companies()
    seen = load_seen_jobs()

    all_new_jobs = []

    for name, url, ats in companies:
        log.info(f"Scraping {name} ({ats})...")
        try:
            if ats.lower() == "greenhouse":
                jobs = scrape_greenhouse(name, url)
            elif ats.lower() == "lever":
                jobs = scrape_lever(name, url)
            elif ats.lower() == "workday":
                jobs = scrape_workday(name, url)
            else:
                jobs = scrape_custom_claude(name, url)
        except Exception as e:
            log.error(f"Failed {name}: {e}")
            jobs = []

        new = [j for j in jobs if j["job_id"] not in seen]
        log.info(f"  {name}: {len(jobs)} matched, {len(new)} new")
        all_new_jobs.extend(new)
        time.sleep(0.5)  # polite delay

    if not all_new_jobs:
        log.info("No new jobs found today.")
        return []

    save_seen_jobs(all_new_jobs, seen)
    log.info(f"Total new jobs: {len(all_new_jobs)}")
    return all_new_jobs


if __name__ == "__main__":
    run()
