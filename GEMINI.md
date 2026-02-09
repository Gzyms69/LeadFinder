# Gemini Project Context: LeadFinder

## 1. Project Vision & Core Objective
Automated Google Maps lead generation tool focusing on "New & Website-less" businesses.

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

## 4. Current State (PHASE 0)
- [x] Project directory initialized.
- [x] Git repository initialized.
- [->] Scaffolding documentation files.

## 5. Known Issues & Risks
- **Scraper Dependency:** Relies on `gosom/google-maps-scraper` maintained status.
- **Rate Limiting:** Google Maps anti-bot measures require cautious usage.
- **Data Privacy:** Tool is intended for low-volume, personal lead generation.
