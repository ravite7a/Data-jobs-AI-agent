import os
import smtplib
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path


def send_email(filepath: str, job_count: int):
    """Send the daily jobs report as an email attachment."""
    sender = os.environ["GMAIL_SENDER"]
    recipient = os.environ["GMAIL_RECIPIENT"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    today = str(date.today())

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = f"📊 Daily Data Roles Report — {today} ({job_count} new jobs)"

    body = f"""Hi,

Your daily data roles digest is ready for {today}.

🆕 New listings found: {job_count}
📋 Companies tracked: 35
🎯 Roles: Data Analyst · Analytics Engineer · Data Engineer · BI Engineer · Data Scientist

The spreadsheet is attached — it includes company, title, department, location, and a direct apply link for each role.

Filters applied:
  ✅ USA-based or Remote-US only
  ✅ Mid-level, Senior, and Staff roles
  ✅ 0 duplicates from previous days

—
Automated Job Tracker
"""

    msg.attach(MIMEText(body, "plain"))

    # Attach the xlsx
    if filepath and Path(filepath).exists():
        with open(filepath, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={Path(filepath).name}",
        )
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"Email sent to {recipient} with {job_count} jobs.")
