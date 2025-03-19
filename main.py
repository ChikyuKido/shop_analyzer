import requests
from db import Database
from parser import Parser
from tqdm import tqdm

MAX_PAGES = 356

if __name__ == "__main__":
    db = Database("database.db")
    parser = Parser()
    page = 3

    with tqdm(total=MAX_PAGES, desc="Pages", unit="page") as pbar:
        while True:
            response = requests.get(f"https://shop.billa.at/kategorie?page={page}")
            shop_entries = parser.ParseHTML(response.text)
            if len(shop_entries) == 0:
                break
            for entry in shop_entries:
                db.insertShopEntry(entry)
            page += 1
            pbar.update(1)
            if page > MAX_PAGES:
                pbar.total = page
    db.close()
