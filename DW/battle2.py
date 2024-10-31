import random as rd
import math
import bot
import player
import party
import numpy as np
from emoji import emojize

class BattleMan:
    def __init__(self, server):
        self.bot = bot.TGBot()
        self.server = server
        self.max_turns = 10
        self.original_hit_prob = 0.25
        self.hit_buff = 0.1
        self.crit_prob = 0.05
        self.chance_to_steal = 0.1

    def calc_player_hp(self, pl):
        player_hp = 0
        for limb in pl.hp:
            player_hp += limb.health
        player_hp = round(player_hp*pl.defense/4)

        return player_hp

    def calc_win_prob(self, Ba, Bd, d, a):
        '''
            Calcula a probabilidade de ganhar uma batalha.

            Parameters:
            Ba: Beast Attack
            Bd: Beast Defense
            d: Player defense
            a: Player attack
        '''
        Bd = max(Bd, 1)
        Ba = max(Ba, 1)
        a = max(a, 1)
        d = max(d, 1)
        # print("Calculating battle:\n")
        # print(f"Beast attack: {Ba}\n")
        # print(f"Beast defense: {Bd}\n")
        # print(f"player defense: {d}\n")
        # print(f"player attack: {a}\n\n")
        # print(f"player attack comparison to beast defense prob: {0.45/(np.exp(-(4.2*a-4*Bd/21)/(Bd/21))+1)}\n")
        # print(f"player defense comparison to beast attack prob: {0.45/(np.exp(-(4.2*d/21-4*Ba)/(Ba))+1)}\n")
        #
        # print(f"Total win prob: {0.45/(np.exp(-(4.2*a-4*Bd/21)/(Bd/21))+1) + 0.45/(np.exp(-(4.2*d/21-4*Ba)/(Ba))+1)}\n")

        return 0.45/(np.exp(-(4.2*a-4*Bd/21)/(Bd/21))+1) + 0.45/(np.exp(-(4.2*d/21-4*Ba)/(Ba))+1)

    def battle(self, obj1, obj2):
        obj1_type = ""
        obj2_type = ""
        '''
            Função que calcula a batalha genérica entre 2 objetos, os objetos podendo ser jogadores, bestas ou parties.

            Retorna -1 se o obj1 ganhou e 1 se o obj2 ganhou.

            Parâmetros:
                obj1: player, party ou beast
                obj2: player, party ou beast
        '''
        if isinstance(obj1, party.Party):
            obj1_type = "party"
        elif isinstance(obj1, player.Player):
            obj1_type = "player"
        else:
            obj1_type = "beast"

        if isinstance(obj2, party.Party):
            obj2_type = "party"
        elif isinstance(obj2, player.Player):
            obj2_type = "player"
        else:
            obj2_type = "beast"

        if obj1_type == "party":
            if obj2_type == "party":
                return self.battle_pt_vs_pt(obj1, obj2)
            elif obj2_type == "player":
                return self.battle_pt_vs_player(obj1, obj2)
            else:
                return self.battle_pt_vs_beast(obj1, obj2)
        elif obj1_type == "player":
            if obj2_type == "party":
                return self.battle_pt_vs_player(obj2, obj1)*(-1)
            elif obj2_type == "player":
                return self.battle_player_vs_player(obj1, obj2)
            else:
                return self.battle_player_vs_beast(obj1, obj2)
        else:
            if obj2_type == "party":
                return self.battle_pt_vs_beast(obj2, obj1)*(-1)
            elif obj2_type == "player":
                return self.battle_player_vs_beast(obj2, obj1)*(-1)
            # Não existe beast vs beast

    def battle_player_vs_beast(self, pl, beast):
        '''
            Função que recebe um jogador pl e uma besta beast e calcula quem vence a batalha.

            Parâmetros:
                pl: Player
                beast: Beast
        '''
        # print("---------------\nEntrou numa batalha de jogador\n\n")
        beast_hp = round(beast.hp*beast.defense/4)
        # print(f"Beast hp: {beast_hp}\n")
        if pl.weapon:
            if "fire" in pl.weapon.powers:
                beast_hp = beast_hp/(pl.weapon.powers["fire"]*0.1 + 1)
            if "poison" in pl.weapon.powers:
                beast_hp = beast_hp/(pl.weapon.powers["poison"]*0.1 + 1)
        # print(f"final Beast hp: {beast_hp}\n")
        player_hp = self.calc_player_hp(pl)
        # print(f"Player hp: {player_hp}")
        turn = 0

        player_crits = 0
        beast_crits = 0
        # while beast_hp > 0 and player_hp > 0 and turn < self.max_turns:
        #     turn += 1
        #     if pl.classe == "Wizard" and pl.is_casting.ready:
        #         beast_hp -= pl.is_casting.damage      # Precisa mudar o dano da fireball
        #         pl.is_casting.ready = False
        #         s = f"You cast a fireball on {beast.tipo}"
        #         fires = pl.spell_power
        #         for i in range(fires):
        #             loc = rd.randint(0,len(s))
        #             s1 = s[:loc]
        #             s2 = s[loc:]
        #             s1+=(emojize(":fire:"))
        #             s = s1+s2
        #         self.bot.send_message(text=s, chat_id=pl.chat_id)
        #
        #     hit_prob = self.original_hit_prob + (pl.stance == emojize("Agressive :crossed_swords:"))*self.hit_buff
        #     if rd.random() < hit_prob:  # Player turn
        #         crit_prob = self.crit_prob + pl.crit_boost
        #         if rd.random() < crit_prob:
        #             player_crits += 1
        #             beast_hp -= pl.atk*2
        #         else:
        #             beast_hp -= pl.atk
        #
        #     hit_prob = self.original_hit_prob - (pl.stance == emojize("Defensive :shield:"))*self.hit_buff
        #     if rd.random() < hit_prob: # Beast turn
        #         crit_prob = self.crit_prob
        #         if rd.random() < crit_prob:
        #             beast_crits += 1
        #             player_hp -= beast.atk*2
        #         else:
        #             player_hp -= beast.atk
        if pl.classe == "Wizard" and pl.is_casting.ready:
            beast_hp = min(beast_hp - pl.is_casting.damage, 1)      # Precisa mudar o dano da fireball
            pl.is_casting.ready = False
            s = f"You cast a fireball on {beast.tipo}"
            fires = pl.spell_power
            for i in range(fires):
                loc = -1
                s1 = s[:loc]
                s2 = s[loc:]
                s1+=(emojize(":fire:"))
                s = s1+s2
            self.bot.send_message(text=s, chat_id=pl.chat_id)


        crit_prob = self.crit_prob + pl.crit_boost

        pl_atk = pl.atk
        if rd.random() < crit_prob:
            player_crits = 1
            pl_atk = pl_atk*2
            player_hp = player_hp*2
            # print(f"Critted! atk:{pl_atk} hp:{player_hp}\n")



        prob = self.calc_win_prob(beast.atk, beast_hp, player_hp, pl_atk)
        r_number = rd.random()
        if r_number < prob:
            beast_hp = 0
            # print("Player won")
        else:
            # print("Beast won")
            player_hp = 0

        if player_crits > 0:
            if player_crits == 1:
                self.bot.send_message(text=emojize(f"You performed a critical attack :high_voltage:"), chat_id=pl.chat_id)

            else:
                self.bot.send_message(text=emojize(f"You performed a critical attack :high_voltage: (x {player_crits})"), chat_id=pl.chat_id)
        pl.stance = emojize("Agressive :crossed_swords:")
        if pl.stance == emojize("Agressive :crossed_swords:"):
            if beast_hp <= 0:
                if pl.weapon:
                    print(f"{pl.name} weapon powers: {pl.weapon.powers}")
                    if "life steal" in pl.weapon.powers:
                        print(f"life steal: {pl.weapon.powers['life steal']}")
                        for i in range(pl.weapon.powers["life steal"]):
                            n = rd.random()
                            if n < self.chance_to_steal:
                                pl.life_steal()
                return -1

        # elif pl.stance == emojize("Defensive :shield:"):
        #     if turn == self.max_turns:
        #         if player_hp > beast_hp:
        #             if pl.weapon:
        #                 if "life steal" in pl.weapon.powers:
        #                     for i in range(pl.weapon.powers["life steal"]):
        #                         n = rd.random()
        #                         if n < self.chance_to_steal:
        #                             pl.life_steal()
        #             return -1

        if player_hp <= 0:
            if pl.buff_man.buff_state > 0:
                pl.buff_man.buff_state -= 1
                self.bot.send_message(text = "You lost a buff.", chat_id = pl.chat_id)
            return 1

        return 0


    def battle_player_vs_player(self, pl1, pl2):
        '''
            Função que recebe um jogador pl e uma besta beast e calcula quem vence a batalha.

            Parâmetros:
                pl: Player
                beast: Beast
        '''
        player1_hp = self.calc_player_hp(pl1)
        player2_hp = self.calc_player_hp(pl2)

        if pl1.weapon:
            if "fire" in pl1.weapon.powers:
                player2_hp = player2_hp/pl1.weapon.powers["fire"]
            if "poison" in pl1.weapon.powers:
                player2_hp = player2_hp/pl1.weapon.powers["poison"]

        if pl2.weapon:
            if "fire" in pl2.weapon.powers:
                player1_hp = player2_hp/pl2.weapon.powers["fire"]
            if "poison" in pl2.weapon.powers:
                player1_hp = player1_hp/pl2.weapon.powers["poison"]

        turn = 0

        player1_crits = 0
        player2_crits = 0
        # while player1_hp > 0 and player2_hp > 0 and turn < self.max_turns:
        #     turn += 1
        #     if pl1.classe == "Wizard" and pl1.is_casting.ready:
        #         player2_hp -= pl1.is_casting.damage      # Precisa mudar o dano da fireball
        #         pl1.is_casting.ready = False
        #         s = f"You cast a fireball on {pl2.name}"
        #         fires = pl1.spell_power
        #         for i in range(fires):
        #             loc = rd.randint(0,len(s))
        #             s1 = s[:loc]
        #             s2 = s[loc:]
        #             s1+=(emojize(":fire:"))
        #             s = s1+s2
        #         self.bot.send_message(text=s, chat_id=pl1.chat_id)
        #
        #     hit_prob = self.original_hit_prob + (pl1.stance == emojize("Agressive :crossed_swords:"))*self.hit_buff - (pl2.stance == emojize("Defensive :shield:"))*self.hit_buff
        #     if rd.random() < hit_prob:  # Player turn
        #         crit_prob = self.crit_prob + pl1.crit_boost
        #         if rd.random() < crit_prob:
        #             player1_crits += 1
        #             player2_hp -= pl1.atk*2
        #         else:
        #             player2_hp -= pl1.atk
        #
        #     hit_prob = self.original_hit_prob + (pl2.stance == emojize("Agressive :crossed_swords:")) - (pl1.stance == emojize("Defensive :shield:"))*self.hit_buff
        #     if rd.random() < hit_prob: # Beast turn
        #         crit_prob = self.crit_prob
        #         if rd.random() < crit_prob:
        #             player2_crits += 1
        #             player1_hp -= pl2.atk*2
        #         else:
        #             player1_hp -= pl2.atk

        if pl1.classe == "Wizard" and pl1.is_casting.ready:
            player2_hp = min(player2_hp - pl1.is_casting.damage, 1)      # Precisa mudar o dano da fireball
            pl1.is_casting.ready = False
            s = f"You cast a fireball on {pl2.name}"
            fires = pl1.spell_power
            for i in range(fires):
                loc = -1
                s1 = s[:loc]
                s2 = s[loc:]
                s1+=(emojize(":fire:"))
                s = s1+s2
            self.bot.send_message(text=s, chat_id=pl1.chat_id)
        if pl2.classe == "Wizard" and pl2.is_casting.ready:
            player1_hp = min(player1_hp - pl2.is_casting.damage, 1)      # Precisa mudar o dano da fireball
            pl2.is_casting.ready = False
            s = f"You cast a fireball on {pl1.name}"
            fires = pl2.spell_power
            for i in range(fires):
                loc = -1
                s1 = s[:loc]
                s2 = s[loc:]
                s1+=(emojize(":fire:"))
                s = s1+s2
            self.bot.send_message(text=s, chat_id=pl2.chat_id)

        crit_prob1 = self.crit_prob + pl1.crit_boost
        crit_prob2 = self.crit_prob + pl2.crit_boost

        pl1_atk = pl1.atk
        pl2_atk = pl2.atk
        if rd.random() < crit_prob1:
            player1_crits = 1
            pl1_atk = pl1_atk*2
            player1_hp = player1_hp*2

        if rd.random() < crit_prob2:
            player2_crits = 1
            pl2_atk = pl2_atk*2
            player2_hp = player2_hp*2


        prob = self.calc_win_prob(pl2_atk, player2_hp, player1_hp, pl1_atk)
        r_number = rd.random()
        if r_number < prob:
            player2_hp = 0
        else:
            player1_hp = 0

        if player1_crits > 0:
            if player1_crits == 1:
                self.bot.send_message(text=emojize(f"You performed a critical attack :high_voltage:"), chat_id=pl1.chat_id)
            else:
                self.bot.send_message(text=emojize(f"You performed a critical attack :high_voltage: (x {player1_crits})"), chat_id=pl1.chat_id)

        if player2_crits > 0:
            if player2_crits == 1:
                self.bot.send_message(text=emojize(f"You performed a critical attack :high_voltage:"), chat_id=pl2.chat_id)
            else:
                self.bot.send_message(text=emojize(f"You performed a critical attack :high_voltage: (x {player2_crits})"), chat_id=pl2.chat_id)
        pl1.stance = emojize("Agressive :crossed_swords:")
        pl2.stance = emojize("Agressive :crossed_swords:")
        if pl1.stance == emojize("Agressive :crossed_swords:"):
            if player2_hp <= 0:
                if pl2.buff_man.buff_state > 0:
                    pl2.buff_man.buff_state -= 1
                    self.bot.send_message(text = f"You lost a buff to {pl1.name}.", chat_id = pl2.chat_id)
                    if pl1.buff_man.buff_state < len(pl1.buff_man.states_list) - 1:
                        self.bot.send_message(text = f"You stole a buff from {pl2.name}.", chat_id = pl1.chat_id)
                        pl1.buff_man.buff_state += 1
                if pl1.weapon:
                    if "life steal" in pl1.weapon.powers:
                        for i in range(pl1.weapon.powers["life steal"]):
                            n = rd.random()
                            if n < self.chance_to_steal:
                                pl1.life_steal()
                return -1

        # elif pl1.stance == emojize("Defensive :shield:"):
        #     if turn == self.max_turns:
        #         if player1_hp > player2_hp:
        #             if pl2.buff_man.buff_state > 0:
        #                 pl2.buff_man.buff_state -= 1
        #                 self.bot.send_message(text = f"You lost a buff to {pl1.name}.", chat_id = pl2.chat_id)
        #                 if pl1.buff_man.buff_state < len(pl1.buff_man.states_list) - 1:
        #                     self.bot.send_message(text = f"You stole a buff from {pl2.name}.", chat_id = pl1.chat_id)
        #                     pl1.buff_man.buff_state += 1
        #             if pl1.weapon:
        #                 if "life steal" in pl1.weapon.powers:
        #                     for i in range(pl1.weapon.powers["life steal"]):
        #                         n = rd.random()
        #                         if n < self.chance_to_steal:
        #                             pl1.life_steal()
        #             return -1

        if pl2.stance == emojize("Agressive :crossed_swords:"):
            if player1_hp <= 0:
                if pl1.buff_man.buff_state > 0:
                    pl1.buff_man.buff_state -= 1
                    self.bot.send_message(text = f"You lost a buff to {pl2.name}.", chat_id = pl1.chat_id)
                    if pl2.buff_man.buff_state < len(pl2.buff_man.states_list) - 1:
                        self.bot.send_message(text = f"You stole a buff from {pl1.name}.", chat_id = pl2.chat_id)
                        pl2.buff_man.buff_state += 1
                if pl2.weapon:
                    if "life steal" in pl2.weapon.powers:
                        for i in range(pl2.weapon.powers["life steal"]):
                            n = rd.random()
                            if n < self.chance_to_steal:
                                pl2.life_steal()
                return 1

        # elif pl2.stance == emojize("Defensive :shield:"):
        #     if turn == self.max_turns:
        #         if player2_hp > player1_hp:
        #             if pl1.buff_man.buff_state > 0:
        #                 pl1.buff_man.buff_state -= 1
        #                 self.bot.send_message(text = f"You lost a buff to {pl2.name}.", chat_id = pl1.chat_id)
        #                 if pl2.buff_man.buff_state < len(pl2.buff_man.states_list) - 1:
        #                     self.bot.send_message(text = f"You stole a buff from {pl1.name}.", chat_id = pl2.chat_id)
        #                     pl2.buff_man.buff_state += 1
        #             if pl2.weapon:
        #                 if "life steal" in pl2.weapon.powers:
        #                     for i in range(pl2.weapon.powers["life steal"]):
        #                         n = rd.random()
        #                         if n < self.chance_to_steal:
        #                             pl2.life_steal()
        #             return 1
        return 0

    def battle_pt_vs_player(self, pt, pl):
        result = 0
        for jog in pt.players:
            result = self.battle_player_vs_player(jog, pl)
            if result == -1:
                return -1
        return 1
        # if result < 0:
        #     return -1
        # elif result > 0:
        #     return 1
        # else:
        #     return 0

    def battle_pt_vs_beast(self, pt, beast):
        result = 0
        for jog in pt.players:
            result = self.battle_player_vs_beast(jog, beast)
            if result == -1:
                return -1
        return 1
        # if result < 0:
        #     return -1
        # elif result > 0:
        #     return 1
        # else:
        #     return 0

    def battle_pt_vs_pt(self, pt1, pt2):
        result = 0
        for jog1 in pt1.players:
            for jog2 in pt2.players:
                result += self.battle_player_vs_player(jog1, jog2)
        if result < 0:
            return -1
        elif result > 0:
            return 1
        else:
            return 0
