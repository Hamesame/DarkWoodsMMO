###################################################
#  Classe que gerencia os encontros da floresta  #
###################################################

import battle2
import death
import bot
import copy
import random as rd
from emoji import emojize
import items
import time
import player
import party  #


class Encounters:

    def __init__(self, server):
        self.server = server
        self.battleMan = battle2.BattleMan(server)
        self.bot = bot.TGBot()
        self.commander = server.messageman
        self.death = death.Death(self.server)

        self.tier_1 = 60*30
        self.tier_2 = 2*60*60
        self.tier_3 = 4*60*60
        self.tier_4 = 6*60*60

        self.min_bs_weaps = 5


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
                            pl.storage.extend(copy.deepcopy(drops))
                            text += emojize(" Your alien puzzle :alien_monster: opens and reveals you a talisman.")
                        if "cosmic_gift" in pl.weapon.talismans:
                            r_tal = [copy.deepcopy(self.Talismandb.talismans["true_cosmic_gift"])]
                            pl.storage.extend(copy.deepcopy(drops))
                            text += emojize(" Your alien puzzle :alien_monster: opens and reveals you a talisman.")
                    self.server.bot.send_message(text=text, chat_id=ch_id)
                #self.server.bot.send_message(text=text, chat_id=user.chat_ids)
            else:
                pl = self.server.playersdb.players_and_parties[code]
                if pl.weapon.name == emojize("alien puzzle :alien_monster:"):
                    if "helios_puzzle" in pl.weapon.talismans:
                        r_tal = [copy.deepcopy(self.Talismandb.talismans["cosmic_gift"])]
                        pl.storage.extend(copy.deepcopy(drops))
                        text += emojize(" Your alien puzzle :alien_monster: opens and reveals you a talisman.")
                    if "cosmic_gift" in pl.weapon.talismans:
                        r_tal = [copy.deepcopy(self.Talismandb.talismans["true_cosmic_gift"])]
                        pl.storage.extend(copy.deepcopy(drops))
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
    # def plot_msg(self, chat_id):
    #     # t0 = time.time()
    #     # text = emojize("While wandering the forest, the path suddenly became insurmountable due to the amount of trees and vines. "
    #     #                "Unable to press forward, you decided to go the long way around. Some time later, you looked back "
    #     #                "from the top of a hill and spotted a lone, gargantuan sunflower :sunflower::sunflower::sunflower::sunflower:"
    #     #                " standing above the nearby trees, which appears to be fenced off by the surrounding plant life. "
    #     #                "Pondering about the sight, you continue your journey")
    #     # text = emojize("You arrived at a darker part of the forest where the trees were sparse and fauna was absent.\n\n"
    #     #                 "After some time, you got to the feet of a mountain. You decided to climb it.\n"
    #     #                 "At its top you could witness a valley. At it's bottom grows a sunflower :sunflower::sunflower::sunflower::sunflower::sunflower: the size of a mountain.\n"
    #     #                 "You couldn't get closer to it. It was surrounded by insurmountable plant life.\n\n"
    #     #                 "Unsure of what that could mean, *you decided to step back*.")
    #     text = ("Exausted from walking all day, you decided to rest on the base of a tree. You fall asleep and dream of a land where people collectively dream and fights the root of evil together with the power of lucid dreaming. You witness a giant rock with many caves. Each leading to a different dream. One of the cavern walls displays a fading text:")
    #     code = "ZHJlYW1hcmdib3Q="
    #     hidden_char = "█"
    #     random_char_to_show = rd.randint(0, len(code)-1)
    #     hidden_code = ""
    #     i = 0
    #     for ch in code:
    #         if random_char_to_show == i:
    #             hidden_code += ch
    #         else:
    #             hidden_code += hidden_char
    #         i += 1
    #     text += hidden_code + "."
    #     self.bot.send_message(text=text, chat_id=chat_id, parse_mode = "MARKDOWN")

        # self.server.helper.append_command("start_WB", chat_id)

    def plot_msg_Hal_event(self, chat_id):
        text = emojize(
            "While waling on the deep snow of the forest you witness a mountain, "
            "its completelly covered in snow :snowflake::snowflake::snowflake: "
            "and its summit isnt visible due to the clouds "
            "forming nearby. You got the conclusion that nothing can survive "
            "that weather and decided to step back. It's a dangerous place."
        )
        caller = self.server.playersdb.players_and_parties[chat_id]
        self.server.playersdb.players_and_parties[caller.chat_id].active = True
        self.server.woods.players[caller.chat_id]["active"] = True
        self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode = "MARKDOWN")

        # self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.server.defkb, parse_mode = 'MARKDOWN')
        # print(f"sunflower msg time: {time.time() - t0}")

    def normal_beast(self, chat_id):
        # t0 = time.time()
        jogador = self.server.playersdb.players_and_parties[chat_id]
        tempo = min(self.server.woods.players[chat_id]["rem_time"], self.server.woods.players[chat_id]["stay_time"] - self.server.woods.players[chat_id]["rem_time"])
        # print(self.server.woods.players[chat_id]["rem_time"])
        # print(self.server.woods.players[chat_id]["stay_time"])
        # print(f"tempo: {tempo}")
        tier = 1
        if tempo > self.tier_1:
            tier = 2
        if tempo > self.tier_2:
            tier = 3
        if tempo > self.tier_3:
            tier = 4
        # print(f"tier: {tier}")
        besta = self.server.beastsdb.get_random_beast(tier)
        battle_result = self.battleMan.battle(jogador, besta)
        dead = False

        if battle_result == -1:
            print("As the battle is won, you gained exp\n")
            jogador.exp += 2*jogador.level
            text = emojize(f"You found a poor {besta.tipo} and killed it, you gained {2*jogador.level} exp.")
            self.bot.send_message(text=text, chat_id=chat_id)
            if jogador.classe == "Druid":
                jogador.beast_in_stack = besta

        elif battle_result == 1:
            print("As the battle is lost, you took damage")
            limb_i = jogador.take_damage()

            jogador.exp += jogador.level
            if isinstance(limb_i, int):
                text = emojize(f"You found a {besta.tipo} and it destroyed your {jogador.hp[limb_i].name}, "
                               f"you gained {jogador.level} exp.")
                self.bot.send_message(text=text, chat_id=chat_id)

                if limb_i < 0:
                    dead = True

            else:
                text = emojize(f"You found a {besta.tipo} and it killed your {limb_i} :loudly_crying_face:, you gained {jogador.level} exp.")
                self.bot.send_message(text=text, chat_id=chat_id)

            if jogador.classe == "Druid":
                jogador.beast_in_stack = None

        else:
            print("Its a draw")
            jogador.exp += jogador.level
            text = emojize("You met a foe who you battled for a very long time, as your strengths were evenly matched. "
                           f"Exhausted, you retreated, and so did the {besta.tipo}. "
                           f"You gained {jogador.level} exp")
            self.bot.send_message(text=text, chat_id=chat_id)

        if besta.tipo not in jogador.pokedex:
            text = emojize(f"Congratulations, {besta.tipo} has been added to the /bestiary!")
            self.bot.send_message(text=text, chat_id=chat_id)
            jogador.pokedex.append(besta.tipo)

        if dead:
            self.death.die(chat_id)
        # print(f"normal beast time: {time.time() - t0}")

    def legendary_beast(self, chat_id):
        # t0 = time.time()
        jogador = self.server.playersdb.players_and_parties[chat_id]
        besta = self.server.beastsdb.get_random_legbeast()
        battle_result = self.battleMan.battle(jogador, besta)
        dead = False

        if battle_result == -1:
            jogador.exp += 2*jogador.level
            text = emojize(f"You found a poor {besta.tipo} named {besta.name} and killed it, you gained {2*jogador.level} exp.")
            self.bot.send_message(text=text, chat_id=chat_id)
            if jogador.classe == "Druid":
                jogador.beast_in_stack = besta

        elif battle_result == 1:
            limb_i = jogador.take_damage()
            jogador.exp += jogador.level

            if isinstance(limb_i, int):
                text = emojize(f"You found a {besta.tipo} named {besta.name} and it destroyed your {jogador.hp[limb_i].name}, "
                               f"you gained {jogador.level} exp.")
                self.bot.send_message(text=text, chat_id=chat_id)

                if limb_i < 0:
                    dead = True

            else:
                text = emojize(f"You found a {besta.tipo} named {besta.name} and it killed your {limb_i}, "
                               f"you gained {jogador.level} exp.")
                self.bot.send_message(text=text, chat_id=chat_id)
            if jogador.classe == "Druid":
                jogador.beast_in_stack = None

        else:
            jogador.exp += jogador.level
            text = emojize("You met a foe who you battled for a very long time, as your strengths were evenly matched. "
                           f"Exhausted, you retreated, and so did the {besta.tipo} named {besta.name}. "
                           f"You gained {jogador.level} exp")
            self.bot.send_message(text=text, chat_id=chat_id)

        if f"{besta.tipo} named {besta.name}" not in jogador.pokedex:
            text = emojize(f"Congratulations, {besta.tipo} named {besta.name} has been added to the /bestiary!")
            self.bot.send_message(text=text, chat_id=chat_id)
            jogador.pokedex.append(f"{besta.tipo} named {besta.name}")

        if dead:
            self.death.die(chat_id)
        # print(f"leg beast time: {time.time() - t0}")

    def player_bat(self, chat_id):
        # t0 = time.time()
        jogador = self.server.playersdb.players_and_parties[chat_id]

        found_opponent = False
        if len(self.server.woods.players) > 0:
            other_guy_id = rd.choices(list(self.server.woods.players.keys()))[0]
            active = self.server.woods.players[other_guy_id]["active"]
            count = 0
            found_opponent = True
            while (not active or other_guy_id == chat_id) and count < 10:
                other_guy_id = rd.choices(list(self.server.woods.players.keys()))[0]
                active = self.server.woods.players[other_guy_id]["active"]
                count += 1
                found_opponent = False

            if found_opponent:
                if other_guy_id[0] == "/":
                    other_guy = self.server.playersdb.players_and_parties[other_guy_id]
                else:
                    other_guy = self.server.playersdb.players_and_parties[other_guy_id]
                bres = self.battleMan.battle(jogador, other_guy)
                winner = None
                loser = None

                if bres == -1:
                    winner = jogador
                    loser = other_guy

                    if not isinstance(other_guy, party.Party):
                        other_guy.exp += jogador.level
                        jogador.exp += 2*other_guy.level
                    else:
                        exp_gain = 0
                        for jogador2 in other_guy.players:
                            jogador2.exp += jogador.level
                            if jogador2.level > exp_gain:
                                exp_gain =  jogador2.level
                        jogador.exp += 2*exp_gain

                elif bres == 1:
                    winner = other_guy
                    loser = jogador
                    if not isinstance(other_guy, party.Party):
                        other_guy.exp += 2*jogador.level
                        jogador.exp += other_guy.level
                    else:
                        exp_gain = 0
                        for jogador2 in other_guy.players:
                            jogador2.exp += 2*jogador.level
                            if jogador2.level > exp_gain:
                                exp_gain =  jogador2.level
                        jogador.exp += exp_gain

                else:
                    if not isinstance(other_guy, party.Party):
                        other_guy.exp += jogador.level
                        jogador.exp += other_guy.level
                    else:
                        exp_gain = 0
                        for jogador2 in other_guy.players:
                            jogador2.exp += jogador.level
                            if jogador2.level > exp_gain:
                                exp_gain =  jogador2.level
                        jogador.exp += exp_gain

                if winner:
                    if isinstance(loser, player.Player) and isinstance(winner, player.Player):
                        aux = "him"
                        if loser.gender == "female":
                            aux = 'her'
                        if loser.weapon:

                            text = emojize(f"In the middle of the forest you found {loser.name}, wielding "
                                           f"{loser.weapon.name} and you destroyed {aux}, you gained {2*loser.level} exp.")
                            self.bot.send_message(text=text, chat_id=winner.chat_id)
                        else:
                            text = emojize(f"In the middle of the forest you found {loser.name} and you destroyed {aux}, "
                                           f"you gained {2*loser.level} exp.")
                            self.bot.send_message(text=text, chat_id=winner.chat_id)
                        aux = "he"
                        if winner.gender == "female":
                            aux = 'she'
                        if winner.weapon:
                            text = emojize(f"In the middle of the forest you found {winner.name} wielding "
                                           f"{winner.weapon.name} and {aux} destroyed you, you gained {winner.level} exp.")
                            self.bot.send_message(text=text, chat_id=loser.chat_id)
                        else:
                            text = emojize(f"In the middle of the forest you found {winner.name} and {aux} destroyed you, "
                                           f"you gained {winner.level} exp.")
                            self.bot.send_message(text=text, chat_id=loser.chat_id)

                        limb_i = loser.take_damage()
                        if isinstance(limb_i, int):
                            if limb_i < 0:
                                self.death.die(loser.chat_id)

                    elif not isinstance(loser, party.Party):
                        aux = "him"
                        if loser.gender == "female":
                            aux = 'her'
                        if loser.weapon:
                            text = emojize(f"In the middle of the forest your group found {loser.name}, wielding "
                                           f"{loser.weapon.name} and you destroyed {aux}, you gained {2*loser.level} exp.")

                            for jogadores in winner.players:
                                self.bot.send_message(text=text, chat_id=jogadores.chat_id)
                        else:
                            text = emojize(f"In the middle of the forest your group found {loser.name} and you destroyed {aux}, "
                                           f"you gained {2*loser.level} exp.")
                            for jogadores in winner.players:
                                self.bot.send_message(text=text, chat_id=jogadores.chat_id)

                        text = f"In the middle of the forest you found a group called {winner.pt_name} and they destroyed you, you gained {exp_gain} exp."
                        self.bot.send_message(text=text, chat_id=loser.chat_id)

                        limb_i = loser.take_damage()
                        if isinstance(limb_i, int):
                            if limb_i < 0:
                                self.death.die(loser.chat_id)

                    else:
                        text = emojize(f"In the middle of the forest you found a group called {loser.pt_name} and you destroyed them, "
                                       f"you gained {2*exp_gain} exp.")
                        self.bot.send_message(text=text, chat_id=winner.chat_id)
                        aux = "he"
                        if winner.gender == "female":
                            aux = 'she'

                        if winner.weapon:
                            text = emojize(f"In the middle of the forest your group found {winner.name} wielding a "
                                           f"{winner.weapon.name} and {aux} destroyed you, you gained {winner.level} exp.")
                            for jogadores in loser.players:
                                self.bot.send_message(text=text, chat_id=jogadores.chat_id)
                        else:
                            text = emojize(f"In the middle of the forest your group found {winner.name} and {aux} destroyed you, "
                                           f"you gained {winner.level} exp.")
                            for jogadores in loser.players:
                                self.bot.send_message(text=text, chat_id=jogadores.chat_id)

                        # limb_i = loser.take_damage()
                        # if isinstance(limb_i, int):
                        #     if limb_i < 0:
                        #         self.death.die(loser.chat_id)

                        # precisa codar o dano das parties
                else:
                    if isinstance(other_guy, player.Player):
                        text = emojize("You met a foe who you battled for a very long time, as your strengths were evenly matched."
                                       f" Exhausted, you retreated, and so did {other_guy.name}. You gained {other_guy.level} exp.")
                        self.bot.send_message(text=text, chat_id=chat_id)
                    else:
                        text = emojize("You met a group who you battled for a very long time, as your strengths were evenly matched."
                                       f" Exhausted, you retreated, and so did {other_guy.pt_name}. You gained {exp_gain} exp.")
                        self.bot.send_message(text=text, chat_id=chat_id)

                    text = emojize("You met a foe who you battled for a very long time, as your strengths were evenly matched."
                                   f" Exhausted, you retreated, and so did {jogador.name}. You gained {jogador.level} exp.")

                    if isinstance(other_guy, party.Party):

                        for jogadores in other_guy.players:
                            self.bot.send_message(text=text, chat_id=jogadores.chat_id)
                    else:
                        self.bot.send_message(text=text, chat_id=other_guy.chat_id)


        if not found_opponent:
            text = "You thought you saw someone sneaking behind you, but it was only your own shadow. You feel lonely."
            self.bot.send_message(text=text, chat_id=chat_id)
        # print(f"player battle time: {time.time() - t0}")

    def item(self, chat_id):
        # t0 = time.time()
        jogador = self.server.playersdb.players_and_parties[chat_id]
        bang = self.server.itemsdb.get_random_weapon()
        item = copy.deepcopy(bang)



        number = 0

        old_code = item.code
        for arma in jogador.inventory:

            if arma.ac_code == item.ac_code:
                number += 1

        if number == 0:
            number = ""
        item.ac_code = item.code + f"{number}"
        temp_ac = item.ac_code
        item.ac_code = item.code
        item.code = temp_ac
        item.owner = chat_id        # Marca o novo dono do item.
        jogador.inventory.append(copy.deepcopy(item))
        text = emojize(f"While wandering in the woods, you found a *{item.name}* and added it to your inventory!")
        self.bot.send_message(text=text, chat_id=chat_id, parse_mode='MARKDOWN')



        if item.is_legendary:
            item.code = old_code
            self.server.itemsdb.remove_weapon_from_pool(item)




        # print(f"item time: {time.time() - t0}")

    def dungeon(self, chat_id):
        # t0 = time.time()
        # user = self.server.playersdb.players_and_parties[chat_id]
        # if not user.last_done_dungeon_time:
        #     user.last_done_dungeon_time = time.time()
        # else:
        #     delta_t = time.time()-user.last_done_dungeon_time
        #     user.average_times_taken.append(delta_t)
        #     user.average_time_between_dungeons = sum(user.average_times_taken)/len(user.average_times_taken)
        #     user.average_time_between_last_dungeons = sum(user.average_times_taken[-5:])/len(user.average_times_taken[-5:])
        # user.average_time_between_WB = user.average_time_between_dungeons*5
        self.server.helper.append_command("start_dg", chat_id)
        # print(f"dg encounter time: {time.time() - t0}")

    def df(self, chat_id):
        tempo = min(self.server.woods.players[chat_id]["rem_time"], self.server.woods.players[chat_id]["stay_time"] - self.server.woods.players[chat_id]["rem_time"])

        if tempo > self.tier_3:
            self.server.helper.append_command("start_df", chat_id)
        else:
            self.server.helper.append_command("start_dg", chat_id)

    # def caverns(self, chat_id):
    #     self.server.helper.append_command("start_caverns", chat_id)

    def blacksmith(self, chat_id):
        # t0 = time.time()
        self.server.helper.append_command("start_bs", chat_id)
        # if len(self.server.playersdb.players_and_parties[chat_id].inventory) >= self.min_bs_weaps:
        #     self.server.helper.append_command("start_bs", chat_id)
        # else:
        #     text = ("In the forest you found a blacksmith, to whom you talked at length about your adventures."
        #             " He was not impressed by your deeds and your small collection, so you continued on your way.")
        #     self.bot.send_message(text=text, chat_id=chat_id)
        # print(f"bs encounter time: {time.time() - t0}")

    def map(self, chat_id):
        # t0 = time.time()
        def hasmap(inventory, map_type):
            n = 0
            for invitem in inventory:
                if invitem.type == "map":
                    if invitem.map_type == map_type:
                        n += 1
            if n > 4:
                return True
            return False
        maps_choices = copy.deepcopy(items.dg_map.possibles_maps)
        jogador = self.server.playersdb.players_and_parties[chat_id]
        item = None
        while item == None and maps_choices:
            map = rd.choice(maps_choices)
            map_type = map[4]
            if hasmap(jogador.inventory, map_type):
                maps_choices.remove(map)
            else:
                item = items.dg_map(*map)

        text = ""
        if item:
            jogador.inventory.append(copy.deepcopy(item))

            if item.map_type == "dg_map":

                # text = ("While walking around the forest, you tripped over a small bottle. Inside it you found a dusty piece of paper containing some strange drawings. You think it might be a map leading to somewhere interesting, probably a dungeon of some sort. It could take some time to get there, though. Better prepare yourself before going!")
                text = emojize("Gazing distractedly at the sunlit leaves overhead, you forgot to look where you were going and tripped over something,"
                " dragging your face in the dirt for a couple of feet. You get up and prepare to fight, but it was just a small, half-buried "
                "bottle with some sort of note inside: a piece of paper with drawings and scribbles, like directions. Maps don't last very long,"
                " as they never seem to lead to the same place twice, but maybe this one can still take you somewhere interesting."
                " You should prepare before going, because your destination is always unknown.")
            elif item.map_type == "deep_forest_map":
                text = emojize("While hunting in the forest, you come across the elusive golden "
                "kalango, which is said to bring good fortune. The lizard's beauty is "
                "mesmerizing, glistening as it bathes in the sunlight. You're about "
                "to ambush it when a drifting sheet of paper lands on your face, "
                "obscuring your vision. Examining the missive, you find a broad "
                "bird's-eye view of the forest, showing further than you usually go. "
                "Heading that deep into the forest must harbor great risk, as well "
                "as rewards. The kalango is gone, so you pout and pocket the map. "
                "So much for good fortune...")
            self.bot.send_message(text=text, chat_id=chat_id)
        else:
            self.legendary_beast(chat_id)
        # print(f"map encounter time: {time.time() - t0}")


        del item

    def sanctu(self, chat_id):
        jog = self.server.playersdb.players_and_parties[chat_id]
        if jog.classe == "Unknown":
            text = "While walking around the woods you found a strange structure, there you see people meditating, you still dont know how to meditate, so you continued on your journey."
            self.bot.send_message(text=text,chat_id=chat_id)
        else:
            jog.sanctuary()


