# Comandos da arena

class ArenaComms:
    def __init__(self, server):
        self.server = server
        self.def_wait_time = 60
        self.actions = {
            "/enter_arena": self.enter_arena,
            "/exit_arena": self.exit_arena,
            "/arena_win": self.show_win_streak,
        }

    def enter_arena(self, caller, *args):
        if caller.pt_code:
            self.server.arena.add_to_arena(self.server.parties_codes[caller.pt_code])
        else:
            self.server.arena.add_to_arena(caller)
        return False

    def exit_arena(self, caller, *args):
        if caller.pt_code:
            self.server.arena.remove_from_arena(self.server.parties_codes[caller.pt_code])
        else:
            self.server.arena.remove_from_arena(caller)
        return False

    def show_win_streak(self, caller, *args):
        if caller.location == "arena":
            arena_lvl = self.server.arena.check_arena_lvl(caller)
            win_streak = "current_win_streak"
            max_win_streak = "max_win_streak"
            if caller.pt_code:
                arena_lvl = "party"
                text = f"Your party won {self.server.arena.arena_players[arena_lvl][caller.pt_code][win_streak]} in a row!\n"
                text += f"Your party's max is {self.server.arena.arena_players[arena_lvl][caller.pt_code][max_win_streak]}"

            text = f"You won {self.server.arena.arena_players[arena_lvl][caller.chat_id][win_streak]} in a row!\n"
            text += f"Your max is {self.server.arena.arena_players[arena_lvl][caller.chat_id][max_win_streak]}"

            self.server.bot.send_message(text = text, chat_id = caller.chat_id)
        else:
            self.server.bot. send_message(text = "You aren't in the arena", chat_id = caller.chat_id)
        return False
