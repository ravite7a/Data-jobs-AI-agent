# Target Companies — Career Pages

> Used by the daily job scraper to find Data Analyst, Analytics Engineer, Data Engineer, and related roles.
> ATS platform noted for each company to optimize scraping strategy.

| # | Company | Career Page URL | ATS Platform |
|---|---------|----------------|--------------|
| 1 | Meta | https://www.metacareers.com/jobs | Custom |
| 2 | Google | https://careers.google.com/jobs/results | Custom |
| 3 | Netflix | https://jobs.netflix.com/search | Custom |
| 4 | Apple | https://jobs.apple.com/en-us/search | Custom |
| 5 | Amazon | https://www.amazon.jobs/en/search | Custom |
| 6 | Microsoft | https://jobs.microsoft.com/us/en/search | Custom |
| 7 | Stripe | https://stripe.com/jobs/search | Greenhouse |
| 8 | Airbnb | https://job-boards.greenhouse.io/airbnb | Greenhouse |
| 9 | Reddit | https://job-boards.greenhouse.io/reddit | Greenhouse |
| 10 | Plaid | https://job-boards.greenhouse.io/plaid | Greenhouse |
| 11 | Upstart | https://job-boards.greenhouse.io/upstart | Greenhouse |
| 12 | NerdWallet | https://job-boards.greenhouse.io/nerdwallet | Greenhouse |
| 13 | DocuSign | https://job-boards.greenhouse.io/docusign | Greenhouse |
| 14 | Coinbase | https://www.coinbase.com/careers/positions | Greenhouse |
| 15 | Jane Street | https://www.janestreet.com/join-jane-street/open-roles | Custom |
| 16 | Two Sigma | https://careers.twosigma.com/careers/JobSearch | Custom |
| 17 | Snowflake | https://careers.snowflake.com/us/en/search-results | Workday |
| 18 | Datadog | https://job-boards.greenhouse.io/datadog | Greenhouse |
| 19 | Chime | https://job-boards.greenhouse.io/chime | Greenhouse |
| 20 | Spotify | https://jobs.lever.co/spotify | Lever |
| 21 | Salesforce | https://salesforce.wd12.myworkdayjobs.com/External_Career_Site | Workday |
| 22 | Zillow | https://job-boards.greenhouse.io/zillow | Greenhouse |
| 23 | Figma | https://job-boards.greenhouse.io/figma | Greenhouse |
| 24 | Acorns | https://job-boards.greenhouse.io/acorns | Greenhouse |
| 25 | Atlassian | https://www.atlassian.com/company/careers/all-jobs | Greenhouse |
| 26 | Bloomberg | https://careers.bloomberg.com/job/search | Custom |
| 27 | Dropbox | https://jobs.dropbox.com/all-jobs | Greenhouse |
| 28 | GitHub | https://job-boards.greenhouse.io/github | Greenhouse |
| 29 | Uber | https://www.uber.com/us/en/careers/list | Custom |
| 30 | Lyft | https://job-boards.greenhouse.io/lyft | Greenhouse |
| 31 | Robinhood | https://job-boards.greenhouse.io/robinhood | Greenhouse |
| 32 | Brex | https://job-boards.greenhouse.io/brex | Greenhouse |
| 33 | Affirm | https://job-boards.greenhouse.io/affirm | Greenhouse |
| 34 | Rippling | https://job-boards.greenhouse.io/rippling | Greenhouse |
| 35 | LinkedIn | https://careers.microsoft.com/us/en/search-results?keywords=linkedin | Custom |
| 36 | Palantir | https://job-boards.greenhouse.io/palantir | Greenhouse |
| 37 | Pinterest | https://job-boards.greenhouse.io/pinterest | Greenhouse |
| 38 | Citadel | https://www.citadel.com/careers/open-positions | Custom |
| 39 | DRW | https://drw.com/work-at-drw/listings | Custom |
| 40 | dbt Labs | https://job-boards.greenhouse.io/dbtlabsinc | Greenhouse |
| 41 | Fivetran | https://job-boards.greenhouse.io/fivetran | Greenhouse |
| 42 | DoorDash | https://job-boards.greenhouse.io/doordashusa | Greenhouse |
| 43 | Instacart | https://instacart.careers/current-openings | Greenhouse |
| 44 | Ramp | https://job-boards.greenhouse.io/ramp | Greenhouse |
| 45 | Notion | https://job-boards.greenhouse.io/notion | Greenhouse |

## Notes
- **Duplicates removed:** DocuSign and Zillow each appeared twice in the original list — kept once each.
- **Total unique companies:** 45
- **ATS breakdown:** Greenhouse (32), Custom (11), Workday (2), Lever (1)
- Greenhouse URLs use the public Job Board API (`job-boards.greenhouse.io/{token}`) — no auth needed.
- Custom ATS pages (Meta, Google, Netflix, Apple, Amazon, Microsoft, Jane Street, Two Sigma, Bloomberg) will use Claude Haiku for HTML extraction.

## Keywords to Match (Job Title Filter)
- Data Analyst
- Analytics Engineer
- Data Engineer
- Analytics Engineer
- Business Intelligence Engineer / BI Engineer
- Data Scientist (optional — remove if too broad)
- Machine Learning Engineer (optional)
