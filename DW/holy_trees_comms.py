import copy
from emoji import emojize
from random import randint
import bot
import deep_items

class HolyTreeComms:
    '''

    '''
    def __init__(self, server):
        '''
            Ele carrega o server, o keyboard padrão, o tempo padrão de espera, que é 1 minuto, o bot pra mandar mensagens, e o único comando, que é o /deep_forest.

        '''
        self.server = server
        self.defkb = server.defkb           # Keyboard padrão
        self.def_wait_time = 60
        self.bot = bot.TGBot()
        self.Talismandb = deep_items.Talismandb()
        self.actions = {
        }
        self.internal = {
            "start_oak_ash_thorn": self.start_oak_ash_thorn
        }

    def start_oak_ash_thorn(self, caller, caller_id = None, *args):
        if not args:
            text = "You walk into a woodland glade and find the holy trees of Oak, Ash and thorn. What would you like to do?"
            self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode = 'MARKDOWN')
            return self.def_wait_time*5+caller.suc_refs*60
        else:
            if args[-1] == "Utter a charm in the verse of three":
                if self.server.is_midnight:
                    text = "Till the summer king is born!"
                    tal = [copy.deepcopy(self.Talismandb.talismans["helianth_petal"])]
                    pl = self.server.playersdb.players_and_parties[caller.chat_id]
                    pl.storage.extend(copy.deepcopy(tal))
                    self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode = 'MARKDOWN')
                    return False
                else:
                    text = f"You tried to {args[-1]}, but nothing happens."
                    self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode = 'MARKDOWN')
                    return False
            else:
                text = f"You tried to {args[-1]}, but nothing happens."
                self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode = 'MARKDOWN')
                return False

    def to(self, chat_id):
        text = f"After {5+self.server.playersdb.players_and_parties[chat_id].suc_refs} minutes of *AWKWARD* starring trees, you decided to run away."
        self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb, parse_mode="MARKDOWN")
