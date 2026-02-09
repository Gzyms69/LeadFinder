# LeadFinder: Google Maps Lead Generator 🇵🇱

Automated tool to find "Digital Gap" leads (new businesses with no website) on Google Maps and sync them directly to Google Sheets.

## 🚀 Quick Start
1. **Configure:** Edit `config/query.json` with your search term and filters.
2. **Activate:** `source venv/bin/activate`
3. **Run:** `python3 src/main.py` (or use `./dev.sh start`)

## 🛠 Features
- **Filter:** Automatically removes businesses that already have a website.
- **Newness Proxy:** Filters by review count (e.g., <= 5) to find fresh businesses.
- **City Extraction:** Identifies the city/town for targeted outreach.
- **Digital Score (0-3):** Ranks leads by their online presence. `0` = Ghost (No phone/web/socials).
- **Consolidated Contacts:** Merges Phone, Email, and Social Media links into a single profile.
- **Geo-Grid Search:** Searches within a specific radius (e.g., 50km around Kielce) to find rural leads.
- **Auto-Sync:** Appends data to Google Sheets with frozen headers and filters.

## ⚙️ Configuration (`config/query.json`)
The tool is driven by a JSON config file.

- **`mode`**: `"geo"` (Lat/Lon radius) or `"text"` (Standard keywords).
- **`lat`, `lon`**: Decimal coordinates for the search center.
- **`radius`**: Radius in METERS (e.g., `50000` = 50km).
- **`keywords`**: List of terms to search for (e.g., `["warsztat", "fryzjer"]`).
- **`depth`**: How deep to scroll (1 = ~20 results, 2 = ~40-60 results).
- **`email_scrape`**: `true` to visit sites and find emails (useful for partial leads).

## 📈 Pro-Strategy: Finding "Hidden" Leads in the Countryside
Google Maps limits the number of results for a single search. Searching for "Warsztat Polska" will only give you a fraction of the total businesses.

### To find every lead in small towns and villages:
1. **Use Geo Mode:** Set a central point (like Kielce) and a large radius (50km). The tool will grid the area.
2. **Target Voivodeships (Województwa):**
   - `warsztat samochodowy mazowieckie`
   - `warsztat samochodowy podlaskie`
3. **Target Powiaty:** This is the most effective way to find countryside leads.
4. **The "Skip Scrape" Feature:** If you have already scraped data but want to change your review threshold (e.g., from 5 to 10), run:
   ```bash
   python3 src/main.py --skip-scrape --max-reviews 10
   ```

## ⚠️ Limits & Safety
- **Pagination:** Google Maps typically shows ~200-400 results per query maximum.
- **Anti-Bot:** To avoid IP blocks, do not run hundreds of queries per hour. For massive bulk scraping, consider using a Proxy (configured in the scraper flags).
- **Terms of Service:** This tool is for personal/internal lead generation. Use responsibly.

## 📂 Project Structure
- `config/`: Credentials (`service_account.json`) and search settings (`query.json`).
- `src/`: Core Python logic.
- `raw_data/`: Archive of raw scraper results.
- `processed_data/`: Filtered leads ready for upload.