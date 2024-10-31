#######################################################
#  Classe que possui funções relacionada ao telegram  #
#  Para mandar e receber mensagens                    #
#######################################################

# TOKENS:
# I like to store the tokens here, like
# "123456789:abcdefghijklmnopqrstuvxwyzABCDEFGHI" # Production bot
# "987654321:1a2B3C4D5e6F7g8H..."                 # Test bot1...

# Also add channel ids
# "-1001123456789" Test channel id
# "-1001909876543" Official channel id


import json  # lê, constrói e salva dicionários
import requests  # pega coisas da web
import urllib  # pega coisas da web
import telegram  # coisas do telegram
import time
import threading
import testers
import copy
# import traceback  # gerenciar erros
# from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

# teste 1

class TGBot:
    def __init__(self, token=""):
        if token != "":
            self.token = token
        else:
            self.token = "123456789:abcdefghijklmnopqrstuvxwyzABCDEFGHI"
        self.dream_token = "987654321:1a2B3C4D5e6F7g8H..."
        self.allowed_test_ids = testers.testers()
        self.tgurl = f"https://api.telegram.org/bot{self.token}/"
        self.dgurl = f"https://api.telegram.org/bot{self.dream_token}/"
        self.last_update_id = 0
        self.bot = telegram.Bot(self.token)
        # self.dream_bot = telegram.Bot(self.dream_token)
        # self.bot.setWebhook("hamesame.pythonanywhere.com" + self.token)

    # Pega conteúdo de uma url
    def get_url(self, url, timeout=70):
        '''
            Pega conteúdo de uma url

        '''
        response = requests.get(url, timeout=timeout+1)
        content = response.content.decode("utf8")
        return content

    #
    def get_json_from_url(self, url, timeout):
        '''Pega conteúdo de uma url como json'''
        content = self.get_url(url, timeout)
        js = json.loads(content)
        return js

    #
    def get_updates(self, offset=None, timeout=0):
        '''Pega todas as mensagens (de até 24h atrás, a partir de um offset)'''
        url = self.tgurl + f"getUpdates?timeout={timeout}"
        if offset:
            url += f"&offset={offset}"
        js = self.get_json_from_url(url, timeout)
        return js

#    def get_updates_dream(self, offset=None, timeout=0):
#        '''Pega todas as mensagens (de até 24h atrás, a partir de um offset)'''
#        url = self.dgurl + f"getUpdates?timeout={timeout}"
#        if offset:
#            url += f"&offset={offset}"
#        js = self.get_json_from_url(url)
#        return js

    #
    def get_last_update_id(self, updates):
        '''Pega id da última mensagem (para o offset)'''
        last_update_id = 0
        if updates["ok"] and len(updates["result"]) > 0:
            last_update_id = updates["result"][-1]["update_id"]
        return last_update_id

    # Pega o chat_id e o texto da última mensagem
    def get_last_chat_id_and_text(self, updates):
        '''Pega id da última mensagem (para o offset)'''
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)

    #
    def get_messages_dict(self, timeout=0):
        '''Retorna todas as mensagens em um dict, separadas por chat_ids'''
        updates = self.get_updates(offset=self.last_update_id + 1, timeout=timeout)

        messages_dict = {}
        if updates["ok"]:
            self.last_update_id = self.get_last_update_id(updates)
            for update in updates["result"]:
                if not "channel_post" in update:
                    if "message" in update:
                        chat_id = str(update["message"]["chat"]["id"])
                        if chat_id not in messages_dict:
                            messages_dict[chat_id] = {}
                            messages_dict[chat_id]["message_list"] = []
                            messages_dict[chat_id]["message_list"].append(update["message"]["text"])
                        else:
                            messages_dict[chat_id]["message_list"].append(update["message"]["text"])
                    elif "callback_query" in update:
                        chat_id = str(update["callback_query"]["from"]["id"])
                        if chat_id not in messages_dict:
                            messages_dict[chat_id] = {}
                            messages_dict[chat_id]["message_list"] = []
                            messages_dict[chat_id]["message_list"].append(update["callback_query"]["data"])
                            messages_dict[chat_id]["message_id_list"] = []
                            messages_dict[chat_id]["message_id_list"].append(update["callback_query"]["message"]["message_id"])
                        else:
                            messages_dict[chat_id]["message_list"].append(update["callback_query"]["data"])
                            messages_dict[chat_id]["message_id_list"].append(update["callback_query"]["message"]["message_id"])
                #     self.bot.send_message(text="oi",chat_id = "-1001335249417")
        # print(messages_dict)
        return messages_dict

