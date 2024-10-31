import os
import time


class ban_controller:
    def __init__(self, server):
        self.ban_dic = {}
        self.server = server
        self.ban_file = "dbs/ban.dat"

        loaded = self.server.helper.load_pickle(self.ban_file)
        if loaded:
            self.ban_dic = loaded

    class BanPlayer:
        def __init__(self):
            self.DAY_DURATION = 86400
            self.ban_level = 1
            self.ban_time = 7  # (in days)
            self.is_banned = True
            self.start_ban = time.time()
            self.end_ban = self.start_ban + (self.ban_time*self.DAY_DURATION)

        def calc_ban_time(self):

            if self.ban_level == 1:
                self.ban_time = 7
            elif self.ban_level == 2:
                self.ban_time = 7*4
            else:
                self.ban_time = 7*4*12
            self.end_ban = self.start_ban + (self.ban_time*self.DAY_DURATION)

    def ban_player(self, chat_id):
        if chat_id not in self.ban_dic:
            new_ban = self.BanPlayer()
            self.ban_dic[chat_id] = new_ban
        else:
            self.ban_dic[chat_id].ban_level += 1
            self.ban_dic[chat_id].start_ban = time.time()
            self.ban_dic[chat_id].calc_ban_time()
            self.ban_dic[chat_id].is_banned = True
        self.save_ban_list()

    def unban_player(self, chat_id):
        self.ban_dic[chat_id].is_banned = False

    def time_tick(self):
        for chat_id, indingente in self.ban_dic.items():
            if indingente.is_banned:
                if time.time() > indingente.end_ban:
                        self.unban_player(chat_id)
                        self.save_ban_list()

    def save_ban_list(self):
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle(self.ban_dic, self.ban_file)
