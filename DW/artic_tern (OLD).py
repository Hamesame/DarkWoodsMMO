import player2
import pickle
import items
import os

class player:                                            # Define o objeto "jogador"
    def __init__(self, name, atk, defense, level, exp, chat_id, hp, is_questing, pokedex, weapon, inventory, classe):    # Name == string, (atk, defense, level, exp, chat_id) == int, hp == lista de limbs, is_questing == bool, pokedex = lista de bestas
        self.name = name
        self.atk = atk
        self.defense = defense
        self.level = level
        self.exp = exp
        self.chat_id = chat_id
        self.hp = hp
        self.is_questing = is_questing
        self.pokedex = pokedex
        self.weapon = weapon
        self.inventory = inventory
        self.classe = classe

class weapon:                                            # Define a classe arma
    def __init__(self, name, atributos, is_legendary, code):
        self.name = name
        self.atributos = atributos
        self.is_legendary = is_legendary
        self.code = code

class beast:                                    # Define o objeto "besta"
    def __init__(self, tipo, atk, defense, hp, name, is_legendary):        # Tipo == string , (atk, def, hp) == int, name == string, is_legendary == bool
        self.tipo = tipo
        self.atk = atk
        self.defense = defense
        self.hp = hp
        self.name = name
        self.is_legendary = is_legendary

class limb:                    # Define o objeto "membro"
    def __init__(self,states,health,name):    # States == lista de strings, Health == int, name == string
        self.states = states
        self.health = health
        self.name = name



class pokedex:                # Define o objeto que sera usado no bestiário
    def __init__(self,lista):
        self.lista = lista





players = []
try:
    with open("players.txt","rb") as fp:        ##
        players = pickle.load(fp)         #
except:
    with open("backup_players.txt","rb") as fp:
        players = pickle.load(fp)


players_migrated = {}

for jogador in players:
    newplayer = player2.Player(str(jogador.chat_id))
    newplayer.level = jogador.level
    newplayer.name = jogador.name
    newplayer.exp = jogador.exp
    newplayer.att_points["unspent"] = jogador.level - 1
    new_inv = []
    for arma in jogador.inventory:
        new_item = items.Weapon(arma.name, arma.is_legendary, arma.code, 1, arma.atributos)
        new_inv.append(new_item)
    newplayer.inventory = new_inv

    b_list = []
    for besta in jogador.pokedex:
        if besta.is_legendary:
            b_list.append(f"{besta.tipo} named {besta.name}")
        else:
            b_list.append(besta.tipo)
    newplayer.pokedex = b_list

    arma = jogador.weapon
    if arma:
        arma_equipada_nova = items.Weapon(arma.name, arma.is_legendary, arma.code, 1, arma.atributos)
    else:
        arma_equipada_nova = None
    newplayer.weapon = arma_equipada_nova
    newplayer.calc_attributes()

    players_migrated[str(jogador.chat_id)] = newplayer


file = "dbs/players.dat"
if not os.path.exists("dbs/"):
    os.makedirs("dbs/")
try:
    with open(file, "wb") as fp:
        pickle.dump(players_migrated, fp)
except:
    pass
