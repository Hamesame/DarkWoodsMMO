######################################################################################
#  Arquivo principal contendo a classe RPG, que gerencia o jogo em si, o loop e etc  #
#  Main File with the RPG class. It manages the entire game itself, the loop, etc    #
######################################################################################

import traceback  # gerenciar erros
import time  # consegue fazer operaçoes que dependem do tempo, por exemplo, deixar o programa inativo ou fazer esperar por x de tempo
# import random as rd  # gera numeros aleatórios
# from emoji import emojize  #le/escreve emojis
# from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

import tracemalloc      # Rastreia o uso de memória


# Importa as classes
import os
import sys
import bot  # manda e recebe mensagens do telegram
import helper  # cinto de utilidades
import player  # classes de jogador
import forest  # classe da F L O R E S T A
import arena2 as arena
import travelman
import messageman  # gerenciador de mensagens
import keyboards  # menus/teclados
import playersdb  # DB dos jogadores
import beastsdb  # DB das bestas
import itemsdb  # DB dos itens
import items
import dungeonDB  # DB das dungeons
import dungeon_processing  # processamento das dungeons
import blacksmith  # processamento do bs
import WB
import WB_mountain
import black_list
import threading
import copy
from emoji import emojize
import party
import datetime
import testers
import deep_forest
# import caverns
import megabeast
import potions
import connector
import shopdb
import old_player
import patrons
# import dream_controller

