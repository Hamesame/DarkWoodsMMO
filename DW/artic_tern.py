import player
import pickle
import items
import os
import playersdb
import helper
import party
from shutil import copyfile
import copy
from emoji import emojize

def load_pickle(file="tmp/blob.dat"):
    '''
        Função que carrega arquivos usando o pickle.

        Parâmetros:

        file (str): arquivo que será carregado. Se ele não existir, ele carregará  os .old
    '''
    blob = None

    if os.path.isfile(file):        # Se o aqruivo existir, caso contrário ele busco os .old
        try:
            with open(file, "rb") as fp:
                blob = pickle.load(fp)
        except Exception as e:          # Se ele não conseguir carregar pq corrompeu ou coisa do gênero, ele pega os .old
            print(e)
            bakfile = file + ".old"
            if os.path.isfile(bakfile):
                try:
                     with open(bakfile, "rb") as fp:
                         blob = pickle.load(fp)
                except Exception as e:          # Se msm assim ele falhar, sei la meu
                    print(e)

    else:
        bakfile = file + ".old"
        if os.path.isfile(bakfile):
            try:
                 with open(bakfile, "rb") as fp:
                     blob = pickle.load(fp)
            except Exception as e:
                print(e)


    return blob

def save_pickle(blob=None, file="tmp/blob.dat"):
    '''
        Função que salva os arquivos

        Parâmetros:

        blob (qqr coisa): Arquivo será salvo.
        file (str): Nome do arquivo em que será salvo.

    '''
    if os.path.isfile(file):
        create_backup(file)        # Cria o backup
    try:
        with open(file, "wb") as fp:
            pickle.dump(blob, fp)       # Salva o arquivo
    except:
        pass

def create_backup(file):
    '''
        Ele literalmente cria um outro arquivo com o msm nome mas com uma extensão .old para caso o jogo morrer no meio do salvamento, ele
         não corromper.
    '''
    dst = file + ".old"
    copyfile(file, dst)

players_not_in_db_counter = 0
players_not_in_db_chat_ids = []

null_parties_counter = 0
null_parties_codes = []

no_member_parties_counter = 0
no_member_parties_codes = []

def new_party_from_old(players_dict, old_party):
    global players_not_in_db_counter
    global players_not_in_db_chat_ids

    global no_member_parties_codes
    global no_member_parties_counter
    chat_ids = []
    for chat_id, jog in old_party.items():
        if isinstance(jog, player.Player):
            if chat_id in players_dict:
                chat_ids.append(chat_id)
            else:
                players_not_in_db_counter += 1
                players_not_in_db_chat_ids.append(chat_id)
    if not chat_ids:
        no_member_parties_codes.append(old_party["code"])
        no_member_parties_counter += 1
        return None
    pt_name = old_party["name"]
    pt_code = old_party["code"]
    dummy_creator = players_dict[chat_ids[0]]


    new_party = party.Party(dummy_creator, pt_code, pt_name)
    chat_ids.remove(chat_ids[0])

    for chat_id in chat_ids:
        new_party.join_pt(players_dict[chat_id])

    for attr in old_party:
        if hasattr(new_party, attr):
            value = old_party[attr]
            setattr(new_party, attr, value)
        elif attr == "pt_inv":
            new_party.inventory = old_party["pt_inv"]
    return new_party

def create_players_and_parties_attr(players_dict, parties_codes):
    global null_parties_codes
    global null_parties_counter

    new_parties_dict = {}
    for pt_code in parties_codes:
        if type(parties_codes[pt_code]) != type(None):
            new_party = new_party_from_old(players_dict, parties_codes[pt_code])
            if new_party:
                new_parties_dict[pt_code] = new_party
        else:
            null_parties_codes.append(pt_code)
            null_parties_counter += 1

    return {**players_dict, **new_parties_dict}

def update_woodplayers(woodplayers, players_and_parties):
    new_woodplayers = {}
    for code in players_and_parties:
        if code in woodplayers:
            new_woodplayers[code] = {}
            new_woodplayers[code]["player"] = players_and_parties[code]
            new_woodplayers[code]["stay_time"] = woodplayers[code]["stay_time"]
            new_woodplayers[code]["rem_time"] = woodplayers[code]["rem_time"]
            new_woodplayers[code]["rem_enctime"] = woodplayers[code]["rem_enctime"]
            new_woodplayers[code]["active"] = woodplayers[code]["active"]
    return new_woodplayers

parties_file = "dbs/parties.dat"
player_file = "dbs/players.dat"
woodplayers_file = "dbs/woods.dat"

new_player_and_parties_file = "dbs/players_and_parties.dat"
new_woodplayers_file = "dbs/woods.dat"


woodplayers = load_pickle(woodplayers_file)
players_dict_from_playersdb = load_pickle(player_file)
old_parties_dict = load_pickle(parties_file)



