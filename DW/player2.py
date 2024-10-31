###########################################
#  Classes que definem um jogador         #
#  Inclui a classe base e as específicas  #
###########################################

from emoji import emojize
import random as rd
import bot

# Classe base
class Player:
    # classe para os membros
    class Limb:
        # state_strings = lista de strings
        # health = int
        # name = string
        def __init__(self, state_strings, health, name):
            self.health = health
            self.name = name
            self.states = []
            health_icons = [
                emojize(":cross_mark:"),
                emojize(":red_heart:"),
                emojize(":yellow_heart::yellow_heart:"),
                emojize(":green_heart::green_heart::green_heart:")
            ]
            for i in range(0, len(state_strings)):
                self.states.append(state_strings[i] + " " + health_icons[i])

    class BuffManager:
        def __init__(self):
            self.states_list = [emojize(":zzz: Natural :zzz:"),
                                emojize(":pile_of_poo: Slightly :pile_of_poo:"),
                                emojize(":OK_hand: Normally :OK_hand:"),
                                emojize(":flexed_biceps: Strongly :flexed_biceps:"),
                                emojize(":angry_face_with_horns: Satanic :angry_face_with_horns:"),
                                emojize(":smiling_face_with_halo: Godly :smiling_face_with_halo:"),
                                emojize(":bright_button: Cosmic :bright_button:")]
            self.buff_state = 0

    def __init__(self, chat_id, name="nameless"):
        self.bot = bot.TGBot()
        self.chat_id = chat_id
        self.admlevel = 0
        self.vanilla_class = "Unknown"
        self.name = name
        self.atk = 1
        self.defense = 1
        self.level = 1
        self.exp = 0
        self.hp = self.create_normal_limbs()
        self.weapon = None
        self.inventory = []
        self.pokedex = []
        self.stat_multiplier = 1
        self.crit_chance = 20
        self.ap = 0
        self.levels = [0, 4, 64, 144, 384, 600, 2880, 3360, 3840, 4320, 4800, 5280, 12120, 13130, 14140,
                       15150, 16160, 17170, 18180, 19190, 20200, 21210, 21210, 22220, 23230, 24240, 25250,
                       26260, 27270, 28280, 29290, 30300, 31310, 32320, 33330, 34340, 35350, 36360, 37370,
                       38380, 39390, 40400, 56448, 57792, 59136, 60480, 61824, 63168, 64512, 65856, 67200]

        self.bot = bot.TGBot()
        self.is_at_forest = False
        self.is_travelling = False
        self.travelling_loc = ""
        self.travel_time = 0
        self.buff_man = self.BuffManager()

        self.new()

    def new(self):
        self.classe = self.vanilla_class
        self.att_points = {
            "unspent": 0,
            emojize(":crossed_swords: Attack :crossed_swords:"): 0,
            emojize(":shield: Defense :shield:"): 0
        }
        self.actions = {}

    def set_name(self, name):
        self.name = name

    def set_attributes(self, atk, defense, exp, level):
        self.atk = atk
        self.defense = defense
        self.exp = exp
        self.level = level

    def set_hp(self, hp):
        self.hp = hp

    def set_quest(self, questing):
        self.questing = questing

    def set_inventory(self, weapon, inventory, pokedex):
        self.weapon = weapon
        self.inventory = inventory
        self.pokedex = pokedex

    def set_adm(self, level):
        self.admlevel = level

    def new_from_player(self, player):
        self.set_name(player.name)
        self.set_attributes(player.atk, player.defense, player.exp, player.level)
        self.set_hp(player.hp)
        self.set_inventory(player.weapon, player.inventory, player.pokedex)
        self.admlevel = player.admlevel
        self.buff_man = player.buff_man
        for att, pts in self.att_points.items():
            self.att_points[att] = 0
        self.att_points["unspent"] = player.level - 1

    def clone_player(self, player):
        self.set_name(player.name)
        self.set_attributes(player.atk, player.defense, player.exp, player.level)
        self.set_hp(player.hp)
        self.set_inventory(player.weapon, player.inventory, player.pokedex)
        self.buff_man = player.buff_man
        self.admlevel = player.admlevel

    def create_normal_limbs(self):
        arm_states = ["torn apart", "broken", "bruised", "fine"]
        left_arm = self.Limb(arm_states, 3, emojize("left arm :flexed_biceps:"))
        right_arm = self.Limb(arm_states, 3, emojize("right arm :flexed_biceps:"))

        chest_states = ["dilacerated", "broken", "bruised", "fine"]
        chest = self.Limb(chest_states, 3, emojize("chest"))

        belly_states = ["cut open", "broken", "bruised", "fine"]
        belly = self.Limb(belly_states, 3, emojize("belly"))

        head_states = ["smashed", "broken", "bruised", "fine"]
        head = self.Limb(head_states, 3, emojize("head :grinning_face:"))

        leg_states = arm_states
        right_leg = self.Limb(leg_states, 3, emojize("right leg"))
        left_leg = self.Limb(leg_states, 3, emojize("left leg"))

        body = []
        body.append(left_arm)
        body.append(right_arm)
        body.append(left_leg)
        body.append(right_leg)
        body.append(chest)
        body.append(belly)
        body.append(head)

        return body

    def random_damaged_limb_index(self, hp):
        limb_i = -1
        damaged_limbs = []
        for i in range(0, len(hp)):
            if hp[i].health < 3:
                damaged_limbs.append(i)

        if len(damaged_limbs) > 0:
            limb_i = damaged_limbs[rd.randint(0, len(damaged_limbs) - 1)]

        return limb_i

    def random_live_limb_index(self, hp):
        limb_i = -1
        live_limbs = []
        for i in range(0, len(hp)):
            if hp[i].health > 0:
                live_limbs.append(i)

        if len(live_limbs) > 0:
            limb_i = live_limbs[rd.randint(0, len(live_limbs) - 1)]

        return limb_i

    def calc_attributes(self):
        self.atk = self.level + self.att_points[emojize(":crossed_swords: Attack :crossed_swords:")]*(self.buff_man.buff_state + 1)
        self.defense = self.level + self.att_points[emojize(":shield: Defense :shield:")]*(self.buff_man.buff_state + 1)
        if self.weapon:
            self.atk += self.weapon.atributos[0]*(self.buff_man.buff_state + 1)
            self.defense += self.weapon.atributos[1]*(self.buff_man.buff_state + 1)

    def get_stats_string(self):
        s = self.get_basic_stats_string()
        return s

    def get_basic_stats_string(self):
        self.calc_attributes()

        weap_name = "None"
        weap_atk = 0
        weap_def = 0
        if self.weapon:
            weap_name = self.weapon.name
            weap_atk = self.weapon.atributos[0]
            weap_def = self.weapon.atributos[1]
        s = (f"{self.name}\n\n"
             f"Attack: {self.atk}:crossed_swords:\n"
             f"Defense: {self.defense}:shield:\n"
             f"Level: {self.level}:up_arrow:\n"
             f"Exp: {self.exp}/{self.levels[self.level]}:TOP_arrow:\n"
             f"Talent points : {self.att_points['unspent']}\n\n"
             f"Class: {self.classe}\n"
             f"Equipped weapon:\n*{weap_name}* :crossed_swords:"
             f"{weap_atk} :shield:{weap_def}\n\n"
             f"Buff: {self.buff_man.states_list[self.buff_man.buff_state]}\n\n")

        return s

    def take_damage(self, dmg=1):
        limb_i = self.random_live_limb_index(self.hp)
        if limb_i > -1:
            self.hp[limb_i].health -= dmg
            return limb_i
        else:
            return -1  # Diz que o jogador morreu, a floresta então apaga ele e tals

    def reset_stats(self):
        self.hp = self.create_normal_limbs()
        self.ap = 0
        self.buff_man.buff_state = 0
        self.calc_attributes()

    def check_level_up(self):
        return (self.exp >= self.levels[self.level])  # or self.level == self.server.levelcap)

    def not_enough_ap(self):
        print("Not enough will to live!")

    def print_self_coms(self):
        text = "You don't have any class! (Yet.)"
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def dg_coms(self):
        text = "You don't have any class! (Yet.)\n\n"
        return text


