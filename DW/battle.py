#####################################
#  Classe que gerencia as batalhas  #
#####################################

import random as rd
import math
import bot
import player
from emoji import emojize


class BattleMan:
    def __init__(self, server):
        self.bot = bot.TGBot()
        self.server = server

    def pt_battle_pt_vs_single(self, group, single):

        if single.defense < 1:
            single.defense = 1
        order = []
        def_ord = ["Unknown", "Druid", "Knight", "Wizard", "Explorer"]
        pt_hp = 0
        pt_def = 0
        for chat_id, jogador in group.items():
            if isinstance(jogador, player.Player):
                if jogador.defense < 1:
                    jogador.defense = 1
                order.append(jogador)
                hp_self = 0
                for limb in jogador.hp:
                    hp_self += limb.health
                pt_hp += 3*hp_self
                pt_def += jogador.defense

        if isinstance(single.hp, int):
            hp_single = 3*single.hp
        else:
            hp_single = 0
            for limb in single.hp:
                hp_single += 3*limb.health

        turns = 0
        while hp_single > 0 and pt_hp > 0 and turns < 14:
            for jogador in order:
                if jogador.classe == "Wizard" and jogador.is_casting.ready:
                    hp_single -= jogador.is_casting.damage
                    jogador.is_casting.ready = False
                    s = f"You cast a fireball on {single.tipo}"
                    fires = jogador.spell_power
                    for i in range(fires):
                        loc = rd.randint(0,len(s))
                        s1 = s[:loc]
                        s2 = s[loc:]
                        s1+=(emojize(":fire:"))
                        s = s1+s2
                    self.bot.send_message(text=s, chat_id=jogador.chat_id)

                if jogador.classe == "Knight":
                    j_dado = rd.randint(jogador.crit_chance, 20)
                else:
                    j_dado = rd.randint(1, 20)
                if j_dado > 10:
                    hp_single -= math.ceil(3*jogador.atk/single.defense)
                if j_dado == 20:
                    hp_single -= math.ceil(3*jogador.atk)
                    self.bot.send_message(text=emojize(":high_voltage: You dealt critical damage! :high_voltage:"), chat_id=jogador.chat_id)

            if isinstance(single, player.Wizard):
                if single.is_casting:
                    pt_hp -= (50 + 50*single.spell_power)*3
                    single.is_casting = ""
            if isinstance(single, player.Knight):
                j_dado = rd.randint(single.crit_chance, 20)
            else:
                j_dado = rd.randint(1, 20)
            if j_dado > 10:
                pt_hp -= math.ceil(3*single.atk/pt_def)
            if j_dado == 20:
                pt_hp -= math.ceil(3*single.atk)
            turns += 1

        if hp_single < pt_hp:
            if isinstance(single, player.Player):
                if single.buff_man.buff_state > 0:
                    single.buff_man.buff_state -= 1
                    single.calc_attributes()
                    for chat,jog in group.items():
                        if jog.buff_man.buff_state < len(jog.buff_man.states_list) - 1:
                            jog.buff_man.buff_state += 1
                            jog.calc_attributes()
            return 1
        elif pt_hp < hp_single:
            damaged = None
            invalidos = []
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
                    l = rd.randint(len(order))
                    damaged = order[l]


                            # self.server.playersdb.players[jogador.chat_id].take_damage()
                            # text = f"You have been hit!"
                            # self.bot.send_message(text = text, chat_id = jogador.chat_id)
                            # if jogador.buff_man.buff_state > 0:
                            #     jogador.buff_man.buff_state -= 1
                            #     jogador.calc_attributes()
                            #     if isinstance(single,player.Player):
                            #         if single.buff_man.buff_state < len(single.buff_man.states_list) - 1:
                            #             single.buff_man.buff_state += 1
                            #             single.calc_attributes()
            if damaged:
                jogador = damaged
                self.server.playersdb.players[jogador.chat_id].take_damage()
                text = f"You have been hit!"
                self.bot.send_message(text = text, chat_id = jogador.chat_id)
                if jogador.buff_man.buff_state > 0:
                    jogador.buff_man.buff_state -= 1
                    jogador.calc_attributes()
                    if isinstance(single,player.Player):
                        if single.buff_man.buff_state < len(single.buff_man.states_list) - 1:
                            single.buff_man.buff_state += 1
                            single.calc_attributes()

                return 2
        else:
            return 3



    def pt_battle_pt_vs_pt(self, group1, group2):
        order1 = []
        def_ord = ["Unknown", "Druid", "Knight", "Wizard", "Explorer"]
        pt1_hp = 0
        pt1_def = 0
        for chat_id, jogador in group1.items():
            if isinstance(jogador, player.Player):
                if jogador.defense < 1:
                    jogador.defense = 1
                order1.append(jogador)
                hp_self = 0
                for limb in jogador.hp:
                    hp_self += limb.health
                pt1_hp += hp_self
                pt1_def += jogador.defense

        order2 = []
        pt2_hp = 0
        pt2_def = 0
        for chat_id, jogador in group2.items():
            if isinstance(jogador, player.Player):
                if jogador.defense < 1:
                    jogador.defense = 1
                order2.append(jogador)
                hp_self = 0
                for limb in jogador.hp:
                    hp_self += limb.health
                pt2_hp += hp_self
                pt2_def += jogador.defense


        turns = 0
        while pt1_hp > 0 and pt2_hp > 0 and turns < 14:
            turns += 1
            i = 0
            for jogador in order1:
                i+=1
                if jogador.classe == "Wizard" and jogador.is_casting.ready:
                    pt2_hp -= jogador.is_casting.damage
                    jogador.is_casting.ready = False
                    temp = "name"
                    s = f"You cast a fireball on {group2[temp]}"
                    fires = jogador.spell_power
                    for i in range(fires):
                        loc = rd.randint(0,len(s))
                        s1 = s[:loc]
                        s2 = s[loc:]
                        s1+=(emojize(":fire:"))
                        s = s1+s2
                    self.bot.send_message(text=s, chat_id=jogador.chat_id)
                if jogador.classe == "Knight":
                    j_dado = rd.randint(jogador.crit_chance, 20)
                else:
                    j_dado = rd.randint(1, 20)
                if j_dado > 10:
                    pt2_hp -= math.ceil(3*jogador.atk/pt2_def)
                if j_dado == 20:
                    pt2_hp -= math.ceil(3*jogador.atk)
                    self.bot.send_message(text=emojize("You performed a critical attack :high_voltage:"), chat_id=jogador.chat_id)

            for jogador in order2:
                if jogador.classe == "Wizard" and jogador.is_casting:
                    pt1_hp -= (50 + 50*jogador.spell_power)*3
                    jogador.is_casting = ""
                    temp = "name"
                    s = f"You cast a fireball on {group1[temp]}"
                    fires = jogador.spell_power
                    for i in range(fires):
                        loc = rd.randint(0,len(s))
                        s1 = s[:loc]
                        s2 = s[loc:]
                        s1+=(emojize(":fire:"))
                        s = s1+s2
                    self.bot.send_message(text=s, chat_id=jogador.chat_id)
                if jogador.classe == "Knight":
                    j_dado = rd.randint(jogador.crit_chance, 20)
                else:
                    j_dado = rd.randint(1, 20)
                if j_dado > 10:
                    pt1_hp -= math.ceil(3*jogador.atk/pt1_def)
                if j_dado == 20:
                    pt1_hp -= math.ceil(3*jogador.atk)
                    self.bot.send_message(text=emojize("You performed a critical attack :high_voltage:"), chat_id=jogador.chat_id)



        if pt1_hp > pt2_hp:
            for cla in def_ord:
                for jogador in order2:
                    if jogador.classe == cla:
                        self.server.playersdb.players[jogador.chat_id].take_damage()     # Precisa conferir se o treco ta funcionando (ta de fato tirando o hp do jagador)
                        text = f"You have been hit!"
                        self.bot.send_message(text = text, chat_id = jogador.chat_id)
                        if jogador.buff_man.buff_state > 0:
                            jogador.buff_man.buff_state -= 1
                            jogador.calc_attributes()
                            for chat,jog in group1.items():
                                if jog.buff_man.buff_state < len(jog.buff_man.states_list) - 1:
                                    jog.buff_man.buff_state += 1
                                    jog.calc_attributes()
                        return 1
        elif pt1_hp < pt2_hp:
            for cla in def_ord:
                for jogador in order1:
                    if jogador.classe == cla:
                        self.server.playersdb.players[jogador.chat_id].take_damage()     # Precisa conferir se o treco ta funcionando (ta de fato tirando o hp do jagador)
                        text = f"You have been hit!"
                        self.bot.send_message(text = text, chat_id = jogador.chat_id)
                        if jogador.buff_man.buff_state > 0:
                            jogador.buff_man.buff_state -= 1
                            jogador.calc_attributes()
                            for chat,jog in group2.items():
                                if jog.buff_man.buff_state < len(jog.buff_man.states_list) - 1:
                                    jog.buff_man.buff_state += 1
                                    jog.calc_attributes()
                        return 2
        else:
            return 3




    def battle(self, thing1, thing2):  # 1 for thing1, 2 fo thing 2
        if isinstance(thing1, dict) and not isinstance(thing2, dict):
            return self.pt_battle_pt_vs_single(thing1, thing2)
        elif not isinstance(thing1, dict) and isinstance(thing2, dict):
            x = self.pt_battle_pt_vs_single(thing2, thing1)
            if x == 1:
                x = 2
            elif x == 2:
                x = 1
            return x
        elif isinstance(thing1, dict) and isinstance(thing2, dict):
            return self.pt_battle_pt_vs_pt(thing1, thing2)
        t3 = 1

        if thing1.defense < 1:
            thing1.defense = 1
        if thing2.defense < 1:
            thing2.defense = 1

        if isinstance(thing2.hp, int):
            t1 = 0
            for i in thing1.hp:
                t1 += i.health*3
            t2 = thing2.hp*3

            while t1 > 0 and t2 > 0 and t3 < 14:

                if thing1.classe == "Wizard" and thing1.is_casting:
                    t2 -= (50 + 50*thing1.spell_power)*3
                    thing1.is_casting = ""
                    s = f"You cast a fireball on {thing2.tipo}"
                    fires = thing1.spell_power
                    for i in range(fires):
                        loc = rd.randint(0,len(s))
                        s1 = s[:loc]
                        s2 = s[loc:]
                        s1+=(emojize(":fire:"))
                        s = s1+s2
                    self.bot.send_message(text=s, chat_id=thing1.chat_id)

                dado1 = rd.randint(1, 20)
                dado2 = rd.randint(1, 20)
                if isinstance(thing1, player.Knight):
                    dado2 = rd.randint(thing1.crit_chance, 20)
                if dado1 > 10:
                    t1 -= math.ceil(3*thing2.atk/thing1.defense)
                if dado2 > 10:
                    t2 -= math.ceil(3*thing1.atk/thing2.defense)
                if dado1 == 20:
                    t1 -= math.ceil(3*thing2.atk)
                if dado2 == 20:
                    t2 -= math.ceil(3*thing1.atk)
                    self.bot.send_message(text=emojize("You performed a critical attack :high_voltage:"), chat_id=thing1.chat_id)
                t3 += 1
            if t3 > 13:
                return 3
            elif t2 == t1:
                return 3
            elif t1 > t2:
                return 1
            else:
                if thing1.buff_man.buff_state > 0:
                    thing1.buff_man.buff_state -= 1
                    thing1.calc_attributes()
                return 2
        else:
            t1 = 0
            for i in thing1.hp:
                t1 += i.health*3
            t2 = 0
            for i in thing2.hp:
                t2 += i.health*3



            while t1 > 0 and t2 > 0 and t3 < 14:


                if thing1.classe == "Wizard" and thing1.is_casting:
                    t2 -= (50 + 50*thing1.spell_power)*3
                    thing1.is_casting = ""
                    s = f"You cast a fireball on {thing2.name}"
                    fires = thing1.spell_power
                    for i in range(fires):
                        loc = rd.randint(0,len(s))
                        s1 = s[:loc]
                        s2 = s[loc:]
                        s1+=(emojize(":fire:"))
                        s = s1+s2
                    self.bot.send_message(text=s, chat_id=thing1.chat_id)
                if thing2.classe == "Wizard" and thing2.is_casting:
                    t1 -= (50 + 50*thing2.spell_power)*3
                    thing2.is_casting = ""
                    s = f"You cast a fireball on {thing1.name}"
                    fires = thing2.spell_power
                    for i in range(fires):
                        loc = rd.randint(0,len(s))
                        s1 = s[:loc]
                        s2 = s[loc:]
                        s1+=(emojize(":fire:"))
                        s = s1+s2
                    self.bot.send_message(text=s, chat_id=thing2.chat_id)


                if isinstance(thing2, player.Knight):
                    dado1 = rd.randint(thing2.crit_chance, 20)
                else:
                    dado1 = rd.randint(1, 20)
                if isinstance(thing1, player.Knight):
                    dado2 = rd.randint(thing1.crit_chance, 20)
                else:
                    dado2 = rd.randint(1, 20)
                if dado1 > 10:
                    t1 -= math.ceil(3*thing2.atk/thing1.defense)
                if dado2 > 10:
                    t2 -= math.ceil(3*thing1.atk/thing2.defense)
                if dado1 == 20:
                    t1 -= math.ceil(3*thing2.atk)
                    self.bot.send_message(text=emojize("You performed a critical attack :high_voltage:"), chat_id=thing2.chat_id)

                if dado2 == 20:
                    t2 -= math.ceil(3*thing1.atk)
                    self.bot.send_message(text=emojize("You performed a critical attack :high_voltage:"), chat_id=thing1.chat_id)

                t3 += 1
            if t3 > 13:
                return 3
            elif t2 == t1:
                return 3
            elif t1 > t2:
                if thing2.buff_man.buff_state > 0:
                    thing2.buff_man.buff_state -= 1
                    thing2.calc_attributes()
                    if thing1.buff_man.buff_state < len(thing1.buff_man.states_list) - 1:
                        thing1.buff_man.buff_state += 1
                        thing1.calc_attributes()
                return 1
            else:
                if thing1.buff_man.buff_state > 0:
                    thing1.buff_man.buff_state -= 1
                    thing1.calc_attributes()
                    if thing2.buff_man.buff_state < len(thing2.buff_man.states_list) - 1:
                        thing2.buff_man.buff_state += 1
                        thing2.calc_attributes()
                return 2