class pt_Encounters:

    def __init__(self, server):
        self.server = server
        self.battleMan = battle2.BattleMan(server)
        self.bot = bot.TGBot()
        self.commander = server.messageman
        self.death = death.Death(self.server)

        self.tier_1 = 60*30
        self.tier_2 = 2*60*60
        self.tier_3 = 4*60*60
        self.tier_4 = 6*60*60

        self.min_bs_weaps = 5

    def aux_deal_damage_to_one_member(self, grupo):
        damaged = None
        invalidos = []
        order = []
        def_ord = ["Unknown", "Druid", "Knight", "Wizard", "Explorer"]
        for jogador in grupo.players:
                order.append(jogador)
        for cla in def_ord:
            for jogador in order:
                if jogador.classe == cla:
                    hp_self = 0
                    for limb in jogador.hp:
                        hp_self += limb.health
                    if hp_self < 5:
                        invalidos.append(jogador)
                    else:
                        damaged = jogador
                        break
            if damaged:
                break

        if not damaged:
            if len(invalidos):
                x = rd.randint(0, len(invalidos)-1)
                damaged = invalidos[x]
            else:
                l = rd.randint(0, len(order)-1)
                damaged = order[l]
        limb_i = self.server.playersdb.players_and_parties[damaged.chat_id].take_damage()
        if isinstance(limb_i, int):
            if limb_i < 0:
                self.death.die(damaged.chat_id)
        text = "You have been hit."
        self.bot.send_message(text=text, chat_id=damaged.chat_id)

    # halloween Event 2023
    def pt_plot_msg(self, code):
        if self.server.is_midnight:
            text = ('You found the ruins of a small shrine. There were old drawings of an island that floated above our world. Also, on the ground, scribbles of some kind of cyclical calendar where we can see our world and the island revolving in opposite directions. The points where they intersect are marked with the words "Samhain" and "Bealtaine". You see other points of the Sabbat shining in a blue light: Yule, Imbolc, Ostara, Litha, Lughnasadh and Mabon.')
            if code.startswith("/"):
                user = self.server.playersdb.players_and_parties[code]
                self.server.bot.send_message(text=text, chat_id=user.chat_ids)
            else:
                self.server.bot.send_message(text=text, chat_id=code)
            # self.server.helper.append_command("start_mag_mell", code)       # It will be considered a new kind of event
        else:
            text = ('You found the ruins of a small shrine. There were old drawings of an island that floated above our world. Also, on the ground, scribbles of some kind of cyclical calendar where we can see our world and the island revolving in opposite directions. The points where they intersect are marked with the words "Samhain" and "Bealtaine".')
            if code.startswith("/"):
                user = self.server.playersdb.players_and_parties[code]
                self.server.bot.send_message(text=text, chat_id=user.chat_ids)
            else:
                self.server.bot.send_message(text=text, chat_id=code)

    # Halloween event 2022
    # def pt_plot_msg(self, pt_code):
    #     # t0 = time.time()
    #     # text = emojize("While wandering the forest, the path suddenly became insurmountable due to the amount of trees and vines. "
    #     #                "Unable to press forward, you decided to go the long way around. Some time later, you looked back "
    #     #                "from the top of a hill and spotted a lone, gargantuan sunflower :sunflower::sunflower::sunflower::sunflower:"
    #     #                " standing above the nearby trees, which appears to be fenced off by the surrounding plant life. "
    #     #                "Pondering about the sight, you continue your journey")
    #
    #     # text = emojize("You arrived at a darker part of the forest where the trees were sparse and fauna was absent.\n\n"
    #     #                 "After some time, you got to the feet of a mountain. You decided to climb it.\n"
    #     #                 "At its top you could witness a valley. At it's bottom grows a sunflower :sunflower::sunflower::sunflower::sunflower::sunflower: the size of a mountain.\n"
    #     #                 "You couldn't get closer to it. It was surrounded by insurmountable plant life.\n\n"
    #     #                 "Unsure of what that could mean, *you decided to step back*.")
    #     #
    #     # for chat_id,jogador in self.server.parties_codes[pt_code].players:
    #     #     if isinstance(jogador, player.Player):
    #     #         self.bot.send_message(text=text, chat_id=chat_id, parse_mode = 'MARKDOWN')
    #     # print(f"sunflower msg time: {time.time() - t0}")
    #
    #     text = ("Exausted from walking all day, you decided to rest on the base of a tree. You fall asleep and dream of a land where people collectively dream and fights the root of evil together with the power of lucid dreaming. You witness a giant rock with many caves. Each leading to a different dream. One of the cavern walls displays a fading text:")
    #     code = "ZHJlYW1hcmdib3Q="
    #     hidden_char = "█"
    #     random_char_to_show = rd.randint(0, len(code)-1)
    #     hidden_code = ""
    #     i = 0
    #     for ch in code:
    #         if random_char_to_show == i:
    #             hidden_code += ch
    #         else:
    #             hidden_code += hidden_char
    #         i += 1
    #     text += hidden_code + "."
    #     caller = self.server.playersdb.players_and_parties[pt_code]
    #     self.bot.send_message(text=text, chat_id=caller.chat_ids, parse_mode = "MARKDOWN")
    #
    #     # self.server.helper.append_command("start_pt_WB", pt_code)

    def pt_plot_msg_Hal_event(self, pt_code):
        text = emojize(
            "While waling on the deep snow of the forest you witness a mountain, "
            "its completelly covered in snow :snowflake::snowflake::snowflake: "
            "and its summit isnt visible due to the clouds "
            "forming nearby. You got the conclusion that nothing can survive "
            "that weather and decided to step back. It's a dangerous place."
        )
        caller = self.server.playersdb.players_and_parties[pt_code]
        self.server.playersdb.players_and_parties[caller.pt_code].active = True
        self.server.woods.players[caller.pt_code]["active"] = True
        self.bot.send_message(text=text, chat_id=caller.chat_ids, parse_mode = "MARKDOWN")


    def pt_normal_beast(self, pt_code):
        # t0 = time.time()
        grupo = self.server.playersdb.players_and_parties[pt_code]
        tempo = min(self.server.woods.players[pt_code]["rem_time"], self.server.woods.players[pt_code]["stay_time"] - self.server.woods.players[pt_code]["rem_time"])
        tier = 1
        if tempo > self.tier_1:
            tier = 2
        if tempo > self.tier_2:
            tier = 3
        if tempo > self.tier_3:
            tier = 4
        besta = self.server.beastsdb.get_random_beast(tier)
        battle_result = self.battleMan.battle(grupo, besta)
        dead = False

        if battle_result == -1:
            for jogador in grupo.players:
                jogador.exp += 2*jogador.level
                text = emojize(f"Your party found a poor {besta.tipo} and killed it, you gained {2*jogador.level} exp.")
                self.bot.send_message(text=text, chat_id=jogador.chat_id)
                if jogador.classe == "Druid":
                    jogador.beast_in_stack = besta


        elif battle_result == 1:
            # limb_i = jogador.take_damage()
            for jogador in grupo.players:
                jogador.exp += jogador.level
                text = emojize(f"You found a {besta.tipo} and your group lost the fight against it.")
                self.bot.send_message(text=text, chat_id=jogador.chat_id)
                if jogador.classe == "Druid":
                    jogador.beast_in_stack = None
                if besta.area_damage:
                    self.server.playersdb.players_and_parties[jogador.chat_id].take_damage()
                    text = "Everyone in the party has been hit."
                    self.bot.send_message(text=text, chat_id=jogador.chat_id)
            if not besta.area_damage:
                self.aux_deal_damage_to_one_member(grupo)
            # codar o daano em parties

        else:
            for jogador in grupo.players:
                jogador.exp += jogador.level
                text = emojize("You met a foe who you battled for a very long time, as your strengths were evenly matched. "
                               f"Exhausted, you retreated, and so did the {besta.tipo}. "
                               f"You gained {jogador.level} exp")
                self.bot.send_message(text=text, chat_id=jogador.chat_id)


        for jogador in grupo.players:
            if besta.tipo not in jogador.pokedex:
                text = emojize(f"Congratulations, {besta.tipo} has been added to the /bestiary!")
                self.bot.send_message(text=text, chat_id=jogador.chat_id)
                jogador.pokedex.append(besta.tipo)



        # print(f"normal beast time: {time.time() - t0}")

    def pt_legendary_beast(self, pt_code):
        # t0 = time.time()
        grupo = self.server.playersdb.players_and_parties[pt_code]
        besta = self.server.beastsdb.get_random_legbeast()
        battle_result = self.battleMan.battle(grupo, besta)
        dead = False

        if battle_result == -1:
            for jogador in grupo.players:
                jogador.exp += 2*jogador.level
                text = emojize(f"You found a poor {besta.tipo} named {besta.name} and you group killed it, you gained {2*jogador.level} exp.")
                self.bot.send_message(text=text, chat_id=jogador.chat_id)
                if jogador.classe == "Druid":
                    jogador.beast_in_stack = besta



        elif battle_result == 1:
            # limb_i = jogador.take_damage()
            for jogador in grupo.players:
                jogador.exp += jogador.level
                text = emojize(f"You found a {besta.tipo} named {besta.name} and your group lost the fight with it")
                self.bot.send_message(text=text, chat_id=jogador.chat_id)
                if jogador.classe == "Druid":
                    jogador.beast_in_stack = None
                if besta.area_damage:
                    self.server.playersdb.players_and_parties[jogador.chat_id].take_damage()
                    text = text = "Everyone in the party has been hit."
                    self.bot.send_message(text=text, chat_id=jogador.chat_id)
            if not besta.area_damage:
                self.aux_deal_damage_to_one_member(grupo)
            # codar o daano em parties

        else:
            for jogador in grupo.players:
                jogador.exp += jogador.level
                text = emojize("Your group met a foe who battled for a very long time, as your strengths were evenly matched. "
                               f"Exhausted, you retreated, and so did the {besta.tipo} named {besta.name}. "
                               f"You gained {jogador.level} exp")
                self.bot.send_message(text=text, chat_id=jogador.chat_id)
                self.server.playersdb.players_and_parties[jogador.chat_id] = jogador
        for jogador in grupo.players:
            if f"{besta.tipo} named {besta.name}" not in jogador.pokedex:
                text = emojize(f"Congratulations, {besta.tipo} named {besta.name} has been added to the /bestiary!")
                self.bot.send_message(text=text, chat_id=jogador.chat_id)
                jogador.pokedex.append(f"{besta.tipo} named {besta.name}")




    def pt_player_bat(self, pt_code):
        # t0 = time.time()
        grupo = self.server.playersdb.players_and_parties[pt_code]

        found_opponent = False
        if len(self.server.woods.players) > 0:
            other_guy_id = rd.choices(list(self.server.woods.players.keys()))[0]
            active = self.server.woods.players[other_guy_id]["active"]
            count = 0
            found_opponent = True
            while (not active or other_guy_id == pt_code) and count < 10:
                other_guy_id = rd.choices(list(self.server.woods.players.keys()))[0]
                active = self.server.woods.players[other_guy_id]["active"]
                count += 1
                found_opponent = False

            if found_opponent:
                if other_guy_id[0] == "/":
                    other_guy = self.server.playersdb.players_and_parties[other_guy_id]
                else:
                    other_guy = self.server.playersdb.players_and_parties[other_guy_id]
                bres = self.battleMan.battle(grupo, other_guy)
                winner = None
                loser = None

                if bres == -1:
                    winner = grupo
                    loser = other_guy
                    if not isinstance(other_guy, party.Party):
                        exp_gain = 0
                        for jogador in grupo.players:
                            jogador.exp += 2*other_guy.level
                            if jogador.level > exp_gain:
                                exp_gain = jogador.level
                        other_guy.exp += exp_gain
                    else:
                        exp_gain = 0
                        for jogador in grupo.players:
                            if jogador.level > exp_gain:
                                exp_gain = jogador.level
                        exp_gain_other = 0
                        for jogador in other_guy.players:
                            jogador.exp += exp_gain
                            if jogador.level > exp_gain_other:
                                exp_gain_other = jogador.level
                        for jogador in grupo.players:
                            jogador.exp += 2*exp_gain_other

                elif bres == 1:
                    winner = other_guy
                    loser = grupo
                    if not isinstance(other_guy, party.Party):
                        exp_gain = 0
                        for jogador in grupo.players:
                            jogador.exp += other_guy.level
                            if jogador.level > exp_gain:
                                exp_gain = jogador.level
                        other_guy.exp += 2*exp_gain
                    else:
                        exp_gain = 0
                        for jogador in grupo.players:
                            if jogador.level > exp_gain:
                                exp_gain = jogador.level
                        exp_gain_other = 0
                        for jogador in other_guy.players:
                            jogador.exp += 2*exp_gain
                            if jogador.level > exp_gain_other:
                                exp_gain_other = jogador.level
                        for jogador in grupo.players:
                            jogador.exp += exp_gain_other

                else:
                    if not isinstance(other_guy, party.Party):
                        exp_gain = 0
                        for jogador in grupo.players:
                            jogador.exp += other_guy.level
                            if jogador.level > exp_gain:
                                exp_gain = jogador.level
                        other_guy.exp += exp_gain
                    else:
                        exp_gain = 0
                        for jogador in grupo.players:
                            if jogador.level > exp_gain:
                                exp_gain = jogador.level
                        exp_gain_other = 0
                        for jogador in other_guy.players:
                            jogador.exp += exp_gain
                            if jogador.level > exp_gain_other:
                                exp_gain_other = jogador.level
                        for jogador in grupo.players:
                            jogador.exp += exp_gain_other

                if winner:
                    if isinstance(winner, party.Party) and isinstance(loser, party.Party):
                        text = f"In the middle of the forest you found a group named {loser.pt_name} and your group has won the fight."
                        self.bot.send_message(text=text, chat_id=winner.chat_ids)
                        text = f"In the middle of the forest you found a group named {winner.pt_name} and your group has lost the fight."
                        self.aux_deal_damage_to_one_member(loser)
                        self.bot.send_message(text=text, chat_id=loser.chat_ids)
                    elif not isinstance(winner, party.Party):
                        text = f"In the middle of the forest you found {winner.name} and your group has lost the fight."
                        self.aux_deal_damage_to_one_member(loser)
                        self.bot.send_message(text=text, chat_id=loser.chat_ids)
                        text = f"In the middle of the forest you found a group named {loser.pt_name} and you destroyed them"
                        self.bot.send_message(text = text, chat_id=winner.chat_id)
                    else:
                        text = f"In the middle of the forest you found {loser.name} and your group have won the fight."
                        self.bot.send_message(text=text, chat_id=winner.chat_ids)
                        text = f"In the middle of the forest you found a group named {winner.pt_name} and they destroyed you."
                        self.bot.send_message(text = text, chat_id=loser.chat_id)
                        limb_i = loser.take_damage()
                        if isinstance(limb_i, int):
                            if limb_i < 0:
                                self.death.die(loser.chat_id)


                else:
                    if not isinstance(other_guy, party.Party):
                        text = emojize("You met a foe who you battled for a very long time, as your strengths were evenly matched."
                                       f" Exhausted, you retreated, and so did {other_guy.name}.")
                        self.bot.send_message(text=text, chat_id=grupo.chat_ids)
                        text = emojize("You met a foe who you battled for a very long time, as your strengths were evenly matched."
                                       f" Exhausted, you retreated, and so did {grupo.pt_name}.")
                        self.bot.send_message(text=text, chat_id=other_guy.chat_id)

                    else:
                        text = emojize("You met a foe who you battled for a very long time, as your strengths were evenly matched."
                                       f" Exhausted, you retreated, and so did {grupo.pt_name}.")
                        self.bot.send_message(text=text, chat_id=other_guy.chat_ids)
                        text = emojize("You met a foe who you battled for a very long time, as your strengths were evenly matched."
                                       f" Exhausted, you retreated, and so did {other_guy.pt_name}.")
                        self.bot.send_message(text=text, chat_id=grupo.chat_ids)


        if not found_opponent:
            text = "You thought you saw someone sneaking behind you, but it was only your own shadow. You feel lonely."
            self.bot.send_message(text=text, chat_id=grupo.chat_ids)
        # print(f"player battle time: {time.time() - t0}")

    def pt_item(self, pt_code):
        # t0 = time.time()
        grupo = self.server.playersdb.players_and_parties[pt_code]
        bang = self.server.itemsdb.get_random_weapon()
        item = copy.deepcopy(bang)
        # elegigble = []
        # for chat_id,jogador in grupo.players:
        #     if isinstance(jogador,player.Player):
        #         elegigble.append(jogador)
        #random_p = elegigble[rd.randint(0,len(elegigble)-1)]

        # number = 0
        # done = False
        # exeed = False
        #
        # while not done:
        #
        #     for arma in self.server.parties_codes[pt_code]["pt_inv"]:
        #         done = True
        #         if arma.code == item.code:
        #             if number == 0:
        #                 number += 1
        #                 item.code += f"{number}"
        #             elif number < 10:
        #                 number += 1
        #                 item.code = item.code[:-1]
        #                 item.code += f"{number}"
        #
        #             else:
        #                 exeed = True
        #             done = False
        #             break
        # item.ac_code = item.code + f"{number}"
        #
        # temp_ac = item.ac_code
        # item.ac_code = item.code
        # item.code = temp_ac
        number = 0

        old_code = item.code

        for arma in self.server.playersdb.players_and_parties[pt_code].inventory:

            if arma.ac_code == item.ac_code:
                number += 1

                    # if number == 0:
                    #     number += 1
                    #     item.code += f"{number}"
                    # elif number < 10:
                    #     number += 1
                    #     item.code = item.code[:-1]
                    #     item.code += f"{number}"

        if number == 0:
            number = ""

        item.ac_code = item.code + f"{number}"

        temp_ac = item.ac_code
        item.ac_code = item.code
        item.code = temp_ac
        item.owner = ""
        self.server.playersdb.players_and_parties[pt_code].inventory.append(copy.deepcopy(item))
        text = emojize(f"While wandering in the woods, your party found *{item.name}* and added it to the shared inventory!")
        self.bot.send_message(text=text, chat_id=grupo.chat_ids, parse_mode='MARKDOWN')

        if item.is_legendary:
            item.code = old_code
            self.server.itemsdb.remove_weapon_from_pool(item)


        # print(f"item time: {time.time() - t0}")

    def pt_dungeon(self, pt_code):
        # party = self.server.playersdb.players_and_parties[pt_code]
        # if not party.last_done_dungeon_time_pt:
        #     party.last_done_dungeon_time_pt = time.time()
        # else:
        #     delta_t = time.time()-party.last_done_dungeon_time_pt
        #     party.average_times_taken_pt.append(delta_t)
        #     party.average_time_between_dungeons_pt = sum(party.average_times_taken_pt)/len(party.average_times_taken_pt)
        #     party.average_time_between_last_dungeons_pt = sum(party.average_times_taken_pt[-5:])/len(party.average_times_taken_pt[-5:])
        # party.average_time_between_WB_pt = party.average_time_between_dungeons_pt*5
        self.server.helper.append_command("start_dg", pt_code)
        # Precisa codar as dungeons para parties

    def pt_df(self, pt_code):

        # self.server.helper.append_command("start_df", pt_code)

        tempo = min(self.server.woods.players[pt_code]["rem_time"], self.server.woods.players[pt_code]["stay_time"] - self.server.woods.players[pt_code]["rem_time"])

        if tempo > self.tier_3:
            self.server.helper.append_command("start_df", pt_code)
        else:
            self.server.helper.append_command("start_dg", pt_code)

    def caverns(self, pt_code):
        self.server.helper.append_command("start_caverns", pt_code)

    def pt_map(self, pt_code):
        # t0 = time.time()

        def hasmap(inventory, map_type):
            n = 0
            for invitem in inventory:
                if invitem.type == "map":
                    if invitem.map_type == map_type:
                        n += 1
            if n > 4:
                return True
            return False
        maps_choices = copy.deepcopy(items.dg_map.possibles_maps)
        grupo = self.server.playersdb.players_and_parties[pt_code]
        item = None
        while item == None and maps_choices:
            map = rd.choice(maps_choices)
            map_type = map[4]
            if hasmap(grupo.inventory, map_type):
                maps_choices.remove(map)
            else:
                item = items.dg_map(*map)

        #
        # grupo = self.server.playersdb.players_and_parties[pt_code]
        # item = items.dg_map(emojize("Dusty map :world_map:"), 0, "dstmp", 1)
        #
        # has_map = False
        #
        # for inv_item in self.server.playersdb.players_and_parties[pt_code].inventory:
        #
        #     if inv_item.code == "dstmp":
        #         has_map = True
        #         break
        text = ""
        if item:


            self.server.playersdb.players_and_parties[pt_code].inventory.append(copy.deepcopy(item))
            if item.map_type == "dg_map":
                text = f"While walking around the forest, someone from {self.server.playersdb.players_and_parties[pt_code].pt_name} tripped over a small bottle. Inside it you found a dusty piece of paper containing some strange drawings. You think it might be a map leading to somewhere interesting, probably a dungeon of some sort. It could take some time to get there, though. Better prepare yourself before going!"
            elif item.map_type == "deep_forest_map":
                text = f"While walking around the forest, someone from {self.server.playersdb.players_and_parties[pt_code].pt_name} tripped over a small bottle. Inside it you found a dusty piece of paper containing some strange drawings. You think it might be a map leading to somewhere interesting, probably a deeper part of the forest. It could take some time to get there, though. Better prepare yourself before going!"
            self.bot.send_message(text=text,chat_id=grupo.chat_ids)
        else:
            text = "You just found another dusty map! What a day! But as you study, your old map is the same as your new, so you threw it away."
            self.bot.send_message(text=text,chat_id=grupo.chat_ids)
        # hasmap = False
        # for chat_id,jogador in grupo.players:
        #     if isinstance(jogador,player.Player):
        #         elegigble.append(jogador)
        # random_p = elegigble[rd.randint(0,len(elegigble)-1)]
        # for invitem in random_p.inventory:
        #     if isinstance(invitem, items.dg_map):
        #         hasmap = True
        #         break
        # if not hasmap:
        #     random_p.inventory.append(item)
        #     text = ("While walking around the forest, you tripped over a small bottle. Inside it you found a dusty piece of paper containing some strange drawings. You think it might be a map leading to somewhere interesting, probably a dungeon of some sort. It could take some time to get there, though. Better prepare yourself before going!")
        #     self.bot.send_message(text=text, chat_id=random_p.chat_id)
        # else:
        #     text = "You just found another dusty map! What a day! But as you study, your old map is the same as your new, so you threw it away."
        #     self.bot.send_message(text=text, chat_id=random_p.chat_id)
        # print(f"map encounter time: {time.time() - t0}")

        del item

    def sanctu(self, pt_code):
        for jog in self.server.playersdb.players_and_parties[pt_code].players:
            if jog.classe == "Unknown":
                text = "While walking around the woods you found a strange structure, there you see people meditating, you still dont know how to meditate, so you continued on your journey."
                self.bot.send_message(text=text,chat_id=jog.chat_id)
            else:
                jog.sanctuary()
