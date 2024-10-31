import bot

class Comms:
    def __init__(self, server):
        self.comm_dic ={
            "/help": self.show_help,
            "/beginning": self.beguinning,
            "/name": self.name,
            "/back": self.back,
            "/me": self.me,
            "/edit": self.edit,
            "/edit_options": self.edit_options,
        }
        self.bot = bot.TGBot()
        self.waiting_from = {}
        self.server = server

    def me(self, chat_id, args):
        user = self.server.playersdb.players[chat_id]
        text = (    f"Author name: {user.name}\n\n"
                    f"Stories Written: {user.nodes_written}\n"
                    f"Stories Read: {user.nodes_read}"
                    )
        self.bot.send_message(text=text, chat_id=chat_id)
        del self.waiting_from[chat_id]

    def show_help(self, chat_id, args):
        text = ("Here are the commands:\n"
                "\n"
                "/help: Shows this menu.\n"
                "/me: Shows your info.\n"
                "/back: Backs one step\n"
                "/beginning: Backs to the start.\n"
                "/name: Changes your name.\n"
                "/edit: Edits the current node text.\n"
                "/edit_options: Edits The options of current node.\n"
                "\n"
                "If you have more doubts, enter the community chat:\n"
                "https://t.me/StoriesComm\n"
                "\n"
                "Please consider donating to support us:\n"
                "https://www.patreon.com/Clini\n"
                )
        self.server.bot.send_message(text=text, chat_id=chat_id)
        del self.waiting_from[chat_id]

    def beguinning(self, chat_id, args):
        if not args:
            text = "Are you sure you want to go back to the start? /y or /n?"
            self.bot.send_message(text=text, chat_id=chat_id)
        else:
            if args == "/y":
                self.server.playersdb.players[chat_id].node = "0"
                self.server.storiesdb.play_node(chat_id, self.server.storiesdb.stories[self.server.playersdb.players[chat_id].node])
                del self.waiting_from[chat_id]
            elif args == "/n":
                text = "Ok!"
                self.bot.send_message(text=text, chat_id=chat_id)
                del self.waiting_from[chat_id]
            else:
                text = "What did you say? /y or /n?"
                self.bot.send_message(text=text, chat_id=chat_id)

    def name(self, chat_id, args):
        if not args:
            text = "Please tell me your new name."
            self.bot.send_message(text=text, chat_id=chat_id)
        else:
            self.server.playersdb.players[chat_id].name = args
            text = "Name changed."
            self.bot.send_message(text=text, chat_id=chat_id)
            del self.waiting_from[chat_id]

    def back(self, chat_id, args):
        if not self.server.playersdb.players[chat_id].node == "0":
            last_char = self.server.playersdb.players[chat_id].node[-1]
            while last_char != " ":
                self.server.playersdb.players[chat_id].node = self.server.playersdb.players[chat_id].node[:-1]
                last_char = self.server.playersdb.players[chat_id].node[-1]
            self.server.playersdb.players[chat_id].node = self.server.playersdb.players[chat_id].node[:-1]
        self.server.storiesdb.play_node(chat_id, self.server.storiesdb.stories[self.server.playersdb.players[chat_id].node])
        del self.waiting_from[chat_id]

    def edit(self, chat_id, args):
        if not self.server.playersdb.players[chat_id].node:
            text = "You are not in a node. Please enter one first."
            self.bot.send_message(text=text, chat_id=chat_id)
            del self.waiting_from[chat_id]
        if not args:
            text = "Please, type the new text for this node."
            self.bot.send_message(text=text, chat_id=chat_id)
        else:
            self.server.storiesdb.stories[self.server.playersdb.players[chat_id].node].text = args
            self.server.storiesdb.stories[self.server.playersdb.players[chat_id].node].creator = chat_id
            text = "Succesfully edited the node text"
            self.bot.send_message(text=text, chat_id=chat_id)
            del self.waiting_from[chat_id]
            self.server.storiesdb.play_node(chat_id, self.server.storiesdb.stories[self.server.playersdb.players[chat_id].node])

    def edit_options(self, chat_id, args):
        text = "Ok, all options have been erased. please type the new options."
        self.bot.send_message(text=text, chat_id=chat_id)
        user = self.server.playersdb.players[chat_id]
        self.server.storiesdb.stories[user.node].options = []
        user.is_creating_a_node = True
        user.is_creating_options = True
        del self.waiting_from[chat_id]

    def process(self, chat_id, msg):
        if not chat_id in self.waiting_from:
            self.waiting_from[chat_id] = msg
            self.comm_dic[msg](chat_id, None)
        else:
            self.comm_dic[self.waiting_from[chat_id]](chat_id, msg)
