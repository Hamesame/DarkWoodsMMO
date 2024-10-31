import os


class OldPlayerdb:
    def __init__(self, server):
        self.players = {}
        self.server = server

        self.old_player_file = "dbs/old_players.dat"
        #self.checker = Player_retification.checker_and_retificator()

        loaded = self.server.helper.load_pickle(self.old_player_file)
        if loaded:
            self.players = loaded
    def add_player(self, chat_id, leaves):
        self.players[chat_id] = leaves

    def save_old_players(self):
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle(self.players, self.old_player_file)
