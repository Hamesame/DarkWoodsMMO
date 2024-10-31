class Powers:
    def __init__(self, server):
        self.server = server
        self.coisas = {
            "life steal": self.lifesteal,
            "boost str": self.str_boost,
            "boost int": self.int_boost,
            "boost dex": self.dex_boost,
            "fire": self.fire,
            "wep damage": self.damage,
            "wep defense": self.defense,
            "rebalance defense": self.rebalance_defense,
            "rebalance attack": self.rebalance_attack,
            "death evasion": self.evade_death,

            }

    def evade_death(self, user):
        pass

    def fire(self, opponent):
        pass

    def damage(self, weapon):
        pass

    def rebalance_attack(self, weapon):
        pass

    def defense(self, weapon):
        pass

    def rebalance_defense(self, weapon):
        pass

    def lifesteal(self, user):
        pass

    def str_boost(self, user):
        pass

    def int_boost(self, user):
        pass

    def dex_boost(self, user):
        pass
