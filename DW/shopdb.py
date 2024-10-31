# Estrutura que vai salvar os itens a venda
import os
import deep_items
from emoji import emojize

class ShopDB:
    def __init__(self, server):
        self.server = server
        self.items_for_sale = [{}, {}, {}, {}, {}, {}, {}]  # A estrutura é bem simples. Uma lista da raridade
                                                            # seguida por um dicionário do código dos talismans
                                                            # que vai referenciar um dicionario contendo os preços das ofertas
                                                            # que cada entrada deste dicionário vai referenciar uma lista contendo as ofertas da seguinte forma:
                                                            # [[chat_id1, quantidade1], [chat_id2, quantidade2], ... ]
                                                            # Assim ó items_for_sale[rarity]["tal_code"]["price"][offer]
        self.shop_file = "dbs/shop.dat"
        self.shop_backup = "dbs/shop.dat.old"
        self.talismandb = deep_items.Talismandb()
        loaded = self.server.helper.load_pickle(self.shop_file)
        if loaded:
            self.items_for_sale = loaded

    def show_talismans_for_sale(self, chat_id):
        text = ""
        rarity_list = [
            emojize(":zzz:"),
            emojize(":pile_of_poo:"),
            emojize(":OK_hand:"),
            emojize(":flexed_biceps:"),
            emojize(":angry_face_with_horns:"),
            emojize(":smiling_face_with_halo:"),
            emojize(":bright_button:"),
        ]
        r = 0
        for rarity in self.items_for_sale:
            print(rarity)
            for tal_code, prices in rarity.items():
                print(prices)
                for price, offers in prices.items():
                    print(offers)
                    for offer in offers:
                        if chat_id == offer[0]:
                            text += f"(x{offer[1]}) |{rarity_list[r]}| *{self.talismandb.talismans[tal_code].name}* price: {price}\n /r_{r}_{tal_code}\n\n"
            r += 1
        text = text.replace("_", "\\_")
        return text + "\n"

    def generate_buy_text(self):

        text = ""
        r = 0
        rarity_list = [
            emojize(":zzz:"),
            emojize(":pile_of_poo:"),
            emojize(":OK_hand:"),
            emojize(":flexed_biceps:"),
            emojize(":angry_face_with_horns:"),
            emojize(":smiling_face_with_halo:"),
            emojize(":bright_button:"),
        ]
        perfect  = False
        found = False
        while not perfect:
            perfect = True
            r = 0
            for rarity in self.items_for_sale:
                if rarity:
                    for tal_code, prices in rarity.items():
                        for price, offers in prices.items():
                            if not offers:
                                found = True
                                perfect = False
                                del self.items_for_sale[r][tal_code][price]
                                break
                        if found:
                            break
                    if found:
                        break
                if found:
                    break
                r += 1

        r = 0
        for rarity in self.items_for_sale:
            if rarity:
                for tal_code, prices in rarity.items():
                    lowest_price = -1
                    qty = 0
                    for price, offers in prices.items():
                        if lowest_price == -1 or lowest_price > int(price):
                            lowest_price = int(price)
                        for offer in offers:
                            qty += offer[1]
                    if qty:
                        text += emojize(f"(x{qty}) |{rarity_list[r]}| *{self.talismandb.talismans[tal_code].name}*\n(lowest price: {lowest_price}:leaf_fluttering_in_wind:) /p_{r}_{tal_code}\n\n")
                text += "\n"
            r += 1
        text = text.replace("_", "\\_")
        return text

    def save_shop(self):
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle(self.items_for_sale, self.shop_file)
