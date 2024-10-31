import battle2 as battle
import player
import random as rd
import beastsdb

class DeepBattleMan:
    def __init__(self, server):
        self.server = server
        self.battle_man = battle.BattleMan(server)
        self.chance_to_steal = 0.1

    def b_battle(self, user, deep_beast):
        atk_mult = 1
        def_mult = 1
        hp_mult = 1
        if "evasion" in deep_beast.powers:
            atk_mult += deep_beast.powers["evasion"]
        if "hard skin" in deep_beast.powers:
            def_mult += deep_beast.powers["hard skin"]
        if "life steal" in deep_beast.powers:
            hp_mult += deep_beast.powers["life steal"]
        # if not user.pt_code:
        #     # Temporário. primeiro vou testar isso.
        #     if user.weapon and "fire" in user.weapon.powers:
        #         hp_mult = hp_mult/(1 + user.weapon.powers["fire"])
        #     if user.weapon and "poison" in user.weapon.powers:
        #         hp_mult = hp_mult/(1 + user.weapon.powers["poison"])

        # print(f"atk: {deep_beast.stats*atk_mult}, def: {deep_beast.stats*def_mult}, health: {deep_beast.stats*hp_mult/30}")
        new_b = beastsdb.Beast(deep_beast.name, deep_beast.stats*atk_mult, deep_beast.stats*def_mult, deep_beast.stats*hp_mult/50, "", 1, False, 1, True)


        bres =  self.battle_man.battle(user, new_b)
        if bres == -1:
            if isinstance(user, player.Player):
                if user.classe == "Druid":

                    user.beast_in_stack = new_b
                if user.weapon:
                    if "life steal" in user.weapon.powers:
                        print(f"Life steal: {user.weapon.powers['life steal']}")
                        for i in range(user.weapon.powers["life steal"]):
                            n = rd.random()
                            if n < self.chance_to_steal:
                                user.life_steal()
            else:
                for jog in user.players:
                    if jog.classe == "Druid":

                        jog.beast_in_stack = new_b
                    if jog.weapon:
                        if "life steal" in jog.weapon.powers:
                            print(f"Life steal: {jog.weapon.powers['life steal']}")
                            for i in range(jog.weapon.powers["life steal"]):
                                n = rd.random()
                                if n < self.chance_to_steal:
                                    jog.life_steal()
        return bres


    def battle(self, user, user2):
        bres =  self.battle_man.battle(user, user2)

        if bres == -1:
            winner = user
        else:
            winner = user2
        if isinstance(winner, player.Player):
            if winner.weapon:
                if "life steal" in winner.weapon.powers:
                    for i in range(winner.weapon.powers["life steal"]):
                        n = rd.random()
                        if n < self.chance_to_steal:
                            winner.life_steal()
        else:
            for chat,jog in winner.players.items():
                if jog.weapon:
                    if "life steal" in jog.weapon.powers:
                        for i in range(jog.weapon.powers["life steal"]):
                            n = rd.random()
                            if n < self.chance_to_steal:
                                jog.life_steal()

        return bres
