# A função do connector é conectar o flask_app com o resto do jogo
import time
import os

class ConnectorMan:
    def __init__(self, server):
        self.server = server
        self.last_message = ""

    def read_message(self):
        current_time = time.time()
        message = self.server.helper.load_pickle("comms/message.dat")
        if message:
            if message != self.last_message:
                self.last_message = message
                print(message)
                if "check_id" in message:
                    result = message["check_id"] in self.server.playersdb.players_and_parties
                    if "add_currency" in message and result:
                        self.server.playersdb.players_and_parties[message["check_id"]].leaves += message["add_currency"]
                        self.server.bot.send_message(text=f"Thanks for your purchase, {message['add_currency']} leaves has been added to your account, now you have {self.server.playersdb.players_and_parties[message['check_id']].leaves} leaves.", chat_id = message["check_id"])
                        self.server.save_all()
                    result = {"response": result, "time": current_time}
                    if not os.path.exists("comms/"):
                        os.makedirs("comms/")
                    print(result)
                    self.server.helper.save_pickle(result, "comms/response.dat")