def main_loop():
    new_players_dict = {}
    for chat,jog in players_dict_from_playersdb.items():
        print(type(jog))
        if type(jog) != type(None):
            # player_example = player.Player("oi")
            # player_list = [f for f in dir(player_example) if not f.startswith("_")]
            # knight_example = player.Knight("oi")
            # knight_list = [f for f in dir(knight_example) if not f.startswith("_")]
            # druid_example = player.Druid("oi")
            # druid_list = [f for f in dir(druid_example) if not f.startswith("_")]
            # explorer_example = player.Explorer("oi")
            # explorer_list = [f for f in dir(explorer_example) if not f.startswith("_")]
            # wizard_example = player.Wizard("oi")
            # wizard_list = [f for f in dir(wizard_example) if not f.startswith("_")]
            # list = []
            # example = None
            example = player.Player(chat)
            if jog.classe == "Unknown":     # Para cada classe, ele recria toto  jogador segundo os parâmetros do jogador

                list = [f for f in dir(example) if not f.startswith("_")]   # E também cria a uma lista com cada parâmtro e método da classe nova

            elif jog.classe == "Knight":

                example = player.Knight(chat)
                #example.new()
                list = [f for f in dir(example) if not f.startswith("_")]
            elif jog.classe == "Druid":

                example = player.Druid(chat)
                #example.new()
                list = [f for f in dir(example) if not f.startswith("_")]
            elif jog.classe == "Explorer":

                example = player.Explorer(chat)
                #example.new()
                list = [f for f in dir(example) if not f.startswith("_")]
            elif jog.classe == "Wizard":

                example = player.Wizard(chat)
                #example.new()
                list = [f for f in dir(example) if not f.startswith("_")]


            # example.new_from_player(jog)
            print(example.att_points)
            for i in list:      # Aqui ele pega os parâmetros do jogador antigo pra setar os do novo. Se prepara
                try:
                    coisa = getattr(jog,i)      # Pega o parâmetro i e chama tudo de coisa
                    if not callable(coisa):     # Se coisa não for um método... (pois métodos não receberão os atributos do jogaddor antigo)
                        if i == "actions":      # Se for actions, coisa é um dicionário de métodos que precisa ser atualizado, caso contrário, ele usa os métodos antigos
                            for code,action in coisa.items():
                                example.actions[code] = getattr(example,action.__name__)
                        else:
                            if i != "levels" and i != "att_points":
                                setattr(example,i,getattr(jog,i))   # Pega o atributo do jogador tal para adicionar no novo que está sendo criado
                except AttributeError:  # Caso ele não encontre tal atributo, quer dizer que ele não tem e ele já foi criado, neste caso ele só vai ignorar
                    pass
            example.att_points['unspent'] = jog.level - 1
            jog = copy.deepcopy(example)    # O jogador de fato é um clone do exemplo pra n bugar nada
            print(jog.att_points)
            arma = jog.weapon
            if arma:
                # jog.weapon.is_shared_and_equipped = False       # Disequipa tudo (pra desequipar jogador com ghost)
                # jog.weapon = None
                example = items.Weapon(emojize("wooden sword"), False, "wd_s", 3, [1, 1])
                list = [f for f in dir(example) if not f.startswith("_")]
                for i in list:
                    try:
                        if not callable(getattr(arma,i)):
                            setattr(example,i,getattr(arma,i))
                    except AttributeError:
                        pass
                    jog.weapon = copy.deepcopy(example)
            new_inv = []
            for arma in jog.inventory:              # Atualiza as armas no inventário do jogador.
                arma.owner = jog.chat_id
                if isinstance(arma, items.dg_map):
                    example = items.dg_map(emojize("Dusty map :world_map:"), 0, "dstmp", 1)
                else:
                    example = items.Weapon(emojize("wooden sword"), False, "wd_s", 3, [1, 1])   # Cria inicialmente uma wooden sword
                    list = [f for f in dir(example) if not f.startswith("_")]
                    for i in list:
                        try:
                            if not callable(getattr(arma,i)):       # E seta os atributos dela de uma forma similar que é feita nos jogadores
                                setattr(example,i,getattr(arma,i))
                        except AttributeError:
                            pass

                new_inv.append(copy.deepcopy(example))
            jog.inventory = new_inv                     # Reseta o inventário do jogador

            new_players_dict[chat] = copy.deepcopy(jog)          # Vai criando o novo dicionário de jogadores

    print(new_players_dict)
    for chat_id, jog in new_players_dict.items():
        print(jog.att_points)
        try:
            print(f"{chat_id} with intelligence {jog.att_points[emojize(':brain: Intelligence :brain:')]}")
        except KeyError:
            print(f"{chat_id} {jog.classe} doesn't have Intelligence attr")
    players_and_parties = create_players_and_parties_attr(new_players_dict, old_parties_dict)
    new_woodplayers = update_woodplayers(woodplayers, players_and_parties)
    save_pickle(players_and_parties, new_player_and_parties_file)
    save_pickle(new_woodplayers, new_woodplayers_file)

main_loop()



# Checando se deu certo --------------------------------------------------------

players_and_parties = load_pickle(new_player_and_parties_file)
new_woodplayers = load_pickle(new_woodplayers_file)

# Codar reassign player in forest.

def print_not_updated_object():
    for code in players_and_parties:
        if not (isinstance(players_and_parties[code], player.Player) or isinstance(players_and_parties[code], party.Party)):
            type_of_thing = type(players_and_parties[code])
            print(f"Code {code} not updated, type is {type_of_thing}")

def check_if_players_from_party_are_same_in_db():
    for code in players_and_parties:
        if code[0] == "/":
            for jog in players_and_parties[code].players:
                if not jog is players_and_parties[jog.chat_id]:
                    print(f"{jog.chat_id} is not the same object as the one in db")

def check_if_the_parties_has_true_players():
    for code in players_and_parties:
        if isinstance(players_and_parties[code], party.Party):
            count = 0
            same_object_players_count = 0
            for jog in players_and_parties[code].players:
                count += 1
                if players_and_parties[jog.chat_id] is jog:
                    same_object_players_count += 1
            if count != same_object_players_count:
                print(f"Found {count - same_object_players_count} not same player object in party {code}")

def check_if_woodplayers_has_true_classes():
    for code in players_and_parties:
        if code in new_woodplayers:
            if not players_and_parties[code] is new_woodplayers[code]["player"]:
                print(f"Object {code} not the same in the forest")
