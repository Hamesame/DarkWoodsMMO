import random as rd
import deep_items

class Potion:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.power = 0
        self.action = None
        self.recipe = {}

    def f_return(self, user):
        pass

    def refresh_stats(self, player):
        prob = self.power*0.01
        if rd.random() < prob:
            player.potion_reset_stats()
        else:
            player.fail_refresh_feedback()

    def recover_mana(self, player):
        prob = self.power*0.02
        if rd.random() < prob:
            player.drink_small_mana_pot()
        else:
            player.fail_mana_feedback()

    def full_health(self, player):
        prob = self.power*0.02
        if rd.random() < prob:
            player.drink_large_pot()
        else:
            player.fail_healing_feedback()

    def full_mana(self, player):
        prob = self.power*0.02
        if rd.random() < prob:
            player.drink_large_mana_pot()
        else:
            player.fail_mana_feedback()

    def heal(self, player):
        prob = self.power*0.02
        if rd.random() < prob:
            player.drink_pot()
        else:
            player.fail_healing_feedback()

    def buff(self, player):
        self.buff_difficulty = [1, 5, 10, 16, 23, 31]
        numbers = round(self.power)
        for i in range(len(self.buff_difficulty)):
            self.buff_difficulty[i] -= numbers
            if self.buff_difficulty[i] < 1:
                self.buff_difficulty[i] = 1
        if player.buff_man.buff_state < len(player.buff_man.states_list) - 1:
            chance = rd.randint(1, self.buff_difficulty[player.buff_man.buff_state])
            if chance == 1:
                player.succesfull_buff_feedback()
                player.buff_man.buff_state += 1
                player.calc_attributes()
            else:
                player.fail_buff_feedback()
        else:
            player.fail_buff_feedback2()

class PotionDB:
    def __init__(self, server):
        self.server = server
        self.Talismandb = deep_items.Talismandb()
        self.potiondb = {}
        self.generate_db()

    def generate_db(self):
        new_pot = Potion("Healing", "1a")
        new_pot.action = new_pot.heal
        new_pot.recipe["fur"] = 1
        new_pot.recipe["chitin"] = 1
        new_pot.recipe["wolf_blood"] = 1
        new_pot.recipe["claw"] = 1
        new_pot.recipe["ligninite"] = 1
        new_pot.recipe["leather"] = 1
        self.potiondb[new_pot.code] = new_pot

        new_pot = Potion("Buff", "1b")
        new_pot.action = new_pot.buff
        new_pot.recipe["feather"] = 1
        new_pot.recipe["gelatine"] = 1
        new_pot.recipe["eye"] = 1
        new_pot.recipe["essence"] = 1
        new_pot.recipe["insect_brain"] = 1
        new_pot.recipe["ice_shards"] = 1
        new_pot.recipe["dark_aura"] = 1
        self.potiondb[new_pot.code] = new_pot

        new_pot = Potion("Camp Teleport", "1c")
        new_pot.action = new_pot.f_return
        new_pot.recipe["feather"] = 1
        new_pot.recipe["chitin"] = 1
        new_pot.recipe["wolf_blood"] = 1
        new_pot.recipe["dragon_eye"] = 1
        new_pot.recipe["cobweb"] = 1
        new_pot.recipe["hydra_blood"] = 1
        self.potiondb[new_pot.code] = new_pot

        new_pot = Potion("Refresh", "1d")
        new_pot.action = new_pot.refresh_stats
        new_pot.recipe["insect_brain"] = 1
        new_pot.recipe["ice_shards"] = 1
        new_pot.recipe["ligninite"] = 1
        new_pot.recipe["leather"] = 1
        new_pot.recipe["dark_aura"] = 1
        new_pot.recipe["dragon_claw"] = 1
        new_pot.recipe["venom_gland"] = 1
        new_pot.recipe["hydra_eye"] = 1
        new_pot.recipe["hard_chitin"] = 1
        self.potiondb[new_pot.code] = new_pot

        new_pot = Potion("Mana Potion", "1e")
        new_pot.action = new_pot.recover_mana
        new_pot.recipe["fur"] = 1
        new_pot.recipe["gelatine"] = 1
        new_pot.recipe["essence"] = 1
        new_pot.recipe["insect_brain"] = 1
        new_pot.recipe["dragon_scale"] = 1
        new_pot.recipe["silk_gland"] = 1
        self.potiondb[new_pot.code] = new_pot

        new_pot = Potion("Full Health", "1f")
        new_pot.action = new_pot.full_health

        new_pot.recipe["ice_shards"] = 3
        new_pot.recipe["ligninite"] = 6
        new_pot.recipe["leather"] = 2
        new_pot.recipe["dark_aura"] = 1
        new_pot.recipe["hydra_claw"] = 1
        new_pot.recipe["hard_chitin"] = 1
        new_pot.recipe["dragon_heart"] = 1
        new_pot.recipe["hydra_heart"] = 1
        new_pot.recipe["giant_snake_louse_heart"] = 1
        new_pot.recipe["giant_centipede_heart"] = 1
        self.potiondb[new_pot.code] = new_pot

        new_pot = Potion("Full Mana", "1g")
        new_pot.action = new_pot.full_mana

        new_pot.recipe["feather"] = 1
        new_pot.recipe["gelatine"] = 1
        new_pot.recipe["eye"] = 1
        new_pot.recipe["essence"] = 1
        new_pot.recipe["ice_shards"] = 1
        new_pot.recipe["dark_aura"] = 1
        new_pot.recipe["repugnatorial_glands"] = 1
        new_pot.recipe["antennae"] = 1
        new_pot.recipe["insect_brain"] = 1
        new_pot.recipe["spider_brain"] = 1
        new_pot.recipe["giant_snake_louse_brain"] = 1
        new_pot.recipe["giant_centipede_brain"] = 1
        self.potiondb[new_pot.code] = new_pot

    def show_recipes(self):
        text = "Here are the recipes:\n\n"
        for pot_code,pot in self.potiondb.items():
            text += f"{pot.name}:\n\n"
            for tal,qty in pot.recipe.items():
                text += f"{self.Talismandb.talismans[tal]} X {qty}\n"
            text += f"To craft, /c_{pot_code}\n\n"
        return text
