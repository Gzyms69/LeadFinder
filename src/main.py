import os
import subprocess
import sys
import argparse
import json
from filter_leads import filter_leads
from upload_to_sheets import upload_to_sheets

def load_config(config_path):
    """Loads configuration from JSON file."""
    if not os.path.exists(config_path):
        print(f"Warning: {config_path} not found. Using defaults.")
        return {}
    with open(config_path, "r") as f:
        return json.load(f)

def run_scrape(query, output_raw, lang="pl", depth=1):
    """Runs the Docker-based scraper."""
    # Write query to temporary file for the scraper
    query_file = "raw_data/queries.txt"
    with open(query_file, "w") as f:
        f.write(query + "\n")

    print(f"--- Starting Scrape for: {query} ---")
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}/raw_data:/data",
        "gosom/google-maps-scraper",
        "-input", "/data/queries.txt",
        "-results", f"/data/{os.path.basename(output_raw)}",
        "-lang", lang,
        "-depth", str(depth)
    ]
    try:
        subprocess.run(cmd, check=True)
        print("Scrape completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during scrape: {e}")
        sys.exit(1)

def main():
    # 0. Load JSON Config
    CONFIG_PATH = "config/query.json"
    conf = load_config(CONFIG_PATH)

    parser = argparse.ArgumentParser(description="LeadFinder: Google Maps Scraper & Filter")
    parser.add_argument("--query", default=conf.get("query"), help="Search query")
    parser.add_argument("--max-reviews", type=int, default=conf.get("max_reviews", 5), help="Max reviews")
    parser.add_argument("--skip-scrape", action="store_true", help="Skip scrape")
    
    args = parser.parse_args()

    if not args.query:
        print("Error: No query provided in config/query.json or via --query")
        sys.exit(1)

    # Paths
    RAW_CSV = "raw_data/last_run_raw.csv"
    FILTERED_CSV = "processed_data/filtered_leads.csv"
    CREDS = "config/service_account.json"
    SHEET_ID = "14oNkRSDRvLw_p0qKSnC_rXPLlsZTDYJCW9R-Vnro6cY"

    # 2. Scrape
    if not args.skip_scrape:
        run_scrape(args.query, RAW_CSV, lang=conf.get("language", "pl"), depth=conf.get("depth", 1))
    else:
        print("Skipping scrape as requested.")

    # 3. Filter
    print(f"--- Filtering Leads (Max Reviews: {args.max_reviews}) ---")
    filter_leads(RAW_CSV, FILTERED_CSV, args.max_reviews)

    # 4. Upload
    print("--- Uploading to Google Sheets ---")
    upload_to_sheets(FILTERED_CSV, CREDS, SHEET_ID)

    print("\n--- ALL DONE ---")
    print(f"Check your spreadsheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}")

if __name__ == "__main__":
    main()