class RPG:
    def __init__(self, rate_mult = 1):
        '''
            Função que inicializa o jogo.

            Parâmetros:

            rate_mult (int): Multiplicador da taxa de encontro da floresta. Ou é 1 (bot normal) ou é 1000 (teste). É o parâmetro usado pra rodar o jogo.
        '''
        print("Initializing...")
        tracemalloc.start()
        self.add_new_att = False           # Função que vai falar se precisa atualizar todos o jogadores (atualização)
        self.bot = bot.TGBot()
        is_test = self.bot.token == "1a2B3C4D5e6F7g8H..."   # add bot token
        if is_test:
            print("is test")
            self.hc_admins = testers.testers()
        else:
            print("is not test")
            self.hc_admins = [
                # Add chat id for super admins like:
                "123456789"
            ]


        self.helper = helper.Helper(self)
        self.keyboards = keyboards.Keyboards()
        self.defkb = self.keyboards.class_main_menu_reply_markup
        self.defkb2 = self.keyboards.at_camp_main_menu_reply_markup
        self.messageman = messageman.MessageMan(self)
        self.shop = shopdb.ShopDB(self)
        self.old_players = old_player.OldPlayerdb(self)
        self.messages = {}
        self.actives_files= "dbs/actives.dat"
        self.actives_backup = "dbs/actives.dat.old"
        loaded = self.helper.load_pickle(self.actives_files)
        self.active_players = {}

        if loaded:
            self.active_players = loaded

        else:
            loaded = self.helper.load_pickle(self.actives_backup)
        self.somewhat_active = {}
        self.somewhat_files = "dbs/somewhat.dat"
        self.somewhat_backup = "dbs/somewhat.dat.old"
        loaded = self.helper.load_pickle(self.somewhat_files)

        if loaded:
            self.somewhat_active = loaded

        else:
            loaded = self.helper.load_pickle(self.somewhat_backup)

        self.rankings = {

            emojize(":bust_in_silhouette: :crossed_swords:️ Player Arena Rankings :crossed_swords:️ :bust_in_silhouette:"): [],
            emojize(":bust_in_silhouette: Global Rankings for Players :bust_in_silhouette:"): [],
            emojize(":busts_in_silhouette: Global Rankings for Parties :busts_in_silhouette:"): [],
            emojize(":incoming_envelope: Invitation Number Rankings :incoming_envelope:"): [],
            emojize(":evergreen_tree: Lasted longer in the deep forest :evergreen_tree:"): [],
        }



        self.enc_rate_mult = rate_mult

        print("Loading databases...")
        self.playersdb = playersdb.PlayersDB(self)
        # for chat,pl in self.playersdb.players_and_parties.items():
        #     for item in range(len(pl.inventory)):
        #         if pl.inventory[item] == None:
        #             del self.playersdb.players_and_parties[chat].inventory[item]
        #             break
        #     if not chat.startswith("/"):
        #         if pl.pt_code:
        #             if not pl.pt_code in self.playersdb.players_and_parties:
        #                 pl.pt_code = ""
        #                 pl.pt_name = ""
        #                 text = "You might have died while the game was very buggy. The consequence of that is that your game stopped working. We are sorry. I think now it should be fixed and you will be able to play the game once again."
        #                 self.bot.send_message(text=text, chat_id=chat)
        index = 0

        # if self.add_new_att:
        #     print("Capping the weapons name length...")
        #
        #     for chat,jog in self.playersdb.players_and_parties.items():
        #         self.playersdb.players_and_parties[chat].pokedex = []
        #
        #         for arma in jog.inventory:
        #             if len(arma.name) > 20:
        #                 arma.name = arma.name[:20]
        #             if len(arma.code) > 20:
        #                 arma.code = arma.code[:20]
        #
        # current, peak = tracemalloc.get_traced_memory()
        # print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        # self.playersdb.save_players()
        # exit()


        # UNCOMMENT THIS TO UPDATE
        # for chat,jog in self.playersdb.players_and_parties.items():
        #     if isinstance(jog, player.Player):
        #         time.sleep(0.1)
        #         current, peak = tracemalloc.get_traced_memory()
        #         print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        #
        #         new_st = player.OrganizedTalismanDB()
        #         for tal in jog.storage:
        #             new_st.append(tal)
        #         jog.storage = new_st
        #
        # self.playersdb.save_players()
        # exit()

        index = 0



        if self.add_new_att:
            new_player_dic = {}
            new_party_dic = {}

            t1 = time.time()
            print("Updating players and parties...")
            for chat,jog in self.playersdb.players_and_parties.items():
                self.playersdb.players_and_parties[chat].pokedex = []
                # t0 = time.time()
                # index += 1
                # print(f"{index}/{len(self.playersdb.players_and_parties)}, time taken: {t0-t1}")
                # time.sleep(0.1)
                # current, peak = tracemalloc.get_traced_memory()
                # print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
                # t1 = time.time()

                if isinstance(jog, player.Player):

                    self.playersdb.players_and_parties[chat].average_times_taken = self.playersdb.players_and_parties[chat].average_times_taken[-5:]
                    # player_example = player.Player("oi")
                    # player_list = [f for f in dir(player_example) if not f.startswith("_")]
                    # knight_example = player.Knight("oi")
                    # knight_list = [f for f in dir(knight_example) if not f.startswith("_")]
                    # druid_example = player.Druid("oi")
                    # druid_list = [f for f in dir(druid_example) if not f.startswith("_")]
                    # explorer_example = player.Explorer("oi")
                    # explorer_list = [f for f in dir(explorer_example) if not f.startswith("_")]
                    # wizard_example = player.Wizard("oi")
                    # wizard_list = [f for f in dir(wizard_example) if not f.startswith("_")]
                    # list = []
                    # example = None
                    example = player.Player(chat)
                    if jog.classe == "Unknown":     # Para cada classe, ele recria toto  jogador segundo os parâmetros do jogador

                        list = [f for f in dir(example) if not f.startswith("_")]   # E também cria a uma lista com cada parâmtro e método da classe nova

                    elif jog.classe == "Knight":

                        example = player.Knight(chat)
                        #example.new()
                        list = [f for f in dir(example) if not f.startswith("_")]
                    elif jog.classe == "Druid":

                        example = player.Druid(chat)
                        #example.new()
                        list = [f for f in dir(example) if not f.startswith("_")]
                    elif jog.classe == "Explorer":

                        example = player.Explorer(chat)
                        #example.new()
                        list = [f for f in dir(example) if not f.startswith("_")]
                    elif jog.classe == "Wizard":

                        example = player.Wizard(chat)
                        #example.new()
                        list = [f for f in dir(example) if not f.startswith("_")]


                    # example.new_from_player(jog)

                    for i in list:      # Aqui ele pega os parâmetros do jogador antigo pra setar os do novo. Se prepara
                        try:
                            coisa = getattr(jog,i)      # Pega o parâmetro i e chama tudo de coisa
                            if not callable(coisa):     # Se coisa não for um método... (pois métodos não receberão os atributos do jogaddor antigo)
                                if i == "actions":      # Se for actions, coisa é um dicionário de métodos que precisa ser atualizado, caso contrário, ele usa os métodos antigos
                                    for code,action in coisa.items():
                                        example.actions[code] = getattr(example,action.__name__)
                                else:
                                    if i != "levels" and i != "is_casting" and i != "lvl_up_text" and i != "status_manager":
                                        setattr(example,i,getattr(jog,i))   # Pega o atributo do jogador tal para adicionar no novo que está sendo criado
                        except AttributeError:  # Caso ele não encontre tal atributo, quer dizer que ele não tem e ele já foi criado, neste caso ele só vai ignorar
                            pass
                    if example.arena_rank == 0:
                        example.arena_rank = 1
                    jog = copy.deepcopy(example)    # O jogador de fato é um clone do exemplo pra n bugar nada

                    arma = jog.weapon
                    if arma:
                        # jog.weapon.is_shared_and_equipped = False       # Disequipa tudo (pra desequipar jogador com ghost)
                        # jog.weapon = None
                        example = items.Weapon(emojize("wooden sword"), False, "wd_s", 3, [1, 1])
                        list = [f for f in dir(example) if not f.startswith("_")]
                        for i in list:
                            try:
                                if not callable(getattr(arma,i)):
                                    setattr(example,i,getattr(arma,i))
                            except AttributeError:
                                pass
                            jog.weapon = copy.deepcopy(example)
                    new_inv = []

                    for arma in jog.inventory:              # Atualiza as armas no inventário do jogador.
                        arma.owner = jog.chat_id
                        if len(arma.name) > 20:
                            arma.name = arma.name[:20]
                        if len(arma.code) > 20:
                            arma.code = arma.code[:20]
                        if isinstance(arma, items.dg_map):
                            example = items.dg_map(emojize("Dusty map :world_map:"), 0, "dstmp", 1)
                            list = [f for f in dir(example) if not f.startswith("_")]
                            for i in list:
                                try:
                                    if not callable(getattr(arma,i)):       # E seta os atributos dela de uma forma similar que é feita nos jogadores
                                        setattr(example,i,getattr(arma,i))
                                except AttributeError:
                                    pass
                        elif isinstance(arma, items.Armor):
                            example = items.Armor(emojize("Simple Clothes"), True, "cloth", 1, {"cold": 1})
                            list = [f for f in dir(example) if not f.startswith("_")]
                            for i in list:
                                try:
                                    if not callable(getattr(arma,i)):       # E seta os atributos dela de uma forma similar que é feita nos jogadores
                                        setattr(example,i,getattr(arma,i))
                                except AttributeError:
                                    pass
                        else:
                            example = items.Weapon(emojize("wooden sword"), False, "wd_s", 3, [1, 1])   # Cria inicialmente uma wooden sword
                            list = [f for f in dir(example) if not f.startswith("_")]
                            for i in list:
                                try:
                                    if not callable(getattr(arma,i)):       # E seta os atributos dela de uma forma similar que é feita nos jogadores
                                        setattr(example,i,getattr(arma,i))
                                except AttributeError:
                                    pass

                        new_inv.append(copy.deepcopy(example))
                    jog.inventory = new_inv                     # Reseta o inventário do jogador
                    jog.calc_attributes()
                    new_player_dic[chat] = copy.deepcopy(jog)          # Vai criando o novo dicionário de jogadores

                elif isinstance(jog, party.Party):
                    dummy_creator = None
                    self.playersdb.players_and_parties[chat].average_times_taken_pt = self.playersdb.players_and_parties[chat].average_times_taken_pt[-5:]
                    if jog.players:
                        dummy_creator = jog.players[0]
                        pt_code = jog.pt_code
                        pt_name = jog.pt_name
                        example = party.Party(dummy_creator, pt_code, pt_name)
                        # for guy in jog.players:
                        #     if not guy is dummy_creator:
                        #         example.join_pt(guy)

                        list = [f for f in dir(example) if not f.startswith("_")]
                        for i in list:      # Aqui ele pega os parâmetros do jogador antigo pra setar os do novo. Se prepara
                            try:
                                coisa = getattr(jog,i)      # Pega o parâmetro i e chama tudo de coisa
                                if not callable(coisa):     # Se coisa não for um método... (pois métodos não receberão os atributos do jogaddor antigo)
                                    if i == "actions":      # Se for actions, coisa é um dicionário de métodos que precisa ser atualizado, caso contrário, ele usa os métodos antigos
                                        for code,action in coisa.items():
                                            example.actions[code] = getattr(example,action.__name__)
                                    else:
                                        if  i != "levels" and i != "status_manager":
                                            setattr(example,i,getattr(jog,i))   # Pega o atributo do jogador tal para adicionar no novo que está sendo criado
                            except AttributeError:  # Caso ele não encontre tal atributo, quer dizer que ele não tem e ele já foi criado, neste caso ele só vai ignorar
                                pass

                        jog = copy.deepcopy(example)

                        new_inv = []
                        for arma in jog.inventory:              # Atualiza as armas no inventário do jogador.
                            if len(arma.name) > 20:
                                arma.name = arma.name[:20]
                            if len(arma.code) > 20:
                                arma.code = arma.code[:20]
                            if isinstance(arma, items.dg_map):
                                example = items.dg_map(emojize("Dusty map :world_map:"), 0, "dstmp", 1)
                                list = [f for f in dir(example) if not f.startswith("_")]
                                for i in list:
                                    try:
                                        if not callable(getattr(arma,i)):       # E seta os atributos dela de uma forma similar que é feita nos jogadores
                                            setattr(example,i,getattr(arma,i))
                                    except AttributeError:
                                        pass
                            elif isinstance(arma, items.Armor):
                                example = items.Armor(emojize("Simple Clothes"), True, "cloth", 1, {"cold": 1})
                                list = [f for f in dir(example) if not f.startswith("_")]
                                for i in list:
                                    try:
                                        if not callable(getattr(arma,i)):       # E seta os atributos dela de uma forma similar que é feita nos jogadores
                                            setattr(example,i,getattr(arma,i))
                                    except AttributeError:
                                        pass
                            else:
                                example = items.Weapon(emojize("wooden sword"), False, "wd_s", 3, [1, 1])   # Cria inicialmente uma wooden sword
                                list = [f for f in dir(example) if not f.startswith("_")]
                                for i in list:
                                    try:
                                        if not callable(getattr(arma,i)):       # E seta os atributos dela de uma forma similar que é feita nos jogadores
                                            setattr(example,i,getattr(arma,i))
                                    except AttributeError:
                                        pass

                            new_inv.append(copy.deepcopy(example))
                            jog.inventory = new_inv

                    new_party_dic[chat] = copy.deepcopy(jog)

            for code in new_party_dic:
                i = 0
                for chat_id in new_party_dic[code].chat_ids:
                    new_party_dic[code].players[i] = new_player_dic[chat_id]
                    i += 1

            self.playersdb.players_and_parties = {**new_player_dic, **new_party_dic}                # Cria o novo dicionário de jogadores e parties




        self.itemsdb = itemsdb.ItemsDB(self)
        if self.add_new_att:
            new_weps = []
            print("Updating Weapons")
            for arma in self.itemsdb.weapons:           # Atualiza as armas em itemsdb
                example = items.Weapon(emojize("wooden sword"), False, "wd_s", 3, [1, 1])
                list = [f for f in dir(example) if not f.startswith("_")]
                for i in list:
                    try:
                        if not callable(getattr(arma,i)):
                            setattr(example,i,getattr(arma,i))
                    except AttributeError:
                        pass
                arma = copy.deepcopy(example)
                new_weps.append(arma)
            self.itemsdb.weapons = new_weps
        # if self.add_new_att:
        #     print("Updating Talismans")
        #     for chat,jog in self.playersdb.players_and_parties.items():
        #         new_sto = []
        #         for tal in jog.storage:
        #             new_tal = copy.copy(tal)
        #             new_tal.code = new_tal.code.replace("\\",'')
        #             new_sto.append(new_tal)
        #         jog.storage = new_sto


        for chat,jog in self.playersdb.players_and_parties.items():
            if isinstance(jog, player.Player):
                jog.generate_stat_points()


        self.travelman = travelman.TravelMan(self)
        self.beastsdb = beastsdb.BeastsDB(self)
        self.dungeonsdb = dungeonDB.dungeonDataBase(self)
        self.dungeon_master = dungeon_processing.DungeonManager(self)
        self.World_boss = WB.WorldBoss(self)
        self.World_boss_mountain = WB_mountain.WorldBoss(self)
        self.blacksmith = blacksmith.Blacksmith(self)
        self.potionsdb = potions.PotionDB(self)
        self.connector = connector.ConnectorMan(self)
        # self.parties_file = "dbs/parties.dat"
        self.levelcap = 40
        self.class_change_lv = 5

        self.save_interval = 3600
        self.timestamp = self.helper.load_pickle("timestamp.dat")
        if not self.timestamp:
            self.timestamp = time.time()

        # for adm_id in self.hc_admins:
        #     if adm_id in self.playersdb.players_and_parties:
        #         self.playersdb.players_and_parties[adm_id].set_adm(10)
        for chat,jog in self.playersdb.players_and_parties.items():
            if not chat.startswith("/"):
                if chat in self.hc_admins:
                    self.playersdb.players_and_parties[chat].set_adm(10)
                else:
                    self.playersdb.players_and_parties[chat].set_adm(0)
        self.shutdown = False
        self.bl_controller = black_list.ban_controller(self)
        self.update_woods = False
        self.forest_tick = 0
        # self.parties_codes = {}
        # loaded = self.helper.load_pickle(self.parties_file)
        # if loaded:
        #     self.parties_codes = loaded
        # if self.add_new_att:                            # Mesma história só que para parties (inventário)
        #     pt_to_del = []
        #     member_to_del = []
        #     for nome,pt in self.parties_codes.items():
        #         if pt:
        #             new_weps = []
        #             for item in pt["pt_inv"]:
        #                 if isinstance(arma, items.dg_map) or item.name[:4] == "Dust":
        #                     example = items.dg_map(emojize("Dusty map :world_map:"), 0, "dstmp", 1)
        #                 else:
        #                     example = items.Weapon(emojize("wooden sword"), False, "wd_s", 3, [1, 1])
        #                 list = [f for f in dir(example) if not f.startswith("_")]
        #                 for i in list:
        #                     try:
        #                         if not callable(getattr(item,i)):
        #                             setattr(example,i,getattr(item,i))
        #                     except AttributeError:
        #                         pass
        #                 item = copy.deepcopy(example)
        #                 if item.owner:
        #                     if not item.owner in pt:
        #                         item.owner = ""
        #                         item.is_shared_and_equipped = False
        #                     else:
        #                         change = True
        #                         for chat,jog in pt.items():
        #                             if isinstance(jog, player.Player):
        #                                 if jog.weapon:
        #                                     if jog.weapon.code == item.code:
        #                                         change = False
        #                         if change:
        #                             item.is_shared_and_equipped = False
        #                 new_weps.append(item)
        #             pt["pt_inv"] = new_weps
        #
        #             for chat,jog in pt.items():
        #                 if isinstance(jog, player.Player):
        #                     # print(self.parties_codes[nome])
        #                     # print(f"chat in playersdb: {chat in self.playersdb.players}")
        #                     # print(f"deu ruim? len = {len(self.parties_codes[nome])}")
        #                     if chat in self.playersdb.players:
        #                         self.parties_codes[nome][chat] = self.playersdb.players[chat]
        #                     else:
        #                         if len(self.parties_codes[nome])<14:
        #                             pt_to_del.append(nome)
        #                         else:
        #                             member_to_del.append((nome, chat))
        #     if pt_to_del:
        #         for code in pt_to_del:
        #             del self.parties_codes[nome]
        #         for tup in member_to_del:
        #             del self.parties_codes[tup[0]][tup[1]]


        self.is_processing_woods = False
        self.woods = forest.Woods(self)
        self.deep_forest_manager = deep_forest.DeepForestManager(self)
        # self.caverns_manager = caverns.Cavernsmanager(self)
        self.megadb = megabeast.MegaBeastMan(self)
        self.arena = arena.Arena(self)
        self.backers = patrons.PatreonDB(self)

        # Halloween event 2023
        self.is_day = True
        self.day_time = [2,3,4,5,10,11,12,13,18,19,20,21]       # Hours that will be considered day
        self.is_midnight = False
        self.midnight_time = [0,8,16]


        # self.dream_controller = dream_controller.Dream(self)

        # for chat,jog in self.playersdb.players_and_parties.items():
        #     if chat[0] == "/":
        #         for jog2 in jog.players:
        #             jog2.storage.extend(jog.storage)
        # for chat,jog in self.playersdb.players_and_parties.items():
        #     if not chat.startswith("/"):
        #         for arma in jog.inventory:
        #             if arma.type == "Weapon":
        #                 arma.update_stats()

        # self.active_players = {}
        print("Done loading!")


    def process_messages(self):
        '''
            Método que processa todas as mensagens na pilha
        '''
        # t0 = time.time()
        self.messageman.update_all_times()
        # print(f"Time to update command times: {time.time() - t0}")
        for chat_id, msgs in self.messages.items():
            time.sleep(0.3)
            is_test = self.bot.token == "12345:1230924bh2jh3gg32KJHKLJH"     # É feito isto pra saber se está rodando ou não o teste, caso sim, ele só deixa passar mensagens de jogadores autorizados.
            can_execute = False
            if is_test and chat_id in self.bot.allowed_test_ids:
                #print("test and autorized")
                can_execute = True
            if not is_test:
                #print("not testing, authorized")
                can_execute =True
            #print(can_execute)
            if can_execute:     # Note que não é necessário checar se o chat_id é código de party, pois self.messages só contém chat_ids.
                if chat_id in self.playersdb.players_and_parties:
                    caller = self.playersdb.players_and_parties[chat_id]
                    message_id = ""
                    msg = msgs["message_list"][-1]
                    if "message_id_list" in msgs:
                        message_id = msgs["message_id_list"][-1]
                    # self.messageman.update_times(chat_id)
                    if caller.pt_code:
                        possible_dg_entries = {emojize("YES :thumbs_up:"):1, emojize("NOPE :thumbs_down:"):2}
                        # O caso abaixo remete ao caso jogador está em uma party numa dungeon ou numa
                        if caller.pt_code in self.playersdb.players_and_parties:
                            if self.playersdb.players_and_parties[caller.pt_code].location == "dungeon" and (msg in possible_dg_entries or (msg in caller.actions and not caller.location == "WB") or (msg[:5] in caller.actions and not caller.location == "WB")):

                                self.messageman.process_message(msg, self.playersdb.players_and_parties[caller.pt_code], message_id, caller_player = caller)

                            elif msg in possible_dg_entries:
                                self.messageman.process_message(msg, self.playersdb.players_and_parties[caller.pt_code], message_id, caller_player = caller)
                            else:
                                # zauarudo boss numa party
                                if caller.location == "WB" and msg[:3] == "/g_":
                                    self.bot.send_message(text = "You are at a battle, where are you trying to go?", chat_id = chat_id)
                                else:
                                    self.messageman.process_message(msg, caller, message_id)
                        else:
                            caller.pt_code = ""
                    else:

                        # zauarudo boss solo
                        if caller.location == "WB" and msg[:3] == "/g_":
                            self.bot.send_message(text = "You are at a battle, where are you trying to go?", chat_id = chat_id)
                        else:
                            # O que sobrou solo
                            self.messageman.process_message(msg, caller, message_id)
                else:
                    # Se ele n ta na lista, cria um jogador novo
                    caller = player.Player(chat_id, "nameless")
                    if chat_id in  self.old_players.players:
                        caller.leaves = self.old_players.players[chat_id]
                    msg = msgs["message_list"][-1]

                    if msg[:6] == "/start":         # Pega o chat id de quem indicou
                        if not chat_id == msg[7:] and not msg[7:].startswith("-"):

                            caller.referal = msg[7:]
                            caller.inventory.append (items.Weapon(emojize("Sharp sword"), False, "ss", 3, [5, 5]))

                    if chat_id in self.hc_admins:
                        caller.set_adm(10)
                    self.playersdb.add_player(caller)
                    self.helper.append_command("new_player", chat_id)

    def save_all(self):
        '''
            Método que salva tudo e printa todos os stats do jogo
        '''
        t0 = time.time()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.bl_controller.save_ban_list()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.playersdb.save_players()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.woods.save_woods()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.messageman.save_comms()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.blacksmith.save_bs()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.dungeon_master.save_dgs()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.itemsdb.save_items()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.beastsdb.save_beasts()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.World_boss.save_status()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.World_boss_mountain.save_status()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.arena.save_arena()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.deep_forest_manager.save_deep_forest()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        # self.caverns_manager.save_caverns()
        # current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.megadb.save_mega()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.shop.save_shop()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.old_players.save_old_players()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.backers.save_patreons()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.save_the_active()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        self.save_the_somewhat()
        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
        # self.save_pts()
        # self.helper.save_pickle(self.timestamp, "timestamp.dat")
        tsave = time.time() - t0
        print("----------")
        print(f"Game saved in {tsave} s.")
        print(f"Total players: {len(self.playersdb.players_and_parties)}")
        group_alts = 0
        parties = 0
        for chat,coisa in self.playersdb.players_and_parties.items():
            if chat.startswith("-"):
                group_alts += 1
            elif chat.startswith("/"):
                parties += 1

        print(f"Number of \"real\" players: {len(self.playersdb.players_and_parties) - group_alts -parties}")
        total = len(self.woods.players)
        print(f"Things in the forest: {total}")
        pl_count = 0
        pl_in_pt_count = 0
        dragged_players = 0
        current_time = time.time()
        for code,woodplayer in self.woods.players.items():
            if isinstance(woodplayer["player"], player.Player):
                pl_count += 1
                self.active_players[code] = current_time
            else:
                for jog in woodplayer["player"].players:
                    pl_in_pt_count += 1
                    if not jog.chat_id in self.active_players:
                        self.somewhat_active[jog.chat_id] = current_time
                        dragged_players += 1
                    # self.active_players[jog.chat_id] = current_time
        to_del = []
        for id,val in self.active_players.items():
            if current_time - val > 172800:         # 2 dias
                to_del.append(id)
        for id,val in self.somewhat_active.items():
            if current_time - val > 172800:         # 2 dias
                to_del.append(id)
        for coisa in to_del:
            if coisa in self.active_players:
                del self.active_players[coisa]
            elif coisa in self.somewhat_active:
                del self.somewhat_active[coisa]


        print(f"Of which, {pl_count} are players and {total - pl_count} parties, in total, {pl_count+pl_in_pt_count} players.")
        print(f"Things in the deep forest: {len(self.deep_forest_manager.jogs)}")
        pl_count = 0
        pl_in_pt_count = 0
        dragged_players = 0
        for code,woodplayer in self.deep_forest_manager.jogs.items():
            if not code[0] == "/":
                pl_count += 1
                self.active_players[code] = current_time
            else:
                for jog in self.playersdb.players_and_parties[code].players:
                    pl_in_pt_count += 1
                    if not jog.chat_id in self.active_players:
                        self.somewhat_active[jog.chat_id] = current_time
                        dragged_players += 1
        total = len(self.deep_forest_manager.jogs)
        print(f"Of which, {pl_count} are players and {total - pl_count} parties, in total, {pl_count+pl_in_pt_count} players.")

        print(f"Active players: {len(self.active_players)+len(self.somewhat_active)}")
        print(f"But, {len(self.somewhat_active)} are being dragged by their parties.")

        active_real = 0
        total_active_power = 0
        average_defense = 0
        for chat,item in self.active_players.items():
            if chat in self.playersdb.players_and_parties:
                total_active_power += self.playersdb.players_and_parties[chat].atk
                average_defense += self.playersdb.players_and_parties[chat].defense/len(self.active_players)
                if not chat.startswith("-"):
                    active_real += 1
        print(f"So, in total, the real active players are {active_real}")
        # print(f"Active \"REAL\" players: {active_real}")
        print(f"Total attack power amongst active players: {total_active_power}")
        print(f"Average defense amonsgt active players: {round(average_defense)}")

        ukclass = 0
        kclass = 0
        dclass = 0
        wclass = 0
        eclass = 0
        for chat_id, jogador in self.playersdb.players_and_parties.items():
            if not isinstance(jogador, party.Party):
                if jogador.classe == "Unknown":
                    ukclass += 1
                if jogador.classe == "Knight":
                    kclass += 1
                if jogador.classe == "Druid":
                    dclass += 1
                if jogador.classe == "Wizard":
                    wclass += 1
                if jogador.classe == "Explorer":
                    eclass += 1
        print(f"Unclassed: {ukclass}")
        print(f"Knights: {kclass}")
        print(f"Druids: {dclass}")
        print(f"Wizards: {wclass}")
        print(f"Explorers: {eclass}")



    def save_pts(self):
        '''
            Método que salva as parties
        '''
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.helper.save_pickle(self.playersdb.players_and_parties, self.parties_file)

    def main_loop(self, interval=0.5):
        '''
            Loop principal que roda no jogo
        '''
        iter = time.time()
        last_now = 0
        while not self.shutdown:
            # self.timestamp = time.time()
            #iter = time.time()
            try:
                # Blacklist
                # print("%%%%%%%%%%%%%%%%%%%")
                # t0 = time.time()
                self.bl_controller.time_tick()
                # print(f"blacklist time {time.time() - t0}s")

                # Processa a floresta
                #
                self.forest_tick += 1
                now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours = -3))).hour
                if now in self.day_time:
                    self.is_day = True
                else:
                    self.is_day = False
                if now in self.midnight_time:
                    self.is_midnight = True
                else:
                    self.is_midnight = False
                # if last_now > now:
                #     for chat,jog in self.playersdb.players_and_parties.items():
                #         if isinstance(jog, player.Player):
                #             jog.arenas_left = jog.max_arenas
                #             text = emojize("Its now midnight in Brazil :Brazil:! This means that you can now acess the arena once more!")
                #             if chat in self.active_players:
                #                 self.bot.send_message(text=text, chat_id=chat)
                last_now = now
                if self.forest_tick == 20:
                    self.update_woods = True
                    self.is_processing_woods = False
                    self.forest_tick = 0
                if self.update_woods and not self.is_processing_woods:
                    self.is_processing_woods = True

                    print(f"processing forests")

                    t = threading.Thread(target = self.woods.process)   # Pra processar as florestas, cria uma thread
                    t.start()
                    # t1 = threading.Thread(target = self.World_boss.process)
                    # t1.start()

                    # t2 = threading.Thread(target = self.arena.process)
                    # t2.start()
                    self.update_woods = False
                    self.forest_tick = 0

                if self.World_boss.std_time + self.World_boss.last_processed < time.time():
                    t1 = threading.Thread(target = self.World_boss.process)
                    t1.start()
                    self.World_boss.last_processed = time.time()
                #

                # Pega e processa mensagens
                # t0 = time.time()
                # print("Starter gathering messages")
                self.messages = self.bot.get_messages_dict(timeout=5) # Coleta as mensagens e as processa
                # print("Read all messages")
                # print(f"gathering messages {time.time() - t0}s")
                # t0 = time.time()

                self.process_messages()
                #dream_messages = self.bot.get_messages_dict_dream(timeout=2)
                #self.dream_controller.process_messages(dream_messages)
                # self.dream_controller.process_dreams()
                # print(f"processing messages {time.time() - t0}s")
                self.connector.read_message()   # Le a mensagem escrita pelo flask app

                if iter + self.save_interval < time.time():
                    self.save_all()
                    iter = time.time()

            except Exception:
                text = traceback.format_exc()
                print(text)
                # self.bot.send_message(text=text, chat_id='576620974')
            time.sleep(interval)

    def shutdown_now(self):
        '''
            Função que desliga tudo
        '''
        print("-----")
        print("Shutting down...")
        self.bot.get_messages_dict(timeout=1)
        self.save_all()
        self.shutdown = True

    def save_the_active(self):
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.helper.save_pickle(self.active_players, self.actives_files)

    def save_the_somewhat(self):
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.helper.save_pickle(self.somewhat_active, self.somewhat_files)

    def dissolve_party(self, pt_code):
        if pt_code in self.deep_forest_manager.jogs:
            if pt_code in self.megadb.players:
                self.megadb.remove_user(pt_code)
            if pt_code in self.deep_forest_manager.jogs:
                self.deep_forest_manager.leave(pt_code)
            else:
                self.woods.add_to_woods(pt_code, 60*60)

        if pt_code in self.woods.players:
            self.woods.exit_woods(pt_code)

        del self.playersdb.players_and_parties[pt_code]

rpg = None
if len(sys.argv) > 1:
    rpg = RPG(int(sys.argv[-1]))
else:
    rpg = RPG()

rpg.main_loop(0)
#
# def check_user(user_id):
#     print(f"checking user {user_id}")
#     return user_id in rpg.playersdb.players_and_parties
#
# def check_signature(signature):
#     return True
