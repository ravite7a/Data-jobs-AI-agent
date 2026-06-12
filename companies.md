# Target Companies — Career Pages

> Used by the daily job scraper to find Data Analyst, Analytics Engineer, Data Engineer, and related roles.
> ATS platform noted for each company to optimize scraping strategy.

| # | Company | Career Page URL | ATS Platform |
|---|---------|----------------|--------------|
| 1 | Stripe | https://stripe.com/jobs/search | Greenhouse |
| 2 | Airbnb | https://job-boards.greenhouse.io/airbnb | Greenhouse |
| 3 | Reddit | https://job-boards.greenhouse.io/reddit | Greenhouse |
| 4 | Plaid | https://job-boards.greenhouse.io/plaid | Greenhouse |
| 5 | Upstart | https://job-boards.greenhouse.io/upstart | Greenhouse |
| 6 | NerdWallet | https://job-boards.greenhouse.io/nerdwallet | Greenhouse |
| 7 | DocuSign | https://job-boards.greenhouse.io/docusign | Greenhouse |
| 8 | Coinbase | https://job-boards.greenhouse.io/coinbase | Greenhouse |
| 9 | Jane Street | https://www.janestreet.com/join-jane-street/open-roles | Custom |
| 10 | Two Sigma | https://careers.twosigma.com/careers/JobSearch | Custom |
| 11 | Snowflake | https://careers.snowflake.com/us/en/search-results | Workday |
| 12 | Datadog | https://job-boards.greenhouse.io/datadog | Greenhouse |
| 13 | Chime | https://job-boards.greenhouse.io/chime | Greenhouse |
| 14 | Spotify | https://jobs.lever.co/spotify | Lever |
| 15 | Salesforce | https://salesforce.wd12.myworkdayjobs.com/External_Career_Site | Workday |
| 16 | Zillow | https://job-boards.greenhouse.io/zillow | Greenhouse |
| 17 | Figma | https://job-boards.greenhouse.io/figma | Greenhouse |
| 18 | Acorns | https://job-boards.greenhouse.io/acorns | Greenhouse |
| 19 | Atlassian | https://job-boards.greenhouse.io/atlassian | Greenhouse |
| 20 | Bloomberg | https://careers.bloomberg.com/job/search | Custom |
| 21 | Dropbox | https://job-boards.greenhouse.io/dropbox | Greenhouse |
| 22 | GitHub | https://job-boards.greenhouse.io/github | Greenhouse |
| 23 | Lyft | https://job-boards.greenhouse.io/lyft | Greenhouse |
| 24 | Robinhood | https://job-boards.greenhouse.io/robinhood | Greenhouse |
| 25 | Brex | https://job-boards.greenhouse.io/brex | Greenhouse |
| 26 | Affirm | https://job-boards.greenhouse.io/affirm | Greenhouse |
| 27 | Rippling | https://job-boards.greenhouse.io/rippling | Greenhouse |
| 28 | Palantir | https://job-boards.greenhouse.io/palantir | Greenhouse |
| 29 | Pinterest | https://job-boards.greenhouse.io/pinterest | Greenhouse |
| 30 | dbt Labs | https://job-boards.greenhouse.io/dbtlabsinc | Greenhouse |
| 31 | Fivetran | https://job-boards.greenhouse.io/fivetran | Greenhouse |
| 32 | DoorDash | https://job-boards.greenhouse.io/doordashusa | Greenhouse |
| 33 | Instacart | https://job-boards.greenhouse.io/instacart | Greenhouse |
| 34 | Ramp | https://job-boards.greenhouse.io/rampfinancial | Greenhouse |
| 35 | Notion | https://job-boards.greenhouse.io/notionhq | Greenhouse |

## Notes
- **Duplicates removed:** DocuSign and Zillow each appeared twice in the original list — kept once each.
- **Removed:** Meta, Google, Netflix, Apple, Amazon, Microsoft, Uber, LinkedIn, Citadel, DRW (custom ATS sites — too unreliable to scrape)
- **Total unique companies:** 35
- **ATS breakdown:** Greenhouse (30), Custom (3), Workday (2), Lever (1)
- Greenhouse URLs use the public Job Board API (`job-boards.greenhouse.io/{token}`) — no auth needed.
- Custom ATS pages (Jane Street, Two Sigma, Bloomberg) will use Claude Haiku for HTML extraction.

## Keywords to Match (Job Title Filter)
- Data Analyst
- Analytics Engineer
- Data Engineer
- Business Intelligence Engineer / BI Engineer
- Data Scientist
- Machine Learning Engineer
