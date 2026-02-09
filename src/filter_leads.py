import pandas as pd
import os
import sys
import json
import whois
import time
import re
# Add src to path so we can import template_matcher
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from template_matcher import get_best_template

def clean_name_for_domain(name):
    """
    Cleans business name for domain checking:
    - Lowers case
    - Converts Polish characters to ASCII
    - Removes all non-alphanumeric characters
    """
    if not name or pd.isna(name):
        return ""
    
    # Lowercase
    name = name.lower()
    
    # Polish character mapping
    replacements = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
        'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z'
    }
    for char, replacement in replacements.items():
        name = name.replace(char, replacement)
    
    # Remove everything except a-z and 0-9
    name = re.sub(r'[^a-z0-9]', '', name)
    return name

def check_domain_availability(domain):
    """
    Checks if a domain is available using WHOIS.
    Returns 'Available', 'Registered', or 'Error'.
    """
    if not domain:
        return "N/A"
    try:
        # Some WHOIS servers are very sensitive. 
        # We add a small sleep before each check in the main loop if needed.
        w = whois.whois(domain)
        # If domain has no expiration date or registrar, it might be available
        if not w.domain_name:
            return "Available"
        return "Registered"
    except Exception as e:
        # python-whois raises an exception if domain is not found (which means it's available)
        if "No match for" in str(e) or "NOT FOUND" in str(e) or "No found" in str(e):
            return "Available"
        return "Check Manually"

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
    # Check for social media presence
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
    Filters leads from multiple CSVs and checks domain availability.
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
    
    # 0. Filter Status
    if 'status' in df.columns:
        df = df[~df['status'].astype(str).str.lower().isin(['permanently_closed', 'permanently closed'])]

    # 1. Filter: No Website
    leads = df[df['website'].isna() | (df['website'].str.strip() == '')].copy()

    # 2. Filter: Review count
    leads['review_count'] = pd.to_numeric(leads['review_count'], errors='coerce').fillna(0)
    leads = leads[leads['review_count'] <= max_reviews]

    if leads.empty:
        print("No leads found matching criteria.")
        return

    # 3. Enrich Data
    leads['City'] = leads['complete_address'].apply(extract_city)
    leads['Phone'] = leads['phone']
    
    for col in ['facebook', 'instagram', 'linkedin', 'emails']:
        if col not in leads.columns:
            leads[col] = None

    leads['Digital Score'] = leads.apply(calculate_digital_score, axis=1)
    leads['Contact Profile'] = leads.apply(build_contact_profile, axis=1)

    # 4. Domain Check (.PL and .COM) & Template Matching
    print(f"--- Checking domain availability and matching templates for {len(leads)} leads ---")
    domain_pl = []
    domain_com = []
    template_slugs = []
    magic_links = []
    
    for idx, row in leads.iterrows():
        # Domain Check
        base_name = clean_name_for_domain(row['title'])
        if base_name:
            print(f"  > Checking: {base_name}.pl/.com")
            domain_pl.append(check_domain_availability(f"{base_name}.pl"))
            time.sleep(0.5) # Anti-block delay
            domain_com.append(check_domain_availability(f"{base_name}.com"))
            time.sleep(0.5)
        else:
            domain_pl.append("N/A")
            domain_com.append("N/A")
            
        # Template Matching
        # Prioritize the keyword used for search, with business name as secondary context
        search_kw = row.get('search_keyword', '')
        slug, link = get_best_template(row['title'], row['City'], row['Phone'], search_keyword=search_kw)
        template_slugs.append(slug)
        magic_links.append(link)

    leads['Domain .PL'] = domain_pl
    leads['Domain .COM'] = domain_com
    leads['Template Slug'] = template_slugs
    leads['Magic Link'] = magic_links

    # 5. Sort: By Digital Score (Ghosts first), then Reviews
    leads = leads.sort_values(by=['Digital Score', 'review_count'], ascending=[True, True])

    # 6. Cleanup
    columns_to_keep = {
        'title': 'Business Name',
        'City': 'City',
        'address': 'Address',
        'Contact Profile': 'Contact Profile',
        'Domain .PL': 'Domain .PL',
        'Domain .COM': 'Domain .COM',
        'Template Slug': 'Template Slug',
        'Magic Link': 'Magic Link',
        'Digital Score': 'Digital Score',
        'review_count': 'Reviews',
        'review_rating': 'Rating',
        'link': 'Maps URL'
    }
    
    existing_cols = [col for col in columns_to_keep.keys() if col in leads.columns]
    final_leads = leads[existing_cols].rename(columns=columns_to_keep)

    # Save
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    final_leads.to_csv(output_file, index=False)
    
    print(f"Filtering & Domain Checks complete. {len(final_leads)} leads found.")
    print(f"Output saved to: {output_file}")
