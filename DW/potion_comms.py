from emoji import emojize
import copy

class PotionComms:
    def __init__(self, server):
        self.server = server
        self.def_wait_time = 60
        self.actions = {
            "/pots": self.pots,
        }
        self.internal = {

        }

    def generate_pot_text(self, user):
        text = "Here are your potions:\n\n"
        for pot_code,pots in user.pocoes.items():
            if pots:
                text += f"(X{len(pots)}) {pots[-1].name} /{pot_code}\n"
        text += "\n"
        text += "To create potions, use /craft_pots. To use the potions, use the /code of the potion you want to drink."
        self.server.bot.send_message(text=text, chat_id = user.chat_id)

    def pots(self, caller, *args):
        if not args:
            self.generate_pot_text(caller)
            return self.def_wait_time*2
        else:
            a = args[-1]
            is_drinking = False
            for pot_code,pots in caller.pocoes.items():
                if pots:
                    if a == f"/{pots[-1].code}":
                        if pots[-1].code == "1c":
                            self.f_return(caller)
                        else:
                            pots[-1].action(caller)
                        del pots[-1]
                        is_drinking = True
                        break

            if a == "/craft_pots":
                if caller.location == "camp":
                    text = self.server.potionsdb.show_recipes()
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return self.def_wait_time*2
                else:
                    text = "You need to be at camp to brew potions."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return False
            if caller.location == "camp":
                if a.startswith("/c_"):
                    carrinho = copy.deepcopy(self.server.potionsdb.potiondb[a[3:]].recipe)
                    for tal_code,qty in carrinho.items():
                        carrinho[tal_code] = 0
                    for tal_codes, qty in self.server.potionsdb.potiondb[a[3:]].recipe.items():
                        for rar in caller.storage.talismans:
                            if tal_codes in rar:
                                carrinho[tal_codes] += rar[tal_codes][1]
                    if self.check_if_can_brew(carrinho, self.server.potionsdb.potiondb[a[3:]].recipe):
                        new_pot = copy.deepcopy(self.server.potionsdb.potiondb[a[3:]])
                        user = caller
                        for material,qty in self.server.potionsdb.potiondb[a[3:]].recipe.items():
                            numbers_to_remove = qty
                            for rarity in range(len(user.storage.talismans)):
                                for tal_code, tal in user.storage.talismans[rarity].items():
                                    if tal[0].code == material:
                                        if user.storage.talismans[rarity][tal_code][1] > numbers_to_remove:
                                            user.storage.talismans[rarity][tal_code][1] -= numbers_to_remove
                                            break
                                        else:
                                            numbers_to_remove -= user.storage.talismans[rarity][tal_code][1]
                                            del user.storage.talismans[rarity][tal_code]
                                            if not numbers_to_remove:
                                                break
                            # to_remove = []
                            # index = 0
                            # while numbers_to_remove > 0 and index < len(user.storage):
                            #     item = user.storage[index]
                            #     if item.code == material:
                            #         to_remove.append(item)
                            #         numbers_to_remove -= 1
                            #     index += 1
                            # for item in to_remove:
                            #     for item2 in range(len(caller.storage)):
                            #         if item.rarity == caller.storage[item2].rarity and item.code == caller.storage[item2].code:
                            #             del self.server.playersdb.players_and_parties[caller.chat_id].storage[item2]
                            #             new_pot.power += item.rarity
                            #             break
                        print(new_pot.power)
                        if not a[3:] in caller.pocoes:
                            caller.pocoes[a[3:]] = []
                        caller.pocoes[a[3:]].append(new_pot)
                        text = f"Succesfully crafted a {new_pot.name} potion!"
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        return self.def_wait_time*2
                    else:
                        text = "You don't have enough talismans to craft this potion."
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        return self.def_wait_time*2
            elif not is_drinking and a.startswith("/c_"):
                text = "I SAID: YOU NEED TO BE AT CAMP TO BREW THE GODDAMN POTIONS!"
                self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                return False
            return self.def_wait_time*2

    def f_return(self, user):
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
            user.calc_attributes()

        # if user.chat_id in self.server.caverns_manager.jogs:
        #     self.server.caverns_manager.leave(user.chat_id)

        # if chat_id in self.server.blacksmith.bs_in_progress:
        #     pass

        if user.chat_id in self.server.woods.players:
            self.server.woods.exit_woods(user.chat_id)

        if user.location != "camp":
            print(user.location)
            user.location = "camp"

        text = (    "As you drink the *Campfire RecAll Potion* you start to feel a bit dizzy. You faint.\n"
                    "You had a weird dream where you step into a black hole and exited a white hole\n\n"
                    "You wake up at the campfire."
                )
        self.server.bot.send_message(text=text, chat_id=user.chat_id, parse_mode='MARKDOWN')

    def check_if_can_brew(self, carrinho, recipe):
        for item,qty in carrinho.items():
            if qty < recipe[item]:
                return False
        return True

    def to(self, chat_id):
        pass

    def to2(self, chat_id):
        pass
