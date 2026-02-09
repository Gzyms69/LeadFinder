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
        data = json.loads(address_json.replace("''", "'"))
        return data.get('city', '')
    except:
        return ""

def calculate_digital_score(row):
    """
    Calculates a 'Digital Presence Score' (0-3).
    0 = Ghost (No phone, no web, no social)
    1 = Minimal (Phone only)
    2 = Partial (Socials but no Web)
    3 = Established (Website)
    """
    score = 0
    if row.get('Phone') and str(row.get('Phone')).strip():
        score += 1
    # Check for social media presence (if columns exist)
    socials = ['facebook', 'instagram', 'linkedin', 'twitter']
    has_social = False
    for s in socials:
        if s in row and pd.notna(row[s]) and str(row[s]).strip():
            has_social = True
            break
    if has_social:
        score += 1
    
    if row.get('website') and pd.notna(row['website']) and str(row['website']).strip():
        score += 1
        
    return score

def build_contact_profile(row):
    """
    Consolidates all contact info into a single readable string.
    """
    parts = []
    if row.get('Phone') and pd.notna(row['Phone']):
        parts.append(f"📞 {row['Phone']}")
    
    if row.get('emails') and pd.notna(row['emails']):
        parts.append(f"📧 {row['emails']}")

    socials = ['facebook', 'instagram', 'linkedin']
    for s in socials:
        if s in row and pd.notna(row[s]) and str(row[s]).strip():
            parts.append(f"🔗 {s.title()}: {row[s]}")
            
    return " | ".join(parts)

def filter_leads(input_files, output_file, max_reviews=5):
    """
    Filters leads from multiple CSVs.
    """
    if isinstance(input_files, str):
        input_files = [input_files]

    dfs = []
    for f in input_files:
        try:
            dfs.append(pd.read_csv(f))
        except Exception as e:
            print(f"Error reading {f}: {e}")

    if not dfs:
        print("No data loaded.")
        return

    df = pd.concat(dfs, ignore_index=True)
    
    # 0. Clean & Standardize
    # Check for 'status' column to filter closed businesses
    if 'status' in df.columns:
        # We only want to REMOVE permanently closed businesses.
        # We KEEP Operational, Temporarily Closed, and NaN (unknown).
        df = df[~df['status'].astype(str).str.lower().isin(['permanently_closed', 'permanently closed'])]

    # 1. Filter: No Website (NaN or empty string)
    leads = df[df['website'].isna() | (df['website'].str.strip() == '')].copy()

    # 2. Filter: Review count <= threshold
    leads['review_count'] = pd.to_numeric(leads['review_count'], errors='coerce').fillna(0)
    leads = leads[leads['review_count'] <= max_reviews]

    # 3. Enrich Data
    leads['City'] = leads['complete_address'].apply(extract_city)
    leads['Phone'] = leads['phone'] # Rename for helper function
    
    # Ensure social columns exist even if scraper didn't find any
    for col in ['facebook', 'instagram', 'linkedin', 'emails']:
        if col not in leads.columns:
            leads[col] = None

    leads['Digital Score'] = leads.apply(calculate_digital_score, axis=1)
    leads['Contact Profile'] = leads.apply(build_contact_profile, axis=1)

    # 4. Sort: By Digital Score (Ghosts first), then Reviews (Newest first)
    leads = leads.sort_values(by=['Digital Score', 'review_count'], ascending=[True, True])

    # 5. Cleanup
    columns_to_keep = {
        'title': 'Business Name',
        'City': 'City',
        'address': 'Address',
        'Contact Profile': 'Contact Profile',
        'Digital Score': 'Digital Score',
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
    # Test mode
    if len(sys.argv) > 1:
        filter_leads([sys.argv[1]], 'processed_data/test_filtered.csv')
