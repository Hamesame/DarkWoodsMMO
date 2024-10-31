import os

class Example:
    '''
        Exemplo de estrutura
    '''
    def __init__(self, server):
        self.server = server
        self.def_wait_time = 60
        self.dgkb = self.server.keyboards.bs_reply_markup
        self.defkb = self.server.keyboards.class_main_menu_reply_markup
        self.ex_file = "dbs/example.dat"
        self.strut_you_want_to_save = {}
        loaded = self.server.helper.load_pickle(self.strut_you_want_to_save)
        if loaded:
            self.strut_you_want_to_save = loaded

    def func1(self, ob1):
        print(ob1)
        return self.def_wait_time

    def save_ex(self):
        '''
            Salva a estrutura que você quer criar
        '''
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle(self.strut_you_want_to_save, self.ex_file)


###
### Agora para comandos:
###

from emoji import emojize

class ExampleCommms:
    '''
        Exemplo de classe de comandos
    '''
    def __init__(self, server):
        '''
            Ele carrega o server, o keyboard padrão, o tempo padrão de espera, que é 1 minuto, o bot pra mandar mensagens, e o único comando, que é o forest.

        '''
        self.server = server
        self.defkb = server.defkb           # Keyboard padrão
        self.ynkb = self.server.keyboards.bs_reply_markup   # Keyboard com YES/NOPE
        self.def_wait_time = 60
        self.actions = {
            "/text_player_sent": self.desired_function_to_run_when_players_sends_this_text
        }
        self.internal = {
            "internal command": self.A_command_players_cant_enter_they_are_activated_via_events
        }

    def A_command_players_cant_enter_they_are_activated_via_events(self, caller, caller_id = None, *args):
        if not args:
            '''
                Code to run when the player finds something
            '''
            text = "text"
            self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.ynkb)
            return self.def_wait_time*2 # 2 mins of wait
        else:
            '''
                Code to run when players answer
            '''
            text = "text"
            self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.ynkb)
            return False # Quando False é retornado o comando dropa

    def desired_function_to_run_when_players_sends_this_textforest(self, caller, *args):
        if not args:
            '''
                Code to run when the player say something
            '''
            text = "text"
            self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.ynkb)
            return self.def_wait_time*2 # 2 mins of wait
        else:
            '''
                Code to run when players answer
            '''
            text = "text"
            self.server.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.ynkb)
            return False # Quando False é retornado o comando dropa

    def to(self, chat_id):
        '''
            Função que roda quando da timeout na função nas actions,
            normalmente é só um pass msm.
        '''
        pass

    def to2(self, chat_id):
        '''
            Função que roda quando da timeout na função interna.
        '''
        if chat_id[0] == "/":
            if chat_id in self.server.playersdb.players_and_parties:
                text = "It's a dangerous place, so your party decided to step back."
                chat_ids = self.server.playersdb.players_and_parties[chat_id].chat_ids
                self.bot.send_message(text=text, chat_id=chat_ids, reply_markup=self.defkb)
        else:

            text = "It's a dangerous place, so you decided to step back."
            self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb)
