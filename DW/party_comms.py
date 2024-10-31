from emoji import emojize
import bot
import player
import random as rd
import helper
import items
import copy
import WB_comms
import party

class PartyComms:
    def __init__(self, server):
        self.server = server
        self.defkb = server.defkb       # Keyboard do chat bot.
        self.helper_man = helper.Helper(server)     # Ver helper.py
        self.WB_controller = WB_comms.WBComms(server)
        self.def_wait_time = 60     # Tempo de espera para quando o bot estiver esperando uma resposta do player.
        self.bot = bot.TGBot()      # Chat bot do Telegram.
        self.actions = {
            emojize(":busts_in_silhouette: Party :busts_in_silhouette:"): self.print_pt,
            "/party": self.print_pt,
            "/ptinv": self.pt_inv,
            "/leave_pt": self.leave_party_comm,
            "/join": self.join_party_comm,
            "/create": self.create_party_comm,
            "/shout": self.shout_comm,
            "/ptname": self.pt_name_comm,
            "/ptsto": self.show_storage,
            "/distribute": self.distribute,
        }          # Dicionário contendo todos os comandos disponíveis para o players.
        self.internal = {
        }

    def show_storage(self, caller, *args):
        '''
            Função que printa os talismans da party.

            Ainda precisa aperfeiçoar muito. por enquanto é só para ver como é que está.
        '''
        pt = self.server.playersdb.players_and_parties[caller.pt_code]
        if not args:
            text = "Here are all the talismans you got. Use /d\_(code) to read the item's description.\n\n"
            text += self.generate_storage_text(pt)
            self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
            return self.def_wait_time
        else:
            code = args[-1]
            for item in pt.storage:
                if code == f"/d_{item.rarity}_{item.code}":
                    text = item.generate_description()
                    self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
                    return self.def_wait_time
            text = "Weapon code not found."
            self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
            return False

    def generate_storage_text(self, user):
        organizer = [{}, {}, {}, {}, {}, {}, {}]
        for item in user.storage:
            if item.code in organizer[item.rarity]:
                organizer[item.rarity][item.code][1] += 1
            else:
                organizer[item.rarity][item.code] = [item, 1]
        text = ""
        r = 0
        for rarity in organizer:
            if rarity:
                for code,item in rarity.items():
                    text += emojize(f"(x{item[1]}) *{item[0]}* /d\_{r}\_{code}\n")
                text += "\n"
            r += 1
        return text

    def party_code_generator(self):
        '''
            Função que gera um código para a criação de parties.
        '''
        code_len = 8
        cd = "/"
        while True:
            cd += self.helper_man.randomnamegenerator(code_len)
            if not cd in self.server.playersdb.players_and_parties:
                return cd

    def create_party_comm(self, caller, *args):
        if not caller.location == "camp":
            text = "You need to be at camp to create or join a party"
            self.bot.send_message(text = text, chat_id = caller.chat_id)
            return False

        pt_name = self.server.messages[caller.chat_id]["message_list"][-1][8:]
        if not pt_name and not args:
            text = "Type a name for your party."
            self.bot.send_message(text = text, chat_id = caller.chat_id)
            return self.def_wait_time

        if caller.pt_code:      # Checa se o player está numa party.
            self.leave_party_comm(caller, "yes")
        caller.has_died = False

        if args:
            if args[-1] == "":
                pt_name = "Nameless party"
            else:
                pt_name = args[-1]
        code = self.party_code_generator()
        self.server.playersdb.players_and_parties[code] = party.Party(caller, code, pt_name)
        self.bot.send_message(text = f"You have founded the {pt_name}!\n Share the following code to recruit new member:", chat_id  = caller.chat_id)
        self.bot.send_message(text = code, chat_id = caller.chat_id)
        return False

    def scoop(self, caller, text):
        done = False
        if len(self.server.playersdb.players_and_parties[caller.pt_code].inventory):        # Nas linhas abaixo, os itens do jogador serão colhidos.
            owned_items = [item for item in self.server.playersdb.players_and_parties[caller.pt_code].inventory if item.owner == caller.chat_id]
            for item in owned_items:
                if item.is_shared_and_equipped:         # Checa se o item está equipado por um outro player da party.
                    for jog in self.server.playersdb.players_and_parties[caller.pt_code].players:      # Procura o jogador que está com o item equipado.
                        if jog.weapon and jog.weapon.code == item.code and jog.weapon.name == item.name:
                                                                    # Desequipa o item do player que o estava usando.
                            # item.is_shared_and_equipped = False
                            jog.weapon.unequip(jog)
                            jog.weapon = None
                            jog.calc_attributes()                                       # Atualiza os status do jogador que perdeu o item equipado.
                            self.bot.send_message(text = text, chat_id = jog.chat_id)
                            break
                    item.is_shared_and_equipped = False
                number = 0
                for arma in caller.inventory:

                    if arma.ac_code == item.ac_code:
                        number += 1
                if number == 0:
                    number = ""
                item.ac_code = item.code + f"{number}"
                item.ac_code = item.code + f"{number}"
                temp_ac = item.ac_code
                item.ac_code = item.code
                item.code = temp_ac
                caller.inventory.append(copy.deepcopy(item))                    # Cria uma cópia verdadeira do item para o inv do caller.
                self.server.playersdb.players_and_parties[caller.pt_code].inventory.remove(item)      # Deleta o item do inv da party.
            del owned_items

    def adm_scoop(self, chat_id, code):
        done = False
        if len(self.server.playersdb.players_and_parties[code].inventory):        # Nas linhas abaixo, os itens do jogador serão colhidos.
            owned_items = [item for item in self.server.playersdb.players_and_parties[code].inventory if item.owner == chat_id]
            for item in owned_items:
                if item.is_shared_and_equipped:         # Checa se o item está equipado por um outro player da party.
                    for jog in self.server.playersdb.players_and_parties[code].players:      # Procura o jogador que está com o item equipado.
                        if jog.weapon and jog.weapon.code == item.code:
                            jog.weapon = None                                           # Desequipa o item do player que o estava usando.
                            # item.is_shared_and_equipped = False
                            jog.calc_attributes()                                       # Atualiza os status do jogador que perdeu o item equipado.
                            # self.bot.send_message(text = text, chat_id = jog.chat_id)
                            break
                    item.is_shared_and_equipped = False
                number = 0
                for arma in self.server.playersdb.players_and_parties[chat_id].inventory:

                    if arma.ac_code == item.ac_code:
                        number += 1
                if number == 0:
                    number = ""
                item.ac_code = item.code + f"{number}"
                item.ac_code = item.code + f"{number}"
                temp_ac = item.ac_code
                item.ac_code = item.code
                item.code = temp_ac
                self.server.playersdb.players_and_parties[chat_id].inventory.append(copy.deepcopy(item))                    # Cria uma cópia verdadeira do item para o inv do caller.
                self.server.playersdb.players_and_parties[code].inventory.remove(item)      # Deleta o item do inv da party.
            del owned_items


    def distribute(self, caller, *args):
        if not args:
            att = {}
            better_list = {}
            for jog in self.server.playersdb.players_and_parties[caller.pt_code].players:
                att[jog.chat_id] = 0
            for item in self.server.playersdb.players_and_parties[caller.pt_code].inventory:
                if not isinstance(item, items.dg_map) and not item.owner:
                    stats = item.atributos[0]+item.atributos[1]
                    better_list[item.code] = [stats, item]

            # for stats,item in better_list.items():
            #     print(stats)

            for codes, tup in sorted(better_list.items(), key=lambda item: item[1][0], reverse = True):
                stats = tup[0]
                # stats = item.atributos[0]+item.atributos[1]
                chos, vel = caller.chat_id, att[caller.chat_id]
                for chat, val in att.items():
                    if val <= vel:
                        vel = val
                        chos = chat

                att[chos] += stats
                # tup[1].owner = chos
            text = emojize(f"*Stats claimed*:\n\n")
            s = "You just lost your equipped weapon because owner has taken it from you."
            for chat, val in att.items():
                text += emojize(f"*{self.server.playersdb.players_and_parties[chat].name}* owned :crossed_swords:️:shield: *{val}* total stats!\n")

            text += "\nAre you sure you want to procede?"
            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.forest_return_reply_markup, parse_mode='MARKDOWN')
            # for jog in self.server.playersdb.players_and_parties[caller.pt_code].players:
            #     self.bot.send_message(text = text, chat_id = jog.chat_id, parse_mode = "MARKDOWN")
            #     self.scoop(jog, s)
            return self.def_wait_time*2
        else:
            if args[-1] == "yes":
                att = {}
                better_list = {}
                for jog in self.server.playersdb.players_and_parties[caller.pt_code].players:
                    att[jog.chat_id] = 0
                for item in self.server.playersdb.players_and_parties[caller.pt_code].inventory:
                    if not isinstance(item, items.dg_map) and not item.owner:
                        stats = item.atributos[0]+item.atributos[1]
                        better_list[item.code] = [stats, item]

                # for stats,item in better_list.items():
                #     print(stats)

                for codes, tup in sorted(better_list.items(), key=lambda item: item[1][0], reverse = True):
                    stats = tup[0]
                    # stats = item.atributos[0]+item.atributos[1]
                    chos, vel = caller.chat_id, att[caller.chat_id]
                    for chat, val in att.items():
                        if val <= vel:
                            vel = val
                            chos = chat

                    att[chos] += stats
                    tup[1].owner = chos
                text = emojize(f"*Stats claimed*:\n\n")
                s = "You just lost your equipped weapon because owner has taken it from you."
                for chat, val in att.items():
                    text += emojize(f"*{self.server.playersdb.players_and_parties[chat].name}* owned :crossed_swords:️:shield: *{val}* total stats!\n")


                # self.bot.send_message(text=text, chat_id=caller.chat_id)
                for jog in self.server.playersdb.players_and_parties[caller.pt_code].players:
                    self.bot.send_message(text = text, chat_id = jog.chat_id, parse_mode = "MARKDOWN", reply_markup=self.server.keyboards.class_main_menu_reply_markup)
                    self.scoop(jog, s)
            elif args[-1] == "no":
                text = "Ok!"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def leave_party_comm(self, caller, *args):
        if caller.pt_code:
            if self.server.playersdb.players_and_parties[caller.pt_code].location == "camp":
                if not args:
                    text = "Do you want to leave current party?"
                    self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.forest_return_reply_markup)
                    return self.def_wait_time

                elif args[-1] == "yes":
                    s = "You just lost your equipped weapon because owner left party."
                    self.scoop(caller, s)
                    if caller.weapon:
                        if caller.weapon.is_shared_and_equipped:
                            for wep in self.server.playersdb.players_and_parties[caller.pt_code].inventory:
                                if caller.weapon.name == wep.name:
                                    caller.weapon.is_shared_and_equipped = False
                                    caller.weapon = None

                    for jogador in self.server.playersdb.players_and_parties[caller.pt_code].players:

                        if jogador.chat_id == caller.chat_id:
                            #text = f"You just left {self.server.playersdb.players_and_parties[caller.pt_code][temp]}"
                            text = emojize(f"Your teammates from {self.server.playersdb.players_and_parties[caller.pt_code].pt_name} wave goodbye as you go your separate ways. Everyone will miss you :frowning_face:")
                            self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.at_camp_main_menu_reply_markup)
                        else:
                            text = f"{caller.name} just left {self.server.playersdb.players_and_parties[caller.pt_code].pt_name}"
                            self.bot.send_message(text = text, chat_id = jogador.chat_id)
                    code = caller.pt_code
                    if caller in self.server.playersdb.players_and_parties[caller.pt_code].players:

                        self.server.playersdb.players_and_parties[code].leave_pt(caller)
                        count = 0 # Conta quantos jogadores de sua classe estão na party
                        for jog1 in self.server.playersdb.players_and_parties[code].players:
                            for jog2 in self.server.playersdb.players_and_parties[code].players:
                                if jog2.classe == jog1.classe:
                                    count += 1
                            if not count > 1:
                                jog1.is_synergyzed = False

                    if not self.server.playersdb.players_and_parties[code].players:
                        del self.server.playersdb.players_and_parties[code]

                else:
                    text = f"You decided to stay in your party."
                    self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.class_main_menu_reply_markup)

            else:
                text = f"You need to be at camp to leave parties!"
                self.bot.send_message(text = text, chat_id = caller.chat_id)

        else:
            text = f"You do not belong to a party yet! try /join or /create first!"
            self.bot.send_message(text = text, chat_id = caller.chat_id)
        return False

    def adm_leave_party_comm(self, chat_id, code):

        s = "You just lost your equipped weapon because owner left party."
        self.adm_scoop(chat_id, code)
        if self.server.playersdb.players_and_parties[chat_id].weapon:
            if self.server.playersdb.players_and_parties[chat_id].weapon.is_shared_and_equipped:
                self.server.playersdb.players_and_parties[chat_id].weapon.is_shared_and_equipped = False
                self.server.playersdb.players_and_parties[chat_id].weapon = None

        for jogador in self.server.playersdb.players_and_parties[code].players:

            if jogador.chat_id == self.server.playersdb.players_and_parties[chat_id].chat_id:
                #text = f"You just left {self.server.playersdb.players_and_parties[code][temp]}"
                text = emojize(f"Your teammates from {self.server.playersdb.players_and_parties[code].pt_name} wave goodbye as you go your separate ways. Everyone will miss you :frowning_face:")
                self.bot.send_message(text = text, chat_id = self.server.playersdb.players_and_parties[chat_id].chat_id, reply_markup = self.server.keyboards.at_camp_main_menu_reply_markup)
            else:
                text = f"{self.server.playersdb.players_and_parties[chat_id].name} just left {self.server.playersdb.players_and_parties[code].pt_name}"
                self.bot.send_message(text = text, chat_id = jogador.chat_id)

        if self.server.playersdb.players_and_parties[chat_id] in self.server.playersdb.players_and_parties[code].players:

            self.server.playersdb.players_and_parties[code].adm_leave_pt(self.server.playersdb.players_and_parties[chat_id])
            count = 0 # Conta quantos jogadores de sua classe estão na party
            for jog1 in self.server.playersdb.players_and_parties[code].players:
                for jog2 in self.server.playersdb.players_and_parties[code].players:
                    if jog2.classe == jog1.classe:
                        count += 1
                if not count > 1:
                    jog1.is_synergyzed = False

        if not self.server.playersdb.players_and_parties[code].players:
            del self.server.playersdb.players_and_parties[code]


        return False

    def join_party(self, code, caller, direct_join = False):
        '''
            Método usado para colocar o player numa party.

            Parâmetros:
                - code (str): código da party na qual o jogador irá entrar;
                - caller (class): o jogador que irá entrar numa party.
                - direct_join (boolean): Uma forma de se juntar a uma party é dando forward no código
                direto. Essa variável checa se o join dado foi direto ou não.
        '''
        if code in self.server.playersdb.players_and_parties:       # Checa se o código usado existe no DW, isto é, checa se a party a ser entrada existe.
            if caller.location == "camp":         # Para o jogador entrar numa party, ele precisa estar no camp.
                if self.server.playersdb.players_and_parties[code].location == "camp":         # A party também precisa estar no camp.
                    if len(self.server.playersdb.players_and_parties[code].players) < 5:           # Checa se a party a ser entrada está cheia.
                        caller.has_died = False     # Se o jogador acabou de morrer e se juntar numa party, ele não poderá se juntar numa party.
                        old_pt_name = caller.pt_name
                        pt_name = self.server.playersdb.players_and_parties[code].pt_name
                        text = f"Congratulations, you just joined {pt_name}"

                        if caller.pt_code:          # Checa se o player já estava em uma party. Caso sim, todos os seus itens compartilhados serão recolhidos e ele sairá da party atual.
                            self.leave_party_comm(caller, "yes")
                            old_pt_name = caller.pt_name
                            text = f"You just left {old_pt_name} to join {pt_name}!"

                        true_caller = self.server.playersdb.players_and_parties[caller.chat_id]     # Para evitar clones (?)
                        self.server.playersdb.players_and_parties[code].join_pt(true_caller)

                        for jogador in self.server.playersdb.players_and_parties[code].players:
                            count = 0 # Conta quantos jogadores de sua classe estão na party
                            for jog2 in self.server.playersdb.players_and_parties[caller.pt_code].players:
                                if jog2.classe == jogador.classe:
                                    count += 1
                            if count > 1:
                                jogador.is_synergyzed = True
                            if jogador.chat_id == caller.chat_id:
                                self.bot.send_message(text = text, chat_id = jogador.chat_id)
                            else:
                                self.bot.send_message(text = f"{caller.name} just entered {pt_name}", chat_id = jogador.chat_id)

                    else:
                        text = "Party is full, aborting"
                        self.bot.send_message(text = text, chat_id = caller.chat_id)

                else:
                    # text = f"{self.server.playersdb.players_and_parties[code][temp]} is currently at the forest, this party need to be at camp for it to be joinable!"
                    text = f"The {self.server.playersdb.players_and_parties[code].pt_name} are currently out exploring the forest. The party must be at camp for you to join them!"
                    self.bot.send_message(text = text, chat_id = caller.chat_id)
            else:
                text = "You need to be at camp to create or join a party"
                self.bot.send_message(text = text, chat_id = caller.chat_id)
            return True             # Um True é retornado aqui, para indicar que o código inserido é válido. Usado no MessageMan para o caso de join direto.
        elif not direct_join:       # Esta linha é pulada em caso de join direto, para que o bot não responda toda hora que o jogador insere comandos inválidos.
            text = f"Party code {code} not found!"
            self.bot.send_message(text = text, chat_id = caller.chat_id)
        return False

    def join_party_comm(self, caller, *args):
        '''
            Esta função é o comando do player para ingressar numa party.

            Parâmetros:
            caller (class): player que entrará numa party;
            args (tuple): argumento que conterá o código da party.
        '''
        if not args:
            text = "Forward here or type the party's code you want to join"
            self.bot.send_message(text = text, chat_id = caller.chat_id)
            return self.def_wait_time

        else:
            code = args[-1]
            self.join_party(code, caller)
        return False

    def pt_name_comm(self, caller, *args):
        if caller.pt_code:
            if not args:
                text = "Type the new party name."
                self.bot.send_message(text = text, chat_id = caller.chat_id)
                return self.def_wait_time
            else:
                pt_name = args[-1]
                self.server.playersdb.players_and_parties[caller.pt_code].pt_name = pt_name
                for jogador in self.server.playersdb.players_and_parties[caller.pt_code].players:
                    text = f"{caller.name} changed the party name to: {pt_name}"
                    self.bot.send_message(text = text, chat_id = jogador.chat_id)
        else:
            text = "You do not belong to party."
            self.bot.send_message(text=text,chat_id = caller.chat_id)
        return False

    def shout_comm(self, caller, *args):
        message = self.server.messages[caller.chat_id]["message_list"][-1][7:]
        if caller.pt_code:
            for jogador in self.server.playersdb.players_and_parties[caller.pt_code].players:
                text = f"{caller.name} said: {message}"
                self.bot.send_message(text = text, chat_id = jogador.chat_id)
        else:
            self.bot.send_message(text=f"You shouted but nothing happened.", chat_id=caller.chat_id)
        return False

    def pt_inv(self, caller, *args):
        if caller.pt_code:
            if args:
                is_description = False
                treco = args[-1]
                # if treco == "/distribute":
                #     self.distribute(caller)

                if treco == "/scoop":         # Recolhe os itens compartilhados do jogador. O código é o mesmo que em join_party.
                    self.bot.send_message(text="You claimed items owned by you.", chat_id = caller.chat_id)
                    s = "You just lost your equipped weapon because owner have taken it from you."
                    self.scoop(caller, s)

                else:       # Se o comando inserido não é nenhum dos anteriores, então o player está equipando um item.
                    try:
                        direct_join = self.join_party(treco, caller, direct_join = True)
                        if direct_join:
                            return self.def_wait_time
                    except:
                        pass
                    text = ""
                    # Checaremos se o item está em uso ou não.
                    for item in self.server.playersdb.players_and_parties[caller.pt_code].inventory:
                        if f"/e_{item.code}" == treco:
                            if item.type == "map":      # Marca se o item é um mapa.
                                item.action(self.server.playersdb.players_and_parties[caller.pt_code])
                                break

                            if item.is_shared_and_equipped:
                                text += "This weapon is already in use by other party member"

                            else:
                                if not item.owner:       # Se o item não for um mapa e não tiver dono, o novo dono da arma será o player que irá equipá-la.
                                    item.owner = caller.chat_id
                                    text = emojize(f"You claimed {item.name}!\n")
                                if caller.weapon and caller.weapon.is_shared_and_equipped:      # Para um item ser equipado, o atual deve ser desequipado. O problema é que o item pode voltar para o inv da party com o mesmo código de outra.
                                    caller.weapon.is_shared_and_equipped = False
                                    index = 0
                                    for item2 in self.server.playersdb.players_and_parties[caller.pt_code].inventory:       # Então, iremos adicionar mais índices ao item para diferenciá-lo de outro item de mesmo código.

                                        if caller.weapon.code == item2.code:
                                            break
                                        index += 1
                                    self.server.playersdb.players_and_parties[caller.pt_code].inventory[index].is_shared_and_equipped = False
                                    index = 0
                                    for item2 in self.server.playersdb.players_and_parties[caller.pt_code].inventory:       # Então, iremos adicionar mais índices ao item para diferenciá-lo de outro item de mesmo código.

                                        if item.code == item2.code:
                                            break
                                        index += 1
                                    self.server.playersdb.players_and_parties[caller.pt_code].inventory[index].is_shared_and_equipped = True

                                    self.server.playersdb.players_and_parties[caller.pt_code].inventory[index].action(self.server.playersdb.players_and_parties[caller.chat_id])         # Equipa o item.
                                    caller.calc_attributes()
                                    text += emojize(f"Succesfully borrowed {item.name}!")

                                else:
                                    item.is_shared_and_equipped = True
                                    index = 0
                                    for item2 in self.server.playersdb.players_and_parties[caller.pt_code].inventory:       # Então, iremos adicionar mais índices ao item para diferenciá-lo de outro item de mesmo código.

                                        if item.code == item2.code:
                                            break
                                        index += 1
                                    self.server.playersdb.players_and_parties[caller.pt_code].inventory[index].is_shared_and_equipped = True

                                    self.server.playersdb.players_and_parties[caller.pt_code].inventory[index].action(self.server.playersdb.players_and_parties[caller.chat_id])         # Equipa o item.
                                    caller.calc_attributes()
                                    text += emojize(f"Succesfully borrowed {item.name}!")
