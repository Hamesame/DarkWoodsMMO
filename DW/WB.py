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
        self.std_time = 15*60           # 15 minutos
        self.status = {"Health":round(3.5e6), "Players":[], "Kill count":0, "Is Dead":False, "Started time":time.time()}
        self.injured = []   # Lista de jogadores com vida abaixo de certo valor
        self.MVP = ["",0]   # Melhor jogador
        self.DPT = 0        # Dano por turno

        self.WB_file = "dbs/WB.dat"
        loaded = self.helper.load_pickle(self.WB_file)  # Carrega o WB
        if loaded:
            self.status = loaded
            # self.dungeons_in_progress = loaded

        self.Max_hp = round(3.5e6)       # Hp máximo do boss


        self.last_processed = 0
        self.channel_id = "-1001123425316" # Channel id
        self.dona_morte = death.Death(server)

        self.hp = [":green_heart:",":yellow_heart:",":orange_heart:",":red_heart:️",":broken_heart:",":black_heart:"]
        # Lista de stats do WB, a medida q ele vai perdendo vida, ele vai mostrando corações diferentes

    def do_things(self,jogador):
        '''
            Método que processa cada jogador individualmente dentro da batalha.

            Parâmetros:

            jogador (Player): jogador que será processado
        '''
        dead = False
        jogador.location = "WB"

        power = 0
        if jogador.armor:
            if "cold" in jogador.armor.status_protection:
                power = jogador.armor.status_protection["cold"]

        a = 1
        b = 0
        c = -3.3
        x = power
        took_damage = "haven't"
        dam_prob = a/(x-c) + b    # Função de cálculo da probabilidade do jogador levar 1 de dano
        thing = rd.random()
        if dam_prob > thing:
            took_damage = "have"
            res = jogador.take_damage()
            if res == -1:
                dead = True

        heal = 0
        for limb in jogador.hp:
            heal += limb.health
        injured = False
        if heal < 5:
            injured = True
            self.injured.append(jogador.chat_id)    # Se o jogador estiver com menos de 5 de vida, ele vai parar na lista dos injured

        damage = 0
        if jogador.weapon:
            if "fire" in jogador.weapon.powers:
                damage = jogador.weapon.powers["fire"]*(jogador.buff_man.buff_state + 1)


        self.status["Health"] -= damage

        if self.MVP[1] < damage:            # Define o mvp
            self.MVP[0] = jogador.chat_id
            self.MVP[1] = damage
        self.DPT += damage

        report = emojize(
                            f"You {took_damage} taken damage last turn.\n"
                            f"To protect yourself, use armor.\n\n"
        )

        if injured:
            report += emojize("Warning :warning:️ Low Health!\n\n")

        report += emojize(
                        f"You have dealt {damage} this turn, You can only deal damage with :fire: *fire* :fire: weapons!"
        )
        jogador.last_wb_report = report

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
        pl = "Players"
        kc = "Kill count"

        if not self.status["Is Dead"]:
            self.injured = []
            self.MVP = ["",0]
            self.DPT = 0                # Toda vez ele da uma resetada nos jogadores machucados, mvp e dpt



            for chat in self.status[pl]:

                self.do_things(self.server.playersdb.players_and_parties[chat])     # Cada jogador é processado individualmente aqui



            frac = self.status["Health"]/self.Max_hp            # Para calcular qual emoji usar
            if frac < 0:
                frac = 0
            other_frac = 1-frac
            thing = round(other_frac*5)
            em = self.hp[thing]
            # print(f"frac = {frac}\nother_frac = {other_frac}\nthing = {thing}")


            ac_health = self.generate_string_from_int(self.status[hel])         # Aqui ele vai gerar as strings das ints pra apresentar com virgulas
            tot_health = self.generate_string_from_int(self.Max_hp)

            text = ""


            text += emojize(
                    #f":sunflower: Sunflower :sunflower:"
                    f"「:snowflake: *Sairacaz, Blizzard Elemental* :snowflake:」\n\n"


                    f"{em} Status: {ac_health} / {tot_health}\n"
                    f":skull_and_crossbones:️ Lives Claimed : {self.status[kc]}\n\n"

                    f"「:castle: *THE BARRACKS* :castle:」\n\n"

                    f"Soldiers in battle :fire:\n"
                    f"{len(self.status[pl])} Brave Souls\n\n"

                    )

            if self.DPT != 0:
                rem_turns = self.status["Health"]/self.DPT


                minutes = rem_turns*self.std_time/60

                hours, minutes = divmod(minutes, 60)

                days, hours = divmod(hours, 24)

                rem_time = f"{round(days)}d {round(hours)}h {round(minutes)}m"
            else:
                rem_time = "∞"

            if not self.MVP[0]:
                coisa = ""

            else:
                coisa = self.server.playersdb.players_and_parties[self.MVP[0]].name
            text += emojize(

                f"MVP :dagger:\n"
                f"{coisa}, dealing {self.generate_string_from_int(self.MVP[1])} damage per turn.\n\n"

                f":crossed_swords:️ Damage Dealt per turn: {self.generate_string_from_int(self.DPT)}\n"
                f":hourglass_not_done: Estimated time to KILL :snowflake: *Sairacaz* :snowflake:\n"
                f"{rem_time}\n\n"

                )


            # for pla in self.status[pl]:
            #     text += f"{self.server.playersdb.players[pla].name}\n"


            if self.status["Health"] > 0:
                self.bot.send_message(text = text, chat_id = self.channel_id, parse_mode = "MARKDOWN")


            if self.status["Health"] < 0:           # Texto de morte
                self.status["Is Dead"] = True
                self.server.levelcap = 40
                self.give_rewards()
                text = emojize(

                    f"「:snowflake: *Sairacaz, Blizzard Elemental* :snowflake:」\n\n"

                    f"The Third to fall. A corrupted fragment that lost all control in its hunger.\n"
                    f"You now feel the warmth of the sun on your face.\n"
                    f"But other fragment grows stronger because of this defeat.\n"
                    f"{self.status[kc]} brave souls perished during the battle.\n\n"

                    f"Others live to tell the tale.\n"
                    f"Those are the responsible for killing :snowflake: *Sairacaz, Blizzard Elemental* :snowflake:\n\n"


                )

                for chat in self.status["Players"]:
                    s = emojize(f":snowflake: *{self.server.playersdb.players_and_parties[chat].name}* :snowflake:\n")
                    s = s.replace("_", "\\_")
                    s = s.replace("*", "\\*")
                    text += s
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
        text = emojize(f"You started venturing the :snowflake: Blizzard :snowflake: mountain. There You will fight against Sairacaz, Blizzard Elemental,"
                        f" now its health is {self.status[hel]}. You can check your health normally. You can check the rankings on: /WB_rankings."
                        f" The only way of dealing damage is by using :fire: *fire* :fire:."
                        f" To check the last turn report, use /WB_report."
                        f" (be careful, you will take damage over time).\n\nYou can leave at any moment by /run_away. You can see whats going on with the Snow Storm with the link: https://t.me/DWSunflower. Good Luck.")
        text = text.replace("_", "\\_")
        self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb, parse_mode="MARKDOWN")

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
                drop = "reverse_entropy_shard"
                drop = copy(self.Talismandb.talismans[drop])
                self.server.playersdb.players_and_parties[chat].storage.append(drop)
                text = emojize("For taking part in the battle againts :snowflake: Sairacaz, Blizzard Elemental :snowflake:, you recieved one shard. Check your /sto!")
                self.bot.send_message(text=text, chat_id=chat, reply_markup=self.defkb)

    def save_status(self):
        '''
            Método que vai salvar a sunflower
        '''
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle(self.status, self.WB_file)
