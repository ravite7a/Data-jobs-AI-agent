# Data-jobs-AI-agent
An AI agent using Claude which sends me email everyday with new data related jobs.

An AI agent that monitors 35 top tech companies every morning and emails you a spreadsheet of new Data Analyst, Analytics Engineer, and Data Engineer job openings.
What it does
Every day at 7am ET, the agent wakes up, visits all 35 company career pages, extracts relevant job listings, filters out anything you've already seen, and sends you a clean Excel report straight to your inbox.
How to set it up

Fork this repo
Add these 4 secrets under Settings → Secrets → Actions:

ANTHROPIC_API_KEY
GMAIL_SENDER
GMAIL_RECIPIENT
GMAIL_APP_PASSWORD


Go to Actions → Daily Data Jobs Scan → Run workflow to test it

That's it.
Companies tracked
35 companies including Stripe, Airbnb, Coinbase, Snowflake, Datadog, Spotify, Figma, Robinhood, DoorDash, Ramp, Jane Street, Two Sigma, Bloomberg, and more.
Filters applied

USA-based or Remote-US roles only
Mid-level, Senior, and Staff titles only
No duplicates from previous days
