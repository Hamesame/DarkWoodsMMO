import player

class checker_and_retificator:
    def __init__(self):
        pass

    def check_class_and_return_new_player_object(self, chat_id, old_player):
        newplayer = old_player

        newplayer = player.Player(chat_id)
        newplayer.clone_player(old_player)

        return newplayer

    def walk_in_the_players_dictionary_and_retificate(self, players_dic):
        for chat_id, jogador in players_dic.items():
            players_dic[chat_id] = self.check_class_and_return_new_player_object(chat_id, jogador)
