#!/usr/bin/env python3
import os
import sys
import json
import requests

# The SmugMug API requires an API key.
API_KEY = os.getenv('SMUGMUG_API_KEY')
ALBUM_ID = os.getenv('SMUGMUG_ALBUM_ID')

if not API_KEY or not ALBUM_ID:
    sys.exit("Error: Please set SMUGMUG_API_KEY and SMUGMUG_ALBUM_ID environment variables.")

# Construct the API URL. (Adjust the endpoint and parameters per SmugMug API documentation.)
api_url = f"https://api.smugmug.com/api/v2/album/{ALBUM_ID}!images?APIKey={API_KEY}"
print("Fetching SmugMug data from:", api_url)

try:
    response = requests.get(api_url)
    response.raise_for_status()
    data = response.json()

    # Write the JSON data to data/smugmug-gallery.json
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "smugmug-gallery.json")
    with open(output_path, "w") as outfile:
        json.dump(data, outfile)
    print("Data saved to", output_path)
except Exception as e:
    sys.exit(f"Error fetching data from SmugMug: {e}")
