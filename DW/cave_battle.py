from random import random


def Battle(player, cave_beast):
    prob = 0.5                      # winning probability
    if player.weapon:
        pl_wep = player.weapon
        atk = pl_wep.atributos[0]
        defense = pl_wep.atributos[1]
        for tal_code, tal in pl_wep.talisman.items():
            if tal_code == cave_beast.good_against:
                prob -= 0.02*(1 + tal.rarity)
            elif tal_code == cave_beast.weak_against:
                prob += 0.02*(1 + tal.rarity)
    else:
        atk = pl.atk
        defense = pl.defense


    if atk%cave_beast.div_strong == 0:
        prob -= 0.15
    if defense%cave_beast.div_strong == 0:
        prob -= 0.15
    if atk%cave_beast.div_weak == 0:
        prob += 0.15
    if defense%cave_beast.div_weak == 0:
        prob += 0.15

    victory = random() < prob

    if victory and player.weapon:
        if "life steal" in player.weapon.powers:
            for i in range(player.weapon.powers["life steal"]):
                if random() < 0.1:
                    player.life_steal()
    return (victory, prob):
