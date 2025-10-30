# parsers.py

import requests
from urllib.parse import urljoin
from parsel import Selector
from settings import BASE_URL, HEADERS, DEFAULT_DELAY, TIMEOUT


def nettoyerLien(base_url, lien):
    """Corrige les liens relatifs pour obtenir un lien complet (URL absolue)."""
    if lien.startswith("../../../"):
        lien = lien.replace("../../../", "catalogue/")
    elif lien.startswith("../../"):
        lien = lien.replace("../../", "catalogue/")
    elif lien.startswith("../"):
        lien = lien.replace("../", "catalogue/")
    return urljoin(base_url, lien)


def get_category_links():
    """Récupère les liens de toutes les catégories sur la page d’accueil."""
    res = requests.get(BASE_URL, headers=HEADERS, timeout=TIMEOUT)
    sel = Selector(text=res.text)

    categories = []
    for a in sel.css(".side_categories ul li ul a"):
        name = a.css("::text").get().strip()  # Nom de la catégorie
        href = a.attrib["href"]  # Lien relatif
        full_url = urljoin(BASE_URL, href)  # Lien complet
        categories.append((name, full_url))
    return categories


def parse_category(category_name, url, max_pages=None, delay=None, outdir="outputs"):
    """Scrape tous les livres d’une catégorie et télécharge les images."""
    from utils import write_csv, download_file, ensure_dir
    import time

    # Prépare les chemins de sortie
    category_name_clean = category_name.replace(" ", "_").lower()
    csv_path = f"{outdir}/csv/category_{category_name_clean}.csv"
    image_folder = f"{outdir}/images/{category_name_clean}"
    ensure_dir(image_folder)

    # Entêtes du fichier CSV
    header = ["Title", "Price", "Rating", "Book URL", "Image", "Stock", "UPC", "Category"]
    rows = []

    page_count = 0
    while url:
        page_count += 1
        if max_pages and page_count > max_pages:
            print(f"🛑 Arrêt après {max_pages} page(s).")
            break

        print(f"🔎 Scraping page: {url}")
        res = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        sel = Selector(text=res.text)

        # Boucle sur chaque livre de la page
        for article in sel.css("article.product_pod"):
            title = article.css("h3 a::attr(title)").get()  # Titre
            price = article.css("p.price_color::text").get()  # Prix
            price = price.replace("Â", "").strip() if price else None
            rating = article.css("p.star-rating::attr(class)").get()  # Évaluation
            book_link = article.css("h3 a::attr(href)").get()
            book_url = nettoyerLien(BASE_URL, book_link)  # Lien du livre
            image_link = article.css("img::attr(src)").get()
            image_url = nettoyerLien(BASE_URL, image_link)  # Lien de l’image

            # Aller sur la page du livre pour plus d’infos
            res_book = requests.get(book_url, headers=HEADERS, timeout=TIMEOUT)
            sel_book = Selector(text=res_book.text)

            # Informations du stock et du code produit (UPC)
            stock = sel_book.css("p.instock.availability::text").getall()
            stock_clean = [s.strip() for s in stock if s.strip()]
            stock = stock_clean[0] if stock_clean else None
            upc = sel_book.css("table tr:nth-child(1) td::text").get()

            # Téléchargement de l’image
            if upc and title:
                safe_title = (
                    title.replace("/", "_")
                    .replace("\\", "_")
                    .replace(":", "_")
                    .replace("?", "_")
                    .replace('"', "_")
                    .replace("*", "_")
                )
                image_path = f"{image_folder}/{upc}_{safe_title}.jpg"

                print(f"📥 Téléchargement de l’image: {image_url} -> {image_path}")
                success = download_file(image_url, image_path)

                if success:
                    print(f"📸 Image enregistrée: {image_path}")
                else:
                    print(f"⚠️ Erreur lors du téléchargement: {title}")
            else:
                image_path = None

            # Ajoute les infos du livre dans le CSV
            rows.append([title, price, rating, book_url, image_url, stock, upc, category_name])
            print(f"✅ [{category_name}] Livre enregistré: {title}")

            # Attendre un peu entre les requêtes
            time.sleep(delay if delay else DEFAULT_DELAY)

        # Vérifie s’il y a une page suivante
        next_page = sel.css("li.next a::attr(href)").get()
        url = urljoin(url, next_page) if next_page else None

    # Sauvegarde des données dans le CSV
    write_csv(csv_path, rows, header)
    print(f"💾 Catégorie enregistrée dans: {csv_path}")
