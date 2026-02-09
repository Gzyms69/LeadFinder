# LeadFinder: Google Maps Lead Generator 🇵🇱

Automated tool to find "Digital Gap" leads (new businesses with no website) on Google Maps and sync them directly to Google Sheets.

## 🚀 Quick Start
1. **Configure:** Edit `config/query.json` with your search term and filters.
2. **Activate:** `source venv/bin/activate`
3. **Run:** `python3 src/main.py`

## 🛠 Features
- **Filter:** Automatically removes businesses that already have a website.
- **Newness Proxy:** Filters by review count (e.g., <= 5) to find fresh businesses.
- **City Extraction:** Identifies the city/town for targeted outreach.
- **Auto-Sync:** Appends data to Google Sheets with frozen headers and filters.

## 📈 Pro-Strategy: Finding "Hidden" Leads in the Countryside
Google Maps limits the number of results for a single search. Searching for "Warsztat Polska" will only give you a fraction of the total businesses.

### To find every lead in small towns and villages:
1. **Use Specific Regions:** Instead of one query, use a list of queries in `config/query.json` or run the tool multiple times.
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
- `config/`: Credentials and search settings.
- `src/`: Core Python logic.
- `raw_data/`: Archive of raw scraper results.
- `processed_data/`: Filtered leads ready for upload.
