# utils.py

import os
import csv
import requests

# Crée un dossier s’il n’existe pas déjà
def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

# Écrit les données dans un fichier CSV avec un en-tête
def write_csv(file_path, rows, header):
    ensure_dir(os.path.dirname(file_path))
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)

# Télécharge un fichier (ex: image) depuis une URL et le sauvegarde
def download_file(url, dest_path):
    try:
        ensure_dir(os.path.dirname(dest_path))
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"⚠️ Erreur lors du téléchargement de {url}: {e}")
        return False
