import copy
from emoji import emojize
from random import randint
import bot

class ShamanComms:
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
        self.actions = {
        }
        self.internal = {
            "start_shaman": self.start_shaman
            #"start_enchanter": self.start_enchanter
        }

    def start_shaman(self, caller, caller_id = None, *args):
        if not args:
            text = "While walking in the dark deep forest, you feel a presence behind you. As you turn you see a lady carrying a cauldron. She does not speaks your language. She points at your ghostly weapon. Will you accept?\n\n"
            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.bs_reply_markup, parse_mode = 'MARKDOWN')

            return self.def_wait_time*5+caller.suc_refs*60
        else:
            resp = args[-1]
            if resp == emojize("YES :thumbs_up:"):
                self.server.playersdb.players_and_parties[caller.chat_id].inventory.append(copy.deepcopy(caller.weapon))
                text = "The Shaman touches your ghostly weapon and chants unintelligible words and sings a spell. Her cauldron starts to boil. Three hot drops spilled on your weapon. It rematerialized back into existance. The lady smiles and bows while turning herself into a hawk to fly away with her cauldron."
                self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb, parse_mode = 'MARKDOWN')
                return False
            else:
                text = "Ceridwen apologizes, turns herself into a greyhound, picks the cauldron with her jaws and runs into the woods."
                self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb, parse_mode = 'MARKDOWN')
                return False

    def to(self, chat_id):
        text = f"After {5+self.server.playersdb.players_and_parties[chat_id].suc_refs} minutes of *AWKWARD* starring, the goddess turns herself into a hen and runs away. It's up to you to imagine how she carried the cauldron."
        self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb, parse_mode="MARKDOWN")
