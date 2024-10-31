###########################################
#  Classes que definem um jogador         #
#  Inclui a classe base e as específicas  #
###########################################

from emoji import emojize
import random as rd
import bot
import travelman
import status_ailments
import deep_beastsdb
import copy

class OrganizedTalismanDB:
    def __init__(self):
        self.talismans = [{},{},{},{},{},{},{}]

    def append(self, tal):

        if tal.code in self.talismans[tal.rarity]:
            self.talismans[tal.rarity][tal.code][1] += 1
        else:
            self.talismans[tal.rarity][tal.code] = [tal, 1]

    def remove(self, tal):
        if tal.code in self.talismans[tal.rarity]:
            self.talismans[tal.rarity][tal.code][1] -= 1
            if self.talismans[tal.rarity][tal.code][1] < 1:
                del self.talismans[tal.rarity][tal.code]

    def extend(self, tals):
        for tal in tals:
            self.append(tal)

# Classe base
class Player:
    '''Classe base de todos os jogadores'''
    # classe para os membros
    class Limb:                                             # Os membros são uma subclasse do jogador PQ SIM!
        '''
            Os membros são uma subclasse do jogador PQ SIM!

            Parâmetros:
                state_strings (lista de strings): Uma lista que contém o nome dos estados do membro
                health (int): Número que vai de 0 até len(state_strings)-1 e mostra quanto de vida tem este membro
                name (str): O nome do membro
        '''
        def __init__(self, state_strings, health, name):
            '''
                Parâmetros:
                    state_strings (lista de strings): Uma lista que contém o nome dos estados do membro
                    health (int): Número que vai de 0 até len(state_strings)-1 e mostra quanto de vida tem este membro
                    name (str): O nome do membro

                Após isto, ele gera o self.states que são sempre os mesmos jusntando os emojis
                em health_icons

            '''
            self.health = health                            # Cada membro vai ter a vida (número de 0 a 3)
            self.name = name                                # Um nome
            self.states = []                                # E uma lista de estados que cada entrada é uma string que vai representar cada estado, sendo o 0 o masi danificado e 3 o sem dano
            self.is_part_of_a_megabeast = False
            health_icons = [
                emojize(":cross_mark:"),
                emojize(":red_heart:"),
                emojize(":yellow_heart::yellow_heart:"),
                emojize(":green_heart::green_heart::green_heart:"),
                emojize(":green_heart::green_heart::green_heart:"),
                emojize(":green_heart::green_heart::green_heart:"),
                emojize(":green_heart::green_heart::green_heart:"),
                emojize(":green_heart::green_heart::green_heart:"),
                emojize(":green_heart::green_heart::green_heart:"),
            ]
            for i in range(0, len(state_strings)):          # state_strings é uma lista de strings que vai representar o estado de cada membro , dilacerado, cortado.. etc
                self.states.append(state_strings[i] + " " + health_icons[i])

    class BuffManager:                                      # Gerenciador de buff é também uma subclasse de jogador PQ SIM!
        '''
        Gerenciador de buff é também uma subclasse de jogador PQ SIM!

        Ele possui o states_list que é igual pra todo mundo.

        E, dependendo do buff_state, é representado um estado diferente
        representado pelas states list ou seja,
        o 0 representa o estado natural e o 7, o cosmic.

        '''
        def __init__(self):
            self.states_list = [emojize(":zzz: Natural :zzz:"),
                                emojize(":pile_of_poo: Slightly :pile_of_poo:"),
                                emojize(":OK_hand: Normally :OK_hand:"),
                                emojize(":flexed_biceps: Strongly :flexed_biceps:"),
                                emojize(":angry_face_with_horns: Satanic :angry_face_with_horns:"),
                                emojize(":smiling_face_with_halo: Godly :smiling_face_with_halo:"),
                                emojize(":bright_button: Cosmic :bright_button:")]
            self.buff_state = 0     # O 0 representa o estado natural. e o 7, o cosmic

    def __init__(self, chat_id, name="nameless"):
        '''
            Vamos la, cada jogador tem muita coisa. (ver os comentários)

            Parâmetros:
                chat_id (str): String que representa um número de identificação do usuário de telegram
                name (str): String que representa o nome do jogador

        '''
        self.bot = bot.TGBot()                          # Cada jogador vai ter uma instacia do bot
        self.chat_id = chat_id                          # O Chat id do telegram
        self.code = chat_id                             # Cópia do chat_id se o jogador não estiver em party. Se estiver code é setado para o ptcode. Usado para deixar o código mais limpo em forest.py etc.
        self.admlevel = 0                               # Nível de adm
        self.vanilla_class = "Unknown"
        self.classe = "Unknown"                         # A classe é uma string
        self.name = name                                # O nome do jogador
        self.atk = 1
        self.defense = 1                                # Ataque e defesa, level, experiencia
        self.stats = 2
        self.level = 1
        self.exp = 0
        self.hp = self.create_normal_limbs()            # Função que cria os membros do jogador
        self.weapon = None                              # A arma é um objeto weapon
        self.armor = None



        self.inventory = []                             # É uma lista de itens
        self.ghost_inv = []                             # É o inventário que conterá os itens não lendários do jogador após sua morte.
        self.pokedex = []                               # É uma lista de strings
        self.storage = OrganizedTalismanDB()
        self.pocoes = {"1a":[], "1b":[], "1c":[], "1d":[], "1e":[], "1f":[], "1g":[]}
        self.stat_multiplier = 1
        self.crit_chance = 20                           # Ver battle.py
        self.ap = 0                                     # Mana/stamina
        self.max_ap = 0
        self.levels = [0, 4, 64, 144, 384, 600, 2880, 3360, 3840, 4320, 4800, 5280, 12120, 13130, 14140,
                       15150, 16160, 17170, 18180, 19190, 20200, 21210*5, 21210*5, 22220*5, 23230*5, 24240*5, 25250*5,
                       26260*5, 27270*5, 28280*5, 29290*5, 30300*5, 31310*5, 32320*5, 33330*5, 34340*5, 35350*5, 36360*5, 37370*5,
                       38380*5, 39390*5, 40400*5, 56448*5, 57792*5, 59136*5, 60480*5, 61824*5, 63168*5, 64512*5, 65856*5, 67200*5]

        # self.bot = bot.TGBot()
        self.is_at_forest = False                       # Pra ver se está na floresta
        self.is_travelling = False                      # Pra ver se está usando um mapa
        self.has_died = False                           # Se o jogador morrer, esta variável será checada para retrace dos itens dropados.
        self.active = False
        self.travelling_loc = ""                        # O local que está viajando
        self.travel_time = 0                            # Quanto tempo falta pra chegar no local
        self.buff_man = self.BuffManager()              # Cria os buffs
        self.pt_code = ""
        self.pt_name = ""                               # Mais flags reduntantes pq n
        self.test = 1                                   # serve pra testar cosias
        self.referal = ""                               # O chat id que vc se referiu quando vc iniciou o jogo
        self.suc_refs = 0                               # Referênias indicadas por vc que chegaram no level 5
        self.location = "camp"      # can be "camp" "forest" "WB" On the future: "deep forest" "underground" "deep undergournd"
        self.prev_location = "camp" # Guarda o location anterior, ex: estava na floresta e entrou numa dungeon location muda de forest -> dungeon, e prev_location muda para forest.
        self.gender = 'male'
        self.sex_changes = 0
        self.has_bought_tsa = False
        self.special_inventory = {"bts": 0, "crs" : 0}

        self.att_points = {

            'unspent': 0,
            emojize(":flexed_biceps: Strength :flexed_biceps:"): 0,
            emojize(':brain: Intelligence :brain:'): 0,
            emojize(':eye: Dexterity :eye:'): 0,

        }

        self.stance = emojize("Agressive :crossed_swords:")        # A postura, "stance" pode ser tanto emojize("Agressive :crossed_swords:") ou emojize("Defensive :shield:")
        self.lvl_up_text =  ("Select an attribute to increase!\n\n"
                            "Attack increases your attack by one.\n"
                            "Defense increases your defense by one.")
        self.crit_boost = 0
        self.bonus_stats_for_inviting_players = 0
        self.is_synergyzed = False                  # Variável que muda quando o jogador possui mais 3 de sua classe na sua party
        self.arena_rank = 1
        self.arenas_left = 5
        self.max_arenas = 5
        self.last_megabeast_report = ""
        self.megabeast_target_limb = ""

        self.weapon_stat_boost = False

        self.longest_at_the_df = 0

        self.status_manager = status_ailments.StatusAilmentManager()

        self.new()

        self.status = []                             # Conterá os status negativos do player por localidade. Esta lista só se altera com a entrada e saída do player do local.

        self.leaves = 10
        self.stat_points = 0
        self.setting_can_get_talismans = False
        self.setting_percentage = 10

        self.average_time_between_dungeons = 0
        self.average_time_between_last_dungeons = 0
        self.average_times_taken = []
        self.last_done_dungeon_time = 0
        self.average_time_between_WB = self.average_time_between_dungeons/5
        self.last_dg_id = {}
        self.time_factor = 1
        self.last_wb_report = ""

        self.attacked_the_wb = False

    def __str__(self):
        text = emojize(f"{self.name}, a {self.classe} with {self.atk} :crossed_swords: {self.defense} :shield: wielding {self.weapon}")
        return text

    def __setattr__(self, name, value):
        if name == "location":
            try:
                present_location = getattr(self, "location")
                super(Player, self).__setattr__("prev_location", present_location)
            except AttributeError:
                # Única forma de dar attrError é quando o prev_location não foi criado
                # Isto é, o __init__ está rodando. Deixamos o init rodar normal pulando
                # o processo do prev_location.
                pass

        super(Player, self).__setattr__(name, value)

        if name == "status":        # Para efetivar o status no momento de entrada e saída do local.
            self.status_manager = status_ailments.StatusAilmentManager()
            self.calc_attributes()  # Também será chamado durante o init, então deixar o atributo como um dos últimos.

    def generate_stat_points(self):
        strongest = 0
        for weapon in self.inventory:
            if weapon.atributos[0] + weapon.atributos[1] > strongest:
                strongest = weapon.atributos[0] + weapon.atributos[1]

        i = 0
        # initial = self.stat_points
        while True:
            if i < len(self.inventory):
                weapon = self.inventory[i]
                if weapon.atributos[0] + weapon.atributos[1] < strongest * self.setting_percentage *1e-2:
                    if "talismans" in dir(weapon):
                        if self.weapon == weapon:
                            self.weapon.unequip(self)
                        if len(weapon.powers):
                            if self.setting_can_get_talismans:
                                for tal_name, tal in weapon.talismans.items():
                                    self.storage.append(copy.deepcopy(tal))
                                weapon.remove_talismans()
                                self.stat_points += weapon.atributos[0] + weapon.atributos[1]
                                del self.inventory[i]
                            else:
                                i += 1
                        else:
                            self.stat_points += weapon.atributos[0] + weapon.atributos[1]
                            del self.inventory[i]
                    else:
                        i += 1
                else:
                    i += 1
            else:
                break
        # if self.stat_points - initial:
        #     text = f"You transformed {self.stat_points - initial} weapon stats into stat coins."
        #     self.bot.send_message(text=text, chat_id=self.chat_id)






    def change_sex(self):
        if self.sex_changes < 10:
            self.sex_changes += 1
            if self.gender == 'male':
                self.gender = 'female'
            else:
                self.gender = 'male'
        else:
            self.gender = "hermaphrodite"

    def change_stance(self):
        if self.stance == emojize("Agressive :crossed_swords:"):
            self.stance = emojize("Defensive :shield:")
        else:
            self.stance = emojize("Agressive :crossed_swords:")

    def new(self):                                      # A vanilla class é criada
        '''
            Cada classe vai ter seu método new.
            Ele é executado toda vez no __init__
            e vai mudar o nome da classe e vai setar os att_points e os actions
        '''
        self.classe = self.vanilla_class
        self.att_points = {                             # Pro jogador sem class temos, 2 atributos q podem ser distribuidos, ataque e defesa
            "unspent": 0,
            emojize(":crossed_swords: Attack :crossed_swords:"): 0,
            emojize(":shield: Defense :shield:"): 0
        }
        self.actions = {}

    # Daqui pra baixo são funções criadas pra na hora de gerar um novo jogador na ora de trocar de classe

    def set_name(self, name):                           # Nani
        self.name = name

    def fail_healing_feedback(self):
        self.bot.send_message(text="You drank the potion, but you notice nothing.", chat_id = self.chat_id)

    def fail_buff_feedback(self):
        self.bot.send_message(text="You drank the potion, but you notice nothing.", chat_id = self.chat_id)

    def fail_buff_feedback2(self):
        self.bot.send_message(text="You drank the potion, you notice something, but its so small compared to your power that you ignored. You also used your immense power to materialize back the potion you just drank.", chat_id = self.chat_id)

    def succesfull_buff_feedback(self):
        self.bot.send_message(text="You drank the potion, now you're stronger.", chat_id = self.chat_id)

    def fail_refresh_feedback(self):
        self.bot.send_message(text="You drank the potion, but you notice nothing.", chat_id = self.chat_id)

    def drink_small_mana_pot(self):
        self.ap = min(self.ap+1, self.max_ap)
        self.bot.send_message(text="You drank the potion, now you have more energy.", chat_id = self.chat_id)

    def fail_mana_feedback(self):
        self.bot.send_message(text="You drank the potion, but you notice nothing.", chat_id = self.chat_id)




    def set_attributes(self, atk, defense, exp, level): # Seta estes atributos de uma vez só
        self.atk = atk
        self.defense = defense
        self.exp = exp
        self.level = level

    def set_hp(self, hp):
        self.hp = hp

    def set_quest(self, questing):                      # Não sei se isto é utilziado
        self.questing = questing

    def set_inventory(self, weapon, inventory, pokedex):
        self.weapon = weapon
        self.inventory = inventory
        self.pokedex = pokedex

    def set_adm(self, level):                           # Altera o nível de adm do jogador
        self.admlevel = level

    def new_from_player(self, player):                  # Método usado quando o jogador da level up ou atualiza o jogo
        '''
            Método usado para quando o jogador da level up

            Parâmetros:

                player (Player): Ele engole um jogador e vomita outro novo meio que cópia
        '''
        self.set_name(player.name)
        self.set_attributes(player.atk, player.defense, player.exp, player.level)
        self.set_hp(player.hp)
        self.set_inventory(player.weapon, player.inventory, player.pokedex)
        self.stat_points = player.stat_points
        self.admlevel = player.admlevel
        self.buff_man = player.buff_man
        self.referal = player.referal
        self.suc_refs = player.suc_refs
        self.arena_rank = player.arena_rank
        self.storage = copy.deepcopy(player.storage)
        self.pocoes = copy.deepcopy(player.pocoes)
        self.special_inventory = copy.deepcopy(player.special_inventory)
        self.leaves = player.leaves
        self.has_bought_tsa = player.has_bought_tsa
        try:
            setattr(self,"pt_code",getattr(player,"pt_code"))
        except AttributeError:
            setattr(self,"pt_code", "")
        try:
            setattr(self,"pt_name",getattr(player,"pt_name"))
        except AttributeError:
            setattr(self,"pt_name", "")
        for att, pts in self.att_points.items():
            self.att_points[att] = 0
        self.att_points["unspent"] = player.level - 1

    def clone_player(self, player):
        self.set_name(player.name)
        self.set_attributes(player.atk, player.defense, player.exp, player.level)
        self.set_hp(player.hp)
        self.set_inventory(player.weapon, player.inventory, player.pokedex)
        self.buff_man = player.buff_man
        self.admlevel = player.admlevel

    def create_normal_limbs(self):                                                  # Cria os membros de um jogador normal
        '''
            Cria os membros de um jogador Normal
            Cada membro tem 4 estados representados por strings
            Para criar um membro com mais hp, basta no hp botar o len(stats) - 1 e colocar mais estados na lista de stats
            O problema de criar um membro com mais de 4 de hp são os emojis de começo. Mas isso da pra mexer depois, caso alguma classe no futuro tenha algum talento que aumente a vida dos membros....
        '''
        arm_states = ["torn apart", "broken", "bruised", "fine"]                    # Cada membro tem 4 estados representados por strings
        left_arm = self.Limb(arm_states, 3, emojize("left arm :flexed_biceps:"))    # Para criar um membro com mais hp, basta no hp botar o len(stats) - 1 e colocar mais estados na lista de stats
        right_arm = self.Limb(arm_states, 3, emojize("right arm :flexed_biceps:"))

        chest_states = ["unrecognizable", "broken", "bruised", "fine"]
        chest = self.Limb(chest_states, 3, emojize("chest"))

        belly_states = ["cut open", "destroyed", "bruised", "fine"]
        belly = self.Limb(belly_states, 3, emojize("belly"))

        head_states = ["smashed", "broken", "bruised", "fine"]
        head = self.Limb(head_states, 3, emojize("head :neutral_face:"))

        leg_states = arm_states
        right_leg = self.Limb(leg_states, 3, emojize("right leg"))
        left_leg = self.Limb(leg_states, 3, emojize("left leg"))

        body = []
        body.append(left_arm)
        body.append(right_arm)
        body.append(left_leg)
        body.append(right_leg)
        body.append(chest)
        body.append(belly)
        body.append(head)

        return body


    def random_damaged_limb_index(self, hp):            # Pega uma membro aleatório com vida menor q 3 pra ser curado.
        '''
            Pega uma membro aleatório com vida menor q 3 pra ser curado.
            Se retornar -1, quer dizer que o jogador está com a vida cheia.

            Parâmetros:
                hp (lista de Limbs): Vida do jogador que será curado.



        '''
        limb_i = -1
        damaged_limbs = []
        for i in range(0, len(hp)):
            if hp[i].health < 3:
                damaged_limbs.append(i)

        if len(damaged_limbs) > 0:
            limb_i = damaged_limbs[rd.randint(0, len(damaged_limbs) - 1)]

        return limb_i                                   # Ele n cura o hp. Mas retorna o índice do membro

    def random_live_limb_index(self, hp):               # Mesma coisa, mas pra tirar vida
        '''
            Pega uma membro aleatório com vida maior q 0 pra tomar dano.
            Se retornar -1 quer dizer que o jogador morreu.

            Parâmetros:
                hp (lista de Limbs): Vida do jogador que levará dano.

        '''
        limb_i = -1
        live_limbs = []
        for i in range(0, len(hp)):
            if hp[i].health > 0:
                live_limbs.append(i)

        if len(live_limbs) > 0:
            limb_i = live_limbs[rd.randint(0, len(live_limbs) - 1)]

        return limb_i

    def calc_attributes(self):                          # Calcula os atributos pra classe vanilla. Cada classe vai ter a sua forma de calcular no fim.
        '''Calcula os atributos pra classe vanilla. Cada classe vai ter a sua forma de calcular os atributos'''
        self.atk = self.level + self.att_points[emojize(":crossed_swords: Attack :crossed_swords:")]*(self.buff_man.buff_state + 1)
        self.defense = self.level + self.att_points[emojize(":shield: Defense :shield:")]*(self.buff_man.buff_state + 1)
        if self.weapon:
            self.atk += self.weapon.atributos[0]*(self.buff_man.buff_state + 1)
            self.defense += self.weapon.atributos[1]*(self.buff_man.buff_state + 1)
        self.bonus_stats_for_inviting_players = min(self.suc_refs*0.01, 1)
        self.atk = round(self.atk*(1 + self.bonus_stats_for_inviting_players))
        self.defense = round(self.defense*(1 + self.bonus_stats_for_inviting_players))
        self.max_arenas = 5 + self.suc_refs
        # print(self.weapon)
        # print(self.armor)
        if self.status:
            for status in self.status:
                self.status_manager.status[status[0]](self, status[1])


        self.stats = self.atk + self.defense

    def get_stats_string(self, remtime):
        '''Cada classe vai ter uma forma diferente de printar o "/me"'''
        s = self.get_basic_stats_string(remtime)
        return s

    # def get_basic_stats_string(self, remtime):          # Stats string da classe vanilla que vai printar quando vc der o '/me'
    #     '''Stats string da classe vanilla que vai printar quando vc der o "/me". Todas as classes vão passar por essa'''
    #     self.calc_attributes()
    #     possible_status = {
    #         "cold": emojize(":snowflake: Cold :snowflake:")
    #     }
    #
    #     def return_status_string():
    #         status_s = ""
    #         if self.status:
    #             for status in self.status:
    #                 if status[1] >= 0:
    #                     status_s += possible_status[status[0]]
    #                     status_s += ", "
    #         if status_s:
    #             status_s = status_s[0:-2]
    #             return status_s
    #         else:
    #             return "None"
    #
    #     status_s = return_status_string()
    #
    #     weap_name = "None"
    #     weap_atk = 0
    #     weap_def = 0
    #     if self.weapon:
    #         weap_name = self.weapon.name
    #         weap_atk = self.weapon.atributos[0]
    #         weap_def = self.weapon.atributos[1]
    #     hours, minutes = divmod(remtime, 60)
    #     locations = {   "camp": emojize(":camping: Camp :camping:"),
    #                     "forest": emojize(f":deciduous_tree: Forest :deciduous_tree:\nYou will be back in {hours} hours and {minutes} minutes"),
    #                     "WB": emojize(":sunflower: *Helianth, the Sunny* :sunflower:\nTo escape, /run_away"), "arena": emojize(":crossed_swords: Arena :crossed_swords:\nTo exit: /exit_arena\nTo show win streak: /arena_win"),
    #                     "dungeon": emojize(":alien_monster: Dungeon :alien_monster:"),
    #                     "deep_forest": emojize(f":evergreen_tree: Deep forest, stay time: {hours} hours and {minutes} minutes"),
    #                     "megabeast": emojize(f":dragon_face: Facing a Megabeast.\n Don't forget to check your health periodically.\nTo check the status of the battle, /boss_battle. To leave the battle, use /leave_battle.\n")
    #                     }
    #
    #     s = (f"{self.name}\n\n"
    #          f"Location: {locations[self.location]}\n\n"
    #          f"Gender: {self.gender}\n"
    #          f"Attack: {self.atk}:crossed_swords:\n"
    #          f"Defense: {self.defense}:shield:\n"
    #          f"Stance: {self.stance}\n"
    #          f"Level: {self.level}:up_arrow:\n"
    #          f"Exp: {self.exp}/{self.levels[self.level]}:TOP_arrow:\n"
    #          f"Talent points : {self.att_points['unspent']}\n\n"
    #          # f":flexed_biceps: Strength :flexed_biceps: {self.att_points['unspent']}\n"
    #          # f":brain: Intelligence :brain: {self.att_points[emojize(':brain: Intelligence :brain:')]}\n"
    #          # f":eye: Dexterity :eye: {self.att_points[emojize(':eye: Dexterity :eye:')]}\n\n"
    #
    #          f"Class: {self.classe}\n"
    #          f"Equipped weapon:\n*{weap_name}* :crossed_swords:"
    #          f"{weap_atk} :shield:{weap_def}\n\n"
    #          f"Buff: {self.buff_man.states_list[self.buff_man.buff_state]}\n"
    #          f"Debuffs: {status_s}\n\n"
    #          f"Party name: {self.pt_name}\n\n"
    #          f"Party code: {self.pt_code}\n\n")
    #
    #
    #
    #     return s

    def get_basic_stats_string(self, remtime):          # Stats string da classe vanilla que vai printar quando vc der o '/me'
        '''Stats string da classe vanilla que vai printar quando vc der o "/me". Todas as classes vão passar por essa'''
        self.calc_attributes()
        possible_status = {
            "cold": [   emojize(":snowflake: Cold :snowflake:"),
                        emojize(":snowflake::snowflake: Colder :snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake: Freezing :snowflake::snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake::snowflake: Frost :snowflake::snowflake::snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake::snowflake::snowflake: Very Frost :snowflake::snowflake::snowflake::snowflake::snowflake:")],
            "hot": [    emojize(":sun: Warm :sun:"),
                        emojize(":smirking_face: Hot :smirking_face:"),
                        emojize(":fire: Hotter :fire:"),
                        emojize(":fire::fire: Melting :fire::fire:"),              # Debuffs
                                                                                    # Buffs
                        emojize(":bright_button::sun: Sun God :sun::bright_button:"),
                        emojize(":sun::sparkles: Sun Blessed :sun::sparkles:"),
                        emojize(":prohibited::fire: Fire Immune :prohibited::fire:"),
                        emojize(":smiling_face_with_sunglasses::thumbs_up::collision::fire:   Super Cool :smiling_face_with_sunglasses::thumbs_up::collision::fire: "),
                        emojize(":smiling_face_with_sunglasses::collision:  Cooler :smiling_face_with_sunglasses::collision: "),
                        emojize(":smiling_face_with_sunglasses:  Cool :smiling_face_with_sunglasses: "),
                        "None",
                        ]
        }

        def return_status_string():
            status_s = ""
            coiso = 0

            if self.status:
                for status in self.status:
                    if self.armor:
                        if status[0] in self.armor.status_protection:
                            coiso = self.armor.status_protection[status[0]]
                    #if status[1] - coiso >= 0:
                        status_s += possible_status[status[0]][status[1] - coiso]
                        status_s += ", "
            if status_s:
                status_s = status_s[0:-2]
                return status_s
            else:
                return "None"
        status_s = return_status_string()

        weap_name = "None"
        weap_atk = 0
        weap_def = 0
        if self.weapon:
            weap_name = self.weapon.name
            weap_atk = self.weapon.atributos[0]
            weap_def = self.weapon.atributos[1]
        hours, minutes = divmod(remtime, 60)

        locations = {   "camp": emojize(":camping: Camp :camping:"),
                        "forest": emojize(f":deciduous_tree: Forest :deciduous_tree:\nYou will be back in {hours} hours and {minutes} minutes"),
                        "WB": emojize(":snowflake: *Sairacaz, Blizzard Elemental* :snowflake:\nTo escape, /run_away"), "arena": emojize(":crossed_swords: Arena :crossed_swords:\nTo exit: /exit_arena\nTo show win streak: /arena_win"),
                        "dungeon": emojize(":alien_monster: Dungeon :alien_monster:"),
                        "deep_forest": emojize(f":evergreen_tree: Deep forest, stay time: {hours} hours and {minutes} minutes"),
                        "megabeast": emojize(f":dragon_face: Facing a Megabeast.\n Don't forget to check your health periodically.\nTo check the status of the battle, /boss_battle. To leave the battle, use /leave_battle.\n"),
                        "Blacksmith": emojize(f":hammer_and_wrench: Blacksmith :hammer_and_pick:"),
                        }

        s = (f"{self.name}\n\n"
             f"Location: {locations[self.location]}\n\n"
             f"Gender: {self.gender}\n"
             f"Attack: {self.atk}:crossed_swords:\n"
             f"Defense: {self.defense}:shield:\n"
             f"Stance: {self.stance}\n"
             f"Level: {self.level}:up_arrow:\n"
             f"Exp: {self.exp}/{self.levels[self.level]}:TOP_arrow:\n"
             f"Talent points : {self.att_points['unspent']}\n\n"
             # f":flexed_biceps: Strength :flexed_biceps: {self.att_points['unspent']}\n"
             # f":brain: Intelligence :brain: {self.att_points[emojize(':brain: Intelligence :brain:')]}\n"
             # f":eye: Dexterity :eye: {self.att_points[emojize(':eye: Dexterity :eye:')]}\n\n"

             f"Equipped weapon:\n*{weap_name}* :crossed_swords:"
             f"{weap_atk} :shield:{weap_def}\n\n"
             f"Stat Coins: {self.stat_points}\n\n"
             f"Buff: {self.buff_man.states_list[self.buff_man.buff_state]}\n\n"
             )
        if self.att_points['unspent']:
            s += "You have unspent talent points. use /lvlup to spend them.\n"




        return s


    def take_damage(self, dmg=1):                       # Cada classe vai ter o seu take_damage, principalmente o druida
        '''Cada classe vai ter o seu take_damage, principalmente o druida'''
        limb_i = self.random_live_limb_index(self.hp)
        if limb_i > -1:
            self.hp[limb_i].health -= dmg
            return limb_i
        else:
            return -1  # Diz que o jogador morreu, a floresta então apaga ele e tals

    def reset_stats(self):
        '''função q roda quando ele volta da floresta'''
        self.hp = self.create_normal_limbs()
        self.ap = 0
        self.buff_man.buff_state = 0
        self.status = []
        self.calc_attributes()

    def potion_reset_stats(self):
        '''função q roda quando ele volta da floresta'''
        self.reset_stats()
        text = "You drank the potion and you experience the same effect of entering the forest."
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def check_level_up(self):
        return (self.exp >= self.levels[self.level])  # or self.level == self.server.levelcap)

    def not_enough_ap(self):
        pass
        # print("Not enough will to live!")

    def print_self_coms(self):                                      # Mensagem enviada quando o jogador da o '/class'. Neste caso, sem classe, ele envia isso
        text = "You haven't learned enough to choose a class."
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def dg_coms(self):                                              # Mesma coisa quando está numa dungeon
        text = "You haven't learned enough to choose a class.\n\n"
        return text

    def life_steal(self):
        '''Cura de uma arma com life steal'''
        limb_i = self.random_damaged_limb_index(self.hp)
        if limb_i > -1:
            self.hp[limb_i].health += 1
            text = f"Your weapon healed your {self.hp[limb_i].name}"
            self.bot.send_message(text=text, chat_id=self.chat_id)

    def drink_pot(self):
        '''Cura de uma arma com life steal'''
        limb_i = self.random_damaged_limb_index(self.hp)
        if limb_i > -1:
            self.hp[limb_i].health += 1
            text = f"Glug glug. The potion healed your {self.hp[limb_i].name}"
            self.bot.send_message(text=text, chat_id=self.chat_id)
        text = "You are in perfect health. If you want an extra limb talk to your local druid."
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def drink_large_pot(self):
        for limb_i in range(len(self.hp)):
            self.hp[limb_i].health = len(self.hp[limb_i].states)-1
        text = "You drink the potion. Now you are full health."
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def drink_large_mana_pot(self):
        self.ap = self.max_ap
        text = "You drink the potion. Glug Glug Your eyes glow for a moment. Your body is entirely filled with energy."
        self.bot.send_message(text=text, chat_id=self.chat_id)

