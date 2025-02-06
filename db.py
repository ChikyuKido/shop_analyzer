import os.path
import sqlite3
from datetime import datetime
from enum import Enum


class ShopEntryTypes(Enum):
    NONE = 0
    LITER = 1
    GRAMM = 2
    STUECK = 3
    ONE_KG = 4
    METER = 5
    KISTE = 6


class ShopEntry:
    def __init__(self, name, price, image_data, product_link, additional_info,type):
        self.name = name
        self.price = price
        self.image_data = image_data
        self.product_link = product_link
        self.additional_info = additional_info
        self.date_added = datetime.now().strftime("%Y%m%d")
        self.type = type

class Database:
    def __init__(self,path):
        is_new = not os.path.exists(path)
        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()
        if is_new:
            self.initTables()

    def initTables(self):
        print("Initializing tables...")
        self.cursor.execute("""
        CREATE TABLE shop_entry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            image_data TEXT,
            product_link TEXT,
            additional_info TEXT,
            date_added TEXT NOT NULL,
            type TEXT NOT NULL,
            UNIQUE(product_link, date_added)
        );
        """)
        self.db.commit()
    def insertShopEntry(self, entry: ShopEntry):
        try:
            self.cursor.execute("""
                INSERT INTO shop_entry (name, price, image_data, product_link, additional_info, date_added,type)
                VALUES (?, ?,?, ?, ?, ?, ?);
            """, (entry.name, entry.price, entry.image_data, entry.product_link, entry.additional_info, entry.date_added,str(entry.type)))

            self.db.commit()
        except sqlite3.IntegrityError:
            print(f"Entry with name '{entry.name}' for date '{entry.date_added}' already exists!")


    def close(self):
        self.db.commit()
        self.db.close()