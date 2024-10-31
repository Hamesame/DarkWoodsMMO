#caller["code"]caller["code"]caller["code"]caller["code"]caller["code"]caller["code"]caller["code"]caller["code"]################################################
# Classe que gerencia as mensagens.            #
# Todas as mensagens do jogo passam por aqui.  #
################################################

# This is the most convoluted file of them all. Was programmed by Paulao. Not even he knows how this works.

# Essencialmente, o MessageMan processa todos as interações do player com o chat bot
# através dos comandos oferecidos a ele. Dessa forma, todas as classes de comandos são
# construídas de forma similar, utilizando funções de mesmo nome e mesmo argumentos,
# mesmo quando elas não serão utilizadas naquela classe de comandos. Assim, algumas
# dessas funções serão vazias para evitar erros.

# O MessageMan trabalha com dois tipos de comandos: dados pelo próprio jogadores e
# comandos internos utilizado pelo código. Por exemplo, em dungeon_comms.py, temos
# um comando interno start_dg. Este comando inicia uma dungeon em duas etapas:
# a primeira é escolhendo uma dungeon para o jogador, perguntando se ele quer ou não
# entrar; a segunda é colocá-lo na dungeon caso a resposta seja sim.

# Por todo o código, será comum termos a mesma função programada para players
# adaptada para parties.

import os
import time
import copy
import bot
import player_comms
import party_comms
import adm_comms
import forest_comms2 as forest_comms
import deep_forest_comms
import blacksmith_comms
import dungeon_comms
import megabeast_comms
import WB_comms
import WB_mountain_comms
import arena_comms2 as arena_comms
import potion_comms
import holy_trees_comms
import shopcomms
# import cave_blacksmith_comms
import mag_mell_comms
import haunt_comms
import shaman_comms
import enchanter_comms
from emoji import demojize
from emoji import emojize
import player
import datetime

