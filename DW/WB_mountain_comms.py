import bot
import player
from emoji import emojize
import random as rd
import helper
import time


class WBMountainComms:
    '''
        Classe que controla os comandos do WB. (sunflower neste caso)
    '''
    def __init__(self, server):
        self.server = server
        self.defkb = server.defkb
        self.def_wait_time = 60
        self.helper = helper.Helper(server)
        self.bot = bot.TGBot()
        # self.wbkb = self.server.keyboards.bs_reply_markup
        # self.defkb = self.server.keyboards.class_main_menu_reply_markup

        # self.WB_file = "dbs/WB_mountain.dat"
        # loaded = self.helper.load_pickle(self.WB_file)
        # if loaded:
        #     self.status = loaded
        #     # self.dungeons_in_progress = loaded

        self.actions = {}
        self.internal = {
            "start_wb_mountain": self.WB,
        }

    def WB(self):
        pass
