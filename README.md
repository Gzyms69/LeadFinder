# LeadFinder: Google Maps Lead Generator

Automated tool to identify businesses with a digital gap on Google Maps and synchronize results directly to Google Sheets with personalized demo links.

## Technical Foundation
This tool utilizes a custom, patched fork of the **google-maps-scraper** engine:
[Gzyms69/google-maps-scraper](https://github.com/Gzyms69/google-maps-scraper).

### Why a Fork?
The original repository frequently fails to capture business reviews due to race conditions and changes in Google's asynchronous loading patterns. This fork includes critical patches to ensure data integrity:

- **Asynchronous Review Fix:** In the original repository, the scraper often "instantly assumed" a business had zero reviews if they didn't load within a millisecond window. This fork implements a sophisticated **waiting and retry logic** that monitors the DOM for changes and simulates user interaction (clicks/scrolling) to ensure reviews are fully materialized before extraction.
- **RPC-to-Browser Fallback:** Google's internal RPC API often blocks direct HTTP requests that lack browser-level session cookies. This fork utilizes Playwright's `page.Eval` to perform `fetch` requests from *within* the authenticated browser context, bypassing bot detection and enabling retrieval of 1000+ reviews per lead.
- **Robust Schema Parsing:** Resolves frequent "could not convert to string" errors by implementing a more resilient extraction of the `APP_INITIALIZATION_STATE`, ensuring core business details (phone, website, coordinates) are always captured even if the underlying HTML structure shifts.

## Prerequisites
- **Python 3.10+**
- **Docker** (Required for the scraper engine)
- **Google Cloud Account** (For Google Sheets API access)

## Quick Start
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Gzyms69/LeadFinder.git
   cd LeadFinder
   ```

2. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Configure the tool:**
   - Edit `config/query.json` and set your `spreadsheet_id`.
   - Place your Google Service Account JSON at `config/service_account.json`.

4. **Run the tool:**
   ```bash
   source venv/bin/activate
   python3 src/main.py
   ```

## Google Sheets Setup
1. Create a new Google Sheet.
2. Go to the [Google Cloud Console](https://console.cloud.google.com/).
3. Create a new project and enable the **Google Sheets API** and **Google Drive API**.
4. Create a **Service Account** under "IAM & Admin" > "Service Accounts".
5. Generate a new **JSON Key** for the service account and save it as `config/service_account.json` in this project.
6. **Important:** Copy the `client_email` from your JSON file and **share your Google Sheet** with that email (Editor permissions).
7. Copy the Spreadsheet ID from the URL (the part between `/d/` and `/edit`) and paste it into `config/query.json`.

## Features
- **Automated Filtering:** Excludes businesses that already possess a website.
- **Newness Proxy:** Filters by review count (e.g., <= 5) to identify recently established businesses.
- **City Extraction:** Automatically identifies the municipality for targeted outreach.
- **Domain Availability Check:** Verifies if `.pl` and `.com` domains matching the business name are available.
- **Template Matching:** Categorizes businesses into industry-specific templates using keyword analysis.
- **Magic Link Generation:** Creates personalized URLs for prospective clients using the Katalog Marketplace.
- **Digital Score:** Ranks leads based on their online presence (0-3 scale).
- **Consolidated Contact Profiles:** Merges phone numbers, emails, and social media links.
- **Geolocation Search:** Performs targeted searches within a specified radius of coordinates.
- **Table Synchronization:** Appends data to Google Sheets with automated formatting.

## Configuration (config/query.json)
- `mode`: "geo" for radius searches or "text" for direct queries.
- `lat`, `lon`: Decimal coordinates for the search center.
- `radius`: Search radius in meters (e.g., 5000 for 5km).
- `keywords`: Array of search terms (e.g., ["warsztat", "fryzjer"]).
- `max_reviews`: Threshold for the "newness" filter.
- `depth`: Result pagination depth (1 scroll ≈ 20-40 results).
- `email_scrape`: Enable/disable website contact crawling.
- `spreadsheet_id`: The ID of your target Google Sheet.

## Project Structure
- `config/`: Configuration templates and API credentials (ignored by git).
- `src/`: Core logic (Scraping, Filtering, Uploading).
- `raw_data/`: Direct outputs from the scraper.
- `processed_data/`: Cleaned and filtered CSVs.
- `setup.sh`: Automated environment setup script.

## Disclaimer
This tool is intended for personal lead generation and educational purposes. Ensure compliance with Google's Terms of Service and local data privacy regulations.
