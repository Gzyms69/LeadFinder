import gspread
import pandas as pd
import sys
import os
from google.oauth2.service_account import Credentials

def upload_to_sheets(csv_file, credentials_file, spreadsheet_id):
    """
    Uploads a CSV file to a Google Spreadsheet.
    """
    if not os.path.exists(csv_file):
        print(f"Error: CSV file {csv_file} not found.")
        return

    # Define scope
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    try:
        # Authenticate
        creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        client = gspread.authorize(creds)

        # Open Spreadsheet
        sh = client.open_by_key(spreadsheet_id)
        worksheet = sh.get_worksheet(0) # Open the first sheet

        # Read CSV data
        df = pd.read_csv(csv_file)
        
        # Convert NaN to empty string (JSON doesn't support NaN)
        df = df.fillna('')

        # Check if sheet is empty to decide on headers
        current_data = worksheet.get_all_values()
        
        if not current_data:
            # Sheet is empty, write headers + data
            data_to_upload = [df.columns.values.tolist()] + df.values.tolist()
            worksheet.update(range_name='A1', values=data_to_upload)
            
            # Table Formatting: Freeze top row and make bold
            worksheet.freeze(rows=1)
            worksheet.format("A1:L1", {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}
            })
            # Enable filter for the header row (using request batch if needed, but simple is better)
            # Basic auto-filter on the first sheet
            worksheet.set_basic_filter()
            
            print(f"Initialized sheet with {len(df)} rows and table formatting.")
        else:
            # Sheet has data, append new rows
            worksheet.append_rows(df.values.tolist())
            print(f"Appended {len(df)} rows to existing sheet.")

    except Exception as e:
        print(f"Error uploading to Sheets: {e}")

if __name__ == "__main__":
    # Configuration
    CSV_FILE = 'processed_data/filtered_leads.csv'
    CREDS_FILE = 'config/service_account.json'
    SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'  # Use config/query.json for main execution

    # Allow command line overrides
    if len(sys.argv) > 1:
        CSV_FILE = sys.argv[1]

    upload_to_sheets(CSV_FILE, CREDS_FILE, SPREADSHEET_ID)
