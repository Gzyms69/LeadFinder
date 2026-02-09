# LeadFinder: Google Maps Lead Generator

Automated tool to identify businesses with a digital gap on Google Maps and synchronize results directly to Google Sheets.

## Quick Start
1. Configure: Edit config/query.json with search terms and filters.
2. Activate: source venv/bin/activate
3. Run: python3 src/main.py or ./dev.sh start

## Features
- Automated Filtering: Excludes businesses that already possess a website.
- Newness Proxy: Filters by review count to identify recently established businesses.
- City Extraction: Automatically identifies the municipality for targeted outreach.
- Domain Availability Check: Automatically verifies if .pl and .com domains matching the business name are available for registration.
- Digital Score: Ranks leads based on their online presence. A score of 0 indicates a high-priority lead with no digital footprint.
- Consolidated Contact Profiles: Merges phone numbers, email addresses, and social media links into a single profile.
- Geolocation Search: Performs targeted searches within a specified radius of decimal coordinates.
- Table Synchronization: Appends data to Google Sheets with automated table formatting, frozen headers, and active filters.

## Configuration (config/query.json)
The application is controlled via a JSON configuration file.

- mode: "geo" for coordinate-based radius searches or "text" for standard keyword queries.
- lat, lon: Decimal coordinates for the geographic center of the search.
- radius: Search radius measured in meters.
- keywords: An array of terms to be searched within the specified parameters.
- depth: Controls the scroll depth of the search results. Higher values yield more results but increase execution time.
- email_scrape: Boolean value to enable crawling discovered websites for contact information.

## Strategy: Regional Lead Generation
Google Maps limits the number of results returned for a single query. Comprehensive data collection requires a granular approach.

1. Use Geo Mode: Define a central point and a significant radius to allow the tool to grid the region.
2. Target Administrative Divisions: Use specific voivodeships or counties in your keywords to circumvent result limits.
3. Iterative Filtering: Use the --skip-scrape flag to adjust filtering thresholds on existing datasets without re-executing the scraping phase.

## Technical Limitations and Safety
- Pagination Constraints: Google Maps typically caps results at 200-400 items per specific query.
- Anti-Automation Measures: To prevent IP restrictions, avoid high-frequency execution. For large-scale operations, consider integrating a proxy rotation service.
- Domain Check Latency: Verifying domain availability introduces a deliberate delay to comply with WHOIS server rate limits.
- Compliance: This software is intended for internal lead generation purposes. Use in accordance with local regulations and terms of service.

## Project Structure
- config/: Contains API credentials and search parameters.
- src/: Contains core Python logic and orchestration scripts.
- raw_data/: Archive of unprocessed scraper outputs.
- processed_data/: Filtered leads optimized for outreach.
