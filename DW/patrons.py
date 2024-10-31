import os

class PatreonDB:
    def __init__(self, server):
        self.helper = server.helper
        self.patreon_file = "dbs/patreons.dat"
        self.patreon_backup = "dbs/patreons.dat.bak"
        loaded = self.helper.load_pickle(self.patreon_file)
        self.patreon_backers = {}
        if loaded:
            self.patreon_backers = loaded


    def save_patreons(self):
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.helper.save_pickle(self.patreon_backers, self.patreon_file)

    def add_patreon(self, chat_id, value):
        '''
        Registra um novo usuario
        '''
        self.patreon_backers[chat_id] = value

    def remove_patreon(self, chat_id):
        '''
        Remove um usuário
        '''
        del self.patreon_backers[chat_id]
