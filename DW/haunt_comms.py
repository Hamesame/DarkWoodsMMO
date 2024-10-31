import items
import random as rd
from emoji import emojize
import telegram
import bot
import copy

class HauntComms:
    '''
        O único comando em deep forest é o próprio "/deep_forest". Fora ele, temos o comando interno "start_df" para o encontro com a deep forest.

        A partir dele, podem ter vários argumentos. Como se quer voltar ou não.

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
            "haunted": self.haunted
        }

    def haunted(self, caller, caller_id = None, *args):
        if not args:

            if caller.code[0] == "/":
                text = "You feel a bit uneasy. As if there is someone behind you. But it is just your party. You feel one of the weapons in the shared inventory shake. What you want to do?\n\n"
                text += "/hold to hold it firmly\n"
                text += "/throw to throw it away\n"
                self.bot.send_message(text=text, chat_id=caller.chat_ids)
            else:
                text = "You feel a bit uneasy. As if there is someone behind you. But there's no one, you are alone. You feel one of your weapons shaking. What you want to do?\n\n"
                text += "/hold to hold it firmly\n"
                text += "/throw to throw it away\n"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
            return self.def_wait_time
        else:

            if args[-1] == '/hold':
                if caller.code[0] == "/":
                    text_ghost = f"Someone from {caller.name} managed to hold it firmly. It's not this time you got your weapon back. Try haunting other time."
                else:
                    text_ghost = f"{caller.name} managed to hold it firmly. It's not this time you got your weapon back. Try haunting other time."
                for wep in caller.inventory:
                    if wep.is_legendary:
                        for chat,pl in self.server.playersdb.players_and_parties.items():
                            if wep.name in pl.weapon.name and wep.talismans == pl.weapon.talismans:
                                self.bot.send_message(text=text_ghost, chat_id=chat)
                                text = "You held it firmly and it shook violently emmiting a sound of grief, after a while it calmed and you stored it back into your inventory."
                                if caller.code[0] == "/":
                                    self.bot.send_message(text=text, chat_id=caller.chat_ids)
                                else:
                                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                                return False
            else:
                found = False
                ii = 0
                for wep in caller.inventory:
                    if wep.is_legendary:
                        for chat,pl in self.server.playersdb.players_and_parties.items():
                            if wep.name in pl.weapon.name and wep.talismans == pl.weapon.talismans:
                                pl.inventory.append(copy.deepcopy(wep))
                                del caller.inventory[ii]
                                found = True
                                text_gost = f"After some haunting, you managed your {wep.name} back."
                                self.bot.send_message(text=text_ghost, chat_id=chat)
                                text_loser = "The weapon went flying away. If you had it equipped, you are left with a ghostly version of it."
                                if caller.code[0] == "/":
                                    self.bot.send_message(text=text_loser, chat_id=caller.chat_ids)
                                else:
                                    self.bot.send_message(text=text_loser, chat_id=caller.chat_id)
                                return False
                    ii += 1
                text = "The weapon shook on the ground but it stopped soon after"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return False

    def to(self, chat_id):
        found = False
        user = self.server.playersdb.players_and_parties[chat_id]
        for wep in user.inventory:
            if wep.is_legendary:
                for chat,pl in self.server.playersdb.players_and_parties.items():
                    if wep.name in pl.weapon.name and wep.talismans == pl.weapon.talismans:
                        pl.inventory.append(copy.deepcopy(wep))
                        del user.inventory[ii]
                        found = True
                        text_gost = f"After some haunting, you managed your {wep.name} back."
                        self.bot.send_message(text=text_ghost, chat_id=chat)
                        text_loser = "The weapon went flying away. If you had it equipped, you are left with a ghostly version of it."
                        if caller.code[0] == "/":
                            self.bot.send_message(text=text_loser, chat_id=caller.chat_ids)
                        else:
                            self.bot.send_message(text=text_loser, chat_id=caller.chat_id)
                        break
            ii += 1
            if found:
                break
