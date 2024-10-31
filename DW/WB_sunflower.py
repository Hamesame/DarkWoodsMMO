import bot
import player
from emoji import emojize
from copy import copy
import random as rd
import helper
import os
import numpy as np
import death
import time
import beastsdb
import deep_items

class WorldBoss:
    '''
        Classe do zauarudo boss.
    '''
    def __init__(self, server):
        self.server = server
        self.defkb = server.defkb
        self.Talismandb = deep_items.Talismandb()
        self.def_wait_time = 60             # 1 minuto
        self.helper = helper.Helper(server)
        self.bot = bot.TGBot()
        self.wbkb = self.server.keyboards.bs_reply_markup               # YES/NOPE
        self.defkb = self.server.keyboards.class_main_menu_reply_markup # Other keyboard

        self.status = {"Health":round(50e9), "Minions":round(300e6), "Players":[], "Kill count":0, "Recover count":0, "Is Dead":False, "Started time":time.time(), "Recovery rate":1e6}
        self.injured = []   # Lista de jogadores com vida abaixo de certo valor
        self.MVP = ["",0]   # Melhor jogador
        self.DPT = 0        # Dano por turno

        self.WB_file = "dbs/WB.dat"
        loaded = self.helper.load_pickle(self.WB_file)  # Carrega o WB
        if loaded:
            self.status = loaded
            # self.dungeons_in_progress = loaded

        self.Max_hp = round(50e9)       # Hp máximo do boss
        self.Max_Minions = round(300e6) # Número máximo de minions
        self.minion_damage = 300
        self.minion_defense = 300

        self.recovery_time = 16         # Número de turnos para regenerar os minions
        self.max_recovery_rate = 1e6   # Quantos miçnions serão regenerados por turno
        self.Minion_recovery_rate = self.status["Recovery rate"]*self.recovery_time
        self.recovery_loss_over_time = 10e3   # quanto de recuperação de minions são perdidas por turno
        self.std_time = 15*60           # 15 minutos
        self.last_processed = 0
        self.channel_id = "-10012343454573" # channel id
        self.dona_morte = death.Death(server)
        self.changed_to_raw = False             # Quando ele acabou de zerar os minions.
        self.changed_to_serv = False            # Quando ele gerou minions e tava sem antes

        self.show_servants = False
        self.show_raw = False
        self.hp = [":green_heart:",":yellow_heart:",":orange_heart:",":red_heart:️",":broken_heart:",":black_heart:"]
        # Lista de stats do WB, a medida q ele vai perdendo vida, ele vai mostrando corações diferentes

    def do_things(self,jogador):
        '''
            Método que processa cada jogador individualmente dentro da batalha.

            Parâmetros:

            jogador (Player): jogador que será processado
        '''
        dead = False
        base_damage = self.minion_damage
        jogador.location = "WB"
        if self.status["Minions"]:
            dam_prob = np.exp(-(jogador.defense/base_damage)**(1/3))    # Função de cálculo da probabilidade do jogador levar 1 de dano
            thing = rd.random()
            if dam_prob > thing:
                res = jogador.take_damage()
                if res == -1:
                    dead = True

            heal = 0
            for limb in jogador.hp:
                heal += limb.health
            if heal < 5:
                self.injured.append(jogador.chat_id)    # Se o jogador estiver com menos de 5 de vida, ele vai parar na lista dos injured

            base_defense = self.minion_defense


            killed = round(jogador.atk/base_defense)    # Quantos minions o jogador matou
            self.status["Minions"] -= killed
            if killed and not dam_prob > thing and jogador.classe == "Druid":
                besta = beastsdb.Beast(emojize(":bouquet: Servant :rose:"), 300, 300, 10, "", 1, False)
                jogador.beast_in_stack = besta

            if self.status["Minions"] <= 0:
                self.status["Minions"] = 0
                self.changed_to_raw = True
            if self.MVP[1] < killed:            # Define o mvp
                self.MVP[0] = jogador.chat_id
                self.MVP[1] = killed
            self.DPT += killed

        else:                                       # Se ele ja estiver tomando dano direto na cara, ele tira do hp
            self.status["Health"] -= jogador.atk
            if self.MVP[1] < jogador.atk:           # Define o mvp
                self.MVP[0] = jogador.chat_id
                self.MVP[1] = jogador.atk
            self.DPT += jogador.atk

        if dead:
            if not jogador.pt_code:
                if jogador.chat_id in self.server.woods.players:
                    self.server.woods.remove_from_woods(jogador.chat_id)
            self.remove_player(jogador.chat_id)                         # Isso pode dar pau numa morte em uma party (bug)
            self.dona_morte.die(jogador.chat_id)
            self.status["Kill count"] += 1



    def generate_string_from_int(self,num):
        '''
            Método que pega uma int e coloca vírgulas nela.

            Parâmetros:

            num (int): Inteiro que será convertido em str
        '''
        a = str(int(num))
        l = len(a)
        c = 0
        while l!=0:

            if c == 3:
                c = 0
                p1 = a[:l]
                p2 = a[l:]
                a = p1 + "," + p2
            l -= 1
            c+=1
        return a


    def process(self):
        '''
            Função que roda pra processar o zauarudo boss.
        '''
        hel = "Health"
        min = "Minions"
        pl = "Players"
        kc = "Kill count"
        rc = "Recover count"    # São usadas variáveis para acessar essas strings pois elas travariam com fstrings
        if not self.status["Is Dead"]:
            self.injured = []
            self.MVP = ["",0]
            self.DPT = 0                # Toda vez ele da uma resetada nos jogadores machucados, mvp e dpt
            if self.status["Minions"]:
                self.status["Recovery rate"] -= self.recovery_loss_over_time                    # A taxa de recuperação de minions por turno cai
                self.Minion_recovery_rate -= self.recovery_loss_over_time*self.recovery_time
                if self.Minion_recovery_rate < 0:
                    self.Minion_recovery_rate = 0
                    self.status["Recovery rate"] = 0
            else:                                                       # Se não houver mais minions, a taxa de recuerção volta ao original
                self.status["Recovery rate"] = self.max_recovery_rate
                self.Minion_recovery_rate = self.status["Recovery rate"]*self.recovery_time
            for chat in self.status[pl]:

                self.do_things(self.server.playersdb.players_and_parties[chat])     # Cada jogador é processado individualmente aqui

            if self.status["Recover count"] == self.recovery_time:          # Recupera os minions
                self.status["Minions"] += self.Minion_recovery_rate
                if self.status["Minions"] == self.Minion_recovery_rate:
                    self.changed_to_serv = True
                if self.status["Minions"] > self.Max_Minions:
                    self.status["Minions"] = self.Max_Minions
                self.status["Recover count"] = 0
            self.status["Recover count"] += 1

            frac = self.status["Health"]/self.Max_hp            # Para calcular qual emoji usar
            if frac < 0:
                frac = 0
            other_frac = 1-frac
            thing = round(other_frac*5)
            em = self.hp[thing]
            # print(f"frac = {frac}\nother_frac = {other_frac}\nthing = {thing}")


            ac_health = self.generate_string_from_int(self.status[hel])         # Aqui ele vai gerar as strings das ints pra apresentar com virgulas
            tot_health = self.generate_string_from_int(self.Max_hp)
            ac_minions = self.generate_string_from_int(self.status[min])
            tot_minions = self.generate_string_from_int(self.Max_Minions)
            regen_minions = self.generate_string_from_int(int(self.Minion_recovery_rate))

            text = ""
            if not self.status["Minions"]:
                text += emojize(":police_car_light::police_car_light::police_car_light::police_car_light::police_car_light::police_car_light::police_car_light::police_car_light:\n")

            regen_time_in_min = self.std_time*(self.recovery_time - self.status[rc])/60
            regen_time_in_hours, regen_time_in_min = divmod(regen_time_in_min, 60)
            text += emojize(
                    #f":sunflower: Sunflower :sunflower:"
                    f"「:sunflower: *Helianth, the Resurrected* :man_zombie:」\n\n"
                    ":police_car_light:PHASE 2!:police_car_light:\n\n"

                    f"{em} Status: {ac_health} / {tot_health}\n"
                    f":bouquet: Servants :man_zombie: {ac_minions} / {tot_minions}\n"
                    f":alarm_clock: Time to regen: {round(regen_time_in_hours)} h {round(regen_time_in_min)} m\n"
                    f":man_zombie: Minions regenerated: {regen_minions}\n"
                    f":skull_and_crossbones:️ Lives Claimed : {self.status[kc]}\n\n"

                    f"「:castle: *THE BARRACKS* :castle:」\n\n"

                    f"Soldiers in battle :fire:\n"
                    f"{len(self.status[pl])} Brave Souls\n\n"

                    )
            if ((self.status["Minions"] or self.changed_to_raw) and not self.changed_to_serv) or (self.changed_to_raw and self.changed_to_serv):
                # Aqui ele calcula o tempo estimado
                if self.status["Minions"] + self.status["Recover count"]*((self.Minion_recovery_rate)/(self.recovery_time)) > self.DPT*(self.recovery_time - self.status["Recover count"]):
                    thing = (self.Minion_recovery_rate)/(self.recovery_time-1) - self.DPT  # Effective damage per turn
                    if thing >= 0:
                        rem_time = "∞"
                    else:


                        remaining  = self.status["Minions"] + self.status["Recover count"]*self.Minion_recovery_rate/(self.recovery_time)
                        rem_turns = -remaining/thing
                        minutes = rem_turns*self.std_time/60

                        hours, minutes = divmod(minutes, 60)

                        days, hours = divmod(hours, 24)

                        rem_time = f"{round(days)}d {round(hours)}h {round(minutes)}m"

                else:
                    thing = -self.DPT
                    remaining  = self.status["Minions"]

                    rem_turns = -remaining/thing
                    minutes = rem_turns*self.std_time/60

                    hours, minutes = divmod(minutes, 60)

                    days, hours = divmod(hours, 24)

                    rem_time = f"{round(days)}d {round(hours)}h {round(minutes)}m"
                if not self.MVP[0]:
                    coisa = ""

                else:
                    coisa = self.server.playersdb.players_and_parties[self.MVP[0]].name
                text += emojize(

                    f"MVP :dagger:\n"
                    f"{coisa}, killing {self.generate_string_from_int(self.MVP[1])} :bouquet: Servants :man_zombie:\n\n"

                    f":bouquet: Servants :man_zombie: killed per turn: {self.generate_string_from_int(self.DPT)}\n"
                    f":hourglass_not_done: Estimated time to expose :sunflower: *Helianth* :sunflower:\n"
                    f"{rem_time}\n\n"

                    )
            else:
                rem_turns = self.status["Health"]/self.DPT
                minutes = rem_turns*self.std_time/60

                hours, minutes = divmod(minutes, 60)

                days, hours = divmod(hours, 24)

                rem_time = f"{round(days)}d {round(hours)}h {round(minutes)}m"
                if not self.MVP[0]:
                    coisa = ""

                else:
                    coisa = self.server.playersdb.players_and_parties[self.MVP[0]].name
                text += emojize(

                    f"MVP :dagger:\n"
                    f"{coisa}, dealing {self.generate_string_from_int(self.MVP[1])} damage per turn.\n\n"

                    f":crossed_swords:️ Damage Dealt per turn: {self.generate_string_from_int(self.DPT)}\n"
                    f":hourglass_not_done: Estimated time to KILL :sunflower: *Helianth* :man_zombie:\n"
                    f"{rem_time}\n\n"

                    )
            if self.changed_to_serv:
                self.changed_to_serv = False

            # for pla in self.status[pl]:
            #     text += f"{self.server.playersdb.players[pla].name}\n"


            if self.status["Health"] > 0:
                self.bot.send_message(text = text, chat_id = self.channel_id, parse_mode = "MARKDOWN")
            if self.changed_to_raw:
                self.changed_to_raw = False

            if self.status["Health"] < 0:           # Texto de morte
                self.status["Is Dead"] = True
                self.server.levelcap = 30
                self.give_rewards()
                text = emojize(

                    f"「:sunflower: *Helianth* :man_zombie:」\n\n"

                    f"The second to fall. A corrupted fragment that lost all control in its hunger\n"
                    f"Now it rots on a valley. Its dreams of overcoming the dark woods were stomped once again.\n"
                    f"But other fragment grows stronger because of this defeat\n"
                    f"{self.status[kc]} brave souls perished during the battle.\n\n"

                    f"Others live to tell the tale.\n"
                    f"Those are the responsible for killing :sunflower: *Helianth* :man_zombie:\n\n"


                )

                for chat in self.status["Players"]:
                    text += emojize(f":sunflower: *{self.server.playersdb.players_and_parties[chat].name}* :sunflower:\n")
                seconds = time.time() - self.status["Started time"]
                minutes, seconds = divmod(seconds, 60)

                hours, minutes = divmod(minutes, 60)

                days, hours = divmod(hours, 24)
                text += emojize(
                    f"\n:alarm_clock: All of this took {round(days)}d {round(hours)}h {round(minutes)}m {round(seconds)}s.\n"

                )
                self.bot.send_message(text = text, chat_id = self.channel_id, parse_mode = "MARKDOWN")

                while self.status["Players"]:
                    chat = self.status["Players"][0]
                    self.remove_player(chat)
                    print(chat)

    def add_player(self, chat_id):
        '''
            Método pra adicionar um jogador à sunflower.

            Parâmetros:

            chat_id (str): chat id do jogador que será adicionado à sunflower
        '''
        self.server.playersdb.players_and_parties[chat_id].location = "WB"
        self.server.playersdb.players_and_parties[chat_id].attacked_the_wb = True
        self.status["Players"].append(chat_id)
        min = "Minions"
        hel = "Health"
        text = emojize(f"You started venturing the :sunflower:sunflower:man_zombie: realm. There You will find his minions,"
                        f" at the moment there are {self.status[min]} of them. When there are none left, The sunflower"
                        f" will be attacked directly, now its health is {self.status[hel]}. You can check your health normally. You can check the rankings on the sunflower: /WB_rankings."
                        f" (be careful, you will take damage over time).\n\nYou can leave at any moment by /run_away. You can see whats going on with the Sunflower with the link: https://t.me/DWSunflower. Good Luck.")
        self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb)

    def remove_player(self,chat_id):
        '''
            Método pra remover um jogador à sunflower.

            Parâmetros:

            chat_id (str): chat id do jogador que será removido da sunflower
        '''
        self.server.playersdb.players_and_parties[chat_id].location = "forest"
        text = "You Stepped back."
        self.status["Players"].remove(chat_id)
        self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb)
        code = self.server.playersdb.players_and_parties[chat_id].pt_code
        if code:
            self.server.playersdb.players_and_parties[code].active = True
            self.server.woods.players[code]["active"] = True
            self.server.playersdb.players_and_parties[code].location = "forest"

    def give_rewards(self):
        for chat,pl in self.server.playersdb.players_and_parties.items():
            if pl.attacked_the_wb:
                drop = "helianth_petal"
                drop = copy(self.Talismandb.talismans[drop])
                self.server.playersdb.players_and_parties[chat].storage.append(drop)
                text = emojize("For taking part in the battle againts :sunflower: Helianth, the Resurrected :man_zombie:, you recieved one petal. Check your /sto!")
                self.bot.send_message(text=text, chat_id=chat, reply_markup=self.defkb)

    def save_status(self):
        '''
            Método que vai salvar a sunflower
        '''
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle(self.status, self.WB_file)
