import bot
import player
from emoji import emojize
import random as rd
import helper
import time


class WBComms:
    '''
        Classe que controla os comandos do WB. (sunflower neste caso)
    '''
    def __init__(self, server):
        self.server = server
        self.defkb = server.defkb
        self.def_wait_time = 60
        self.helper = helper.Helper(server)
        self.bot = bot.TGBot()
        self.wbkb = self.server.keyboards.bs_reply_markup
        self.defkb = self.server.keyboards.class_main_menu_reply_markup

        self.status = {"Health":50e9, "Minions":300e6, "Players":[], "Kill count":0, "Recover count":0, "Is Dead":False, "Started time":time.time(), "Recovery rate":1e6}

        self.WB_file = "dbs/WB.dat"
        loaded = self.helper.load_pickle(self.WB_file)
        if loaded:
            self.status = loaded
            # self.dungeons_in_progress = loaded

        self.actions = {}
        self.internal = {
            "start_WB": self.WB,
            "start_pt_WB": self.pt_WB
        }


    def WB(self, caller, caller_id = None, *args):
        '''
            Comando que roda quando o jogador acha a sunflower na floresta em solo

            Parâmetros:

            caller (Player): Jogador que achou a sunflower
        '''
        if not self.server.World_boss.status["Is Dead"]:
            # Se n morreu, ele entra na sunflower e fala que o jogador não está ativo.
            self.server.woods.players[caller.chat_id]["active"] = False

            if not args:


                text = emojize("You arrived at a darker part of the forest where the trees were sparse and fauna was absent.\n\n"
                                "After some time, you got to the feet of a mountain. You decided to climb it.\n"
                                "At its top you could witness a valley. At it's bottom grows a rotten sunflower :sunflower::sunflower::sunflower::sunflower::sunflower::sunflower: the size of a mountain.\n"
                                "You couldn't get closer to it. It was surrounded by insurmountable plant life and the entire area stinks death and blood.\n\n"
                                "*Would you like to adventure there*?.")

                text = emojize(
                "A long time ago, when the first dwellers of this world arrived, a small Sunflower :sunflower: caught the attention of many travellers, it stood in the center of a clearing, looking like an innocent being, all travellers that passed by just glanced the overly beatiful part of the forest and preferred to *leave it intact*.\n"
                "Then the Sunflower :sunflower::sunflower: grew day after day, some adventurers noted the difference others were simply not caring about it. All of them preffered to *leave the place intact*.\n"
                "The appearance of new plant based beasts was thought to be something expected as the place itself is a forest. But it was the making of Sunflower :sunflower::sunflower::sunflower: all along, but still no passerby made the correlation of its growth with the appearance of new plant beasts and still preffered to *leave it intact*.\n"
                "Adventurers learned new skills and some could tame the forest beasts. They noted that those plants were stronger than regular animals. As the Sunflower :sunflower::sunflower::sunflower::sunflower: was now bigger than its surrounding trees. But it was surrounded by insurmountable plant life, and *noone could approach it*.\n"
                "Out of the blue, an Old Man appeared in the woods, talking about the one enemy you never fought :sunflower::sunflower::sunflower::sunflower::sunflower: as the Sunflower surroundings became barren, and usure of what that could mean, *adventurers decided to step back*.\n\n"

                "Then, the Sun dimmed and the sky grew dark with stormy clouds. Giant roots emerged from the bowels of the forest, toppling dead trees and causing animals to flee.\n\n"

                "A 4-day battle was fought to defeat this threat, and with the help of 100 brave soldiers, the sunflower was defeated."

                "The sunflower had been rotting for almost a year when the Druids decided to try to tame it."

                "You might ask. How can druids tame something that is already dead? That is why those are no common druids, those are necromancers."

                "As you approach a rotten valley with a giant rotten Sunflower :sunflower::sunflower::sunflower::sunflower::sunflower::sunflower::sunflower: you smell blood and death."

                "*Would you like to adventure there*?."

                )

                self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.bs_reply_markup, parse_mode = 'MARKDOWN')

                return self.def_wait_time*5+caller.suc_refs*60
            else:
                if args[-1] == emojize("YES :thumbs_up:") and caller.chat_id not in self.server.World_boss.status["Players"]:           # Comando pra entrar na sunflower
                    self.server.World_boss.add_player(caller.chat_id)
                    return False
                elif args[-1] == emojize("NOPE :thumbs_down:"):                                             # Comando pra rejeitar a sunflower
                    text = "It's a dangerous place, so you decided to step back."
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    self.server.woods.players[caller.chat_id]["active"] = True

                    return False

                else:                                       # Caso o cara seja um babaca e n saiba escrever
                    text = ("The gods did not understand your prayer. You can seek help at the campfire: \nhttps://t.me/DWcommchat")
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.defkb)
                    return self.def_wait_time*5+caller.suc_refs*60
        else:
            # Caso a sunflower esteja morta

            text = emojize(
                "While waling on the deep snow of the forest you witness a mountain, "
                "its completelly covered in snow :snowflake::snowflake::snowflake: "
                "and its summit isnt visible due to the clouds "
                "forming nearby. You got the conclusion that nothing can survive "
                "that weather and decided to step back. It's a dangerous place."
            )
            self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode = "MARKDOWN")
            self.server.woods.players[caller.chat_id]["active"] = True
            return False

    def pt_WB(self, caller, caller_id = None, *args):
        '''
            Método que administra o comando de WB pra parties.
            Este código é extremamente similar ao de cima, mas com a adição das parties.

            Parâmetros:

            caller_id (str): id do jogador que respondeu

            caller (dic): Party que achou o WB
        '''
        if not self.server.World_boss.status["Is Dead"]:
            self.server.playersdb.players_and_parties[caller.pt_code].active = False
            self.server.woods.players[caller.pt_code]["active"] = False
            if not args:


                text = emojize("Your party arrived at a darker part of the forest where the trees were sparse and fauna was absent.\n\n"
                                "After some time, you got to the feet of a mountain. You decided to climb it.\n"
                                "At its top you could witness a valley. At it's bottom grows a sunflower :sunflower::sunflower::sunflower::sunflower::sunflower::sunflower: the size of a mountain.\n"
                                "You couldn't get closer to it. It was surrounded by insurmountable plant life.\n\n"
                                "*Would you like to adventure there*?.")
                text = emojize(
                "A long time ago, when the first dwellers of this world arrived, a small Sunflower :sunflower: caught the attention of many travellers, it stood in the center of a clearing, looking like an innocent being, all travellers that passed by just glanced the overly beatiful part of the forest and preferred to *leave it intact*.\n"
                "Then the Sunflower :sunflower::sunflower: grew day after day, some adventurers noted the difference others were simply not caring about it. All of them preffered to *leave the place intact*.\n"
                "The appearance of new plant based beasts was thought to be something expected as the place itself is a forest. But it was the making of Sunflower :sunflower::sunflower::sunflower: all along, but still no passerby made the correlation of its growth with the appearance of new plant beasts and still preffered to *leave it intact*.\n"
                "Adventurers learned new skills and some could tame the forest beasts. They noted that those plants were stronger than regular animals. As the Sunflower :sunflower::sunflower::sunflower::sunflower: was now bigger than its surrounding trees. But it was surrounded by insurmountable plant life, and *noone could approach it*.\n"
                "Out of the blue, an Old Man appeared in the woods, talking about the one enemy you never fought :sunflower::sunflower::sunflower::sunflower::sunflower: as the Sunflower surroundings became barren, and usure of what that could mean, *adventurers decided to step back*.\n\n"

                "Today, the Sun dimmed and the sky grew dark with stormy clouds. Giant roots emerged from the bowels of the forest, toppling dead trees and causing animals to flee.\n\n"

                "A 4-day battle was fought to defeat this threat, and with the help of 100 brave soldiers, the sunflower was defeated."

                "The sunflower had been rotting for almost a year when the Druids decided to try to tame it."

                "You might ask. How can druids tame something that is already dead? That is why those are no common druids, those are necromancers."

                "As you approach a rotten valley with a giant rotten Sunflower :sunflower::sunflower::sunflower::sunflower::sunflower::sunflower::sunflower: you smell blood and death."

                "*Would you like to adventure there*?."

                )

                self.bot.send_message(text=text, chat_id=caller.chat_ids, reply_markup=self.server.keyboards.bs_reply_markup, parse_mode = "MARKDOWN")

                return self.def_wait_time*5
            else:

                if args[-1] == emojize("YES :thumbs_up:") and caller_id.chat_id not in self.server.World_boss.status["Players"]:
                    for chat in caller.chat_ids:
                        self.server.World_boss.add_player(chat)
                    self.server.playersdb.players_and_parties[caller.pt_code].location = "WB"
                    return False
                elif args[-1] == emojize("NOPE :thumbs_down:"):
                    text = "It's a dangerous place, so your party decided to step back."
                    self.bot.send_message(text=text, chat_id=caller.chat_ids, reply_markup=self.defkb)
                    self.server.playersdb.players_and_parties[caller.pt_code].active = True
                    self.server.woods.players[caller.pt_code]["active"] = True

                    return False


                else:
                    text = ("The gods did not understand your prayer. You can seek help at the campfire: \nhttps://t.me/DWcommchat")

                    # for chat,jog in caller.items():
                    #     if isinstance(jog, player.Player):
                    self.bot.send_message(text=text, chat_id=caller_id.chat_id, reply_markup=self.server.keyboards.bs_reply_markup)

                    return False
        else:

            text = emojize(
                "While waling on the deep snow of the forest you witness a mountain, "
                "its completelly covered in snow :snowflake::snowflake::snowflake: "
                "and its summit isnt visible due to the clouds "
                "forming nearby. You got the conclusion that nothing can survive "
                "that weather and decided to step back. It's a dangerous place."
            )
            self.server.playersdb.players_and_parties[caller.pt_code].active = True
            self.server.woods.players[caller.pt_code]["active"] = True
            self.bot.send_message(text=text, chat_id=caller.chat_ids, parse_mode = "MARKDOWN")
            return False

    def to(self, chat_id):
        '''
            Função de timeout da sunflower.

            chat_id (str): id do telegram ou código da party que deu timeout
        '''
        if chat_id[0] == "/":
            text = "It's a dangerous place, so your party decided to step back."
            pt = self.server.playersdb.players_and_parties[chat_id]
            self.bot.send_message(text=text, chat_id=pt.chat_ids, reply_markup=self.defkb)
        else:

            text = "It's a dangerous place, so you decided to step back."
            self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb)
        if chat_id in self.server.woods.players:
            if chat_id[0] == "/":
                try:
                    self.server.woods.players[chat_id]["active"] = True
                    self.server.playersdb.players_and_parties[chat_id].active = True
                    self.server.woods.players[chat_id]["entered_dg"] = False
                except:
                    self.server.playersdb.players_and_parties[chat_id].active = True
            else:
                    self.server.woods.players[chat_id]["active"] = True
                    self.server.woods.players[chat_id]["entered_dg"] = False