#    def get_messages_dict_dream(self, timeout=0):
#        '''Retorna todas as mensagens em um dict, separadas por chat_ids'''
#        updates = self.get_updates_dream(offset=self.last_update_id + 1, timeout=timeout)
#
#        messages_dict = {}
#        if updates["ok"]:
#            self.last_update_id = self.get_last_update_id(updates)
#            for update in updates["result"]:
#                if not "channel_post" in update:
#                    if "message" in update:
#                        chat_id = str(update["message"]["chat"]["id"])
#                        if chat_id not in messages_dict:
#                            messages_dict[chat_id] = {}
#                            messages_dict[chat_id]["message_list"] = []
#                            if "text" in update["message"]:
#
#                                messages_dict[chat_id]["message_list"].append(update["message"]["text"])
#                            else:
#                                messages_dict[chat_id]["message_list"].append("/start")
#                        else:
#                            if "text" in update["message"]:
#
#                                messages_dict[chat_id]["message_list"].append(update["message"]["text"])
#                            else:
#                                messages_dict[chat_id]["message_list"].append("/start")
#                    elif "callback_query" in update:
#                        chat_id = str(update["callback_query"]["from"]["id"])
#                        if chat_id not in messages_dict:
#                            messages_dict[chat_id] = {}
#                            messages_dict[chat_id]["message_list"] = []
#                            messages_dict[chat_id]["message_list"].append(update["callback_query"]["data"])
#                            messages_dict[chat_id]["message_id_list"] = []
#                            messages_dict[chat_id]["message_id_list"].append(update["callback_query"]["message"]["message_id"])
#                        else:
#                            messages_dict[chat_id]["message_list"].append(update["callback_query"]["data"])
#                            messages_dict[chat_id]["message_id_list"].append(update["callback_query"]["message"]["message_id"])
#                #     self.bot.send_message(text="oi",chat_id = "-1001335249417")
#        # print(messages_dict)
#        return messages_dict

    #
    def send_simple_message(self, text, chat_id):
        '''Manda uma mensagem para o chat_id, contendo o "text"'''
        text = urllib.parse.quote_plus(text)
        url = self.tgurl + f"sendMessage?text={text}&chat_id={chat_id}"
        self.get_url(url)

#    def send_dream_message(self, **kwargs):
#        try:
#            message = self.dream_bot.send_message(**kwargs)
#            # print(f"message_id: {message.message_id}")
#        except telegram.error.Unauthorized:
#            pass

    def send_true_message(self, **kwargs):
         '''
                Método que vai enviar a mensagem pro jogador. Dado o limite de  4096 caracteres, esta função vai querbrar a mensagem em várias páginas
         '''
         limit = 4000
         for key,value in kwargs.items():
            if key == "text":
                if len(value) < limit:
                    try:
                        message = self.bot.send_message(**kwargs)
                        # print(f"message_id: {message.message_id}")
                    except telegram.error.Unauthorized:
                        pass


                    break
                else:
                    treco = value
                    position = limit
                    while len(treco) > limit:
                        try:
                            while treco[position]!= "\n":
                                position += 1
                        except IndexError:
                            pass

                        msg = treco[:position]
                        treco = treco[position+1:]
                        kwargs["text"] = msg
                        try:
                            self.bot.send_message(**kwargs)
                        except telegram.error.BadRequest:
                            # kwargs["text"]+="</b>"
                            # treco = "<b>"+treco
                            pass
                        position = limit
                    kwargs["text"] = treco
                    try:
                        message = self.bot.send_message(**kwargs)
                        # print(f"message_id: {message.message_id}")
                    except telegram.error.Unauthorized:
                        pass
                    break

    def send_message(self, **kwargs):
        '''
            Método que é chamado para enviar mensagens. Dentro de **kwargs é encontrado diversos parâmetros.

            Parâmetros:
                chat_id (str): Id do telegram pra enviar a mensagem
                text (str): Texto que será enviado
                reply_markup (array): Keyboard
                parse_mode (str): markdown ou html
        '''
        if kwargs["text"] == "":
            pass

        if type(kwargs["chat_id"]) == list:
            indv_kwargs = copy.deepcopy(kwargs)
            for chat_id in kwargs["chat_id"]:
                indv_kwargs["chat_id"] = chat_id
        # print(kwargs["text"])

                ac = threading.active_count()
                if ac < 120:                    # Número máximo de threads permitidas é 128, pra ter segurança, 120.
                    t = threading.Thread(target = self.send_true_message, kwargs = indv_kwargs)      # Ele vai enviar a mensagem aqui.
                    t.start()
                else:
                    while threading.active_count() > 119:
                        print("waiting")
                        time.sleep(0.1)
                    t = threading.Thread(target = self.send_true_message, kwargs = indv_kwargs)
                    t.start()
        # print(f"sending message, {ac}")
        else:
            ac = threading.active_count()
            if ac < 120:                    # Número máximo de threads permitidas é 128, pra ter segurança, 120.
                t = threading.Thread(target = self.send_true_message, kwargs = kwargs)      # Ele vai enviar a mensagem aqui.
                t.start()
            else:
                while threading.active_count() > 119:
                    print("waiting")
                    time.sleep(0.1)
                t = threading.Thread(target = self.send_true_message, kwargs = kwargs)
                t.start()

    def edit_message(self, **kwargs):
        # print(kwargs)
        if isinstance(kwargs["message_id"], int):

            try:
                self.bot.edit_message_text(**kwargs)
            except telegram.error.BadRequest:
                pass
        else:
            if isinstance(kwargs["chat_id"], str):
                if kwargs["chat_id"] in kwargs["message_id"]:
                    kw2 = copy.deepcopy(kwargs)
                    kw2["message_id"] = kwargs["message_id"][kwargs["chat_id"]]
                    try:
                        self.bot.edit_message_text(**kw2)
                    except telegram.error.BadRequest:
                        pass
            else:
                for chat,id in kwargs["message_id"].items():
                    kw2 = copy.deepcopy(kwargs)
                    kw2["message_id"] = id
                    kw2["chat_id"] = chat
                    try:
                        self.bot.edit_message_text(**kw2)
                    except telegram.error.BadRequest:
                        pass
    def send_audio(self, **kwargs):
        '''Enviar músicas'''
        self.bot.send_audio(**kwargs)


    def send_photo(self, **kwargs):
        '''Enviar fotos'''
        self.bot.send_photo(**kwargs)
