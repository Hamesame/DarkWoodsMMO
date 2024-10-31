#############################################
#  Classe que contém as ações das dungeons  #
#############################################

import bot
import player
from emoji import emojize
import random as rd
import helper
import time


class DungeonComms:
    '''
        Classe que controla os comandos de uma dungeon
    '''
    def __init__(self, server):
        '''
            Os comandos engolem o server e os keyboards, carrega o helper pra enviar mensagens e o bot pra enviar mensagens
        '''
        self.server = server
        self.defkb = server.defkb
        self.def_wait_time = 60
        self.helper = helper.Helper(server)
        self.bot = bot.TGBot()
        self.dgkb = self.server.keyboards.bs_reply_markup
        self.defkb = self.server.keyboards.class_main_menu_reply_markup

        self.dgs_file = "dbs/dgs.dat"
        self.dungeons_in_progress = {}
        loaded = self.helper.load_pickle(self.dgs_file)
        if loaded:
            self.dungeons_in_progress = loaded

        self.actions = {}
        self.internal = {
            "start_dg": self.dung

        }
        self.tier_1 = 60*30
        self.tier_2 = 2*60*60
        self.tier_3 = 4*60*60
        self.tier_4 = 6*60*60
            # "start_pt_dg": self.pt_dung

    # def dung(self, caller, *args):
    #     '''
    #         Método que processa as dungeons solo. Se é a primeira, ele vai mandar o "você achou x", caso contrário, ele vai processar a dungeon
    #     '''
    #     self.server.woods.players[caller.chat_id]["active"] = False
    #
    #     if not args:
    #         dungeon_selected = self.server.dungeonsdb.dungeons[rd.randint(0, len(self.server.dungeonsdb.dungeons) - 1)]     # Escolhe uma dungeon aleatóriamente
    #         self.server.dungeon_master.dungeons_in_progress[caller.chat_id] = {
    #             "dungeon": dungeon_selected,
    #             "dnpc": 0
    #         }
    #
    #         text = emojize(f"You found a {dungeon_selected.name} level {dungeon_selected.level}."
    #                        f" Would you like to adventure there? You have {5+caller.suc_refs} minutes to decide.")
    #         self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.bs_reply_markup)
    #
    #         return self.def_wait_time*5+caller.suc_refs*60
    #
    #     else:
    #         player_text = args[-1]
    #         result = self.server.dungeon_master.dungeon_iteration(caller.chat_id, player_text)
    #
    #         if result:
    #             return result
    #         else:
    #             return False


    # def pt_dung_master(self, caller):
    #     pass
    #
    # def pt_dung_slave(self, caller, action):
    #     pass

    
    def dung(self, caller, caller_id = None, *args):
        '''
            Método que processa dungeons em party. Neste caso, ele recebe o id de quem chamou e o caller é a party toda.
        '''
        code = caller.code

        if not args:
            self.server.playersdb.players_and_parties[caller.code].active = False
            self.server.woods.players[caller.code]["active"] = False
            self.server.playersdb.players_and_parties[caller.code].location = "dungeon"
            tempo = min(self.server.woods.players[caller.code]["rem_time"], self.server.woods.players[caller.code]["stay_time"] - self.server.woods.players[caller.code]["rem_time"])
            tier = [0, 1, 2]
            if tempo > self.tier_1:
                tier = [3, 4]
            if tempo > self.tier_2:
                tier = [5, 6]
            if tempo > self.tier_3:
                tier = [7, 8, 9, 10]
            eligible = []
            for dg in self.server.dungeonsdb.dungeons:
                if dg.level in tier:
                    eligible.append(dg)

            dungeon_selected = eligible[rd.randint(0, len(eligible) - 1)]
            self.server.dungeon_master.dungeons_in_progress[code] = {
                "dungeon": dungeon_selected,
                "dnpc": 0,
                "msgs_id": {},
            }

            text = emojize(f"You found a {dungeon_selected.name} level {dungeon_selected.level}."
                           " Would you like to adventure there? You have 5 minutes to decide.")
            if isinstance(caller, player.Player):
                self.bot.send_message(text=text, chat_id= caller.chat_id, reply_markup=self.server.keyboards.inline_dg_reply_markup)
                return self.def_wait_time*5+caller.suc_refs*60
            else:
                self.bot.send_message(text=text, chat_id= caller.chat_ids, reply_markup=self.server.keyboards.inline_dg_reply_markup)
            return self.def_wait_time*5

        else:
            player_text = args[-1]
            message_id = args[0]
            code = caller.code
            if code[0] == "/":
                party = self.server.playersdb.players_and_parties[code]
                if party.last_dg_id_pt != self.server.dungeon_master.dungeons_in_progress[code]["msgs_id"]:
                    party.last_dg_id_pt = self.server.dungeon_master.dungeons_in_progress[code]["msgs_id"]
                    c_time = time.time()
                    if not party.last_done_dungeon_time_pt:
                        party.last_done_dungeon_time_pt = c_time
                    else:
                        delta_t = c_time-party.last_done_dungeon_time_pt
                        party.last_done_dungeon_time_pt = c_time
                        party.average_times_taken_pt.append(delta_t)
                        party.average_times_taken_pt = party.average_times_taken_pt[-20:]
                        party.average_time_between_dungeons_pt = sum(party.average_times_taken_pt)/len(party.average_times_taken_pt)
                        party.average_time_between_last_dungeons_pt = sum(party.average_times_taken_pt[-5:])/len(party.average_times_taken_pt[-5:])
                    party.average_time_between_WB_pt = party.average_time_between_dungeons_pt*5

            else:
                user = self.server.playersdb.players_and_parties[code]
                if user.last_dg_id != self.server.dungeon_master.dungeons_in_progress[code]["msgs_id"]:
                    user.last_dg_id = self.server.dungeon_master.dungeons_in_progress[code]["msgs_id"]
                    c_time = time.time()
                    if not user.last_done_dungeon_time:
                        user.last_done_dungeon_time = c_time
                        # print(f"c_time: {c_time}")
                    else:
                        delta_t = c_time-user.last_done_dungeon_time
                        user.last_done_dungeon_time = c_time
                        user.average_times_taken.append(delta_t)
                        user.average_times_taken = user.average_times_taken[-20:]
                        user.average_time_between_dungeons = sum(user.average_times_taken)/len(user.average_times_taken)
                        user.average_time_between_last_dungeons = sum(user.average_times_taken[-5:])/len(user.average_times_taken[-5:])
                        # print(f"delta_t: {delta_t}")
                    user.average_time_between_WB = user.average_time_between_dungeons*5


            if caller_id:
                result = self.server.dungeon_master.pt_dungeon_iteration(caller_id.chat_id, caller.pt_code, player_text, message_id)
            else:
                result = self.server.dungeon_master.dungeon_iteration(caller.chat_id, player_text, message_id)
            if result:
                # if caller.code in self.server.playersdb.players_and_parties:
                #     self.server.playersdb.players_and_parties[caller.code].location = "dungeon"
                return result
            else:
                if caller.code in self.server.playersdb.players_and_parties:
                    prev_location = self.server.playersdb.players_and_parties[caller.code].prev_location
                    self.server.playersdb.players_and_parties[caller.code].location = prev_location
                return False

    def to(self, chat_id):
        '''
            Timeout para a dungeon, se o chat_id for o código de party, ele fará o timeout para parties, caso contrário, ele fará o timeout solo.
        '''
        # print(f"chat = {chat_id}")
        if chat_id[0] == "/":
            if chat_id in self.server.playersdb.players_and_parties:
                text = "It's a dangerous place, so your party decided to step back."
                chat_ids = self.server.playersdb.players_and_parties[chat_id].chat_ids
                self.bot.send_message(text=text, chat_id=chat_ids, reply_markup=self.defkb)
        else:

            text = "It's a dangerous place, so you decided to step back."
            self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb)
        self.server.playersdb.players_and_parties[chat_id].active = True
        if chat_id in self.server.woods.players:
                # Daqui pra frente ele reseta tudo como se n tivesse achado a dungeon.
                # try:
            self.server.woods.players[chat_id]["active"] = True

            self.server.playersdb.players_and_parties[chat_id].location = self.server.playersdb.players_and_parties[chat_id].prev_location
                    #self.server.woods.players[chat_id]["entered_dg"] = False
            #     except:
            #         self.server.playersdb.players_and_parties[chat_id]["active"] = True
            #         self.server.playersdb.players_and_parties[chat_id]["entered_dg"] = False
            # else:
            #         self.server.woods.players[chat_id]["active"] = True
            #         self.server.woods.players[chat_id]["entered_dg"] = False
            if chat_id in self.dungeons_in_progress:
                del self.dungeons_in_progress[chat_id]
