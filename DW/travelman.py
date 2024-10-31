from emoji import emojize
import copy
import player

class BasicTravelMan:
    def __init__(self):
        self.def_travel_time = 40*60
        self.travel_locations = []

    def arrive(self, traveller):
        traveller.is_travelling = False
        traveller.travel_time = 0
        traveller.travelling_loc = ""

    def set_travel(self, traveller, loc, called_from_travel_book = 0):
        traveller.is_travelling = True
        traveller.travelling_loc = loc

        travel_time = self.def_travel_time
        if isinstance(traveller, player.Player):
            if traveller.classe == "Explorer":
                travel_time = traveller.e_travel_time
        else:
            if called_from_travel_book:
                travel_time = called_from_travel_book
            else:
                for jog in traveller.players:
                    if jog.classe == "Explorer":
                        if travel_time > jog.e_travel_time:
                            travel_time = jog.e_travel_time

        traveller.travel_time = travel_time

class TravelMan(BasicTravelMan):
    def __init__(self, server):
        super().__init__()
        self.server = server

    def arrive(self, traveller):
# ------------------------------------------------------------------------------
        if traveller.travelling_loc.endswith("map"):
            for item in traveller.inventory:
                if item.type == "map":
                    if item.map_type == traveller.travelling_loc:
                        traveller.inventory.remove(item)
                        loc = traveller.travelling_loc[:-4]
                        if isinstance(traveller, player.Player):
                            text = emojize(f"The {item.name} have led you to the destination.")
                            self.server.bot.send_message(text = text, chat_id = traveller.chat_id)
                            self.server.woods.encounters[loc][1](traveller.chat_id)
                        else:
                            text = emojize(f"The {item.name}: have led your group to the destination.")
                            self.server.bot.send_message(text = text, chat_id = traveller.chat_ids)
                            self.server.woods.pt_encounters[loc][1](traveller.pt_code)

                        del item
                        break
# ------------------------------------------------------------------------------
        elif traveller.travelling_loc == "death_site":
            self.server.playersdb.players_and_parties[traveller.chat_id].inventory.extend(self.server.playersdb.players_and_parties[traveller.chat_id].ghost_inv)   # Copia todas os itens do ghost inv para o inv original.
            self.server.playersdb.players_and_parties[traveller.chat_id].ghost_inv = []                                     # Reseta o ghost inv.
            player_leg_item = [copy.deepcopy(item) for item in self.server.itemsdb.weapons if item.owner == traveller.chat_id]    # Iremos buscar os itens lendários do jogador para readicioná-los em seu inv.
            self.server.playersdb.players_and_parties[traveller.chat_id].inventory.extend(player_leg_item)
            for item in player_leg_item:
                self.server.itemsdb.remove_weapon_from_pool(item)
            del player_leg_item
            text = emojize(f"After following your footsteps for a while, you come accross your old body, a comical skeleton still wearing most of your old gear."
                            f" You pocket whatever wasn't scavenged and your memories come flooding back..."
                            f" yes, that's right! You were the villain this whole time!"
                            f" Now that you've cast off suspicion, you can finally resume your master plan to-\n\n"
                            f" Wait, these aren't your memories; yours are over here."
                            f" Good thing you're just a regular, unsuspecting adventurer."
                            f" Yep, that's you. Nothing to see here, no sir.")
            self.server.bot.send_message(text=text, chat_id=traveller.chat_id)
# ------------------------------------------------------------------------------
        else:
            loc = traveller.travelling_loc
            if isinstance(traveller, player.Player):
                text = "The travel book have led you to the destination."
                self.server.bot.send_message(text=text, chat_id=traveller.chat_id)
                traveller.chegou(loc)
                self.server.woods.encounters[loc][1](traveller.chat_id)
            else:
                text = f"{traveller.travel_guider.name} have led your group to the destination."
                traveller.travel_guider.chegou(loc)
                traveller.travel_guider = None
                self.server.bot.send_message(text = text, chat_id = traveller.chat_ids)
                self.server.woods.pt_encounters[loc][1](traveller.pt_code)
# ------------------------------------------------------------------------------

        super().arrive(traveller)

    def cancel_travel(self, traveller):
        traveller.is_travelling = False
        traveller.travel_time = 0
        traveller.travelling_loc = ""
