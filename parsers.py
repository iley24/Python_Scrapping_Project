#parsers.py

import requests
from urllib.parse import urljoin
from parsel import Selector
from settings import BASE_URL, HEADERS, DEFAULT_DELAY, TIMEOUT

def nettoyerLien(base_url, lien):
    """Normalize relative links correctly for books.toscrape.com."""
    if lien.startswith("../../../"):
        lien = lien.replace("../../../", "catalogue/")
    elif lien.startswith("../../"):
        lien = lien.replace("../../", "catalogue/")
    elif lien.startswith("../"):
        lien = lien.replace("../", "catalogue/")
    return urljoin(base_url, lien)

def get_category_links():
    """Extract all category links from homepage."""
    res = requests.get(BASE_URL, headers=HEADERS, timeout=TIMEOUT)
    sel = Selector(text=res.text)

    categories = []
    for a in sel.css(".side_categories ul li ul a"):
        name = a.css("::text").get().strip()
        href = a.attrib["href"]
        full_url = urljoin(BASE_URL, href)
        categories.append((name, full_url))
    return categories


def parse_category(category_name, url, max_pages=None, delay=None, outdir="outputs"):
    """Scrape all books from a category (with pagination)."""
    from utils import write_csv, download_file, ensure_dir
    import time

    category_name_clean = category_name.replace(" ", "_").lower()
    csv_path = f"{outdir}/csv/category_{category_name_clean}.csv"
    image_folder = f"{outdir}/images/{category_name_clean}"
    ensure_dir(image_folder)

    header = ["Title", "Price", "Rating", "Book URL", "Image", "Stock", "UPC", "Category"]
    rows = []

    page_count = 0
    while url:
        page_count += 1
        if max_pages and page_count > max_pages:
            print(f"🛑 Stopped after {max_pages} pages for testing.")
            break

        print(f"🔎 Scraping page: {url}")
        res = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        sel = Selector(text=res.text)

        for article in sel.css("article.product_pod"):
            title = article.css("h3 a::attr(title)").get()
            price = article.css("p.price_color::text").get()
            price = price.replace("Â", "").strip() if price else None
            rating = article.css("p.star-rating::attr(class)").get()
            book_link = article.css("h3 a::attr(href)").get()
            book_url = nettoyerLien(BASE_URL, book_link)
            image_link = article.css("img::attr(src)").get()
            image_url = nettoyerLien(BASE_URL, image_link)

            # Go to product page for details
            res_book = requests.get(book_url, headers=HEADERS, timeout=TIMEOUT)
            sel_book = Selector(text=res_book.text)

            stock = sel_book.css("p.instock.availability::text").getall()
            stock_clean = [s.strip() for s in stock if s.strip()]
            stock = stock_clean[0] if stock_clean else None
            upc = sel_book.css("table tr:nth-child(1) td::text").get()

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

                print(f"📥 Downloading image: {image_url} -> {image_path}")
                success = download_file(image_url, image_path)

                if success:
                    print(f"📸 Image saved: {image_path}")
                else:
                    print(f"⚠️ Failed to save image for: {title}")
            else:
                image_path = None

            rows.append([title, price, rating, book_url, image_url, stock, upc, category_name])
            print(f"✅ [{category_name}] Saved: {title}")

            time.sleep(delay if delay else DEFAULT_DELAY)

        # Pagination
        next_page = sel.css("li.next a::attr(href)").get()
        url = urljoin(url, next_page) if next_page else None

    write_csv(csv_path, rows, header)
    print(f"💾 Category saved to: {csv_path}")
