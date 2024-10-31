#####################################
#  Classe que processa as dungeons  #
#####################################

import os
import bot
import battle2
import death
from emoji import emojize
import player_comms
import player
import copy
import random as rd


class DungeonManager:
    '''
        Classe principal controladora de dungeons.
    '''
    def __init__(self, server):
        '''
            Neste caso, ele vai controlar comandos do jogador, a batalha, o bote, a morte e os keyboards
        '''
        self.server = server
        self.commander = player_comms.PlayerComms(server)
        self.battleman = battle2.BattleMan(server)
        self.bot = bot.TGBot()
        #self.playerComs = player_comms.PlayerComms(server)
        self.dona_morte = death.Death(server)
        self.def_wait_time = 60
        self.dgkb = self.server.keyboards.inline_dg_reply_markup
        self.defkb = self.server.keyboards.class_main_menu_reply_markup

        self.dgs_file = "dbs/dgs.dat"
        self.dungeons_in_progress = {}
        loaded = self.server.helper.load_pickle(self.dgs_file)
        if loaded:
            self.dungeons_in_progress = loaded

    def dungeon_iteration(self, chat_id, text, msg_id):
        '''
            Função controladora principal das dungeons solo. Que, dependendo do chat_id do jogador, e do texto, ele interpreta a dungeon.
        '''
        textinho = ""
        if chat_id in self.dungeons_in_progress:                    # Primeiro ele confere se o jogador está nas dg em progresso
            if msg_id != text:
                self.dungeons_in_progress[chat_id]["msgs_id"][chat_id] = msg_id
            jogador = self.server.playersdb.players_and_parties[chat_id]
            dungeon = self.dungeons_in_progress[chat_id]["dungeon"] # E já define as variáveis para não ter que ficar chamando o nome inteiro.
            dnpc = self.dungeons_in_progress[chat_id]["dnpc"]

            if text == emojize("YES :thumbs_up:") or text in self.server.playersdb.players_and_parties[chat_id].actions:        # Ele ve se quer continuar ou se jogou um dos comandos de classe
                self.server.woods.players[chat_id]["active"] = False
                if text in self.server.playersdb.players_and_parties[chat_id].actions:
                    self.server.playersdb.players_and_parties[chat_id].actions[text]()      # Executa o comando de classe se jogou um

                besta = dungeon.beasts[dnpc]
                bres = self.battleman.battle(jogador, besta)            # Executa a batalha da besta com o jogador.
                dead = False
                exit = False

                if not besta.is_legendary:          # Se a besta for lendária, é um boss, caso contrário, é só um inimigo normal
                    if bres == -1:                   # Vitória.
                        jogador.exp += 2*dungeon.level

                        textinho += emojize(f"You found a poor {besta.tipo} and killed it, you gained "
                                       f"{2*dungeon.level} exp.\n\n")
                        #self.bot.send_message(text=text, chat_id=jogador.chat_id)
                        self.dungeons_in_progress[chat_id]["dnpc"] += 1             # Passa de nível na dungeon
                        if jogador.classe == "Druid":
                            jogador.beast_in_stack = besta                          # Druida pode pegar a besta se derrotar ela.

                    else:                 # Derrota.
                        jogador.exp += dungeon.level
                        limb_i = jogador.take_damage()      # Toma dano
                        if jogador.classe == "Druid":
                            jogador.beast_in_stack = None   # Druida perde a besta

                        if isinstance(limb_i, int):

                            textinho += emojize(f"You found a {besta.tipo} and it destroyed your {jogador.hp[limb_i].name}"
                                           f", you gained {dungeon.level} exp.\n\n")
                            #self.bot.send_message(text=text, chat_id=jogador.chat_id)

                            if limb_i < 0:
                                dead = True                 # Checa se o jogador morreu na dungeon
                        else:
                            textinho += emojize(f"You found a {besta.tipo} and it killed your {limb_i}"     # se não for um inteiro, é uma string e significa que uma besta do druida morreu
                                           f":loudly_crying_face:, you gained {dungeon.level} exp.\n\n")
                            #self.bot.send_message(text=text, chat_id=jogador.chat_id)

                    # else:                           # Empate
                    #     jogador.exp += dungeon.level
                    #
                    #     textinho += emojize(f"You met a foe who you battled for a very long time, as your strengths were evenly matched. "
                    #                    f"Exhausted, you retreated, and so did the {besta.tipo}. "
                    #                    f"You gained {dungeon.level} exp.\n\n")
                        #self.bot.send_message(text=text, chat_id=jogador.chat_id)

                    # if besta.tipo not in jogador.pokedex:
                    #         textinho += emojize(f"Congratulations, {besta.tipo} has been added to the /bestiary!\n\n")
                    #         #self.bot.send_message(text=text, chat_id=chat_id)
                    #         jogador.pokedex.append(besta.tipo)

                    if not dead:
                        # Se o jogador n morreu ele printa a vida e o estado de buff
                        #self.playerComs.show_health(jogador)
                        s = ""
                        for limb in jogador.hp:
                            s += emojize(f"Your {limb.name} is {limb.states[limb.health]}\n")
                        textinho += s + "\n"

                        if jogador.buff_man.buff_state > 0:
                            textinho += f"Buff: {jogador.buff_man.states_list[jogador.buff_man.buff_state]}\n\n"

                        #self.bot.send_message(text=s, chat_id=caller.chat_id)
                        #self.server.playersdb.players_and_parties[chat_id].print_self_coms()
                        textinho += self.server.playersdb.players_and_parties[chat_id].dg_coms()
                        textinho += "Would you like to continue? You have 2 minutes to decide."
                        #self.bot.send_message(text=text, chat_id=jogador.chat_id, reply_markup=self.dgkb)

                else:               # Besta lendária, é um boss
                    if bres == -1:                       # Vitória
                        jogador.exp += 4*dungeon.level
                        if jogador.classe == "Druid":
                            jogador.beast_in_stack = besta  # Druidas podem domesticar bosses
                        for i in dungeon.rewards:
                            item = copy.deepcopy(i)         # Joga as recompensas no inventário do jogador
                            number = 0


                            for arma in jogador.inventory:

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
                            # done = False
                            # number = 0
                            # exeed = False
                            # while not done:
                            #
                            #     for arma in jogador.inventory:
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
                            # if not exeed:
                            item.owner = chat_id
                            jogador.inventory.append(copy.deepcopy(item))
                            # else:
                            #     textinho += "Crumbled inventory, aborting\n"


                        textinho += emojize(f"You found a legendary {besta.tipo} named {besta.name} and killed it, you gained "
                                       f"{4*dungeon.level} exp *and some items*! Go check your /inv entory!\n\n")

                        # self.bot.send_message(text=text, chat_id=jogador.chat_id, parse_mode='MARKDOWN', reply_markup=self.defkb)

                    else:                        # Derrota
                        if jogador.classe == "Druid":
                            jogador.beast_in_stack = None   # Druida perde a besta
                        limb_i = jogador.take_damage()
                        jogador.exp += 2*dungeon.level

                        if isinstance(limb_i, int):
                            textinho += emojize(f"You found a legendary {besta.tipo} named {besta.name} and it destroyed"
                                           f" your {jogador.hp[limb_i].name}, you gained {2*dungeon.level} exp.\n\n")
                            #self.bot.send_message(text=text, chat_id=jogador.chat_id)

                            if limb_i < 0:
                                dead = True         # Dead, not big surprise

                        else:
                            textinho += emojize(f"You found a legendary {besta.tipo} named {besta.name} and it killed"
                                           f" your {limb_i} :loudly_crying_face:, you gained {2*dungeon.level} exp.\n\n")
                            #self.bot.send_message(text=text, chat_id=jogador.chat_id)

                    # else:                               # Empate
                    #     jogador.exp += 2*dungeon.level
                    #
                    #     textinho += emojize(f"You met a foe who you battled for a very long time, as your strengths were evenly matched. "
                    #                    f"Exhausted, you retreated, and so did the legendary {besta.tipo} named {besta.name}. "
                    #                    f"You gained {2*dungeon.level} exp.\n\n")
                        #self.bot.send_message(text=text, chat_id=jogador.chat_id)

                    if f"{besta.tipo} named {besta.name}" not in jogador.pokedex:           # Somente bosses entram na pokedex
                        textinho += emojize(f"Congratulations, {besta.tipo} named {besta.name} has been added to the /bestiary!\n\n")
                        #self.bot.send_message(text=text, chat_id=chat_id)
                        jogador.pokedex.append(f"{besta.tipo} named {besta.name}")

                    if not dead:            # Caso o jogador n esteja morto ele mostra a vida e pergunta se quer continuar
                        s = ""
                        for limb in jogador.hp:
                            s += emojize(f"Your {limb.name} is {limb.states[limb.health]}\n")

                        if jogador.buff_man.buff_state > 0:
                            textinho += f"Buff: {jogador.buff_man.states_list[jogador.buff_man.buff_state]}\n\n"

                        textinho += s + "\n"
                        if bres != -1:
                            textinho += self.server.playersdb.players_and_parties[chat_id].dg_coms()
                            text += "Would you like to continue? You have 2 minutes to decide."
                            #self.server.playersdb
                            #self.bot.send_message(text=text, chat_id=jogador.chat_id, reply_markup=self.dgkb)
                        else:
                            self.server.woods.players[chat_id]["active"] = True
                            del self.dungeons_in_progress[chat_id]

                            exit = True

                textinho = textinho.replace("_", "\\_")

                if dead: # Not big surprise
                    del self.dungeons_in_progress[chat_id]
                    self.server.woods.remove_from_woods(chat_id)
                    self.dona_morte.die(chat_id)
                    self.bot.edit_message(text=textinho, chat_id=chat_id, reply_markup=self.defkb, parse_mode="MARKDOWN", message_id = self.dungeons_in_progress[chat_id]["msgs_id"][chat_id])
                    return 1

                if exit:
                    self.bot.send_message(text=textinho, chat_id=chat_id, reply_markup=self.defkb, parse_mode="MARKDOWN")
                    return False
                else:
                    self.bot.edit_message(text=textinho, chat_id=chat_id, reply_markup=self.dgkb, parse_mode="MARKDOWN", message_id = self.dungeons_in_progress[chat_id]["msgs_id"][chat_id])
                    return 2*self.def_wait_time

            elif text == emojize("NOPE :thumbs_down:"):                             # Caso o jogador desista da dungeon
                textinho = "It's a dangerous place, so you decided to step back."
                self.bot.send_message(text=textinho, chat_id=jogador.chat_id, reply_markup=self.defkb)
                self.server.woods.players[chat_id]["active"] = True
                del self.dungeons_in_progress[chat_id]
                return False

            else:
                return 2*self.def_wait_time

        else:
            self.server.woods.players[chat_id]["active"] = True

            return False

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
                l = rd.randint(len(order))
                damaged = order[l]
        limb_i = self.server.playersdb.players_and_parties[damaged.chat_id].take_damage()
        if isinstance(limb_i, int):
            if limb_i < 0:
                self.death.die(damaged.chat_id)
        text = "You have been hit."
        # self.bot.send_message(text=text, chat_id=damaged.chat_id)

    def pt_dungeon_iteration(self, chat_id, code, text, msg_id):
        '''
            Função controladora principal das dungeons em party. Que, dependendo do chat_id do jogador, e do texto, ele interpreta a dungeon.
            É a mesma coisa que o solo mas nesta, ele recebe o chat_id do jogador que deu o comando e o código da party.

            E tbm fica um pouco mais complexa
        '''

        textinho = ""
        if code in self.dungeons_in_progress:
            if msg_id != text:
                self.dungeons_in_progress[code]["msgs_id"][chat_id] = msg_id
            group = self.server.playersdb.players_and_parties[code]
            dungeon = self.dungeons_in_progress[code]["dungeon"]
            dnpc = self.dungeons_in_progress[code]["dnpc"]
            to_die = []
            if text == emojize("YES :thumbs_up:") or text in self.server.playersdb.players_and_parties[chat_id].actions or text[:5] in self.server.playersdb.players_and_parties[chat_id].actions:      # ele executa os comandos das ações dos jogadores aqui
                self.server.woods.players[code]["active"] = False
                self.server.playersdb.players_and_parties[code].active = False
                if text in self.server.playersdb.players_and_parties[chat_id].actions or text[:5] in self.server.playersdb.players_and_parties[chat_id].actions:
                    if self.server.playersdb.players_and_parties[chat_id].pt_code:
                        if self.server.playersdb.players_and_parties[chat_id].classe == "Explorer":
                            if text[:5] == "/heal":
                                target_chat = text[6:]
                                if target_chat:
                                    if target_chat in self.server.playersdb.players_and_parties[self.server.playersdb.players_and_parties[chat_id].pt_code].chat_ids:
                                        self.commander.heal_in_pt(target_chat, self.server.playersdb.players_and_parties[chat_id].chat_id, 3)   # Neste caso, é o comando de cura do explorer
                                    else:
                                        self.bot.send_message(text="Player not found! Aborting.", chat_id = self.server.playersdb.players_and_parties[chat_id].chat_id)
                                else:
                                    self.server.playersdb.players_and_parties[chat_id].actions[text]()
                        elif self.server.playersdb.players_and_parties[chat_id].classe == "Wizard":

                            if text[:5] == "/heal":
                                target_chat = text[6:]
                                if target_chat:
                                    if target_chat in self.server.playersdb.players_and_parties[self.server.playersdb.players_and_parties[chat_id].pt_code].chat_ids:
                                        self.commander.heal_in_pt(target_chat, self.server.playersdb.players_and_parties[chat_id].chat_id, self.server.playersdb.players_and_parties[chat_id].buff_man.buff_state+1) # Cura do wizard
                                    else:
                                        self.bot.send_message(text="Player not found! Aborting.", chat_id = self.server.playersdb.players_and_parties[chat_id].chat_id)
                                else:
                                    self.server.playersdb.players_and_parties[chat_id].actions[text]()
                            elif text[:5] == "/buff":

                                target_chat = text[6:]
                                if target_chat:
                                    if target_chat in self.server.playersdb.players_and_parties[self.server.playersdb.players_and_parties[chat_id].pt_code].chat_ids:
                                        self.commander.buff_in_pt(target_chat, self.server.playersdb.players_and_parties[chat_id].chat_id, self.server.playersdb.players_and_parties[chat_id].spell_power)  # Buff do Wizard
                                    else:
                                        self.bot.send_message(text="Player not found! Aborting.", chat_id = self.server.playersdb.players_and_parties[chat_id].chat_id)
                                else:
                                    self.server.playersdb.players_and_parties[chat_id].actions[text]()
                            else:
                                self.server.playersdb.players_and_parties[chat_id].actions[text]()
                        else:
                            self.server.playersdb.players_and_parties[chat_id].actions[text]()
                    else:
                        self.server.playersdb.players_and_parties[chat_id].actions[text]()
                besta = dungeon.beasts[dnpc]
                bres = self.battleman.battle_pt_vs_beast(group, besta)
                dead = False
                exit = False

                if not besta.is_legendary:          # N é um boss
                    if bres == -1:                   # Vitória
                        for jog in self.server.playersdb.players_and_parties[code].players:
                            jog.exp += 2*dungeon.level
                            if jog.classe == "Druid":
                                jog.beast_in_stack = besta

                        textinho += emojize(f"Your party found a poor {besta.tipo} and killed it, you gained "
                                       f"{2*dungeon.level} exp.\n\n")
                        #self.bot.send_message(text=text, chat_id=jogador.chat_id)
                        self.dungeons_in_progress[code]["dnpc"] += 1

                    else:         # Derrota

                        for jog in self.server.playersdb.players_and_parties[code].players:    # Itera em tudo
                            jog.exp += dungeon.level
                            if besta.area_damage:
                                text = "Everyone in the party has been hit."
                                jog.take_damage()
                                # self.bot.send_message(text = text, chat_id = jog.chat_id)
                            if jog.classe == "Druid":
                                jog.beast_in_stack = None


                        #limb_i = jogador.take_damage()
                                hp = 0
                                for limb in jog.hp:
                                    hp+=limb.health
                                if hp == 0:
                                    to_die.append(jog)
                                    dead = True
                                self.server.playersdb.players_and_parties[jog.chat_id] = jog






                        textinho += emojize(f"Your party found a {besta.tipo} and your group lost the fight"
                                       f", you gained {dungeon.level} exp.\n\n")
                        #self.bot.send_message(text=text, chat_id=jogador.chat_id)

                        if not besta.area_damage:
                            self.aux_deal_damage_to_one_member(group)
                    #
                    # else:           # Empate
                    #     for jog in self.server.playersdb.players_and_parties[code].players:
                    #         jog.exp += dungeon.level
                    #
                    #     textinho += emojize(f"Your party met a foe who you battled for a very long time, as your strengths were evenly matched. "
                    #                    f"Exhausted, you retreated, and so did the {besta.tipo}. "
                    #                    f"You gained {dungeon.level} exp.\n\n")
                        #self.bot.send_message(text=text, chat_id=jogador.chat_id)

                    # if besta.tipo not in jogador.pokedex:
                    #         textinho += emojize(f"Congratulations, {besta.tipo} has been added to the /bestiary!\n\n")
                    #         #self.bot.send_message(text=text, chat_id=chat_id)
                    #         jogador.pokedex.append(besta.tipo)

                    if not dead:                # Se n tiver morto, ele vai printar tudo
                        #self.playerComs.show_health(jogador)
                        s = ""
                        tt_hp = 0
                        for jog in self.server.playersdb.players_and_parties[code].players:
                            emoji = ":green_heart:"
                            j_hp = 0
                            for limb in jog.hp:
                                j_hp += limb.health
                            if j_hp < 5:
                                emoji = ":yellow_heart:"
                            if j_hp < 2:
                                emoji = ":red_heart:"
                            s += emojize(f"{jog.name}, '''{jog.chat_id}'''':\n*Health*: {j_hp}{emoji} {jog.classe}\n")
                            s += f"*Buff*: {jog.buff_man.states_list[jog.buff_man.buff_state]}\n"
                            s += emojize(f"*Stats*: {jog.atk} :crossed_swords: {jog.defense} :shield:\n\n")
                            tt_hp += j_hp
                        s += f"*Total health*: {tt_hp} "
                        textinho += s + "\n"

                        # if jogador.buff_man.buff_state > 0:
                        #     textinho += f"Buff: {jogador.buff_man.states_list[jogador.buff_man.buff_state]}\n\n"

                        #self.bot.send_message(text=s, chat_id=caller.chat_id)
                        #self.server.playersdb.players_and_parties[chat_id].print_self_coms()
                        for jog in self.server.playersdb.players_and_parties[code].players:
                            new_text = ""
                            new_text += self.server.playersdb.players_and_parties[jog.chat_id].dg_coms()
                            new_text += "Would you like to continue? You have 2 minutes to decide."
                            texto = textinho+new_text
                            texto = texto.replace("_", "\\_")
                            self.bot.edit_message(text=texto, chat_id= jog.chat_id, parse_mode="MARKDOWN", reply_markup = self.dgkb, message_id = self.dungeons_in_progress[code]["msgs_id"])


                        #self.bot.send_message(text=text, chat_id=jogador.chat_id, reply_markup=self.dgkb)

                else:                   # É lendário, portanto é um boss
                    if bres == -1:       # Vitória
                        for jog in self.server.playersdb.players_and_parties[code].players:
                            jog.exp += 4*dungeon.level
                            if jog.classe == "Druid":
                                jog.beast_in_stack = besta

                        for i in dungeon.rewards:
                            item = copy.deepcopy(i)
                            # done = False
                            # number = 0
                            # exeed = False
                            # while not done:
                            #
                            #     for arma in self.server.parties_codes[code]["pt_inv"]:
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
                            number = 0

                            n = 0
                            for arma in self.server.playersdb.players_and_parties[code].inventory:

                                try:
                                    if arma.ac_code == item.ac_code:
                                        number += 1

                                            # if number == 0:
                                            #     number += 1
                                            #     item.code += f"{number}"
                                            # elif number < 10:
                                            #     number += 1
                                            #     item.code = item.code[:-1]
                                            #     item.code += f"{number}"
                                except:
                                    del self.server.playersdb.players_and_parties[code].inventory[n]
                                    break
                                n += 1

                            if number == 0:
                                number = ""

                            item.ac_code = item.code + f"{number}"

                            temp_ac = item.ac_code
                            item.ac_code = item.code
                            item.code = temp_ac
                            self.server.playersdb.players_and_parties[code].inventory.append(copy.deepcopy(item))   # Adiciona as armas ao inventário da party


                        textinho += emojize(f"Your party found a legendary {besta.tipo} named {besta.name} and killed it, you gained "
                                       f"{4*dungeon.level} exp *and some items*! Go check your shared inv in /party to claim those items!\n\n")

                        # self.bot.send_message(text=text, chat_id=jogador.chat_id, parse_mode='MARKDOWN', reply_markup=self.defkb)

                    else:     # Derrota

                        for jog in self.server.playersdb.players_and_parties[code].players:
                            if besta.area_damage:
                                text = "Everyone in the party has been hit."
                                jog.take_damage()
                                # self.bot.send_message(text = text, chat_id = jog.chat_id)
                            if jog.classe == "Druid":
                                jog.beast_in_stack = None
                            jog.exp += 2*dungeon.level
                            hp = 0
                            for limb in jog.hp:
                                hp += limb.health
                            if hp == 0:
                                to_die.append(jog)
                                dead = True
                            self.server.playersdb.players_and_parties[jog.chat_id] = jog
                        if not besta.area_damage:
                            self.aux_deal_damage_to_one_member(group)
                        textinho += emojize(f"Your party found a legendary {besta.tipo} named {besta.name} and it won the fight"
                                           f", you gained {2*dungeon.level} exp.\n\n")
                            #self.bot.send_message(text=text, chat_id=jogador.chat_id)



                    #
                    # else:               # Empate
                    #     for jog in self.server.playersdb.players_and_parties[code].players:
                    #         jog.exp += 2*dungeon.level
                    #
                    #     textinho += emojize(f"Your party met a foe who you battled for a very long time, as your strengths were evenly matched. "
                    #                    f"Exhausted, you retreated, and so did the legendary {besta.tipo} named {besta.name}. "
                    #                    f"You gained {2*dungeon.level} exp.\n\n")
                        #self.bot.send_message(text=text, chat_id=jogador.chat_id)



                    if not dead:    # Se não ta morto, printa a vida
                        s = ""
                        tt_hp = 0
                        for jog in self.server.playersdb.players_and_parties[code].players:
                            emoji = ":green_heart:"
                            j_hp = 0
                            for limb in jog.hp:
                                j_hp += limb.health
                            if j_hp < 5:
                                emoji = ":yellow_heart:"
                            if j_hp < 2:
                                emoji = ":red_heart:"
                            s += emojize(f"{jog.name}, '''{jog.chat_id}''':\n*Health*: {j_hp}{emoji} {jog.classe}\n")
                            s += f"*Buff*: {jog.buff_man.states_list[jog.buff_man.buff_state]}\n"
                            s += emojize(f"*Stats*: {jog.atk} :crossed_swords: {jog.defense} :shield:\n\n")

                            tt_hp += j_hp
                        s += f"*Total health*: {tt_hp} "
                        textinho += s + "\n"
                        # if jogador.buff_man.buff_state > 0:
                        #     textinho += f"Buff: {jogador.buff_man.states_list[jogador.buff_man.buff_state]}\n\n"

                        if bres != -1:
                            for jog in self.server.playersdb.players_and_parties[code].players:            # Vai checar a pokedex
                                new_text = ""
                                if f"{besta.tipo} named {besta.name}" not in jog.pokedex:
                                    new_text += emojize(f"Congratulations, {besta.tipo} named {besta.name} has been added to the /bestiary!\n\n")
                                    #self.bot.send_message(text=text, chat_id=chat_id)
                                    jog.pokedex.append(f"{besta.tipo} named {besta.name}")
                                new_text += self.server.playersdb.players_and_parties[jog.chat_id].dg_coms()
                                new_text += "Would you like to continue? You have 2 minutes to decide."
                                texto = textinho+new_text
                                texto = texto.replace("_", "\\_")
                                self.bot.send_message(text=texto, chat_id=jog.chat_id, parse_mode="MARKDOWN")

                            #self.server.playersdb
                            #self.bot.send_message(text=text, chat_id=jogador.chat_id, reply_markup=self.dgkb)
                        else:
                            for jog in self.server.playersdb.players_and_parties[code].players:        # Vai cehcar a pokedex denovo tbm
                                new_text = ""
                                if f"{besta.tipo} named {besta.name}" not in jog.pokedex:
                                    new_text += emojize(f"Congratulations, {besta.tipo} named {besta.name} has been added to the /bestiary!\n\n")
                                    #self.bot.send_message(text=text, chat_id=chat_id)
                                    jog.pokedex.append(f"{besta.tipo} named {besta.name}")
                                texto = textinho+new_text
                                texto = texto.replace("_", "\\_")
                                self.bot.send_message(text=texto, chat_id=jog.chat_id, parse_mode="MARKDOWN", reply_markup = self.defkb)

                            self.server.playersdb.players_and_parties[code].active = True
                            self.server.woods.players[code]["active"] = True
                            # self.server.playersdb.players_and_parties[code].location = self.server.playersdb.players_and_parties[code].prev_location
                            del self.dungeons_in_progress[code]

                            exit = True



                # if dead:
                #     del self.dungeons_in_progress[chat_id]
                #     self.server.woods.remove_from_woods(chat_id)
                #     self.dona_morte.die(chat_id)
                #     self.bot.send_message(text=textinho, chat_id=chat_id, reply_markup=self.defkb, parse_mode="MARKDOWN")
                #     return 1
                for jog in to_die:                                              # Todos os jogadores que morreram só foram apendados em to_die. agora eles morrem
                    # del self.server.parties_codes[jog.pt_code][jog.chat_id]
                    #     del self.server.parties_codes[jog.pt_code]
                    # del self.server.woods.players[jog.pt_code]
                    self.dona_morte.die(jog.chat_id)
                if not self.server.playersdb.players_and_parties[code].players:
                    del self.dungeons_in_progress[code]

                if exit:
                    return False
                else:
                    return 2*self.def_wait_time

            elif text == emojize("NOPE :thumbs_down:") or text == "/run_away":          # Caso o jogador desista da dungen
                textinho = "It's a dangerous place, so you decided to step back."
                self.bot.send_message(text=textinho, chat_id= self.server.playersdb.players_and_parties[code].chat_ids, reply_markup=self.defkb)
                self.server.playersdb.players_and_parties[code].active = True
                self.server.woods.players[code]["active"] = True
                # self.server.playersdb.players_and_parties[code].location = self.server.playersdb.players_and_parties[code].prev_location
                del self.dungeons_in_progress[code]
                return False

            else:
                return 2*self.def_wait_time

        else:
            self.server.playersdb.players_and_parties[code].active = True
            self.server.woods.players[code]["active"] = True
            # self.server.playersdb.players_and_parties[code].location = self.server.playersdb.players_and_parties[code].prev_location

            return False

    def save_dgs(self):
        '''
            Salva as dungeons
        '''
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle(self.dungeons_in_progress, self.dgs_file)