# Classe Knight, derivada de Player
class Knight(Player):
    # Redefinimos somente algumas coisas, e definimos funções específicas
    def new(self):
        self.classe = "Knight"
        self.ap = 3
        self.att_points = {
            "unspent": 0,
            emojize(":crossed_swords: Critical chance :crossed_swords:"): 0,
            emojize(":crossed_swords: Weapon strength boost :crossed_swords:"): 0
        }
        self.actions = {"/self_heal": self.self_heal}

    def calc_attributes(self):
        max_crit_pts = 9
        over_crit = self.att_points[emojize(":crossed_swords: Critical chance :crossed_swords:")] - max_crit_pts
        if over_crit > 0:  # Só por segurança
            self.crit_chance = max_crit_pts
            self.stat_multiplier = 1 + 0.2*(self.att_points[emojize(":crossed_swords: Weapon strength boost :crossed_swords:")] + over_crit)
        else:
            self.crit_chance = self.att_points[emojize(":crossed_swords: Critical chance :crossed_swords:")]
            self.stat_multiplier = 1 + 0.2*self.att_points[emojize(":crossed_swords: Weapon strength boost :crossed_swords:")]

        if self.weapon:
            self.atk = round(self.weapon.atributos[0]*self.stat_multiplier)*(self.buff_man.buff_state + 1)
            self.defense = round(self.weapon.atributos[1]*self.stat_multiplier)*(self.buff_man.buff_state + 1)
        else:
            self.atk = round(self.level*self.stat_multiplier)*(self.buff_man.buff_state + 1)
            self.defense = round(self.level*self.stat_multiplier)*(self.buff_man.buff_state + 1)

    def reset_stats(self):
        self.hp = self.create_normal_limbs()
        self.ap = 3
        self.buff_man.buff_state = 0
        self.calc_attributes()

    def not_enough_ap(self):
        text = "You tried your best to heal your wounds, but your brain is hurting and you don't remember how to make some bandages."
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def self_heal(self):
        if self.ap > 0:
            self.heal_random_limb()
        else:
            self.not_enough_ap()

    def heal_random_limb(self):
        limb_i = self.random_damaged_limb_index(self.hp)
        if limb_i > -1:
            self.hp[limb_i].health += 1
            self.ap -= 1
            text = f"You heal {self.hp[limb_i].name}"
            self.bot.send_message(text=text, chat_id=self.chat_id)
        else:
            text = "You wanted so hard to heal your limbs, but there was nothing to heal."
            self.bot.send_message(text=text, chat_id=self.chat_id)

    def get_stats_string(self):
        s = self.get_basic_stats_string()
        crit_perc = round(100/(20 - self.crit_chance), 2)
        s += (f"Stamina: {self.ap}/3\n"
              f"Critical chance: {crit_perc:0.2f}%\n"
              f"Weapon strength boost: {100*self.stat_multiplier}%\n\n")

        return s

    def print_self_coms(self):
        s = "You're a weapon on a stick, the only ability you know is a poor self healing. To do so, /self_heal"
        self.bot.send_message(text=s, chat_id=self.chat_id)

    def dg_coms(self):
        s = "You're a weapon on a stick, the only ability you know is a poor self healing. To do so, /self_heal\n\n"
        return s


