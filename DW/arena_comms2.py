from emoji import emojize

class ArenaComms:
    def __init__(self, server):
        self.server = server
        self.def_wait_time = 60
        self.actions = {
            "/enter_arena": self.enter_arena_lobby,
            emojize(":crossed_swords: Arena :crossed_swords:"): self.enter_arena_lobby,
            "/exit_arena": self.exit_arena,
            # "/arena_win": self.show_rank,
        }
        self.internal = {

        }

    def enter_arena_lobby(self, caller, *args):
        '''
            Comando dado pelo jogador quando está no camp.

            Ele vai mostrar todas as opções de arena existentes.
        '''

        text = "The arena has been dismantled, and will never return. :("
        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

        if not args:
            if caller.location == "camp":
                text = emojize(

                    f"Welcome to the :crossed_swords: Arena :crossed_swords:! Here you can test your skills and your weapons forged at the forest.\n\n"
                    f"You have {caller.arenas_left}/{caller.max_arenas} free arenas left\n\n"        # Toda meia noite reseta as arenas
                    f"Your arena rank: {caller.arena_rank}\n\n"
                    f"You have 2 options:\n\n"
                    f"/enter the common arena, where you can fight any player in your rank range and gain experience there.\n\n"
                    f"/ENTER the ranked arena, which is the same as the common arena, but players will have to bet a weapon. The minimum bet is a 100-stats weapon. The winner takes both weapons.\n\n"
                    f"You can enter any arena for free for a maximum of {caller.max_arenas} per day. More than that you'll have to pay a weapon as a fee (we are going to take the one with the lowest stats)."

                )
                self.server.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.arena_lobby_reply_markup)
                return self.def_wait_time*2
            else:
                text = "You can access the arena when you are at the camp."
                self.server.bot.send_message(text = text, chat_id = caller.chat_id)
                return self.def_wait_time*2
        else:
            if args[-1] == "/enter" or args[-1] ==emojize(":crossed_swords: Common Arena :crossed_swords:"):
                if caller.pt_code:
                    text = f"Only solo arenas available for now. If you want to take part at the arena, please /leave_pt your party."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return False
                else:
                    return self.server.arena.add_to_arena(caller)

            elif args[-1] == "/ENTER" or args[-1] == emojize(":fire: Ranked Arena :fire:"):
                if caller.pt_code:
                    text = f"Only solo arenas available for now. If you want to take part at the arena, please /leave_pt your party."
                    self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                    return False
                else:
                    return self.server.arena.add_to_ranked_arena(caller)

            elif args[-1] == emojize(":BACK_arrow: Back :BACK_arrow:"):
                text = "Ok, you decided to step back."
                self.server.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup =self.server.keyboards.at_camp_main_menu_reply_markup)
                return False
            else:
                return self.server.arena.process(caller, args[-1])
            return False

    def exit_arena(self, caller, *args):
        if caller.pt_code:
            self.server.arena.remove_from_arena(self.server.parties_codes[caller.pt_code])
        else:
            # self.server.arena.remove_from_arena(caller)
            self.to(caller.chat_id)
        return False

    def to(self, chat_id):
        '''
            Essa função vai abrangir o timeout em várias etapas.

        '''
        self.server.playersdb.players_and_parties[chat_id].location = "camp"
        if chat_id in self.server.arena.main_lobby:
            del self.server.arena.main_lobby[chat_id]
            text = "2 minutes have passed and you have not chosen what type of arena you want."
            self.server.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.server.defkb2)
        elif chat_id in self.server.arena.common_arena_lobby:
            del self.server.arena.common_arena_lobby[chat_id]
            text = "2 minutes have passed and you have not found an opponent."
            self.server.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.server.defkb2)
        elif chat_id in self.server.arena.ranked_arena_lobby:
            del self.server.arena.ranked_arena_lobby[chat_id]
            text = "2 minutes have passed and you have not found an opponent."
            self.server.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.server.defkb2)
        elif self.server.arena.check_if_code_in_ongoing_battles(chat_id):
            code = self.server.arena.check_if_code_in_ongoing_battles(chat_id)
            if self.server.arena.ongoing_battles[code].pl1.chat_id == chat_id:
                if self.server.arena.ongoing_battles[code].pl1.is_ready and self.server.arena.ongoing_battles[code].pl2.is_ready:
                    self.server.arena.ongoing_battles[code].pl1.total_health = 0
                    text = "You were standing at the arena doing nothing, so you lost the fight."
                    self.server.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.server.defkb2)
                else:
                    text = "The Opponent did not accepted the battle, back to the lobby.."
                    self.server.bot.send_message(text=text, chat_id=self.server.arena.ongoing_battles[code].pl2.chat_id)
                    if self.server.arena.ongoing_battles[code].pl2.arena_type == "ranked":
                        self.server.arena.ranked_arena_lobby[self.server.arena.ongoing_battles[code].pl2.chat_id] = self.server.arena.ongoing_battles[code].pl2
                    else:
                        self.server.arena.common_arena_lobby[self.server.arena.ongoing_battles[code].pl2.chat_id] = self.server.arena.ongoing_battles[code].pl2
                    text = "You did not accept the fight, quitting the arena."
                    self.server.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.server.defkb2)
                    del self.server.arena.ongoing_battles[code]

            else:
                if self.server.arena.ongoing_battles[code].pl1.is_ready and self.server.arena.ongoing_battles[code].pl2.is_ready:
                    self.server.arena.ongoing_battles[code].pl2.total_health = 0
                    text = "You were standing at the arena doing nothing, so you lost the fight."
                    self.server.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.server.defkb2)
                else:
                    text = "The Opponent did not accepted the battle, back to the lobby.."
                    self.server.bot.send_message(text=text, chat_id=self.server.arena.ongoing_battles[code].pl1.chat_id)
                    if self.server.arena.ongoing_battles[code].pl1.arena_type == "ranked":
                        self.server.arena.ranked_arena_lobby[self.server.arena.ongoing_battles[code].pl1.chat_id] = self.server.arena.ongoing_battles[code].pl1
                    else:
                        self.server.arena.common_arena_lobby[self.server.arena.ongoing_battles[code].pl1.chat_id] = self.server.arena.ongoing_battles[code].pl1

                    del self.server.arena.ongoing_battles[code]
                    text = "You did not accept the fight, quitting the arena."
                    self.server.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.server.defkb2)

            # text = "You were standing at the arena doing nothing, so you lost the fight."
            # self.server.bot.send_message(text=text, chat_id=chat_id)
