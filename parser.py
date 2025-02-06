from bs4 import BeautifulSoup

from db import ShopEntry, ShopEntryTypes


class Parser:
    def __init__(self):
        pass

    def ParseHTML(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        products = soup.select('li.ws-product-item-base')

        product_data = []

        for product in products:
            name_tag = product.select_one('[data-test="product-title"]')
            name = name_tag.text.strip() if name_tag else "Unknown"
            original_price_tag = product.select_one('.ws-product-price-strike')
            if original_price_tag:
                price = original_price_tag.text.strip()
            else:
                price_tag = product.select_one('.ws-product-price-type__value')
                price = price_tag.text.strip() if price_tag else "0"
            price = price.replace('\xa0', '').replace('€', '').strip()
            price = float(price.replace(',', '.')) if price else 0.0

            img_tag = product.select_one('.ws-product-image')
            img_url = img_tag['src'] if img_tag else "No image"

            link_tag = product.select_one('a.ws-product-tile__link')
            link = link_tag['href'] if link_tag else "#"

            additional_info_tag = product.select_one('.ws-product-information__piece-description li')
            additional_info = additional_info_tag.text.strip() if additional_info_tag else "No additional info"
            additional_info = additional_info.replace('\xa0',"")
            args = additional_info.split(" ")
            if args[1] == "g" or args[1] == "kg":
                type = ShopEntryTypes.GRAMM
                value = float(args[0].replace(",","."))
                if args[1] == "kg":
                    value *= 1000
                additional_info = value
            elif args[1] == "liter" or args[1] == "ml":
                type = ShopEntryTypes.LITER
                value = float(args[0].replace(",","."))
                if args[1] == "ml":
                    value /= 1000
                additional_info = value
            elif args[1] == "stk" or args[1] == "Rollen" or args[1] == "Bund" or args[1] == "Blatt" or args[1] == "Packung" or args[1] == "Teebeutel" or args[1] == "Waschgang" or args[1] == "Beutel" or args[1] == "Paar" or args[1] == "Portion":
                type = ShopEntryTypes.STUECK
                value = int(args[0])
                additional_info = value
            elif args[0] == "Ab":
                type = ShopEntryTypes.ONE_KG
            elif args[1] == "m":
                type = ShopEntryTypes.METER
                value = float(args[0])
                additional_info = value
            elif args[1] == "Kiste" or args[1] == "Tray":
                type = ShopEntryTypes.KISTE
                value = int(args[0].replace("er",""))
                additional_info = value
            else:
                type = ShopEntryTypes.NONE
                print("Not found: " + additional_info)
            if type != ShopEntryTypes.NONE:
                product_data.append(ShopEntry(name,price,img_url,f"https://shop.billa.at{link}",additional_info,type))
        return product_data