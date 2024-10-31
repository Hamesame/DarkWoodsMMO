import bot
import player
from emoji import emojize
from copy import copy
import random as rd
import helper
import os
import numpy as np
import death
import time
import beastsdb
import deep_items
import Labyrinth

class WBUser:
    def __init__(self, code, location):
        self.code = code
        self.location = location
        self.time_spent = 0 #In seconds


class WorldBoss:
    '''
        Classe do zauarudo boss.
    '''
    def __init__(self, server):
        self.server = server
        self.defkb = server.defkb
        self.Talismandb = deep_items.Talismandb()
        self.def_wait_time = 60             # 1 minuto
        self.helper = helper.Helper(server)
        self.bot = bot.TGBot()
        self.wbkb = self.server.keyboards.bs_reply_markup               # YES/NOPE
        self.defkb = self.server.keyboards.class_main_menu_reply_markup # Other keyboard
        self.std_time = 15*60           # 15 minutos

        self.Max_hp = round(1e4)       # Hp máximo do boss
        self.status = {"hp": self.Max_hp, "players": []}

        # The players are stored as a class with code, location and time spent

        self.WB_file = "dbs/WB_mountain.dat"
        loaded = self.helper.load_pickle(self.WB_file)  # Carrega o WB
        if loaded:
            self.status = loaded
            # self.dungeons_in_progress = loaded




        self.last_processed = 0
        self.channel_id = "-1001123456" # Channel id
        self.dona_morte = death.Death(server)

        self.hp = [":green_heart:",":yellow_heart:",":orange_heart:",":red_heart:️",":broken_heart:",":black_heart:"]
        # Lista de stats do WB, a medida q ele vai perdendo vida, ele vai mostrando corações diferentes


    def save_status(self):
        '''
            Método que vai salvar a sunflower
        '''
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle(self.status, self.WB_file)