class MessageMan:
    def __init__(self, server):
        self.server = server        # server será o jogo inteiro (contendo informações sobre todos jogadores e tudo o que está acontecendo)
        self.bot = bot.TGBot()      # bot do Telegram para receber e enviar mensagens.
        self.timestamp = time.time()    # Marca para calcular intervalos de tempo.
        self.defkb = server.keyboards.class_main_menu_reply_markup
        self.def_wait_time = 1#60
        self.commtrees = [
            player_comms.PlayerComms(server),
            party_comms.PartyComms(server),
            blacksmith_comms.BlacksmithComms(server),
            # cave_blacksmith_comms.CaveBlacksmithComms(server),
            dungeon_comms.DungeonComms(server),
            forest_comms.ForestComms(server),
            deep_forest_comms.DeepForestComms(server),
            adm_comms.ADMComms(server),
            WB_comms.WBComms(server),
            arena_comms.ArenaComms(server),
            megabeast_comms.MegaBeastMan(server),
            potion_comms.PotionComms(server),
            shopcomms.ShopComms(server),
            WB_mountain_comms.WBMountainComms(server),
            mag_mell_comms.MagMellComms(server),
            haunt_comms.HauntComms(server),
            shaman_comms.ShamanComms(server),
            enchanter_comms.EnchanterComms(server),
            holy_trees_comms.HolyTreeComms(server),
        ]       # Lista de todos os comandos utilizados no jogo.

        self.waiting_from = {}      # Contém todos os players (ou parties), separados por chat_id, na qual o BOT está esperando por alguma resposta. Associamos a cada chat_id outro dicionário, onde terá outras informações utilizadas pelo MessageMan. Ver process_message.
        self.comms_file = "dbs/comms.dat"       # O dicionário waiting_from é salvado caso o bot caia, para que todos os comandos não sejam recarregados.
        loaded = self.server.helper.load_pickle(self.comms_file)
        if loaded:
            self.waiting_from = loaded


    # Veja "process_message" antes.
    def update_times(self, chat_id):
        '''
            Cada comando que necessita de uma resposta possui um tempo na qual o player precisa responder.
            update_times é a função que atualiza esses tempos de resposta.
        '''
        to_del = []
        for i in range(len(self.waiting_from[chat_id]["comms"])):       # ver process_message.
            if self.waiting_from[chat_id]["remtimes"][i] != 1:
                deltat = time.time() - self.timestamp       # Calcula o intervalo de tempo entre o tempo atual e o último tempo marcado pelo MessageMan.
                rem_time = self.waiting_from[chat_id]["remtimes"][i] - deltat
                if rem_time == 1:
                    rem_time = 0.999999
                if rem_time <= 0:
                    to_del.append(i)
                    self.exec_to(chat_id, self.waiting_from[chat_id]["comms"][i],
                                 self.waiting_from[chat_id]["internals"][i])        # Ver "exec_to" abaixo.
                else:
                    self.waiting_from[chat_id]["remtimes"][i] = rem_time
        for i in sorted(to_del, reverse=True):
            del self.waiting_from[chat_id]["comms"][i]
            del self.waiting_from[chat_id]["remtimes"][i]
            del self.waiting_from[chat_id]["internals"][i]

        del_chat_id = False
        if len(self.waiting_from[chat_id]["comms"]) == 0:       # Se todos os comandos tiverem sidos processados, o player (ou party) será deletado do waiting_from em "updates_all_times".
            del_chat_id = True
        return del_chat_id

    def update_all_times(self):
        '''
            Função que chama update_times a fim de atualizar todos os tempos de espera de todos os jogadores.
        '''
        to_del = []     # Se o tempo de resposta do player terminar, ele será deletado do waiting_from.
        for chat_id, blah in self.waiting_from.items():
            if self.update_times(chat_id):      # Checa se o player (ou party) deve ser deletado do waiting_from.
                to_del.append(chat_id)
        for chat_id in to_del:
            del self.waiting_from[chat_id]

        self.timestamp = time.time()        # Reseta o timestamp.

    def send_reminder(self):
        pass


    def exec_to(self, chat_id, comm, internal):
        '''
            exec_to executa o método "to" (timeout) encontrada em todas as classes de comandos.
            As funções "to" são respostas dada ao player quando ele não responde o bot.
            Ex: do comando interno start_dg, o player deve responder sim ou não. Caso nada é inserido, a função "to" é ativada em "update_all_times".
        '''
        if internal:
            for commtree in self.commtrees:
                if comm in commtree.internal:
                    if "to2" in dir(commtree):
                        commtree.to2(chat_id)
                    else:
                        commtree.to(chat_id)
                    break
        else:
            for commtree in self.commtrees:
                if comm in commtree.actions:
                    commtree.to(chat_id)
                    break


    def exec_comm(self, caller, comm, arg, internal, caller_id = None):
        '''
            exec_comm é o método que chama a comtree certa de self.comtrees pra executar o comando pedido pelo jogador.

            Parâmetros:
            caller (class): jogador que inseriu um comando;
            comm (str): string contendo o primeiro comando da árvore de comandos inserido pelo jogador;
            arg (str): string contendo o último comando inserido pelo jogador (ou dado pelo comando interno).
            internal (str): string contendo o comando interno.
        '''
        result = False      # result será, ou o valor False, ou um valor int contendo um tempo de espera.
        executed_command = False        # Ao final da função, isto indicará se o comando inserido foi executado ou não.
        if internal:
            for commtree in self.commtrees:
                if comm in commtree.internal:       # Só executa se o comando inserido for válido.
                    executed_command = True
                    if arg is None:
                        result = commtree.internal[comm](caller, caller_id)
                    else:
                        result = commtree.internal[comm](caller, caller_id, *arg)
                    break
        else:
            for commtree in self.commtrees:
                for valid_comm in commtree.actions:

                    if comm.startswith(valid_comm):      # Só executa se o comando inserido for válido.
                #if comm in commtree.actions:
                        if isinstance(commtree, party_comms.PartyComms):
                            is_test = self.bot.token == "12323454356:skjldfhlh2jk13"    # Add test bot token here
                            if is_test:
                                executed_command = True
                                if arg is None:
                                    result = commtree.actions[valid_comm](caller)
                                else:
                                    result = commtree.actions[valid_comm](caller, *arg)
                                break
                            elif not caller.chat_id.startswith("-"):
                                executed_command = True
                                if arg is None:
                                    result = commtree.actions[valid_comm](caller)
                                else:
                                    result = commtree.actions[valid_comm](caller, *arg)
                                break
                            else:
                                text = "You are a group alt. It won't be fair if you could join parties. Any doubts talk to @DWWikiBot."
                                self.bot.send_message(text=text, chat_id=caller.chat_id)
                                result = False
                        else:

                            executed_command = True
                            if arg is None:
                                result = commtree.actions[valid_comm](caller)
                            else:
                                result = commtree.actions[valid_comm](caller, *arg)
                            break
        return executed_command, result


    def dg_exec_comm(self, caller_player, caller, comm, arg, internal):     # parties são dicionários contendo os players. Aqui, caller = party.
        '''
            dg_exec_comm é o exec_comm adaptado para parties no caso em que uma dungeon é encontrada.

            Parâmetros:
            caller_player (class): jogador que inseriu um comando;
            caller (dict): party do jogador que inseriu um comando;
            comm (str): string contendo o primeiro comando da árvore de comandos inserido pelo jogador;
            arg (str): string contendo o último comando inserido pelo jogador (ou dado pelo comando interno).
            internal (str): string contendo o comando interno.
        '''
        result = False
        executed_command = False

        if internal:
            for commtree in self.commtrees:
                if comm in commtree.internal:
                    executed_command = True
                    if arg is None:
                        result = commtree.internal[comm](caller_player, caller)
                    else:
                        result = commtree.internal[comm](caller_player, caller, arg)
                    break
        else:
            for commtree in self.commtrees:
                if comm in commtree.actions:
                    executed_command = True
                    if arg is None:
                        result = commtree.actions[comm](caller_player, caller)
                    else:
                        result = commtree.actions[comm](caller_player, caller, arg)
                    break

        return executed_command, result


    # def process_message(self, msg, caller, caller_player = None, internal=False):
    #     '''
    #         Processa os comandos inseridos pelo player ou pelo próprio programa. Ver exec_comm primeiro.
    #         Aqui é utilizado o waiting_from. Para cada chat_id, associamos um dicionário. Neste dicionário temos
    #         três listas. Indexada por "comms" é a lista contendo todos os comandos inseridos pelo player que foram executados.
    #         Indexada por "remtimes", todos os tempos restantes de cada comando.
    #         Indexada por "internals" todos os comandos internos executados.
    #         Dessa forma, o waiting_from mantém a árvore de comandos na qual o jogador está navegando.
    #
    #         Parâmetros:
    #         caller (class): jogador da party que insere um comando;
    #         msg (str): string contendo o comando inserido pelo jogador;
    #         internal (str): string contendo o comando interno.
    #     '''
    #     a_str = "%d/%m/%Y, %H:%M:%S"        # String que ordena a data em dia/mês/ano e hora:minutos:segundos. Utilizado para printar as interações dos player com o chat bot no console (linha abaixo).
    #     print(demojize(f"{caller.chat_id} ({caller.name})  at {datetime.datetime.now(datetime.timezone(datetime.timedelta(hours = -3))).strftime(a_str)} said: {msg}"))
    #     comm = msg      # msg é o string dado pelo player em forma de comando. Ex: /inv
    #     arg = None      # Setado em None devido ao exec_comm
    #
    #     executed_command, result = self.exec_comm(caller, comm, arg, internal, caller_id = caller_player)
    #     was_waiting = caller.chat_id in self.waiting_from       # chat_id do player na qual o bot está esperando o comando.
    #     # print(self.waiting_from)
    #     if not was_waiting:     # Coloca o player (ou party) no waiting_from caso o comando dele seja o primeiro da árvore de comandos. Ex: /party -> /scoop e /party foi o comando inserido.
    #         self.waiting_from[caller.chat_id] = {}                # TESTE
    #         self.waiting_from[caller.chat_id]["comms"] = [comm]
    #         self.waiting_from[caller.chat_id]["remtimes"] = [int(result)]
    #         self.waiting_from[caller.chat_id]["internals"] = [internal]
    #     elif executed_command:
    #         self.waiting_from[caller.chat_id]["comms"].append(comm)
    #         self.waiting_from[caller.chat_id]["remtimes"].append(int(result))
    #         self.waiting_from[caller.chat_id]["internals"].append(internal)
    #
    #     if not executed_command and was_waiting:      # Se o comando não foi executado, então é provável que ele seja o próximo comando da árvore. Adicionamos o comm na lista e o executaremos como arg abaixo.
    #         comm = self.waiting_from[caller.chat_id]["comms"][-1]
    #         arg = msg       # A mensagem do player é vista como argumento para executar os comandos.
    #         internal = self.waiting_from[caller.chat_id]["internals"][-1]
    #         # print(f"waiting from: {self.waiting_from}")
    #         executed_command, result = self.exec_comm(caller, comm, arg, internal)
    #     elif not executed_command:      # Se nada for executado novamente, o player deu um input inválido ou esta tentando se juntar a uma party via forward direto do código da party.
    #         was_direct_join = False
    #         try:
    #             was_direct_join = self.commtrees[0].join_party(comm, caller, direct_join = True)
    #         except:
    #             pass
    #         if not was_direct_join:
    #             text = ("The gods did not understand your prayer. You can seek help at the campfire: \nhttps://t.me/DWcommchat")
    #             self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.defkb)
    #     # print(f"result: {result}, caller.chat_id in self.waiting_from: {caller.chat_id in self.waiting_from}")
    #     if result:      # Se houve resultado, então o bot está esperando o input do próximo comando da árvore de comandos.
    #         self.waiting_from[caller.chat_id]["remtimes"][-1] = result
    #         self.waiting_from[caller.chat_id]["internals"][-1] = internal
    #     elif caller.chat_id in self.waiting_from:       # Se não houve resultados, o penúltimo comando inserido é deletado.
    #         # print(f"waiting_from before: {self.waiting_from[caller.chat_id]}")
    #         del self.waiting_from[caller.chat_id]["comms"][-1]
    #         del self.waiting_from[caller.chat_id]["remtimes"][-1]
    #         del self.waiting_from[caller.chat_id]["internals"][-1]
    #         # print(f"waiting_from after: {self.waiting_from[caller.chat_id]}")
    #         if len(self.waiting_from[caller.chat_id]["comms"]) == 0:
    #             del self.waiting_from[caller.chat_id]
    #
    #     # Em geral, isto dá certo, pois na maioria (se não todos) das árvores de comando temos apenas dois comandos.
    #     # Dessa forma, a lista indexada por "comms" sempre terá tamanho 1.
    #     # print(self.waiting_from)
    #
    #     return result


    def process_message(self, msg, caller, message_id, caller_player = None, internal=False):
        '''
            group_process_message é process_message adaptada para parties.


            Parameters:
            caller_player (class): jogador da party que insere um comando;
            caller (dict): parties são dicionários contendo os players. Aqui, caller = party;
            msg (str): string contendo o comando inserido pelo jogador;
            internal (str): string contendo o comando interno.
        '''
        def list_reversed_index(lista, thing):
            '''
            Não sei pq codei isso, o waiting_from nunca será tão grande a ponto de mudar qualquer coisas usando isso
            ou o método reverse.
            '''
            for index in range(-1, -(len(lista) + 1), -1):
                if lista[index] == thing:
                    return index

            raise ValueError


        code = ""
        name = ""
        if isinstance(caller, player.Player):
            self.server.active_players[caller.chat_id] = time.time()
        if caller_player:
            code = caller.pt_code
            chat_id = caller_player.chat_id
            name = caller.pt_name
        else:
            code = caller.chat_id
            chat_id = caller.chat_id
            name = caller.name
        a_str = "%d/%m/%Y, %H:%M:%S"
        print(demojize(f"{code} ({name}) at {datetime.datetime.now(datetime.timezone(datetime.timedelta(hours = -3))).strftime(a_str)} said: {msg}"))
        comm = msg
        arg = None

