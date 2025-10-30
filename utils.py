#utils.py

import os
import csv
import requests

def ensure_dir(path: str):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def write_csv(file_path, rows, header):
    """Write rows to a CSV file with header."""
    ensure_dir(os.path.dirname(file_path))
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)

def download_file(url, dest_path):
    """Download a file from a URL and save it to dest_path."""
    try:
        ensure_dir(os.path.dirname(dest_path))
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"⚠️ Failed to download {url}: {e}")
        return False
