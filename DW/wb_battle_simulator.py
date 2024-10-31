import numpy as np
import matplotlib.pyplot as plt
from copy import copy

class simulated_player:
    def __init__(self, Player):

        self.avg_time = Player.average_time_between_WB
        self.turn_to_leave = -1
        self.turn_to_enter = self.avg_time/(15*60)
        self.defense = Player.defense
        self.atk = Player.atk
        self.chat = Player.chat_id


def generate_graph(server):

    # The x axis is turns (2880 turns in 1 month)
    fig, ax = plt.subplots( nrows=1, ncols=1 )  # create figure & 1 axis
    x_axis = list(range(2880))
    sim_players = {}
    for chat,pl in server.active_players.items():
        new_pl = simulated_player(server.playersdb.players_and_parties[chat])
        sim_players[chat] = new_pl

    health = [server.World_boss.status["Health"]]
    minions = [server.World_boss.status["Minions"]]
    attacking_players = {}
    attacking_players_numbers = []

    m_atk = server.World_boss.minion_damage
    m_def = server.World_boss.minion_defense
    rec_time = server.World_boss.recovery_time
    r2 = rec_time
    original_rec = server.World_boss.max_recovery_rate
    rec_rate = original_rec
    rec_loss = server.World_boss.recovery_loss_over_time

    for turn in x_axis:
        minions.append(minions[turn])
        health.append(health[turn])
        attacking_players_numbers.append(len(attacking_players))
        rec_rate = max(0,rec_rate-rec_loss)
        r2 -= 1
        if r2 == 0:
            r2 = rec_time
            minions[turn+1] = min(server.World_boss.Max_Minions, minions[turn+1]+rec_rate*rec_time)
        if attacking_players:
            to_rem = []
            for chat,pl in attacking_players.items():
                if minions[turn]:
                    minions[turn+1] = max(0, minions[turn+1] - pl.atk/m_def)
                    if pl.turn_to_leave == -1:
                        pl.turn_to_leave = turn + 21/np.exp(-(pl.defense/m_atk)**(1/3))

                    if turn > pl.turn_to_leave:
                        to_rem.append(pl.chat)
                        sim_players[pl.chat].turn_to_enter = turn + pl.avg_time/(15*60)
                else:
                    pl.turn_to_leave += 1
                    health[turn+1] = max(0, health[turn+1] - pl.atk)
                    rec_rate = original_rec
            for chat in to_rem:
                del attacking_players[chat]
        for chat,pl in sim_players.items():
            if pl.turn_to_enter != -1:
                if turn > pl.turn_to_enter:
                    attacking_players[chat] = copy(pl)
                    pl.turn_to_enter = -1
    health = health[:2880]
    health = [float(i)/health[0] for i in health]
    minions = minions[:2880]
    minions = [float(i)/minions[0] for i in minions]
    attacking_players_numbers = attacking_players_numbers[:2880]
    attacking_players_numbers = [float(i)/max(attacking_players_numbers) for i in attacking_players_numbers]
    ax.plot(x_axis, health, label = "health", color = "r")
    ax.plot(x_axis, minions, label = "minions", color = "g")
    ax.plot(x_axis, attacking_players_numbers, label = "players", color = "b")
    fig.savefig('tests/test.png')   # save the figure to file
    plt.close(fig)    # close the figure window