# ------ Forest/ Deep Forest command disambiguation ----------------------------
        if comm.startswith("/forest") or comm.startswith("/deep_forest"):
            comm = emojize(":deciduous_tree: Forest :deciduous_tree:")

        if comm == emojize(":deciduous_tree: Forest :deciduous_tree:"):
            if caller.code in self.server.deep_forest_manager.jogs:
                if caller.location == "deep_forest" or caller.location == "megabeast":
                    comm = "/deep_forest"
# ------------------------------------------------------------------------------

        executed_command, result = self.exec_comm(caller, comm, arg, internal, caller_id = caller_player)
        was_waiting = code in self.waiting_from
        # print(self.waiting_from)
        if not was_waiting:
            self.waiting_from[code] = {}
            self.waiting_from[code]["comms"] = [comm]
            self.waiting_from[code]["remtimes"] = [int(result)]
            self.waiting_from[code]["internals"] = [internal]
        elif executed_command:
            self.waiting_from[code]["comms"].append(comm)
            self.waiting_from[code]["remtimes"].append(int(result))
            self.waiting_from[code]["internals"].append(internal)

        if not executed_command and was_waiting:
            comm = self.waiting_from[code]["comms"][-1]
            arg = (message_id, msg)
            internal = self.waiting_from[code]["internals"][-1]
            executed_command, result = self.exec_comm(caller, comm, arg, internal, caller_id = caller_player)
        elif not executed_command:
            was_direct_join = False
            try:
                was_direct_join = self.commtrees[1].join_party(comm, caller, direct_join = True)
            except:
                pass
            if not was_direct_join:
                text = ("The gods did not understand your prayer. You can seek help at the campfire: \nhttps://t.me/DWcommchat\n\n If you like our game and want to help improve it, please support us at patreon!\nhttps://www.patreon.com/Clini")
                # for chat_id,jogador in caller.items():
                #     if isinstance(jogador,player.Player):
                self.bot.send_message(text=text, chat_id = chat_id, reply_markup=self.server.defkb)

        if result:
            self.waiting_from[code]["remtimes"][-1] = result
            self.waiting_from[code]["internals"][-1] = internal
        elif code in self.waiting_from:
            # O índice do comando atual é buscado para evitar problemas quando o
            # helper.append_command é chamado dentro de outro comando interno ou
            # do jogador (ver adm_comms ou blacksmith_comms)
            index = list_reversed_index(self.waiting_from[code]["comms"], comm)
            del self.waiting_from[code]["comms"][index]
            del self.waiting_from[code]["remtimes"][index]
            del self.waiting_from[code]["internals"][index]
            if len(self.waiting_from[code]["comms"]) == 0:
                del self.waiting_from[code]


        return result

    def process_message_v2(self, caller, msg, internal=False):
        '''
            Processa os comandos inseridos pelo player ou pelo próprio programa. Ver exec_comm primeiro.
            Aqui é utilizado o waiting_from. Para cada chat_id, associamos um dicionário. Neste dicionário temos
            três listas. Indexada por "comms" é a lista contendo todos os comandos inseridos pelo player que foram executados.
            Indexada por "remtimes", todos os tempos restantes de cada comando.
            Indexada por "internals" todos os comandos internos executados.
            Dessa forma, o waiting_from mantém a árvore de comandos na qual o jogador está navegando.

            Comando utilizado para apendar comandos no waiting_from

            Parâmetros:
            caller (class): jogador da party que insere um comando;
            msg (str): string contendo o comando inserido pelo jogador;
            internal (str): string contendo o comando interno.
        '''
        a_str = "%d/%m/%Y, %H:%M:%S"        # String que ordena a data em dia/mês/ano e hora:minutos:segundos. Utilizado para printar as interações dos player com o chat bot no console (linha abaixo).
        print(demojize(f"{caller.chat_id} ({caller.name})  at {datetime.datetime.now(datetime.timezone(datetime.timedelta(hours = -3))).strftime(a_str)} said: {msg}"))
        comm = msg      # msg é o string dado pelo player em forma de comando. Ex: /inv
        arg = None      # Setado em None devido ao exec_comm
        executed_command, result = self.exec_comm(caller, comm, arg, internal)
        was_waiting = caller.chat_id in self.waiting_from       # chat_id do player na qual o bot está esperando o comando.
        if not caller.chat_id in self.waiting_from:
            self.waiting_from[caller.chat_id] = {}
            self.waiting_from[caller.chat_id]["comms"] = [comm]
            self.waiting_from[caller.chat_id]["remtimes"] = [int(result)]
            self.waiting_from[caller.chat_id]["internals"] = [internal]
        else:

            self.waiting_from[caller.chat_id]["comms"].append(comm)
            self.waiting_from[caller.chat_id]["remtimes"].append(int(result))
            self.waiting_from[caller.chat_id]["internals"].append(internal)



        return result

    def group_process_message_v2(self, caller_player, caller, msg, internal=False):
        '''
            group_process_message é process_message adaptada para parties.

            Usada para apendar comandos.


            Parameters:
            caller_player (class): jogador da party que insere um comando;
            caller (dict): parties são dicionários contendo os players. Aqui, caller = party;
            msg (str): string contendo o comando inserido pelo jogador;
            internal (str): string contendo o comando interno.
        '''
        temp_arg1 = "code"
        temp_arg2 = "name"
        a_str = "%d/%m/%Y, %H:%M:%S"
        print(demojize(f"{caller[temp_arg1]} ({caller[temp_arg2]}) at {datetime.datetime.now(datetime.timezone(datetime.timedelta(hours = -3))).strftime(a_str)} said: {msg}"))
        comm = msg
        arg = None

        executed_command, result = self.dg_exec_comm(caller_player, caller, comm, arg, internal)
        was_waiting = caller["code"] in self.waiting_from
        if not caller["code"] in self.waiting_from:
            self.waiting_from[caller["code"]] = {}
            self.waiting_from[caller["code"]]["comms"] = [comm]
            self.waiting_from[caller["code"]]["remtimes"] = [int(result)]
            self.waiting_from[caller["code"]]["internals"] = [internal]
        else:
            self.waiting_from[caller["code"]]["comms"].append(comm)
            self.waiting_from[caller["code"]]["remtimes"].append(int(result))
            self.waiting_from[caller["code"]]["internals"].append(internal)



        return result


    def save_comms(self):       # Salva os comandos.
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle(self.waiting_from, self.comms_file)
