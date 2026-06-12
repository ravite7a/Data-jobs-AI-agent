#!/usr/bin/env python3
"""
Daily Data Jobs Pipeline
Scrapes 35 companies, filters roles, deduplicates, appends to Google Sheet.
"""
import logging
from scraper import run as scrape
from sheets import append_jobs

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def main():
    log.info("=== Daily Job Scan Starting ===")

    # 1. Scrape & filter
    new_jobs = scrape()

    # 2. Append to Google Sheet
    if new_jobs:
        append_jobs(new_jobs)
        log.info(f"Done — {len(new_jobs)} new jobs added to sheet.")
    else:
        log.info("No new jobs found today.")

    log.info("=== Done ===")


if __name__ == "__main__":
    main()