# Classe Knight, derivada de Player
class Knight(Player):   # Dentre as classes especializadas, é a mais simples.
    '''
        Classe Knight, derivada de Player
        Redefinimos somente algumas coisas, e definimos funções específicas

    '''
    # Redefinimos somente algumas coisas, e definimos funções específicas
    def new(self):                          # No init é rodado o new. onde é setado as novas funções e att e coisas e a classe
        '''No init é rodado o new. Onde é setado a classe, o ap desta classe, os atributos de classe e as ações desta classe.'''
        self.classe = "Knight"
        self.ap = 3
        self.max_ap = 3
        # self.att_points = {
        #
        #     "unspent": 0,
        #     emojize(":flexed_biceps: Strength :flexed_biceps:"): 0,
        #     emojize(":brain: Intelligence :brain:"): 0,
        #     emojize(":eye: Dexterity :eye:"): 0,
        #
        # }
        self.att_points = {
            "unspent": 0,
            emojize(":flexed_biceps: Strength :flexed_biceps:"): 0,
            emojize(":brain: Intelligence :brain:"): 0,
            emojize(":eye: Dexterity :eye:"): 0
        }
        self.actions = {"/heal_self": self.self_heal}       # As ações do '/class'
        self.lvl_up_text =  emojize("Select an attribute to increase!\n\n"
                            ":flexed_biceps: Strength :flexed_biceps: increases your melee weapon stat multiplier by 20%.\n"
                            ":brain: Intelligence :brain: increases your maximum stamina by one.\n"
                            ":eye: Dexterity :eye: increases your critical chance (2%).\n")

    def calc_attributes(self):          # Pra calcular o ataque, a defesa e, neste caso, o crit chance
        '''
            Usada para calcular o ataque, defese e a chance de crítico.

            No caso do knight, os atributos ataque e defesa são multiplicados por quantos pontos estão gastos em Weapon strenght boost
            E aumentado a chance de crítico baseado no Critical chance

        '''
        # print(self.weapon)
        # print(self.armor)

        max_crit_pts = 47
        over_crit = self.att_points[emojize(":eye: Dexterity :eye:")] - max_crit_pts
        self.stat_multiplier = 1
        if over_crit > 0:  # Só por segurança
            self.crit_boost = max_crit_pts*0.02
            if self.weapon and self.weapon.type2 == "melee":
                self.stat_multiplier = 1 + 0.2*(self.att_points[emojize(":flexed_biceps: Strength :flexed_biceps:")] + over_crit)
        else:
            self.crit_boost = self.att_points[emojize(":eye: Dexterity :eye:")]*0.02
            if  not self.weapon or self.weapon.type2 == "melee":
                self.stat_multiplier = 1 + 0.2*self.att_points[emojize(":flexed_biceps: Strength :flexed_biceps:")]

        if self.weapon:
            if self.weapon.type2 == "melee":
                self.atk = round(self.weapon.atributos[0]*self.stat_multiplier)*(self.buff_man.buff_state + 1)
                self.defense = round(self.weapon.atributos[1]*self.stat_multiplier)*(self.buff_man.buff_state + 1)
            else:
                self.atk = round(self.weapon.atributos[0]*self.stat_multiplier*(self.buff_man.buff_state/2 + 1))
                self.defense = round(self.weapon.atributos[1]*self.stat_multiplier*(self.buff_man.buff_state/2 + 1))

        else:
            self.atk = round(self.level*self.stat_multiplier)*(self.buff_man.buff_state + 1)
            self.defense = round(self.level*self.stat_multiplier)*(self.buff_man.buff_state + 1)

        self.max_ap = 3 + self.att_points[emojize(":brain: Intelligence :brain:")]

        self.bonus_stats_for_inviting_players = min(self.suc_refs*0.01, 1)
        self.atk = round(self.atk*(1 + self.bonus_stats_for_inviting_players))
        self.defense = round(self.defense*(1 + self.bonus_stats_for_inviting_players))
        if self.is_synergyzed:          # Precisa de uma forma de representar isso
            self.atk = round(self.atk*1.2)           # O synergyzed é ativado qd o jogador da um /party
            self.defense = round(self.defense*1.2)
        self.max_arenas = 5 + self.suc_refs

        if self.status:
            for status in self.status:
                self.status_manager.status[status[0]](self, status[1])

        self.stats = self.atk + self.defense

    def reset_stats(self):                      # Usado quando volta da floresta
        '''Usado quando volta da floresta'''
        self.hp = self.create_normal_limbs()
        self.ap = self.max_ap
        self.buff_man.buff_state = 0
        self.status = []
        self.calc_attributes()

    def not_enough_ap(self):                # Usado quando o tenta usar /heal e n tem stamina
        '''Usado quando o tenta usar /heal e n tem stamina'''
        #text = "You tried your best to heal your wounds, but your brain is hurting and you don't remember how to make some bandages."
        text = "You tried your best to heal your wounds, but your brain hurts and you don't know how to make bandages."
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def self_heal(self):
        '''Função executada quando o knight da /heal_self'''
        if self.ap > 0:
            self.heal_random_limb()
        else:
            self.not_enough_ap()

    def heal_random_limb(self):                                 # Cura do knight
        '''Cura do Knight para curar 1 de hp de um membro aleatório e manda a mensagem que foi curado ou se você está de vida cheia'''
        limb_i = self.random_damaged_limb_index(self.hp)
        if limb_i > -1:
            self.hp[limb_i].health += 1
            self.ap -= 1
            text = f"You heal your {self.hp[limb_i].name}"
            self.bot.send_message(text=text, chat_id=self.chat_id)
        else:
            text = "You really wanted to heal yourself, but nothing was damaged. You got a boost to your self-esteem instead."
            self.bot.send_message(text=text, chat_id=self.chat_id)

    def get_stats_string(self, remtime):                    # No caso do knight, ele pega as strings originais e bota o bonus de crit, stamina e bonus de dano
        '''Pra mostrar o "/me" do knight'''
        s = self.get_basic_stats_string(remtime)
        crit_perc = self.crit_boost*100 + 5
        s += (f"Stamina: {self.ap}/{self.max_ap}\n"
              f"Critical chance: {crit_perc}%\n"
              f"Weapon strength boost: {round(100*self.stat_multiplier)}%\n\n")

        return s

    def print_self_coms(self):          # '/class' pro knight
        '''Pra mostrar o "/class" do Knight'''
        s = (f"You\'re a living weapon, one that wields even more weapons. You\'ve trained intensely, day and night, to harden your body and reflexes in order to outperform the forest. Besides crushing skulls between your thighs, your only useful skill is focusing your mana to heal, but it's pretty tiring.\n\n"
            f"Stamina {self.ap}/{self.max_ap} :droplet:\n\n"
            f"You can:\n"
            f"Concentrate and /heal_self")
        self.bot.send_message(text=emojize(s), chat_id=self.chat_id)

    def dg_coms(self):
        '''Mesmo do de cima mas para dungeons'''
        s = f"Stamina {self.ap}/{self.max_ap} :droplet:\n"
        s += "You can /heal_self\n\n"

        return emojize(s)

    def sanctuary(self):            # Função quando o knight acha um santuário. Recuperando a stamina dele.
        '''Função quando o knight acha um santuário. Recuperando a stamina dele.'''
        s = "You found a small pond, there you took a rest, all stamina has been recovered."
        self.ap = self.max_ap
        self.bot.send_message(text=s,chat_id=self.chat_id)

    def get_basic_stats_string(self, remtime):          # Stats string da classe vanilla que vai printar quando vc der o '/me'
        '''Stats string da classe vanilla que vai printar quando vc der o "/me". Todas as classes vão passar por essa'''
        self.calc_attributes()
        possible_status = {
            "cold": [   emojize(":snowflake: Cold :snowflake:"),
                        emojize(":snowflake::snowflake: Colder :snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake: Freezing :snowflake::snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake::snowflake: Frost :snowflake::snowflake::snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake::snowflake::snowflake: Very Frost :snowflake::snowflake::snowflake::snowflake::snowflake:")],
            "hot": [    emojize(":sun: Warm :sun:"),
                        emojize(":smirking_face: Hot :smirking_face:"),
                        emojize(":fire: Hotter :fire:"),
                        emojize(":fire::fire: Melting :fire::fire:"),              # Debuffs
                                                                                    # Buffs
                        emojize(":bright_button::sun: Sun God :sun::bright_button:"),
                        emojize(":sun::sparkles: Sun Blessed :sun::sparkles:"),
                        emojize(":prohibited::fire: Fire Immune :prohibited::fire:"),
                        emojize(":smiling_face_with_sunglasses::thumbs_up::collision::fire:   Super Cool :smiling_face_with_sunglasses::thumbs_up::collision::fire: "),
                        emojize(":smiling_face_with_sunglasses::collision:  Cooler :smiling_face_with_sunglasses::collision: "),
                        emojize(":smiling_face_with_sunglasses:  Cool :smiling_face_with_sunglasses: "),
                        "None",
                        ]
        }

        def return_status_string():
            status_s = ""
            coiso = 0

            if self.status:
                for status in self.status:
                    if self.armor:
                        if status[0] in self.armor.status_protection:
                            coiso = self.armor.status_protection[status[0]]
                    #if status[1] - coiso >= 0:
                        status_s += possible_status[status[0]][status[1] - coiso]
                        status_s += ", "
            if status_s:
                status_s = status_s[0:-2]
                return status_s
            else:
                return "None"

        status_s = return_status_string()
        weap_name = "None"
        weap_atk = 0
        weap_def = 0
        if self.weapon:
            weap_name = self.weapon.name
            weap_atk = self.weapon.atributos[0]
            weap_def = self.weapon.atributos[1]
        hours, minutes = divmod(remtime, 60)
        locations = {   "camp": emojize(":camping: Camp :camping:"),
                        "forest": emojize(f":deciduous_tree: Forest :deciduous_tree:\nYou will be back in {hours} hours and {minutes} minutes"),
                        "WB": emojize(":sunflower: *Helianth, the Resurrected* :man_zombie:\nTo escape, /run_away"), "arena": emojize(":crossed_swords: Arena :crossed_swords:\nTo exit: /exit_arena\nTo show win streak: /arena_win"),
                        "dungeon": emojize(":alien_monster: Dungeon :alien_monster:"),
                        "deep_forest": emojize(f":evergreen_tree: Deep forest, stay time: {hours} hours and {minutes} minutes"),
                        "megabeast": emojize(f":dragon_face: Facing a Megabeast.\n Don't forget to check your health periodically.\nTo check the status of the battle, /boss_battle. To leave the battle, use /leave_battle.\n"),
                        "blacksmith": emojize(":hammer: Blacksmith :hammer_and_pick:"),
                        }
        if self.is_synergyzed:
            bonus = "20% bonus on Attack and Defense!"
        else:
            bonus = "nothing... (To have a synergy bonus, make a party with at least 2 knights in it)"
        s = (f"{self.name}\n\n"
             f"Location: {locations[self.location]}\n\n"
             f"Gender: {self.gender}\n"
             f"Attack: {self.atk}:crossed_swords:\n"
             f"Defense: {self.defense}:shield:\n"
             f"Stance: {self.stance}\n"
             f"Level: {self.level}:up_arrow:\n"
             f"Exp: {self.exp}/{self.levels[self.level]}:TOP_arrow:\n"
             f"Talent points : {self.att_points['unspent']}\n"
             f":flexed_biceps: Strength :flexed_biceps:: {self.att_points[emojize(':flexed_biceps: Strength :flexed_biceps:')]}\n"
             f":brain: Intelligence :brain:: {self.att_points[emojize(':brain: Intelligence :brain:')]}\n"
             f":eye: Dexterity :eye:: {self.att_points[emojize(':eye: Dexterity :eye:')]}\n\n"
             f"Class: {self.classe}\n"
             f"Equipped weapon:\n*{weap_name}* :crossed_swords:"
             f"{weap_atk} :shield:{weap_def}\n\n"
             f"Stat Coins: {self.stat_points}\n\n"
             f"Equipped armor:\n*{self.armor}*\n\n"
             f"Debuffs: {status_s}\n\n"
             f"Buff: {self.buff_man.states_list[self.buff_man.buff_state]}\n"
             # f"Debuffs: {status_s}\n\n"
             f"Party name: {self.pt_name}\n\n"
             f"Party code: {self.pt_code}\n\n"
             f"Synergy bonus: {bonus}\n\n")
        if self.att_points['unspent']:
            s += "You have unspent talent points. use /lvlup to spend them.\n"


        return s