#
                                break
                        if f"/d_{item.code}" == treco:
                            is_description = True
                            new_name = copy.copy(item.name)
                            new_name.replace("_", "\\_")
                            new_name.replace("*", "\\*")
                            text += emojize(f"{new_name}\n"
                                            f"Original weapon stats: {item.atributos[0]} :crossed_swords: {item.atributos[1]} :shield:\n"
                                            f"Weapon type: {item.type2}\n\n"
                                            f"Weapon Talismans: {item.talisman_list()}\n\n"
                                            f"Weapon Powers: {item.power_list()}\n\n"
                                            f"Description:\n\n"
                                            f"{item.description}")

                            break
                    if text:
                        self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode = 'MARKDOWN')
                        return self.def_wait_time
                    else:
                        text = "Code not found."
                        self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode = 'MARKDOWN')
                        return self.def_wait_time


            else:
                text = self.print_pt_inv(caller)
                self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode='MARKDOWN')
                return self.def_wait_time
        else:
            text = "You do not belong to party to look at its shared inventory, create a party first with /party, then /create (name)"
            self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode='MARKDOWN')
            return False

    def print_pt_inv(self, caller):
        '''
            Mostra o inventário da party. Retorna um string.
        '''
        s = ""
        for i in self.server.playersdb.players_and_parties[caller.pt_code].inventory:       # Printa o inventário.
            s += f"*{i}* /e_{i.code}\n" #emojize(f"*{i.name}* :crossed_swords:{i.atributos[0]} :shield:{i.atributos[1]} /e_{i.code}\n")
        if s == "":
            s = "The party inventory is empty"

        else:
            s += "\nBorrow a weapon using the '/e_' codes above. To add an item to the shared invetory, /inv then /s_(code). /scoop to scoop all items owned by you. /distribute will evenly distribute the item stats amongst members."
            s = s.replace("_", "\\_")
        return s

    def print_pt(self, caller):
        '''
            Exibe os status da party, seus jogadores e seu inventário.
        '''

        text = "Do you want to /join a party ,/create one or /leave_pt your current party?\nTo join use /join or copy and paste the party code you want to join!\nTo create a new party use /create ; you can also create directly by /create (name of the party) like: /create the company of the chicken axe. \nUse /shout (message) to send a message to members and /ptname (name) to change party name.\n\n"
        text = text.replace("_", "\\_")
        if not caller.pt_code:
            self.bot.send_message(text = text, chat_id = caller.chat_id)
            return False

        grupo = self.server.playersdb.players_and_parties[caller.pt_code]
        new_name = copy.copy(grupo.pt_name)
        new_name = new_name.replace("_", "\\_")
        text += emojize(f":party_popper: *Party members* from {new_name}, {grupo.pt_code}: \n\n")
        tt_hp = 0
        txt2 = ""
        for jogador in self.server.playersdb.players_and_parties[caller.pt_code].players:       # Printa os jogadores e seus status.
            count = 0 # Conta quantos jogadores de sua classe estão na party
            jogador.calc_attributes()
            for jog2 in self.server.playersdb.players_and_parties[caller.pt_code].players:
                if jog2.classe == jogador.classe:
                    count += 1
            if count > 1:
                self.server.playersdb.players_and_parties[jogador.chat_id].is_synergyzed = True
            else:
                if jogador.chat_id in self.server.playersdb.players_and_parties:
                    self.server.playersdb.players_and_parties[jogador.chat_id].is_synergyzed = False
            self.server.playersdb.players_and_parties[jogador.chat_id].calc_attributes()
            emoji = ":green_heart:"
            j_hp = 0
            for limb in jogador.hp:
                j_hp += limb.health
            if j_hp < 5:
                emoji = ":yellow_heart:"
            if j_hp < 2:
                emoji = ":red_heart:"
            txt2 += emojize(f"{jogador.name}, ''{jogador.chat_id}'':\nHealth: {j_hp}{emoji} {jogador.classe}\n")
            txt2 += f"*Buff*: {jogador.buff_man.states_list[jogador.buff_man.buff_state]}\n"
            txt2 += emojize(f"*Stats*: {jogador.atk} :crossed_swords: {jogador.defense} :shield:\n\n")
            tt_hp += j_hp
        txt2 = txt2.replace("_", "\\_")
        text += txt2
        text += f"*Total health*: {tt_hp} \n"

        text += f"Check shared inventory: /ptinv\n\n"
        # print(text)
        # text.replace("_", "\\_")
        # print(text)
        self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode = 'MARKDOWN')
        return False

    def adm_print_pt(self, caller):
        '''
            Exibe os status da party, seus jogadores e seu inventário.
        '''

        text = "Do you want to /join a party, /create one or /leave_pt your current party?\nTo join use /join or copy and paste the party code you want to join!\nTo create a new party use /create ; you can also create directly by /create (name of the party) like: /create the company of the chicken axe. \nUse /shout (message) to send a message to members and /ptname (name) to change party name.\n\n"
        if not caller.pt_code:
            text = text.replace("_", "\\_")
            self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode = 'MARKDOWN')
            return text

        grupo = self.server.playersdb.players_and_parties[caller.pt_code]
        text += emojize(f":party_popper: *Party members* from {grupo.pt_name}, {grupo.pt_code}: \n\n")
        tt_hp = 0
        txt2 = ""
        for jogador in self.server.playersdb.players_and_parties[caller.pt_code].players:       # Printa os jogadores e seus status.
            count = 0 # Conta quantos jogadores de sua classe estão na party
            for jog2 in self.server.playersdb.players_and_parties[caller.pt_code].players:
                if jog2.classe == jogador.classe:
                    count += 1
            if count > 1:
                self.server.playersdb.players_and_parties[jogador.chat_id].is_synergyzed = True
            else:
                if jogador.chat_id in self.server.playersdb.players_and_parties:
                    self.server.playersdb.players_and_parties[jogador.chat_id].is_synergyzed = False
            self.server.playersdb.players_and_parties[jogador.chat_id].calc_attributes()
            emoji = ":green_heart:"
            j_hp = 0
            for limb in jogador.hp:
                j_hp += limb.health
            if j_hp < 5:
                emoji = ":yellow_heart:"
            if j_hp < 2:
                emoji = ":red_heart:"
            txt2 += emojize(f"{jogador.name}, ''{jogador.chat_id}'':\nHealth: {j_hp}{emoji} {jogador.classe}\n")
            txt2 += f"*Buff*: {jogador.buff_man.states_list[jogador.buff_man.buff_state]}\n"
            txt2 += emojize(f"*Stats*: {jogador.atk} :crossed_swords: {jogador.defense} :shield:\n\n")
            tt_hp += j_hp
        txt2 = txt2.replace("_", "\\_")
        text += txt2
        text += f"*Total health*: {tt_hp} \n"

        text += f"Check shared inventory: /ptinv\n\n"

        # self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode = 'MARKDOWN')
        return text

    def to(self, caller):
        pass
