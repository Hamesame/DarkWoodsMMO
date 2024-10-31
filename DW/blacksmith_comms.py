########################################
# Classe que contém os comandos do BS  #
########################################

import items
import random as rd
from emoji import emojize
import telegram
import bot
import copy


class BlacksmithComms:
    '''
        Classe dos comandos do blacksmith.
    '''
    def __init__(self, server):
        self.bot = bot.TGBot()          # Bot pra mandar mensagens
        self.server = server            # O jogo inteiro
        self.defkb = server.defkb       # O keyboard padrão
        self.def_wait_time = 60         # 1 minuto

        self.actions = {}
        self.internal = {
            "forge_weapon": self.bs_proc,   # Comando interno que só é ativado quando o jogador acha o bs
            "start_bs": self.bs_user_interface,
            "forge_armor": self.forge_armor,
            "infuse_manager": self.infuse_manager,

        }
        self.possible_armors = {
            emojize("Simple Clothes"): [(1, emojize("Fur"), 3)],
            emojize("Winter Clothes"): [(2, emojize("Fur"), 5),(2, emojize("Gelatine :custard:"), 5),(1, emojize("Leather"), 2)],
            emojize("Waterproof Winter Clothes"): [(3, emojize("Fur"), 10), (3, emojize("Gelatine :custard:"), 10), (3, emojize("Feather"), 10)],
            emojize("Full Sweatshirt Set"): [(4, emojize("Fur"), 30), (4, emojize("Gelatine :custard:"), 10), (4, emojize("Feather"), 10), (4, emojize("Cobweb :spider_web:"), 3)],

            }
        self.rarity_list = [
            emojize(":zzz:"),
            emojize(":pile_of_poo:"),
            emojize(":OK_hand:"),
            emojize(":flexed_biceps:"),
            emojize(":angry_face_with_horns:"),
            emojize(":smiling_face_with_halo:"),
            emojize(":bright_button:"),
        ]

    # def storage_append(self, storage):
    #     '''
    #         storage (list): Lista do storage do jogador. Não iremos modificar, retornaremos uma outra lista.
    #         storage example: [{"item_code": [item_object, number_of_objects]}, {}, {}, {}, {}, {}, {}]
    #     '''
    #     for item in storage:
    #         found_item = False
    #         for storaged_item_code in user.storage[item.rarity]:
    #             if storaged_item_code == item.code:
    #                 user.storage[item.rarity][storaged_item_code][1] += 1
    #                 found_item = True
    #                 break
    #         if not found_item:
    #             user.storage[item.rarity][item.code] = [item, 1]



    def print_possible_armors(self, chat_id):
        def storage_organizer(user_storage):
            '''
                Organizer do storage. Retorna os itens organizados por raridade e por código.
            '''
            # organizer = [{}, {}, {}, {}, {}, {}, {}]
            # for item in user_storage:
            #     if item.code in organizer[item.rarity]:
            #         organizer[item.rarity][item.code][1] += 1
            #     else:
            #         organizer[item.rarity][item.code] = [item, 1]
            organizer = user_storage.talismans

            return organizer

        def search_material(storage, bs_material):
            player_quantity = 0
            rarity_index = 0
            for rarity in storage:
                if rarity_index >= bs_material[0]:
                    for item_code, item in rarity.items():
                        if item[0].name == bs_material[1]:
                            player_quantity += item[1]
                rarity_index += 1
            return player_quantity

        def generate_armor_name_display(user_storage, armor_name):
            text = ""
            text = f"{armor_name}\n\n"
            text += "Materials needed:\n"

            for material in self.possible_armors[armor_name]:
                text += f"{self.rarity_list[material[0]]} {material[1]} or higher: x{search_material(user_storage, material)}/{material[2]}\n"

            text += "\n"
            return text

        def check_armors_that_can_be_crafted(storage):
            can_craft_list = []
            for armor in self.possible_armors:
                can_craft = True
                for material in self.possible_armors[armor]:
                    if search_material(storage, material) < material[2]:
                        can_craft = False
                        break
                if can_craft:
                    can_craft_list.append(armor)
            return can_craft_list

        user = self.server.playersdb.players_and_parties[chat_id]
        user_storage = storage_organizer(user.storage)
        display_text = "Armors that can be craft: \n\n\n"

        for armor in self.possible_armors:
            display_text += f"{generate_armor_name_display(user_storage, armor)}"

        player_can_craft_list = check_armors_that_can_be_crafted(user_storage)
        player_can_craft_list.append(emojize(":BACK_arrow: Back :BACK_arrow:"))

        can_craft_keyboard = self.server.keyboards.create_keyboard_from_list(player_can_craft_list)

        display_text = display_text.replace("_", "\\_")
        self.server.bot.send_message(text = display_text, chat_id = chat_id, parse_mode='MARKDOWN', reply_markup = can_craft_keyboard)

    def forge_armor(self, caller, caller_id = None, *args):
        def storage_organizer(user_storage):
            '''
                Organizer do storage. Retorna os itens organizados por raridade e por código.
            '''
            # organizer = [{}, {}, {}, {}, {}, {}, {}]
            # for item in user_storage:
            #     if item.code in organizer[item.rarity]:
            #         organizer[item.rarity][item.code][1] += 1
            #     else:
            #         organizer[item.rarity][item.code] = [item, 1]
            organizer = user_storage.talismans

            return organizer
        def search_material(storage, bs_material):
            player_quantity = 0
            rarity_index = 0
            for rarity in storage:
                if rarity_index >= bs_material[0]:
                    for item_code, item in rarity.items():
                        if item[0].name == bs_material[1]:
                            player_quantity += item[1]
                rarity_index += 1
            return player_quantity
        def check_armors_that_can_be_crafted(storage):
            can_craft_list = []
            for armor in self.possible_armors:
                can_craft = True
                for material in self.possible_armors[armor]:
                    if search_material(storage, material) < material[2]:
                        can_craft = False
                        break
                if can_craft:
                    can_craft_list.append(armor)
            return can_craft_list
        def remove_materials(chat_id, armor_name):
            user = self.server.playersdb.players_and_parties[chat_id]
            for material in self.possible_armors[armor_name]:
                numbers_to_remove = material[2]
                index = 0
                for rarity in range(len(user.storage.talismans)):
                    if rarity >= material[0]:
                        for tal_code, tal in user.storage.talismans[rarity].items():
                            if tal[0].name == material[1]:
                                if user.storage.talismans[rarity][tal_code][1] > numbers_to_remove:
                                    user.storage.talismans[rarity][tal_code][1] -= numbers_to_remove
                                    break
                                else:
                                    numbers_to_remove -= user.storage.talismans[rarity][tal_code][1]
                                    del user.storage.talismans[rarity][tal_code]
                                    if not numbers_to_remove:
                                        break
                # while numbers_to_remove > 0 and index < len(user.storage):
                #     item = user.storage[index]
                #     if item.name == material[1]:
                #         if item.rarity >= material[0]:
                #             to_remove.append(item)
                #             numbers_to_remove -= 1
                #     index += 1
                # for item in to_remove:
                #     for item2 in range(len(self.server.playersdb.players_and_parties[chat_id].storage)):
                #         if item.rarity == self.server.playersdb.players_and_parties[chat_id].storage[item2].rarity and item.code == self.server.playersdb.players_and_parties[chat_id].storage[item2].code:
                #             del self.server.playersdb.players_and_parties[chat_id].storage[item2]
                #             break

        chat_id = caller.chat_id
        if not args:
            self.print_possible_armors(chat_id)
            return self.def_wait_time*5

        else:
            if args[-1] == emojize(":BACK_arrow: Back :BACK_arrow:"):
                self.server.helper.append_command("start_bs", chat_id)
                return False
                # codar o menu principal do bs. Tem que retornar na função.

            text = ""
            user = self.server.playersdb.players_and_parties[chat_id]

            armor_name = args[-1]
            user_storage = storage_organizer(self.server.playersdb.players_and_parties[chat_id].storage)
            if armor_name in check_armors_that_can_be_crafted(user_storage):
                if armor_name in self.possible_armors:
                    armor = copy.deepcopy(self.server.itemsdb.possible_armors[armor_name])
                    self.server.playersdb.players_and_parties[chat_id].inventory.append(copy.deepcopy(armor))

                    remove_materials(chat_id, armor_name)
                    text = f"A {armor_name} was added to your inventory!"
                    self.print_possible_armors(chat_id)

                else:
                    text = "The blacksmith does not know this armor."
                    self.print_possible_armors(chat_id)
            else:
                text = f"You do not have the items to craft {armor_name}"
            text = text.replace("_", "\\_")
            self.server.bot.send_message(text = text, chat_id = chat_id, parse_mode='MARKDOWN')

            return self.def_wait_time*5

        return False

    def Infuse_step_1(self, chat_id, *args):
        user = self.server.playersdb.players_and_parties[chat_id]
        if not args:
            text = "Choose a weapon to apply talismans.\n\n"
            if user.weapon:
                text += f"Equipped weapon: {user.weapon} /e_{user.weapon.code}\n\n"
            for arma in user.inventory:
                if arma.type == "Weapon":
                    text += f"{arma} /e_{arma.code}\n"
            text = text.replace("_", "\\_")
            back_button = [emojize(":BACK_arrow: Back :BACK_arrow:")]
            back_button_keyboard = self.server.keyboards.create_keyboard_from_list(back_button)
            self.server.bot.send_message(text = text, chat_id = chat_id, parse_mode='MARKDOWN', reply_markup = back_button_keyboard)
            return self.def_wait_time*5

        else:
            if args[-1] == emojize(":BACK_arrow: Back :BACK_arrow:"):
                self.server.helper.append_command("start_bs", chat_id)
                # Retorne o passo anterior.
                return False
            found_weapon = False
            can_be_infused = False
            if self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] == 0:
                weapon_code = args[-1][3:]

                for arma in user.inventory:
                    if arma.code == weapon_code:
                        found_weapon = True
                        n_a = copy.deepcopy(arma)

                        for tal_name, tal in arma.talismans.items():
                            user.storage.append(copy.deepcopy(tal))

                        n_a.remove_talismans()

                        self.server.blacksmith.bs_in_progress[chat_id] = {
                            "weapon": n_a,
                            "talismans": [],
                            "bs_stage": 1,
                            "simulated_player_storage": copy.deepcopy(user.storage),
                        }
                        can_be_infused = True
                text = ""
                back_button = [emojize(":BACK_arrow: Back :BACK_arrow:")]
                back_button_keyboard = self.server.keyboards.create_keyboard_from_list(back_button)
                if not found_weapon:
                    text = "Weapon not found. Try again!"
                else:
                    if not can_be_infused:
                        text = "Your weapon is already stacked af dude, stop please, it can't handle it anymore!"
                if text:
                    self.server.bot.send_message(text = text, chat_id = chat_id, reply_markup = back_button_keyboard)
            if found_weapon and can_be_infused:
                result = self.Infuse_step_2(chat_id)
                return result
            else:
                return self.def_wait_time*5
        return False

    def Infuse_step_2(self, chat_id, *args):
        def generate_storage_text(user):
            # organizer = [{}, {}, {}, {}, {}, {}, {}]
            # for item in user.storage:
            #     if item.code in organizer[item.rarity]:
            #         organizer[item.rarity][item.code][1] += 1
            #     else:
            #         organizer[item.rarity][item.code] = [item, 1]
            text = ""
            organizer = user.storage.talismans
            r = 0
            for rarity in organizer:
                if rarity:
                    for code, item in rarity.items():
                        text += emojize(f"(x{item[1]}) *{item[0]}* /d_{r}_{code}\n")
                    text += "\n"
                r += 1
            return text

        user = self.server.playersdb.players_and_parties[chat_id]
        if not args:
            text = f"Choose the talismans you would like to apply! (Click the code to add)\n\n"
            text += f"Chosen weapon: {self.server.blacksmith.bs_in_progress[chat_id]['weapon']}\n\n\n"
            text += generate_storage_text(user)

            text = text.replace("_", "\\_")
            back_button = [emojize(":BACK_arrow: Back :BACK_arrow:")]
            back_button_keyboard = self.server.keyboards.create_keyboard_from_list(back_button)
            self.server.bot.send_message(text = text, chat_id = chat_id, parse_mode='MARKDOWN', reply_markup = back_button_keyboard)
            return self.def_wait_time*5

        else:

            # if args[-1] == emojize(":BACK_arrow: Back :BACK_arrow:"):
            #     self.server.blacksmith.bs_in_progress[chat_id]["weapon"] = None
            #     self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] = 0
            #     return self.def_wait_time
            #     # Retorne o passo anterior.
            if args[-1] == "Done" or args[-1] == emojize(":BACK_arrow: Back :BACK_arrow:"):
                self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] = 2
                result = self.Infuse_talismans(chat_id)
                return result

            text = ""
            can_add = True
            if len(self.server.blacksmith.bs_in_progress[chat_id]["talismans"]) >= 5:
                text = "If you try to add more, you're gonna overflow the game. Please stop.\n\n"
                can_add = False
            talism_code = args[-1][5:]
            rarity = args[-1][3]

            have_talism = False
            if can_add:
                r = 0
                for rar in self.server.blacksmith.bs_in_progress[chat_id]["simulated_player_storage"].talismans:

                    if str(r) == rarity:
                        for tal_code, tal in rar.items():
                            if tal_code == talism_code:
                                repeated = False
                                for item2 in self.server.blacksmith.bs_in_progress[chat_id]["talismans"]:
                                    if item2.code == talism_code:
                                        repeated = True
                                        break
                                if not repeated:
                                    item = tal[0]
                                    self.server.blacksmith.bs_in_progress[chat_id]["talismans"].append(item)
                                    have_talism = True
                                    self.server.blacksmith.bs_in_progress[chat_id]["simulated_player_storage"].remove(item)
                                    break
                                else:
                                    text += "You already put that talisman on the weapon. no repetitions allowed! Try Again.\n\n"
                                    break
                    r += 1
                if not have_talism:
                    text += "You doesn't seem that you have that talisman. Try again.\n\n"

            text += f"Chosen weapon: {self.server.blacksmith.bs_in_progress[chat_id]['weapon']}\n\n"
            text += f"Chosen talismans:\n"

            for talisman in self.server.blacksmith.bs_in_progress[chat_id]["talismans"]:
                s = f"|{self.rarity_list[talisman.rarity]}| {talisman.name}\n"
                text += s
            text += "\n\n"

            text += "When done, press Done."

            text = text.replace("_","\\_")
            custom_keyboard_list = ["Done", emojize(":BACK_arrow: Back :BACK_arrow:")]
            custom_keyboard = self.server.keyboards.create_keyboard_from_list(custom_keyboard_list)

            self.server.bot.send_message(text = text, chat_id = chat_id, parse_mode='MARKDOWN', reply_markup = custom_keyboard)

            return self.def_wait_time*5

        return False

    def Infuse_talismans(self, chat_id):
        user = self.server.playersdb.players_and_parties[chat_id]
        chosen_weapon = None
        for weapon in user.inventory:
            if weapon.code == self.server.blacksmith.bs_in_progress[chat_id]["weapon"].code:
                chosen_weapon = weapon
                break
        is_eq_wep = False
        if user.weapon and user.weapon.code == chosen_weapon.code:
            user.weapon.unequip(user)
            user.weapon = None        # Desequipa o item.
            user.calc_attributes()        # Atualiza os status do player
            is_eq_wep = True

        text = "Your weapon was applied with talismans."
        chosen_weapon.remove_talismans()
        chosen_weapon.add_talismans(self.server.blacksmith.bs_in_progress[chat_id]["talismans"])
        if chosen_weapon.name == emojize("alien puzzle :alien_monster:"):
            for tal in self.server.blacksmith.bs_in_progress[chat_id]["talismans"]:
                if tal.code == "helios_puzzle" or tal.code == "cosmic_gift":
                    text += emojize("\nAlso, your alien puzzle :alien_monster: ticked while the Helios Puzzle engaged gears with it.")
                    break
        if is_eq_wep:
            chosen_weapon.action(user)
            user.calc_attributes()
        # chosen_weapon = self.server.blacksmith.bs_in_progress[chat_id]["weapon"]
        for talisman in self.server.blacksmith.bs_in_progress[chat_id]["talismans"]:
            user.storage.remove(talisman)
            # for item in range(len(user.storage)):
            #     if user.storage[item].code == talisman.code and user.storage[item].rarity == talisman.rarity:
            #         del user.storage[item]# Se der pau, tem que procurar os talismans no storage também.
            #         break


        self.server.bot.send_message(text = text, chat_id = chat_id)

        self.server.blacksmith.bs_in_progress[chat_id] = {}
        self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] = 0

        result = self.infuse_manager(user)
        return result

    def infuse_manager(self, caller, caller_id = None, *args):
        chat_id = caller.chat_id
        bs_stage = self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"]
        result = False
        if not args:
            if bs_stage == 0:
                result = self.Infuse_step_1(chat_id)
            elif bs_stage == 1:
                result = self.Infuse_step_2(chat_id)
            elif bs_stage == 2:
                result = self.Infuse_talismans(chat_id)
        else:
            if bs_stage == 0:
                result = self.Infuse_step_1(chat_id, *args)
            elif bs_stage == 1:
                result = self.Infuse_step_2(chat_id, *args)

        return result


    def bs_user_interface(self, caller, caller_id = None, *args):
        if caller.chat_id in self.server.woods.players:
            self.server.woods.players[caller.chat_id]["active"] = False
        if caller.chat_id in self.server.deep_forest_manager.jogs:
            self.server.deep_forest_manager.jogs[caller.chat_id].active = False
        chat_id = caller.chat_id
        if not args:
            self.server.blacksmith.bs_in_progress[chat_id] = {"bs_stage": 0}
            text = "Welcome to the blacksmith. What would you like to do?"
            self.server.playersdb.players_and_parties[caller.chat_id].location = "blacksmith"
            self.server.bot.send_message(text = text, chat_id = chat_id, reply_markup = self.server.keyboards.bs_keyboard_reply_markup)
            return self.def_wait_time*5 + 60*caller.suc_refs

        else:
            if caller.chat_id in self.server.woods.players:
                self.server.woods.players[caller.chat_id]["active"] = False
            if caller.chat_id in self.server.deep_forest_manager.jogs:
                self.server.deep_forest_manager.jogs[caller.chat_id].active = False
            comm = args[-1]
            if comm == emojize("Exit"):
                text = "Ok, bye :)"
                self.server.bot.send_message(text = text, chat_id = chat_id, reply_markup = self.defkb)
                if caller.chat_id in self.server.woods.players:
                    self.server.woods.players[caller.chat_id]["active"] = True
                    self.server.playersdb.players_and_parties[caller.chat_id].location = "forest"
                if caller.chat_id in self.server.deep_forest_manager.jogs:
                    self.server.deep_forest_manager.jogs[caller.chat_id].active = True
                    self.server.playersdb.players_and_parties[caller.chat_id].location = "deep_forest"


            elif comm == emojize("Forge Weapon"):
                self.server.blacksmith.bs_in_progress[chat_id] = {
                    "bs_inv": [],
                    "wep_name": "",
                    # "wep_type": "",
                    # "wep_description": "",
                    "bs_stage": 0
                }
                # text = "Coming soon (need to adapt the old code)"
                # self.server.bot.send_message(text = text, chat_id = chat_id, reply_markup = self.bs_keyboard_reply_markup)
                self.server.helper.append_command("forge_weapon", chat_id)


            elif comm == emojize("Forge Armor"):
                self.server.helper.append_command("forge_armor", chat_id)

            elif comm == emojize("Apply talismans"):
                self.server.helper.append_command("infuse_manager", chat_id)

            else:
                text = "Chose something valid you dummy."
                self.server.bot.send_message(text = text, chat_id = chat_id, reply_markup = self.server.keyboards.bs_keyboard_reply_markup)
                return self.def_wait_time*5

        return False

    def print_bs_value(self, chat_id):
        '''
            Função que vai printar todas as armas do jogador, as armas do blacksmith e o valor de cada arma e o valor total das armas que vc colocou no blacksmith.

            Parâmetros:
                chat_id (str): chat id do usuario de telegram que achou o blacksmith
        '''
        s = ("Welcome to the shop, you can use the equip command to add weapons to my workshop, "
             "so i can merge them into one. But be careful, the total stats of your new weapon is "
             "going to be divided by 2. Beware. If your weapon have talismans <b>they are going to be removed before the forging</b>. "
             "So, the weapon will have less than or equal stats than half the total."
             "To throw all items to the workshop, use /all. \n\n")
        total_val = 0
        for arma in self.server.blacksmith.bs_in_progress[chat_id]["bs_inv"]:
            val = arma.atributos[0]+arma.atributos[1]                           # O valor é a soma do ataque e a defesa da arma
            total_val += val
            s += "<b>" + arma.name + "</b>" + " value = " + str(val) + " /r_" + arma.code + "\n"    # Neste caso é usado html pra n bugar com alguns nomes de armas

        s += "\n"
        s += f"Your stat coins: {self.server.playersdb.players_and_parties[chat_id].stat_points}\n"
        total_val += self.server.playersdb.players_and_parties[chat_id].stat_points
        s += "Total value = " + str(total_val) + "\n" + "If you are done, /done\n\n"

        for arma in self.server.playersdb.players_and_parties[chat_id].inventory:                                   # Após isto, ele mostra as armas no inventário do jogador
            s += ("<b>"+arma.name+"</b>" + emojize(" :crossed_swords: ") + str(arma.atributos[0]))
            s += emojize(" :shield: ") + str(arma.atributos[1]) + " /e_" + arma.code + "\n"

        self.bot.send_message(text=s, chat_id=chat_id, parse_mode=telegram.ParseMode.HTML)

    def bs_proc(self, caller, caller_id = None, *args):
        '''
            Função controladora do blacksmith. que vai direcionar o jogador para a função correta do blacksmith dependendo do estágio

            Parâmetros:
                caller (player): jogador que entrou no Blacksmith
                *args (tuple de str): args[-1] é a mensagem do jogador, se tiver uma.
        '''
        if caller.chat_id in self.server.woods.players:
            self.server.woods.players[caller.chat_id]["active"] = False
        if caller.chat_id in self.server.deep_forest_manager.jogs:
            self.server.deep_forest_manager.jogs[caller.chat_id].active = False
        chat_id = caller.chat_id
        result = False
        if args:
            if self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] == 0:
                result = self.bs_0(caller, *args)
            elif self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] == 1:
                result = self.bs_1(caller, *args)
            elif self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] == 2:
                result = self.bs_2(caller, *args)
            elif self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] == 3:
                result = self.bs_3(caller, *args)
            elif self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] == 4:
                result = self.bs_4(caller, *args)
            elif self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] == 5:
                result = self.bs_5(caller, *args)
        else:
            if chat_id in self.server.blacksmith.bs_in_progress:
                if self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] == 0:
                    result = self.bs_0(caller, emojize("YES :thumbs_up:"))
                elif self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] == 1:
                    result = self.bs_1(caller)
                elif self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] == 2:
                    result = self.bs_2(caller)
                elif self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] == 2:   # Nani
                    result = self.bs_0(caller)
            else:
                result = self.bs_0(caller, emojize("YES :thumbs_up:"))

        return result

    def bs_0(self, caller, *args):
        '''
            Primeira etapa do blacksmith. Em que é um encontro na floresta.
        '''
        chat_id = caller.chat_id
        if args:
            text = args[-1]
            if text == emojize("YES :thumbs_up:"):
                self.print_bs_value(chat_id)
                self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] = 1

                return 5*self.def_wait_time

            else:
                if caller.chat_id in self.server.woods.players:
                    self.server.woods.players[caller.chat_id]["active"] = True
                    self.server.playersdb.players_and_parties[caller.chat_id].location = "forest"
                if caller.chat_id in self.server.deep_forest_manager.jogs:
                    self.server.deep_forest_manager.jogs[caller.chat_id].active = True
                    self.server.playersdb.players_and_parties[caller.chat_id].location = "deep_forest"
                text = ("The blacksmith said:\nNo worries, one time you will be ready to craft"
                        " the greatest weapon of all time.")
                self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb)

                return False

        else:
            bs_reply_markup = self.server.keyboards.bs_reply_markup
            self.server.blacksmith.bs_in_progress[chat_id] = {
                "bs_inv": [],
                "wep_name": "",
                # "wep_type": "",
                # "wep_description": "",
                "bs_stage": 0
            }
            # self.print_bs_value(chat_id)
            text = emojize("In the forest you found a blacksmith, to whom you talked at length about your adventures."
                           " You were offered to trade in your weapons for a new one.\n*Do you accept the trade?*")
            self.bot.send_message(text=text, chat_id=chat_id, parse_mode='MARKDOWN', reply_markup=bs_reply_markup)

            return self.def_wait_time*5 + caller.suc_refs*60 # 1 minuto pra cada referência kk

    def bs_1(self, caller, *args):
        '''
            Segunda etapa do blacksmith, em que o jogador vai tacando as armas dele no bs até ele dar um /done
        '''
        chat_id = caller.chat_id
        if args:
            equip_text = args[-1]
            if equip_text[1] == "e":        # adicionar uma arma específica no inventário do bs
                for index in range(len(self.server.playersdb.players_and_parties[chat_id].inventory)):
                    if equip_text == "/e_"+self.server.playersdb.players_and_parties[chat_id].inventory[index].code:
                        self.server.blacksmith.bs_in_progress[chat_id]["bs_inv"].append(self.server.playersdb.players_and_parties[chat_id].inventory[index])
                        del self.server.playersdb.players_and_parties[chat_id].inventory[index]
                        break
                self.print_bs_value(chat_id)

            elif equip_text[1] == "r":      # retirar uma arma específica do inventário do bs
                bs_inv = self.server.blacksmith.bs_in_progress[chat_id]["bs_inv"]
                for index in range(len(bs_inv)):
                    if equip_text == "/r_"+bs_inv[index].code:
                        self.server.playersdb.players_and_parties[chat_id].inventory.append(bs_inv[index])
                        del self.server.blacksmith.bs_in_progress[chat_id]["bs_inv"][index]
                        break
                self.print_bs_value(chat_id)

            elif equip_text == "/all":      # adicionar todas as suas armas no inventário do bs
                if len(self.server.playersdb.players_and_parties[chat_id].inventory) > 0:
                    for arma in self.server.playersdb.players_and_parties[chat_id].inventory:
                        self.server.blacksmith.bs_in_progress[chat_id]["bs_inv"].append(arma)
                    self.server.playersdb.players_and_parties[chat_id].inventory = []
                self.print_bs_value(chat_id)

            elif equip_text == "/done":     # acabou e passa pra próxima etapa
                self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] = 2
                text = ("Please, name this godly creation that will sunder the heavens and slay a thousand enemies!"
                        " There is no character limit and it can contain emojis. *Careful, only one chance!!!"
                        "* You have 5 minutes.")
                self.bot.send_message(text=text, parse_mode='MARKDOWN', chat_id=caller.chat_id)

            else:
                text = "Command not recognized"
                self.bot.send_message(text=text, chat_id=chat_id)
                self.print_bs_value(chat_id)

            return 5*self.def_wait_time

        else:
            text = "Ok then, give me any number of artifacts you like and I'll see what I can do, you have 5 minutes"
            self.bot.send_message(text=text, chat_id=chat_id)

            return self.def_wait_time*5

    def bs_2(self, caller, *args):
        '''
            Terceira etapa do blacksmith emq ue o jogador fala o nome da arma

        '''
        chat_id = caller.chat_id
        if args:
            nome = args[-1]
            if len(nome) > 128:
                nome = nome[:128]
            self.server.blacksmith.bs_in_progress[chat_id]["bs_wep_name"] = nome
            self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] = 3

            text = "Very good name!\nThis weapon is going to be a melee weapon, a magical weapon or a ranged weapon? *You have 5 minutes.*"
            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup = self.server.keyboards.bs_type_custom_keyboard, parse_mode = 'MARKDOWN')

            return self.def_wait_time*5

        else:
            text = ("Please, name this godly creation that will sunder the heavens and slay a thousand enemies!"
                    " The character limit is 128 and it can contain emojis. *Careful, only one chance!!!"
                    "* You have 5 minutes.")
            self.bot.send_message(text=text, parse_mode='MARKDOWN', chat_id=caller.chat_id)

            return self.def_wait_time*5

    def bs_3(self, caller, *args):
        '''
            Quarta etapa em que o jogador fala se a arma será melee, mágica ou ranged
        '''
        chat_id = caller.chat_id
        if not args:
            text = "Very good name!\nThis weapon is going to be a melee weapon, a magical weapon or a ranged weapon? *You have 5 minutes.*"
            self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode='MARKDOWN', reply_markup = self.server.keyboards.bs_type_custom_keyboard)
            return self.def_wait_time*5
        else:
            tipo = args[-1]
            worked = True
            if tipo == emojize(":crossed_swords: Melee :crossed_swords:"):
                tipo2 = "melee"
            elif tipo == emojize(":crystal_ball: Magic :crystal_ball:"):
                tipo2 = "magic"
            elif tipo == emojize(":bow_and_arrow: Ranged :bow_and_arrow:"):
                tipo2 = "ranged"
            else:
                worked = False
            if worked:
                self.server.blacksmith.bs_in_progress[chat_id]["wep_type"] = tipo2
                self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] = 4
                text = f"Perfect! A {tipo2} weapon. Now type a description for it. *You have 15 minutes*"
                self.bot.send_message(text = text, chat_id = chat_id, parse_mode = "MARKDOWN")
                return self.def_wait_time*15
            else:
                text = "Please, come again? This weapon is going to be a melee weapon, a magical weapon or a ranged weapon? *You have 5 minutes.*"
                self.bot.send_message(text = text, chat_id = chat_id, parse_mode = "MARKDOWN", reply_markup = self.server.keyboards.bs_type_custom_keyboard)
                return self.def_wait_time*5

    def bs_4(self, caller, *args):
        chat_id = caller.chat_id
        if not args:
            text = f"Perfect! A {self.server.blacksmith.bs_in_progress[chat_id]['wep_type']} weapon. Now type a description for it. *You have 15 minutes*"
            self.bot.send_message(text = text, chat_id = chat_id, parse_mode = "MARKDOWN")
            return self.def_wait_time*15
        else:
            description = args[-1]
            self.server.blacksmith.bs_in_progress[chat_id]["wep_des"] = description
            self.server.blacksmith.bs_in_progress[chat_id]["bs_stage"] = 5
            text = ("Ah, what a fine piece. What would ye shout to summon this weapon?(no spaces or special symbols) I'll give ye 5 minutes to decide.")
            self.bot.send_message(text=text, chat_id=caller.chat_id)
            return self.def_wait_time*5

    def bs_5(self, caller, *args):
        '''
            Quarta etapa do blackmith em que o jogador fala o código da arma e recebe ela.

        '''
        chat_id = caller.chat_id
        if args:
            code = args[-1]
            # done = False
            # i = 0
            # while not done:
            #     if code[i] == " " or code[i] == "/" or code[i] == "," or code[i] == "!" or code[i] == "." or code:
            #
            #         s1 = code[:i]
            #         s2 = code[i+1:]
            #         code = s1+s2
            #         i-=1
            #     i+=1
            #     if i > len(code)-1:
            #         done = True
            for character in '!?. ,;:~^@#$%¨&*()-+={}[]´`/°ªº§¹²³£¢¬"\\\'':
                code = code.replace(character, '')
            if code == "dstmp":         # impedir o jogador de chamar o negócio de dusty map
                code = "nice_try"

            if len(code) > 48:          # Limitar o tamanho do código em 48 caracteres
                code = code[:48]
            total_stats = 0
            number = 0
            for arma in caller.inventory:

                if arma.ac_code == code:
                    number += 1             # Não repetir nomes

            ac_code = code
            if number:
                code = code + f"{number}"
            if self.server.playersdb.players_and_parties[chat_id].weapon:
                self.server.playersdb.players_and_parties[chat_id].weapon.unequip(self.server.playersdb.players_and_parties[chat_id])
                self.server.playersdb.players_and_parties[chat_id].weapon = None
            self.server.playersdb.players_and_parties[chat_id].calc_attributes()


            for arma in self.server.blacksmith.bs_in_progress[chat_id]["bs_inv"]:
                if "talismans" in dir(arma):
                    for tal_name, tal in arma.talismans.items():
                        caller.storage.append(copy.deepcopy(tal))
                    arma.remove_talismans()
                total_stats += arma.atributos[0]+arma.atributos[1]

            total_stats += caller.stat_points
            caller.stat_points = 0
            at = rd.randint(0, round(total_stats/2))
            de = round(total_stats/2) - at

            weapon = items.Weapon(self.server.blacksmith.bs_in_progress[chat_id]["bs_wep_name"], True, code, 1, [at, de])
            weapon.ac_code = ac_code
            weapon.owner = chat_id
            weapon.type2 =  self.server.blacksmith.bs_in_progress[chat_id]["wep_type"]
            weapon.description = self.server.blacksmith.bs_in_progress[chat_id]["wep_des"]
            # print(weapon.owner)
            self.server.playersdb.players_and_parties[chat_id].inventory.append(weapon)
            self.server.playersdb.players_and_parties[chat_id].calc_attributes()
            text = "You received your legendary weapon and unequipped your current weapon."
            if caller.chat_id in self.server.woods.players:
                self.server.woods.players[caller.chat_id]["active"] = True
            if caller.chat_id in self.server.deep_forest_manager.jogs:
                self.server.deep_forest_manager.jogs[caller.chat_id].active = True
            self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb)
            del self.server.blacksmith.bs_in_progress[chat_id]
            #
            # self.server.helper.append_command("start_bs", chat_id)
            return False

        else:
            text = ("Now send me the code to equip the weapon. The format is: /e_(code)."
                    " I want you to send me only the (code), without the \"/e_\" part. You have 5 minutes")
            self.bot.send_message(text=text, chat_id=caller.chat_id)

            return self.def_wait_time*5

    def to(self, chat_id):
        # for item in self.server.blacksmith.bs_in_progress[chat_id]["bs_inv"]:
        #     self.server.playersdb.players_and_parties[chat_id].inventory.append(item)
        text = f"After {5+self.server.playersdb.players_and_parties[chat_id].suc_refs} minutes of *AWKWARD* starring, the trader ran away."
        self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb, parse_mode="MARKDOWN")
        if chat_id in self.server.woods.players:
            self.server.woods.players[chat_id]["active"] = True
            self.server.playersdb.players_and_parties[chat_id].location = "forest"
        if chat_id in self.server.deep_forest_manager.jogs:
            self.server.deep_forest_manager.jogs[chat_id].active = True
            self.server.playersdb.players_and_parties[chat_id].location = "deep_forest"
        if chat_id in self.server.blacksmith.bs_in_progress:
            if "bs_inv" in self.server.blacksmith.bs_in_progress[chat_id]:
                self.server.playersdb.players_and_parties[chat_id].inventory.extend(self.server.blacksmith.bs_in_progress[chat_id]["bs_inv"])
            del self.server.blacksmith.bs_in_progress[chat_id]