# Classe Druid, derivada de Player
class Druid(Player):
    '''
        Classe Druid, derivada de Player.

        O Druida pode domesticar bestas e se curar.

    '''
    # Redefinimos somente algumas coisas, e definimos funções específicas
    def new(self):
        '''
            No new do Druid são criados as estruturas de tamed_beasts que são uma lista de bestas, definido o max_mana que pode ser aumentado com os talentos. Também é criado a estrutura de beast in stack

        '''
        self.classe = "Druid"
        self.ap = 5
        # self.att_points = {
        #     "unspent": 0,
        #     emojize(":wolf_face: Max. tamed beasts :wolf_face:"): 0,
        #     emojize(":dizzy: Max. Mana :dizzy:"): 0
        # }
        self.att_points = {
            "unspent": 0,
            emojize(":flexed_biceps: Strength :flexed_biceps:"): 0,
            emojize(":brain: Intelligence :brain:"): 0,
            emojize(":eye: Dexterity :eye:"): 0
        }

        self.actions = {"/heal": self.heal, "/tame": self.tame}
        self.max_ap = 5
        self.tamed_beasts = []
        self.tamed_legends = []
        self.tamed_megabeasts = []
        self.max_tamed_beasts = 1
        self.max_tamed_legends = 0
        self.beast_in_stack = None
        self.lvl_up_text =  emojize("Select an attribute to increase!\n\n"
                            ":flexed_biceps: Strength :flexed_biceps: increases your maximum tamed beasts every 3 points and melee weapon damage.\n"
                            ":brain: Intelligence :brain: increases your maximum mana by one and magical weapon damage.\n"
                            ":eye: Dexterity :eye: slightly increases critical (0.5%) chance and ranged weapon damage.\n")

    def calc_attributes(self):                                      # Calcula o ataque e a defesa
        '''
            Calcula os atributos para a classe do druida.

            Neste caso, o buff só se aplica no stats das bestas domesticadas

        '''
        # print(self.weapon)
        # print(self.armor)
        actual_points = round(self.att_points[emojize(":flexed_biceps: Strength :flexed_biceps:")]/3)
        self.max_tamed_beasts = 1 + actual_points
        self.max_ap = 5 + self.att_points[emojize(":brain: Intelligence :brain:")]
        self.crit_boost = self.att_points[emojize(":eye: Dexterity :eye:")]*0.005


        beasts_attack = 0
        beasts_defense = 0
        if len(self.tamed_beasts) > 0:
            for besta in self.tamed_beasts:
                beasts_attack += besta.atk*(self.buff_man.buff_state + 1)       # O buff só influencia do ataque e defesa das bestas.
                beasts_defense += besta.defense*(self.buff_man.buff_state + 1)
        if len(self.tamed_legends) > 0:
            for besta in self.tamed_legends:
                beasts_attack += besta.atk*(self.buff_man.buff_state + 1)       # O buff só influencia do ataque e defesa das bestas.
                beasts_defense += besta.defense*(self.buff_man.buff_state + 1)
        if len(self.tamed_megabeasts) > 0:
            for besta in self.tamed_megabeasts:
                beasts_attack += besta.attack*(self.buff_man.buff_state + 1)       # O buff só influencia do ataque e defesa das bestas.
                beasts_defense += besta.attack*(self.buff_man.buff_state + 1)

        if self.weapon:
            mult = 1
            if self.weapon.type2 == "melee":
                mult = 1 + self.att_points[emojize(":flexed_biceps: Strength :flexed_biceps:")]*0.05
            elif self.weapon.type2 == "magic":
                mult = 1 + self.att_points[emojize(":brain: Intelligence :brain:")]*0.05
            else:
                mult = 1 + self.att_points[emojize(":eye: Dexterity :eye:")]*0.05
            self.atk = round(self.weapon.atributos[0]*mult) + beasts_attack
            self.defense = self.weapon.atributos[1] + beasts_defense
        else:
            mult = 1 + self.att_points[emojize(":flexed_biceps: Strength :flexed_biceps:")]*0.05
            self.atk = round(7*mult) + beasts_attack
            self.defense = 8 + beasts_attack

        self.bonus_stats_for_inviting_players = min(self.suc_refs*0.01, 1)
        self.atk = round(self.atk*(1 + self.bonus_stats_for_inviting_players))
        self.defense = round(self.defense*(1 + self.bonus_stats_for_inviting_players))
        if self.is_synergyzed:
            self.max_tamed_legends = 1
        else:
            self.max_tamed_legends = 0
            if self.tamed_legends:
                self.tamed_legends = []
                text = "You lost the power of taming legendary beasts, and the one that has been tamed by you, just enraged itself and ran into the wild."
                self.bot.send_message(text = text, chat_id = self.chat_id)
        self.max_arenas = 5 + self.suc_refs
        if self.status:
            for status in self.status:
                self.status_manager.status[status[0]](self, status[1])
        self.stats = self.atk + self.defense

    def reset_stats(self):                      # Quando volta da floresta, ele solta as bestas domadas
        '''
            Quando volta da floresta, ele não solta as bestas domadas, mas só solta elas se ele entra na floresta

        '''
        self.hp = self.create_normal_limbs()
        self.ap = self.max_ap
        self.status = []
        if self.location == 'forest':
            self.tamed_beasts = []
            self.tamed_legends = []
            self.tamed_megabeasts = []
            self.beast_in_stack = None
        else:
            for besta in self.tamed_beasts:
                self.convert_beast_to_limb_and_append(besta)
            for besta in self.tamed_legends:
                self.convert_beast_to_limb_and_append(besta)
            for besta in self.tamed_megabeasts:
                self.convert_beast_to_limb_and_append(besta)
        self.buff_man.buff_state = 0
        self.calc_attributes()

    def not_enough_ap(self):
        '''Função executada pelo druida quando ele tenta soltar uma magia mas n tem mana suficiente'''
        text = "You tried, but you are exausted."
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def heal(self):
        '''Função de cura do druida'''
        if self.ap > 0:
            self.heal_random_limb()
        else:
            self.not_enough_ap()

    def heal_random_limb(self):                         # Função de cura é a mesma.
        '''
            A cura do druida cura um membro em 100%

        '''
        w_limb = -1
        w_limb_damage = 0
        for limb_i in range(len(self.hp)):
            if (len(self.hp[limb_i].states) - 1 - self.hp[limb_i].health) > w_limb_damage:
                w_limb = limb_i
                w_limb_damage = (len(self.hp[limb_i].states) - 1 - self.hp[limb_i].health)

        limb_i = w_limb  # self.random_damaged_limb_index(self.hp)
        if limb_i > -1:
            self.hp[limb_i].health = len(self.hp[limb_i].states)-1
            self.ap -= 1
            text = f"You succesfully healed your {self.hp[limb_i].name}"
            self.bot.send_message(text=text, chat_id=self.chat_id)
        else:
            text = "You're in perfect health"
            self.bot.send_message(text=text, chat_id=self.chat_id)

    def take_damage(self, dmg=1):                           # Take damage muda um pouco, por causa da exceção de quando um bicho seu morre
        '''
            O take damage pode causar a morte de uma besta domesticada.
            Ai ao invés de retornar um inteiro falando qual membro foi danificado ele fala o nome da besta que morreu.

        '''
        limb_i = self.random_live_limb_index(self.hp)
        self.beast_in_stack = None
        if limb_i > -1:
            self.hp[limb_i].health -= dmg
            dead_beast = self.check_tamed_beast_states()
            if dead_beast:
                self.calc_attributes()
                return dead_beast
            else:
                return limb_i
        else:
            return -1  # Diz que o jogador morreu, a floresta então apaga ele e tals

    def tame(self):
        '''Função pra domesticar uma besta que está em beast_in_stack'''
        if self.beast_in_stack is not None:
            if self.ap > 1:
                self.ap -= 2
                # print(self.beast_in_stack.is_legendary and len(self.tamed_legends) < self.max_tamed_legends)
                # print(len(self.tamed_legends))
                # print(self.max_tamed_legends)
                # print(not self.beast_in_stack.is_legendary and len(self.tamed_beasts) < self.max_tamed_beasts)
                # print(len(self.tamed_beasts))
                # print(self.max_tamed_beasts)
                if (not self.beast_in_stack.is_legendary and (len(self.tamed_beasts)+len(self.tamed_megabeasts)) < self.max_tamed_beasts) or (self.beast_in_stack.is_legendary and len(self.tamed_legends) < self.max_tamed_legends):
                    if not isinstance(self.beast_in_stack, deep_beastsdb.Megabeast):
                        if self.beast_in_stack.is_legendary:
                            self.tamed_legends.append(self.beast_in_stack)
                        else:
                            self.tamed_beasts.append(self.beast_in_stack)               # Ele só apenda a besta na lista
                        self.convert_beast_to_limb_and_append(self.beast_in_stack)
                        text = f"succesfully tamed {self.beast_in_stack.tipo}"
                        self.bot.send_message(text=text, chat_id=self.chat_id)
                        self.beast_in_stack = None
                    else:
                        if len(self.tamed_megabeasts) < 3:
                            self.tamed_megabeasts.append(self.beast_in_stack)
                            self.convert_beast_to_limb_and_append(self.beast_in_stack)
                            text = f"succesfully tamed {self.beast_in_stack.name}"
                            self.bot.send_message(text=text, chat_id=self.chat_id)
                            self.beast_in_stack = None
                        else:
                            text = "You already tamed 3 megabeasts. You dont have enough power."
                            self.bot.send_message(text=text, chat_id=self.chat_id)
                else:
                    text = "Your power does not support taming more beasts"
                    self.ap+=2
                    self.bot.send_message(text=text, chat_id=self.chat_id)
            else:
                self.not_enough_ap()

        else:
            text = "No tamable beasts nearby"
            self.bot.send_message(text=text, chat_id=self.chat_id)

    def get_stats_string(self, remtime):                            # Adiciona coisas no '/me' se o jogador for um druida
        '''Adiciona coisas no '/me' se o jogador for um druida'''
        s = self.get_basic_stats_string(remtime)
        s += (f"Mana: {self.ap}/{self.max_ap}\n"
              f"Max. tamed beasts: {self.max_tamed_beasts}\n\n")

        return s

    def print_self_coms(self):
        '''"/class" de um Druida'''
        s = "Your affinity with nature allows you to blend into the forest almost like you're a part of it. Always in tune with all forms of life, you feel like you could stay away from camp forever. As you spend so much time in the company of beasts rather than people, you have come to understand their thoughts; and they, yours.\n\n"
        s += f"Mana {self.ap}/{self.max_ap}\n\nYou can:"
        beast = self.beast_in_stack
        b_str = "None"
        if beast is not None:
            if isinstance(self.beast_in_stack, deep_beastsdb.Megabeast):
                b_str = self.beast_in_stack.name
            else:
                b_str = self.beast_in_stack.tipo
        s += f"Attempt to /tame a felled beast: {b_str}\n"
        s += f"/heal your most damaged limb"

        self.bot.send_message(text=s, chat_id=self.chat_id)

    def dg_coms(self):
        '''comandos printados quando o druida está em uma dungeon'''
        beast = self.beast_in_stack
        b_str = "None"
        if beast is not None:
            b_str = self.beast_in_stack.tipo
        s = f"Mana {self.ap}/{self.max_ap} :droplet:\n"
        s += "Choose an ability to use:\n\n"
        s += f"Attempt to /tame a felled beast: {b_str}\n"
        s += f"/heal your most damaged limb \n\n"

        return emojize(s)

    def limb_states_generator(self, health):
        base = ["destroyed"]
        states = ["holy crap this limb got health", "cut open", "dismantled", "badly injured", "damaged", "injured", "bruised", "fine"]
        base.extend(states[-health:])
        return base


    def convert_beast_to_limb_and_append(self, beast):
        '''Comando usado para transformar uma besta em um membro'''
        if isinstance(beast, deep_beastsdb.Megabeast):
            # print(beast.original_limb)
            # print(beast.limbs)
            for limb,health in beast.original_limb.items():
                # print(health)
                limb_states = self.limb_states_generator(health)
                newlimb = Player.Limb(limb_states, health, f"{beast.name}'s {limb}")
                newlimb.is_part_of_a_megabeast = True
                self.hp.append(newlimb)
        else:
            beast_states = ["gone", "heavily injured", "injured", "fine"]
            newlimb = Player.Limb(beast_states, 3, beast.tipo)
            self.hp.append(newlimb)

    def check_tamed_beast_states(self):
        '''Ele checa se uma besta morreu. Se sim, ele retorna o nome da besta, caso contrário, ele retorna False'''
        for i in range(7, len(self.hp)):
            if self.hp[i].health == 0 and not self.hp[i].is_part_of_a_megabeast:

                b_name = self.hp[i].name
                del self.hp[i]
                for besta in range(len(self.tamed_beasts)):
                    if self.tamed_beasts[besta].tipo == b_name:
                        del self.tamed_beasts[besta]
                        break
                return b_name

        return False

    def sanctuary(self):
        '''Santuário pro Druida'''
        s = "You found a mana sanctuary. All Mana has been restored!"
        self.ap=self.max_ap
        self.bot.send_message(text=s,chat_id=self.chat_id)

    def get_basic_stats_string(self, remtime):          # Stats string da classe vanilla que vai printar quando vc der o '/me'
        '''Stats string da classe vanilla que vai printar quando vc der o "/me". Todas as classes vão passar por essa'''
        self.calc_attributes()
        possible_status = {
            "cold": [   emojize(":snowflake: Cold :snowflake:"),
                        emojize(":snowflake::snowflake: Colder :snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake: Freezing :snowflake::snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake::snowflake: Frost :snowflake::snowflake::snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake::snowflake::snowflake: Very Frost :snowflake::snowflake::snowflake::snowflake::snowflake:")],
            "hot": [    emojize(":sun: Warm :sun:"),
                        emojize(":smirking_face: Hot :smirking_face:"),
                        emojize(":fire: Hotter :fire:"),
                        emojize(":fire::fire: Melting :fire::fire:"),              # Debuffs
                                                                                    # Buffs
                        emojize(":bright_button::sun: Sun God :sun::bright_button:"),
                        emojize(":sun::sparkles: Sun Blessed :sun::sparkles:"),
                        emojize(":prohibited::fire: Fire Immune :prohibited::fire:"),
                        emojize(":smiling_face_with_sunglasses::thumbs_up::collision::fire:   Super Cool :smiling_face_with_sunglasses::thumbs_up::collision::fire: "),
                        emojize(":smiling_face_with_sunglasses::collision:  Cooler :smiling_face_with_sunglasses::collision: "),
                        emojize(":smiling_face_with_sunglasses:  Cool :smiling_face_with_sunglasses: "),
                        "None",
                        ]
        }

        def return_status_string():
            status_s = ""
            coiso = 0

            if self.status:
                for status in self.status:
                    if self.armor:
                        if status[0] in self.armor.status_protection:
                            coiso = self.armor.status_protection[status[0]]
                    #if status[1] - coiso >= 0:
                        status_s += possible_status[status[0]][status[1] - coiso]
                        status_s += ", "
            if status_s:
                status_s = status_s[0:-2]
                return status_s
            else:
                return "None"

        status_s = return_status_string()
        weap_name = "None"
        weap_atk = 0
        weap_def = 0
        if self.weapon:
            weap_name = self.weapon.name
            weap_atk = self.weapon.atributos[0]
            weap_def = self.weapon.atributos[1]
        hours, minutes = divmod(remtime, 60)
        locations = {   "camp": emojize(":camping: Camp :camping:"),
                        "forest": emojize(f":deciduous_tree: Forest :deciduous_tree:\nYou will be back in {hours} hours and {minutes} minutes"),
                        "WB": emojize(":snowflake: *Sairacaz, Blizzard Elemental* :snowflake:\nTo escape, /run_away"), "arena": emojize(":crossed_swords: Arena :crossed_swords:\nTo exit: /exit_arena\nTo show win streak: /arena_win"),
                        "dungeon": emojize(":alien_monster: Dungeon :alien_monster:"),
                        "deep_forest": emojize(f":evergreen_tree: Deep forest, stay time: {hours} hours and {minutes} minutes"),
                        "megabeast": emojize(f":dragon_face: Facing a Megabeast.\n Don't forget to check your health periodically.\nTo check the status of the battle, /boss_battle. To leave the battle, use /leave_battle.\n"),
                        "Blacksmith": emojize(f":hammer_and_wrench: Blacksmith :hammer_and_pick:"),
                        }

        if self.is_synergyzed:
            bonus = "Able to tame one legendary beast!"
        else:
            bonus = "nothing...(To have a synergy bonus, make a party with at least 2 druids in it)"
        s = (f"{self.name}\n\n"
             f"Location: {locations[self.location]}\n\n"
             f"Gender: {self.gender}\n"
             f"Attack: {self.atk}:crossed_swords:\n"
             f"Defense: {self.defense}:shield:\n"
             f"Stance: {self.stance}\n"
             f"Level: {self.level}:up_arrow:\n"
             f"Exp: {self.exp}/{self.levels[self.level]}:TOP_arrow:\n"
             f"Talent points : {self.att_points['unspent']}\n"
             f":flexed_biceps: Strength :flexed_biceps:: {self.att_points[emojize(':flexed_biceps: Strength :flexed_biceps:')]}\n"
             f":brain: Intelligence :brain:: {self.att_points[emojize(':brain: Intelligence :brain:')]}\n"
             f":eye: Dexterity :eye:: {self.att_points[emojize(':eye: Dexterity :eye:')]}\n\n"
             f"Class: {self.classe}\n"
             f"Equipped weapon:\n*{weap_name}* :crossed_swords:"
             f"{weap_atk} :shield:{weap_def}\n\n"
             f"Stat Coins: {self.stat_points}\n\n"
             f"Equipped armor:\n*{self.armor}*\n\n"
             f"Debuffs: {status_s}\n\n"
             f"Buff: {self.buff_man.states_list[self.buff_man.buff_state]}\n\n"
             f"Party name: {self.pt_name}\n\n"
             f"Party code: {self.pt_code}\n\n"
             f"Synergy bonus: {bonus}\n\n")
        if self.att_points['unspent']:
            s += "You have unspent talent points. use /lvlup to spend them.\n"

        return s


