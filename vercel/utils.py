import os
import json
from django.conf import settings

def load_temple_data():
    """
    Load temple data from data.json with multiple fallback locations
    """
    possible_paths = [
        # Try BASE_DIR first
        os.path.join(settings.BASE_DIR, 'data.json'),
        # Try current working directory
        'data.json',
        # Try in the vercel app directory
        os.path.join(os.path.dirname(__file__), '..', 'data.json'),
        # Try absolute path in case we're in a subdirectory
        os.path.join(os.path.dirname(settings.BASE_DIR), 'data.json'),
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    return data
        except Exception as e:
            print(f"Failed to load data from {path}: {e}")
            continue
    
    # Final fallback: use the Python backup data
    try:
        from .temple_data import TEMPLE_DATA
        print("Using Python backup temple data")
        return TEMPLE_DATA
    except ImportError:
        pass
    
    # If no file found, return empty data
    print("Warning: Could not find data.json in any location")
    return {'ancient_sites_sisaket': []}

def get_temple_by_name(temple_name):
    """
    Get a specific temple by name from the data
    """
    data = load_temple_data()
    for site in data.get('ancient_sites_sisaket', []):
        if site.get('ชื่อสถานที่') == temple_name:
            return site
    return None