import player
import party
import copy
import death
import items
import cave_beastsdb
import cave_battle
import deep_items

def isprime(num):
    for x in range(2, num**0.5 + 1):
        if num%x == 0:
            return False
    return True

class CaveEncounters:
    def __init__(self, server):
        self.server = server
        self.CaveBeastsDB = cave_beastsdb.BeastDB()
        self.death = death.Death(server)
        self.Talismandb = deep_items.Talismandb()
        self.chance_to_up_rarity = 0.15
        self.chance_to_drop = 0.3

    def IndividualBattleResponse(self, pl, ind_res):
        limb_dmg = ""
        gain = 10
        if ind_res[0]:
            add_txt = "win"
            gain += 10
            limb_dmg += f" You gained {gain} exp."
        else:
            add_txt = "lose"
            limb_i = self.server.playersdb.players_and_parties[pl.chat_id].take_damage()
            if limb_i != -1:
                if isinstance(limb_i, int):
                    limb_dmg = f"And the {cave_beast.name} followed you as you tried to escape and it, finally reaching you and destroying your {jogador.hp[limb_i].name}. But you gained {gain} exp."
                else:
                    limb_dmg = f"And the {cave_beast.name} followed you as you tried to escape and it, finally reaching you and killed your {limb_i}. But you gained {gain} exp."

            else:
                limb_dmg = f"And the {deep_beast.name} followed you as you tried to escape and it, finally reaching you *finishing your life*. But you gained {gain} exp."
                self.death.die(pl.chat_id)
        self.server.playersdb.players_and_parties[pl.chat_id].exp += gain
        txt = f"In the cavern you found a {cave_beast.name}, having {round(ind_res[1]*100)}% chance of winning, you managed to {add_txt} the fight."
        self.server.bot.send_message(text=txt, chat_id=pl.chat_id, parse_mode='MARKDOWN')


    def normal_beast(self, code):
        user = self.server.playersdb.players_and_parties[code]
        cave_beast = copy.deepcopy(rd.choice(self.CaveBeastsDB.beasts))
        if code.startswith("/"):
            for pl in user.players:
                ind_res = cave_battle.Battle(pl, cave_beast)
                self.IndividualBattleResponse(pl, ind_res)
        else:
            res = cave_battle.Battle(user, cave_beast)
            self.IndividualBattleResponse(user, res)

    def sanc(self, code):
        jog = self.server.playersdb.players_and_parties[code]
        if code.startswith("/"):
            for jog2 in jog.players:
                if jog2.classe == "Unknown":
                    text = "While walking around the caverns you found a strange structure, there you see people meditating, you still dont know how to meditate, so you continued on your journey."
                    self.server.bot.send_message(text=text, chat_id=jog2.chat_id)
                else:
                    jog2.sanctuary()
        else:
            if jog.classe == "Unknown":
                text = "While walking around the caverns you found a strange structure, there you see people meditating, you still dont know how to meditate, so you continued on your journey."
                self.server.bot.send_message(text=text, chat_id=code)
            else:
                jog.sanctuary()


    def plot_msg(self, code):
        text = ("Exausted from walking all day, you decided to rest on the cave walls. You fall asleep and dream of a land where people collectively dream and fights the root of evil together with the power of lucid dreaming. You witness a giant rock with many caves. Each leading to a different dream. One of the cavern walls displays a fading text:")
        code = "ZHJlYW1hcmdib3Q="
        hidden_char = "█"
        random_char_to_show = rd.randint(0, len(code))
        hidden_code = ""
        i = 0
        for ch in code:
            if random_char_to_show == i:
                hidden_code += ch
            else:
                hidden_code += hidden_char
            i += 1
        text += hidden_code + "."
        if code.startswith("/"):
            user = self.server.playersdb.players_and_parties[code]

            self.server.bot.send_message(text=text, chat_id=user.chat_ids)
        else:
            self.server.bot.send_message(text=text, chat_id=code)

    def wep(self, code):
        user = self.server.playersdb.players_and_parties[code]
        cave_player = self.server.cavern_manager.jogs[code]

        # Primeiramente ele cria uma besta baseada no nível de dificuldade
        power_level = int(cave_player.stay_time/(3*3600)) + 1
        avg_stats = power_level*10                              # Status médio que a arma vai ter
        fluc = 0.2                                              # Flutuação que a arma vai ter de stats
        stats = int(avg_stats*(1 + fluc*(1 - 2*rd.random())))   # vários queixos
        attack = int(stats/2)
        while not isprime(attack):
            attack += 1
        defense = attack

        # Ok, temos ataque e defesa, vamos agora selecionar os talismans.

        low_levels = 11         # Número de talimans dropáveis por bestas normais.


        prob1 = 1/4 - 1/(4 + exp((power_level - 94)/20)) # Distribuição de bose-einstein
        t_list = []
        for i in range(power_level):
            if rd.random() < self.chance_to_drop and len(t_list) < 5:
                r_up = 0
                for i in range(power_level):
                    if rd.random() < self.chance_to_up_rarity:    # Se ele conseguir upar a radidade da arma..
                        r_up += 1
                if rd.random() < prob1:
                    r_tal = copy.deepcopy(rd.choice(list(self.Talismandb.talismans.items())[:-2])[1])    # Turdnado
                    if r_tal.rarity + r_up > 6:
                        r_up = 6 - r_tal.rarity
                    r_tal.rarity += r_up
                    for power_name, power in r_tal.powers.items():
                        r_tal.powers[power_name] = power*(r_up + 1)
                    t_list.append(r_tal)
                else:
                    r_tal = copy.deepcopy(rd.choice(list(self.Talismandb.talismans.items())[:low_levels])[1])    # Turdnado
                    if r_tal.rarity + r_up > 6:
                        r_up = 6 - r_tal.rarity
                    r_tal.rarity += r_up
                    for power_name, power in r_tal.powers.items():
                        r_tal.powers[power_name] = power*(r_up + 1)
                    t_list.append(r_tal)
        adjectives = ["Dark", "Sad", "Forgotten", "Obscure", "Forbidden", "Malicious", "Angry", "Vile", "Mad", "Chaotic", "Conniving", "Deceitful", "Cruel", "Malevolent", "Manipulative", "Violent", "Sadistic", "Obnoxious"]
        wep_types = ["Sword", "Staff", "Axe", "Mace", "Warhammer", "Bow", "Khopesh", "Club", "Ppear", "Dagger", "Flamethrower", "Shield", 'Kpinga', "Chakram", "Katar", "Zhua"]
        connectors = ["of"]
        name = self.server.helper.randomnamegenerator(min(power_level + 1, 20))
        adj = rd.choice(adjectives)
        w_type = rd.choice(wep_types)
        w_name = f"{adj} {w_type} {rd.choice(connectors)} {name}"
        description = f"Some {w_type} found at the caverns. It is {adj} and you see inscriptions on the weapon saying it belong to someone named {name}."
        number = 0
        for arma in user.inventory:

            if arma.ac_code == name:
                number += 1             # Não repetir nomes


        if number: #
            name = name + f"{number}"
        types2 = ["ranged", "melee", "magic"]
        newwep = items.Weapon(w_name, False, name, 1, [attack, defense])
        newwep.description = description
        newwep.type2 = rd.choice(types2)
        newwep.add_talismans(t_list)
        user.inventory.append(newwep)
        if user.pt_code:

            text = f"While wandering in the caverns your party found {w_name} and added to the shared inventory."
            self.server.bot.send_message(text=text, chat_id=user.chat_ids)
        else:
            text = f"While wandering in the caverns you found {w_name} and added to the inventory."
            self.server.bot.send_message(text=text, chat_id=code)

    def blacksmith(self, code):
        if code.startswith("\"):
            self.wep(code)
        else:
            self.server.helper.append_command("start_cave_bs", chat_id)
