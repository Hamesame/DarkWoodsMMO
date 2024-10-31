###################################
#  Classes que descrevem itens    #
#  Derivadas da classe base Item  #
###################################
import helper
import threading
import bot
import player
import travelman
from emoji import emojize
import copy

class Item:
    '''
        Classe base de todos os itens do jogo.
    '''
    def __init__(self, name, is_legendary, code, prob, *args):
        self.name = name        # Nome do item
        self.is_legendary = is_legendary        # Itens lendários no DW significa que ele é único (só existe um), mesmo que tenha os mesmos nomes e status. Veja itemsdb.py para maior entendimento.
        self.code = code        # Código do item que atribui um comando ao player para poder usá-lo.
        self.ac_code = code
        self.prob = prob        # Probabilidade de encontrar o itemna floresta.
        self.atributos = [0, 0] # Status do item.
        self.description = ""

        self.new(*args)         # Carrega mais características do item.

    def __str__(self):
        type_emoji = {"armor":emojize(":running_shirt:"), "melee":emojize(":dagger:"), "magic":emojize(":crystal_ball:"), "ranged":emojize(":bow_and_arrow:"), "magical":emojize(":crystal_ball:"), "consumable":emojize(":red_apple:")}
        s = emojize(f"|{type_emoji[self.type2]}| {self.name} :crossed_swords: {self.atributos[0]} :shield: {self.atributos[1]}")
        s = s.replace("*", "\\*")
        return emojize(f"|{type_emoji[self.type2]}| {self.name} :crossed_swords: {self.atributos[0]} :shield: {self.atributos[1]}")

    def new(self, *args):
        '''
            Função que será inicializada pelo init para carregar mais características.
            O parâmetro args não é implementado.
        '''
        self.type = "item"
        self.action = None      # Possíveis ações do item que podem ser chamados como comandos pelo player.

