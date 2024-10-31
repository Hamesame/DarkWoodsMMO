################################################
# Classe que contém os comandos da deep forest #
################################################

from emoji import emojize
from emoji import demojize
import bot
import items
import player
import time

class DeepForestComms:
    '''
        O único comando em deep forest é o próprio "/deep_forest". Fora ele, temos o comando interno "start_df" para o encontro com a deep forest.

        A partir dele, podem ter vários argumentos. Como se quer voltar ou não.

    '''
    def __init__(self, server):
        '''
            Ele carrega o server, o keyboard padrão, o tempo padrão de espera, que é 1 minuto, o bot pra mandar mensagens, e o único comando, que é o /deep_forest.

        '''
        self.server = server
        self.defkb = server.defkb           # Keyboard padrão
        self.def_wait_time = 60
        self.bot = bot.TGBot()
        self.actions = {
            "/deep_forest": self.deep_forest
        }
        self.internal = {
            "start_df": self.df
        }

    def deep_forest(self, caller, *args):
        self.server.woods.process()         # Toda vez que este comando for chamado, ele irá processar as florestas.
        self.server.deep_forest_manager.process()

        if not args:
            if not self.server.deep_forest_manager.jogs[caller.code].is_leaving:
                stay_time = int(self.server.deep_forest_manager.jogs[caller.code].stay_time)
                minutes, seconds = divmod(stay_time, 60)
                hours, minutes = divmod(minutes, 60)
                days, hours = divmod(hours, 24)
                time_factor = 1
                if caller.pt_code:
                    time_factor = self.server.playersdb.players_and_parties[caller.pt_code].time_factor_pt
                else:
                    time_factor = caller.time_factor
                return_time = int(stay_time*time_factor/4)
                text = f"You are inside the deep forest for {days} days {hours} hours {minutes} minutes and {seconds} seconds."
                if caller.pt_code:
                    text = f"Your party is inside the deep forest for {days} days {hours} hours {minutes} minutes and {seconds} seconds."
                minutes, seconds = divmod(return_time, 60)
                hours, minutes = divmod(minutes, 60)
                days, hours = divmod(hours, 24)
                text += f" If you want to return, you will take {days} days {hours} hours {minutes} minutes and {seconds} seconds. Would you like to return?"
                self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.forest_return_reply_markup)
            else:
                c_time = time.time()
                delta_t = c_time - self.server.deep_forest_manager.jogs[caller.code].decision_to_stop
                time_left_to_leave = int(self.server.deep_forest_manager.jogs[caller.code].leave_time - delta_t)
                minutes, seconds = divmod(time_left_to_leave, 60)
                hours, minutes = divmod(minutes, 60)
                days, hours = divmod(hours, 24)
                text = f"You are returning to the normal forest, you will get there in {days} days {hours} hours {minutes} minutes and {seconds} seconds. Would you like to stay more?"
                self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.forest_return_reply_markup)

            return self.def_wait_time

        else:
            if self.server.deep_forest_manager.jogs[caller.code].is_leaving:
                if args[-1] == "yes":
                    text = self.server.deep_forest_manager.jogs[caller.code].continue_at_df()
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return False
                elif args[-1] == "no":
                    text = "Truly, it is time to retun."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return False
                else:
                    return False
            else:
                if args[-1] == "yes":
                    if not caller.location == "megabeast":
                        time_factor = 1
                        if caller.pt_code:
                            time_factor = self.server.playersdb.players_and_parties[caller.pt_code].time_factor_pt
                        else:
                            time_factor = caller.time_factor
                        text = self.server.deep_forest_manager.jogs[caller.code].come_back(time_factor)
                        if caller.pt_code:
                            chat_ids = self.server.playersdb.players_and_parties[caller.pt_code].chat_ids
                            self.server.bot.send_message(text=text, chat_id=chat_ids, reply_markup=self.defkb)
                        else:
                            self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    else:
                        text = "You are now fighting a megabeast, if you want to leave the forest, firstly you should /leave_battle the battle."
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return False
                elif args[-1] == "no":
                    text = "You decide to stay in the deep forest a little longer."
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False
                else:
                    return False




    def df(self, caller, caller_id = None, *args):
        if not args:
            text = "You approach a darker part of the forest where trees are taller, the vegetation is less dense than in normal forest and you can see a clear path going there. Do you want to venture there?"
            if isinstance(caller, player.Player):
                self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.bs_reply_markup)
                return self.def_wait_time*5+caller.suc_refs*60
            else:
                self.bot.send_message(text=text, chat_id=caller.chat_ids, reply_markup=self.server.keyboards.bs_reply_markup)
            return self.def_wait_time*5
        else:
            if args[-1] == emojize("YES :thumbs_up:"):
                if isinstance(caller, player.Player):
                    self.server.deep_forest_manager.enter(caller.chat_id)
                else:
                    self.server.deep_forest_manager.enter(caller.pt_code)
            else:
                text = "Its a dangerous place, so you decided to step back."
                if isinstance(caller, player.Player):
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                else:
                    self.bot.send_message(text=text, chat_id=caller.chat_ids)

            return False

    def to(self, chat_id):
        pass

    def to2(self, chat_id):
        if chat_id[0] == "/":
            if chat_id in self.server.playersdb.players_and_parties:
                text = "It's a dangerous place, so your party decided to step back."
                chat_ids = self.server.playersdb.players_and_parties[chat_id].chat_ids
                self.bot.send_message(text=text, chat_id=chat_ids, reply_markup=self.defkb)
        else:

            text = "It's a dangerous place, so you decided to step back."
            self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb)
