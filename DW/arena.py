# Arena

import battle
import time
import random as rd
import player
import player_comms
import os
import traceback

class Arena:
    def __init__(self, server):
        self.server = server
        self.helper = server.helper
        self.BattleMan = battle.BattleMan(server)
        self.player_comms = player_comms.PlayerComms(server)
        self.arena_players = {"5": {}, "10": {}, "15": {}, "20": {}, "party": {}}
        self.timestamp0 = time.time()
        self.timestamp = time.time()
        self.encounter_time = 15
        self.arena_file = "dbs/arena.dat"
        self.arena_backup = "dbs/arena.bak"
        loaded = self.helper.load_pickle(self.arena_file)
        if loaded:
            self.arena_players = loaded

    def save_arena(self):
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.helper.save_pickle(self.arena_players, self.arena_file)

    def check_arena_lvl(self, player):
        if not isinstance(player, dict):
            lvl = player.level

            if lvl < 5:
                return "5"

            if 5 <= lvl < 10:
                return "10"

            if 10 <= lvl < 15:
                return "15"

            if 15 <= lvl <= 20:
                return "20"
        else:
            return "party"

    def check_death(self, player):
        to_die = []
        if isinstance(player, dict):
            for chat_id, jogador in self.arena_players["party"]["player"].items():
                if isinstance(jogador, player.Player):
                    hp = 0
                    for limb in jogador.hp:
                        hp+=limb.health
                    if hp == 0:
                        to_die.append(jogador)
        else:
            hp = 0
            for limb in player.hp:
                hp+=limb.health
            if hp == 0:
                to_die.append(player)
        return to_die

    def add_to_arena(self, jog):
        if not isinstance(jog, dict):
            if jog.location == "camp":
                jog.location = "arena"
                arena_lvl = self.check_arena_lvl(jog)
                self.arena_players[str(arena_lvl)][jog.chat_id] = {
                    "player": jog,
                    "arena_lvl": arena_lvl,
                    "max_win_streak": 0,
                    "current_win_streak": 0,
                    "rem_enctime": self.encounter_time
                }
                self.server.bot.send_message(text = f"You just entered the arena level {self.check_arena_lvl(jog)}!", chat_id = jog.chat_id)
            else:
                self.server.bot.send_message(text = "You need to be in the camp to join the arena", chat_id = jog.chat_id)
        else:
            if jog["location"] == "camp":
                jog["location"] = "arena"
                self.arena_parties["party"][jog["code"]] = {
                    "player": jog,
                    "arena_lvl": "party",
                    "max_win_streak": 0,
                    "current_win_streak": 0,
                    "rem_enctime": self.encounter_time
                }
                for chat_id, player in jog.items():
                    if isinstance(player, player.Player):
                        self.server.bot.send_message(text = "Your party has entered the arena!", chat_id = player.chat_id)
            else:
                for chat_id, player in jog.items():
                    if isinstance(player, player.Player):
                        self.server.bot.send_message(text = "Your party needs to be at the camp to join the arena", chat_id = player.chat_id)

    def remove_from_arena(self, jog):
        if not isinstance(jog, dict):
            jog.location = "camp"
            for arena_lvl in self.arena_players:
                if jog.chat_id in self.arena_players[arena_lvl]:
                    del self.arena_players[arena_lvl][jog.chat_id]
                    self.server.bot.send_message(text = "You have returned to the camp", chat_id = jog.chat_id)

        else:
            jog["location"] = "camp"
            if jog["code"] in self.arena_players["party"]:
                del self.arena_players[arena_lvl][jog["code"]]
                for chat_id, player in jog.items():
                    if isinstance(player, player.Player):
                        self.server.bot.send_message(text = "Your party has returned to the camp", chat_id = player.chat_id)

    def player_battle(self, jog1, jog2):

        winner = None
        loser = None

        battle_res = self.BattleMan.battle(jog1, jog2)

        if battle_res == 1:
            winner = jog1
            loser = jog2
            if isinstance(winner, dict) and isinstance(loser, dict):
                name_str = "name"
                for chat_id, player in winner.items():
                    if isinstance(player, player.Player):
                        self.server.bot.send_message(text = f"Your party fought with {loser[name_str]} and won", chat_id = chat_id)
                for chat_id, player in loser.items():
                    if isinstance(player, player.Player):
                        self.server.bot.send_message(text = f"Your party fought with {winner[name_str]} and lost", chat_id = chat_id)

                self.arena_players[loser["code"]]["current_win_streak"] = 0
                self.arena_players[winner["code"]]["current_win_streak"] += 1
                if self.arena_players[winner["code"]]["max_win_streak"] < self.arena_players[winner["code"]]["current_win_streak"]:
                    self.arena_players[winner["code"]]["max_win_streak"] = self.arena_players[winner["code"]]["current_win_streak"]

            self.arena_players[jog2.chat_id]["current_win_streak"] = 0
            self.arena_players[jog1.chat_id]["current_win_streak"] += 1
            if self.arena_players[jog1.chat_id]["max_win_streak"] < self.arena_players[jog1.chat_id]["current_win_streak"]:
                self.arena_players[jog1.chat_id]["max_win_streak"] = self.arena_players[jog1.chat_id]["current_win_streak"]

        if battle_res == 2:

            winner = jog2
            loser = jog1

            if isinstance(winner, dict) and isinstance(loser, dict):
                name_str = "name"
                for chat_id, player in winner.items():
                    if isinstance(player, player.Player):
                        self.server.bot.send_message(text = f"Your party fought with {loser[name_str]} and won", chat_id = chat_id)
                for chat_id, player in loser.items():
                    if isinstance(player, player.Player):
                        self.server.bot.send_message(text = f"Your party fought with {winner[name_str]} and lost", chat_id = chat_id)

                self.arena_players[loser["code"]]["current_win_streak"] = 0
                self.arena_players[winner["code"]]["current_win_streak"] += 1
                if self.arena_players[winner["code"]]["max_win_streak"] < self.arena_players[winner["code"]]["current_win_streak"]:
                    self.arena_players[winner["code"]]["max_win_streak"] = self.arena_players[winner["code"]]["current_win_streak"]

            self.arena_players[jog1.chat_id]["current_win_streak"] = 0
            self.arena_players[jog2.chat_id]["current_win_streak"] += 1
            if self.arena_players[jog2.chat_id]["max_win_streak"] < self.arena_players[jog2.chat_id]["current_win_streak"]:
                self.arena_players[jog2.chat_id]["max_win_streak"] = self.arena_players[jog2.chat_id]["current_win_streak"]

        if battle_res == 3:
            if isinstance(jog1, dict) and isinstance(jog2, dict):
                name_str = "name"
                for chat_id, player in jog1.items():
                    if isinstance(player, player.Player):
                        self.server.bot.send_message(text = f"Your party fought with {jog2[name_str]} and draw the battle", chat_id = chat_id)
                for chat_id, player in jog2.items():
                    if isinstance(player, player.Player):
                        self.server.bot.send_message(text = f"Your party fought with {jog1[name_str]} and draw the battle", chat_id = chat_id)
            self.server.bot.send_message(text = f"In the arena you fought {jog1.name} and draw the battle", chat_id = jog2.chat_id)
            self.server.bot.send_message(text = f"In the arena you fought {jog2.name} and draw the battle", chat_id = jog1.chat_id)
            return None

        self.server.bot.send_message(text = f"In the arena you fought {loser.name} and won the battle", chat_id = winner.chat_id)
        self.server.bot.send_message(text = f"In the arena you fought {winner.name} and lost the battle", chat_id = loser.chat_id)
        return None

    def process(self):

        print("Processing Arena...")

        to_remove = []
        self.timestamp0 = time.time()       # Marca um tempo de referência novo.
        deltat = self.timestamp0 - self.timestamp
        for arena_lvl in self.arena_players:
            for chat_id, arena_player in self.arena_players[arena_lvl].items():
                print((chat_id, arena_lvl))
                arena_player["rem_enctime"] -= deltat
                if arena_player["rem_enctime"] <= 0:
                    try:
                        player_list = list(self.arena_players[arena_lvl])
                        player_list.remove(chat_id)
                        if len(player_list) >= 1:
                            opponent_id = rd.choice(player_list)
                            jog1 = arena_player["player"]
                            jog2 = self.arena_players[arena_lvl][opponent_id]["player"]
                            self.player_battle(jog1, jog2)
                            to_remove.extend(self.check_death(jog1))
                            to_remove.extend(self.check_death(jog2))
                    except Exception:
                        traceback.print_exc()
                    arena_player["rem_enctime"] = self.encounter_time

        for player in to_remove:
            if player.pt_code:
                self.player_comms.leave_party_comm(player, "yes")
                player.reset_stats()
            self.remove_from_arena(player)
        self.timestamp = time.time()