# Note que, em cada subclasse abaixo, temos a função new redefinida.
class Weapon(Item):
    '''
        Classe referente às armas do DW.
    '''
    def new(self, atributos):
        '''
            Função que será inicializada pelo init da classe mãe.

            Parâmetros:
                atributos (list): lista contendo os status de ataque e defesa da arma.
        '''
        self.type = "Weapon"
        self.atributos = atributos
        self.og_attr = atributos
        self.action = self.equip    # Única ação do item é equipar.
        self.owner = ""     # Indexa o dono da arma, quando este estiver compartilhando a arma numa party.
        self.is_shared_and_equipped = False     # Checa se o item está sendo usado por algum jogador da party (incluíndo o dono) após o item ter sido compartilhado.
        self.type2 = "melee"        # O type2 se refere ao tipo de arma, ele pode ser "melee", "magic", "ranged"
        self.powers = {}
        self.talismans = {}
        self.stats_boost_by_talisman = 0.05
        self.update_stats()  # Chamado para caso haja atualização dos poderes da arma num update do jogo.

    def equip(self, jogador):
        '''
            Equipa o item.

            Parâmetros:
                jogador (class): jogador que irá equipar o item.
        '''
        if jogador.weapon:      # Checa que se o jogador possui uma arma equipada.
            if jogador.weapon.is_shared_and_equipped:       # Checa se a arma está compartilhada na party.
                jogador.weapon.is_shared_and_equipped = False
            if jogador.weapon_stat_boost:
                jogador.weapon_stat_boost = False
                for power,stat in jogador.weapon.powers.items():
                    if power.startswith("boost"):
                        if power[6:] == "str":
                            jogador.att_points[emojize(":flexed_biceps: Strength :flexed_biceps:")] -= stat
                        if power[6:] == "int":
                            jogador.att_points[emojize(':brain: Intelligence :brain:')] -= stat
                        if power[6:] == "dex":
                            jogador.att_points[emojize(':eye: Dexterity :eye:')] -= stat

        jogador.weapon = self
        if jogador.classe != "Unknown":
            if not jogador.weapon_stat_boost:
                jogador.weapon_stat_boost = True
                print(self.powers)
                print(jogador.att_points)
                for power,stat in self.powers.items():
                    if power.startswith("boost"):
                        if power[6:] == "str":
                            jogador.att_points[emojize(":flexed_biceps: Strength :flexed_biceps:")] += stat
                        if power[6:] == "int":
                            jogador.att_points[emojize(':brain: Intelligence :brain:')] += stat
                        if power[6:] == "dex":
                            jogador.att_points[emojize(':eye: Dexterity :eye:')] += stat
                print(jogador.att_points)

    def unequip(self, jogador):
        '''
            Função que vai desequipar o item do jogador.
        '''
        # jogador.weapon_stat_boost = False
        print(f"jogador.weapon_stat_boost: {jogador.weapon_stat_boost}")
        if jogador.weapon_stat_boost:
            # if jogador.weapon.is_shared_and_equipped:       # Checa se a arma está compartilhada na party.
            #     jogador.weapon.is_shared_and_equipped = False
            jogador.weapon_stat_boost = False
            print(self.powers)
            for power,stat in self.powers.items():
                if power.startswith("boost"):
                    if power[6:] == "str":
                        jogador.att_points[emojize(":flexed_biceps: Strength :flexed_biceps:")] -= stat
                    if power[6:] == "int":
                        jogador.att_points[emojize(':brain: Intelligence :brain:')] -= stat
                    if power[6:] == "dex":
                        jogador.att_points[emojize(':eye: Dexterity :eye:')] -= stat


    def add_talismans(self, talisman_list):
        ''' Método para adicionar talismãns. É necessário para reescrever poderes que já existem na arma. '''
        # self.powers = {}
        for talisman in talisman_list:
            self.talismans[talisman.code] = copy.deepcopy(talisman)
            print(talisman.powers)
            for power in talisman.powers:
                if power in self.powers:
                    # if talisman.powers[power] > self.powers[power]:
                        self.powers[power] += talisman.powers[power]
                else:
                    self.powers[power] = talisman.powers[power]
        print(self.powers)
        self.update_stats()

    def update_stats(self):
        ''' Calcula os atributos da arma quando esta tiver talismãns. É necessário devido à ordem das operações de boost e de rebalence. '''

        # print(self.og_attr)
        # print(self.atributos)
        # try:
        #     print(self.powers)
        #
        # except:
        #     self.powers = {}
        #     self.talismans = {}
        #     self.og_stats = self.atributos
        if not len(self.powers):
             self.atributos = copy.deepcopy(self.og_attr)
        else:
            self.atributos = copy.deepcopy(self.og_attr)
            if "wep defense" in self.powers:
                self.atributos[1] = round(self.og_attr[1] * (1 + self.stats_boost_by_talisman * self.powers['wep defense']))
            if "wep damage" in self.powers:
                self.atributos[0] = round(self.og_attr[0] * (1 + self.stats_boost_by_talisman * self.powers['wep damage']))
            if "rebalance defense" in self.powers:
                self.atributos[1] = min(round(self.atributos[1]  + 0.15 * self.powers['rebalance defense'] * self.atributos[0]),  self.atributos[1] + self.atributos[0])
                self.atributos[0] = max(round(self.atributos[0]  - 0.15 * self.powers['rebalance defense'] * self.atributos[0]),  0)
            if "rebalance attack" in self.powers:
                self.atributos[0] = min(round(self.atributos[0]  + 0.15 * self.powers['rebalance attack'] * self.atributos[1]),  self.atributos[1] + self.atributos[0])
                self.atributos[1] = max(round(self.atributos[1]  - 0.15 * self.powers['rebalance attack'] * self.atributos[1]),  0)

        # print(self.og_attr)
        # print(self.atributos)

    def remove_talismans(self):
        self.talismans = {}
        self.powers = {}
        self.update_stats()

    def talisman_list(self):
        s = "\n"
        for tal_name,talisman in self.talismans.items():
            s += f"*{talisman}*\n"
        return s

    def power_list(self):
        s = "\n"
        for pow_name,power in self.powers.items():
            s += f"*{pow_name}: {power}*\n"
        return s
