#############################
# Classe que gerencia o BS  #
#############################

import os


class Blacksmith:
    def __init__(self, server):
        self.server = server
        self.bs_file = "dbs/bs.dat"
        self.bs_in_progress = {}
        loaded = self.server.helper.load_pickle(self.bs_file)
        if loaded:
            self.bs_in_progress = loaded

    def clear_blacksmith(self, chat_id):
        text = f"After {5+self.server.playersdb.players_and_parties[chat_id].suc_refs} minutes of *AWKWARD* starring, the trader ran away."
        self.server.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.server.defkb, parse_mode="MARKDOWN")
        if chat_id in self.server.woods.players:
            self.server.woods.players[chat_id]["active"] = True
            self.server.playersdb.players_and_parties[chat_id].location = "forest"
        if chat_id in self.server.deep_forest_manager.jogs:
            self.server.deep_forest_manager.jogs[chat_id].active = True
            self.server.playersdb.players_and_parties[chat_id].location = "deep_forest"
        if chat_id in self.server.blacksmith.bs_in_progress:
            if "bs_inv" in self.server.blacksmith.bs_in_progress[chat_id]:
                self.server.playersdb.players_and_parties[chat_id].inventory.extend(self.server.blacksmith.bs_in_progress[chat_id]["bs_inv"])
            del self.server.blacksmith.bs_in_progress[chat_id]

    def save_bs(self):
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle(self.bs_in_progress, self.bs_file)
