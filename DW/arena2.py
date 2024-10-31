import player
from emoji import emojize
import random as rd
import os
from math import ceil

class Arena:
    class ArenaPlayer:
        '''
            Classe que vai guardar o jogador com a vida dele.
        '''

        def __init__(self, caller, arena_type):
            hp = 21
            self.debuffs = {}
            self.is_druid = False
            self.classe = caller.classe
            if isinstance(caller, player.Player):
                if caller.classe == "Druid":
                    hp += len(caller.tamed_beasts)+len(caller.tamed_legends)

                    self.is_druid = True
                self.total_health = caller.defense*hp
                self.max_health = self.total_health
                self.chat_id = caller.chat_id
                self.rank = caller.arena_rank
                self.ap = caller.ap
                for limb in caller.hp:
                    self.debuffs[limb.name] = 0
            else:
                self.chat_id = caller.pt_code           # Isso pode dar uma baguncinha depois
                self.rank = 0
            self.bet = None
            self.arena_type = arena_type
            self.is_ready = False
            self.is_ready2 = False
            self.is_hitting = ""
            self.is_defending = ""


    class ArenaBattleMan:
        '''
            Classe que vai juntar 2 coisas batalhando
        '''
        def __init__(self, pl1, pl2):
            self.pl1 = pl1
            self.pl2 = pl2
            self.is_ranked = False
            self.is_party = False
            self.started_battle = False
            self.turn = 0

    def __init__(self, server):
        self.server = server
        self.helper = server.helper

        self.main_lobby = {}
        self.common_arena_lobby = {}
        self.party_arena_lobby = {}
        self.ranked_arena_lobby = {}
        self.ranked_party_arena_lobby = {}
        self.ongoing_battles = {}
        self.arena_players = [self.main_lobby, self.common_arena_lobby, self.ranked_arena_lobby, self.party_arena_lobby, self.ranked_party_arena_lobby, self.ongoing_battles]
        self.arena_file = "dbs/arena.dat"
        self.arena_backup = "dbs/arena.dat.old"
        loaded = self.helper.load_pickle(self.arena_file)
        if loaded:
            self.arena_players = loaded
            self.main_lobby = self.arena_players[0]
            self.common_arena_lobby = self.arena_players[1]
            self.ranked_arena_lobby = self.arena_players[2]
            self.party_arena_lobby = self.arena_players[3]
            self.ranked_party_arena_lobby = self.arena_players[4]
            self.ongoing_battles = self.arena_players[5]

        else:
            loaded = self.helper.load_pickle(self.arena_backup)
            # self.arena_players = loaded
            # self.main_lobby = self.arena_players[0]
            # self.common_arena_lobby = self.arena_players[1]
            # self.ranked_arena_lobby = self.arena_players[2]
            # self.party_arena_lobby = self.arena_players[3]
            # self.ranked_party_arena_lobby = self.arena_players[4]
            # self.ongoing_battles = self.arena_players[5]
        self.def_wait_time = 60*2
        self.max_turns = 10

    def save_arena(self):
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.helper.save_pickle(self.arena_players, self.arena_file)

    def select_least_stat_item(self, inv):
        '''
            Função para pegar o custo de entrada de um jogador.

            A função escolhe o item no inventário com os menores stats.
        '''
        least_stat_item = None
        for item in inv:
            if not least_stat_item:
                least_stat_item = item
            if item.atributos[0]+item.atributos[1] < least_stat_item.atributos[0]+least_stat_item.atributos[1]:
                least_stat_item = item
        return least_stat_item

    def can_enter_ranked(self, inv):
        '''
            Função que vai checar se tem um item com mais de 100 de stats no
            inv que pode servir de aposta.
        '''
        lst = self.select_least_stat_item(inv)
        for item in inv:
            if item.code != lst.code:
                if item.atributos[0] + item.atributos[1] > 99:
                    return True
        return False

    def add_to_arena(self, thing):
        '''
            Função que vai adicionar uma coisa (party ou player)
            ao lobby comum. (Primeiramente ele vai perguntar se realmente quer entrar pagando a taxa)

            Na real ele só adicina ao main lobby

            Ela retorna o tempo de espera para o comando dropar.
        '''
        if isinstance(thing, player.Player):

            if thing.arenas_left != 0:
                # text = emojize(f"You want to join the :crossed_swords: Common arena? The fee is going to be paid automatically with your {least_stat_item.name} {least_stat_item.atributos[0]} :crossed_swords: {least_stat_item.atributos[1]} :shield:")
                text = emojize(f"You want to join the :crossed_swords: Common arena? You have {thing.arenas_left} free arenas left.")
                self.server.bot.send_message(text=text, chat_id=thing.chat_id, reply_markup=self.server.keyboards.bs_reply_markup)
                self.main_lobby[thing.chat_id] = self.ArenaPlayer(thing, "common")
                return self.def_wait_time*2

            else:
                least_stat_item = self.select_least_stat_item(thing.inventory)
                if not least_stat_item:
                    text = "You do not have an item to pay as a fee."
                    self.server.bot.send_message(text=text, chat_id=thing.chat_id, reply_markup = self.server.keyboards.class_main_menu_reply_markup)
                    return False

                else:
                    # text = "You already did all arenas you got for today. Come back tomorrow."
                    # self.server.bot.send_message(text=text, chat_id=thing.chat_id, reply_markup=self.server.keyboards.bs_reply_markup)
                    # return False
                    text = emojize(f"You want to join the :crossed_swords: Common arena? The fee is going to be paid automatically with your {least_stat_item.name} {least_stat_item.atributos[0]} :crossed_swords: {least_stat_item.atributos[1]} :shield:")
                    self.server.bot.send_message(text=text, chat_id=thing.chat_id, reply_markup=self.server.keyboards.bs_reply_markup)
                    self.main_lobby[thing.chat_id] = self.ArenaPlayer(thing, "common")
                    return self.def_wait_time*2


        else:
            least_stat_item = self.select_least_stat_item(thing.inventory)
            if not least_stat_item:
                text = "Your party do not have an item to pay as a fee."
                self.server.bot.send_message(text=text, chat_id=thing.chat_id, reply_markup = self.server.keyboards.class_main_menu_reply_markup)
                return False

            else:
                text = emojize(f"You want your party to join the :crossed_swords: Common arena? The fee is going to be paid automatically with your {least_stat_item.name} {least_stat_item.atributos[0]} :crossed_swords: {least_stat_item.atributos[1]} :shield:")
                self.server.bot.send_message(text=text, chat_id=thing.chat_id, reply_markup=self.server.keyboards.bs_reply_markup)
                self.main_lobby[thing.pt_code] = self.ArenaPlayer(self.server.playersdb.players_and_parties[thing.pt_code], "common")
                return self.def_wait_time*2

    def add_to_ranked_arena(self, thing):
        '''
            Função que vai adicionar uma coisa (party ou player)
            ao lobby ranked.

            Na real, ele adiciona só ao main_lobby
        '''
        if isinstance(thing, player.Player):
            if self.can_enter_ranked(thing.inventory):
                if thing.arenas_left != 0:
                    text = emojize(f"You want to join the :fire: Ranked arena? You have {thing.arenas_left} free arenas left.")
                    self.server.bot.send_message(text = text, chat_id = thing.chat_id, reply_markup = self.server.keyboards.bs_reply_markup)
                    self.main_lobby[thing.chat_id] = self.ArenaPlayer(thing, "ranked")
                    return self.def_wait_time*2

                else:
                    least_stat_item = self.select_least_stat_item(thing.inventory)
                    if len(thing.inventory) < 2:
                        text = "You do not have an item to pay as a fee."
                        self.server.bot.send_message(text=text, chat_id=thing.chat_id, reply_markup = self.server.keyboards.class_main_menu_reply_markup)
                        return False

                    else:
                        text = emojize(f"You want to join the :fire: Ranked arena? The fee is going to be paid automatically with your {least_stat_item.name} {least_stat_item.atributos[0]} :crossed_swords: {least_stat_item.atributos[1]} :shield:")
                        self.server.bot.send_message(text = text, chat_id = thing.chat_id, reply_markup = self.server.keyboards.bs_reply_markup)
                        self.main_lobby[thing.chat_id] = self.ArenaPlayer(thing, "ranked")
                        return self.def_wait_time*2

            # elif thing.arenas_left <= 0:
            #     text = "You already did all arenas you got for today. Come back tomorrow."
            #     self.server.bot.send_message(text=text, chat_id=thing.chat_id, reply_markup=self.server.keyboards.bs_reply_markup)
            #     return False

            else:
                text = emojize("You do not have an item strong enough to take part in the :fire: Ranked Arena :fire:.")
                self.server.bot.send_message(text=text, chat_id=thing.chat_id, reply_markup=self.server.keyboards.class_main_menu_reply_markup)
                return False

        else:
            if self.can_enter_ranked(thing.inventory):
                least_stat_item = self.select_least_stat_item(thing.inventory)
                text = emojize(f"You want your party to join the :fire: Ranked arena? The fee is going to be paid automatically with your {least_stat_item.name} {least_stat_item.atributos[0]} :crossed_swords: {least_stat_item.atributos[1]} :shield:")
                self.server.bot.send_message(text = text, chat_id = thing.chat_id, reply_markup = self.server.keyboards.bs_reply_markup)
                self.main_lobby[thing.pt_code] = self.ArenaPlayer(self.server.playersdb.players_and_parties[thing.pt_code], "ranked")
                return self.def_wait_time*2

            else:
                text = emojize("Your party do not have enough items to take part in the :fire: Ranked Arena :fire:.")
                self.server.bot.send_message(text=text, chat_id=thing.chat_id, reply_markup=self.server.keyboards.class_main_menu_reply_markup)
                return False

    def remove_from_arena(self, thing):
        '''
            Função que vai remover de qualquer arena uma coisa, seja ela um
            jogador ou uma party.
        '''
        if isinstance(thing, player.Player):
            pass
        else:
            pass

    def process(self, caller, text):
        '''
            Função encarregada de processar todas as mensagens genéricas da
            arena. Ele processa:

            - Confimação de entrada na arena comum e na arena ranqueada.
            - Apostas.
            - Texto das batalhas. (As batalhas em sí são em outra função).

            Além disto, ela retorna o tempo de espera para o comando dropar.

        '''
        # print(f"self.main_lobby = {self.main_lobby}")
        # print(f"self.common_arena_lobby = {self.common_arena_lobby}")
        # print(f"self.party_arena_lobby = {self.party_arena_lobby}")
        # print(f"self.ranked_arena_lobby = {self.ranked_arena_lobby}")
        # print(f"self.ranked_party_arena_lobby = {self.ranked_party_arena_lobby}")
        # print(f"self.ongoing_battles = {self.ongoing_battles}")
        # First of all, entrada na arena
        # Vai ver se o jogador está no main lobby e vai jogar pros lobbies das arenas específicas.
        if (caller.pt_code and caller.pt_code in self.main_lobby) or (caller.chat_id in self.main_lobby):
            if text == emojize("YES :thumbs_up:"):
                if caller.pt_code:
                    if self.main_lobby[caller.pt_code].arena_type == "ranked":
                        # least_stat_item = self.select_least_stat_item(self.server.playersdb.players_and_parties[caller.pt_code].inventory)
                        # self.server.playersdb.players_and_parties[caller.pt_code].inventory.remove(least_stat_item)
                        del self.main_lobby[caller.pt_code]
                        self.ranked_arena_lobby[caller.pt_code] = self.ArenaPlayer(self.server.playersdb.players_and_parties[caller.pt_code], "ranked")
                        self.ranked_arena_lobby[caller.pt_code].rank = self.server.playersdb.players_and_parties[caller.pt_code].arena_rank
                        text = "Your party entered the ranked arena. And the fee is going to be paid when the battle ends.. As soon as you find a match, you are going to place bets and start fighting."
                        self.server.bot.send_message(text=text, chat_id=caller.pt_code)
                        self.find_match(self.ranked_party_arena_lobby)
                        return self.def_wait_time*10

                    else:
                        # least_stat_item = self.select_least_stat_item(self.server.playersdb.players_and_parties[caller.pt_code].inventory)
                        # self.server.playersdb.players_and_parties[caller.pt_code].inventory.remove(least_stat_item)
                        del self.main_lobby[caller.pt_code]
                        self.common_arena_lobby[caller.pt_code] = self.ArenaPlayer(self.server.playersdb.players_and_parties[caller.pt_code], "common")
                        self.common_arena_lobby[caller.pt_code].rank = self.server.playersdb.players_and_parties[caller.pt_code].arena_rank
                        text = "Your party entered the common arena. And the fee is going to be paid when the battle ends.. As soon as you find a match you are going to start fighting."
                        self.server.bot.send_message(text=text, chat_id=caller.pt_code)
                        self.find_match(self.party_arena_lobby)
                        return self.def_wait_time*10

                else:
                    caller.location = "arena"
                    if self.main_lobby[caller.chat_id].arena_type == "ranked":
                        # least_stat_item = self.select_least_stat_item(caller.inventory)
                        # caller.inventory.remove(least_stat_item)
                        del self.main_lobby[caller.chat_id]
                        self.ranked_arena_lobby[caller.chat_id] = self.ArenaPlayer(self.server.playersdb.players_and_parties[caller.chat_id], "ranked")
                        text = "You entered the ranked arena. And the fee is going to be paid when the battle ends.. As soon as you find a match, you are going to place bets and start fighting."
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        self.find_match(self.ranked_arena_lobby)
                        return self.def_wait_time*10

                    else:
                        # least_stat_item = self.select_least_stat_item(caller.inventory)
                        # caller.inventory.remove(least_stat_item)
                        del self.main_lobby[caller.chat_id]
                        self.common_arena_lobby[caller.chat_id] = self.ArenaPlayer(self.server.playersdb.players_and_parties[caller.chat_id], "common")
                        text = "You entered the common arena. And the fee is going to be paid when the battle ends.. As soon as you find a match, you are going to place bets and start fighting."
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        self.find_match(self.common_arena_lobby)
                        return self.def_wait_time*10

            elif text == emojize("NOPE :thumbs_down:"):
                if caller.pt_code:
                    text = "Ok. Your party was not ready to enter the arena. Heading back."
                    self.server.bot.send_message(text = text, chat_id = caller.chat_id)
                    del self.main_lobby[caller.pt_code]
                    return False

                else:
                    caller.location = "camp"
                    text = "Ok. You are not ready to enter the arena. Heading back."
                    self.server.bot.send_message(text = text, chat_id = caller.chat_id)
                    del self.main_lobby[caller.chat_id]
                    return False

        # A próxima etapa é conferir se ele ja ta no ongoing_battles pra confirmar a entrada.
        elif (caller.pt_code and self.check_if_code_in_ongoing_battles(caller.pt_code)) or self.check_if_code_in_ongoing_battles(caller.chat_id):
            if caller.pt_code and self.check_if_code_in_ongoing_battles(caller.pt_code):
                arena_man = self.ongoing_battles[self.check_if_code_in_ongoing_battles(caller.pt_code)]
            else:
                code = self.check_if_code_in_ongoing_battles(caller.chat_id)
                arena_man = self.ongoing_battles[code]
            # Entrando neste if, ele vai ver se os jogadores estão prontos
            if (not arena_man.pl1.is_ready) or (not arena_man.pl2.is_ready):
                if text == emojize("YES :thumbs_up:"):
                    if arena_man.is_party:
                        # Precisamos discutir o fucionamento das parties na arena.
                        if arena_man.is_ranked:
                            return self.def_wait_time*2
                        else:
                            return self.def_wait_time*2
                    else:
                        if arena_man.is_ranked:
                            if caller.chat_id == arena_man.pl1.chat_id:
                                arena_man.pl1.is_ready = True
                                if arena_man.pl2.is_ready:
                                    text = "Great! Now place your bets. Choose one item with stats greater than 99. When you are ready, /ready."
                                    text1 = self.bet_text(arena_man, arena_man.pl1)
                                    text2 = self.bet_text(arena_man, arena_man.pl2)
                                    self.server.bot.send_message(text=text+text1, chat_id=arena_man.pl1.chat_id)
                                    self.server.bot.send_message(text=text+text2, chat_id=arena_man.pl2.chat_id)
                                else:
                                    text = "Great! Waiting for the other player to accept the challange."
                                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                            else:
                                arena_man.pl2.is_ready = True
                                if arena_man.pl1.is_ready:
                                    text = "Great! Now place your bets. Choose one item with stats greater than 99. When you are ready, /ready."
                                    text1 = self.bet_text(arena_man, arena_man.pl1)
                                    text2 = self.bet_text(arena_man, arena_man.pl2)
                                    self.server.bot.send_message(text=text+text1, chat_id=arena_man.pl1.chat_id)
                                    self.server.bot.send_message(text=text+text2, chat_id=arena_man.pl2.chat_id)
                                else:
                                    text = "Great! Waiting for the other player to accept the challange."
                                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        else:
                            if caller.chat_id == arena_man.pl1.chat_id:
                                arena_man.pl1.is_ready = True
                                # print(f"Player 1 is the caller. pl1.is_ready:{arena_man.pl1.is_ready}, pl2.is_ready:{arena_man.pl2.is_ready}")
                                if arena_man.pl2.is_ready:
                                    text = emojize("The battle has started! Choose a limb to hit :crossed_swords:.")
                                    keyboard1 = self.server.keyboards.create_keyboard_from_player(self.server.playersdb.players_and_parties[arena_man.pl2.chat_id])
                                    keyboard2 = self.server.keyboards.create_keyboard_from_player(self.server.playersdb.players_and_parties[arena_man.pl1.chat_id])

                                    self.server.bot.send_message(text=text, chat_id=arena_man.pl1.chat_id, reply_markup=keyboard1)
                                    self.server.bot.send_message(text=text, chat_id=arena_man.pl2.chat_id, reply_markup=keyboard2)
                                else:
                                    text = "Great! Waiting for the other player to accept the challange."
                                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                            elif caller.chat_id == arena_man.pl2.chat_id:
                                arena_man.pl2.is_ready = True
                                # print(f"Player 2 is the caller. pl1.is_ready:{arena_man.pl1.is_ready}, pl2.is_ready:{arena_man.pl2.is_ready}")
                                if arena_man.pl1.is_ready:
                                    text = emojize("The battle has started! Choose a limb to hit :crossed_swords:.")
                                    keyboard1 = self.server.keyboards.create_keyboard_from_player(self.server.playersdb.players_and_parties[arena_man.pl2.chat_id])
                                    keyboard2 = self.server.keyboards.create_keyboard_from_player(self.server.playersdb.players_and_parties[arena_man.pl1.chat_id])
                                    self.server.bot.send_message(text=text, chat_id=arena_man.pl1.chat_id, reply_markup=keyboard1)
                                    self.server.bot.send_message(text=text, chat_id=arena_man.pl2.chat_id, reply_markup=keyboard2)
                                else:
                                    text = "Great! Waiting for the other player to accept the challange."
                                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                            else:

                                print("caller is not here")
                    return self.def_wait_time*2

                elif text == emojize("NOPE :thumbs_down:"):
                    if arena_man.is_party:
                        # Precisa discutir como funciona as parties na arena
                        pass
                    else:
                        caller.location = "camp"
                        text = "Oh ok, leaving the arena."
                        self.server.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.at_camp_main_menu_reply_markup)
                        text2 = "Your opponent just gave up before the battle, back at the lobby."
                        if caller.chat_id == arena_man.pl1.chat_id:
                            if arena_man.pl1.arena_type == "ranked":
                                self.server.arena.ranked_arena_lobby[arena_man.pl2.chat_id] = arena_man.pl2
                            else:
                                self.server.arena.common_arena_lobby[arena_man.pl2.chat_id] = arena_man.pl2
                            self.server.bot.send_message(text = text2, chat_id = arena_man.pl2.chat_id)

                        else:
                            if arena_man.pl2.arena_type == "ranked":
                                self.server.arena.ranked_arena_lobby[arena_man.pl1.chat_id] = arena_man.pl1
                            else:
                                self.server.arena.common_arena_lobby[arena_man.pl1.chat_id] = arena_man.pl1
                            self.server.bot.send_message(text = text2, chat_id = arena_man.pl1.chat_id)


                        del self.ongoing_battles[code]       # Não sei se isso vai funcionar
                        return False

            # Neste else, quer dizer que os jogadores já estão prontos e ele processa 2 coisas: as apostas e as batalhas
            else:
                # Primeiramente, apostas.
                if text.startswith("/b_"):
                    if arena_man.pl1.chat_id == caller.chat_id:
                        pl = arena_man.pl1
                    else:
                        pl = arena_man.pl2
                    if arena_man.is_ranked:
                        if caller.pt_code:
                            found = False
                            for coisa in self.server.playersdb.players_and_parties[caller.pt_code].inventory:
                                if f"/b_{coisa.code}" == text:
                                    if coisa.atributos[0]+coisa.atributos[1] > 99:
                                        pl.bet = coisa
                                        found = True
                                        break
                            if not found:
                                text = "Item not found in party inventory"
                                self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                            else:
                                text = "Great! You can change your bet if you want. Choose one item with stats greater than 99. When you are ready, /ready."
                                text1 = self.bet_text(arena_man, pl)
                                self.server.bot.send_message(text=text+text1, chat_id=caller.chat_id)
                        else:
                            found = False
                            for coisa in self.server.playersdb.players_and_parties[caller.chat_id].inventory:
                                if f"/b_{coisa.code}" == text:
                                    if coisa.atributos[0]+coisa.atributos[1] > 99:
                                        pl.bet = coisa
                                        found = True
                                        break
                            if not found:
                                text = "Item not found in inventory"
                                self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                            else:
                                text = "Great! You can change your bet if you want. Choose one item with stats greater than 99. When you are ready, /ready."
                                text1 = self.bet_text(arena_man, pl)
                                self.server.bot.send_message(text=text+text1, chat_id=caller.chat_id)
                    else:
                        text = "wtf?"
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return self.def_wait_time*2
                elif text == "/ready":
                    if arena_man.pl1.chat_id == caller.chat_id:
                        pl = arena_man.pl1
                        opl = arena_man.pl2     # Other player
                    else:
                        pl = arena_man.pl2
                        opl = arena_man.pl1     # Other player
                    if arena_man.is_ranked:
                        if caller.pt_code:
                            pass
                        else:
                            pl.is_ready2 = True
                            if opl.is_ready2:
                                text = emojize("The battle has started! Choose a limb to hit :crossed_swords:.")
                                keyboard1 = self.server.keyboards.create_keyboard_from_player(self.server.playersdb.players_and_parties[arena_man.pl2.chat_id])
                                keyboard2 = self.server.keyboards.create_keyboard_from_player(self.server.playersdb.players_and_parties[arena_man.pl1.chat_id])

                                self.server.bot.send_message(text=text, chat_id=arena_man.pl1.chat_id, reply_markup=keyboard1)
                                self.server.bot.send_message(text=text, chat_id=arena_man.pl2.chat_id, reply_markup=keyboard2)
                            else:
                                text = "Great! You are ready, waiting the opponent to be ready."
                                self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    else:
                        text = "wtf?"
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return self.def_wait_time*2
                # Aqui ele vai processar as batalhas
                else:
                    if not caller.pt_code:
                        if arena_man.pl1.chat_id == caller.chat_id:
                            pl = arena_man.pl1
                            opl = arena_man.pl2     # Other player
                        else:
                            pl = arena_man.pl2
                            opl = arena_man.pl1     # Other player

                        if pl.total_health > 0 and opl.total_health > 0 and arena_man.turn < self.max_turns:
                            # arena_man.turn += 1
                            if text in caller.actions:
                                if not pl.is_hitting:
                                    if pl.ap > 0:
                                        pl.ap -= 1
                                        self.server.playersdb.players_and_parties[caller.chat_id].ap -= 1
                                        pl.is_hitting = text
                                        text = emojize("Great! Now choose a limb to defend :shield:.")
                                        keyboard1 = self.server.keyboards.create_keyboard_from_player(self.server.playersdb.players_and_parties[pl.chat_id])
                                        self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=keyboard1)
                                    else:
                                        text = "Not enough mana"
                                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                                else:
                                    text = "You can only cast spells when deciding what you will attack."
                                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                                return self.def_wait_time*2
                            else:
                                if pl.is_hitting:
                                    if text in pl.debuffs:
                                        pl.is_defending = text
                                        if opl.is_hitting and opl.is_defending:
                                            if pl.debuffs[emojize("head :neutral_face:")] == 3:
                                                pl.is_hitting = "nothing"
                                                pl.is_defending = "nothing"
                                                pl.debuffs[emojize("head :neutral_face:")] = 0
                                            if opl.debuffs[emojize("head :neutral_face:")] == 3:
                                                opl.is_hitting = "nothing"
                                                opl.is_defending = "nothing"
                                                opl.debuffs[emojize("head :neutral_face:")] = 0
                                            self.process_battle(arena_man)
                                            pl.is_hitting = ""
                                            opl.is_hitting = ""
                                            pl.is_defending = ""
                                            opl.is_defending = ""

                                        else:
                                            text = "Good! Now wait your opponent to make its choices."
                                            self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                                    else:
                                        text = f"{text} is not a member you can defend."
                                        self.server.bot.send_message(text=text, chat_id = caller.chat_id)
                                else:
                                    if text in opl.debuffs:
                                        pl.is_hitting = text
                                        text = emojize("Great! Now choose a limb to defend :shield:.")
                                        keyboard1 = self.server.keyboards.create_keyboard_from_player(self.server.playersdb.players_and_parties[pl.chat_id])
                                        self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=keyboard1)
                                    else:
                                        text = f"{text} is not a member you can attack."
                                        self.server.bot.send_message(text=text, chat_id = caller.chat_id)
                                return self.def_wait_time*2

                        else:
                            if caller.arenas_left <= 0:
                                least_stat_item = self.select_least_stat_item(self.server.playersdb.players_and_parties[pl.chat_id].inventory)
                                caller.inventory.remove(least_stat_item)
                            if self.server.playersdb.players_and_parties[opl.chat_id].arenas_left <= 0:
                                least_stat_item = self.select_least_stat_item(self.server.playersdb.players_and_parties[opl.chat_id].inventory)
                                self.server.playersdb.players_and_parties[opl.chat_id].inventory.remove(least_stat_item)

                            if pl.total_health > opl.total_health:
                                winner = pl
                                loser = opl
                            else:
                                winner = opl
                                loser = pl
                            self.server.playersdb.players_and_parties[winner.chat_id].arena_rank = min(self.server.playersdb.players_and_parties[winner.chat_id].arena_rank + 1, 40)
                            self.server.playersdb.players_and_parties[loser.chat_id].arena_rank = max(self.server.playersdb.players_and_parties[loser.chat_id].arena_rank - 1, 1)
                            if arena_man.is_ranked:
                                l_exp_gain = winner.rank*50
                                w_exp_gain = loser.rank*100
                                w_text = emojize(f"You won the fight and also, you won your {loser.bet}. But you got {l_exp_gain} exp (100 times the opponent's rank)! Your arena rank went one up and now you are rank {self.server.playersdb.players_and_parties[winner.chat_id].arena_rank}.")
                                l_text = emojize(f"You lost the fight and also, you lost your {loser.bet}. But you got {w_exp_gain} exp (50 times the opponent's rank)! Your arena rank went down one and now you are rank {self.server.playersdb.players_and_parties[loser.chat_id].arena_rank}.")
                                self.server.bot.send_message(text=w_text, chat_id=winner.chat_id, reply_markup = self.server.keyboards.at_camp_main_menu_reply_markup)
                                self.server.bot.send_message(text=l_text, chat_id=loser.chat_id, reply_markup = self.server.keyboards.at_camp_main_menu_reply_markup)
                                if loser.bet != None:
                                    self.server.playersdb.players_and_parties[winner.chat_id].inventory.append(loser.bet)
                                    i = 0
                                    for thing in self.server.playersdb.players_and_parties[loser.chat_id].inventory:
                                        if thing.code == loser.bet.code:
                                            del self.server.playersdb.players_and_parties[loser.chat_id].inventory[i]
                                            break
                                        i += 1

                                # self.server.playersdb.players_and_parties[loser.chat_id].inventory.remove(loser.bet)
                            else:
                                l_exp_gain = winner.rank*50
                                w_exp_gain = loser.rank*100
                                w_text = emojize(f"You won the fight. And gained {w_exp_gain} exp (100 times the opponent's rank)! Your arena rank went one up and now you are rank {self.server.playersdb.players_and_parties[winner.chat_id].arena_rank}.")
                                l_text = emojize(f"You lost the fight. And gained {l_exp_gain} exp (50 times the opponent's rank)! Your arena rank went down one and now you are rank {self.server.playersdb.players_and_parties[loser.chat_id].arena_rank}.")
                                self.server.bot.send_message(text=w_text, chat_id=winner.chat_id, reply_markup = self.server.keyboards.at_camp_main_menu_reply_markup)
                                self.server.bot.send_message(text=l_text, chat_id=loser.chat_id, reply_markup = self.server.keyboards.at_camp_main_menu_reply_markup)
                            if self.server.playersdb.players_and_parties[pl.chat_id].arenas_left > 0:   # Isso é necessário para não contabilizar as arenas pagas.
                                self.server.playersdb.players_and_parties[pl.chat_id].arenas_left -= 1
                            if self.server.playersdb.players_and_parties[opl.chat_id].arenas_left > 0:
                                self.server.playersdb.players_and_parties[opl.chat_id].arenas_left -= 1
                            self.server.playersdb.players_and_parties[pl.chat_id].location = "camp"
                            self.server.playersdb.players_and_parties[opl.chat_id].location = "camp"
                            self.server.playersdb.players_and_parties[winner.chat_id].exp += w_exp_gain
                            self.server.playersdb.players_and_parties[loser.chat_id].exp += l_exp_gain
                            if self.server.playersdb.players_and_parties[pl.chat_id].classe != "Unknown":
                                self.server.playersdb.players_and_parties[pl.chat_id].ap = self.server.playersdb.players_and_parties[pl.chat_id].max_ap
                            if self.server.playersdb.players_and_parties[opl.chat_id].classe != "Unknown":
                                self.server.playersdb.players_and_parties[opl.chat_id].ap = self.server.playersdb.players_and_parties[opl.chat_id].max_ap
                            del self.ongoing_battles[self.check_if_code_in_ongoing_battles(caller.chat_id)]
                            return False
                    else:
                        pass

        else:
            text = "um? What did you say?"
            self.server.bot.send_message(text=text, chat_id=caller.chat_id)
            return self.def_wait_time


    def check_if_code_in_ongoing_battles(self, code):
        for mixed_code, arena in self.ongoing_battles.items():
            if code in mixed_code:
                return mixed_code
        return False

    def find_match(self, lobby):
        '''
            Função que engole um lobby e tenta fazer matches com ele.
        '''
        done = False
        index = 0
        max_rank_diff = 5
        list = lobby.items()
        for chat1, pl1 in list:
            for chat2, pl2 in list:
                if chat1 != chat2:
                    if abs(pl1.rank - pl2.rank) <= max_rank_diff:
                        new_arena = self.ArenaBattleMan(pl1, pl2)
                        if pl1.chat_id.startswith("/"):
                            new_arena.is_party = True
                        if pl1.arena_type == 'ranked':
                            new_arena.is_ranked = True
                        mixed_id = f"{pl1.chat_id} {pl2.chat_id}"
                        self.ongoing_battles[mixed_id] = new_arena
                        text = "Opponent found! Are you ready to start the battle?"
                        # print(f"messageman waiting_from: {self.server.messageman.waiting_from}")
                        self.server.messageman.waiting_from[pl1.chat_id] = {'comms': [emojize(":crossed_swords: Arena :crossed_swords:")], 'remtimes': [120], 'internals': [False]}
                        self.server.messageman.waiting_from[pl2.chat_id] = {'comms': [emojize(":crossed_swords: Arena :crossed_swords:")], 'remtimes': [120], 'internals': [False]}
                        # print(f"messageman waiting_from: {self.server.messageman.waiting_from}")
                        self.server.bot.send_message(text=text, chat_id=pl1.chat_id, reply_markup=self.server.keyboards.bs_reply_markup)
                        self.server.bot.send_message(text=text, chat_id=pl2.chat_id, reply_markup=self.server.keyboards.bs_reply_markup)
                        del lobby[pl1.chat_id]
                        del lobby[pl2.chat_id]
                        return



    def bet_text(self, arena_battle, arena_player):
        '''
            Função que vai criar o texto para colocar apostas.
        '''
        if arena_battle.pl1.chat_id == arena_player.chat_id:
            other = arena_battle.pl2
        else:
            other = arena_battle.pl1
        other_name = self.server.playersdb.players_and_parties[other.chat_id].name
        text = emojize( f"Your rank: {arena_player.rank}\n"
                        f"Opponent's rank: {other.rank}\n"
                        f"Your bet: {arena_player.bet}\n"
                        f"{other_name} bet: {other.bet}\n\n"
                        f"To place a bet just enter a /b_(code) below.\n\n")
        jog = self.server.playersdb.players_and_parties[arena_player.chat_id]
        for coisa in jog.inventory:
            if coisa.atributos[0]+coisa.atributos[1] > 99:
                text += emojize(f"{coisa.name}, stats: {coisa.atributos[0]+coisa.atributos[1]} /b_{coisa.code}\n")
        return text

    def process_battle(self, manager):
        manager.turn += 1
        pl1_crit = 0.05 + self.server.playersdb.players_and_parties[manager.pl1.chat_id].crit_boost
        if rd.random() < pl1_crit:
            pl1_crit = True
        else:
            pl1_crit = False
        pl2_crit = 0.05 + self.server.playersdb.players_and_parties[manager.pl2.chat_id].crit_boost
        if rd.random() < pl2_crit:
            pl2_crit = True
        else:
            pl2_crit = False
        pl1_dam_penalty_left = 0.1*(manager.pl1.debuffs[emojize("left arm :flexed_biceps:")])
        pl1_dam_penalty_right = 0.1*(manager.pl1.debuffs[emojize("right arm :flexed_biceps:")])
        pl1_dam_penalty = pl1_dam_penalty_left + pl1_dam_penalty_right
        pl1_dam = 4*self.server.playersdb.players_and_parties[manager.pl1.chat_id].atk*(1 - pl1_dam_penalty)*(1+pl1_crit)
        pl2_dam_penalty_left = 0.1*(manager.pl2.debuffs[emojize("left arm :flexed_biceps:")])
        pl2_dam_penalty_right = 0.1*(manager.pl2.debuffs[emojize("right arm :flexed_biceps:")])
        pl2_dam_penalty = pl2_dam_penalty_left + pl2_dam_penalty_right
        pl2_dam = 4*self.server.playersdb.players_and_parties[manager.pl2.chat_id].atk*(1 - pl2_dam_penalty)*(1+pl2_crit)
        pl1_defense = self.server.playersdb.players_and_parties[manager.pl1.chat_id].defense
        pl2_defense = self.server.playersdb.players_and_parties[manager.pl2.chat_id].defense
        pl1_text = f"Turn: {manager.turn}/{self.max_turns}\n\n"
        pl2_text = f"Turn: {manager.turn}/{self.max_turns}\n\n"
        pl1_evade_penalty_left = 0.04*(manager.pl1.debuffs[emojize("left leg")])
        pl1_evade_penalty_right = 0.04*(manager.pl1.debuffs[emojize("right leg")])
        pl1_evade_penalty = pl1_evade_penalty_right + pl1_evade_penalty_left
        pl1_evade_prob = 0.25 - pl1_evade_penalty
        pl2_evade_penalty_left = 0.04*(manager.pl2.debuffs[emojize("left leg")])
        pl2_evade_penalty_right = 0.04*(manager.pl2.debuffs[emojize("right leg")])
        pl2_evade_penalty = pl2_evade_penalty_right + pl2_evade_penalty_left
        pl2_evade_prob = 0.25 - pl2_evade_penalty

        pl1_text += f"Opponent: {self.server.playersdb.players_and_parties[manager.pl2.chat_id]}\n\n"
        pl2_text += f"Opponent: {self.server.playersdb.players_and_parties[manager.pl1.chat_id]}\n\n"

        if manager.pl1.is_hitting != manager.pl2.is_defending:
            if manager.pl1.is_hitting not in manager.pl2.debuffs:
                spell = manager.pl1.is_hitting
                if spell == "nothing":
                    pl1_text += "You passed out. You tried but you could not attack, use spells or defend this turn.\n"
                    pl2_text += "The opponent passed out\n"
                else:
                    if manager.pl1.classe == "Knight":
                        if spell == "/heal_self":
                            heal_amount = min(pl1_defense*4, manager.pl1.max_health - manager.pl1.total_health)
                            pl1_text += f"You healed yourself by {heal_amount}.\n"
                            if self.server.playersdb.players_and_parties[manager.pl1.chat_id].gender == "female":
                                aux = "her"
                            else:
                                aux = "him"
                            pl2_text += f"Your opponent healed {aux}self by {heal_amount}.\n"
                            manager.pl1.total_health += heal_amount
                    elif manager.pl1.classe == "Druid" or manager.pl1.classe == "Explorer":
                        if spell == "/heal":
                            heal_amount = min(3*pl1_defense*4, manager.pl1.max_health - manager.pl1.total_health)
                            pl1_text += f"You healed yourself by {heal_amount}.\n"
                            if self.server.playersdb.players_and_parties[manager.pl1.chat_id].gender == "female":
                                aux = "her"
                            else:
                                aux = "him"
                            pl2_text += f"Your opponent healed {aux}self by {heal_amount}.\n"
                            manager.pl1.total_health += heal_amount

                    else:
                        if spell == "/heal":
                            heal_amount = min((self.server.playersdb.players_and_parties[manager.pl1.chat_id].buff_man.buff_state + 1)*pl1_defense*4, manager.pl1.max_health - manager.pl1.total_health)
                            pl1_text += f"You healed yourself by {heal_amount}.\n"
                            if self.server.playersdb.players_and_parties[manager.pl1.chat_id].gender == "female":
                                aux = "her"
                            else:
                                aux = "him"
                            pl2_text += f"Your opponent healed {aux}self by {heal_amount}.\n"
                            manager.pl1.total_health += heal_amount
                        else:
                            at = self.server.playersdb.players_and_parties[manager.pl1.chat_id]
                            if at.is_synergyzed:
                                damage = round(at.atk*(1+0.5*at.spell_power)*3*4)
                            else:
                                damage = round(at.atk*(1+0.5*at.spell_power)*4)
                            pl1_text += f"You cast a fireball dealing {round(damage)}.\n"
                            pl2_text += f"The opponent cast a fireball dealing {round(damage)}.\n"
                            manager.pl2.total_health -= damage
            elif rd.random() > pl2_evade_prob:
                if pl1_crit:
                    pl1_text += emojize("You dealt Double damage! :high_voltage:️ (critical)\n")
                if pl2_crit:
                    pl1_text += emojize("You took Double damage! :high_voltage:️ (critical)\n")
                manager.pl2.total_health -= pl1_dam
                manager.pl2.debuffs[manager.pl1.is_hitting] = min(manager.pl2.debuffs[manager.pl1.is_hitting] + ceil(pl1_dam/(4*pl2_defense)),3)
                pl1_text += f"You hit the opponent's {manager.pl1.is_hitting} dealing {round(pl1_dam)}.\n"
                pl2_text += f"You have been it in the {manager.pl1.is_hitting} taking {round(pl1_dam)}.\n"
            else:
                pl2_text += "You dodged the attack.\n"
                pl1_text += "The opponent dodged your attack.\n"
        else:
            pl2_text += "Successfully defended!\n"
            pl1_text += "The opponent defended!\n"
        if manager.pl2.is_hitting != manager.pl1.is_defending:
            if manager.pl2.is_hitting not in manager.pl1.debuffs:
                spell = manager.pl2.is_hitting
                if spell == "nothing":
                    pl2_text += "You passed out. You tried but you could not attack, use spells or defend this turn.\n"
                    pl1_text += "The opponent passed out\n"
                else:
                    if manager.pl2.classe == "Knight":
                        if spell == "/heal_self":
                            heal_amount = min(pl2_defense*4, manager.pl2.max_health - manager.pl2.total_health)
                            pl2_text += f"You healed yourself by {heal_amount}.\n"
                            if self.server.playersdb.players_and_parties[manager.pl2.chat_id].gender == "female":
                                aux = "her"
                            else:
                                aux = "him"
                            pl1_text += f"Your opponent healed {aux}self by {heal_amount}.\n"
                            manager.pl2.total_health += heal_amount
                    elif manager.pl2.classe == "Druid" or manager.pl2.classe == "Explorer":
                        if spell == "/heal":
                            heal_amount = min(3*pl2_defense*4, manager.pl2.max_health - manager.pl2.total_health)
                            pl2_text += f"You healed yourself by {heal_amount}.\n"
                            if self.server.playersdb.players_and_parties[manager.pl2.chat_id].gender == "female":
                                aux = "her"
                            else:
                                aux = "him"
                            pl1_text += f"Your opponent healed {aux}self by {heal_amount}.\n"
                            manager.pl2.total_health += heal_amount

                    else:
                        if spell == "/heal":
                            heal_amount = min((self.server.playersdb.players_and_parties[manager.pl2.chat_id].buff_man.buff_state + 1)*pl2_defense*4, manager.pl2.max_health - manager.pl2.total_health)
                            pl2_text += f"You healed yourself by {heal_amount}.\n"
                            if self.server.playersdb.players_and_parties[manager.pl2.chat_id].gender == "female":
                                aux = "her"
                            else:
                                aux = "him"
                            pl1_text += f"Your opponent healed {aux}self by {heal_amount}.\n"
                            manager.pl2.total_health += heal_amount
                        else:
                            at = self.server.playersdb.players_and_parties[manager.pl2.chat_id]
                            if at.is_synergyzed:
                                damage = round(at.atk*(1+0.5*at.spell_power)*3*4)
                            else:
                                damage = round(at.atk*(1+0.5*at.spell_power)*4)
                            pl2_text += f"You cast a fireball dealing {round(damage)}.\n"
                            pl1_text += f"The opponent cast a fireball dealing {round(damage)}.\n"
                            manager.pl1.total_health -= damage
            elif rd.random() > pl1_evade_prob:
                if pl1_crit:
                    pl2_text += emojize("You took Double damage! :high_voltage:️ (critical)\n")
                if pl2_crit:
                    pl2_text += emojize("You dealt Double damage! :high_voltage:️ (critical)\n")
                manager.pl1.total_health -= pl2_dam
                manager.pl1.debuffs[manager.pl2.is_hitting] = min(manager.pl1.debuffs[manager.pl2.is_hitting] + ceil(pl2_dam/(pl1_defense*4)),3)
                pl2_text += f"You hit the opponent's {manager.pl2.is_hitting} dealing {round(pl2_dam)}.\n"
                pl1_text += f"You have been it in the {manager.pl2.is_hitting} taking {round(pl2_dam)}.\n"
            else:
                pl1_text += "You dodged the attack.\n"
                pl2_text += "The opponent dodged your attack.\n"
        else:
            pl1_text += "Successfully defended!\n"
            pl2_text += "The opponent defended!\n"

        pl1_text += emojize(    f"Total health: {round(manager.pl1.total_health)} :red_heart:\n"
                                f"Opponent's health: {round(manager.pl2.total_health)} :red_heart:\n")

        pl2_text += emojize(    f"Total health: {round(manager.pl2.total_health)} :red_heart:\n"
                                f"Opponent's health: {round(manager.pl1.total_health)} :red_heart:\n")

        pl1_dam_penalty_left = ( 0.1*(manager.pl1.debuffs[emojize("left arm :flexed_biceps:")]))
        pl1_dam_penalty_right = ( 0.1*(manager.pl1.debuffs[emojize("right arm :flexed_biceps:")]))
        pl2_dam_penalty_left = ( 0.1*(manager.pl2.debuffs[emojize("left arm :flexed_biceps:")]))
        pl2_dam_penalty_right = ( 0.1*(manager.pl2.debuffs[emojize("right arm :flexed_biceps:")]))

        pl1_evade_penalty_left = ( 0.05*(manager.pl1.debuffs[emojize("left leg")]))
        pl1_evade_penalty_right = ( 0.05*(manager.pl1.debuffs[emojize("right leg")]))
        pl2_evade_penalty_left = ( 0.05*(manager.pl2.debuffs[emojize("left leg")]))
        pl2_evade_penalty_right = ( 0.05*(manager.pl2.debuffs[emojize("right leg")]))

        pl1_dbuff_dic = {       emojize("head :neutral_face:"):["You feel dizzy", "Your vision is blackening", "You fainted (lost a turn)"],
                                emojize("right leg"):[f"Your attack evasions are {round(pl1_evade_penalty_right*100)}% worse",f"Your attack evasions are {round(pl1_evade_penalty_right*100)}% worse",f"Your attack evasions are {round(pl1_evade_penalty_right*100)}% worse"],
                                emojize("left leg"):[f"Your attack evasions are {round(pl1_evade_penalty_left*100)}% worse",f"Your attack evasions are {round(pl1_evade_penalty_left*100)}% worse",f"Your attack evasions are {round(pl1_evade_penalty_left*100)}% worse"],
                                emojize("left arm :flexed_biceps:"):[f"Your attack power is reduced by {round(pl1_dam_penalty_left*100)}%",f"Your attack power is reduced by {round(pl1_dam_penalty_left*100)}%",f"Your attack power is reduced by {round(pl1_dam_penalty_left*100)}%",],
                                emojize("right arm :flexed_biceps:"):[f"Your attack power is reduced by {round(pl1_dam_penalty_right*100)}%",f"Your attack power is reduced by {round(pl1_dam_penalty_right*100)}%",f"Your attack power is reduced by {round(pl1_dam_penalty_right*100)}%",],
                                "chest": ["nothing","nothing","nothing"],
                                "belly": ["nothing","nothing","nothing"]

                                }
        if manager.pl1.is_druid:
            for besta in self.server.playersdb.players_and_parties[manager.pl1.chat_id].tamed_beasts:
                pl1_dbuff_dic[besta.tipo] = ["Your beast might seem injured but its damaged is dictated by the health of your arms.", "Your beast might seem injured but its damaged is dictated by the health of your arms.", "Your beast might seem injured but its damaged is dictated by the health of your arms."]
            for besta in self.server.playersdb.players_and_parties[manager.pl1.chat_id].tamed_legends:
                pl1_dbuff_dic[besta.tipo] = ["Your beast might seem injured but its damaged is dictated by the health of your arms.", "Your beast might seem injured but its damaged is dictated by the health of your arms.", "Your beast might seem injured but its damaged is dictated by the health of your arms."]
            for besta in self.server.playersdb.players_and_parties[manager.pl1.chat_id].tamed_megabeasts:
                for limb in besta.original_limb:
                    nome = f"{besta.name}'s {limb}"
                    pl1_dbuff_dic[nome] = ["Your beast might seem injured but its damaged is dictated by the health of your arms.", "Your beast might seem injured but its damaged is dictated by the health of your arms.", "Your beast might seem injured but its damaged is dictated by the health of your arms."]


        pl2_dbuff_dic = {       emojize("head :neutral_face:"):["You feel dizzy", "Your vision is blackening", "You fainted (lost a turn)"],
                                emojize("right leg"):[f"Your attack evasions are {round(pl2_evade_penalty_right*100)}% worse",f"Your attack evasions are {round(pl2_evade_penalty_right*100)}% worse",f"Your attack evasions are {round(pl2_evade_penalty_right*100)}% worse"],
                                emojize("left leg"):[f"Your attack evasions are {round(pl2_evade_penalty_left*100)}% worse",f"Your attack evasions are {round(pl2_evade_penalty_left*100)}% worse",f"Your attack evasions are {round(pl2_evade_penalty_left*100)}% worse"],
                                emojize("left arm :flexed_biceps:"):[f"Your attack power is reduced by {round(pl2_dam_penalty_left*100)}%",f"Your attack power is reduced by {round(pl2_dam_penalty_left*100)}%",f"Your attack power is reduced by {round(pl2_dam_penalty_left*100)}%",],
                                emojize("right arm :flexed_biceps:"):[f"Your attack power is reduced by {round(pl2_dam_penalty_right*100)}%",f"Your attack power is reduced by {round(pl2_dam_penalty_right*100)}%",f"Your attack power is reduced by {round(pl2_dam_penalty_right*100)}%",],
                                "chest": ["nothing","nothing","nothing"],
                                "belly": ["nothing","nothing","nothing"]

                                }
        if manager.pl2.is_druid:
            for besta in self.server.playersdb.players_and_parties[manager.pl2.chat_id].tamed_beasts:
                pl2_dbuff_dic[besta.tipo] = ["Your beast might seem injured but its damaged is dictated by the health of your arms.", "Your beast might seem injured but its damaged is dictated by the health of your arms.", "Your beast might seem injured but its damaged is dictated by the health of your arms."]
            for besta in self.server.playersdb.players_and_parties[manager.pl2.chat_id].tamed_legends:
                pl2_dbuff_dic[besta.tipo] = ["Your beast might seem injured but its damaged is dictated by the health of your arms.", "Your beast might seem injured but its damaged is dictated by the health of your arms.", "Your beast might seem injured but its damaged is dictated by the health of your arms."]
            for besta in self.server.playersdb.players_and_parties[manager.pl2.chat_id].tamed_megabeasts:
                pl2_dbuff_dic[besta.name] = ["Your beast might seem injured but its damaged is dictated by the health of your arms.", "Your beast might seem injured but its damaged is dictated by the health of your arms.", "Your beast might seem injured but its damaged is dictated by the health of your arms."]


        damage_list = ["Bruised","In bad shape", "Destroyed"]
        pl1_text += "\nDebuffs inflicted on yourself:\n"
        pl2_text += "\nDebuffs inflicted on your opponent:\n"

        if self.server.playersdb.players_and_parties[manager.pl1.chat_id].gender == "female":
            aux = "Her"
        else:
            aux = "His"
        for dbuff, value in manager.pl1.debuffs.items():
            if value > 0:
                pl1_text += emojize(f"Your {dbuff} is {damage_list[value-1]}: {pl1_dbuff_dic[dbuff][value-1]}\n")
                pl2_text += emojize(f"{aux} {dbuff} is {damage_list[value-1]}: {pl1_dbuff_dic[dbuff][value-1]}\n")
        pl2_text += "\nDebuffs inflicted on yourself:\n"
        pl1_text += "\nDebuffs inflicted on your opponent:\n"

        if self.server.playersdb.players_and_parties[manager.pl2.chat_id].gender == "female":
            aux = "Her"
        else:
            aux = "His"
        for dbuff, value in manager.pl2.debuffs.items():
            if value > 0:
                pl2_text += emojize(f"Your {dbuff} is {damage_list[value-1]}: {pl2_dbuff_dic[dbuff][value-1]}\n")
                pl1_text += emojize(f"{aux} {dbuff} is {damage_list[value-1]}: {pl2_dbuff_dic[dbuff][value-1]}\n")
        pl1_text += "\n\n What is going to be your next move?\n\n"
        pl1_text += self.server.playersdb.players_and_parties[manager.pl1.chat_id].dg_coms()
        pl2_text += "\n\n What is going to be your next move?\n\n"
        pl2_text += self.server.playersdb.players_and_parties[manager.pl2.chat_id].dg_coms()
        keyboard1 = self.server.keyboards.create_keyboard_from_player(self.server.playersdb.players_and_parties[manager.pl2.chat_id])
        keyboard2 = self.server.keyboards.create_keyboard_from_player(self.server.playersdb.players_and_parties[manager.pl1.chat_id])
        self.server.bot.send_message(text=pl1_text, chat_id=manager.pl1.chat_id, reply_markup=keyboard1)
        self.server.bot.send_message(text=pl2_text, chat_id=manager.pl2.chat_id, reply_markup=keyboard2)


    # def remove_a_debuff(self, debuffs, power):
    #     pass
