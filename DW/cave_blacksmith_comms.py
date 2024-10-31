########################################
# Classe que contém os comandos do BS  #
########################################

import items
import random as rd
from emoji import emojize
import telegram
import bot
import copy


class CaveBlacksmithComms:
    '''
        Classe dos comandos do blacksmith.
    '''
    def __init__(self, server):
        self.bot = bot.TGBot()          # Bot pra mandar mensagens
        self.server = server            # O jogo inteiro
        self.defkb = server.defkb       # O keyboard padrão
        self.def_wait_time = 60         # 1 minuto

        self.actions = {}
        self.internal = {
            "equalize_weapon": self.equalize,   # Comando interno que só é ativado quando o jogador acha o bs
            "start_cave_bs": self.bs_user_interface,
            "reshape_talisman": self.reshape,
        }
