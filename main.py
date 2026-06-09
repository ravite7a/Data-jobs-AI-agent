#!/usr/bin/env python3
"""
Daily Data Jobs Pipeline
Scrapes 35 companies, filters roles, deduplicates, generates xlsx, emails report.
"""
import logging
from scraper import run as scrape
from report import generate_report
from emailer import send_email

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def main():
    log.info("=== Daily Job Scan Starting ===")

    # 1. Scrape & filter
    new_jobs = scrape()

    # 2. Generate report (even if 0 jobs — send "nothing new" email)
    if new_jobs:
        filepath = generate_report(new_jobs)
        log.info(f"Report saved: {filepath}")
    else:
        filepath = None
        log.info("No new jobs today — sending summary email with 0 count.")

    # 3. Email
    send_email(filepath, len(new_jobs))
    log.info("=== Done ===")


if __name__ == "__main__":
    main()
