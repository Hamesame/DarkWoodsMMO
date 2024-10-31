#################################################
#  Classe para segurar toda a DB dos jogadores  #
#################################################

import os
import random as rd
#import Player_retification

class PlayersDB:
    def __init__(self, server):
        self.server = server
        self.players_and_parties = {}
        self.players_file = "dbs/players_and_parties.dat"
        #self.checker = Player_retification.checker_and_retificator()

        loaded = self.server.helper.load_pickle(self.players_file)
        if loaded:
            # for code in loaded:
            #     if code[0] == "/":
            #         for chat_id in loaded[code].chat_ids:
            #             for guy in loaded[code].players:
            #                 if guy.chat_id == chat_id:
            #                     guy = loaded[chat_id]
                                # i = loaded[code].players.index(guy)
                                # loaded[code].players[i] = loaded[chat_id]
            self.players_and_parties = loaded

        
        #self.checker.walk_in_the_players_dictionary_and_retificate(self.players)



    def get_player(self, chat_id):
        player = None
        if chat_id in self.players_and_parties:
            player = self.players_and_parties[chat_id]
        return player

    def get_random_player(self):
        chat_id = rd.choices(list(self.players_and_parties.keys()))[0]
        return self.players_and_parties[chat_id]

    def add_player(self, player):
        if player.chat_id not in self.players_and_parties:
            self.players_and_parties[player.chat_id] = player
            self.save_players()

    def remove_player(self, chat_id):
        if chat_id in self.players_and_parties:
            del self.players_and_parties[chat_id]
            self.save_players()

    def save_players(self):
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle(self.players_and_parties, self.players_file)
