import urllib.parse
import re

# Base URL for the marketplace - Updated to V2 Production
BASE_URL = "https://katalog.czerwinskidawid.pl"

# Template Registry
# Maps template slugs to a list of keywords (lowercase).
# Includes Polish grammatical variations (singular, plural, adjective forms).
TEMPLATE_REGISTRY = {
    "warsztat-pro": [
        # Polish
        "warsztat", "warsztaty", "samochod", "samochodowy", "samochodowe", "auto", "auta", 
        "mechanik", "mechanika", "naprawa", "naprawy", "serwis", "serwisy", "wulkanizacja", 
        "opony", "opon", "blacharstwo", "lakiernictwo", "lakiernik", "blacharz", "stacja kontroli",
        "pojazdow", "pojazd", "motoryzacja", "moto", "garage", "detailing", "autodetailing", 
        "auto detailing", "detailingowe", "auto spa", "car spa", "myjnia", "kosmetyka aut",
        "kosmetyka samochodowa", "pielęgnacja aut", "pielęgnacja samochodów", "pielegnacja",
        "ceramiczna", "powłoka ceramiczna", "powloka", "kwarcowa", "wosk", "woskowanie",
        "polerowanie", "korekta lakieru", "renowacja lakieru", "czyszczenie tapicerki",
        "pranie tapicerki", "czyszczenie wnętrza", "niewidzialna wycieraczka", "konserwacja skóry",
        "zabezpieczenie lakieru", "ppf", "folia ochronna", "przyciemnianie szyb", "odgrzybianie",
        "elektryka", "elektryk", "klimatyzacja", "tłumiki", "szyby", "holowanie", "pomoc drogowa",
        "części", "akcesoria", "tuning", "offroad", "4x4", "skrzynie biegów", "regeneracja",
        # English
        "workshop", "repair", "service", "car", "cars", "auto", "automotive", "mechanic", 
        "garage", "tires", "tyres", "body shop", "paint shop", "detailing", "car detailing",
        "auto detailing", "auto spa", "car spa", "wash", "car wash", "towing", "ceramic coating",
        "paint correction", "polishing", "interior cleaning", "upholstery cleaning", "ppf",
        "window tinting"
    ],
    "bistro-modern": [
        # Polish
        "restauracja", "restauracje", "bistro", "bar", "bary", "jadłodajnia", "jadlodajnia",
        "kawiarnia", "kawiarnie", "cafe", "kafejka", "cukiernia", "piekarnia", "pieczywo",
        "pizza", "pizzeria", "pizzerie", "włoska", "wloska", "kuchnia", "smaki", "obiady",
        "lunch", "kolacje", "śniadania", "sniadania", "burger", "burgery", "kebab", "keby",
        "sushi", "ramen", "azjatycka", "chińska", "chinska", "wietnamska", "tajska", "indie",
        "pierogi", "pierogarnia", "naleśniki", "nalesniki", "pub", "klub", "wino", "piwo",
        "alkohole", "koktajle", "drink", "lody", "lodziarnia", "gofry", "zapiekanki", "food truck",
        "catering", "dieta", "pudełkowa", "pudelkowa", "wege", "wegańska", "weganska", "zdrowa",
        # English
        "restaurant", "bistro", "bar", "cafe", "coffee", "bakery", "pastry", "pizza", "pizzeria",
        "kitchen", "cuisine", "food", "lunch", "dinner", "breakfast", "burger", "sushi", "pub",
        "club", "wine", "beer", "cocktails", "ice cream", "catering", "diet", "vegan", "healthy"
    ],
    "helios-advise": [
        # Polish
        "kancelaria", "kancelarie", "prawnik", "prawnicy", "adwokat", "adwokaci", "radca", "radcy",
        "prawny", "prawne", "prawo", "notariusz", "notarialna", "doradztwo", "doradca", "doradcy",
        "konsulting", "consulting", "biuro rachunkowe", "ksiegowosc", "księgowość", "księgowy",
        "ksiegowy", "podatki", "podatkowe", "finanse", "finansowe", "kredyty", "ubezpieczenia",
        "ubezpieczeniowa", "audyt", "audytor", "biegły", "biegly", "rzeczoznawca", "windykacja",
        "szkolenia", "edukacja", "kursy", "tłumacz", "tlumacz", "tłumaczenia", "tlumaczenia",
        "agencja nieruchomości", "nieruchomości", "nieruchomosci", "zarządzanie", "zarzadzanie",
        # English
        "law firm", "lawyer", "attorney", "solicitor", "legal", "notary", "advisory", "advisor",
        "consulting", "consultant", "accounting", "accountant", "bookkeeping", "tax", "taxes",
        "finance", "financial", "credit", "loans", "insurance", "audit", "auditor", "expert",
        "debt collection", "training", "education", "courses", "translator", "translation",
        "real estate", "property", "management"
    ],
    "cyber-security": [
        # Polish
        "informatyka", "informatyk", "it", "komputery", "komputerowy", "serwis komputerowy",
        "naprawa laptopów", "naprawa komputerów", "laptop", "pc", "software", "hardware",
        "sieci", "sieciowe", "serwery", "administrator", "admin", "bezpieczeństwo", "bezpieczenstwo",
        "cyber", "security", "ochrona", "dane", "odzyskiwanie danych", "telefony", "gsm",
        "smartfon", "tablet", "serwis gsm", "akcesoria gsm", "elektronika", "elektroniczny",
        "programowanie", "programista", "kodowanie", "web", "strony www", "hosting", "domeny",
        "kamery", "monitoring", "alarmy", "systemy alarmowe", "automatyka", "smart home",
        # English
        "informatics", "computer", "computers", "laptop", "pc", "repair", "software", "hardware",
        "network", "networking", "server", "servers", "admin", "security", "protection", "data",
        "recovery", "phone", "mobile", "smartphone", "gsm", "electronics", "programming",
        "developer", "coding", "web", "websites", "hosting", "domains", "cameras", "cctv",
        "monitoring", "alarms", "automation"
    ],
    "landing-aplikacji": [
        # Polish
        "aplikacja", "aplikacje", "app", "apps", "mobile", "mobilne", "saas", "startup",
        "platforma", "portal", "system", "rozwiązania", "rozwiazania", "cyfrowe", "digital",
        "technologie", "technologia", "innowacje", "innowacja", "ai", "sztuczna inteligencja",
        "machine learning", "bot", "boty", "automatyzacja", "cloud", "chmura", "big data",
        "analytics", "analiza", "narzędzia", "narzedzia", "online", "internet",
        # English
        "application", "app", "apps", "mobile", "saas", "startup", "platform", "portal", "system",
        "solutions", "digital", "technology", "tech", "innovation", "ai", "artificial intelligence",
        "bot", "automation", "cloud", "data", "analytics", "tools", "online", "internet"
    ],
    "agencja-kreatywna": [
        # Polish
        "marketing", "reklama", "reklamowa", "agencja", "kreatywna", "neon", "media", "group", 
        "design", "designu", "branding", "brandingowa", "social media", "content", "seo", 
        "sem", "ads", "kampanie", "kampania", "grafika", "graficzne", "web design", 
        "tworzenie stron", "strony www", "identyfikacja wizualna", "logo", "logotyp",
        # English
        "marketing", "advertising", "agency", "creative", "media", "design", "branding",
        "social media", "content", "seo", "sem", "ads", "campaign", "graphics", "web design",
        "web development", "websites", "identity", "logo"
    ],
    "portfolio-osobista": [
        # Polish
        "fotograf", "fotografia", "zdjęcia", "zdjecia", "sesje", "grafik", "grafika", "design",
        "designer", "projektant", "projektowanie", "architekt", "wnętrza", "wnetrza", "ogrody",
        "artysta", "sztuka", "malarz", "rzeźbiarz", "rekodzieło", "rękodzieło", "handmade",
        "muzyk", "zespół", "zespol", "dj", "wodzirej", "trener", "trener personalny", "coach",
        "nauczyciel", "korepetycje", "tłumacz przysięgły", "freelancer", "wolny strzelec",
        "bloger", "blog", "vlog", "influencer", "twórca", "tworca", "wideo", "film", "montaż",
        "copywriter", "pisarz", "dziennikarz", "redaktor", "wizażystka", "wizazystka", "makijaż",
        "fryzjerka", "stylista", "stylistka",
        # English
        "photographer", "photography", "photos", "graphic", "graphics", "design", "designer",
        "architect", "interior", "garden", "artist", "art", "painter", "sculptor", "craft",
        "handmade", "musician", "band", "dj", "trainer", "personal trainer", "coach", "teacher",
        "tutor", "freelancer", "blogger", "vlog", "influencer", "creator", "video", "film",
        "editing", "copywriter", "writer", "journalist", "editor", "makeup", "makeup artist",
        "hairdresser", "stylist"
    ]
}