# Só um exemplo de item com ação
# A ação seria chamada assim: item.actions["heal"](player.hp)
class LifePotion(Item):
    '''
        Item que cura o jogador.
    '''
    def new(self, *args):
        self.type = "potion"
        self.action = self.heal_random_limb

    def heal_random_limb(self, player):
        limb_i = player.random_damaged_limb_index()
        if limb_i > -1:
            player.hp[limb_i].health += 1
        else:
            pass
            # print("No limbs are damaged!")

class Armor(Item):

    def new(self, status_protection_dict = {"cold": 1}):
        '''
        status_protection_list (dict): { "status": status_reduction}.
        '''
        self.type = "Armor"
        self.action = self.equip2
        self.owner = ""
        self.is_shared_and_equipped = False
        self.type2 = "armor"
        self.status_protection = status_protection_dict

    def talisman_list(self):
        s = "Armors can't have talismans"
        return s

    def power_list(self):
        s = ""
        return s

    def equip2(self, jogador):
        '''
            Equipa o item.

            Parâmetros:
                jogador (class): jogador que irá equipar o item.
        '''
        if jogador.armor:      # Checa que se o jogador possui uma arma equipada.
            if jogador.armor.is_shared_and_equipped:       # Checa se a arma está compartilhada na party.
                jogador.armor.is_shared_and_equipped = False
        jogador.armor = self

class dg_map(Item):
    '''
        Este é o dusty map, mapa que leva o jogador a uma dungeon aleatória do DW.
    '''
    possibles_maps = [
        (emojize("Dusty map :world_map:"), 0, "dstmp", 1, "dg_map"),
        (emojize("Crumbling map :world_map:"), 0, "crbmp", 1, "deep_forest_map")
    ]

    def new(self, map_type = "dg_map"):
        self.bot = bot.TGBot()      # Seta o bot para mandar mensagens.
        self.type = "map"
        self.type2 = "consumable"
        self.map_type = map_type
        self.action = self.use_map
        self.owner = ""
        self.is_shared_and_equipped = False
        self.travelkid = travelman.BasicTravelMan()
        self.description = ""
        if self.map_type == "dg_map":
            self.description = ("A dusty piece of paper that can lead you to a dungeon. A normal adventurer will take 40 minutos to get there")
        if self.map_type == "deep_forest_map":
            self.description = "A map that leads to a deeper part of the forest."

    def use_map(self, jogador):
        if jogador.location == "forest":
            self.travelkid.set_travel(jogador, self.map_type)
            if isinstance(jogador, player.Player):
                text = f"You used the map to the dungeon/deep forest, you will get there in {round(jogador.travel_time/60)} minutes"
                self.bot.send_message(text=text, chat_id=jogador.chat_id)
            else:
                text = f"You used the map to the dungeon/deep forest. Your party will get there in {round(jogador.travel_time/60)} minutes."
                self.bot.send_message(text=text, chat_id=jogador.chat_ids)
        else:
            if isinstance(jogador, player.Player):
                self.bot.send_message(text="You need to be at the forest to follow the map.", chat_id=jogador.chat_id)
            else:
                self.bot.send_message(text = "Someone tried to use the map while not in the forest!", chat_id = jogador.chat_ids)

    def talisman_list(self):
        s = "Maps can't have talismans"
        return s

    def power_list(self):
        s = ""
        return s
