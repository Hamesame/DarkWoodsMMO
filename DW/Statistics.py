import player
import playersdb
import forest
import helper
# import rpg_revamp
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import random as rd

class FakeServer:
    def __init__(self):
        self.defkb = "oi"
        self.messageman = "oi"
        self.enc_rate_mult = 1
        self.helper = helper.Helper("oi")
        self.playersdb = playersdb.PlayersDB(self)
        self.woods = forest.Woods(self)


fkserv = FakeServer()

coisa = fkserv.woods
jogadores2 = coisa.players

# a_spacing = 100
# a_max_value = 10000#160000
# a_tam = round(a_max_value/a_spacing)
# attack = np.zeros(a_tam)
#
# d_spacing = 100
# d_max_value = 10000#80000
# d_tam = round(d_max_value/d_spacing)
# defense = np.zeros(d_tam)
#
# for chat,jog in jogadores2.items():
#     pl = jog["player"]
#     try:
#         if isinstance(pl,dict):
#             for a,b in pl.items():
#                 if isinstance(b,player.Player):
#                     loc,rest = divmod(b.atk, a_spacing)
#                     attack[loc] += 1
#                     loc,rest = divmod(b.defense, d_spacing)
#                     defense[loc] += 1
#         else:
#
#             loc,rest = divmod(pl.atk, a_spacing)
#             attack[loc] += 1
#             loc,rest = divmod(pl.defense, d_spacing)
#             defense[loc] += 1
#     except:
#         pass
#     # except IndexError():
#     #     print("oi")
#
#
# def func2(t, tau, a):
#     return a*np.exp(-t / tau)
#
#
#
# atks = np.linspace(0,a_max_value,a_tam)
# defs = np.linspace(0,d_max_value,d_tam)
#
# attack_norm = attack/attack[0]
# atks_norm = (atks - atks[0])/(atks[-1] - atks[0])
#
#
# tau_0 = 1
# a_0 = 1
#
# popt2, pcov2 = curve_fit(func2, atks_norm, attack_norm, p0=(tau_0,a_0))
#
# tau4, A = popt2
# tau4 = tau4*atks[-1]
# print(tau4, A)
# attack_fit = func2(atks, tau4, A)
# fig, ax = plt.subplots()
# ax.plot(atks_norm,attack_norm,label = "attack",color = 'r')
# ax.plot(atks_norm,attack_fit,label = "attack fit",color = 'g')
# plt.show()
#
# def_norm = defense/defense[0]
# defs_norm = (defs - defs[0])/(defs[-1] - defs[0])
#
#
# tau_0 = 1
# a_0 = 1
#
# popt2, pcov2 = curve_fit(func2, defs_norm, def_norm, p0=(tau_0,a_0))
#
# tau4, A = popt2
# tau4 = tau4*defs[-1]
# print(tau4, A)
# defense_fit = func2(defs, tau4, A)
# fig, ax = plt.subplots()
# ax.plot(defs_norm,def_norm,label = "attack",color = 'r')
# ax.plot(defs_norm,defense_fit,label = "attack fit",color = 'g')
# plt.show()
#
# fig, ax = plt.subplots()
# ax.plot(atks,attack,label = "attack",color = 'r')
# ax.plot(atks,attack_fit*attack[0],label = "attack fit",color = 'g')
# ax.plot(atks,defense_fit*defense[0],label = "defense fit",color = 'y')
# ax.plot(defs,defense,label = "defense",color = 'b')
#
# ax.set(xlabel='Stats', ylabel='Number of players',
#        title=f'By {a_spacing} for attack and {d_spacing} for defense')
# ax.grid()
#
#
# plt.legend()
# plt.show()

class Fakeplayer:
    def __init__(self, id, attack, defense):
        self.awarness_event = 1
        self.awarness_health = 1
        self.health = 31
        self.defense = defense
        self.attack = attack
        self.id = id
        self.remaining_turns_to_reach = 0
        self.is_hitting = False
        self.ptid = ""

class Fakeparty:
    def __init__(self, id):
        self.players = {}
        self.id = id
        self.remaining_turns_to_reach = 3
        self.is_hitting = False

parties = {}
jogadores = {}
coisa = 0
index = 0
for chat,jog in jogadores2.items():
    pl = jog["player"]
    try:
        if isinstance(pl,dict):
            new_pt = Fakeparty(str(index))
            new_pt.remaining_turns_to_reach = rd.randint(4,125)
            parties[str(index)] = new_pt
            for a,b in pl.items():
                if isinstance(b,player.Player):
                    newplayer = Fakeplayer(str(coisa),b.atk,b.defense)
                    newplayer.awarness_health = rd.uniform(0.8, 0.99)
                    newplayer.awarness_event = rd.uniform(0.8, 0.99)
                    newplayer.ptid = str(index)
                    parties[str(index)].players[coisa] = newplayer
                    coisa+=1
            index+=1
        else:

            newplayer = Fakeplayer(str(coisa), pl.atk,pl.defense)
            newplayer.remaining_turns_to_reach = rd.randint(75,125)
            newplayer.awarness_health = rd.uniform(0.8, 0.99)
            newplayer.awarness_event = rd.uniform(0.8, 0.99)
            jogadores[coisa] = newplayer
            coisa += 1
    except:
        pass

