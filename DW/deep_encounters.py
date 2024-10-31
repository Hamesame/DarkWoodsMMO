import deep_battle
import random as rd
from random import random
import player
import party
from emoji import emojize
import deep_beastsdb
import copy
import deep_items
import death #
import items
from numpy import exp

class DeepEncounters:
    def __init__(self, server):
        self.server = server
        self.battleMan = deep_battle.DeepBattleMan(server)
        self.bdbs = deep_beastsdb.DeepBeastsdb()
        self.Talismandb = deep_items.Talismandb()
        self.chance_to_up_rarity = 0.15
        self.chance_to_drop = 0.3
        self.original_chance_to_get_hit = 0.25
        self.death = death.Death(server)

    def check_if_hit(self, level):
        x = 1 - self.original_chance_to_get_hit
        x = x**(level + 1)
        x = 1 - x
        n = rd.random()
        if n < x:
            return True
        return False


    def World_boss_encounter(self, code):
        self.server.helper.append_command("start_wb_mountain", code)

    def wep(self, code):
        user = self.server.playersdb.players_and_parties[code]
        wood_player = self.server.deep_forest_manager.jogs[code]

        # Primeiramente ele cria uma besta baseada no nível de dificuldade
        power_level = int(wood_player.stay_time/(3*3600)) + 1
        avg_stats = power_level*10                              # Status médio que a arma vai ter
        fluc = 0.2                                              # Flutuação que a arma vai ter de stats
        stats = int(avg_stats*(1 + fluc*(1 - 2*rd.random())))   # vários queixos
        attack = rd.randint(0, stats)
        defense = stats - attack

        # Ok, temos ataque e defesa, vamos agora selecionar os talismans.

        low_levels = 11         # Número de talimans dropáveis por bestas normais.


        prob1 = 1/4 - 1/(4 + exp((power_level - 94)/20)) # Distribuição de bose-einstein
        t_list = []
        for i in range(power_level):
            if rd.random() < self.chance_to_drop and len(t_list) < 5:
                r_up = 0
                for i in range(power_level):
                    if rd.random() < self.chance_to_up_rarity:    # Se ele conseguir upar a radidade da arma..
                        r_up += 1
                if rd.random() < prob1:
                    r_tal = copy.deepcopy(rd.choice(list(self.Talismandb.talismans.items())[:-4])[1])    # Turdnado
                    if r_tal.rarity + r_up > 6:
                        r_up = 6 - r_tal.rarity
                    r_tal.rarity += r_up
                    for power_name, power in r_tal.powers.items():
                        r_tal.powers[power_name] = power*(r_up + 1)
                    t_list.append(r_tal)
                else:
                    r_tal = copy.deepcopy(rd.choice(list(self.Talismandb.talismans.items())[:low_levels])[1])    # Turdnado
                    if r_tal.rarity + r_up > 6:
                        r_up = 6 - r_tal.rarity
                    r_tal.rarity += r_up
                    for power_name, power in r_tal.powers.items():
                        r_tal.powers[power_name] = power*(r_up + 1)
                    t_list.append(r_tal)
        adjectives = ["wierd", "powerful", "weak", "round", "curvy", "edgy", "angry", "picky", "kidding"]
        wep_types = ["sword", "wand", "axe", "mace", "crossbow", "hammer", "bow", "catapult", "club", "spear", "warhammer", "dagger", "fireball launcher", "shield", "cutlass", "scimitar", "excalibur", "whip"]
        connectors = ["of"]
        name = self.server.helper.randomnamegenerator(min(power_level + 1, 20))
        adj = rd.choice(adjectives)
        w_type = rd.choice(wep_types)
        w_name = f"{adj} {w_type} {rd.choice(connectors)} {name}"
        description = f"Some {w_type} found at the deep forest. It is {adj} and you see inscriptions on the weapon saying it belong to someone named {name}."
        number = 0
        for arma in user.inventory:

            if arma.ac_code == name:
                number += 1             # Não repetir nomes


        if number: #
            name = name + f"{number}"
        types2 = ["ranged", "melee", "magic"]
        is_alien_puzzle = False
        if random() < 0.01:
            w_name = emojize("alien puzzle :alien_monster:")
            is_alien_puzzle = True
        newwep = items.Weapon(w_name, False, name, 1, [attack, defense])
        if is_alien_puzzle:
            description = "A puzzle that does not look to belong to this world. (its incredibly hard to solve)."
        newwep.description = description
        newwep.type2 = rd.choice(types2)

        if not is_alien_puzzle:
            newwep.add_talismans(t_list)
        user.inventory.append(newwep)
        if user.pt_code:

            text = f"While wandering in the deep forest your party found {w_name} and added to the shared inventory."
            self.server.bot.send_message(text=text, chat_id=user.chat_ids)
        else:
            text = f"While wandering in the deep forest you found {w_name} and added to the inventory."
            self.server.bot.send_message(text=text, chat_id=code)

    def sanc(self, code):
        jog = self.server.playersdb.players_and_parties[code]
        if code.startswith("/"):
            for jog2 in jog.players:
                if jog2.classe == "Unknown":
                    text = "While walking around the woods you found a strange structure, there you see people meditating, you still dont know how to meditate, so you continued on your journey."
                    self.server.bot.send_message(text=text, chat_id=jog2.chat_id)
                else:
                    jog2.sanctuary()
        else:
            if jog.classe == "Unknown":
                text = "While walking around the woods you found a strange structure, there you see people meditating, you still dont know how to meditate, so you continued on your journey."
                self.server.bot.send_message(text=text, chat_id=code)
            else:
                jog.sanctuary()

    def normal_beast(self, code):
        user = self.server.playersdb.players_and_parties[code]
        if self.server.is_day:
            deep_beast = copy.deepcopy(rd.choice(self.bdbs.beasts))
        else:
            deep_beast = copy.deepcopy(rd.choice(self.bdbs.night_beasts))
        wood_player = self.server.deep_forest_manager.jogs[code]

        # Primeiramente ele cria uma besta baseada no nível de dificuldade
        power_level = int(wood_player.stay_time/(3*3600)) + 1

        deep_beast.stats = deep_beast.stats*(power_level)
        if deep_beast.powers:
            for name, att in deep_beast.powers.items():
                deep_beast.powers[name] = att*(power_level)
        # print(f"Power level: {power_level} {deep_beast.name}")
        bres = self.battleMan.b_battle(user, deep_beast)

        if bres == -1:
            drops = []
            probs = []         # Lista que conterá todas as probabilidades dos drop
            for key, item in deep_beast.drop.items():
                probs.append(item)
            for rounds in range(power_level):   # para cada power level ele pode dropar um item da besta
                drop = rd.choices(list(deep_beast.drop.keys()), probs)[0]
                if drop != "nothing":
                    drop = copy.deepcopy(self.Talismandb.talismans[drop])
                    rarity_up = 0
                    for r2 in range(power_level):   # Para cada power level ele tem a chance de 75% de aumentar em 1 a raridade do item.
                        n = rd.random()
                        if n < self.chance_to_up_rarity:
                            rarity_up += 1
                    # print(f"rarity_up = {rarity_up}, drop.rarity: {drop.rarity}")
                    if drop.rarity + rarity_up > 6:
                        rarity_up = 6 - drop.rarity

                    drop.rarity += rarity_up
                    # print(f"rarity_up = {rarity_up}, drop.rarity: {drop.rarity}")
                    # print("---------------------")
                    for power_name, power in drop.powers.items():
                        drop.powers[power_name] = power*(rarity_up + 1)
                    drops.append(drop)


            if code.startswith("/"):

                text = f"In the deep forest your party found a level {power_level} {deep_beast.name} and killed it.\n Upon butchering the beast you got these items:\n\n"
                for item in drops:
                    text += f"*{item}*\n"
                for pl in user.players:
                    gain = (power_level+1)*pl.level*2
                    pl.exp += gain
                    specific_text = text + f"*{gain}* exp"
                    pl.storage.extend(copy.deepcopy(drops))
                    self.server.bot.send_message(text=specific_text, chat_id=pl.chat_id, parse_mode="MARKDOWN")
            else:
                    # if self.server.playersdb.players_and_parties[code].classe == "Druid":
                    #     self.server.playersdb.players_and_parties[code].beast_in_stack = deep_beast
                    text = f"In the deep forest you found a level {power_level} {deep_beast.name} and killed it.\n Upon butchering the beast you got these items:\n\n"
                    for item in drops:
                        text += f"*{item}*\n"
                    user.storage.extend(drops)
                    gain = (power_level+1)*self.server.playersdb.players_and_parties[code].level*2
                    self.server.playersdb.players_and_parties[code].exp += gain
                    specific_text = text + f"*{gain}* exp"
                    self.server.bot.send_message(text=specific_text, chat_id=code, parse_mode="MARKDOWN")

        else:
            if code.startswith("/"):
                text = f"In the deep forest your party found a level {power_level} {deep_beast.name} it destroyed your party. "
                for chat in user.chat_ids:
                    jogador = self.server.playersdb.players_and_parties[chat]
                    gain = (power_level+1)*jogador.level
                    self.server.playersdb.players_and_parties[chat].exp += gain

                    if self.check_if_hit(power_level):
                        limb_i = self.server.playersdb.players_and_parties[chat].take_damage()
                        if self.server.playersdb.players_and_parties[chat].classe == "Druid":
                            self.server.playersdb.players_and_parties[chat].beast_in_stack = None
                        if limb_i != -1:
                            if isinstance(limb_i, int):
                                specific_text = f"And the {deep_beast.name} followed you as you tried to escape and it, finally reaching you and destroying your {jogador.hp[limb_i].name}. But you gained {gain} exp."
                            else:
                                specific_text = f"And the {deep_beast.name} followed you as you tried to escape and it, finally reaching you and killed your {limb_i}. But you gained {gain} exp."

                        else:
                            specific_text = f"And the {deep_beast.name} followed you as you tried to escape and it, finally reaching you *finishing your life*. But you gained {gain} exp."
                            self.death.die(chat)
                        self.server.bot.send_message(text=text+specific_text, chat_id=chat, parse_mode='MARKDOWN')
                    else:
                        specific_text = f"And the {deep_beast.name} followed you as you tried to escape and it, good thing you could outrun it. And you gained {gain} exp."
                        self.server.bot.send_message(text=text+specific_text, chat_id=chat, parse_mode='MARKDOWN')
            else:
                text = f"In the deep forest you found a level {power_level} {deep_beast.name} it destroyed you. "
                gain = (power_level+1)*self.server.playersdb.players_and_parties[code].level
                self.server.playersdb.players_and_parties[code].exp += gain
                jogador = self.server.playersdb.players_and_parties[code]
                if self.check_if_hit(power_level):
                    limb_i = self.server.playersdb.players_and_parties[code].take_damage()
                    if self.server.playersdb.players_and_parties[code].classe == "Druid":
                        self.server.playersdb.players_and_parties[code].beast_in_stack = None
                    if limb_i != -1:
                        if isinstance(limb_i, int):
                            specific_text = f"And the {deep_beast.name} followed you as you tried to escape and it, finally reaching you and destroying your {jogador.hp[limb_i].name}. But you gained {gain} exp."
                        else:
                            specific_text = f"And the {deep_beast.name} followed you as you tried to escape and it, finally reaching you and killed your {limb_i}. But you gained {gain} exp."

                    else:
                        specific_text = f"And the {deep_beast.name} followed you as you tried to escape and it, finally reaching you *finishing your life*. But you gained {gain} exp."
                        self.death.die(code)
                    self.server.bot.send_message(text=text+specific_text, chat_id=code, parse_mode='MARKDOWN')
                else:
                    specific_text = f"And the {deep_beast.name} followed you as you tried to escape and it, good thing you could outrun it. And you gained {gain} exp."
                    self.server.bot.send_message(text=text+specific_text, chat_id=code, parse_mode='MARKDOWN')


    def mega_beast(self, code):
        self.server.helper.append_command("start_mega1", code)

    def shaman(self, code):
        if code[0] == "/":
            # You need to be alone for the shaman to appear
            user = self.server.playersdb.players_and_parties[code]
            text = "You hear footsteps and whispers but you dont understand what is happening. Maybe there's someone shy nearby."
            self.server.bot.send_message(text=text, chat_id=user.chat_ids, parse_mode='MARKDOWN')
            print("shaman event with parties was triggered")
        else:
            user = self.server.playersdb.players_and_parties[code]
            is_there = False
            for wep in user.inventory:
                if wep.code == user.weapon.code:
                    is_there = True
                    break
            if not is_there:
                self.server.helper.append_command("start_shaman", code)
                print("shaman worked")
            else:
                # The shaman only appears when you have a ghostly weapon.
                text = "You hear footsteps and whispers but you dont understand what is happening. Maybe there's someone attracted to ghosts nearby but you don't own any ghostly weapons."
                self.server.bot.send_message(text=text, chat_id=code, parse_mode='MARKDOWN')
                print("shaman but without ghostly")

    def enchanter(self, code):
        self.server.helper.append_command("start_enchanter", code)

    def blacksmith(self, code):
        if code[0] == "/":
            self.normal_beast(code)
        else:
            self.server.helper.append_command("start_bs", code)


    def holy_trees(self, code):
        # txt = "You walk into a glade and find the holy trees of Oak, Ash and thorn"
        if code[0] == "/":
            self.normal_beast(code)
        else:
            self.server.helper.append_command("start_oak_ash_thorn", code)
    # halloween Event 2023
    def plot_msg(self, code):
        if self.server.is_midnight:
            text = ('You found the ruins of a small shrine. There were old drawings of an island that floated above our world. Also, on the ground, scribbles of some kind of cyclical calendar where we can see our world and the island revolving in opposite directions. The points where they intersect are marked with the words "Samhain" and "Bealtaine". You see other points of the Sabbat shining in a blue light: Yule, Imbolc, Ostara, Litha, Lughnasadh and Mabon.')
            if code.startswith("/"):
                user = self.server.playersdb.players_and_parties[code]
                for ch_id in user.chat_ids:
                    pl = self.server.playersdb.players_and_parties[ch_id]
                    if pl.weapon.name == emojize("alien puzzle :alien_monster:"):
                        if "helios_puzzle" in pl.weapon.talismans:
                            r_tal = [copy.deepcopy(self.Talismandb.talismans["cosmic_gift"])]
                            pl.storage.extend(copy.deepcopy(r_tal))
                            text += emojize(" Your alien puzzle :alien_monster: opens and reveals you a talisman.")
                        if "cosmic_gift" in pl.weapon.talismans:
                            r_tal = [copy.deepcopy(self.Talismandb.talismans["true_cosmic_gift"])]
                            pl.storage.extend(copy.deepcopy(r_tal))
                            text += emojize(" Your alien puzzle :alien_monster: opens and reveals you a talisman.")
                    self.server.bot.send_message(text=text, chat_id=ch_id)
                #self.server.bot.send_message(text=text, chat_id=user.chat_ids)
            else:
                pl = self.server.playersdb.players_and_parties[code]
                if pl.weapon.name == emojize("alien puzzle :alien_monster:"):
                    if "helios_puzzle" in pl.weapon.talismans:
                        r_tal = [copy.deepcopy(self.Talismandb.talismans["cosmic_gift"])]
                        pl.storage.extend(copy.deepcopy(r_tal))
                        text += emojize(" Your alien puzzle :alien_monster: opens and reveals you a talisman.")
                    if "cosmic_gift" in pl.weapon.talismans:
                        r_tal = [copy.deepcopy(self.Talismandb.talismans["true_cosmic_gift"])]
                        pl.storage.extend(copy.deepcopy(r_tal))
                        text += emojize(" Your alien puzzle :alien_monster: opens a secret compartment and reveals you a talisman.")
                self.server.bot.send_message(text=text, chat_id=code)
        else:
            text = ('You found the ruins of a small shrine. There were old drawings of an island that floated above our world. Also, on the ground, scribbles of some kind of cyclical calendar where we can see our world and the island revolving in opposite directions. The points where they intersect are marked with the words "Samhain" and "Bealtaine".')
            if code.startswith("/"):
                user = self.server.playersdb.players_and_parties[code]
                self.server.bot.send_message(text=text, chat_id=user.chat_ids)
            else:
                self.server.bot.send_message(text=text, chat_id=code)
    # Halloween event 2022
    # def plot_msg(self, code):
    #     text = ("Exausted from walking all day, you decided to rest on the base of a tree. You fall asleep and dream of a land where people collectively dream and fights the root of evil together with the power of lucid dreaming. You witness a giant rock with many caves. Each leading to a different dream. One of the cavern walls displays a fading text:")
    #     code = "ZHJlYW1hcmdib3Q="
    #     hidden_char = "█"
    #     random_char_to_show = rd.randint(0, len(code))
    #     hidden_code = ""
    #     i = 0
    #     for ch in code:
    #         if random_char_to_show == i:
    #             hidden_code += ch
    #         else:
    #             hidden_code += hidden_char
    #         i += 1
    #     text += hidden_code + "."
    #     if code.startswith("/"):
    #         user = self.server.playersdb.players_and_parties[code]
    #
    #         self.server.bot.send_message(text=text, chat_id=user.chat_ids)
    #     else:
    #         self.server.bot.send_message(text=text, chat_id=code)
