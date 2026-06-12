import os
import json
import logging
from datetime import date
import gspread
from google.oauth2.service_account import Credentials

log = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

HEADERS = ["Date", "Job ID", "Company", "Title", "Location", "URL"]


def get_sheet():
    creds_json = os.environ["GOOGLE_CREDENTIALS"]
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet_id = os.environ["SHEET_ID"]
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


if __name__ == "__main__":
    sample = [
        {
            "job_id": "gh_airbnb_123456",
            "company": "Airbnb",
            "title": "Senior Data Engineer",
            "location": "San Francisco, CA",
            "url": "https://job-boards.greenhouse.io/airbnb/jobs/123456",
        },
        {
            "job_id": "gh_stripe_789",
            "company": "Stripe",
            "title": "Analytics Engineer II",
            "location": "Remote, USA",
            "url": "https://stripe.com/jobs/789",
        },
    ]
    append_jobs(sample)
    print("Done.")