class Explorer(Player):
    # Redefinimos somente algumas coisas, e definimos funções específicas
    def new(self):
        '''Para o caso do explorer, ele consegue se curar e usar o travel book pra revisitar os lugares'''
        self.classe = "Explorer"
        # self.att_points = {
        #     "unspent": 0,
        #     emojize(":game_die: Rare chance :game_die:"): 0,
        #     emojize(":warning: More encounters :warning:"): 0
        # }
        self.att_points = {
            "unspent": 0,
            emojize(":flexed_biceps: Strength :flexed_biceps:"): 0,
            emojize(":brain: Intelligence :brain:"): 0,
            emojize(":eye: Dexterity :eye:"): 0
        }
        self.actions = {"/heal": self.heal}
        self.prob_boost = 1
        self.enc_time_multiplier = 1
        self.time_reduction = 0
        self.travel_book = []
        self.ap = 3
        self.max_ap = 3
        self.travelkid = travelman.BasicTravelMan()
        self.e_travel_time = self.travelkid.def_travel_time
        self.lvl_up_text =  emojize("Select an attribute to increase!\n\n"
                            ":flexed_biceps: Strength :flexed_biceps: slightly increases melee weapon damage.\n"
                            ":brain: Intelligence :brain: increases your probability of finding rare encounters and reduce travel time.\n"
                            ":eye: Dexterity :eye: increases your encounter rate and ranged weapon damage by 20%\n")
        self.given_bonus = False

    def calc_attributes(self):
        '''O buff do explorer vai pra bonus de encontros e defesa'''
        # print(self.weapon)
        # print(self.armor)
        self.prob_boost = self.att_points[emojize(":brain: Intelligence :brain:")]*(self.buff_man.buff_state + 1)
        self.enc_time_multiplier = 1+0.1*self.att_points[emojize(":eye: Dexterity :eye:")]
        self.time_reduction = self.att_points[emojize(":brain: Intelligence :brain:")]
        self.e_travel_time = -self.travelkid.def_travel_time*10/(-10 - self.time_reduction)
        self.time_factor = self.e_travel_time/self.travelkid.def_travel_time
        if self.weapon:
            mult = 1
            if self.weapon.type2 == "melee":
                mult = 1 + self.att_points[emojize(":flexed_biceps: Strength :flexed_biceps:")]*0.05
            elif self.weapon.type2 == "ranged":
                mult = 1 + self.att_points[emojize(":eye: Dexterity :eye:")]*0.2
            self.atk = round(self.weapon.atributos[0]*mult)
            self.defense = self.weapon.atributos[1]*(self.buff_man.buff_state + 1)
        else:
            mult = 1 + self.att_points[emojize(":flexed_biceps: Strength :flexed_biceps:")]*0.05
            self.atk = round(7*mult)
            self.defense = 8*(self.buff_man.buff_state + 1)

        self.bonus_stats_for_inviting_players = min(self.suc_refs*0.01, 1)
        self.atk = round(self.atk*(1 + self.bonus_stats_for_inviting_players))
        self.defense = round(self.defense*(1 + self.bonus_stats_for_inviting_players))
        if self.is_synergyzed:
            # print("is_synergized")
            if not self.given_bonus:
                # print("bonus_not given")
                for att,points in self.att_points.items():
                    if att != "unspent":
                        # print(f"att: {att} is boosted")
                        self.att_points[att] += 1
                self.given_bonus = True
        else:
            # print("not is_synergyzed")
            if self.given_bonus:
                # print("bonus is given")
                for att,points in self.att_points.items():
                    if att != "unspent":
                        # print(f"att {att} is reduced")
                        self.att_points[att] -= 1
                        if self.att_points[att] < 0:
                            self.att_points[att] = 0
                self.given_bonus = False
        self.max_arenas = 5 + self.suc_refs
        if self.status:
            for status in self.status:
                self.status_manager.status[status[0]](self, status[1])
        self.stats = self.atk + self.defense

    def reset_stats(self):
        '''Função que roda quando o explorer retorna da floresta'''
        self.hp = self.create_normal_limbs()
        self.ap = 3
        self.buff_man.buff_state = 0
        self.status = []
        self.calc_attributes()

    def not_enough_ap(self):
        '''Função que roda quando o explorer ta sem mana'''
        text = "You started to hear voices around you. Your hand are sweaty. You need a break, not enought stamina."
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def heal(self):
        '''Função de cura do explorer'''
        if self.ap > 0:
            self.heal_random_limb()
        else:
            self.not_enough_ap()

    def heal_random_limb(self):
        '''O explorer vai curar 3 corações sempre'''
        # limb_i = self.random_damaged_limb_index(self.hp)
        # if limb_i > -1:
        #     self.hp[limb_i].health += 1
        # else:
        #     print("No limbs are damaged!")
        w_limb = -1
        w_limb_health = 3
        for limb_i in range(len(self.hp)):
            if self.hp[limb_i].health < w_limb_health:
                w_limb = limb_i
                w_limb_health = self.hp[limb_i].health

        limb_i = w_limb  # self.random_damaged_limb_index(self.hp)
        if limb_i > -1:
            self.hp[limb_i].health = 3
            self.ap -= 1
            text = f"You succesfully healed your {self.hp[limb_i].name}"
            self.bot.send_message(text=text, chat_id=self.chat_id)
        else:
            text = "You're in perfect health"
            self.bot.send_message(text=text, chat_id=self.chat_id)

    def add_to_travel_book(self, loc):
        '''Ao visitar um lugar, roda esta função pra adicionar o local no travel book'''
        self.travel_book.append(loc)
        self.create_coms(loc)

    def remove_from_travel_book(self, loc):
        '''Ao chegar a um lugar após viagem pelo comando /g_loc, roda esta função pra remover do travel book'''
        self.travel_book.remove(loc)
        del self.actions[f"/g_{loc}"]

    def get_stats_string(self, remtime):
        '''Função que vai printar o "/me" do explorer'''
        s = self.get_basic_stats_string(remtime)
        s += (f"Stamina: {self.ap}/3\n"
              f"Time Reduction percentage: {round(100 - self.time_factor*100)}%\n"
              f"Rare encounter boost: {self.prob_boost*10}%\n"
              f"Encounter rate: {self.enc_time_multiplier*100:.0f}%\n\n")

        return s

    def create_coms(self, encounter):
        '''Função que vai adiconar no actions do explorer os "/g_lugar" quando ele achar estes lugares'''
        if encounter == "dg":
            self.actions["/g_dg"] = self.travel_to_dg
        elif encounter == "bs":
            self.actions["/g_bs"] = self.travel_to_bs
        elif encounter == "plot_msg":
            self.actions["/g_sunflower"] = self.travel_to_plot_msg
        elif encounter == "sanct":
            self.actions["/g_sanct"] = self.travel_to_sanct
        elif encounter == "deep_forest":
            self.actions["/g_deep_forest"] = self.travel_to_df

    def print_self_coms(self):
        '''Método pra mostrar o "/class" do explorer'''
        text = ("You were never strong enough to stand up to the threats of the forest; thus, you sought other means to make your way around. Through wit and ingenuity, you learned to navigate the treacherous landscape. You're familiar enough with the surrounding area to remember a few locations, although they seem to change from time to time...\n\n"
                f"Stamina {self.ap}/3\n\n"
                f"You can:\n")
        text += "Mix some herbs to /heal yourself\n\n"
        if self.pt_code:
            text += "To heal a teammate, /heal (chat_id) or.. \n\n"
        text += "Visit a recent location\n\n"
        for loc in self.travel_book:
            if loc == "plot_msg":
                text += f"/g_sunflower\n"
            else:
                text += f"/g_{loc}\n"
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def dg_coms(self):
        '''Método usado pro explorer printar o "/class" numa dungeon'''
        text = f"Stamina {self.ap}/{self.max_ap} :droplet:\n"
        text += "Do you want to heal? /heal \n\n"
        if self.pt_code:
            text += "To heal a teammate, /heal (chat_id).\n"
        return emojize(text)

    def travel_to_dg(self):
        '''Método do explorer pra ele viajar pra dg'''
        if self.pt_code:
            pass

        if self.location == "forest":
            self.travelkid.set_travel(self, "dg")
            self.bot.send_message(text=f"You used the map to the dungeon, you will get there in {round(self.travel_time/60)} minutes", chat_id=self.chat_id)

        else:
            self.bot.send_message(text="You need to be at the forest to activate the travel book.", chat_id=self.chat_id)

    def travel_to_plot_msg(self):
        '''Método do explorer pra ele viajar pra sunflower'''
        if self.pt_code:
            pass

        if self.location == "forest":
            self.travelkid.set_travel(self, "plot_msg")
            self.bot.send_message(text=f"You used the map to the sunflower, you will get there in {round(self.travel_time/60)} minutes", chat_id=self.chat_id)

        else:
            self.bot.send_message(text="You need to be at the forest to activate the travel book.", chat_id=self.chat_id)


    def travel_to_bs(self):
        '''Método do explorer pra ele viajar pro blacksmith'''
        if self.pt_code:
            self.bot.send_message(text="You are in a party now. Blacksmiths can only serve one at a time.", chat_id=self.chat_id)
            return False


        if self.location == "forest":
            self.travelkid.set_travel(self, "bs")
            self.bot.send_message(text=f"You used the map to the blacksmith, you will get there in {round(self.travel_time/60)} minutes", chat_id=self.chat_id)

        else:
            self.bot.send_message(text="You need to be at the forest to activate the travel book.", chat_id=self.chat_id)
    def travel_to_sanct(self):
        ''' Método do explorer para viajar ao santuário'''
        if self.pt_code:
            pass

        if self.location == "forest":
            self.travelkid.set_travel(self, "sanct")
            self.bot.send_message(text=f"You used the map to the sanctuary, you will get there in {round(self.travel_time/60)} minutes", chat_id=self.chat_id)

        else:
            self.bot.send_message(text="You need to be at the forest to activate the travel book.", chat_id=self.chat_id)

    def travel_to_df(self):
        ''' Método para viajar à deep forest. '''
        if self.pt_code:
            pass

        if self.location == "forest":
            self.travelkid.set_travel(self, "deep_forest")
            self.bot.send_message(text=f"You used the map to the deep_forest, you will get there in {round(self.travel_time/60)} minutes", chat_id=self.chat_id)

        else:
            self.bot.send_message(text="You need to be at the forest to activate the travel book.", chat_id=self.chat_id)
    def chegou(self, location):
        '''Método do explorer pra quando ele chegar em algum lugar, remover no travel book e dos actions'''

        # print(self.travel_book)
        if location in self.travel_book:
            self.travel_book.remove(location)
        if location == "plot_msg":
            location = "sunflower"
        if f"/g_{location}" in self.actions:
            del self.actions[f"/g_{location}"]
        self.travelkid.arrive(self)

    def sanctuary(self):
        '''Santuário pro Explorer'''
        s = "You found a small pond, there you took a rest, all stamina has been recovered."
        self.ap=3
        self.bot.send_message(text=s,chat_id=self.chat_id)

    def get_basic_stats_string(self, remtime):          # Stats string da classe vanilla que vai printar quando vc der o '/me'
        '''Stats string da classe vanilla que vai printar quando vc der o "/me". Todas as classes vão passar por essa'''
        self.calc_attributes()
        possible_status = {
            "cold": [   emojize(":snowflake: Cold :snowflake:"),
                        emojize(":snowflake::snowflake: Colder :snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake: Freezing :snowflake::snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake::snowflake: Frost :snowflake::snowflake::snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake::snowflake::snowflake: Very Frost :snowflake::snowflake::snowflake::snowflake::snowflake:")],
            "hot": [    emojize(":sun: Warm :sun:"),
                        emojize(":smirking_face: Hot :smirking_face:"),
                        emojize(":fire: Hotter :fire:"),
                        emojize(":fire::fire: Melting :fire::fire:"),              # Debuffs
                                                                                    # Buffs
                        emojize(":bright_button::sun: Sun God :sun::bright_button:"),
                        emojize(":sun::sparkles: Sun Blessed :sun::sparkles:"),
                        emojize(":prohibited::fire: Fire Immune :prohibited::fire:"),
                        emojize(":smiling_face_with_sunglasses::thumbs_up::collision::fire:   Super Cool :smiling_face_with_sunglasses::thumbs_up::collision::fire: "),
                        emojize(":smiling_face_with_sunglasses::collision:  Cooler :smiling_face_with_sunglasses::collision: "),
                        emojize(":smiling_face_with_sunglasses:  Cool :smiling_face_with_sunglasses: "),
                        "None",
                        ]
        }

        def return_status_string():
            status_s = ""
            coiso = 0

            if self.status:
                for status in self.status:
                    if self.armor:
                        if status[0] in self.armor.status_protection:
                            coiso = self.armor.status_protection[status[0]]
                    #if status[1] - coiso >= 0:
                        status_s += possible_status[status[0]][status[1] - coiso]
                        status_s += ", "
            if status_s:
                status_s = status_s[0:-2]
                return status_s
            else:
                return "None"

        status_s = return_status_string()
        weap_name = "None"
        weap_atk = 0
        weap_def = 0
        if self.weapon:
            weap_name = self.weapon.name
            weap_atk = self.weapon.atributos[0]
            weap_def = self.weapon.atributos[1]
        hours, minutes = divmod(remtime, 60)
        locations = {   "camp": emojize(":camping: Camp :camping:"),
                        "forest": emojize(f":deciduous_tree: Forest :deciduous_tree:\nYou will be back in {hours} hours and {minutes} minutes"),
                        "WB": emojize(":snowflake: *Sairacaz, Blizzard Elemental* :snowflake:\nTo escape, /run_away"), "arena": emojize(":crossed_swords: Arena :crossed_swords:\nTo exit: /exit_arena\nTo show win streak: /arena_win"),
                        "dungeon": emojize(":alien_monster: Dungeon :alien_monster:"),
                        "deep_forest": emojize(f":evergreen_tree: Deep forest, stay time: {hours} hours and {minutes} minutes"),
                        "megabeast": emojize(f":dragon_face: Facing a Megabeast.\n Don't forget to check your health periodically.\nTo check the status of the battle, /boss_battle. To leave the battle, use /leave_battle.\n"),
                        "Blacksmith": emojize(f":hammer_and_wrench: Blacksmith :hammer_and_pick:"),
                        }

        if self.is_synergyzed:
            bonus = "1 extra point in strength, inteligence and dexterity."
        else:
            bonus = "nothing...(To have a synergy bonus, make a party with at least 2 explorers in it)"

        s = (f"{self.name}\n\n"
             f"Location: {locations[self.location]}\n\n"
             f"Gender: {self.gender}\n"
             f"Attack: {self.atk}:crossed_swords:\n"
             f"Defense: {self.defense}:shield:\n"
             f"Stance: {self.stance}\n"
             f"Level: {self.level}:up_arrow:\n"
             f"Exp: {self.exp}/{self.levels[self.level]}:TOP_arrow:\n"
             f"Talent points : {self.att_points['unspent']}\n"
             f":flexed_biceps: Strength :flexed_biceps:: {self.att_points[emojize(':flexed_biceps: Strength :flexed_biceps:')]}\n"
             f":brain: Intelligence :brain:: {self.att_points[emojize(':brain: Intelligence :brain:')]}\n"
             f":eye: Dexterity :eye:: {self.att_points[emojize(':eye: Dexterity :eye:')]}\n\n"
             f"Class: {self.classe}\n"
             f"Equipped weapon:\n*{weap_name}* :crossed_swords:"
             f"{weap_atk} :shield:{weap_def}\n\n"
             f"Stat Coins: {self.stat_points}\n\n"
             f"Equipped armor:\n*{self.armor}*\n\n"
             f"Debuffs: {status_s}\n\n"
             f"Buff: {self.buff_man.states_list[self.buff_man.buff_state]}\n\n"
             f"Party name: {self.pt_name}\n\n"
             f"Party code: {self.pt_code}\n\n"
             f"Synergy bonus: {bonus}\n\n")
        if self.att_points['unspent']:
            s += "You have unspent talent points. use /lvlup to spend them.\n"

        return s


