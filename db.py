import os.path
import sqlite3
from datetime import datetime
from enum import Enum


class ShopEntryTypes(Enum):
    NONE = 0
    LITER = 1
    GRAMM = 2
    STUECK = 3
    METER = 4
    KISTE = 5


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
        self.path = path
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
                SELECT image_data FROM shop_entry WHERE product_link = ?;
            """, (entry.product_link,))
            existing_image_data = self.cursor.fetchone()
            if existing_image_data and existing_image_data[0] == entry.image_data:
                entry.image_data = ""
            self.cursor.execute("""
            INSERT INTO shop_entry (name, price, image_data, product_link, additional_info, date_added, type)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (entry.name, entry.price, entry.image_data, entry.product_link, entry.additional_info, entry.date_added, str(entry.type)))
            self.db.commit()

        except sqlite3.IntegrityError:
            print(f"Entry with name '{entry.name}' for date '{entry.date_added}' already exists!")

    def searchShopEntry(self,query):
        self.cursor.execute(f"""
        SELECT DISTINCT * FROM shop_entry group by product_link HAVING name like "%{query}%" 
        """)
        results = self.cursor.fetchall()
        if not results:
            return None
        return [{"name": r[1],"image": r[3],"product_link":r[4],"additional_info":r[5],"type":r[7]} for r in results]
    def getInfoForShopEntry(self,product_link):
        self.cursor.execute(f"""
         SELECT DISTINCT * FROM shop_entry group by product_link HAVING product_link like "{product_link}" 
        """)
        result = self.cursor.fetchone()
        if not result:
            return None
        return {"name": result[1],"price":result[2], "image": result[3],"product_link":result[4],"additional_info":result[5],"type":result[7]}
    def getPriceHistoryForShopEntry(self,product_id):
        self.cursor.execute(f"""
         SELECT * FROM shop_entry  WHERE product_link like "{product_id}" 
        """)
        results = self.cursor.fetchall()
        if not results:
            return None
        return [{"price": r[2],"additional_info":r[5],"date":r[6]} for r in results]
    def close(self):
        self.db.commit()
        self.db.close()