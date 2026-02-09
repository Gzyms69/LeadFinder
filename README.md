# LeadFinder: Google Maps Lead Generator

Automated tool to identify businesses with a digital gap on Google Maps and synchronize results directly to Google Sheets with personalized demo links.

## Quick Start
1. Configure: Edit config/query.json with search terms and filters.
2. Activate: source venv/bin/activate
3. Run: python3 src/main.py or ./dev.sh start

## Features
- Automated Filtering: Excludes businesses that already possess a website.
- Newness Proxy: Filters by review count to identify recently established businesses.
- City Extraction: Automatically identifies the municipality for targeted outreach.
- Domain Availability Check: Verifies if .pl and .com domains matching the business name are available.
- Template Matching: Automatically categorizes businesses into industry-specific website templates using keyword analysis of search terms and business names.
- Magic Link Generation: Creates personalized URLs for prospective clients, allowing for instant generation of custom demo websites.
- Digital Score: Ranks leads based on their online presence (0-3 scale).
- Consolidated Contact Profiles: Merges phone numbers, email addresses, and social media links.
- Geolocation Search: Performs targeted searches within a specified radius of decimal coordinates.
- Table Synchronization: Appends data to Google Sheets with automated table formatting and active filters.

## Configuration (config/query.json)
- mode: "geo" for radius searches or "text" for direct queries.
- lat, lon: Decimal coordinates for the search center.
- radius: Search radius in meters.
- keywords: Array of search terms.
- depth: Result pagination depth.
- email_scrape: Enable/disable website contact crawling.

## Dynamic Sales Architecture Integration
The tool integrates with the Katalog Marketplace to generate personalized demo links.

### Matching Logic
The system prioritizes the search keyword to determine the industry category (e.g., searching for "mechanik" automatically assigns the "warsztat-pro" template). If the keyword is generic, it analyzes the business name against a comprehensive registry of Polish and English industry terms.

### Supported Templates
- warsztat-pro: Automotive services, detailing, and repair.
- bistro-modern: Restaurants, cafes, and gastronomy.
- helios-advise: Legal, financial, and consulting services.
- cyber-security: IT services, computer repair, and security.
- landing-aplikacji: Software and mobile applications.
- portfolio-osobista: Freelancers, artists, and personal brands.

## Spreadsheet Column Definitions
- Column A (Business Name): Name as listed on Google Maps.
- Column B (City): Identified municipality.
- Column C (Address): Physical location.
- Column D (Contact Profile): Consolidated phone, email, and social links.
- Column E (Domain .PL): Availability of matching .pl domain.
- Column F (Domain .COM): Availability of matching .com domain.
- Column G (Template Slug): Assigned industry template identifier.
- Column H (Magic Link): Personalized demo website URL.
- Column I (Digital Score): Online presence ranking.
- Column J (Reviews): Total user review count (Patched for accuracy).
- Column K (Rating): Average star rating.
- Column L (Maps URL): Direct link to the business profile.

## Project Structure
- config/: API credentials and search parameters.
- src/: Core Python logic and template matching engine.
- raw_data/: Archive of scraper outputs.
- processed_data/: Filtered leads ready for outreach.