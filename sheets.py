import os
import json
import base64
import logging
from datetime import date
import gspread
from google.oauth2.service_account import Credentials

log = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
HEADERS = ["Date", "Job ID", "Company", "Title", "Location", "URL"]


def get_sheet():
    raw = os.environ.get("GOOGLE_CREDENTIALS", "").strip()
    if not raw:
        raise ValueError("GOOGLE_CREDENTIALS secret is missing or empty.")

    # Try base64 decode first, fall back to raw JSON
    try:
        decoded = base64.b64decode(raw).decode("utf-8")
        creds_dict = json.loads(decoded)
    except Exception:
        try:
            creds_dict = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"GOOGLE_CREDENTIALS could not be parsed: {e}")

    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)

    sheet_id = os.environ.get("SHEET_ID", "").strip()
    if not sheet_id:
        raise ValueError("SHEET_ID secret is missing or empty.")

    return client.open_by_key(sheet_id).sheet1


def ensure_headers(sheet):
    first_row = sheet.row_values(1)
    if first_row != HEADERS:
        sheet.insert_row(HEADERS, index=1)
        log.info("Headers written to sheet.")


def append_jobs(jobs: list[dict]):
    if not jobs:
        log.info("No new jobs to append to sheet.")
        return

    sheet = get_sheet()
    ensure_headers(sheet)

    today = str(date.today())
    rows = []
    for job in jobs:
        url = job.get("url", "")
        rows.append([
            today,
            job.get("job_id", ""),
            job.get("company", ""),
            job.get("title", ""),
            job.get("location", ""),
            f'=HYPERLINK("{url}", "Apply")' if url else "",
        ])

    sheet.append_rows(rows, value_input_option="USER_ENTERED")
    log.info(f"Appended {len(rows)} rows to Google Sheet.")