def clean_text(text):
    """Normalize text for comparison."""
    if not text:
        return ""
    # Remove special chars and lowercase
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def get_best_template(business_name, city, phone, address, search_keyword=None, forced_template=None):
    """
    Analyzes search keyword and business name to find the best template match.
    Prioritizes forced_template if provided.
    Returns: (template_slug, magic_link)
    """
    # 0. Forced Template Strategy
    if forced_template and forced_template.strip():
        best_slug = forced_template.strip()
    else:
        # Intelligent Selection Logic
        normalized_name = clean_text(business_name)
        normalized_kw = clean_text(search_keyword) if search_keyword else ""
        
        best_slug = "agencja-kreatywna" # Default fallback
        max_matches = 0

        # 1. Primary Strategy: Match against Search Keyword
        if normalized_kw:
            for slug, keywords in TEMPLATE_REGISTRY.items():
                for kw in keywords:
                    if kw in normalized_kw:
                        best_slug = slug
                        max_matches = 100 # High confidence
                        break
                if max_matches == 100:
                    break

        # 2. Secondary Strategy: Match against Business Name
        if max_matches < 100:
            for slug, keywords in TEMPLATE_REGISTRY.items():
                matches = 0
                for keyword in keywords:
                    if keyword in normalized_name:
                        matches += 1
                        if f" {keyword} " in f" {normalized_name} ":
                            matches += 2
                
                if matches > max_matches:
                    max_matches = matches
                    best_slug = slug

    # Construct Magic Link (DSA V2 Format)
    # https://katalog.czerwinskidawid.pl/templates/[slug]?name=...&city=...&address=...&phone=...
    params = {
        "name": business_name,
        "city": city if city else "",
        "address": address if address else "",
        "phone": phone if phone else ""
    }
    
    # Clean up None values
    params = {k: v for k, v in params.items() if v is not None}
    
    query_string = urllib.parse.urlencode(params)
    magic_link = f"{BASE_URL}/templates/{best_slug}?{query_string}"

    return best_slug, magic_link
