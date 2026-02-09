import os
import subprocess
import sys
import argparse
import json
import glob
from filter_leads import filter_leads
from upload_to_sheets import upload_to_sheets

def load_config(config_path):
    """Loads configuration from JSON file."""
    if not os.path.exists(config_path):
        print(f"Warning: {config_path} not found. Using defaults.")
        return {}
    with open(config_path, "r") as f:
        return json.load(f)

def run_scrape_geo(keyword, lat, lon, radius, output_raw, lang="pl", depth=1, email=False):
    """Runs the Docker-based scraper in GEO mode."""
    
    # In geo mode, the scraper takes the query as the keyword (e.g., "dentist") 
    # and restricts it to the geo-fence.
    
    # We write the single keyword to the input file
    query_file = "raw_data/queries.txt"
    with open(query_file, "w") as f:
        f.write(keyword + "\n")

    geo_string = f"{lat},{lon}"
    
    print(f"--- Starting GEO Scrape for: '{keyword}' around {geo_string} (r={radius}m) ---")
    
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}/raw_data:/data",
        "ghcr.io/gzyms69/google-maps-scraper:latest",
        "-input", "/data/queries.txt",
        "-results", f"/data/{os.path.basename(output_raw)}",
        "-lang", lang,
        "-geo", geo_string,
        "-radius", str(radius),
        "-depth", str(depth)
    ]
    
    if email:
        cmd.append("-email")

    try:
        subprocess.run(cmd, check=True)
        print("Scrape completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during scrape: {e}")
        # We don't exit here so other keywords can proceed
        pass

def main():
    # 0. Load JSON Config
    CONFIG_PATH = "config/query.json"
    conf = load_config(CONFIG_PATH)

    parser = argparse.ArgumentParser(description="LeadFinder: Google Maps Scraper & Filter")
    parser.add_argument("--skip-scrape", action="store_true", help="Skip scrape")
    
    args = parser.parse_args()

    # Settings
    RAW_DIR = "raw_data"
    FILTERED_CSV = "processed_data/filtered_leads.csv"
    CREDS = "config/service_account.json"
    SHEET_ID = "14oNkRSDRvLw_p0qKSnC_rXPLlsZTDYJCW9R-Vnro6cY"
    
    # 1. Scrape Logic
    if not args.skip_scrape:
        # Clear old raw data to avoid mixing searches
        for f in glob.glob(f"{RAW_DIR}/raw_*.csv"):
            os.remove(f)

        keywords = conf.get("keywords", [])
        if not keywords and conf.get("query"):
             # Fallback to single query if keywords missing
             keywords = [conf.get("query")]

        for i, kw in enumerate(keywords):
            # Create unique filename for each keyword run
            output_file = f"{RAW_DIR}/raw_{i}_{kw.replace(' ', '_')}.csv"
            
            run_scrape_geo(
                keyword=kw,
                lat=conf.get("lat"),
                lon=conf.get("lon"),
                radius=conf.get("radius", 5000),
                output_raw=output_file,
                lang=conf.get("language", "pl"),
                depth=conf.get("depth", 1),
                email=conf.get("email_scrape", False)
            )

            # Tag the raw data with the keyword that found it
            if os.path.exists(output_file):
                try:
                    df_raw = pd.read_csv(output_file)
                    df_raw['search_keyword'] = kw
                    df_raw.to_csv(output_file, index=False)
                except Exception as e:
                    print(f"Warning: Could not tag {output_file} with keyword: {e}")

    # 2. Merge Raw Data
    # Since we ran multiple scrapes (one per keyword), we need to merge them for filtering
    all_files = glob.glob(f"{RAW_DIR}/raw_*.csv")
    if not all_files:
        print("No raw data found to process.")
        sys.exit(1)
        
    print(f"--- Merging {len(all_files)} raw data files ---")
    
    # 3. Filter
    print(f"--- Filtering Leads (Max Reviews: {conf.get('max_reviews', 5)}) ---")
    filter_leads(all_files, FILTERED_CSV, conf.get('max_reviews', 5))

    # 4. Upload
    print("--- Uploading to Google Sheets ---")
    upload_to_sheets(FILTERED_CSV, CREDS, SHEET_ID)

    print("\n--- ALL DONE ---")
    print(f"Check your spreadsheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}")

if __name__ == "__main__":
    main()