# for i in range(39):
#     new_pt = Fakeparty(str(i))
#     new_pt.remaining_turns_to_reach = rd.randint(4,100)
#     parties[str(i)] = new_pt
#     for j in range(4):
#         newplayer = Fakeplayer(str(coisa),8400,6400)
#         newplayer.ptid = str(i)
#         parties[str(i)].players[coisa] = newplayer
#         coisa += 1
#
# for i in range(55): # 55
#     newplayer = Fakeplayer(str(coisa),8400,6400)
#     newplayer.remaining_turns_to_reach = rd.randint(4,100)
#     jogadores[coisa] = newplayer
#     coisa += 1

class SF:
    def __init__(self):
        self.in_hp = 50e6
        self.hp = self.in_hp
        self.in_minions = 100e3
        self.minions = self.in_minions
        self.minion_attack = 300
        self.minion_defense = 300
        self.time_unit = 15*60          # in seconds
        self.recovery_time = 16
        self.original_recover = 1750
        self.minions_recovered = self.original_recover*self.recovery_time
        self.minion_recovery_loss_over_turn = 12

girassol = SF()

turn = 0
max_time = 28           # in days
hitting = {}
time_to_reach = 3       # in turns
turns = np.linspace(0,2688,2688)
num_hit = np.zeros(2688)
min = np.zeros(2688)
vida = np.zeros(2688)

to_remove = []
to_print = 5


n = 1000
scale_radius = 50
central_surface_density = 100 #I would like this to be the controlling variable, even if it's specification had knock on effects on n.

radius_array = np.random.exponential(scale_radius,(n,1))

while girassol.hp > 0 and turn*girassol.time_unit < max_time*86400:
    girassol.minions_recovered -= girassol.minion_recovery_loss_over_turn*girassol.recovery_time
    if girassol.minions_recovered < girassol.recovery_time:
        girassol.minions_recovered = girassol.recovery_time
    num_hit[turn] = len(hitting)
    min[turn] = girassol.minions*200/girassol.in_minions
    vida[turn] = girassol.hp*200/girassol.in_hp
    turn += 1
    for id, pt in parties.items():
        if not pt.is_hitting:
            pt.remaining_turns_to_reach -= 1
            if pt.remaining_turns_to_reach < 0:
                for id2, pl in pt.players.items():

                    hitting[id2] = pl
                pt.is_hitting = True
    for id, pl in jogadores.items():
        if not pl.is_hitting:
            pl.remaining_turns_to_reach -= 1
            if pl.remaining_turns_to_reach < 0:
                pl.is_hitting = True
                hitting[id] = pl


    for id,pl in hitting.items():
        leave = False
        if girassol.minions:

            dam_prob = np.exp(-(pl.defense/girassol.minion_attack)**(1/3))
            thing = rd.random()
            if dam_prob > thing:
                pl.health -= 1
                healing = rd.randint(4,14)
                dead = rd.random()
                death_prob = 1 - pl.awarness_health
                if pl.health <= healing:
                    if dead < death_prob:
                        pl.attack = 7
                        pl.defense = 8
                    else:
                        leave = True

            killed = round(pl.attack/girassol.minion_defense)
            if killed > girassol.minions:
                girassol.minions = 0
            else:
                girassol.minions -= killed

        else:
            girassol.hp -= pl.attack
            girassol.minions_recovered = girassol.original_recover*girassol.recovery_time



        if leave:
            if pl.ptid:

                parties[pl.ptid].is_hitting = False
                m_sum = 0
                for id2,pl2 in parties[pl.ptid].players.items():
                    pl2.health = 31
                    to_remove.append(id2)

                parties[pl.ptid].remaining_turns_to_reach = round(rd.choice(radius_array)[0])

            else:
                mult = 1/jogadores[id].awarness_event
                jogadores[id].is_hitting = False
                jogadores[id].remaining_turns_to_reach = round(rd.choice(radius_array)[0])
                jogadores[id].health = 31
                to_remove.append(id)
    if turn%girassol.recovery_time == 0:
        girassol.minions += girassol.minions_recovered
        if girassol.minions > girassol.in_minions:
            girassol.minions = girassol.in_minions
    if to_remove:
        for item in to_remove:
            del hitting[item]
    to_remove = []

print(f"Turns = {turn}") # max is 2688
print(f"Weeks = {turn/672}")
print(f"SF hp = {girassol.hp}")

fig, ax = plt.subplots()
ax.plot(turns,num_hit,label = "attacking players",color = 'r')
ax.plot(turns,min,label = "minions (normalized)",color = 'g')
ax.plot(turns,vida,label = "health (normalized)",color = 'k')
ax.set(xlabel='Turns', ylabel='Number of players',
       title=f'Sunflower simulation')
plt.legend()
plt.show()
