import pandas as pd
import os
import sys
import json

def extract_city(address_json):
    """
    Safely extracts city from the complete_address JSON string.
    """
    try:
        if pd.isna(address_json) or not address_json:
            return ""
        # The scraper sometimes returns a string that looks like JSON
        data = json.loads(address_json.replace("''", "'"))
        return data.get('city', '')
    except:
        return ""

def filter_leads(input_file, output_file, max_reviews=5):
    """
    Filters Google Maps leads for those without websites and low review counts.
    """
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    # Load the data
    try:
        df = pd.read_csv(input_file)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # 1. Filter: No Website (NaN or empty string)
    leads = df[df['website'].isna() | (df['website'].str.strip() == '')].copy()

    # 2. Filter: Review count <= threshold
    leads['review_count'] = pd.to_numeric(leads['review_count'], errors='coerce').fillna(0)
    leads = leads[leads['review_count'] <= max_reviews]

    # 3. Extra: Extract City from complete_address
    leads['City'] = leads['complete_address'].apply(extract_city)

    # 4. Sort: By review count ascending
    leads = leads.sort_values(by='review_count', ascending=True)

    # 5. Cleanup: Select and rename columns for clarity
    columns_to_keep = {
        'title': 'Business Name',
        'City': 'City',
        'address': 'Address',
        'phone': 'Phone',
        'review_count': 'Reviews',
        'review_rating': 'Rating',
        'link': 'Maps URL'
    }
    
    existing_cols = [col for col in columns_to_keep.keys() if col in leads.columns]
    final_leads = leads[existing_cols].rename(columns=columns_to_keep)

    # Save to processed_data
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    final_leads.to_csv(output_file, index=False)
    
    print(f"Filtering complete. {len(final_leads)} leads found.")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    # Default values
    INPUT = 'raw_data/test_poland.csv'
    OUTPUT = 'processed_data/filtered_leads.csv'
    THRESHOLD = 5
    
    # Allow command line overrides
    if len(sys.argv) > 1:
        INPUT = sys.argv[1]
    if len(sys.argv) > 2:
        THRESHOLD = int(sys.argv[2])
    
    filter_leads(INPUT, OUTPUT, THRESHOLD)