class map(Item):
    '''
        Este é o dusty map, mapa que leva o jogador a uma dungeon aleatória do DW.
    '''
    possibles_maps = [
        (emojize("Dusty map :world_map:"), 0, "dstmp", 1, "dg_map"),
        (emojize("Crumbling map :world_map:"), 0, "crbmp", 1, "deep_forest_map")
    ]

    def new(self, map_type = "dg_map"):
        self.bot = bot.TGBot()      # Seta o bot para mandar mensagens.
        self.type = "map"
        self.type2 = "consumable"
        self.map_type = map_type
        self.action = self.use_map
        self.owner = ""
        self.is_shared_and_equipped = False
        self.travelkid = travelman.BasicTravelMan()
        self.description = ""
        if self.map_type == "dg_map":
            self.description = ("A dusty piece of paper that can lead you to a dungeon. A normal adventurer will take 40 minutos to get there")
        if self.map_type == "deep_forest_map":
            self.description = "A map that leads to a deeper part of the forest."

    def use_map(self, jogador):
        if jogador.location == "forest":
            self.travelkid.set_travel(jogador, self.map_type)
            if isinstance(jogador, player.Player):
                text = f"You used the map to the dungeon/deep forest, you will get there in {round(jogador.travel_time/60)} minutes"
                self.bot.send_message(text=text, chat_id=jogador.chat_id)
            else:
                text = f"You used the map to the dungeon/deep forest. Your party will get there in {round(jogador.travel_time/60)} minutes."
                self.bot.send_message(text=text, chat_id=jogador.chat_ids)
        else:
            if isinstance(jogador, player.Player):
                self.bot.send_message(text="You need to be at the forest to follow the map.", chat_id=jogador.chat_id)
            else:
                self.bot.send_message(text = "Someone tried to use the map while not in the forest!", chat_id = jogador.chat_ids)
    def talisman_list(self):
        s = "Maps can't have talismans"
        return s

    def power_list(self):
        s = ""
        return s
    # def chegou(self, jogador):
    #     '''
    #         Função que é chamada quando o jogador (ou party) chega da dungeon. O mapa é deletado do inventário com essa função.
    #
    #         Parâmetros:
    #             jogador (class or dict): representa o jogador individual ou uma party.
    #     '''
    #     if isinstance(jogador, dict):       # Checa se é party.
    #         if self in jogador["pt_inv"]:   # Checa se o mesmo dusty map está no inventário.
    #             jogador["is_travelling"] = False    # A party não está mais viajando, então todos os atributos de classe referentes à viagem são resetados.
    #             jogador["travel_time"] = 0
    #             jogador["travelling_loc"] = ""
    #             jogador["pt_inv"].remove(self)      # Retira o mapa do inventário.
    #     else:
    #         if self in jogador.inventory:
    #             jogador.is_travelling = False
    #             jogador.travel_time = 0
    #             jogador.travelling_loc = ""
    #             jogador.inventory.remove(self)
    #
    # def use_map(self, jogador):
    #     '''
    #         Função que põe o jogador ou a party em movimento para a dungeon.
    #         Para que o jogador ou party viajem para uma dungeon é necessário estar na floresta.
    #         Além disso, se o jogador estiver numa party, o item deve estar compartilhado (ver player_comms.py).
    #
    #         Parâmetros:
    #             jogador (class or dict): representa o jogador individual ou uma party.
    #     '''
    #     if isinstance(jogador,dict):        # Checa se é party.
    #
    #         if jogador["is_at_forest"]:     # Tem que estar na floresta.
    #
    #             tt = 40*60 #40*60       Tempo de viagem em segundos.
    #             jogador["is_travelling"] = True
    #             jogador["travel_time"] = tt
    #             jogador["travelling_loc"] = "dg_map"        # Aponta o destino do jogador ou party através do comando utilizado.
    #             text = f"You used the map to the dungeon. Your party will get there in {round(tt/60)} minutes."
    #             for chat,jog in jogador.items():
    #                 if isinstance(jog, player.Player):
    #                     self.bot.send_message(text=text,chat_id=chat)
    #
    #         else:
    #             text="Someone tried to use the map while not in the forest!"
    #             for chat,jog in jogador.items():
    #                 if isinstance(jog, player.Player):
    #                     self.bot.send_message(text=text,chat_id=chat)
    #
    #
    #     else:
    #         if jogador.is_at_forest:
    #             jogador.is_travelling = True
    #             jogador.travel_time = 40*60 #40*60
    #             jogador.travelling_loc = "dg_map"
    #             self.bot.send_message(text="You used the map to the dungeon, you will get there in 40 minutes", chat_id=jogador.chat_id)
    #
    #         else:
    #             self.bot.send_message(text="You need to be at the forest to follow the map.", chat_id=jogador.chat_id)
