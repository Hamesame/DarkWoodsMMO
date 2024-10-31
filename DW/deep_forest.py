import helper
import os
import time
import deep_encounters
import death
import player
from emoji import emojize
import random as rd
import traceback


class DeepForestManager:
    class DeepForestPlayer:
        def __init__(self, code, remtime, staytime, boost):
            self.code = code
            self.stay_time = 0
            self.leave_time = -1
            self.is_leaving = False
            self.decision_to_stop = -1
            self.entry_time = time.time()
            self.old_rem_time = remtime
            self.old_stay_time = staytime
            self.next_encounter_time = self.entry_time + rd.randint(int((900-100)/boost),int((900+100)/boost))
            self.is_active = True
            self.counter_next_encounter = False

        def update_time(self):
            c_time = time.time()
            self.stay_time = c_time - self.entry_time

        def come_back(self, time_factor):
            self.is_leaving = True
            self.leave_time = round(self.stay_time*time_factor/4)       # Podia ser boostado pela habilidade do explorer.
            self.decision_to_stop = time.time()
            minutes, seconds = divmod(self.leave_time, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)
            text = emojize(f"You decide to bail from the deep forest and its dangers."
                           f" The travel to the forest will take {days} days {hours} hours {minutes} minutes and {seconds} seconds.")
            return text

        def continue_at_df(self):
            self.is_leaving = False
            self.decision_to_stop = float("inf")
            text = emojize(f'You thought a lot in your way back. "It was a mistake to return". You created courage and re-entered the deep forest to brave its mysteries.')
            return text

    def __init__(self, server):
        self.defkb = server.defkb
        self.server = server
        self.jogs = {}
        self.df_file = "dbs/deep_forest.dat"
        self.df_backup  = "dbs/deep_forest.dat.old"
        loaded = self.server.helper.load_pickle(self.df_file)
        if loaded:
            self.jogs = loaded
        self.encounters = deep_encounters.DeepEncounters(server)
        self.deep_encounters = {
            # "player": [150, self.encounters.player_bat],
            "beast": [1000, self.encounters.normal_beast],
            "megabeast": [100, self.encounters.mega_beast],
            "sanctuary": [75, self.encounters.sanc],
            "weapon": [50, self.encounters.wep],
            "plot_msg": [10, self.encounters.plot_msg],
            "shaman": [10, self.encounters.shaman],
            "oak ash thorn": [1, self.encounters.holy_trees],
            "enchanter": [10, self.encounters.enchanter],
            "blacksmith": [10, self.encounters.blacksmith],
        }
        self.probs = []         # Lista que conterá todas as probabilidades de encontro de players.
        for key, item in self.deep_encounters.items():
            self.probs.append(item[0])
        if self.server.add_new_att:
            new_jogs = {}
            for code,jog in self.jogs.items():
                newjog = self.DeepForestPlayer(code, jog.old_rem_time, 12*3600, self.server.enc_rate_mult)
                list = [f for f in dir(newjog) if not f.startswith("_")]
                for i in list:      # Aqui ele pega os parâmetros do jogador antigo pra setar os do novo. Se prepara
                    try:
                        coisa = getattr(jog,i)      # Pega o parâmetro i e chama tudo de coisa
                        if not callable(coisa):     # Se coisa não for um método... (pois métodos não receberão os atributos do jogaddor antigo)
                            setattr(newjog,i,getattr(jog,i))   # Pega o atributo do jogador tal para adicionar no novo que está sendo criado
                    except AttributeError:  # Caso ele não encontre tal atributo, quer dizer que ele não tem e ele já foi criado, neste caso ele só vai ignorar
                        pass
                new_jogs[code] = newjog    # O jogador de fato é um clone do exemplo pra n bugar nada
            self.jogs = new_jogs

        self.death = death.Death(server)
        self.to_remove = []  # contem os jogadores ou parties mortas na df.
        self.status = [
            # ("cold", 3)
            ("hot", 3)
        ]                   # Contem os status passivos do local.

    def enter(self, code):
        if code in self.server.woods.players:
            self.jogs[code] = self.DeepForestPlayer(code, self.server.woods.players[code]["rem_time"], self.server.woods.players[code]["stay_time"], self.server.enc_rate_mult)
            self.server.woods.remove_from_woods_to_df(code)
            # self.server.woods.players[code]["active"] = False
            self.server.playersdb.players_and_parties[code].location = "deep_forest"

            self.server.playersdb.players_and_parties[code].status = self.status
            if code.startswith("/"):
                self.server.bot.send_message(text="Your party entered the deep forest.", chat_id=self.server.playersdb.players_and_parties[code].chat_ids, reply_markup=self.defkb)
            else:
                self.server.bot.send_message(text="You entered the deep forest.", chat_id=code, reply_markup=self.defkb)

    def leave(self, code):
        if code in self.jogs:
            self.server.woods.add_from_deep_forest(self.server.playersdb.players_and_parties[code], self.jogs[code].old_rem_time, self.jogs[code].old_stay_time)

            # self.server.woods.players[code]["active"] = True
            self.server.playersdb.players_and_parties[code].location = "forest"
            self.server.playersdb.players_and_parties[code].status = []

            del self.jogs[code]
            if code.startswith("/"):
                self.server.bot.send_message(text="Your party left the deep forest.", chat_id=self.server.playersdb.players_and_parties[code].chat_ids)
            else:
                self.server.bot.send_message(text="You left the deep forest.", chat_id=code)

    def death_in_deep_forest(self, code):
        jog = self.server.playersdb.players_and_parties[code]
        self.server.playersdb.players_and_parties[code].status = []
        players = []
        if isinstance(jog, player.Player):
            players.append(jog)
        else:
            players = jog.players
        to_die = []     # Após o encontro, checamos se algum jogador morreu para poder retirá-lo da party e da floresta.
        for jogador in players:
            hp = 0
            for limb in jogador.hp:
                hp+=limb.health
            if hp == 0:
                to_die.append(jogador)

                # self.server.playersdb.players[jogador.chat_id] = jogador
        for jogador in to_die:
            # del self.server.parties_codes[jogador.pt_code][jogador.chat_id]     # Deleta o jogador da party.
            # if len(self.server.parties_codes[jogador.pt_code]) < 13:            # Deleta a party caso ela se torne vazia.
            #     del self.server.parties_codes[jogador.pt_code]
            # del self.players[jogador.pt_code]   # Deleta da floresta.
            self.death.die(jogador.chat_id)     # Roda a morte no jogador.

    def process(self):
        c_time = time.time()
        to_del = []
        to_leave = []
        self.server.megadb.process()
        for chat,jog in self.jogs.items():  # Checa parties ou players fantasmas para serem removidas da df.
            if chat not in self.server.playersdb.players_and_parties:
                to_del.append(chat)
        for i in to_del:
            del self.jogs[i]

        for chat,jog in self.jogs.items(): # Processo dos encontros
            # print(f"jog.is_active = {jog.is_active}\njog.next_encounter_time = {jog.next_encounter_time}")
            try:
                jog.update_time()
                self.server.playersdb.players_and_parties[jog.code].status = self.status
                if self.server.playersdb.players_and_parties[jog.code].location == "deep_forest":
                    jog.is_active = True
                if jog.code[0] != "/":
                    if self.server.playersdb.players_and_parties[jog.code].longest_at_the_df < jog.stay_time:
                        self.server.playersdb.players_and_parties[jog.code].longest_at_the_df = jog.stay_time
                else:
                    for jog2 in self.server.playersdb.players_and_parties[jog.code].players:
                        if jog2.longest_at_the_df < jog.stay_time:
                            jog2.longest_at_the_df = jog.stay_time

                if jog.is_active:
                    if c_time > jog.next_encounter_time:
                        jog.next_encounter_time = c_time + rd.randint(int((900-500)/self.server.enc_rate_mult),int((900+500)/self.server.enc_rate_mult))
                        if jog.stay_time%(12*60*60) < (900+500) and jog.stay_time>6*60*60:
                            encounter = "megabeast"#[100, self.encounters.mega_beast]
                        else:
                            encounter = rd.choices(list(self.deep_encounters.keys()), self.probs)[0]
                        if jog.is_leaving or jog in self.server.megadb.players:
                            while encounter == "megabeast":
                                encounter = rd.choices(list(self.deep_encounters.keys()), self.probs)[0]
                        if jog.counter_next_encounter:
                            jog.counter_next_encounter = False
                        else:
                            self.deep_encounters[encounter][1](chat)

                        self.death_in_deep_forest(chat)     # roda a morte após o encontro.

                if jog.is_leaving:
                    if c_time - jog.decision_to_stop > jog.leave_time:
                        to_leave.append(chat)

            except Exception:
                traceback.print_exc()

        for chat in to_leave:
            self.leave(chat)

        for code in self.to_remove:
            if code in self.jogs:
                del self.jogs[code]
                self.server.playersdb.players_and_parties[code].location = "camp"

        self.to_remove = []

    def save_deep_forest(self):
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle(self.jogs, self.df_file)
