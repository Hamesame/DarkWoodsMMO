########################################
# Classe que contém os comandos do do evento de halloween  #
########################################

import items
import random as rd
from emoji import emojize
import telegram
import bot
import copy
import death
import player


class MagMellComms:
    '''
        Classe dos comandos do blacksmith.
    '''
    def __init__(self, server):
        self.bot = bot.TGBot()          # Bot pra mandar mensagens
        self.server = server            # O jogo inteiro
        self.defkb = server.defkb       # O keyboard padrão
        self.def_wait_time = 60         # 1 minuto
        self.Death = death.Death(server)
        self.actions = {}
        self.internal = {
            "start_mag_mell": self.mag_mell

        }


    def mag_mell(self, caller, caller_id = None, *args):
        if not args:
            text = ('You found the ruins of a small shrine. There were old drawings of an island that floated above our world. Also, on the ground, scribbles of some kind of cyclical calendar where we can see our world and the island revolving in opposite directions. The points where they intersect are marked with the words "Samhain" and "Bealtaine". Also, above the calendar, a portal to the otherworld is opened, would you like to adventure there?')
            if isinstance(caller, player.Player):
                self.bot.send_message(text=text, chat_id= caller.chat_id, reply_markup=self.server.keyboards.inline_dg_reply_markup)
            else:
                self.bot.send_message(text=text, chat_id= caller.chat_ids, reply_markup=self.server.keyboards.inline_dg_reply_markup)
            return self.def_wait_time*5
        else:
            player_text = args[-1]
            message_id = args[0]
            code = caller.code
            if player_text == emojize("YES :thumbs_up:"):
                # Ok, let me think, the player will do something very close do dying but will continue it's progress where he is
                text = "You stepped into the otherworld into the womb where centuries pass like a day. After some hours inside there, you look at your weapon and it is glowing leaving a ghoslty trail behind. When you leave the portal you just entered, you notice one thing. You have died. Luckly you just lost your items and not your progress."
                if code[0] == "/":

                    for weapon in self.server.playersdb.players_and_parties[code].inventory:
                        if weapon.is_legendary:
                            weapon.is_shared_and_equipped = False
                            self.server.itemsdb.add_weapon_to_pool(copy.deepcopy(weapon))
                            # self.server.playersdb.players_and_parties[code].inventory.remove(weapon)
                        else:
                            print(f"weapon owner = {weapon.owner}")
                            if weapon.owner:
                                self.server.playersdb.players_and_parties[weapon.owner].ghost_inv.append(weapon)
                    self.server.playersdb.players_and_parties[code].inventory = []
                    for cid in caller.chat_ids:
                        self.Death.die_event(cid)
                else:
                    self.Death.die_event(code)

            else:
                text = "Out of fear or wisdom, you opted for not venturing into Mag Mell"
            if isinstance(caller, player.Player):
                self.bot.send_message(text=text, chat_id= caller.chat_id)
            else:
                self.bot.send_message(text=text, chat_id= caller.chat_ids)

    def to(self, chat_id):
        text = f"After 5 minutes of pondering, you decided not to venture into the otherworld."
        if chat_id[0] == "/":
            chat_ids = self.server.playersdb.players_and_parties[chat_id].chat_ids
            self.bot.send_message(text=text, chat_id=chat_ids, reply_markup=self.defkb, parse_mode="MARKDOWN")
        else:
            self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb, parse_mode="MARKDOWN")
