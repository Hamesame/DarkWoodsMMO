from numpy import exp
from random import random as rd
from random import randint as randint
from emoji import emojize

class BattleMan:
    def __init__(self, server):
        self.server = server
        self.crit_prob = 0.05
        self.chance_to_steal = 0.25
        self.power_multiplier = 100     # Um multiplicador de poder, pra mudar a dificuldade, e o poder de todo mundo, bast mudar esta variável.

    def battle(self, user_id, beast):
        '''
            Batalha entre o user_id e a besta, retorna a lista de mortos.
        '''

        to_del = []
        print("Started to process the battle.")
        if user_id[0] == "/":
            print(f"Its a party, user_id in self.server.playersdb.players_and_parties: {user_id in self.server.playersdb.players_and_parties}")
            if user_id in self.server.playersdb.players_and_parties:
                for user_id2 in self.server.playersdb.players_and_parties[user_id].chat_ids:
                    print(f"party {user_id}, user_id2: {user_id2}, user_id2 in self.server.deep_forest_manager.jogs: {user_id2 in self.server.deep_forest_manager.jogs}")
                    # if user_id2 in self.server.deep_forest_manager.jogs:
                    print("Executed the individual battle for party!")
                    died = self.individual_battle(user_id2, beast)
                    if died == "dead":
                        self.server.megadb.winners_id.append(user_id)
                        return to_del
                    elif died:
                        to_del.append(user_id2)
            else:
                to_del.append(user_id)
        else:
            print("Executed the individual battle for a player.")
            died = self.individual_battle(user_id, beast)
            if died == "dead":
                self.server.megadb.winners_id.append(user_id)
                return to_del
            elif died:
                to_del.append(user_id)
        return to_del

    def individual_battle(self, user, beast):
        '''
            Recebe o id do usuário e a besta com quem vai lutar.
            Retorna False se alguém morreu
            Retorna True se ngm morreu.
            Retorna 'dead' se a besta morreu.
        '''
        flying = False
        evade_multiplier = 1
        damage_multiplier = 1
        # level = 1 + int(self.server.deep_forest_manager.jogs[user].stay_time/(3*60*60))
        user = self.server.playersdb.players_and_parties[user]
        if user.pt_code:
            code = user.pt_code
        else:
            code = user.chat_id
        level = 1 + int(self.server.deep_forest_manager.jogs[code].stay_time/(3*60*60))
        exp_gained = 0
        for limb, hab in beast.habilities.items():
            if limb in beast.limbs:
                if beast.limbs[limb] == 0:
                    pass
                elif hab == "flying":
                    flying = True
                elif hab == "perception":
                    evade_multiplier += 1
                    damage_multiplier += 1
                elif hab == "standing":
                    evade_multiplier += 1
                elif hab == "damage":
                    damage_multiplier += 1
        extra = False
        if user.weapon:
            if "poison" in user.weapon.powers or "fire" in user.weapon.powers:
                extra = True
        damage_taken = beast.attack*damage_multiplier*self.power_multiplier*level
        # print(f"Beast attack: {beast.attack}")
        # print(f"damage_taken: {damage_taken}")
        x = user.defense/damage_taken
        # print(f"x: {x}")
        damage_chance = exp(-(x/20)**(1/2))*(0.75 + 0.25*flying - 0.25*extra)
        # print(f"Chance to take damage: {damage_chance}")
        # print("--------------")
        taken_damage = False
        if rd() < damage_chance:
            exp_gained += level
            taken_damage = True
            limb_i = user.take_damage()
            if limb_i == -1:
                return True
        else:
            exp_gained += level*2
        hp = 0
        for limb in user.hp:
            hp += limb.health
        if hp < 7:
            text = emojize( f":warning:️ Your health is low! "
                            f"Please heal yourself, "
                            f"request healing or leave the battle! :warning:️" )
            self.server.bot.send_message(text=text, chat_id=user.chat_id)

        defense = beast.attack*evade_multiplier*self.power_multiplier*level

        # print(f"beast attack: {beast.attack}")
        # print(f"defense: {defense}")
        x = defense/user.atk
        # print(f"x: {x}")
        damage_chance = exp(-(x/20)**(1/2))*(0.75 - 0.25*flying + 0.25*extra)
        # print(f"Chance to deal damage: {damage_chance}")
        dealt_damage = False
        dealt_critical = False
        if not user.megabeast_target_limb or not user.megabeast_target_limb in beast.limbs:
            limb = beast.select_live_limb()
            if limb == -1:
                return "dead"
            text = f"You are now targeting the {beast.name}'s {limb}."
            self.server.bot.send_message(text=text, chat_id=user.chat_id)
            user.megabeast_target_limb = beast.select_live_limb()
        limb_h = beast.limbs[user.megabeast_target_limb]
        if limb_h < 1:
            limb = beast.select_live_limb()
            if limb == -1:
                return "dead"
            text = f"You are now targeting the {beast.name}'s {limb}."
            self.server.bot.send_message(text=text, chat_id=user.chat_id)
            user.megabeast_target_limb = beast.select_live_limb()

        # print(self.crit_prob + user.crit_boost)
        if rd() < self.crit_prob + user.crit_boost:
            exp_gained += level
            dealt_critical = True
            limb_h = beast.take_damage(user.megabeast_target_limb)
            self.server.bot.send_message(text=emojize(f"You performed a critical attack :high_voltage:"), chat_id=user.chat_id)
            if user.weapon:
                if "life steal" in user.weapon.powers:
                    for i in range(user.weapon.powers["life steal"]):
                        n = rd()
                        if n < self.chance_to_steal:
                            user.life_steal()
        if limb_h < 1:
            limb = beast.select_live_limb()
            if limb == -1:
                return "dead"
            text = f"You are now targeting the {beast.name}'s {limb}."
            self.server.bot.send_message(text=text, chat_id=user.chat_id)
            user.megabeast_target_limb = beast.select_live_limb()


        if user.classe == "Wizard" and user.is_casting.ready:
            damage = user.is_casting.damage      # Precisa mudar o dano da fireball
            x = defense/damage
            damage_chance = exp(-(x/20)**(1/2))/(2 + flying)
            dealt_fireball = False
            if rd() < damage_chance:
                exp_gained += level*2
                dealt_fireball = True
                limb_h = beast.take_damage(user.megabeast_target_limb)
                s = f"You cast a fireball on {beast.name}'s {user.megabeast_target_limb}."
            else:
                exp_gained += level
                s = f"You tried to cast a fireball on {beast.name}'s {user.megabeast_target_limb}. But you missed the fireball."
            if limb_h < 1:
                limb = beast.select_live_limb()
                if limb == -1:
                    return "dead"
                text = f"You are now targeting the {beast.name}'s {limb}."
                self.server.bot.send_message(text=text, chat_id=user.chat_id)
                user.megabeast_target_limb = beast.select_live_limb()
            user.is_casting.ready = False
            fires = user.spell_power
            for i in range(fires):
                loc = randint(0,len(s))
                s1 = s[:loc]
                s2 = s[loc:]
                s1+=(emojize(":fire:"))
                s = s1+s2
            self.server.bot.send_message(text=s, chat_id=user.chat_id)


        if rd() < damage_chance:
            exp_gained += level*2
            dealt_damage = True
            limb_h = beast.take_damage(user.megabeast_target_limb)
            if user.weapon:
                if "life steal" in user.weapon.powers:
                    for i in range(user.weapon.powers["life steal"]):
                        n = rd()
                        if n < self.chance_to_steal:
                            user.life_steal()
        else:
            exp_gained += level

        if limb_h < 1:
            limb = beast.select_live_limb()
            if limb == -1:
                return "dead"
            text = f"You are now targeting the {beast.name}'s {limb}."
            self.server.bot.send_message(text=text, chat_id=user.chat_id)
            user.megabeast_target_limb = beast.select_live_limb()

        stoopid = ["Haven't", "Have"]
        user.exp += exp_gained
        user_report = emojize(  f"On the last battle, you:\n"
                                f"Gained *{exp_gained}* exp.\n"
                                f"{stoopid[taken_damage]} taken damage.\n"
                                f"{stoopid[dealt_damage]} dealt damage.\n"
                                f"{stoopid[dealt_critical]} dealt critial damage.\n")
        if user.classe == "Wizard" and user.is_casting.ready:
            user_report += f"{stoopid[dealt_fireball]} dealt fireball damage.\n\n"
        else:
            user_report += f"\n"
        hp_emoji = emojize(":green_heart:")
        if hp < 7:
            hp_emoji = emojize(":yellow_heart:")
        if hp < 4:
            hp_emoji = emojize(":red_heart:")
        if hp < 2:
            hp_emoji = emojize(":black_heart:")
        user_report += emojize(f"Health: {hp} {hp_emoji}\n\n")
        user.last_megabeast_report = user_report
        return False
