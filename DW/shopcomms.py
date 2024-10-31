# Todos os comandos relacionados a leaves é feito aqui.

from emoji import emojize
import items
import player
import deep_items
import copy
import time


class ShopComms:
    def __init__(self, server):
        self.server = server
        self.def_wait_time = 60
        self.bs_scroll_cost = 50
        self.class_reset_cost = 10
        self.tsa_cost = 10
        self.Talismandb = deep_items.Talismandb()
        self.phase_organizer = {}
        self.actions = {
            "/shop": self.show_shop,
            "/purchase": self.purchase_leaves,
            "/special_inv": self.show_special_inv,
            "/player_market": self.show_market,
            "/sell_talismans": self.sell_talismans,
            "/buy_talismans": self.buy_talismans,
            # "/arena_win": self.show_rank,
        }
        self.internal = {

        }


    def show_shop(self, caller, *args):
        if not args:
            text = emojize( f"Welcome to the shop. Here you can buy items using leaves :leaf_fluttering_in_wind:.\n"
                            f"Or if you want you can purchase some with /purchase\n\n"
                            f"Your current balance: {caller.leaves} leaves :leaf_fluttering_in_wind:\n\n"
                            f"*Blacksmith Teleport Scroll*. Price: {self.bs_scroll_cost} leaves :leaf_fluttering_in_wind: /p\_bts\n"
                            f"*Class Reset Scroll*. Price: {self.class_reset_cost} leaves :leaf_fluttering_in_wind: /p\_crs\n")
            if not caller.has_bought_tsa:
                text += emojize(f"*Time Singularity Apparatus*. Price: {self.tsa_cost} leaves :leaf_fluttering_in_wind: (only one in stock) /p\_tsa\n")
            else:
                text += f"*Time Singularity Apparatus*. Sold off\n"
            self.server.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
            return self.def_wait_time*2
        else:
            if args[-1] == "/p_bts":
                if caller.leaves >= self.bs_scroll_cost:
                    caller.leaves -= self.bs_scroll_cost
                    self.give_bts(caller)
                    text = "Thanks for your purchase. With this item you can find the blacksmith instantly wherever you are. You can find it in your /special_inv."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return self.def_wait_time*2
                else:
                    text = emojize("You dont have enough leaves :leaf_fluttering_in_wind: to purchase the balcksmith teleport scroll.")
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return self.def_wait_time*2
            elif args[-1] == "/p_crs":
                if caller.leaves >= self.class_reset_cost:
                    caller.leaves -= self.class_reset_cost
                    self.give_crs(caller)
                    text = "Thanks for your purchase. With this item you can reset your class and return all spent talent points. You can find it in your /special_inv."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return self.def_wait_time*2
                else:
                    text = emojize("You dont have enough leaves :leaf_fluttering_in_wind: to purchase the Class Reset Scroll.")
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return self.def_wait_time*2
            elif args[-1] == "/p_tsa":
                if not caller.has_bought_tsa:
                    if caller.leaves >= self.tsa_cost:
                        caller.leaves -= self.tsa_cost
                        caller.has_bought_tsa = True
                        self.give_tsa(caller)
                        text = "Thanks for your purchase. You can equip it or toss it at a blacksmith. You can find it in your /inv."
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        return self.def_wait_time*2
                    else:
                        text = emojize("You dont have enough leaves :leaf_fluttering_in_wind: to purchase the Time Singularity Apparatus.")
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        return self.def_wait_time*2
                else:
                    text = "No more TSA's for sale."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return self.def_wait_time*2
            return False

    def give_bts(self, user):
        user.special_inventory["bts"] += 1

    def give_crs(self, user):
        user.special_inventory["crs"] += 1

    def give_tsa(self, user):
        newwep = items.Weapon(emojize("Time Singularity Apparatus"), False, "tsa", 1, [30, 30])
        newwep.type2 = "magic"
        newwep.description = "An instrument used by time travellers. A long time ago a fracture in spacetime made the time roll back a couple of days but just for some people. The people that travelled in time recieved this apparatus in their travels. But some never existed in that time, so they never got that. Others never got the apparatus despite of travelling in time. That fracture caused the universe to become unstable and since then many weird things are happening. Like negative strength, item duplication, and infinite loops. This instrument, once owned by an unknown time traveller lost its use as the universe becomes stable again and was set for sale."
        user.inventory.append(newwep)

    def show_special_inv(self, caller, *args):
        if not args:
            text = "Here are some items you purchased at the shop:\n\n"
            if caller.special_inventory["bts"]:
                text += f"(x{caller.special_inventory['bts']}) *Blacksmith Teleport Scroll*. /u\_bts\n"
            if caller.special_inventory["crs"]:
                text += f"(x{caller.special_inventory['crs']}) *Class Reset Scroll*. /u\_crs\n"
            self.server.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
            return self.def_wait_time*2
        else:
            if args[-1] == "/u_bts":
                if caller.special_inventory["bts"]:
                    caller.special_inventory["bts"] -= 1
                    self.use_bts(caller)
                    return False
                else:
                    text = "You don't have any blacksmith teleport scrolls"
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return self.def_wait_time*2
            if args[-1] == "/u_crs":
                if caller.location == "camp":
                    if caller.special_inventory["crs"]:
                        caller.special_inventory["crs"] -= 1
                        self.use_crs(caller)
                        return self.def_wait_time*2
                    else:
                        text = "You don't have any class reset scrolls"
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        return self.def_wait_time*2
                else:
                    text = "Remember, you need to be at camp to spend points, thats why this scoll can only be used at camp."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return self.def_wait_time*2
            return False

    def use_bts(self, user):
        if user.pt_code:
            if user.pt_code in self.server.playersdb.players_and_parties:
                self.server.playersdb.players_and_parties[user.pt_code].leave_pt(user)
        if user.chat_id in self.server.deep_forest_manager.jogs:
            if user.location == "megabeast":
                if user.chat_id in self.server.megadb.players:
                    self.server.megadb.remove_user(user.chat_id)
            if user.chat_id in self.server.deep_forest_manager.jogs:
                self.server.deep_forest_manager.leave(user.chat_id)
            else:
                self.server.woods.add_to_woods(user, 60*60)
        else:
            self.server.woods.add_to_woods(user, 60*60)
        self.server.woods.encounters["bs"][1](user.chat_id)
        text = (    "As you read the *Blacksmith Teleport Scroll* you start to feel a bit dizzy. You faint.\n"
                    "You had a weird dream where you step into a black hole and exited a white hole\n\n"
                    "You wake up at the blacksmith."
                )
        self.server.bot.send_message(text=text, chat_id=user.chat_id, parse_mode='MARKDOWN')

    def use_crs(self, user):
        old_weapon = user.weapon
        if old_weapon:
            if user.weapon.is_shared_and_equipped:       # Checa se a arma está compartilhada na party.
                user.weapon.is_shared_and_equipped = False

            user.weapon.unequip(user)
            user.weapon = None
        new_player = player.Player(user.chat_id)
        new_player.new_from_player(user)

        new_player.att_points["unspent"] = user.level - 1
        self.server.playersdb.players_and_parties[user.chat_id] = new_player
        if old_weapon:
            old_weapon.equip(self.server.playersdb.players_and_parties[user.chat_id])
        if user.pt_code:
            code = user.pt_code
            self.server.playersdb.players_and_parties[user.pt_code].leave_pt(user)
            self.server.playersdb.players_and_parties[code].join_pt(self.server.playersdb.players_and_parties[user.chat_id])
        text = "As you read the *Class Reset Scroll*, all the knowledge you gained was drained back to a vessel."
        self.server.bot.send_message(text=text, chat_id=user.chat_id, parse_mode='MARKDOWN')

    def show_market(self, caller, *args):
        text = "Welcome to the Player Market! Here you can trade talismans with other players using leaves!\n\n"
        text += "What do you want to do?\n\n"
        text += "Put your talismans for sale /sell_talismans\n"
        text += "Buy talismans /buy_talismans\n"
        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def generate_storage_text(self, user):
        # organizer = [{}, {}, {}, {}, {}, {}, {}]
        # for item in user.storage:
        #     if item.code in organizer[item.rarity]:
        #         organizer[item.rarity][item.code][1] += 1
        #     else:
        #         organizer[item.rarity][item.code] = [item, 1]
        organizer = copy.copy(user.storage.talismans)
        text = ""
        r = 0
        for rarity in organizer:
            if rarity:
                for code,item in rarity.items():
                    text += emojize(f"(x{item[1]}) *{item[0]}* /s_{r}_{code}\n")
                text += "\n"
            r += 1
        text = text.replace("_", "\\_")
        return [text, organizer]

    def sell_talismans(self, caller, *args):
        if not args:
            text = emojize("Here you can sell your talismans for leaves :leaf_fluttering_in_wind:!\n\n")
            text += "Talismans you have for sale:\n\n"
            text += self.server.shop.show_talismans_for_sale(caller.chat_id)
            text += "To remove them of sale, use the /r\_code\n\n"
            text += "To sell talismans click on the codes below:\n\n"
            storage = self.generate_storage_text(caller)
            text += storage[0]
            self.server.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
            self.phase_organizer[caller.chat_id] = {"phase":1, "chat_id":caller.chat_id, "talisman_code":"", "organizer":storage[1], "sell_qty":0}
            return self.def_wait_time*2
        else:
            if caller.chat_id in self.phase_organizer:
                if args[-1].startswith("/s_"):
                    if self.phase_organizer[caller.chat_id]["phase"] == 1:

                        code = args[-1][3:]
                        self.phase_organizer[caller.chat_id]["talisman_code"] = code
                        rarity = int(code[0])
                        t_code = code[2:]
                        found = False
                        text = ""
                        for r in caller.storage.talismans:
                            for tal_code, tal in r.items():
                                if code == f"{tal[0].rarity}_{tal[0].code}":
                                    text += tal[0].generate_description()
                                    found = True
                                    break
                        if not found:
                            text = "You dont have that talisman"
                            self.server.bot.send_message(text=text, chat_id=caller.chat_id)

                        else:
                            text += "\n\n"
                            text += "How many of that talisman you want to sell?\n\n"
                            text += f"0 - {self.phase_organizer[caller.chat_id]['organizer'][rarity][t_code][1]}?"
                            self.phase_organizer[caller.chat_id]["phase"] += 1
                            self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        return self.def_wait_time*2
                elif args[-1].startswith("/r_"):
                    code = args[-1][3:]
                    found = False
                    r = 0
                    for rarity in self.server.shop.items_for_sale:
                        for tal_code, prices in rarity.items():
                            for price, offers in prices.items():
                                o = 0
                                for offer in offers:
                                    if caller.chat_id == offer[0]:
                                        if code == f"{r}_{tal_code}":
                                            # long boi
                                            found = True
                                            for n in range(offer[1]):
                                                drop = copy.deepcopy(self.Talismandb.talismans[tal_code])

                                                original_rarity = drop.rarity
                                                drop.rarity = r
                                                rarity_up = r-original_rarity
                                                # print(f"rarity_up = {rarity_up}, drop.rarity: {drop.rarity}")
                                                # print("---------------------")
                                                for power_name, power in drop.powers.items():
                                                    drop.powers[power_name] = power*(rarity_up + 1)
                                                caller.storage.append(drop)

                                            del self.server.shop.items_for_sale[r][tal_code][price][o]
                                            break
                                    if found:
                                        break
                                    o += 1
                            if found:
                                break
                        if found:
                            break
                        r += 1

                    if found:
                        text = "Ok, talismans are now back at your /sto!"
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup = self.server.keyboards.forest_return_reply_markup)
                        return self.def_wait_time*2
                    else:
                        text = "You don't have that talisman."
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup = self.server.keyboards.forest_return_reply_markup)
                        return self.def_wait_time*2
                if self.phase_organizer[caller.chat_id]["phase"] == 2:
                    try:
                        code = self.phase_organizer[caller.chat_id]["talisman_code"]
                        rarity = int(code[0])
                        t_code = code[2:]
                        qty = max(min(int(args[-1]), self.phase_organizer[caller.chat_id]['organizer'][rarity][t_code][1]),0)

                    except ValueError:
                        text = "Please input a number."
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        return self.def_wait_time*2
                    text = f"Are you sure you want to sell {qty} of:\n\n"
                    for r in caller.storage.talismans:
                        for tal_code, tal in r.items():
                            if f"{code}" == f"{tal[0].rarity}_{tal[0].code}":
                                text += tal[0].generate_description()
                                break
                    self.phase_organizer[caller.chat_id]["sell_qty"] = qty
                    self.phase_organizer[caller.chat_id]["phase"] += 1
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup = self.server.keyboards.forest_return_reply_markup)
                    return self.def_wait_time*2
                if self.phase_organizer[caller.chat_id]["phase"] == 3:
                    if args[-1] == "yes":
                        self.phase_organizer[caller.chat_id]["phase"] += 1
                        text = "Great! How much leaves are going to be paid for your talismans?."
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')

                    elif args[-1] == "no":
                        text = "Ok. back to start menu"
                        text += emojize("Here you can sell your talismans for leaves :leaf_fluttering_in_wind:!\n\n")
                        text += "Talismans you have for sale:\n\n"
                        text += self.server.shop.show_talismans_for_sale(caller.chat_id)
                        text += "To sell talismans click on the codes below:\n\n"
                        storage = self.generate_storage_text(caller)
                        text += storage[0]
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
                        self.phase_organizer[caller.chat_id] = {"phase":1, "chat_id":caller.chat_id, "talisman_code":"", "organizer":storage[1], "sell_qty":0}

                    return self.def_wait_time*2
                if self.phase_organizer[caller.chat_id]["phase"] == 4:
                    try:
                        price = max(int(args[-1]),1)
                    except ValueError:
                        text = "Please input a number."
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        return self.def_wait_time*2
                    phase_organizer = self.phase_organizer[caller.chat_id]
                    code = phase_organizer["talisman_code"]


                    for number in range(phase_organizer["sell_qty"]):
                        i = 0
                        f = False
                        for r in caller.storage.talismans:
                            for tal_code, tal in r.items():
                                if f"{code}" == f"{tal[0].rarity}_{tal[0].code}":
                                    caller.storage.remove(tal[0])
                                    f = True
                                    break
                            if f:
                                break


                    # get ready
                    print(self.server.shop.items_for_sale[int(phase_organizer["talisman_code"] [0])])
                    if phase_organizer["talisman_code"][2:] in self.server.shop.items_for_sale[int(phase_organizer["talisman_code"] [0])]:
                        if str(price) in self.server.shop.items_for_sale[int(phase_organizer["talisman_code"] [0])] [phase_organizer["talisman_code"][2:]]:
                            # Caso o talismã ja exista no shop por esse preço

                            self.server.shop.items_for_sale[int(phase_organizer["talisman_code"] [0])] [phase_organizer["talisman_code"][2:]][str(price)].append([caller.chat_id, phase_organizer["sell_qty"]])
                            print(self.server.shop.items_for_sale[int(phase_organizer["talisman_code"] [0])] [phase_organizer["talisman_code"][2:]][str(price)])
                        else:
                            # Caso o talismã ja exista no shop mas não com esse preço

                            self.server.shop.items_for_sale[int(phase_organizer["talisman_code"] [0])] [phase_organizer["talisman_code"][2:]][str(price)] = [ [caller.chat_id, phase_organizer["sell_qty"]], ]
                            print(self.server.shop.items_for_sale[int(phase_organizer["talisman_code"] [0])] [phase_organizer["talisman_code"][2:]][str(price)])
                    else:
                        # Caso o este código não exista ainda no shop

                        self.server.shop.items_for_sale[int(phase_organizer["talisman_code"] [0])] [phase_organizer["talisman_code"][2:]] = {str(price):[ [caller.chat_id, phase_organizer["sell_qty"]], ]}
                        print(self.server.shop.items_for_sale[int(phase_organizer["talisman_code"] [0])] [phase_organizer["talisman_code"][2:]])
                    text = "Great! Your talismans are at the shop now. As soon as someone buys your talismans, you will recieve your leaves."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    del self.phase_organizer[caller.chat_id]
                    return False

        return False

    def buy_talismans(self, caller, *args):
        if not args:
            text = "Welcome to the Talisman Player Market!\n"
            text += "Here you can buy talismans from other players.\n"
            text += "To purchase a talisman, use the /p\_(code)\n\n"
            text += self.server.shop.generate_buy_text()
            self.phase_organizer[caller.chat_id] = {"phase":1, "chat_id":caller.chat_id, "talisman_code":"", "quantity":0, "talisman":None}
            self.server.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
            return self.def_wait_time*2

        else:
            if args[-1].startswith("/p_"):
                if self.phase_organizer[caller.chat_id]["phase"] == 1:

                    code = args[-1][3:]
                    self.phase_organizer[caller.chat_id]["talisman_code"] = code
                    text = "How many of that talisman would you like to purchase?"
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
                    self.phase_organizer[caller.chat_id]["phase"] += 1
                    return self.def_wait_time*2
            if caller.chat_id in self.phase_organizer:
                if self.phase_organizer[caller.chat_id]["phase"] == 2:
                    try:
                        qty = max(int(args[-1]), 0)

                    except ValueError:
                        text = "Please input a number."
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        return self.def_wait_time*2
                    self.phase_organizer[caller.chat_id]["quantity"] = qty
                    drop = copy.deepcopy(self.Talismandb.talismans[self.phase_organizer[caller.chat_id]["talisman_code"][2:]])
                    original_rarity = drop.rarity
                    drop.rarity = int(self.phase_organizer[caller.chat_id]["talisman_code"][0])
                    rarity_up = drop.rarity-original_rarity
                    # print(f"rarity_up = {rarity_up}, drop.rarity: {drop.rarity}")
                    # print("---------------------")
                    for power_name, power in drop.powers.items():
                        drop.powers[power_name] = power*(rarity_up + 1)
                    self.phase_organizer[caller.chat_id]["talisman"] = drop
                    text = f"Are you sure you want to purchase {qty} x {drop}?"
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN', reply_markup = self.server.keyboards.forest_return_reply_markup)
                    self.phase_organizer[caller.chat_id]["phase"] += 1
                    return self.def_wait_time*2
                if self.phase_organizer[caller.chat_id]["phase"] == 3:
                    if args[-1] == "yes":
                        phase_organizer = self.phase_organizer[caller.chat_id]
                        location = self.server.shop.items_for_sale[int(phase_organizer["talisman_code"][0])][phase_organizer["talisman_code"][2:]]
                        go_on = True
                        chosen_qty = phase_organizer["quantity"]
                        qty = 0
                        cost = 0
                        print(location)
                        while go_on:
                            found = False
                            found2 = False
                            lowest_price = -1

                            # Primeiro ele procura o menor preço

                            for price, offers in location.items():
                                print(offers)
                                if offers:
                                    if lowest_price == -1 or int(price) < lowest_price:
                                        found2=  True
                                        lowest_price = int(price)
                            if not found2:
                                go_on = False
                                break

                            # Depois naquele preço, ele compra tudo que tem antes de ir para o próximo.

                            while qty < chosen_qty:
                                i1 = 0
                                found = False
                                for offer in location[str(lowest_price)]:
                                    print(f"offer: {offer}")
                                    for i in range(chosen_qty - qty):
                                        time.sleep(1)
                                        print(f"caller.leaves:{caller.leaves} lowest_price: {lowest_price}")
                                        if caller.leaves >= lowest_price:
                                            found = True
                                            cost += lowest_price
                                            offer[1] -= 1
                                            qty += 1
                                            self.server.playersdb.players_and_parties[offer[0]].leaves += lowest_price
                                            caller.leaves -= lowest_price
                                            text2 = emojize(f"You've sold a talisman ({phase_organizer['talisman_code'][2:]}) for {lowest_price} leaves :leaf_fluttering_in_wind:")
                                            print(text2)
                                            self.server.bot.send_message(text=text2, chat_id=offer[0])
                                            if not offer[1]:
                                                del location[str(lowest_price)][i1]
                                                break
                                        else:
                                            go_on = False
                                            break
                                    if qty == chosen_qty:
                                        go_on = False
                                        break
                                    if not go_on:
                                        break
                                    i1 += 1
                                if not found:
                                    break
                                if qty == chosen_qty:
                                    go_on = False
                                    break
                                if not go_on:
                                    break

                            if qty == chosen_qty:
                                go_on = False
                                break
                            print(f"go_on: {go_on}, qty: {qty}, chosen_qty = {chosen_qty}, found = {found}, found2 = {found2}")
                            time.sleep(1)

                        for i in range(qty):
                            caller.storage.append(phase_organizer["talisman"])
                        text = emojize(f"You have sucessfully purchased {qty} x {phase_organizer['talisman']} for a total of {cost} leaves :leaf_fluttering_in_wind:")
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')

                        return False


                    elif args[-1] == "no":
                        text = "Ok! back at the start!\n"
                        text += "Welcome to the Talisman Player Market!\n"
                        text += "Here you can buy talismans from other players.\n"
                        text += "To purchase a talisman, use the /p\_(code)\n\n"
                        text += self.server.shop.generate_buy_text()
                        self.phase_organizer[caller.chat_id] = {"phase":1, "chat_id":caller.chat_id, "talisman_code":"", "quantity":0, "talisman":None}
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
                        return self.def_wait_time*2


        return False

    def purchase_leaves(self, caller, *args):
        text = "To gain leaves, you can back us on Patreon! https://www.patreon.com/Clini. You will receive your leaves each start of the month (as soon as patreons charges)."
        self.server.bot.send_message(text=text, chat_id=caller.chat_id)

        return False

    def to(self, chat_id):
        if chat_id in self.phase_organizer:
            del self.phase_organizer[chat_id]

    def to2(self, chat_id):
        pass
