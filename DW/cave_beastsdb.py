import os
from emoji import emojize
import random as rd
import copy

class Beast:
    # Tipo = string , (atk, def, hp) = int, name = string, prob = int, is_legendary = bool
    def __init__(self, name="name", prob=1, tier = 1, area_damage = False, good_against = "fur", weak_against = "ice_shards", div_strong = 2, div_weak = 3):
        self.name = name
        self.prob = prob
        self.tier = tier
        self.area_damage = area_damage

        # Originally the probability of winning a fight is 50%

        self.good_against = strong_against      # If the player is equipped with a weapon with this talisman, the beast has  2*(x+1)% increased chance of winning the fight. X is the quality
        self.weak_against = weak_against        # If the player is equipped with a weapon with this talisman, the beast has  2*(x+1)% reduced chance of winning the fight. X is the quality
        self.div_strong = div_strong            # If the player is equipped with a weapon and its attack or defense is divisible by this number, the beast has 15% increased chance of winning. If both, 30%
        self.div_weak = div_weak                # If the player is equipped with a weapon and its attack or defense is divisible by this number, the beast has 15% reduced chance of winning. If both, 30%
        self.new()

    def new(self):
        pass

class BeastDB:
    def __init__(self):
        self.beasts = [
                        Beast(emojize("Dwarf Warrior"), 1, 1, False, "fur", "ice_shards", 2, 3),
                        Beast(emojize("Dwarf Warlock"), 1, 1, False, "eye", "wolf_blood", 11, 7),
                        Beast(emojize("Dwarf Aberration"), 1, 1, False, "dark_aura", "ligninite", 5, 1),
                        Beast(emojize("Dwarf Rogue"), 1, 1, False, "gelatine", "chitin", 9, 8),
                        Beast(emojize("Dwarf Artificer"), 1, 1, False, "claw", "feather", 13, 7),
                        Beast(emojize("Dwarf Bower"), 1, 1, False, "insect_brain", "leather", 17, 2),

                        Beast(emojize("roirraW frawD"), 1, 1, False,"ice_shards" , "fur", 3, 2),
                        Beast(emojize("kcolraW frawD"), 1, 1, False, "wolf_blood", "eye", 7, 11),
                        Beast(emojize("noitarrebA frawD"), 1, 1, False, "ligninite", "dark_aura", 1, 5),
                        Beast(emojize("eugoR frawD"), 1, 1, False, "chitin", "gelatine", 8, 9),
                        Beast(emojize("recifitrA frawD"), 1, 1, False,"feather" , "claw", 7, 13),
                        Beast(emojize("rewoB frawD"), 1, 1, False, "leather", "insect_brain", 2, 17),

                        ]
