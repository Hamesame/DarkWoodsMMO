import deep_beastsdb
import random as rd
import copy
from emoji import emojize


class MegaBeastMan:
    '''
        Classe criada para controlar o encontro do jogador com a megabeasta e a batalha dele com ela.
    '''
    def __init__(self, server):
        self.server = server
        self.def_wait_time = 60
        self.bdbs = deep_beastsdb.DeepBeastsdb()
        self.mbdbs = self.bdbs.megabeasts
        self.ynkb = self.server.keyboards.bs_reply_markup

        self.ynkb2 = self.server.keyboards.forest_return_reply_markup
        self.defkb = self.server.keyboards.class_main_menu_reply_markup
        self.def_wait_time = 60
        self.actions = {
            "/boss_battle": self.battle_stats,
            "/leave_battle": self.leave
            }
        self.internal = {
            "start_mega1": self.start_mega,
            "start_mega2": self.start_mega2,
            }
        self.players = {}

    def battle_stats(self, caller, *args):
        '''
            Ainda preciso ver como vai funcionar a batalha.
        '''
        if not args:

            if caller.pt_code:
                code = caller.pt_code
            else:
                code = caller.chat_id
            if code in self.server.megadb.players:
                m_b = self.server.megadb.players[code].beast
                text = f"Battle against {m_b.name}\n\n"
                text += caller.last_megabeast_report
                health_icons = [
                    emojize(":cross_mark:"),
                    emojize(":red_heart:"),
                    emojize(":yellow_heart:"),
                    emojize(":green_heart:"),
                    emojize(":green_heart:"),
                    emojize(":green_heart:"),
                    emojize(":green_heart:"),
                    emojize(":green_heart:"),
                    emojize(":green_heart:"),
                ]
                i = 0
                for limb, health in m_b.limbs.items():
                    text += f"{limb}: {health} {health_icons[health]} /target_{i}\n"
                    i += 1
                text += "\n"
                text += "To select a limb to attack, just select one of the /target_(code) of the above. (Be sure to select a limb with health > 0.)"
                text = text.replace("_", "\\_")
                self.server.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
                return self.def_wait_time*2
            else:
                text = "You are not in a battle with a megabeast right now, to face one, go to the deep forest and find one."
                if caller.location == "megabeast":
                    caller.location = "deep_forest"
                self.server.bot.send_message(text=text, chat_id=caller.chat_id)
        else:
            # print("HEY OVER HERE")
            if args[-1].startswith("/target_"):
                # print("it entered")
                if caller.pt_code:
                    code = caller.pt_code
                else:
                    code = caller.chat_id
                m_b = self.server.megadb.players[code].beast
                limb_i = int(args[-1][8:])
                limb_list = list(m_b.limbs)
                if limb_i < len(limb_list):
                    caller.megabeast_target_limb = limb_list[limb_i]
                    text = f"You are now targeting the {limb_list[limb_i]} of the {m_b.name}."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def leave(self, caller, caller_id = None, *args):
        if not args:
            if caller.pt_code:
                code = caller.pt_code
            else:
                code = caller.chat_id
            if code in self.server.megadb.players:
                text = f"Are you sure you want to run from the {self.server.megadb.players[code].beast.name}?"
                self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.ynkb2)
                return self.def_wait_time
            else:
                text = "You are not battling a megabeast, to find one, go to the deep forest."
                self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                return False
        else:

            if args[-1] == emojize("yes"):

                if caller.pt_code:
                    pt = self.server.playersdb.players_and_parties[caller.pt_code]
                    self.server.megadb.remove_user(caller.pt_code)
                    text = "Your party decided to run away from the fight.."
                    self.server.bot.send_message(text=text, chat_id=pt.chat_ids, reply_markup=self.defkb)

                else:
                    self.server.megadb.remove_user(caller.chat_id)
                    text = "You decided to run away from the fight.."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)

            elif text == emojize("no"):
                if caller.pt_code:
                    pt = self.server.playersdb.players_and_parties[caller.pt_code]
                    text = "You decided to continue with the battle."
                    self.server.bot.send_message(text=text, chat_id=pt.chat_id, reply_markup=self.defkb)

                else:
                    text = "You decided to continue with the battle."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)

        return False

    def start_mega(self, caller, caller_id = None, *args):
        if not args:
            '''
                Code to run when the player finds a megabeast
            '''
            mega_beast = copy.deepcopy(rd.choice(self.mbdbs))
            # if caller.pt_code:
            #     code = caller.pt_code
            # else:
            #     code = caller.chat_id
            code = caller.code

            level = 1 + int(self.server.deep_forest_manager.jogs[code].stay_time/(3*60*60))
            mega_beast.attack = mega_beast.attack*level
            text = f"While wandering in the forest you see {mega_beast.traces}. Do you want to follow these tracks?"
            # self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.ynkb)

            if not caller.pt_code:
                if caller.chat_id in self.server.megadb.players:

                    text = f"While following the {self.server.megadb.players[caller.chat_id].beast.traces} you see {mega_beast.traces}. Do you want to follow these tracks?"
                    self.players[caller.chat_id] = mega_beast
                    self.server.bot.send_message(text=text, chat_id= caller.chat_id, reply_markup=self.ynkb)
                    return self.def_wait_time*5+caller.suc_refs*60
                else:
                    self.players[caller.chat_id] = mega_beast
                    self.server.bot.send_message(text=text, chat_id= caller.chat_id, reply_markup=self.ynkb)
                    return self.def_wait_time*5+caller.suc_refs*60
            else:
                if caller.pt_code in self.server.megadb.players:

                    text = f"While following the {self.server.megadb.players[caller.pt_code].beast.traces} you see {mega_beast.traces}. Do you want to follow these tracks?"
                    self.players[caller.pt_code] = mega_beast
                    self.server.bot.send_message(text=text, chat_id= caller.chat_ids, reply_markup=self.ynkb)
                    return self.def_wait_time*5
                else:
                    self.players[caller.pt_code] = mega_beast
                    self.server.bot.send_message(text=text, chat_id= caller.chat_ids, reply_markup=self.ynkb)
                    return self.def_wait_time*5
        else:
            '''
                Code to run when players answer
            '''
            if args[-1] == emojize("YES :thumbs_up:"):
                if caller.pt_code:
                    self.server.playersdb.players_and_parties[caller.code].location = "megabeast"
                    self.server.megadb.add_user(caller.pt_code, self.players[caller.pt_code], caller.time_factor_pt)
                    minutes = 3*60*caller.time_factor_pt
                    hours, minutes = divmod(minutes, 60)
                    text = f"Your party started following the tracks, to find what caused them usually takes {round(hours)} hours and {round(minutes)} minutes."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_ids, reply_markup=self.defkb)
                    del self.players[caller.pt_code]
                else:
                    self.server.playersdb.players_and_parties[caller.code].location = "megabeast"
                    self.server.megadb.add_user(caller.chat_id, self.players[caller.chat_id], caller.time_factor)
                    minutes = 3*60*caller.time_factor
                    hours, minutes = divmod(minutes, 60)
                    text = f"You started following the tracks, to find what caused them usually takes {round(hours)} hours and {round(minutes)} minutes."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    del self.players[caller.chat_id]
                return False
            elif args[-1] == emojize("NOPE :thumbs_down:"):
                if caller.pt_code:
                    text = "Your party decided not to follow the tracks, its a dangerous battle."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_ids, reply_markup=self.defkb)
                    del self.players[caller.pt_code]
                else:
                    text = "You decided not to follow the tracks, its a dangerous battle."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    del self.players[caller.chat_id]
                return False

            return False # Quando False é retornado o comando dropa

    def start_mega2(self, caller, caller_id = None, *args):
        if not args:
            if not caller.pt_code:
                return self.def_wait_time*5+caller.suc_refs*60    #  Eu sei, parece lixo, mas é assim por causa que a megabesta não está armazenada aqui
            else:
                return self.def_wait_time*5
        else:
            '''
                Code to run when players answer
            '''
            if caller.pt_code:
                code = caller.pt_code

            else:
                code = caller.chat_id
            self.server.playersdb.players_and_parties[code].location = "megabeast"
            self.server.megadb.players[code].is_at_battle = True
            self.server.deep_forest_manager.jogs[code].is_active = False
            text = emojize( f"You've engaged into battle with the {self.server.megadb.players[code].beast.name}.\n\n" # Este é o porque a primeira parte ficou com o outro.
                            f"Don't forget to check your health periodically.\n"
                            f"To check the status of the battle, /boss_battle.\n"
                            f"To leave the battle, use /leave_battle.\n"
                            f"Good luck!\n"
                            )
            if caller.pt_code:
                self.server.bot.send_message(text=text, chat_id=caller.chat_ids, reply_markup=self.defkb)
            else:
                self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)

            return False # Quando False é retornado o comando dropa




    def to(self, chat_id):
        # print("normal timeout")
        pass

    def to2(self, chat_id):
        '''
            Função que roda quando da timeout na função interna.
        '''
        # print("timeout de internal")
        if chat_id in self.server.playersdb.players_and_parties:
            code = self.server.playersdb.players_and_parties[chat_id].code
            if code in self.server.megadb.players:
                if self.server.megadb.players[code].time_to_arrive < 14*60:
                    self.server.megadb.remove_user(code)
            if chat_id[0] == "/":
                if chat_id in self.server.playersdb.players_and_parties:
                    text = "It looks dangerous, so your party decided to step back."
                    chat_ids = self.server.playersdb.players_and_parties[chat_id].chat_ids
                    self.server.bot.send_message(text=text, chat_id=chat_ids, reply_markup=self.defkb)
            else:

                text = "It looks dangerous, so you decided to step back."
                self.server.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb)
