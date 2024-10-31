##############################################
# Classe que contém os comandos da floresta  #
##############################################

from emoji import emojize
from emoji import demojize
import bot
import items
import player
import time

class ForestCommms:
    '''
        O único comando em forest é o próprio "/forest"

        A partir dele, podem ter vários argumentos. Como se quer voltar ou não ou quantas horas vc quer ficar lá.

    '''
    def __init__(self, server):
        '''
            Ele carrega o server, o keyboard padrão, o tempo padrão de espera, que é 1 minuto, o bot pra mandar mensagens, e o único comando, que é o forest.

        '''
        self.server = server
        self.defkb = server.defkb           # Keyboard padrão
        self.def_wait_time = 60
        self.bot = bot.TGBot()
        self.actions = {
            emojize(":deciduous_tree: Forest :deciduous_tree:"): self.forest
        }
        self.internal = {
            "start_df": self.df,
            "start_caverns": self.caverns,
        }

    def forest(self, caller, *args):
        '''
            Comando executado quando o jogador da um "/forest"
        '''
        self.server.woods.process()         # Toda vez que este comando for chamado, ele irá processar as florestas.
        self.server.deep_forest_manager.process()
        if caller.location == "arena":
            text = "You are battling in the arena now, to enter the forest please finish your fight."
            self.bot.send_message(text=text, chat_id=caller.chat_id)
            return False
        else:

            if not caller.pt_code:              # Existem 8 casos, pois o jogador pode fazer parte ou não de uma party e ele pode ou não estar na floresta e se ele ja jogou um argumento ou não
                if not args:

                    if (not caller.chat_id in self.server.woods.players) and (not caller.chat_id in self.server.deep_forest_manager.jogs):         # Não faz parte de uma party e não está na floresta e não respondeu
                        text = emojize("There are many resources available for those who dare venture into the hungry woods... however, the forest :deciduous_tree: will not remain passive at your intrusion. How long will you stay?")
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.time_reply_markup)
                        return self.def_wait_time
                    elif caller.chat_id in self.server.woods.players:                                                       # Não faz parte de uma party e está na floresta e não respondeu
                        # self.server.woods.players[caller.chat_id]["active"] = True
                        remtime = int(self.server.woods.players[caller.chat_id]["rem_time"]/60)
                        hours, minutes = divmod(remtime, 60)            # Calcula o tempo que falta pra voltar da floresta em minutos e com isto, calcula os minutos e horas restantes
                        if hours != 0:
                            text = f"You'll return in {hours} hours and {minutes} minutes. Should you head back early?"
                        else:
                            text = f"You'll return in {minutes} minutes. Should you head back early?"
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.forest_return_reply_markup)
                        return self.def_wait_time
                    elif caller.chat_id in self.server.deep_forest_manager.jogs:
                        if not self.server.deep_forest_manager.jogs[caller.chat_id].is_leaving:
                            stay_time = int(self.server.deep_forest_manager.jogs[caller.chat_id].stay_time)
                            minutes, seconds = divmod(stay_time, 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            return_time = int(stay_time/4)
                            text = f"You are inside the deep forest for {days} days {hours} hours {minutes} minutes and {seconds} seconds."
                            minutes, seconds = divmod(return_time, 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            text += f" If you want to return, you will take {days} days {hours} hours {minutes} minutes and {seconds} seconds. Would you like to return?"
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.forest_return_reply_markup)
                        else:
                            c_time = time.time()
                            delta_t = c_time - self.server.deep_forest_manager.jogs[caller.chat_id].decision_to_stop
                            time_left_to_leave = int(self.server.deep_forest_manager.jogs[caller.chat_id].leave_time - delta_t)
                            minutes, seconds = divmod(time_left_to_leave, 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            text = f"You are already returning to the normal forest, you will get ther in {days} days {hours} hours {minutes} minutes and {seconds} seconds."
                            self.bot.send_message(text=text, chat_id=caller.chat_id)
                            return False

                        return self.def_wait_time
                    elif caller.chat_id in self.server.caverns_manager.jogs:

                        if not self.server.caverns_manager.jogs[caller.chat_id].is_leaving:
                            stay_time = int(self.server.caverns_manager.jogs[caller.chat_id].stay_time)
                            minutes, seconds = divmod(stay_time, 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            return_time = int(stay_time/4)
                            text = f"Your party is inside the caverns for {days} days {hours} hours {minutes} minutes and {seconds} seconds."
                            minutes, seconds = divmod(return_time, 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            text += f" If you want to return, you will take {days} days {hours} hours {minutes} minutes and {seconds} seconds. Would you like to return?"
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.forest_return_reply_markup)
                            return self.def_wait_time
                        else:
                            c_time = time.time()
                            delta_t = c_time - self.server.caverns_manager.jogs[caller.chat_id].decision_to_stop
                            time_left_to_leave = int(self.server.caverns_manager.jogs[caller.chat_id].leave_time - delta_t)
                            minutes, seconds = divmod(time_left_to_leave, 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            text = f"You are already returning to the normal forest, you will get there in {days} days {hours} hours {minutes} minutes and {seconds} seconds."
                            self.bot.send_message(text=text, chat_id=caller.chat_id)
                            return False
                else:
                    if (not caller.chat_id in self.server.woods.players) and (not caller.chat_id in self.server.deep_forest_manager.jogs):         # Não faz parte de uma party e não está na floresta e respondeu
                        time_s = args[-1]
                        if time_s != "Back":
                            time2 = 3600
                            if time_s == "4 hours":
                                time2 = time2*4
                            elif time_s == "8 hours":
                                time2 = time2*8
                            elif time_s == "12 hours":          # Vai ver quantas horas ele quer ficar na floresta
                                time2 = time2 * 12

                            self.server.woods.add_to_woods(caller, time2)

                            timeh = int(time2/3600)
                            text = (f"You prepared for a {timeh} hour trip. Maybe you'll find something useful in that time.")
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)

                            if caller.has_died:                 # Checa se o jogador morreu para ele poder dar retrace nos seus itens dropados.
                                # text = emojize(f"As you struggle to regain your bearings after death, you notice some paw prints :paw_prints: heading off the camp. "
                                #                 f"Will you follow the paw prints :paw_prints:? "
                                #                 f"They will probably lead where you died. "
                                #                 f"Some items might have already been taken. "
                                #                 f"But with this you have the chance of reclaiming what is left. "
                                #                 f"Or will you accept the fresh start you've been given?")

                                text = emojize(f"As you struggle to regain your bearings after death, you notice "
                                                f"some familiar tracks coming out from the bushes: paw prints :paw_prints: "
                                                f"resembling a dog's paws are said to belong to Alileb, the guardian "
                                                f"spirit. She must have dragged your mercilessly beaten body "
                                                f"through here. The lingering regrets from your past life leave you "
                                                f"restless. Will you retrace her steps and attempt to reclaim what "
                                                f"you've lost? Or will you accept the fresh start you've been given?")

                                self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.retrace_steps_markup)
                                return self.def_wait_time*5
                        elif time_s == "Back":
                            text = "You decided to step back and remain in the camp."
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                        else:
                            return False

                        return False

                    elif caller.has_died:       # Se o jogador acabou de morrer, então o bot está esperando ele responder se irá dar retrace ou não.
                        if args[-1] == emojize(":paw_prints: Retrace steps :paw_prints:"):
                            text = emojize(f"Alas, unable to let go of your past achievements and riches, you take a detour to find your body.")
                            caller.has_died = False
                            self.server.travelman.set_travel(caller, "death_site")
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                            return False
                        else:
                            caller.has_died = False
                            text = emojize(f"You decide that those material goods weren't really what mattered. "
                                            f"You've got friends to adventure with and a newly unburdened heart. "
                                            f"You're happy now.\n\n"
                                            f"Your old tracks are left behind, never to be seen again. "
                                            )
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                            return False
                    elif caller.chat_id in self.server.woods.players:                                                       # Não faz parte de uma party e está na floresta e respondeu
                        if args[-1] == "yes":               # Ele tinha pergutnado se fica ou não na floresta
                            if caller.is_travelling:
                                self.bot.send_message(text="You decided to stop your journey.", chat_id=caller.chat_id)
                                self.server.travelman.cancel_travel(self.server.playersdb.players_and_parties[caller.chat_id])

                            remtime = self.server.woods.players[caller.chat_id]["rem_time"]     # calcula o tempo q falta pra voltar
                            remtime2 = remtime
                            if remtime > self.server.woods.trip_time:
                                remtime2 = self.server.woods.trip_time
                            if remtime > self.server.woods.players[caller.chat_id]["stay_time"] - self.server.woods.trip_time:
                                remtime2 = self.server.woods.players[caller.chat_id]["stay_time"] - remtime

                            self.server.woods.players[caller.chat_id]["rem_time"] = remtime2

                            remtime2 = int(remtime2/60)
                            text = f"You will be back in {remtime2} minutes"
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                            return False

                        elif args[-1] == "no":
                            text = "You decide to stay in the forest a little longer."
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                            return False

                        else:
                            return False

                    elif caller.chat_id in self.server.deep_forest_manager.jogs:
                        if args[-1] == "yes":
                            text = self.server.deep_forest_manager.jogs[caller.chat_id].come_back()
                            self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        elif args[-1] == "no":
                            text = "You decide to stay in the deep forest a little longer."
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                            return False
                        else:
                            return False

                    elif caller.chat_id in self.server.caverns_manager.jogs:
                        if args[-1] == "yes":
                            text = self.server.caverns_manager.jogs[caller.chat_id].come_back()
                            self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        elif args[-1] == "no":
                            text = "You decide to stay in the caverns a little longer."
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                            return False
                        else:
                            return False


            else:               # Para parties. Neste caso, o código é bem similar, mas ao invpes de se referir ao parâmetro do objeto player.is_at_forest, ele se refere à entrada do dicionário "is_at_forest" da party do jogador

                chat_ids = self.server.playersdb.players_and_parties[caller.pt_code].chat_ids

                if not args:

                    if self.server.playersdb.players_and_parties[caller.pt_code].location == "camp":   # Faz parte de uma party e não está na floresta e não respondeu
                        text = emojize("There are many resources available for those who dare venture into the hungry woods... however, the forest :deciduous_tree: will not remain passive at your intrusion. How long will you stay?")
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.time_reply_markup)
                        return self.def_wait_time
                    elif self.server.playersdb.players_and_parties[caller.pt_code].location == "forest":                                                               # Faz parte de uma party e está na floresta e não respondeu
                        # self.server.woods.players[caller.pt_code]["active"] = True
                        if not caller.pt_code in self.server.woods.players:
                            # self.server.playersdb.players_and_parties[caller.pt_code]["is_at_forest"] = False
                            self.server.playersdb.players_and_parties[caller.pt_code].location == "camp"        # be aware of this. Não checamos aonde a party realmente está.
                            return False
                        remtime = int(self.server.woods.players[caller.pt_code]["rem_time"]/60)
                        hours, minutes = divmod(remtime, 60)
                        if hours != 0:
                            text = f"You'll return in {hours} hours and {minutes} minutes. Should you head back early?"
                        else:
                            text = f"You'll return in {minutes} minutes. Should you head back early?"
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.forest_return_reply_markup)
                        return self.def_wait_time
                    elif self.server.playersdb.players_and_parties[caller.pt_code].location == "deep_forest":
                        if not self.server.deep_forest_manager.jogs[caller.pt_code].is_leaving:
                            stay_time = int(self.server.deep_forest_manager.jogs[caller.pt_code].stay_time)
                            minutes, seconds = divmod(stay_time, 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            return_time = int(stay_time/4)
                            text = f"Your party is inside the deep forest for {days} days {hours} hours {minutes} minutes and {seconds} seconds."
                            minutes, seconds = divmod(return_time, 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            text += f" If you want to return, you will take {days} days {hours} hours {minutes} minutes and {seconds} seconds. Would you like to return?"
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.forest_return_reply_markup)
                            return self.def_wait_time
                        else:
                            c_time = time.time()
                            delta_t = c_time - self.server.deep_forest_manager.jogs[caller.pt_code].decision_to_stop
                            time_left_to_leave = int(self.server.deep_forest_manager.jogs[caller.pt_code].leave_time - delta_t)
                            minutes, seconds = divmod(time_left_to_leave, 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            text = f"You are already returning to the normal forest, you will get there in {days} days {hours} hours {minutes} minutes and {seconds} seconds."
                            self.bot.send_message(text=text, chat_id=caller.chat_id)
                            return False
                    elif self.server.playersdb.players_and_parties[caller.pt_code].location == "caverns":
                        if not self.server.caverns_manager.jogs[caller.pt_code].is_leaving:
                            stay_time = int(self.server.caverns_manager.jogs[caller.pt_code].stay_time)
                            minutes, seconds = divmod(stay_time, 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            return_time = int(stay_time/4)
                            text = f"Your party is inside the caverns for {days} days {hours} hours {minutes} minutes and {seconds} seconds."
                            minutes, seconds = divmod(return_time, 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            text += f" If you want to return, you will take {days} days {hours} hours {minutes} minutes and {seconds} seconds. Would you like to return?"
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.forest_return_reply_markup)
                            return self.def_wait_time
                        else:
                            c_time = time.time()
                            delta_t = c_time - self.server.caverns_manager.jogs[caller.pt_code].decision_to_stop
                            time_left_to_leave = int(self.server.caverns_manager.jogs[caller.pt_code].leave_time - delta_t)
                            minutes, seconds = divmod(time_left_to_leave, 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            text = f"You are already returning to the normal forest, you will get there in {days} days {hours} hours {minutes} minutes and {seconds} seconds."
                            self.bot.send_message(text=text, chat_id=caller.chat_id)
                            return False
                else:
                    if (not self.server.playersdb.players_and_parties[caller.pt_code].location == "forest") and (not self.server.playersdb.players_and_parties[caller.pt_code].location == "deep_forest"):   # Faz parte de uma party e não está na floresta e respondeu
                        time_s = args[-1]
                        if time_s != "Back":
                            time2 = 3600
                            if time_s == "4 hours":
                                time2 = time2*4
                            elif time_s == "8 hours":
                                time2 = time2*8
                            elif time_s == "12 hours":
                                time2 = time2 * 12

                            self.server.woods.add_to_woods(self.server.playersdb.players_and_parties[caller.pt_code], time2)     # Neste caso, ele adicona a party à floresta ao invés do objeto jogador

                            timeh = int(time2/3600)
                            text = (f"You prepared for a {timeh} hour trip. Maybe your party finds something useful in that time.")
                            self.bot.send_message(text = text, chat_id = chat_ids, reply_markup = self.defkb)      # Neste caso, ele amnda a mensagem pra td mundo na party
                        elif time_s == "Back":
                            text = "You decided to step back and remain in the camp."
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)


                        else:
                            return False

                        return False

                    elif self.server.playersdb.players_and_parties[caller.pt_code].location == "forest":                           # Faz parte de uma party e está na floresta e respondeu
                        if args[-1] == "yes":
                            if self.server.playersdb.players_and_parties[caller.pt_code].is_travelling:
                                text="You decided to stop your journey."                                    # Para a viagem se alguém está viajando
                                self.bot.send_message(text=text, chat_id=chat_ids, reply_markup=self.defkb)
                                self.server.travelman.cancel_travel(self.server.playersdb.players_and_parties[caller.pt_code])
                                # self.server.playersdb.players_and_parties[caller.pt_code]["is_travelling"] = False
                                # self.server.playersdb.players_and_parties[caller.pt_code]["travel_time"] = 0
                                # self.server.playersdb.players_and_parties[caller.pt_code]["travelling_loc"] = ""

                            remtime = self.server.woods.players[caller.pt_code]["rem_time"]             # calcula o tempo pra voltar
                            remtime2 = remtime
                            if remtime > self.server.woods.trip_time:
                                remtime2 = self.server.woods.trip_time
                            if remtime > self.server.woods.players[caller.pt_code]["stay_time"] - self.server.woods.trip_time:
                                remtime2 = self.server.woods.players[caller.pt_code]["stay_time"] - remtime

                            self.server.woods.players[caller.pt_code]["rem_time"] = remtime2

                            remtime2 = int(remtime2/60)
                            text = f"Your party will be back in {remtime2} minutes"

                            self.bot.send_message(text=text, chat_id= chat_ids, reply_markup=self.defkb)
                            # for chat_id,jogador in self.server.playersdb.players_and_parties[caller.pt_code].items():
                            #     if isinstance(jogador, player.Player):
                            #         self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb)      # Esta mensagem ele envia pra td mundo

                            return False

                        elif args[-1] == "no":
                            text = "You decide to stay in the forest a little longer."
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)

                            return False

                        else:
                            return False
                    else:
                        if args[-1] == "yes":
                            text = self.server.deep_forest_manager.jogs[caller.pt_code].come_back()
                            self.server.bot.send_message(text=text, chat_id=self.server.playersdb.players_and_parties[caller.pt_code].chat_ids)

                            return False
                        elif args[-1] == "no":
                            text = "You decide to stay in the deep forest a little longer."
                            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                            return False
                        else:
                            return False

            return False # Por hora. Pensar no caso de /forest em outras localizações.

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

    def caverns(self, caller, caller_id = None, *args):
        if not args:
            text = "You found a small cave entrance with smooth walls in the ground. Do you want to venture there?"
            if isinstance(caller, player.Player):
                self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.bs_reply_markup)
                return self.def_wait_time*5+caller.suc_refs*60
            else:
                self.bot.send_message(text=text, chat_id=caller.chat_ids, reply_markup=self.server.keyboards.bs_reply_markup)
            return self.def_wait_time*5
        else:
            if args[-1] == emojize("YES :thumbs_up:"):
                if isinstance(caller, player.Player):
                    self.server.caverns_manager.enter(caller.chat_id)
                else:
                    self.server.caverns_manager.enter(caller.pt_code)
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
