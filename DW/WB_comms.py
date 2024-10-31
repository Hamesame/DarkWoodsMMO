import bot
import player
from emoji import emojize
import random as rd
import helper
import time


class WBComms:
    '''
        Classe que controla os comandos do WB. (sunflower neste caso)
    '''
    def __init__(self, server):
        self.server = server
        self.defkb = server.defkb
        self.def_wait_time = 60
        self.helper = helper.Helper(server)
        self.bot = bot.TGBot()
        self.wbkb = self.server.keyboards.bs_reply_markup
        self.defkb = self.server.keyboards.class_main_menu_reply_markup

        self.status = {"Health":600e3, "Players":[], "Kill count":0, "Is Dead":False, "Started time":time.time()}

        self.WB_file = "dbs/WB.dat"
        loaded = self.helper.load_pickle(self.WB_file)
        if loaded:
            self.status = loaded
            # self.dungeons_in_progress = loaded

        self.actions = {}
        self.internal = {
            "start_WB": self.WB,
            "start_pt_WB": self.pt_WB
        }


    def WB(self, caller, caller_id = None, *args):
        '''
            Comando que roda quando o jogador acha a sunflower na floresta em solo

            Parâmetros:

            caller (Player): Jogador que achou a sunflower
        '''
        if not self.server.World_boss.status["Is Dead"]:
            # Se n morreu, ele entra na sunflower e fala que o jogador não está ativo.
            self.server.woods.players[caller.chat_id]["active"] = False

            if not args:


                text = emojize(
                                "After walking for a long time, you realize you've been walking up a slight hill.\n"
                                "The air is dense and filled with a mist.\n"
                                "Then the trees became sparse and you sight a snow covered mountain up the hill.\n"
                                "There is a strong and cold wind coming from the summit.\n"
                                "Dark and heavy clouds cover the entire sky.\n"
                                "Thunders roar from the clouds near the mountain.\n\n"         # Preciso pensar no texto
                                "*Would you like to adventure there*?"
                                )

                self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.bs_reply_markup, parse_mode = 'MARKDOWN')

                return self.def_wait_time*5+caller.suc_refs*60
            else:
                if args[-1] == emojize("YES :thumbs_up:") and caller.chat_id not in self.server.World_boss.status["Players"]:           # Comando pra entrar na sunflower
                    self.server.World_boss.add_player(caller.chat_id)
                    return False
                elif args[-1] == emojize("NOPE :thumbs_down:"):                                             # Comando pra rejeitar a sunflower
                    text = "It's a dangerous place, so you decided to step back."
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    self.server.woods.players[caller.chat_id]["active"] = True

                    return False

                else:                                       # Caso o cara seja um babaca e n saiba escrever
                    text = ("The gods did not understand your prayer. You can seek help at the campfire: \nhttps://t.me/DWcommchat")
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.defkb)
                    return self.def_wait_time*5+caller.suc_refs*60
        else:
            # Caso a sunflower esteja morta

            text = emojize(
                "You reach the foot of a snow covered mountain.\n"
                "The sky is blue and you feel the warmth of the sun shining on your face.\n"
                "The top of this mountain was once the lair of Sairacaz, the blizzard elemental.\n"
                "Defeated, the dark woods is now free from the eternal winter.\n"
                "After enjoying the view from the foot of the mountain, you decide to return to explore the forest.\n"
            )
            self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode = "MARKDOWN")
            self.server.woods.players[caller.chat_id]["active"] = True
            return False

    def pt_WB(self, caller, caller_id = None, *args):
        '''
            Método que administra o comando de WB pra parties.
            Este código é extremamente similar ao de cima, mas com a adição das parties.

            Parâmetros:

            caller_id (str): id do jogador que respondeu

            caller (dic): Party que achou o WB
        '''
        if not self.server.World_boss.status["Is Dead"]:
            self.server.playersdb.players_and_parties[caller.pt_code].active = False
            self.server.woods.players[caller.pt_code]["active"] = False
            if not args:


                text = emojize(
                                "After walking for a long time, you realize your party have been walking up a slight hill.\n"
                                "The air is dense and filled with a mist.\n"
                                "Then the trees became sparse and you sight a snow covered mountain up the hill.\n"
                                "There is a strong and cold wind coming from the summit.\n"
                                "Dark and heavy clouds cover the entire sky.\n"
                                "Thunders roar from the clouds near the mountain.\n\n"         # Preciso pensar no texto
                                "*Would you like to adventure there*?"
                                )

                self.bot.send_message(text=text, chat_id=caller.chat_ids, reply_markup=self.server.keyboards.bs_reply_markup, parse_mode = "MARKDOWN")

                return self.def_wait_time*5
            else:

                if args[-1] == emojize("YES :thumbs_up:") and caller_id.chat_id not in self.server.World_boss.status["Players"]:
                    for chat in caller.chat_ids:
                        self.server.World_boss.add_player(chat)
                    self.server.playersdb.players_and_parties[caller.pt_code].location = "WB"
                    return False
                elif args[-1] == emojize("NOPE :thumbs_down:"):
                    text = "It's a dangerous place, so your party decided to step back."
                    self.bot.send_message(text=text, chat_id=caller.chat_ids, reply_markup=self.defkb)
                    self.server.playersdb.players_and_parties[caller.pt_code].active = True
                    self.server.woods.players[caller.pt_code]["active"] = True

                    return False


                else:
                    text = ("The gods did not understand your prayer. You can seek help at the campfire: \nhttps://t.me/DWcommchat")

                    # for chat,jog in caller.items():
                    #     if isinstance(jog, player.Player):
                    self.bot.send_message(text=text, chat_id=caller_id.chat_id, reply_markup=self.server.keyboards.bs_reply_markup)

                    return False
        else:

            text = emojize(
                "Your party reach the foot of a snow covered mountain.\n"
                "The sky is blue and you feel the warmth of the sun shining on your face.\n"
                "The top of this mountain was once the lair of Sairacaz, the blizzard elemental.\n"
                "Defeated, the dark woods is now free from the eternal winter.\n"
                "After enjoying the view from the foot of the mountain, you decide to return to explore the forest.\n"
            )
            self.server.playersdb.players_and_parties[caller.pt_code].active = True
            self.server.woods.players[caller.pt_code]["active"] = True
            self.bot.send_message(text=text, chat_id=caller.chat_ids, parse_mode = "MARKDOWN")
            return False

    def to(self, chat_id):
        '''
            Função de timeout da sunflower.

            chat_id (str): id do telegram ou código da party que deu timeout
        '''
        if chat_id[0] == "/":
            text = "It's a dangerous place, so your party decided to step back."
            if chat_id in self.server.playersdb.players_and_parties:
                pt = self.server.playersdb.players_and_parties[chat_id]
                self.bot.send_message(text=text, chat_id=pt.chat_ids, reply_markup=self.defkb)
        else:

            text = "It's a dangerous place, so you decided to step back."
            self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb)
        if chat_id in self.server.woods.players:
            if chat_id[0] == "/":
                try:
                    self.server.woods.players[chat_id]["active"] = True
                    self.server.playersdb.players_and_parties[chat_id].active = True
                    self.server.woods.players[chat_id]["entered_dg"] = False
                except:
                    self.server.playersdb.players_and_parties[chat_id].active = True
            else:
                    self.server.woods.players[chat_id]["active"] = True
                    self.server.woods.players[chat_id]["entered_dg"] = False