# Classe Druid, derivada de Player
class Druid(Player):
    # Redefinimos somente algumas coisas, e definimos funções específicas
    def new(self):
        self.classe = "Druid"
        self.ap = 5
        self.att_points = {
            "unspent": 0,
            emojize(":wolf_face: Max. tamed beasts :wolf_face:"): 0,
            emojize(":dizzy: Max. Mana :dizzy:"): 0
        }
        self.actions = {"/heal": self.heal, "/tame": self.tame}
        self.max_mana = 5
        self.tamed_beasts = []
        self.max_tamed_beasts = 1
        self.beast_in_stack = None

    def calc_attributes(self):
        actual_points = round(self.att_points[emojize(":wolf_face: Max. tamed beasts :wolf_face:")]/3)
        self.max_tamed_beasts = 1 + actual_points
        self.max_mana = 5 + self.att_points[emojize(":dizzy: Max. Mana :dizzy:")]

        beasts_attack = 0
        beasts_defense = 0
        if len(self.tamed_beasts) > 0:
            for besta in self.tamed_beasts:
                beasts_attack += besta.atk*(self.buff_man.buff_state + 1)
                beasts_defense += besta.defense*(self.buff_man.buff_state + 1)

        if self.weapon:
            self.atk = self.weapon.atributos[0] + beasts_attack
            self.defense = self.weapon.atributos[1] + beasts_defense
        else:
            self.atk = 7 + beasts_attack
            self.defense = 8 + beasts_attack

    def reset_stats(self):
        self.hp = self.create_normal_limbs()
        self.ap = self.max_mana
        self.tamed_beasts = []
        self.beast_in_stack = None
        self.buff_man.buff_state = 0
        self.calc_attributes()

    def not_enough_ap(self):
        text = "You tried, but you are exausted."
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def heal(self):
        if self.ap > 0:
            self.heal_random_limb()
        else:
            self.not_enough_ap()

    def heal_random_limb(self):
        w_limb = -1
        w_limb_health = 3
        for limb_i in range(len(self.hp)):
            if self.hp[limb_i].health < w_limb_health:
                w_limb = limb_i
                w_limb_health = self.hp[limb_i].health

        limb_i = w_limb  # self.random_damaged_limb_index(self.hp)
        if limb_i > -1:
            self.hp[limb_i].health = 3
            self.ap -= 1
            text = f"You succesfully healed your {self.hp[limb_i].name}"
            self.bot.send_message(text=text, chat_id=self.chat_id)
        else:
            text = "You're in perfect health"
            self.bot.send_message(text=text, chat_id=self.chat_id)

    def take_damage(self, dmg=1):
        limb_i = self.random_live_limb_index(self.hp)
        if limb_i > -1:
            self.hp[limb_i].health -= dmg
            dead_beast = self.check_tamed_beast_states()
            if dead_beast:
                return dead_beast
            else:
                return limb_i
        else:
            return -1  # Diz que o jogador morreu, a floresta então apaga ele e tals

    def tame(self):
        if self.beast_in_stack is not None:
            if self.ap > 1:
                self.ap -= 2
                if len(self.tamed_beasts) < self.max_tamed_beasts:
                    self.tamed_beasts.append(self.beast_in_stack)
                    self.convert_beast_to_limb_and_append(self.beast_in_stack)
                    text = f"succesfully tamed {self.beast_in_stack.tipo}"
                    self.bot.send_message(text=text, chat_id=self.chat_id)
                    self.beast_in_stack = None
                else:
                    text = "Your power does not support taming more beasts"
                    self.bot.send_message(text=text, chat_id=self.chat_id)
            else:
                self.not_enough_ap()

        else:
            text = "No tamable beasts nearby"
            self.bot.send_message(text=text, chat_id=self.chat_id)

    def get_stats_string(self):
        s = self.get_basic_stats_string()
        s += (f"Mana: {self.ap}/{self.max_mana}\n"
              f"Max. tamed beasts: {self.max_tamed_beasts}\n\n")

        return s

    def print_self_coms(self):
        s = "Choose an ability to use:\n\n"
        beast = self.beast_in_stack
        b_str = "None"
        if beast is not None:
            b_str = self.beast_in_stack.tipo
        s += f"/tame Beast nearby: {b_str}\n"
        s += f"/heal Heals worst limb"

        self.bot.send_message(text=s, chat_id=self.chat_id)

    def dg_coms(self):
        s = "Choose an ability to use:\n\n"
        s += f"/heal Heals worst limb \n\n"

        return s

    def convert_beast_to_limb_and_append(self, beast):
        beast_states = ["gone", "heavily injured", "injured", "fine"]
        newlimb = Player.Limb(beast_states, 3, beast.tipo)
        self.hp.append(newlimb)

    def check_tamed_beast_states(self):
        for i in range(7, len(self.hp)):
            if self.hp[i].health == 0:
                b_name = self.hp[i].name
                del self.hp[i]
                return b_name

        return False


