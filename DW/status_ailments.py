
class StatusAilmentManager:
    '''
    Classe de status negativos. Por hora só temos um status negativo
    associado a localização.
    '''
    def __init__(self):
        self.status = {
        "cold": self.cold,
        "hot": self.hot
        }
        self.debuff_power = 0.1

    def cold(self, player, boost):
        power = 1

        if player.armor:
            if "cold" in player.armor.status_protection:
                power -= player.armor.status_protection["cold"]

        player.atk = round(player.atk * (1 - self.debuff_power * (power + boost)))
        player.defense = round(player.defense * (1 - self.debuff_power * (power + boost)))

    def hot(self, player, boost):
        power = 1

        if player.armor:
            if "hot" in player.armor.status_protection:
                power -= player.armor.status_protection["hot"]

        player.atk = round(player.atk * (1 - self.debuff_power * (power + boost)))
        player.defense = round(player.defense * (1 - self.debuff_power * (power + boost)))