class Wizard(Player):
    # Redefinimos somente algumas coisas, e definimos funções específicas
    class Magic:
        def __init__(self, spell_name = "fireball", damage = 0):
            self.spell_name = spell_name
            self.damage = damage
            self.ready = False
    def new(self):
        '''O wizard tem 3 magias, o /buff, /fireball e /heal'''
        self.classe = "Wizard"
        self.ap = 5
        self.max_ap = 5
        # self.att_points = {
        #     "unspent": 0,
        #     emojize(":open_book: Spell Power :open_book:"): 0,
        #     emojize(":dizzy: Max. Mana :dizzy:"): 0
        # }
        self.att_points = {
            "unspent": 0,
            emojize(":flexed_biceps: Strength :flexed_biceps:"): 0,
            emojize(":brain: Intelligence :brain:"): 0,
            emojize(":eye: Dexterity :eye:"): 0
        }
        self.actions = {"/heal": self.heal, "/buff": self.buff, "/fireball": self.fireball}
        self.buff_difficulty = [1, 5, 10, 16, 23, 31]
        self.spell_power = 0
        self.is_casting = self.Magic()
        self.lvl_up_text =  emojize("Select an attribute to increase!\n\n"
                            ":flexed_biceps: Strength :flexed_biceps: slightly increases melee weapon damage.\n"
                            ":brain: Intelligence :brain: increases your maximum mana by one and magic weapon damage by 20%.\n"
                            ":eye: Dexterity :eye: increases your spell power, increasing your fireball damage and probability of a sucessful buff.\n")

    def calc_buff_difficulty(self):
        '''A dificuldade de buff aumenta com o buff que vc ta agr'''
        self.buff_difficulty = [1, 5, 10, 16, 23, 31]
        numbers = round(self.spell_power/5)
        for i in range(len(self.buff_difficulty)):
            self.buff_difficulty[i] -= numbers
            if self.buff_difficulty[i] < 1:
                self.buff_difficulty[i] = 1

    def buff(self):
        '''Função de buff do wizard'''
        self.calc_buff_difficulty()
        if self.ap > 0:
            if self.buff_man.buff_state < len(self.buff_man.states_list) - 1:
                self.ap -= 1
                chance = rd.randint(1, self.buff_difficulty[self.buff_man.buff_state])
                if chance == 1:
                    self.bot.send_message(text="You succesfully buffed yourself", chat_id=self.chat_id)
                    self.buff_man.buff_state += 1
                    self.calc_attributes()
                else:
                    self.bot.send_message(text="You failed to buff yourself", chat_id=self.chat_id)

            else:
                self.bot.send_message(text="You are already the most powerful being, no need to buff", chat_id=self.chat_id)
        else:
            self.not_enough_ap()

    def calc_attributes(self):
        '''O buff pro wizard aumenta o ataque e a cura'''
        # print(self.weapon)
        # print(self.armor)
        self.max_ap = 5 + self.att_points[emojize(":brain: Intelligence :brain:")]
        self.spell_power = self.att_points[emojize(":eye: Dexterity :eye:")]

        if self.weapon:
            if self.weapon.type2 == "melee":
                mult = 1 + self.att_points[emojize(":flexed_biceps: Strength :flexed_biceps:")]*0.05
            elif self.weapon.type2 == "magic":
                mult = 1 + self.att_points[emojize(":brain: Intelligence :brain:")]*0.2
            else:
                mult = 1
            self.atk = round(self.weapon.atributos[0]*(self.buff_man.buff_state + 1)*mult)
            self.defense = self.weapon.atributos[1]
        else:
            mult = 1 + self.att_points[emojize(":flexed_biceps: Strength :flexed_biceps:")]*0.05
            self.atk = round(7*(self.buff_man.buff_state + 1)*mult)
            self.defense = 8

        self.bonus_stats_for_inviting_players = min(self.suc_refs*0.01, 1)
        self.atk = round(self.atk*(1 + self.bonus_stats_for_inviting_players))
        self.defense = round(self.defense*(1 + self.bonus_stats_for_inviting_players))
        self.max_arenas = 5 + self.suc_refs
        if self.status:
            for status in self.status:
                self.status_manager.status[status[0]](self, status[1])
        self.stats = self.atk + self.defense

    def reset_stats(self):
        '''Método que executa quando o wizard volta da floresta'''
        self.hp = self.create_normal_limbs()
        self.ap = self.max_ap
        self.buff_man.buff_state = 0
        self.status = []
        self.calc_attributes()

    def not_enough_ap(self):
        '''Caso o wizard n tenha mana'''
        text = "Not enough mana."
        self.bot.send_message(text=text, chat_id=self.chat_id)

    def fireball(self):
        '''Fireball que será dada no próximo inimigo'''
        if self.ap > 0:
            if not self.is_casting.ready:
                if self.is_synergyzed:
                    damage = round(self.atk*(1+0.5*self.spell_power)*3)
                else:
                    damage = round(self.atk*(1+0.5*self.spell_power))
                self.is_casting = self.Magic("fireball", damage)
                self.is_casting.ready = True
                self.ap -= 1
                text = emojize(f"For the next encounter, you will cast a fireball :fire: dealing {damage} damage.")
                self.bot.send_message(text=text, chat_id=self.chat_id)
            else:
                text = "You are casting a fireball already"
                self.bot.send_message(text=text, chat_id=self.chat_id)
        else:
            text = "Not enough mana."
            self.bot.send_message(text=text, chat_id=self.chat_id)

    def heal(self):
        '''Função de cura do wizard'''
        if self.ap > 0:
            self.heal_random_limb()
        else:
            self.not_enough_ap()

    def heal_random_limb(self):
        '''Como a cura do wizard depende do buff, ela fica meio complicada'''
        w_limb = -1
        w_limb_health = 3
        for limb_i in range(len(self.hp)):
            if self.hp[limb_i].health < w_limb_health:
                w_limb = limb_i
                w_limb_health = self.hp[limb_i].health
        limb_i = w_limb
        # limb_i = self.random_damaged_limb_index(self.hp)
        if limb_i > -1:
            if (self.buff_man.buff_state + 1) > 3:
                healing_boost = 3
            else:
                healing_boost = (self.buff_man.buff_state + 1)

            self.hp[limb_i].health += healing_boost
            if self.hp[limb_i].health > 3:
                self.hp[limb_i].health = 3
            self.ap -= 1
            text = f"Succesfully healed {self.hp[limb_i].name}"
            self.bot.send_message(text=text, chat_id=self.chat_id)
        else:
            text = "You are in perfect health"
            self.bot.send_message(text=text, chat_id=self.chat_id)

    def get_stats_string(self, remtime):
        '''"/me" do wizard'''
        s = self.get_basic_stats_string(remtime)
        s += (f"Mana: {self.ap}/{self.max_ap}\n")
        s += f"Spell power: {self.spell_power}\n\n"

        return s

    def print_self_coms(self):
        '''"/class" do Wizard Como o mago pode buffar e curar outros membros da party, esta função muda quando está em uma party'''
        if self.buff_man.buff_state+1 > 3:
            power = 3
        else:
            power = self.buff_man.buff_state+1
        s = "Choose you spell wisely\n"
        s += f"{self.ap}/{self.max_ap} Mana :droplet:\n"
        s += f"/heal to heal {power} hp of worst limb\n"
        s += "/buff to buff\n"
        if self.pt_code:
            s += "/buff (chat_id) to buff target from party\n"
            s += f"/heal (chat_id) to heal {power} hp of a party member\n"
        s += "/fireball to cast a fireball"
        self.bot.send_message(text= emojize(s), chat_id=self.chat_id)

    def dg_coms(self):
        '''Método que retorna uma string que será usada pra mostrar o "/class" do wizard quando este estiver em uma dungeon'''
        if self.buff_man.buff_state+1 > 3:
            power = 3
        else:
            power = self.buff_man.buff_state+1
        s = "Choose you spell wisely\n"
        s += f"{self.ap}/{self.max_ap} Mana :droplet:\n"
        s += f"/heal to heal {power} hp of worst limb\n"
        s += "/buff to buff\n"
        if self.pt_code:
            s += "/buff (chat_id) to buff target from party\n"
            s += f"/heal (chat_id) to heal {power} hp of a party member\n"
        s += "/fireball to cast a fireball\n\n"
        return emojize(s)

    def sanctuary(self):
        '''Santuário pro wizard'''
        s = "You found an ancient library, there you studied the books and took a rest. All mana has been recovered."
        self.ap=self.max_ap
        self.bot.send_message(text=s,chat_id=self.chat_id)

    def get_basic_stats_string(self, remtime):          # Stats string da classe vanilla que vai printar quando vc der o '/me'
        '''Stats string da classe vanilla que vai printar quando vc der o "/me". Todas as classes vão passar por essa'''
        self.calc_attributes()
        possible_status = {
            "cold": [   emojize(":snowflake: Cold :snowflake:"),
                        emojize(":snowflake::snowflake: Colder :snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake: Freezing :snowflake::snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake::snowflake: Frost :snowflake::snowflake::snowflake::snowflake:"),
                        emojize(":snowflake::snowflake::snowflake::snowflake::snowflake: Very Frost :snowflake::snowflake::snowflake::snowflake::snowflake:")],
            "hot": [    emojize(":sun: Warm :sun:"),
                        emojize(":smirking_face: Hot :smirking_face:"),
                        emojize(":fire: Hotter :fire:"),
                        emojize(":fire::fire: Melting :fire::fire:"),              # Debuffs
                                                                                    # Buffs
                        emojize(":bright_button::sun: Sun God :sun::bright_button:"),
                        emojize(":sun::sparkles: Sun Blessed :sun::sparkles:"),
                        emojize(":prohibited::fire: Fire Immune :prohibited::fire:"),
                        emojize(":smiling_face_with_sunglasses::thumbs_up::collision::fire:   Super Cool :smiling_face_with_sunglasses::thumbs_up::collision::fire: "),
                        emojize(":smiling_face_with_sunglasses::collision:  Cooler :smiling_face_with_sunglasses::collision: "),
                        emojize(":smiling_face_with_sunglasses:  Cool :smiling_face_with_sunglasses: "),
                        "None",
                        ]
        }

        def return_status_string():
            status_s = ""
            coiso = 0

            if self.status:
                for status in self.status:
                    if self.armor:
                        if status[0] in self.armor.status_protection:
                            coiso = self.armor.status_protection[status[0]]
                    #if status[1] - coiso >= 0:
                        status_s += possible_status[status[0]][status[1] - coiso]
                        status_s += ", "
            if status_s:
                status_s = status_s[0:-2]
                return status_s
            else:
                return "None"

        status_s = return_status_string()
        weap_name = "None"
        weap_atk = 0
        weap_def = 0
        if self.weapon:
            weap_name = self.weapon.name
            weap_atk = self.weapon.atributos[0]
            weap_def = self.weapon.atributos[1]
        hours, minutes = divmod(remtime, 60)
        locations = {   "camp": emojize(":camping: Camp :camping:"),
                        "forest": emojize(f":deciduous_tree: Forest :deciduous_tree:\nYou will be back in {hours} hours and {minutes} minutes"),
                        "WB": emojize(":snowflake: *Sairacaz, Blizzard Elemental* :snowflake:\nTo escape, /run_away"), "arena": emojize(":crossed_swords: Arena :crossed_swords:\nTo exit: /exit_arena\nTo show win streak: /arena_win"),
                        "dungeon": emojize(":alien_monster: Dungeon :alien_monster:"),
                        "deep_forest": emojize(f":evergreen_tree: Deep forest, stay time: {hours} hours and {minutes} minutes"),
                        "megabeast": emojize(f":dragon_face: Facing a Megabeast.\n Don't forget to check your health periodically.\nTo check the status of the battle, /boss_battle. To leave the battle, use /leave_battle.\n"),
                        "Blacksmith": emojize(f":hammer_and_wrench: Blacksmith :hammer_and_pick:"),
                        }

        if self.is_synergyzed:
            bonus = "Fireball damage is multiplied by 3."
        else:
            bonus = "nothing...(To have a synergy bonus, make a party with at least 2 wizards in it)"


        s = (f"{self.name}\n\n"
             f"Location: {locations[self.location]}\n\n"
             f"Gender: {self.gender}\n"
             f"Attack: {self.atk}:crossed_swords:\n"
             f"Defense: {self.defense}:shield:\n"
             f"Stance: {self.stance}\n"
             f"Level: {self.level}:up_arrow:\n"
             f"Exp: {self.exp}/{self.levels[self.level]}:TOP_arrow:\n"
             f"Talent points : {self.att_points['unspent']}\n"
             f":flexed_biceps: Strength :flexed_biceps:: {self.att_points[emojize(':flexed_biceps: Strength :flexed_biceps:')]}\n"
             f":brain: Intelligence :brain:: {self.att_points[emojize(':brain: Intelligence :brain:')]}\n"
             f":eye: Dexterity :eye:: {self.att_points[emojize(':eye: Dexterity :eye:')]}\n\n"
             f"Class: {self.classe}\n"
             f"Equipped weapon:\n*{weap_name}* :crossed_swords:"
             f"{weap_atk} :shield:{weap_def}\n\n"
             f"Stat Coins: {self.stat_points}\n\n"
             f"Equipped armor:\n*{self.armor}*\n\n"
             f"Debuffs: {status_s}\n\n"
             f"Buff: {self.buff_man.states_list[self.buff_man.buff_state]}\n\n"
             f"Party name: {self.pt_name}\n\n"
             f"Party code: {self.pt_code}\n\n"
             f"Synergy bonus: {bonus}\n\n")
        if self.att_points['unspent']:
            s += "You have unspent talent points. use /lvlup to spend them.\n"


        return s
