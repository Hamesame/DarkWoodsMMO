###############################
#  Classe da F L O R E S T A  #
###############################

import forest_encounters
import random as rd
import time
import os
from telegram.error import Unauthorized
import items
import player
import death
import copy
from emoji import emojize
import traceback

class Woods:
    '''
        Classe que representa a floresta do Dark Woods.
    '''
    def __init__(self, server):
        self.server = server
        self.death = death.Death(server)
        self.encounters = forest_encounters.Encounters(server)
        self.pt_encounters = forest_encounters.pt_Encounters(server)
        self.players = {}       # Dicionário que conterá todos os players e paries na floresta.
        self.woods_file = "dbs/woods.dat"
        self.woods_backup = "dbs/woods.dat.old"
        self.helper = server.helper
        self.to_remove = {"exit": [], "remove": []}    # Lista que será usada para remover players de self.players ao final do processo da floresta.

        loaded = self.helper.load_pickle(self.woods_file)
        if loaded:
            # Atualizamos os players na floresta para os players verdadeiros na db,
            # para evitar clonagem ao carregar os jogadores na floresta.
            for code in self.server.playersdb.players_and_parties:
                if code in loaded:
                    loaded[code]["player"] = self.server.playersdb.players_and_parties[code]
            self.players = loaded

        # dicti = {}
        # for key, pl in self.players.items():
        #     dicti[key] = {}
        #     for coisa,coisa1 in pl.items():
        #         if coisa == "player":
        #             if isinstance(coisa1, dict):
        #                 dicti[key]["player"] = self.server.parties_codes[coisa1["code"]]
        #             else:
        #                 dicti[key]["player"] = self.server.playersdb.players[coisa1.chat_id]
        #         else:
        #             dicti[key][coisa] = self.players[key][coisa]
        #
        # self.players = dicti

            # if isinstance(pl["player"], dict):
            #     pl["player"] = self.server.parties_codes[pl["player"]["code"]]
            # else:
            #     pl["player"] = self.server.playersdb.players[pl["player"].chat_id]

        self.trip_time = 15*60
        self.firstenc_lowert = int(700/self.server.enc_rate_mult)       # O tempo de encontro de cada jog/party será um valor aleatório dentro de um intervalo.
        self.firstenc_highert = int(1100/self.server.enc_rate_mult)
        self.enc_lowert = int(100/self.server.enc_rate_mult)
        self.enc_highert = int(1700/self.server.enc_rate_mult)
        # dg prob = 10
        # item prob = 30
        # dg_map prob = 10
        self.encounters = {
            "plot_msg": [10, self.encounters.plot_msg],
            "leg_beast": [10, self.encounters.legendary_beast],
            "dg": [10, self.encounters.dungeon],
            "bs": [20, self.encounters.blacksmith],
            "item": [30, self.encounters.item],
            "player": [150, self.encounters.player_bat],
            "beast": [1000, self.encounters.normal_beast],
            "map": [10, self.encounters.map],
            "sanct": [40, self.encounters.sanctu],
            "deep_forest": [40, self.encounters.df],
            # "caverns": [40, self.encounters.caverns],
        }       # Dicionário com todos os encontros possíveis.
        self.pt_encounters = {
            "plot_msg": [10, self.pt_encounters.pt_plot_msg],
            "leg_beast": [10, self.pt_encounters.pt_legendary_beast],
            "dg": [10, self.pt_encounters.pt_dungeon],
            "item": [30, self.pt_encounters.pt_item],
            "player": [150, self.pt_encounters.pt_player_bat],
            "beast": [1000, self.pt_encounters.pt_normal_beast],
            "map": [10, self.pt_encounters.pt_map],
            "sanct": [40, self.pt_encounters.sanctu],
            "deep_forest": [40, self.pt_encounters.pt_df],
            # "caverns": [40, self.pt_encounters.caverns],
        }
        self.probs = []         # Lista que conterá todas as probabilidades de encontro de players.
        for key, item in self.encounters.items():
            self.probs.append(item[0])

        self.pt_probs = []      # Idem para party.
        for key, item in self.pt_encounters.items():
            self.pt_probs.append(item[0])


        self.timestamp0 = time.time()
        self.timestamp = time.time()        # Marca o tempo atual para comparação e atualização.

    def add_to_woods(self, jog, rem_time):
        '''
            Adiciona um player ou party na floresta, isto é, apenda no dicionário self.players.

            Parâmetros:
                jog (class or dict): jogador ou party que entrará na floresta;
                rem_time (int): tempo remanescente do player ou party na floresta.
        '''

        self.server.update_woods = True     # Indica que houve alterações na floresta para serem atualizadas.
               # No caso, qualquer habilidade possível de ser usada no jogo só pode ser usada na floresta. Então os status são resetados antes de entrar na floresta por garantia (maybe).
        self.players[jog.code] = {
            "player": jog,
            "stay_time": rem_time,
            "rem_time": rem_time,
            "rem_enctime": rd.randint(self.firstenc_lowert, self.firstenc_highert),
            "active": True
        }                       # Adiciona o player no dicionário que contém todos os jogadores e parties na floresta.
        self.server.playersdb.players_and_parties[jog.code].location = "forest"
        self.server.playersdb.players_and_parties[jog.code].active = True
        self.server.playersdb.players_and_parties[jog.code].reset_stats()
        # if not isinstance(jog, player.Player):
        #     for jogador in jog.players:
        #         print([jogador.chat_id, jogador.location, jogador.classe])

    def add_from_deep_forest(self, jog, rem_time, stay_time):
        '''
            Adiciona um player ou party na floresta, isto é, apenda no dicionário self.players.

            Parâmetros:
                jog (class or dict): jogador ou party que entrará na floresta;
                rem_time (int): tempo remanescente do player ou party na floresta.
        '''

        self.server.update_woods = True     # Indica que houve alterações na floresta para serem atualizadas.
               # No caso, qualquer habilidade possível de ser usada no jogo só pode ser usada na floresta. Então os status são resetados antes de entrar na floresta por garantia (maybe).
        self.players[jog.code] = {
            "player": jog,
            "stay_time": stay_time,
            "rem_time": rem_time,
            "rem_enctime": rd.randint(self.firstenc_lowert, self.firstenc_highert),
            "active": True
        }                       # Adiciona o player no dicionário que contém todos os jogadores e parties na floresta.
        self.server.playersdb.players_and_parties[jog.code].location = "forest"
        self.server.playersdb.players_and_parties[jog.code].active = True
        # self.server.playersdb.players_and_parties[jog.code].reset_stats()

    def exit_woods(self, code):
        '''
            Função que é chamada quando o jogador ou party sai da floresta após seu tempo remanescente terminar.

            Parâmetros:
                chat_id (str): Telegram chat ID de um player, ou o código de uma party.
        '''
        if code in self.players:
            if self.players[code]["active"]:
                if code[0] == "/":
                    if code in self.server.playersdb.players_and_parties:
                        text = "Your party has returned from the forest"
                        for player in self.server.playersdb.players_and_parties[code].players:
                            self.server.bot.send_message(text = text, chat_id = player.chat_id, reply_markup = self.server.keyboards.at_camp_main_menu_reply_markup)
                            if player.check_level_up():
                                self.server.helper.append_command("level_up", player.chat_id)
                else:
                    text = "You have returned from the forest"
                    self.server.bot.send_message(text = text, chat_id = code, reply_markup = self.server.keyboards.at_camp_main_menu_reply_markup)
                    if self.server.playersdb.players_and_parties[code].check_level_up():
                        self.server.helper.append_command("level_up", code)
                self.remove_from_woods(code)     # Remove do dicionário self.players

    # def pt_exit_woods(self, name):
    #     '''
    #         Função que é chamada quando o uma party sai da floresta após seu tempo remanescente terminar.
    #
    #         Parâmetros:
    #             name (str): código de uma party.
    #     '''
    #     if name in self.players:
    #         if not name in self.server.parties_codes:
    #             del self.players[name]
    #         else:
    #             if self.players[name]["active"]:
    #                 text = "Your party has returned from the forest"
    #                 for chat_id,jogador in self.server.parties_codes[name].items():
    #                     if isinstance(jogador, player.Player):
    #                         self.server.bot.send_simple_message(text, chat_id)
    #                         if self.server.playersdb.players[chat_id].check_level_up():
    #                             self.server.helper.append_command("level_up", chat_id)
    #             self.pt_remove_from_woods(name)

    def remove_from_woods(self, code):
        '''
            Função que remove os jogadores da floresta. Pode ser acessada por adms para kickar pessoas da floresta.

            Parâmetros:
                chat_id (str): chat ID do jogador a ser removido.
        '''
        self.server.update_woods = True
        #self.players[chat_id]["player"].is_at_forest = False
        if code in self.players:
            self.players[code]["active"] = False

        if code in self.server.dungeon_master.dungeons_in_progress:  # Checa se o player está numa dungeon. Caso sim, a dungeon é abortada.
            self.server.helper.remove_command("start_dg", code)
            self.server.helper.remove_command("pt_start_dg", code)  # Se for chat_id, não dá problema, devido a como o append_command funciona.
            del self.server.dungeon_master.dungeons_in_progress[code]
        if code in self.server.blacksmith.bs_in_progress:            # Idem para o blacksmith.
            self.server.helper.remove_command("start_bs", code)
            self.server.blacksmith.clear_blacksmith(code)
            # del self.server.blacksmith.bs_in_progress[code]

        if code in self.server.playersdb.players_and_parties:
            self.server.playersdb.players_and_parties[code].location = "camp"
            self.server.playersdb.players_and_parties[code].reset_stats()
        if code in self.players:
            del self.players[code]

    def remove_from_woods_to_df(self, code):
        '''
            Função que remove os jogadores da floresta. Pode ser acessada por adms para kickar pessoas da floresta.

            Parâmetros:
                chat_id (str): chat ID do jogador a ser removido.
        '''
        self.server.update_woods = True
        #self.players[chat_id]["player"].is_at_forest = False
        if code in self.players:
            self.players[code]["active"] = False

        if code in self.server.dungeon_master.dungeons_in_progress:  # Checa se o player está numa dungeon. Caso sim, a dungeon é abortada.
            self.server.helper.remove_command("start_dg", code)
            self.server.helper.remove_command("pt_start_dg", code)  # Se for chat_id, não dá problema, devido a como o append_command funciona.
            del self.server.dungeon_master.dungeons_in_progress[code]
        if code in self.server.blacksmith.bs_in_progress:            # Idem para o blacksmith.
            self.server.helper.remove_command("start_bs", code)
            del self.server.blacksmith.bs_in_progress[code]

        if code in self.server.playersdb.players_and_parties:
            self.server.playersdb.players_and_parties[code].location = "camp"
        if code in self.players:
            del self.players[code]

    # def pt_remove_from_woods(self, name):
    #     '''
    #         Função que remove as parties da floresta. Pode ser acessada por adms para kickar pessoas da floresta.
    #
    #         Parâmetros:
    #             name (str): código da party a ser removida.
    #     '''
    #     self.players[name]["player"]["is_at_forest"] = False
    #     self.players[name]["active"] = False
    #     for chat_id,jogador in self.server.parties_codes[name].items():     # Dungeons precisam ser abortadas. Para isso é escolhido um player qualquer da party e um "NOPE" é forçado por este player.
    #         if isinstance(jogador, player.Player):
    #             caller_id = chat_id
    #             break
    #     if name in self.server.dungeon_master.dungeons_in_progress:
    #         # self.server.helper.remove_command("start_dg", name)
    #         self.server.dungeon_master.pt_dungeon_iteration(caller_id, name, emojize("NOPE :thumbs_down:"))
    #
    #     # Precisa fazer as dungeons primeiro
    #
    #     for chat_id, jogador in self.server.parties_codes[name].items():
    #         if isinstance(jogador, player.Player):
    #             jogador.reset_stats()
    #             self.server.playersdb.players[jogador.chat_id].reset_stats()
    #             self.server.playersdb.players[jogador.chat_id].location = "camp"
    #             jogador.is_at_forest = False
    #     del self.players[name]


    def pause_woods(self, code):
        '''
            Desativa um jogador. Dessa forma ele não será visto pelo jogo (sem batalhas) e seus tempos remanescentes são congelados.
        '''
        self.players[code]["active"] = False


    def resume_woods(self, code):
        '''
            Reativa um jogador. Dessa forma seus tempos remanescentes voltam a serem atualizados e outros players podem encontrá-lo numa batalha.
        '''
        self.players[code]["active"] = True

    def save_woods(self):
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.helper.save_pickle(self.players, self.woods_file)

    def death_in_forest(self, jog):
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
        t0 = time.time()
        self.timestamp0 = time.time()       # Marca um tempo de referência novo.
        # to_del = []         # Parties vazias serão deletadas da floresta.
        # for code, woodplayer in self.players.items():            # To remove empty parties from forest
        #     if not isinstance(woodplayer["player"], player.Player):
        #         pl = "player"
        #         cd = "code"
        #         # print(f"woodplayer: {woodplayer[pl]}, len: {len(woodplayer[pl])}")
        #         if not woodplayer["player"].players:
        #             to_del.append(woodplayer["player"]["code"])
        #
        # for inst in to_del:
        #     del self.players[inst]
        # del to_del
        self.server.deep_forest_manager.process()
        for code, woodplayer in self.players.items():
            if woodplayer["player"].location == "forest":
                if not woodplayer["active"]:
                    print("Player was not active")
                    woodplayer["active"] = True

            try:
                if woodplayer["active"]:        # Os processos da floresta só rodam se o jogador for ativo.
                    # if isinstance(woodplayer["player"], dict):      # A localização de todos os players e de parties são atualizados para floresta.
                    #     woodplayer["player"] = self.server.parties_codes[woodplayer["player"]["code"]]
                    #     cod = woodplayer["player"]["code"]
                    #     self.server.parties_codes[cod]["location"] = "forest"
                    #     for chat,jog in woodplayer["player"].items():
                    #         if isinstance(jog, player.Player):
                    #             self.server.playersdb.players[chat].location = "forest"
                    #             woodplayer["player"][chat].location = "forest"
                    #             self.server.parties_codes[cod][chat].location = "forest"
                    # else:
                    #     self.server.playersdb.players[woodplayer["player"].chat_id].location = "forest"
                    deltat = self.timestamp0 - self.timestamp   # Calcula a diferença de tempo entre o último processo e o novo.
                    woodplayer["rem_time"] -= deltat            # Atualiza o tempo remanescente de todos os jogadores.
                    woodplayer["rem_enctime"] -= deltat         # Atualiza o tempo remanescente de encontro de todos os jogadores.
                    if woodplayer["rem_time"] < 0:              # Se o tempo acabar, ele será removido ao final do processo.
                        self.to_remove["exit"].append(code)

                    if woodplayer["player"].is_travelling:
                        if woodplayer["player"].travel_time > 0:    # Atualiza o tempo de viagem.
                            woodplayer["player"].travel_time -= deltat
                        if woodplayer["player"].travel_time <= 0:
                            self.server.travelman.arrive(woodplayer["player"])

                    # if not isinstance(woodplayer["player"], dict):      # Checa se o player está viajando para algum lugar (dg ou bs por exemplo). Caso sim, atualizará o tempo de chegada e/ou executará o local.
                    #     if woodplayer["player"].is_travelling:
                    #         if woodplayer["player"].travel_time > 0:    # Atualiza o tempo de viagem.
                    #             woodplayer["player"].travel_time -= deltat
                    #         if woodplayer["player"].travel_time <= 0:
                    #             if woodplayer["player"].travelling_loc == "dg_map":
                    #                 for item in woodplayer["player"].inventory:
                    #                     if isinstance(item, items.dg_map):
                    #                         text = "The dusty map have led you to the destination"
                    #                         self.server.bot.send_message(text=text,chat_id=chat_id)
                    #                         item.chegou(woodplayer["player"])
                    #                         self.encounters["dg"][1](chat_id)
                    #                         break
                    #             elif woodplayer["player"].travelling_loc == "death_site":           # Checa se o jogador estava indo buscar seus itens.
                    #                 woodplayer["player"].is_travelling = False
                    #                 woodplayer["player"].travel_time = 0
                    #                 woodplayer["player"].travelling_loc = ""
                    #                 woodplayer["player"].inventory.extend(woodplayer["player"].ghost_inv)   # Copia todas os itens do ghost inv para o inv original.
                    #                 woodplayer["player"].ghost_inv = []                                     # Reseta o ghost inv.
                    #                 player_leg_item = [copy.deepcopy(item) for item in self.server.itemsdb.weapons if item.owner == woodplayer["player"].chat_id]    # Iremos buscar os itens lendários do jogador para readicioná-los em seu inv.
                    #                 woodplayer["player"].inventory.extend(player_leg_item)
                    #                 for item in player_leg_item:
                    #                     self.server.itemsdb.remove_weapon_from_pool(item)
                    #                 del player_leg_item
                    #                 text = emojize(f"After following your footsteps for a while, you come accross your old body, a comical skeleton still wearing most of your old gear."
                    #                                 f" You pocket whatever wasn't scavenged and your memories come flooding back..."
                    #                                 f" yes, that's right! You were the villain this whole time!"
                    #                                 f" Now that you've cast off suspicion, you can finally resume your master plan to-\n\n"
                    #                                 f" Wait, these aren't your memories; yours are over here."
                    #                                 f" Good thing you're just a regular, unsuspecting adventurer."
                    #                                 f" Yep, that's you. Nothing to see here, no sir.")
                    #                 self.server.bot.send_message(text=text,chat_id=chat_id)
                    #
                    #                 # Talvez seja uma boa ideia codar um travelman
                    #             else:
                    #                 loc = woodplayer["player"].travelling_loc
                    #                 text = "The travel book have led you to the destination"
                    #                 self.server.bot.send_message(text=text,chat_id=chat_id)
                    #                 woodplayer["player"].chegou(woodplayer["player"].travelling_loc)
                    #                 self.encounters[loc][1](chat_id)
                    #
                    # else:           # Para parties será similar.
                    #     if woodplayer["player"]["is_travelling"]:
                    #         if woodplayer["player"]["travel_time"] > 0:
                    #             woodplayer["player"]["travel_time"] -= deltat
                    #         if woodplayer["player"]["travel_time"] <= 0:
                    #             if woodplayer["player"]["travelling_loc"] == "dg_map":
                    #                 # for chat_id,jogador in woodplayer["player"].items():
                    #                 #     if isinstance(jogador, player.Player):
                    #                 #         for item in jogador:
                    #                 #             if isinstance(item, items.dg_map):
                    #                 #                 item.chegou(jogador)
                    #                 #                 self.pt_encounters["dg"][1](woodplayer["player"]["code"])
                    #                 #                 break
                    #
                    #                 encounter = "dg"
                    #                 for inv_item in woodplayer["player"]["pt_inv"]:        # Para utilizar o dusty map, ao chegar no local o mapa deve ser destruído. Um dg map é escolhido do inventário da party para ser sacrificado.
                    #                     if isinstance(inv_item, items.dg_map):              # Isto não causa nenhum problema, pois para se usar dg_map é necessário compartilhar o item primeiro (ver player_comms.py).
                    #                         item.chegou(woodplayer["player"])
                    #                         break
                    #                         #test
                    #                 text = emojize(f"The Dusty map :world_map: have led your group to the destination.")
                    #                 for chat,jog in woodplayer["player"].items():
                    #                     if isinstance(jog,player.Player):
                    #                         self.server.bot.send_message(text=text,chat_id=chat)
                    #                 self.pt_encounters[encounter][1](woodplayer["player"]["code"])      # Executa o encontro (neste caso uma dungeon).
                    #                 woodplayer["rem_enctime"] = rd.randint(self.enc_lowert, self.enc_highert)   # Reseta o tempo de encontro.
                    #                 to_die = []     # Após o encontro, checamos se algum jogador morreu para poder retirá-lo da party e da floresta.
                    #                 for chat_id,jogador in woodplayer["player"].items():
                    #                     if isinstance(jogador, player.Player):
                    #                         hp = 0
                    #                         for limb in jogador.hp:
                    #                             hp+=limb.health
                    #                         if hp == 0:
                    #                             to_die.append(jogador)
                    #
                    #                         self.server.playersdb.players[jogador.chat_id] = jogador
                    #                 for jogador in to_die:
                    #                     del self.server.parties_codes[jogador.pt_code][jogador.chat_id]     # Deleta o jogador da party.
                    #                     if len(self.server.parties_codes[jogador.pt_code]) < 13:            # Deleta a party caso ela se torne vazia.
                    #                         del self.server.parties_codes[jogador.pt_code]
                    #                     del self.players[jogador.pt_code]   # Deleta da floresta.
                    #                     self.death.die(jogador.chat_id)     # Roda a morte no jogador.
                    #             else:       # Similar ao código anterior.
                    #                 loc = woodplayer["player"]["travelling_loc"]
                    #                 woodplayer["player"]["is_travelling"] = False
                    #                 woodplayer["player"]["travel_time"] = 0
                    #                 woodplayer["player"]["travelling_loc"] = ""
                    #                 for chat,jog in woodplayer["player"].items():
                    #                     if isinstance(jog, player.Explorer):
                    #                         if loc in jog.travel_book:
                    #
                    #                             text = f"{jog.name} have led your group to the destination."
                    #                             for chat2,jog2 in woodplayer["player"].items():
                    #                                 if isinstance(jog2,player.Player):
                    #                                     self.server.bot.send_message(text=text,chat_id=chat2)
                    #
                    #                             jog.travel_book.remove(loc)
                    #                             chng = False
                    #                             if loc =="plot_msg":
                    #                                 loc = "sunflower"
                    #                                 chng = True
                    #
                    #                             del jog.actions[f"/g_{loc}"]
                    #                             if chng:
                    #                                 loc = "plot_msg"
                    #
                    #                             break
                    #                 # woodplayer["player"].chegou(woodplayer["player"]["travelling_loc"])
                    #
                    #                 self.pt_encounters[loc][1](woodplayer["player"]["code"])



                    if woodplayer["rem_time"] > 0:


                        if woodplayer["rem_enctime"] < 0:   # Um encontro aleatório será ativado.

                            if isinstance(woodplayer["player"], player.Player):
                                try:
                                    if not woodplayer["player"].classe == "Explorer":       # Explorers mudam a taxa de encontro e a probabilidade de encontros raros.
                                        encounter = rd.choices(list(self.encounters.keys()), self.probs)[0]
                                        self.encounters[encounter][1](code)
                                        woodplayer["rem_enctime"] = rd.randint(self.enc_lowert, self.enc_highert)
                                    else:       # As probabilidades devem ser atualizadas para o Explorer. Além disso, novos comandos devem ser registrados em seu travel_book.
                                        newprob = []
                                        for i in range(len(self.probs)):
                                            newprob.append(self.probs[i] + woodplayer["player"].prob_boost)
                                        # newprob.append(100)
                                        encounter = rd.choices(list(self.encounters.keys()), newprob)[0]

                                        if (encounter in ["dg", "bs", "plot_msg", "sanct", "deep_forest"]) and (encounter not in woodplayer["player"].travel_book):
                                            woodplayer["player"].add_to_travel_book(encounter)
                                        # if encounter == "dg" and encounter not in woodplayer["player"].travel_book:
                                        #     woodplayer["player"].travel_book.append(encounter)
                                        #     woodplayer["player"].create_coms(encounter)
                                        # if encounter == "bs" and encounter not in woodplayer["player"].travel_book:
                                        #     woodplayer["player"].travel_book.append(encounter)
                                        #     woodplayer["player"].create_coms(encounter)
                                        # if encounter == "plot_msg" and encounter not in woodplayer["player"].travel_book:
                                        #     woodplayer["player"].travel_book.append(encounter)
                                        #     woodplayer["player"].create_coms(encounter)

                                        self.encounters[encounter][1](code)
                                        woodplayer["rem_enctime"] = rd.randint(round(self.enc_lowert/woodplayer["player"].enc_time_multiplier), round(self.enc_highert/woodplayer["player"].enc_time_multiplier)) # A taxa de encontros do explorer entra aqui.
                                    self.death_in_forest(woodplayer["player"])

                                except Unauthorized:    # Se algum erro é encontrado, o player será removido da floresta e seus comandos resetados.
                                    self.to_remove["remove"].append(code)
                                    self.server.messageman.waiting_from[code] = {}
                                    del self.server.messageman.waiting_from[code]


                            else:       # Se for uma party, o código é similar.

                                try:
                                    exp_number = 0      # Conta o número de explorers numa party.
                                    for jogador in woodplayer["player"].players:

                                        # if isinstance(jogador, player.Player):

                                        if jogador.classe == "Explorer":
                                            exp_number += 1
                                            newprob = []
                                            for i in range(len(self.pt_probs)):
                                                newprob.append(self.pt_probs[i] + jogador.prob_boost)
                                            # newprob.append(100)
                                            encounter = rd.choices(list(self.pt_encounters.keys()), newprob)[0]
                                            if (encounter in ["dg", "plot_msg", "sanct", "deep_forest"]) and (encounter not in jogador.travel_book):
                                                jogador.add_to_travel_book(encounter)
                                            # if encounter == "dg" and encounter not in jogador.travel_book:
                                            #     jogador.travel_book.append(encounter)
                                            #     jogador.create_coms(encounter)
                                            # if encounter == "plot_msg" and encounter not in jogador.travel_book:
                                            #     jogador.travel_book.append(encounter)
                                            #     jogador.create_coms(encounter)
                                                # precisa criar a dg do explorer qd usa a habilidade
                                            self.pt_encounters[encounter][1](jogador.pt_code)
                                            woodplayer["rem_enctime"] = rd.randint(round(self.enc_lowert/jogador.enc_time_multiplier), round(self.enc_highert/jogador.enc_time_multiplier))
                                            break
                                    if not exp_number:      # Se não houver explorers na party, a taxa e a prob de encontro são as do server.
                                        encounter = rd.choices(list(self.pt_encounters.keys()), self.pt_probs)[0]
                                        self.pt_encounters[encounter][1](woodplayer["player"].pt_code)
                                        woodplayer["rem_enctime"] = rd.randint(self.enc_lowert, self.enc_highert)

                                    self.death_in_forest(woodplayer["player"])

                                except Unauthorized:            # Se algum erro é encontrado, o player será removido da floresta e seus comandos resetados.
                                    self.to_remove['remove'].append(code)
                                    self.server.messageman.waiting_from[code] = {}
                                    del self.server.messageman.waiting_from[code]
            except Exception:
                traceback.print_exc()


        for code in self.to_remove['exit']:
            self.exit_woods(code)
        for code in self.to_remove["remove"]:
            self.remove_from_woods(code)
        self.timestamp = self.timestamp0        # Marca o tempo atual.
        self.to_remove["exit"] = []                     # Reseta a lista de jogadores a serem removidos.
        self.to_remove['remove'] = []

        # print(f"woods time {time.time() - t0}s")
        self.server.is_processing_woods = False
