

class Party:

    exception_attr_name = ["storage", "inventory", "atk", "defense", "stats", "name", "arena_rank", "arenas_left", "max_arenas"] # Lista para exceções no setattr.

    def __init__(self, creator, pt_code, pt_name):
        self.players = [creator]
        self.chat_ids = [creator.chat_id]

        self.pt_code = pt_code
        self.pt_name = pt_name
        self.code = pt_code
        self.location = "camp"
        self.prev_location = "camp"
        self.active = False
        self.is_travelling = False
        self.travel_time = 0
        self.travelling_loc = ""
        self.travel_guider = None
        self.inventory = []
        self.arena_rank = 0
        self.arenas_left = 5
        self.max_arenas = 5

        self.time_factor_pt = 1

        # atributos para /rankings
        self.atk = 0
        self.defense = 0
        self.stats = 0
        self.name = pt_name

        self.status = []

        self.average_time_between_dungeons_pt = 0
        self.average_time_between_last_dungeons_pt = 0
        self.average_times_taken_pt = []
        self.last_done_dungeon_time_pt = 0
        self.average_time_between_WB_pt = self.average_time_between_dungeons_pt/5
        self.last_dg_id_pt = {}

        self.attacked_the_wb = False

        self.calc_attributes()

    def __setattr__(self, name, value):
        # Antes de setar o local novo, setamos o prev_location primeiro
        # para não perder o location atual.
        if name == "location":
            try:
                present_location = getattr(self, "location")
                self.__setattr__("prev_location", present_location)
            except AttributeError:
                # Única forma de dar attrError é quando o prev_location não foi criado
                # Isto é, o __init__ está rodando. Deixamos o init rodar normal pulando
                # o processo do prev_location.
                pass
                # print("loop infinito?")
                # setattr(self, name, value)
                # setattr(self, "prev_location", value)


        super(Party, self).__setattr__(name, value) # Chamamos o setattr da classe mãe, para não dar loop infinito.

        if name == "pt_name":
            try:
                super(Party, self).__setattr__("name", value)
            except AttributeError:
                pass

        for player in self.players:
            if name not in self.exception_attr_name:
                try:
                    attr = getattr(player, name)
                    if not callable(attr):
                        setattr(player, name, value)
                except AttributeError:
                    pass

    # def __getattribute__(self, name):
    #     ''' Utilizado no /rankings. Ver print_ranking_list em show_rankings em
    #         players_comms.py '''
    #     if name == "name":
    #         attr = getattr(self, "pt_name")
    #         return attr
    #     else:
    #         attr = getattr(self, name)
    #         return attr

    def join_pt(self, player):
        self.players.append(player)
        self.chat_ids.append(player.chat_id)
        player.pt_code = self.pt_code
        player.pt_name = self.pt_name
        player.code = self.pt_code
        player.calc_attributes()
        self.calc_attributes()

    def leave_pt(self, player):
        if player in self.players:
            self.players.remove(player)
            self.chat_ids.remove(player.chat_id)
            player.pt_code = ""
            player.pt_name = ""
            player.is_synergyzed = False
            player.code = player.chat_id
            player.calc_attributes()
        self.calc_attributes()

    def adm_leave_pt(self, player):
        self.players.remove(player)
        self.chat_ids.remove(player.chat_id)
        player.calc_attributes()

    def reset_stats(self):
        for player in self.players:
            player.reset_stats()

    def calc_attributes(self):
        self.atk = 0
        self.defense = 0
        self.stats = 0
        lowest_time_factor = 1
        for player in self.players:
            self.atk += player.atk
            self.defense += player.defense
            self.stats += player.stats
            # print(player.classe)
            if player.classe == "Explorer":
                if player.time_factor < lowest_time_factor:
                    lowest_time_factor = player.time_factor
        self.time_factor_pt = lowest_time_factor
        # print(self.time_factor_pt)
