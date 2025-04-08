#!/usr/bin/env python3
import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env if present (optional)
load_dotenv()

# Only the API key is now required.
API_KEY = os.getenv('SMUGMUG_API_KEY')
if not API_KEY:
    sys.exit("Error: Please set SMUGMUG_API_KEY environment variable.")

# Load the album mapping from data/smugmug_albums.json.
mapping_file = os.path.join(os.path.dirname(__file__), "..", "data", "smugmug_albums.json")
try:
    with open(mapping_file, 'r') as mf:
        album_mapping = json.load(mf)
except Exception as e:
    sys.exit(f"Error: Could not load mapping file {mapping_file}: {e}")

# Create the output directory for the per-album JSON files.
output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "smugmug")
os.makedirs(output_dir, exist_ok=True)

# Iterate over each album in the mapping.
for slug, album_id in album_mapping.items():
    api_url = f"https://api.smugmug.com/api/v2/album/{album_id}!images?APIKey={API_KEY}"
    print(f"Fetching data for album '{slug}' from: {api_url}")
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        output_path = os.path.join(output_dir, f"{album_id}.json")
        with open(output_path, "w") as outfile:
            json.dump(data, outfile)
        print("Data saved to", output_path)
    except Exception as e:
        sys.exit(f"Error fetching data for album '{slug}': {e}")
