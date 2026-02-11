# Gemini Project Context: LeadFinder

## 1. Project Vision & Core Objective
Automated Google Maps lead generation tool focusing on "New & Website-less" businesses.

- **GitHub Repository:** https://github.com/Gzyms69/LeadFinder
- **Target Spreadsheet:** [Configured in config/query.json]

### Primary Filters
- **No Website:** `website` field is null or empty.
- **Newness Proxy:** `review_count` is below a user-defined threshold (default <= 5).

## 2. Technical Stack
- **Scraper Engine:** `gosom/google-maps-scraper` (Docker-based).
- **Processing:** Python 3.x with `pandas` for filtering/sorting.
- **Integration:** `gspread` for Google Sheets API.
- **Environment:** Docker, Git.

## 3. Project Structure (Proposed)
- `src/`: Python source code for filtering and uploading.
- `config/`: Credentials (service account JSON) and settings.
- `raw_data/`: Direct outputs from the scraper.
- `processed_data/`: Cleaned CSVs ready for upload.
- `docs/`: Supplemental documentation.

## 4. Current State
- [x] Project directory initialized.
- [x] Git repository initialized.
- [x] Scraper Integration (Docker + Poland localization).
- [x] Filtering Logic (No Website + Max Reviews + City extraction).
- [x] Google Sheets Integration (Table formatting + Auto-filters).
- [x] JSON-driven Configuration.

## 5. Usage
1. Edit `config/query.json` to set your search term and filters.
2. Run the tool:
   ```bash
   python3 src/main.py
   ```
3. (Optional) Override with CLI:
   ```bash
   python3 src/main.py --query "nowa kawiarnia Warszawa" --max-reviews 5
   ```

## 6. Known Issues & Risks
- **Scraper Dependency:** Relies on `gosom/google-maps-scraper` maintained status.
- **Rate Limiting:** Google Maps anti-bot measures require cautious usage.
- **Data Privacy:** Tool is intended for low-volume, personal lead generation.
