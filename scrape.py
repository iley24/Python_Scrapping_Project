# scrape.py

import argparse
import time
from parsers import get_category_links, parse_category

def main():
    # Définition des options que l'utilisateur peut passer en ligne de commande
    parser = argparse.ArgumentParser(description="Book Scraper (Books to Scrape)")
    parser.add_argument("--categories", type=str, help="Liste des catégories à scraper, séparées par des virgules (ex: Travel,Poetry)")
    parser.add_argument("--max-pages", type=int, default=None, help="Nombre max de pages à scraper par catégorie (optionnel)")
    parser.add_argument("--delay", type=float, default=None, help="Délai entre chaque requête (en secondes)")
    parser.add_argument("--outdir", type=str, default="outputs", help="Dossier de sortie pour les CSV et les images")

    args = parser.parse_args()

    # Récupère toutes les catégories disponibles sur le site
    categories = get_category_links()

    # Filtre les catégories choisies par l'utilisateur
    if args.categories:
        selected = [c.strip().lower() for c in args.categories.split(",")]
        categories = [(name, url) for name, url in categories if name.lower() in selected]
        if not categories:
            print(f"❌ Aucune catégorie trouvée pour : {args.categories}")
            return
    else:
        print("⚠️ Aucune catégorie spécifiée, toutes les catégories seront scrappées.")

    # Lance le scraping pour chaque catégorie sélectionnée
    for name, url in categories:
        print(f"\n🚀 Début du scraping pour la catégorie : {name}")
        parse_category(
            category_name=name,
            url=url,
            max_pages=args.max_pages,
            delay=args.delay,
            outdir=args.outdir
        )
        time.sleep(1)  # Petite pause entre les catégories

if __name__ == "__main__":
    main()
