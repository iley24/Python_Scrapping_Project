# scrape.py

import argparse
import time
from parsers import get_category_links, parse_category

def main():
    parser = argparse.ArgumentParser(description="Book Scraper (Books to Scrape)")
    parser.add_argument("--categories", type=str, help="Comma-separated list of categories to scrape (e.g. Travel,Poetry)")
    parser.add_argument("--max-pages", type=int, default=None, help="Limit number of pages per category (for tests)")
    parser.add_argument("--delay", type=float, default=None, help="Delay (in seconds) between requests")
    parser.add_argument("--outdir", type=str, default="outputs", help="Output directory for CSV and images")

    args = parser.parse_args()

    # Load all available categories
    categories = get_category_links()

    # Prepare selected categories
    if args.categories:
        selected = [c.strip().lower() for c in args.categories.split(",")]
        categories = [(name, url) for name, url in categories if name.lower() in selected]
        if not categories:
            print(f"❌ No matching categories found for: {args.categories}")
            return
    else:
        print("⚠️ No category specified, scraping ALL categories...")

    # Scrape each selected category
    for name, url in categories:
        print(f"\n🚀 Starting category: {name}")
        parse_category(
            category_name=name,
            url=url,
            max_pages=args.max_pages,
            delay=args.delay,
            outdir=args.outdir
        )
        time.sleep(1)

if __name__ == "__main__":
    main()
