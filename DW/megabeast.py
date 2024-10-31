import os
import deep_beastsdb
import time
import mega_battle
import death
import deep_items
from emoji import emojize
import random as rd
import copy


class MegaBeastMan:
    '''
        Classe criada para controlar o encontro do jogador com a megabeasta e
        a batalha dele com ela.
    '''
    class MegaBeastUser:
        def __init__(self, code, beast, time_factor):
            self.code = code
            self.is_at_battle = False
            self.time_to_arrive = time.time() + 3*60*60*time_factor
            self.beast = beast

    def __init__(self, server):
        self.server = server
        self.def_wait_time = 60
        self.bdbs = deep_beastsdb.DeepBeastsdb()
        self.mbdbs = self.bdbs.megabeasts
        self.dgkb = self.server.keyboards.bs_reply_markup
        self.defkb = self.server.keyboards.class_main_menu_reply_markup
        self.battle_man = mega_battle.BattleMan(server)
        self.death = death.Death(server)
        self.mega_file = "dbs/megas.dat"
        self.players = {}
        self.winners_id = []
        self.Talismandb = deep_items.Talismandb()
        self.chance_to_up_rarity = 0.25
        loaded = self.server.helper.load_pickle(self.mega_file)
        if loaded:
            self.players = loaded

    def add_user(self, code, beast, time_factor):
        self.players[code] = self.MegaBeastUser(code, beast, time_factor)

    def remove_user(self, code):
        if code in self.server.deep_forest_manager.jogs:
            self.server.playersdb.players_and_parties[code].location = "deep_forest"
            self.server.deep_forest_manager.jogs[code].active = True
        del self.players[code]

    def process(self):
        c_time = time.time()
        to_del = []
        to_del2 = []
        #print("started processing the megabeasts...")
        for code,user in self.players.items():
            # if user.time_to_arrive > 3*60*60 + c_time:
            #     user.time_to_arrive = 0
            #print(f"code in self.server.playersdb.players_and_parties: {code in self.server.playersdb.players_and_parties}, code: {code}")
            #print(f"code in self.server.deep_forest_manager.jogs: {code in self.server.deep_forest_manager.jogs}, code: {code}")
            if code in self.server.deep_forest_manager.jogs:
                if code in self.server.playersdb.players_and_parties:
                    #print(f"user.is_at_battle: {user.is_at_battle}")
                    if not user.is_at_battle:
                        if c_time > user.time_to_arrive:
                            user.time_to_arrive = c_time + 15*60                       # seta um número bem grande
                            self.server.helper.append_command("start_mega2", code)
                            text = f"After following the {user.beast.traces} you face a {user.beast.name}. Do you want to face it?"
                            if code[0] == "/":
                                pt = self.server.playersdb.players_and_parties[code]
                                self.server.bot.send_message(text=text, chat_id=pt.chat_ids, reply_markup=self.dgkb)
                            else:
                                self.server.bot.send_message(text=text, chat_id=code, reply_markup=self.dgkb)
                    else:
                        if c_time > user.time_to_arrive:
                            #print("Started the processing at megabeast.py")
                            to_del.extend(self.battle_man.battle(user.code, user.beast))
                            user.time_to_arrive = c_time + 15*60
                else:
                    to_del2.append(code)
            else:
                to_del2.append(code)
        #print("--------------------------------------------")
        for user_id in to_del:
            if user_id in self.players:
                self.remove_user(user_id)

            self.death.die(user_id)
        for user_id in to_del2:
            if user_id in self.players:
                self.remove_user(user_id)

        for id in self.winners_id:
            # Primeiramente somente a opção de lootear a besta
            deep_beast = self.players[id].beast
            if id in self.server.deep_forest_manager.jogs:
                power_level = int(self.server.deep_forest_manager.jogs[id].stay_time/(3*3600)) + 1
            else:
                power_level = 1
            text = emojize( f"After a long fight, the {deep_beast.name} is dead. And after butchering the beast, you got those items:\n\n")
            if not self.server.playersdb.players_and_parties[id].pt_code and self.server.playersdb.players_and_parties[id].classe == "Druid":
                deep_beast.attack = power_level*self.battle_man.power_multiplier*deep_beast.attack
                self.server.playersdb.players_and_parties[id].beast_in_stack = deep_beast

            drops = []
            probs = []         # Lista que conterá todas as probabilidades dos drop
            for key, item in deep_beast.drop.items():
                probs.append(item)
            for rounds in range(power_level):   # para cada power level ele pode dropar um item da besta
                drop = rd.choices(list(deep_beast.drop.keys()), probs)[0]
                if drop != "nothing":
                    drop = copy.deepcopy(self.Talismandb.talismans[drop])
                    rarity_up = 0
                    for r2 in range(power_level):   # Para cada power level ele tem a chance de 75% de aumentar em 1 a raridade do item.
                        n = rd.random()
                        if n < self.chance_to_up_rarity:
                            rarity_up += 1
                    # print(f"rarity_up = {rarity_up}, drop.rarity: {drop.rarity}")
                    if drop.rarity + rarity_up > 6:
                        rarity_up = 6 - drop.rarity

                    drop.rarity += rarity_up
                    # print(f"rarity_up = {rarity_up}, drop.rarity: {drop.rarity}")
                    # print("---------------------")
                    for power_name, power in drop.powers.items():
                        drop.powers[power_name] = power*(rarity_up + 1)
                    text += f"*{drop}*\n"
                    drops.append(drop)

            if id[0] == "/":
                for pl in self.server.playersdb.players_and_parties[id].players:
                    pl.storage.extend(copy.deepcopy(drops))
                self.server.bot.send_message(text=text, chat_id=self.server.playersdb.players_and_parties[id].chat_ids, parse_mode = 'MARKDOWN')
            else:
                self.server.playersdb.players_and_parties[id].storage.extend(drops)
                self.server.bot.send_message(text=text, chat_id=id, parse_mode = 'MARKDOWN')
            self.server.deep_forest_manager.jogs[id].counter_next_encounter = True
            self.remove_user(id)
        self.winners_id = []

    def save_mega(self):
        '''
            Salva a estrutura que você quer criar
        '''
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle(self.players, self.mega_file)
