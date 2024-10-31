#####################################################
#  Classe contendo funções que ajudam no dia-a-dia  #
#####################################################

import random as rd
from shutil import copyfile
import pickle
import os
import player


class Helper:
    '''
        O Helper possui algumas funções usadas no código, como o gerador de palavras aleatórias e
        a função para apendar e remover comandos do messageman. Também possui funções para salvar o jogo.
    '''
    
    def __init__(self, server):
        self.server = server

    def randomsilaba(self, is_last):
        '''
            Gerador de sílabas aprimorado.

            Parâmetros:

            is_last (bool): para falar se é a última sílaba ou não.
        '''
        vogal = ["a", "e", "i", "o", "u", "y",
                 "a", "e", "i", "o", "u", "y",
                 "a", "e", "i", "o", "u", "y",
                 "a", "e", "i", "o", "u", "y", "ai", "oi", "ei"]            # Vogais, as vogais repetidas são para aumentar a probabilidade
        cons = ["w", "r", "t", "p", "s", "d", "f", "g", "h", "j", "k", "l",
                "z", "x", "c", "v", "b", "n", "m", "w", "r", "t", "p", "s", "d", "f", "g", "h", "j", "k", "l",
                        "z", "x", "c", "v", "b", "n", "m"]

        specials = {"w":"r","b":"b","l":"h","p":"h","c":"h","t":"h","g":"u","q":"u","m":"m","f":"r","r":"t","s":"s","i":"n"}
        p = rd.randint(0, 5)
        s = ""
        s += cons[rd.randint(0,len(cons)-1)]        # pega consoante aleatória
        if p == 0 and s in specials:
            s += specials[s]
        s += vogal[rd.randint(0,len(vogal)-1)]
        p = rd.randint(0, 5)
        if p == 0 and s[-1] in specials:
            s += specials[s[-1]]
        return s
        # if is_last:
        #     v = len(vogal)-1
        #     c = len(cons)-1
        # else:
        #     v = len(vogal)-2
        #     c = len(cons)-1
        # if p == 5:
        #     s = cons[rd.randint(0, c)] + vogal[rd.randint(0, v)] + cons[rd.randint(0, c)]
        # else:
        #     s = cons[rd.randint(0, c)] + vogal[rd.randint(0, v)]
        # return s

    def randomnamegenerator(self, media):
        '''
            Gerador aleatório de nomes.

            Parâmetros:

            media (int): a média de sílabas.
        '''
        i = round(media/3)
        if media == 1:
            size = 1
        elif media == 2:
            size = 1 + rd.randint(0, 1)
        else:
            size = rd.randint(1, i) + rd.randint(0, i) + rd.randint(0, i)
        s = ""
        last = 0
        for j in range(size):
            if j == size - 1:
                last = 1
            s += self.randomsilaba(last)
        return s.capitalize()

    def load_pickle(self, file="tmp/blob.dat"):
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

    def save_pickle(self, blob=None, file="tmp/blob.dat"):
        '''
            Função que salva os arquivos

            Parâmetros:

            blob (qqr coisa): Arquivo será salvo.
            file (str): Nome do arquivo em que será salvo.

        '''
        if os.path.isfile(file):
            self.create_backup(file)        # Cria o backup
        try:
            with open(file, "wb") as fp:
                pickle.dump(blob, fp)       # Salva o arquivo
        except:
            pass

    def create_backup(self, file):
        '''
            Ele literalmente cria um outro arquivo com o msm nome mas com uma extensão .old para caso o jogo morrer no meio do salvamento, ele
             não corromper.
        '''
        dst = file + ".old"
        copyfile(file, dst)

    def append_command(self, command, code):
        '''
            Função do messageman que apenda um comando em waiting_from. Como se o jogador tivesse falado o nome do comando. Usado pra iniciar dungeons e blacksmiths

            Parâmetros:

            command (str): Nome do comando
            chat_id (str): Chat id do usuario de telegram que ganhou a dungeon ou blacksmith

        '''
        if code in self.server.playersdb.players_and_parties:
            if code[0] == "/":
                first_p = None
                if self.server.playersdb.players_and_parties[code].players:
                    leader = self.server.playersdb.players_and_parties[code].players[0]
                else:
                    self.server.dissolve_party(code)
                return self.server.messageman.process_message(command, self.server.playersdb.players_and_parties[code], "", caller_player = leader, internal=True) # Pra ele mandar a mensgaem pra td mundo e iniciar o comando
            return self.server.messageman.process_message(command, self.server.playersdb.players_and_parties[code], "", internal=True)


    def remove_command(self, command, chat_id):
        '''
            Função que remove um comando específico do jogador, provavelmente por timeout. Ou pq acabou oq ele tava fazendo

            Parâmetros:

            command (str): comando que será removido de waiting_from
            chat_id (srt): Chat id do usuario de telegram que terá o comando removido
        '''
        if chat_id in self.server.messageman.waiting_from:
                if command in self.server.messageman.waiting_from[chat_id]["comms"]:
                    i = self.server.messageman.waiting_from[chat_id]["comms"].index(command)
                    del self.server.messageman.waiting_from[chat_id]["comms"][i]
                    del self.server.messageman.waiting_from[chat_id]["remtimes"][i]
                    del self.server.messageman.waiting_from[chat_id]["internals"][i]
                if len(self.server.messageman.waiting_from[chat_id]["comms"]) == 0:
                    del self.server.messageman.waiting_from[chat_id]

    def remove_all_commands(self, chat_id):
        '''
            Remove todos os comandos. Função utilziada quando o jogador é morto ou apagado.

            Parâmetros:

            chat_id (str): Chat id do usuario de telegram que terá o comando removido.
        '''
        if chat_id in self.server.messageman.waiting_from:
            del self.server.messageman.waiting_from[chat_id]