class Explorer(Player):
    # Redefinimos somente algumas coisas, e definimos funções específicas
    def new(self):
        self.classe = "Explorer"
        self.ap = 10
        self.att_points = {
            "unspent": 0,
            emojize(":game_die: Rare chance :game_die:"): 0,
            emojize(":warning: More encounters :warning:"): 0
        }
        self.actions = {"/heal": self.heal}
        self.prob_boost = 1
        self.enc_time_multiplier = 1
        self.travel_book = []
        self.ap = 3

    def calc_attributes(self):
        self.prob_boost = self.att_points[emojize(":game_die: Rare chance :game_die:")]*(self.buff_man.buff_state + 1)
        self.enc_time_multiplier = 1+0.1*self.att_points[emojize(":warning: More encounters :warning:")]

        if self.weapon:
            self.atk = self.weapon.atributos[0]
            self.defense = self.weapon.atributos[1]*(self.buff_man.buff_state + 1)
        else:
            self.atk = 7
            self.defense = 8*(self.buff_man.buff_state + 1)

    def reset_stats(self):
        self.hp = self.create_normal_limbs()
        self.ap = 3
        self.buff_man.buff_state = 0
        self.calc_attributes()

    def not_enough_ap(self):
        text = "You started to hear voices around you. Your hand are sweaty. You need a break, not enought stamina."
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def heal(self):
        if self.ap > 0:
            self.heal_random_limb()
        else:
            self.not_enough_ap()

    def heal_random_limb(self):
        # limb_i = self.random_damaged_limb_index(self.hp)
        # if limb_i > -1:
        #     self.hp[limb_i].health += 1
        # else:
        #     print("No limbs are damaged!")
        w_limb = -1
        w_limb_health = 3
        for limb_i in range(len(self.hp)):
            if self.hp[limb_i].health < w_limb_health:
                w_limb = limb_i
                w_limb_health = self.hp[limb_i].health

        limb_i = w_limb  # self.random_damaged_limb_index(self.hp)
        if limb_i > -1:
            self.hp[limb_i].health = 3
            self.ap -= 1
            text = f"You succesfully healed your {self.hp[limb_i].name}"
            self.bot.send_message(text=text, chat_id=self.chat_id)
        else:
            text = "You're in perfect health"
            self.bot.send_message(text=text, chat_id=self.chat_id)

    def add_to_travel_book(self, loc):
        self.travel_book.append(loc)

    def get_stats_string(self):
        s = self.get_basic_stats_string()
        s += (f"Stamina: {self.ap}/3\n"
              f"Rare encounter boost: {self.prob_boost*10}%\n"
              f"Encounter rate: {self.enc_time_multiplier*100:.0f}%\n\n")

        return s

    def create_coms(self, encounter):
        if encounter == "dg":
            self.actions["/g_dg"] = self.travel_to_dg
        elif encounter == "bs":
            self.actions["/g_bs"] = self.travel_to_bs

    def print_self_coms(self):
        text = "Do you want to heal? /heal or.. \n\n"
        text += "Where do you want to go?\n\n"
        for loc in self.travel_book:
            text += f"/g_{loc}\n"
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def dg_coms(self):
        text = "Do you want to heal? /heal \n\n"
        return text

    def travel_to_dg(self):
        print("indo")
        if self.is_at_forest:
            self.is_travelling = True
            print(self.is_travelling)
            self.travel_time = 40*60
            print(self.travel_time)
            self.travelling_loc = "dg"
            print(self.travelling_loc)
            self.bot.send_message(text="You used the map to the dungeon, you will get there in 40 minutes", chat_id=self.chat_id)

        else:
            self.bot.send_message(text="You need to be at the forest to activate the travel book.", chat_id=self.chat_id)

    def travel_to_bs(self):
        print("indo")
        if self.is_at_forest:
            self.is_travelling = True
            self.travel_time = 40#*60
            self.travelling_loc = "bs"
            self.bot.send_message(text="You used the map to the blacksmith, you will get there in 40 minutes", chat_id=self.chat_id)

        else:
            self.bot.send_message(text="You need to be at the forest to activate the travel book.", chat_id=self.chat_id)

    def chegou(self, location):
        print("chegou")
        del self.actions[f"/g_{location}"]
        self.travel_book.remove(location)
        self.is_travelling = False
        self.travel_time = 0
        self.travelling_loc = ""

class Wizard(Player):
    # Redefinimos somente algumas coisas, e definimos funções específicas
    def new(self):
        self.classe = "Wizard"
        self.ap = 5
        self.max_ap = 5
        self.att_points = {
            "unspent": 0,
            emojize(":open_book: Spell Power :open_book:"): 0,
            emojize(":dizzy: Max. Mana :dizzy:"): 0
        }
        self.actions = {"/heal": self.heal, "/buff": self.buff, "/fireball": self.fireball}
        self.buff_difficulty = [1, 5, 10, 16, 23, 31]
        self.spell_power = 0
        self.is_casting = ""

    def calc_buff_difficulty(self):
        self.buff_difficulty = [1, 5, 10, 16, 23, 31]
        numbers = round(self.spell_power/5)
        for i in range(len(self.buff_difficulty)):
            self.buff_difficulty[i] -= numbers
            if self.buff_difficulty[i] < 1:
                self.buff_difficulty[i] = 1
        print(self.buff_difficulty)

    def buff(self):
        self.calc_buff_difficulty()
        if self.ap > 0:
            if self.buff_man.buff_state < len(self.buff_man.states_list) - 1:
                self.ap -= 1
                chance = rd.randint(1, self.buff_difficulty[self.buff_man.buff_state])
                if chance == 1:
                    self.bot.send_message(text="You succesfully buffed yourself", chat_id=self.chat_id)
                    self.buff_man.buff_state += 1
                    self.calc_attributes()
                else:
                    self.bot.send_message(text="You failed to buff yourself", chat_id=self.chat_id)

            else:
                self.bot.send_message(text="You are already the most powerful being, no need to buff", chat_id=self.chat_id)
        else:
            self.not_enough_ap()

    def calc_attributes(self):
        self.max_ap = 5 + self.att_points[emojize(":dizzy: Max. Mana :dizzy:")]
        self.spell_power = self.att_points[emojize(":open_book: Spell Power :open_book:")]

        if self.weapon:
            self.atk = self.weapon.atributos[0]*(self.buff_man.buff_state + 1)
            self.defense = self.weapon.atributos[1]
        else:
            self.atk = 7*(self.buff_man.buff_state + 1)
            self.defense = 8

    def reset_stats(self):
        self.hp = self.create_normal_limbs()
        self.ap = self.max_ap

    def not_enough_ap(self):
        text = "Not enough mana."
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def fireball(self):
        if self.ap > 0:
            self.is_casting = "fireball"
            damage = 50 + 10*self.spell_power
            self.ap -= 1
            text = f"For the next encounter, you will cast a fireball dealing {damage} damage."
            self.bot.send_message(text=text, chat_id=self.chat_id)
        else:
            text = "Not enough mana."
            self.bot.send_message(text=text, chat_id=self.chat_id)

    def heal(self):
        if self.ap > 0:
            self.heal_random_limb()
        else:
            self.not_enough_ap()

    def heal_random_limb(self):
        limb_i = self.random_damaged_limb_index(self.hp)
        if limb_i > -1:
            if (self.buff_man.buff_state + 1) > 3:
                healing_boost = 3
            else:
                healing_boost = (self.buff_man.buff_state + 1)
            self.hp[limb_i].health += healing_boost
            self.ap -= 1
            text = f"Succesfully healed {self.hp[limb_i].name}"
            self.bot.send_message(text=text, chat_id=self.chat_id)
        else:
            text = "You are in perfect health"
            self.bot.send_message(text=text, chat_id=self.chat_id)

    def get_stats_string(self):
        s = self.get_basic_stats_string()
        s += (f"Mana: {self.ap}/{self.max_ap}\n")
        s += f"Spell power: {self.spell_power}\n\n"

        return s

    def print_self_coms(self):
        s = "Choose you spell wisely\n"
        s += "/heal to heal 1 hp\n"
        s += "/buff to buff\n"
        s += "/fireball to cast a fireball"
        self.bot.send_message(text=s, chat_id=self.chat_id)

    def dg_coms(self):
        s = "Choose you spell wisely\n"
        s += "/heal to heal 1 hp\n"
        s += "/buff to buff\n"
        s += "/fireball to cast a fireball\n\n"
        return s
