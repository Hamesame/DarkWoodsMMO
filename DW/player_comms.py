################################################
# Classe que contém os comandos dos jogadores  #
################################################

# Ver messageman.py primeiro.
# Em geral, a única forma com que o Player interage com o chat bot do Telegram é
# através de comandos.

from emoji import emojize
import bot
import player
import random as rd
import helper
import items
import copy
import WB_comms
import death
import traceback

class PlayerComms:
    '''
        Contém todos os comandos disponíveis para o jogador.
    '''
    def __init__(self, server):

        self.server = server        # server é a classe RPG em rpg_revamp.py
        self.helper_man = helper.Helper(server)     # Ver helper.py
        self.WB_controller = WB_comms.WBComms(server)       #Comandos do World Boss.
        self.defkb = server.defkb       # Keyboard do chat bot.
        self.defkb2 = server.defkb2
        self.def_wait_time = 60     # Tempo de espera para quando o bot estiver esperando uma resposta do player.
        self.bot = bot.TGBot()      # Chat bot do Telegram.
        self.death = death.Death(server)
        self.actions = {
            emojize("/help"): self.show_help,
            emojize("/name"): self.show_name_change,
            emojize("/inv"): self.show_inv,
            emojize("/credits"): self.show_credits,
            emojize("/rankings"): self.show_rankings,
            emojize("/WB_rankings"): self.WB_rankings,
            emojize(":trophy: Me :trophy:"): self.show_stats,
            emojize("/me"): self.show_stats,
            emojize(":green_heart: Health :green_heart:"): self.show_health,
            emojize(":fleur-de-lis: Class :fleur-de-lis:"): self.print_self_coms,
            emojize("/bestiary"): self.show_pokedex,
            emojize("/lvlup"): self.spend_points,
            emojize("/erase"): self.erase,
            emojize(":school_backpack: Inventory :school_backpack:"): self.show_inv,
            "/0": self.nada,
            "/referral": self.promo,
            "/run_away": self.exit_wb,
            "/change_sex": self.change_sex,
            "/change_stance": self.change_stance,
            "/sto": self.show_storage,
            "/stat_points": self.stat_points,
            "/scrap_weapons": self.scrap_weapons,
            "/settings_percentage": self.set_percentage,
            "/setting_can_get_talismans": self.tog_talimans,
            "/WB_report": self.show_last_wb_report,
            # "/haunt": self.show_haunt_menu,
        }          # Dicionário contendo todos os comandos disponíveis para o players.
        self.internal = {
            "new_player": self.new_player,
            "level_up": self.level_up,
        }          # Dicionário contendo todos os comandos utilizados apenas pelo próprio código. (Ver messageman.py)

        self.ranking_comms = {}

    def show_last_wb_report(self, caller, *args):
        text = caller.last_wb_report
        if text:
            self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
        else:
            text = "You've never fought the world boss."
            self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
        return False

    def tog_talimans(self, caller, *args):
        if caller.setting_can_get_talismans:
            caller.setting_can_get_talismans = False
            aux = "won't"
        else:
            caller.setting_can_get_talismans = True
            aux = "will"
        text = f"Next time you scrap, weapons with talismans {aux} be included."
        self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
        return False

    def set_percentage(self, caller, *args):
        if not args:
            text = "Please type the new percentage threshold. (1-99)"
            self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
            return self.def_wait_time*2
        else:
            try:
                val = max(min(99, int(args[-1])), 0)
            except ValueError:
                text = "Please input a number."
                self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
                return self.def_wait_time*2
            caller.setting_percentage = val
            text = f"The new stat threshold is {val}%"
            self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
            return False

    def scrap_weapons(self, caller, *args):
        initial = caller.stat_points
        caller.generate_stat_points()
        text = f"You transformed {caller.stat_points - initial} weapon stats into stat coins."
        self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def stat_points(self, caller, *args):
        if caller.setting_can_get_talismans:
            aux = "may have"
        else:
            aux = "musn't have"
        text = f"You have {caller.stat_points} Stat Coins. What you want to do?\n\n"
        text += f"/scrap_weapons: Makes your weapons that have {caller.setting_percentage}% or less stats than your strongest weapon and {aux} talismans be converted to Stat Coins that can be used in the blacksmith.\n\n"
        text += f"/settings_percentage: Sets the percentage threshold of stats that are going to be scrapped. Actual: {caller.setting_percentage}\n\n"
        text += f"/setting_can_get_talismans: Toggle between accepting talismans or not in the scrapping process. Actual: {caller.setting_can_get_talismans}\n\n"

        self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False


    def show_storage(self, caller, *args):
        '''
            Função que printa os talismans do jogador.

            Ainda precisa aperfeiçoar muito. por enquanto é só para ver como é que está.
        '''
        if not args:
            text = "Here are all the talismans you got. Use /d\_(code) to read the item's description.\n\n"
            text += self.generate_storage_text(caller)
            self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
            return self.def_wait_time
        else:
            code = args[-1]
            for r in caller.storage.talismans:
                for tal_code, tal in r.items():
                    if code == f"/d_{tal[0].rarity}_{tal[0].code}":
                        item = tal[0]
                        text = item.generate_description()
                        self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
                        return self.def_wait_time
            text = "Talisman code not found."
            self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode='MARKDOWN')
            return False

    def generate_storage_text(self, user):
        # organizer = [{}, {}, {}, {}, {}, {}, {}]
        # for item in user.storage:
        #     if item.code in organizer[item.rarity]:
        #         organizer[item.rarity][item.code][1] += 1
        #     else:
        #         organizer[item.rarity][item.code] = [item, 1]
        text = ""
        organizer = user.storage.talismans
        r = 0
        for rarity in organizer:
            if rarity:
                for code,item in rarity.items():
                    text += emojize(f"(x{item[1]}) *{item[0]}* /d_{r}_{code}\n")
                text += "\n"
            r += 1
        text = text.replace("_", "\\_")
        return text

    def nada(self, caller):
        return False

    def change_stance(self, caller):
        self.server.playersdb.players_and_parties[caller.chat_id].change_stance()
        text = f"Your stance now is {self.server.playersdb.players_and_parties[caller.chat_id].stance}"
        self.bot.send_message(text = text, chat_id = caller.chat_id)
        return False

    def change_sex(self, caller):
        self.server.playersdb.players_and_parties[caller.chat_id].change_sex()
        text = f"Congratulations! You're now a {self.server.playersdb.players_and_parties[caller.chat_id].gender}!"
        self.bot.send_message(text = text, chat_id = caller.chat_id)
        return False

    def WB_rankings(self, caller):
        player_list = self.server.World_boss.status["Players"]
        atk_list = []
        for chat in player_list:
            jog = self.server.playersdb.players_and_parties[chat]
            place = 0
            if atk_list:
                for item in atk_list:
                    if item.atk < jog.atk:
                        break
                    place += 1
                atk_list.insert(place, jog)
            else:
                atk_list.append(jog)

        text = emojize("List of heros that are facing :snowflake: *Snow Storm* :snowflake:\n\n")
        index = 0
        for item in atk_list:
            index += 1
            text += emojize(f"{index} - {item.name} :crossed_swords: {item.atk} :shield: {item.defense}\n")
            if index > 9:
                break
        if caller in atk_list:
            place = atk_list.index(caller)+1
            if place > 10:
                text += "...\n"
                text += emojize(f"{place} - {caller.name} :crossed_swords: {caller.atk} :shield: {caller.defense}\n")
        text = text.replace("_","\\_")
        self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode = 'MARKDOWN')

        return False

    def exit_wb(self, caller):
        if not caller.pt_code:

            # if caller.location == "WB":
            if caller.chat_id in self.server.World_boss.status["Players"]:
                self.server.World_boss.remove_player(caller.chat_id)
                self.server.woods.players[caller.chat_id]["active"] = True
            elif caller.location == "dungeon":
                caller.location = "forest"
                self.server.woods.players[caller.chat_id]["active"] = True
                self.server.playersdb.players_and_parties[caller.code].active = True
                text = "It's a dangerous place, so your party decided to step back."
                self.bot.send_message(text = text, chat_id = caller.chat_id)
            else:
                text = "What are you trying to run away from?"
                self.bot.send_message(text = text, chat_id = caller.chat_id)
            return False

        else:

            # if caller.location == "WB":
            if caller.chat_id in self.server.World_boss.status["Players"]:
                for chat in self.server.playersdb.players_and_parties[caller.pt_code].chat_ids:
                    self.server.World_boss.remove_player(chat)
                self.server.playersdb.players_and_parties[caller.pt_code].active = True
                self.server.woods.players[caller.code]["active"] = True
                self.server.playersdb.players_and_parties[caller.pt_code].location = "forest"
                return False
            elif caller.location == "dungeon":
                self.server.playersdb.players_and_parties[caller.pt_code].location = "forest"
                self.server.playersdb.players_and_parties[caller.pt_code].active = True
                self.server.woods.players[caller.code]["active"] = True
                text = "It's a dangerous place, so your party decided to step back."
                self.bot.send_message(text = text, chat_id = caller.chat_id)
            else:
                text = "What are you trying to run away from?"
                self.bot.send_message(text = text, chat_id = caller.chat_id)
        return False

    def show_help(self, caller):        # Printa todos os comandos disponiveis para o player.
        text = ("Commands:\n"
                "/help: display this menu \n"
                "/name: change your name \n"
                "/inv: shows your inventory\n"
                "/sto: shows your talismans storage\n"
                "/bestiary: shows seen beasts\n"
                "/lvlup: spend talent points\n"
                "/party: find or join one\n"
                "/credits\n"
                "/rankings: Displays the best players and equips\n"
                "/WB_rankings: Displays the players that are in the world boss battle\n"
                "/referral: generates a link to invite friends\n"
                "/change_sex: Changes your gender\n"
                "/change_stance: Changes your stance\n"
                "/pots: Display your potions\n"
                "/shop: displays the leaf shop\n"
                "/special_inv: shows some items bought at the shop\n"
                "/player_market: Shows the player market where players can trade leaves.\n"
                "/stat_points: Shows your stat points and settings\n"
                "/WB_report: Shows last World boss battle report\n"
                "/run_away: Makes you leave the world boss or dungeon (if you are gltiched)\n"
                # "/haunt: If you are equipped with a ghostly weapon and your weapon has already been found in the woods, you can haunt the player who found your weapon to retrieve it back.\n"
                "/ptinv: If you are in a party, shows its inventory\n\n"

                "If you like our game and want to help improve it, please support us at patreon!\nhttps://www.patreon.com/Clini\n\n"

                )
        if caller.admlevel > 0:
            text += (
                "\n"
                "/adm_inv: show a player's inventory\n"
                "/adm_st: show a player's status\n"
                "/adm_hp: show a player's health\n"
                "/adm_bst: show a player's bestiary\n"
                "/adm_zeus: kills a player\n"
                "/adm_proc_f: processes the forests\n"
                "/adm_activate_player\n"
                "/adm_give_arena\n"
                "/adm_infinite_arenas\n"
                "/adm_zero_rank\n"
                "/adm_find_player: searches player name and gives all ids with current name\n"
                "/adm_solve_multiple_party_players\n"
                "/adm_tier3\n"
                "/adm_next_level\n"
                "/adm_back_level\n"
                "/adm_give_af\n"
                "/adm_d_inv\n"
                "/adm_give_leaves\n"
                "/adm_check_probe_info: Checks the info of users regarding average time between dungeons.\n"
                "/adm_fix_stuck_players: Unstuck all players on the blacksmith and dungeons.\n"
                "/adm_multiple_party_players\n\n"
                )
        if caller.admlevel > 4:
            text += (
                "\n"
                "/adm_gm: give GM capabilities to a player\n"
                "/adm_gw: give a weapon to a player\n"
                "/adm_forest: starts or stops the forest for a player\n"
                "/adm_buff: buff a player\n"
                "/adm_heal: heals a player (fully)\n"
                "/adm_rename_player: renames a player and locks him\n"
                "/adm_list_gr_alts_in_pt\n"
                "/adm_sunflower: Removes a player from the sunflower\n\n"
                "/adm_move_account: clones a player into other. (make sure both are at camp and both are not in a party)"
                )
        if caller.admlevel > 9:
            text += (
                "\n"
                "/adm_adm: give admin capabilities to a player\n"
                "/adm_pls: print the list of all players\n"
                "/adm_dummy: create a new dummy player\n"
                "/adm_kill: kill a player (0 hp)\n"
                "/adm_lvlup: force a player to level up\n"
                "/adm_lv5: force a player to go to level 5\n"
                "/adm_rsp: all talent points returned, and class reset\n"
                "/adm_del: delete a player\n"
                "/adm_blessing: all players level becomes 5\n"
                "/save: save the game\n"
                "/sd: shut the server down\n"
                "/adm_clear_wating_from: clear the messagman's waiting_from\n"
                "/adm_encounter_f: force a forest encounter for a player. (only use when player is at the forest)\n"
                "/adm_encounter_df: force a deep forest encounter for a player. (only use when player is at the forest)\n"
                "/adm_give_talisman: give a talisman with chosen rarity to a player\n"
                "/adm_give_all_talismans: give all talismans defined in the database for a player\n"
                "/adm_clear_probe: Clears the info of time between dungeons for all players and parties\n"
                "/adm_add_patreon: Add a new patreon.\n"
                "/adm_remove_patreon: Remove patreon\n"
                "/adm_pay_patreon: self.adm_pay_patreon\n"
                "/adm_check_patreon: Prints all the patreons\n"
                "/adm_reset_wb: set the 'attacked_the_wb' of all players to False\n"
                "/adm_give_lots_of_leaves: gives all players 100 leaves."

                )

        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
        return False

    def show_credits(self, caller, *args):      # Printa a equipe Clini Studios mais contribuidores Patreon.
        text = emojize(f"Creators:\n\n"
               "Arthur Clini as the creator\n"
               "André Monteiro as level designer\n"
               "Vinicius Santiago, Juliana, red_jack and Caio as artists\n"
               "Paulo Jarschel and Lucas as coder\n\n"
               "Patrons:\n\n"
               "Mug Ruith with :banana: Banana Hammock :banana:\n\n"
               "Baltazar Devias\n\n"
               "Testers:\n\n"
               "Arthur, Paul, Red Moon, Juliana, Joaquim, 披狼皮的醉貓女, knightniwrem, André, Ming, Beatriz, Neto, Mateus, Caio, Helio, Rycers, iBittz, MJ, Bear, Lucas, Paulo, Lenner, Santiago.")
        self.bot.send_message(text=text,chat_id=caller.chat_id)
        return False


    # def show_rankings(self, caller, *args):
    #     best_weapon_in_forest = self.server.itemsdb.weapons[0]
    #     best_atk_in_forest = self.server.itemsdb.weapons[0]
    #     best_def_in_forest = self.server.itemsdb.weapons[0]
    #
    #     for arma in self.server.itemsdb.weapons:
    #         if arma.attributes[0]+arma.attributes[1] > best_weapon_in_forest.attributes[0]+best_weapon_in_forest.attributes[1]:
    #             best_weapon_in_forest = arma
    #         if arma.attributes[0] > best_atk_in_forest.attributes[0]:
    #             best_atk_in_forest = arma
    #         if arma.attributes[1] > best_def_in_forest.attributes[1]:
    #             best_def_in_forest = arma
    #
    #     best_player = self.server.playersdb.players["576620974"]
    #     best_atk = self.server.playersdb.players["576620974"]
    #     best_def = self.server.playersdb.players["576620974"]
    #
    #     for chat_id,jogador in self.server.playersdb.players.items():
    #         if jogador.atk + jogador.defense > best_player.atk + best_player.defense:
    #             best_player = jogador
    #         if jogador.atk > best_atk.atk:
    #             best_atk = jogador
    #         if jogador.defense > best_def.defense:
    #             best_def = jogador
    #
    #     text = emojize(f"Best weapons:\n\n"
    #            "Best weapon: {best_weapon_in_forest.name} :crossed_swords: {best_weapon_in_forest.attributes[0] :shield: {best_weapon_in_forest.attributes[1]}\n\n"
    #            "Weapon with highest attack {best_atk_in_forest.name} :crossed_swords: {best_atk_in_forest.attributes[0]}\n\n"
    #            "Weapon with highest defense {best_def_in_forest.name} :shield: {best_def_in_forest.attributes[1]}\n\n"
    #            "Best players:\n\n"
    #            "Best stats: {best_player.name} :crossed_swords: {best_player.atk} :shield: {best_player.defense}\n\n"
    #            "Best attack: {best_atk.name} :crossed_swords: {best_atk.atk}\n\n"
    #            "Best defense: {best_def.name} :shield: {best_def.defense}")
    #     self.bot.send_message(text=text,chat_id=caller.chat_id)
    #     return False
    def show_rankings(self, caller, *args):
        '''
            Printa:
                - Melhor arma em termos da soma de seu ataque e defesa;
                - Melhor arma em termos de ataque somente;
                - Melhor arma em termos de defesa somente;
                - Melhor jogador em termos da soma de seu ataque e defesa;
                - Melhor jogador em termos de ataque somente;
                - Melhor jogador em termos de defesa somente.
        '''
        def update_rankings():
            for ranking in self.server.rankings:
                for code in self.server.rankings[ranking]:
                    if code not in self.server.playersdb.players_and_parties:
                        self.server.rankings[ranking].remove(code)

            for code in self.server.playersdb.players_and_parties:
                if code[0] == "/":
                    self.server.playersdb.players_and_parties[code].calc_attributes()
                    if code not in self.server.rankings[emojize(":busts_in_silhouette: Global Rankings for Parties :busts_in_silhouette:")]:
                        self.server.rankings[emojize(":busts_in_silhouette: Global Rankings for Parties :busts_in_silhouette:")].append(code)
                else:
                    if code not in self.server.rankings[emojize(":bust_in_silhouette: Global Rankings for Players :bust_in_silhouette:")]:
                        self.server.rankings[emojize(":bust_in_silhouette: Global Rankings for Players :bust_in_silhouette:")].append(code)
                    if code not in self.server.rankings[emojize(":bust_in_silhouette: :crossed_swords:️ Player Arena Rankings :crossed_swords:️ :bust_in_silhouette:")]:
                        self.server.rankings[emojize(":bust_in_silhouette: :crossed_swords:️ Player Arena Rankings :crossed_swords:️ :bust_in_silhouette:")].append(code)
                    if code not in self.server.rankings[emojize(":incoming_envelope: Invitation Number Rankings :incoming_envelope:")]:
                        self.server.rankings[emojize(":incoming_envelope: Invitation Number Rankings :incoming_envelope:")].append(code)
                    if code not in self.server.rankings[emojize(":evergreen_tree: Lasted longer in the deep forest :evergreen_tree:")]:
                        self.server.rankings[emojize(":evergreen_tree: Lasted longer in the deep forest :evergreen_tree:")].append(code)


        def print_ranking_list(ranking_list, codigo, type):
            text = ""
            index = 1
            for code in ranking_list:
                jog = self.server.playersdb.players_and_parties[code]
                if type == "arena":
                    text += emojize(f"{index} - {jog.name} :flexed_biceps: {jog.arena_rank}\n")
                elif type == "invite":
                    text += emojize(f"{index} - {jog.name} :incoming_envelope: {jog.suc_refs}\n")
                elif type == "df_time":
                    stay_time = int(jog.longest_at_the_df)
                    minutes, seconds = divmod(stay_time, 60)
                    hours, minutes = divmod(minutes, 60)
                    days, hours = divmod(hours, 24)
                    text += emojize(f"{index} - {jog.name} :evergreen_tree: {days}d {hours}h {minutes}m {seconds}s\n")
                elif type == "global":
                    text += emojize(f"{index} - {jog.name} :crossed_swords: {jog.atk} :shield: {jog.defense}\n")
                index += 1
                if index > 10:
                    break
            if codigo in ranking_list:
                jog = self.server.playersdb.players_and_parties[codigo]
                place = ranking_list.index(codigo)+1
                if place > 10:
                    if not place == 11:
                        text += "...\n"
                    if type == "arena":
                        text += emojize(f"{place} - {jog.name} :flexed_biceps: {jog.arena_rank}\n")
                    elif type == "invite":
                        text += emojize(f"{place} - {jog.name} :incoming_envelope: {jog.suc_refs}\n")
                    elif type == "df_time":
                        stay_time = int(jog.longest_at_the_df)
                        minutes, seconds = divmod(stay_time, 60)
                        hours, minutes = divmod(minutes, 60)
                        days, hours = divmod(hours, 24)
                        text += emojize(f"{place} - {jog.name} :evergreen_tree: {days}d {hours}h {minutes}m {seconds}s\n")
                    elif type == "global":
                        text += emojize(f"{place} - {jog.name} :crossed_swords: {jog.atk} :shield: {jog.defense}\n")

            if not text:
                text = "This ranking list is empty."
            return text

        def sort_ranking_list(ranking_list, sort_by):
            new_ranking_list = copy.deepcopy(ranking_list)
            index = 0
            while index <= len(ranking_list) - 1:
                code = ranking_list[index]
                place = 0
                jog = self.server.playersdb.players_and_parties[code]
                for code2 in new_ranking_list:
                    jog2 = self.server.playersdb.players_and_parties[code2]
                    if getattr(jog2, sort_by) <= getattr(jog, sort_by):
                        break
                    place += 1
                new_ranking_list.remove(code)
                new_ranking_list.insert(place, code)
                index += 1
            return new_ranking_list

        def not_args_text():
            best_weapon_in_forest = self.server.itemsdb.weapons[0]
            best_atk_in_forest = self.server.itemsdb.weapons[0]
            best_def_in_forest = self.server.itemsdb.weapons[0]

            for arma in self.server.itemsdb.weapons:
                if arma.atributos[0]+arma.atributos[1] > best_weapon_in_forest.atributos[0]+best_weapon_in_forest.atributos[1]:
                    best_weapon_in_forest = arma
                if arma.atributos[0] > best_atk_in_forest.atributos[0]:
                    best_atk_in_forest = arma
                if arma.atributos[1] > best_def_in_forest.atributos[1]:
                    best_def_in_forest = arma

            text = emojize(f"Best weapons that can be found at the forest:\n\n"
                f"Best weapon: {best_weapon_in_forest.name} :crossed_swords: {best_weapon_in_forest.atributos[0]} :shield: {best_weapon_in_forest.atributos[1]}\n\n"
                f"Highest attack: {best_atk_in_forest.name} :crossed_swords: {best_atk_in_forest.atributos[0]}\n\n"
                f"Highest defense: {best_def_in_forest.name} :shield: {best_def_in_forest.atributos[1]}\n\n"
                # f"Ranking of Players:\n\nBest attack: {best_atk.name} :crossed_swords: {best_atk.atk}\n\nBest defense: {best_def.name} :shield: {best_def.defense}\n\n"
                # f"Ranking List:\n\n"
                )

            text += emojize(f"What do you want to look at?")

            return text

        update_rankings()

        if not args:
            text = not_args_text()
            self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.inline_rankings_keyboard_reply_markup)
            return self.def_wait_time

        else:
            try:
                codigo = caller.chat_id
                ranking_choice = args[-1]
                sort_by = ""
                if caller.chat_id not in self.ranking_comms:
                    if ranking_choice == emojize(":busts_in_silhouette: Global Rankings for Parties :busts_in_silhouette:"):
                        codigo = caller.pt_code

                    elif ranking_choice == emojize(":bust_in_silhouette: :crossed_swords:️ Player Arena Rankings :crossed_swords:️ :bust_in_silhouette:"):
                        ranking_list = sort_ranking_list(self.server.rankings[ranking_choice], "arena_rank")
                        text = print_ranking_list(ranking_list, codigo, "arena")
                        self.bot.edit_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.inline_rankings_keyboard_reply_markup, message_id = args[0])
                        return self.def_wait_time

                    elif ranking_choice == emojize(":incoming_envelope: Invitation Number Rankings :incoming_envelope:"):
                        ranking_list = sort_ranking_list(self.server.rankings[ranking_choice], "suc_refs")
                        text = print_ranking_list(ranking_list, codigo, "invite")
                        self.bot.edit_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.inline_rankings_keyboard_reply_markup, message_id = args[0])
                        return self.def_wait_time
                    elif ranking_choice == emojize(":evergreen_tree: Lasted longer in the deep forest :evergreen_tree:"):
                        ranking_list = sort_ranking_list(self.server.rankings[ranking_choice], "longest_at_the_df")
                        text = print_ranking_list(ranking_list, codigo, "df_time")
                        self.bot.edit_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.inline_rankings_keyboard_reply_markup, message_id = args[0])
                        return self.def_wait_time
                    elif ranking_choice == emojize(":BACK_arrow: Back :BACK_arrow:"):
                        keyboard = self.server.keyboards.return_proper_keyboard_based_on_location(caller)
                        text = "You can explore more to climb the rankings!"
                        self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = keyboard)
                        return False
                    self.ranking_comms[caller.chat_id] = {"ranking_choice": ranking_choice, "codigo": codigo}
                    ranking_list = sort_ranking_list(self.server.rankings[ranking_choice], "stats")
                    text = print_ranking_list(ranking_list, codigo, "global")
                    self.bot.edit_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.inline_sort_by_keyboard_reply_markup, message_id = args[0])
                    return self.def_wait_time

                else:
                    sort_by = args[-1]
                    sort = ""
                    if sort_by == emojize(":crossed_swords:️ Attack :crossed_swords:️"):
                        sort = "atk"
                    elif sort_by == emojize(":shield: Defense :shield:"):
                        sort = "defense"
                    elif sort_by == emojize(":crossed_swords: :shield: Total Stats :shield: :crossed_swords:️"):
                        sort = "stats"
                    elif sort_by == emojize(":BACK_arrow: Back :BACK_arrow:"):
                        del self.ranking_comms[caller.chat_id]
                        text = not_args_text()
                        self.bot.edit_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.inline_rankings_keyboard_reply_markup, message_id = args[0])
                        return self.def_wait_time

                    ranking_choice = self.ranking_comms[caller.chat_id]["ranking_choice"]
                    ranking_list = sort_ranking_list(self.server.rankings[ranking_choice], sort)
                    text = print_ranking_list(ranking_list, codigo, "global")
                    self.bot.edit_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.inline_sort_by_keyboard_reply_markup, message_id = args[0])
                    return self.def_wait_time

            except Exception:
                traceback.print_exc()
                text = "Something went wrong, try again."
                if caller.chat_id in self.ranking_comms:
                    del self.ranking_comms[caller.chat_id]
                self.bot.edit_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.inline_rankings_keyboard_reply_markup, message_id = args[0])
                return self.def_wait_time









        # player_list = list(self.server.active_players)
        # ranking_list = []
        # for chat in player_list:
        #     jog = self.server.playersdb.players_and_parties[chat]       # Jogador fixo que será comparado com os outros jogadores em ranking_list.
        #     place = 0
        #     if ranking_list:
        #         for player in ranking_list:
        #             if player.atk + player.defense <= jog.atk + jog.defense:
        #                 break
        #             place += 1
        #         ranking_list.insert(place, jog)
        #     else:
        #         ranking_list.append(jog)
        #
        # best_atk = ranking_list[0]
        # best_def = ranking_list[0]
        #
        # for chat_id, jogador in self.server.playersdb.players_and_parties.items():
        #     if chat_id[0] != "/":
        #         if jogador.atk > best_atk.atk:
        #             best_atk = jogador
        #         if jogador.defense > best_def.defense:
        #             best_def = jogador




        # best_player = self.server.playersdb.players["576620974"]


        # text = text.replace("_","\\_")
        # self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode = 'MARKDOWN')

        # text += emojize(f"You can also check the best players that are facing the :sunflower: *Helianth, the Sunny* :sunflower: right now with /WB_rankings!")

        return False



    # É a árvore de comandos referente às habilidade de classe acessado pelo player via o keyboard "Class".
    def print_self_coms(self, caller, *args):
        '''
            Árvore de comandos referente às habilidades de classe do player.

            Esta função funciona em duas etapas:
                O jogador insere um comando através do keyboard "Class" do chat bot.
                Logo depois, seus comandos referentes à classe são exibidos para o jogador.
                Um tempo de espera é ativado e o bot passa a esperar por uma resposta.
                Se o player resolver utilizar alguma habilidade, a função é ativada novamente
                para executar tal habilidade.

            Parâmetros:
                - caller(class): player que insere "Class" via o keyboard do chat bot.
                - args(list): lista contendo os comandos anteriores (menos o primeiro comando) e o atual da árvore de comandos.
        '''
        if not args:        # Se não houver comandos após o primeiro, então este é o primeiro comando.
            caller.print_self_coms()        # Printa os comandos de classe para o jogador.
            if caller.classe != caller.vanilla_class:
                return self.def_wait_time       # Após os comandos serem exibidos, o bot espera uma resposta.
            else:       # A classe vanilla não possui habilidades, então a árvore morre aqui.
                return False
        else:
            if args[-1] in caller.actions or args[-1][:5] in caller.actions:    # Checa se o comando inserido é válido para o player. O segundo checa se o comando é do tipo \heal.

                if caller.pt_code:      # Checa se o player está numa party.

                    if caller.classe == "Explorer":

                        if args[-1][:5] == "/heal":
                            target_chat = args[-1][6:]     # Se o player está curando outro jogador, o chat id do jogador alvo estará escrito após o índice 5 do string.
                            if target_chat:
                                if target_chat in self.server.playersdb.players_and_parties[caller.pt_code].chat_ids:        # Checa se o player alvo é um membro da party.
                                    self.heal_in_pt(target_chat, caller.chat_id, 3)     # Cura jogador alvo.
                                else:
                                    self.bot.send_message(text="Player not found! Aborting.", chat_id = caller.chat_id)
                            else:
                                caller.actions[args[-1]]()      # Se não houver chat id após /heal, o jogador se cura.
                        if args[-1] == "/g_dg":
                            if self.server.playersdb.players_and_parties[caller.pt_code].location == "forest":       # Checa se a party está na floresta para poderem utilizar o /g_dg.

                                self.server.travelman.set_travel(self.server.playersdb.players_and_parties[caller.pt_code], "dg", caller.e_travel_time)
                                text = f"{caller.name} Used a map to a dungeon, {caller.pt_name} will get there in {round(self.server.playersdb.players_and_parties[caller.pt_code].travel_time/60)} minutes."

                                self.server.playersdb.players_and_parties[caller.pt_code].travel_guider = caller

                                for jog in self.server.playersdb.players_and_parties[caller.pt_code].players:
                                    self.bot.send_message(text=text,chat_id=jog.chat_id)

                        if args[-1] == "/g_sanct":
                            if self.server.playersdb.players_and_parties[caller.pt_code].location == "forest":       # Checa se a party está na floresta para poderem utilizar o /g_dg.

                                self.server.travelman.set_travel(self.server.playersdb.players_and_parties[caller.pt_code], "sanct", caller.e_travel_time)
                                text = f"{caller.name} Used a map to a sanctuary, {caller.pt_name} will get there in {round(self.server.playersdb.players_and_parties[caller.pt_code].travel_time/60)} minutes."

                                self.server.playersdb.players_and_parties[caller.pt_code].travel_guider = caller

                                for jog in self.server.playersdb.players_and_parties[caller.pt_code].players:
                                    self.bot.send_message(text=text,chat_id=jog.chat_id)

                        if args[-1] == "/g_deep_forest":
                            if self.server.playersdb.players_and_parties[caller.pt_code].location == "forest":       # Checa se a party está na floresta para poderem utilizar o /g_dg.

                                self.server.travelman.set_travel(self.server.playersdb.players_and_parties[caller.pt_code], "deep_forest", caller.e_travel_time)
                                text = f"{caller.name} Used a map to the deep forest, {caller.pt_name} will get there in {round(self.server.playersdb.players_and_parties[caller.pt_code].travel_time/60)} minutes."

                                self.server.playersdb.players_and_parties[caller.pt_code].travel_guider = caller

                                for jog in self.server.playersdb.players_and_parties[caller.pt_code].players:
                                    self.bot.send_message(text=text,chat_id=jog.chat_id)

                        if args[-1] == "/g_sunflower":
                            # Checa se a party está na floresta para poderem ir para o World Boss.
                            if self.server.playersdb.players_and_parties[caller.pt_code].location == "forest":

                                self.server.travelman.set_travel(self.server.playersdb.players_and_parties[caller.pt_code], "plot_msg", caller.e_travel_time)
                                text = f"{caller.name} Used a map to a dungeon, {caller.pt_name} will get there in {round(self.server.playersdb.players_and_parties[caller.pt_code].travel_time/60)} minutes."

                                self.server.playersdb.players_and_parties[caller.pt_code].travel_guider = caller

                                for jog in self.server.playersdb.players_and_parties[caller.pt_code].players:
                                    self.bot.send_message(text=text,chat_id=jog.chat_id)

                    elif caller.classe == "Wizard":

                        if args[-1][:5] == "/heal":
                            target_chat = args[-1][6:]
                            if target_chat:
                                if target_chat in self.server.playersdb.players_and_parties[caller.pt_code].chat_ids:
                                    self.heal_in_pt(target_chat, caller.chat_id, caller.buff_man.buff_state+1)
                                else:
                                    self.bot.send_message(text="Player not found! Aborting.", chat_id = caller.chat_id)
                            else:
                                caller.actions[args[-1]]()
                        elif args[-1][:5] == "/buff":

                            target_chat = args[-1][6:]
                            if target_chat:
                                if target_chat in self.server.playersdb.players_and_parties[caller.pt_code].chat_ids:
                                    self.buff_in_pt(target_chat, caller.chat_id, caller.spell_power)
                                else:
                                    self.bot.send_message(text="Player not found! Aborting.", chat_id = caller.chat_id)
                            else:
                                if args[-1] in caller.actions:
                                    caller.actions[args[-1]]()
                                elif args[-1][:5] in caller.actions:
                                    caller.actions[args[-1][:5]]()
                        else:
                            if args[-1] in caller.actions:
                                caller.actions[args[-1]]()
                            elif args[-1][:5] in caller.actions:
                                caller.actions[args[-1][:5]]()
                    else:
                        if args[-1] in caller.actions:
                            caller.actions[args[-1]]()
                        elif args[-1][:5] in caller.actions:
                            caller.actions[args[-1][:5]]()
                else:
                    if args[-1] in caller.actions:
                        caller.actions[args[-1]]()
                    elif args[-1][:5] in caller.actions:
                        caller.actions[args[-1][:5]]()

                # if caller.pt_code:
                #     for chat,jog in self.server.parties_codes[caller.pt_code].items(): # Redundante?
                #         if isinstance(jog, player.Player):
                #             self.server.parties_codes[caller.pt_code][chat] = self.server.playersdb.players[chat]

                return self.def_wait_time


            return False        # Se o comando inserido não for válido, a árvore morre aqui.

    def heal_in_pt(self, target_chat_id, caster_id, power):
        '''
            Habilidade de cura em parties. Isto é uma adaptação da função de cura normal
            da classe Wizard ou Explorer para poder curar membros da party.

            Parâmetros:
                - target_chat_id (str): chat id do jogador a ser curado;
                - caster_id (str): chat id do jogador que usará a cura;
                - power (int): força da cura. Quanto maior o valor, mais vida é curada do membro alvo pela cura.
        '''
        if self.server.playersdb.players_and_parties[caster_id].ap > 0:     # Checa se o player caster possui stamina ou mana para curar.

            w_limb = -1
            w_limb_health = 3
            for limb_i in range(len(self.server.playersdb.players_and_parties[target_chat_id].hp)):     # Procura o membro com a menor vida possível.
                if self.server.playersdb.players_and_parties[target_chat_id].hp[limb_i].health < w_limb_health:
                    w_limb = limb_i     # Carrega o índice do membro de menor vida
                    w_limb_health = self.server.playersdb.players_and_parties[target_chat_id].hp[limb_i].health     # Vida do membro de menor vida.

            limb_i = w_limb  # self.random_damaged_limb_index(self.hp)
            if limb_i > -1:     # Checa se houve algum membro com vida menor que 3.
                if power > 3 - w_limb_health:   # Subtrai o valor a ser curado do membro.
                    power = 3 - w_limb_health
                self.server.playersdb.players_and_parties[target_chat_id].hp[limb_i].health += power    # Cura o membro do jogador alvo.
                self.server.playersdb.players_and_parties[caster_id].ap -= 1    # Subtrai a mana/stamina do jogador caster.
                text = f"Your {self.server.playersdb.players_and_parties[target_chat_id].hp[limb_i].name} have been succesfully healed!"
                self.bot.send_message(text=text, chat_id=target_chat_id)
                text = f"You healed the {self.server.playersdb.players_and_parties[target_chat_id].hp[limb_i].name} of {self.server.playersdb.players_and_parties[target_chat_id].name}"
                self.bot.send_message(text=text, chat_id=caster_id)
            else:
                text = "Target player is in perfect health"
                self.bot.send_message(text=text, chat_id=caster_id)
        else:

            text = "Not enought mana or stamina"
            self.bot.send_message(text = text, chat_id = caster_id)

    def buff_in_pt(self, target_chat_id, caster_id, spell_power):
        '''
            Habilidade de buff em parties. Isto é uma adaptação da função de buff normal
            da classe Wizard para poder buffar membros da party.

            Parâmetros:
            - target_chat_id (str): chat id do jogador a ser buffado;
            - caster_id (str): chat id do jogador que usará o buff;
            - spell_power (int): força do buff. Quanto maior o valor, maior a chance do buff ser bem sucedido.
    '''
        self.server.playersdb.players_and_parties[caster_id].calc_buff_difficulty()     # Calcula a dificuldade de buffar (seja ele mesmo, ou outro jogador).
        if self.server.playersdb.players_and_parties[caster_id].ap > 0:     # Checa se o jogador possui mana o suficiente.
            if self.server.playersdb.players_and_parties[target_chat_id].buff_man.buff_state < len(self.server.playersdb.players_and_parties[target_chat_id].buff_man.states_list) - 1:     # Checa se o jogador alvo já está no estado máximo de buff.
                self.server.playersdb.players_and_parties[caster_id].ap -= 1
                chance = rd.randint(1, self.server.playersdb.players_and_parties[caster_id].buff_difficulty[self.server.playersdb.players_and_parties[target_chat_id].buff_man.buff_state])
                if chance == 1:
                    self.bot.send_message(text=f"You succesfully buffed {self.server.playersdb.players_and_parties[target_chat_id].name}", chat_id=caster_id)
                    self.bot.send_message(text=f"You have been buffed by {self.server.playersdb.players_and_parties[caster_id].name}", chat_id=target_chat_id)
                    # previous = self.server.playersdb.players_and_parties[target_chat_id].buff_man.buff_state
                    self.server.playersdb.players_and_parties[target_chat_id].buff_man.buff_state += 1
                    # if previous+1 > self.server.parties_codes[self.server.playerdb.players[target_chat_id].pt_code][target_chat_id].buff_man.buff_state:
                    #     self.server.parties_codes[self.server.playerdb.players[target_chat_id].pt_code][target_chat_id].buff_man.buff_state += 1

                    self.server.playersdb.players_and_parties[target_chat_id].calc_attributes()     # Com o buff bem sucedido, os status do jogador alvo mudam. "calc_attributes" é a função que atualiza os status do player.
                    self.server.playersdb.players_and_parties[caster_id].calc_attributes()
                    # self.server.playersdb.players_and_parties[self.server.playersdb.players_and_parties[target_chat_id].pt_code][target_chat_id].calc_attributes()
                else:
                    self.bot.send_message(text=f"You failed to buff {self.server.playersdb.players_and_parties[target_chat_id].name}", chat_id=caster_id)

            else:
                self.bot.send_message(text=f"{self.server.playersdb.players_and_parties[target_chat_id].name} is already the most powerful being, no need to buff", chat_id=caster_id)
        else:
            text = "Not enought mana or stamina"
            self.bot.send_message(text = text, chat_id = caster_id)


    def new_player(self, caller, caller_id = None, *args):
        '''
            Este é um comando interno do DW. Ela é chamada toda vez que um novo player
            começa o jogo, ou quando o jogador é banido.
        '''
        if caller.chat_id in self.server.bl_controller.ban_dic:     # Checa se o jogador está banido.
            if self.server.bl_controller.ban_dic[caller.chat_id].is_banned:
                text = f"Once you had an offensive name. Now you are locked with this name for {self.server.bl_controller.ban_dic[caller.chat_id].ban_time} days"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                caller.set_name("once an offensive name, now just shame")
                return False
        if not args:        # Se não houver args, então o jogador acabou de entrar no jogo.
            if caller.referal:      # Checa se o jogador entrou por convite de outro jogador do DW.

                text = emojize(f"A sea of trees coats the land as far as the eye can see. They cover tall mountains, they part for rivers, but the canopy never ceases.\n\n"
                                f"The forest is relentless; the creatures that roam the trails are constantly drawn to humans, like an immune system fighting off pathogens."
                                f" Places and landmarks shift around like living beings, giving maps limited use. Nevertheless, people still try their hardest to survive."
                                f" It's safest around the campfire, where most of them rest and pass the time.\n\n"
                                f" Welcome to the Dark Woods.\n"
                                f" You have been called by {self.server.playersdb.players_and_parties[caller.referal].name}\n"
                                f" You just found a *wooden sword*\n\n"
                                f"The guardian spirits wish to know your name")
            else:

                text = emojize("A sea of trees coats the land as far as the eye can see. They cover tall mountains, they part for rivers, but the canopy never ceases.\n\n"
                                "The forest is relentless; the creatures that roam the trails are constantly drawn to humans, like an immune system fighting off pathogens."
                                " Places and landmarks shift around like living beings, giving maps limited use. Nevertheless, people still try their hardest to survive."
                                " It's safest around the campfire, where most of them rest and pass the time.\n\n"
                                " Welcome to the Dark Woods.\n\n"
                                "The guardian spirits wish to know your name")






            self.bot.send_message(text=text, chat_id=caller.chat_id, parse_mode = "MARKDOWN")
            return 1
        else:       # Se houver args, então o jogador respondeu a mensagem enviada pelo bot contendo o nome dele.
            name = args[-1]

            print(f"{name} has joined the woods!")
            if caller.referal:
                ref_text = f"{name} just used your code to join the game! When he chooses a class you will gain 1 extra minute to answer dungeons and blacksmiths!"
                self.bot.send_message(chat_id=caller.referal, text = ref_text)
            caller.set_name(name)
            self.bot.send_audio(chat_id=caller.chat_id, audio=open('music/DWtheme.mp3', 'rb'))
            text = (f"A newly minted adventurer, {name} prepares for their first expedition with the blessing of the gods.\n"
                    "You make one last mental note that if you ever want to talk to someone from the camp, you need only recite the words of power: https://t.me/DWcommchat")
            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
            return False

    def erase(self, caller, *args):
        '''
            Função acessada pelo comando /erase.

            Este é um comando secreto do player. Sua função é deletar completamente o seu personagem do DW.
        '''
        if not args:
            text = "Are you absolutely sure you want to erase your character?"
            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.forest_return_reply_markup)
            return self.def_wait_time
        else:
            if args[-1] == "yes":
                if caller.classe != "Unknown" and caller.referal:
                    self.server.playersdb.players_and_parties[caller.referal].suc_refs -= 1
                self.death.die(caller.chat_id)
                # self.party(self.server.playersdb.players_and_parties[caller.chat_id],"/leave")
                self.server.old_players.add_player(caller.chat_id, caller.leaves)
                del self.server.playersdb.players_and_parties[caller.chat_id]
                return False

            elif args[-1] == "no":
                self.bot.send_message(text="Alrighty then", chat_id=caller.chat_id, reply_markup=self.defkb)
            else:
                return False

    def show_stats(self, caller, target=None):
        '''
            Função acessada através do comando /me.

            Mostra todos os status do player.

            A função também pode ser chamada por um adm do DW para ver os status do player alvo.

            Parâmetros:
                - caller (class): se não houver target, caller = player que deu /me. Se houve target, então caller = adm;
                - target (class): se não houver target, então targer = player que deu /me (veja abaixo). Se houve target, então target = player alvo.
        '''
        show_links = False
        if not target or caller.admlevel < 1:       # Checa se houve target e se o caller é um adm com permissão de ver os status de outros players.
            target = caller
            show_links = True
        remtime = 0
        if caller.pt_code:
            if caller.pt_code in self.server.woods.players:
                if self.server.woods.players[caller.pt_code]["active"] and self.server.playersdb.players_and_parties[caller.chat_id].location != "forest":
                    self.server.playersdb.players_and_parties[caller.pt_code].location = "forest"
        else:
            if caller.chat_id in self.server.woods.players:
                if self.server.woods.players[caller.chat_id]["active"] and caller.location != "forest":
                    caller.location = "forest"
        if (caller.location == "forest" or caller.location == "dungeon") and not caller.pt_code:
            self.server.woods.process()
            if (not caller.chat_id in self.server.woods.players) and (not caller.chat_id in self.server.deep_forest_manager.jogs):
                caller.location = "camp"

            # caller.is_at_forest = caller.chat_id in self.server.woods.players
            # if caller.location == "forest":
            remtime = int(self.server.woods.players[caller.chat_id]["rem_time"]/60)
        elif caller.pt_code and (self.server.playersdb.players_and_parties[caller.pt_code].location == "forest" or self.server.playersdb.players_and_parties[caller.pt_code].location == "dungeon"):
            self.server.woods.process()
            if not caller.pt_code in self.server.woods.players:
                self.server.playersdb.players_and_parties[caller.pt_code].location = "camp"
            # self.server.parties_codes[caller.pt_code]["is_at_forest"] = caller.pt_code in self.server.woods.players
            # if caller.pt_code and self.server.playersdb.players_and_parties[caller.pt_code].location == "forest":
            remtime = int(self.server.woods.players[caller.pt_code]["rem_time"]/60)

        if caller.location == "deep_forest" and not caller.pt_code:
            self.server.deep_forest_manager.process()
            if (not caller.chat_id in self.server.deep_forest_manager.jogs):
                caller.location = "forest"

            # caller.is_at_forest = caller.chat_id in self.server.woods.players
            if caller.location == "forest":
                remtime = int(self.server.woods.players[caller.chat_id]["rem_time"]/60)
            elif caller.location == "deep_forest":
                remtime = int(self.server.deep_forest_manager.jogs[caller.chat_id].stay_time/60)
        elif caller.pt_code and self.server.playersdb.players_and_parties[caller.pt_code].location == "deep_forest":
            self.server.deep_forest_manager.process()
            if not caller.pt_code in self.server.deep_forest_manager.jogs:
                self.server.playersdb.players_and_parties[caller.pt_code].location = "forest"
            # self.server.parties_codes[caller.pt_code]["is_at_forest"] = caller.pt_code in self.server.woods.players
            if caller.pt_code and self.server.playersdb.players_and_parties[caller.pt_code].location == "forest":
                remtime = int(self.server.woods.players[caller.pt_code]["rem_time"]/60)
            elif caller.pt_code and self.server.playersdb.players_and_parties[caller.pt_code].location == "deep_forest":
                remtime = remtime = int(self.server.deep_forest_manager.jogs[caller.pt_code].stay_time/60)

        if self.server.is_day:
            s = emojize(":sun: Day\n\n")
        else:
            s = emojize(":waning_crescent_moon: Night\n\n")
        s += emojize(target.get_stats_string(remtime))
        s += emojize(f"Leaves :leaf_fluttering_in_wind:: {caller.leaves}\n")
        if show_links:
            s += (f"Check the posible commands: /help")

        s = s.replace("_", "\\_")
        # s = s.replace("*", "\\*")
        if caller.pt_code and self.server.playersdb.players_and_parties[caller.pt_code].location == "camp" or (not caller.pt_code and caller.location == "camp"):
            self.bot.send_message(text=s, chat_id=caller.chat_id, parse_mode='MARKDOWN', reply_markup=self.defkb2)
        else:
            self.bot.send_message(text=s, chat_id=caller.chat_id, parse_mode='MARKDOWN', reply_markup=self.defkb)
        return False

    def show_inv(self, caller, *args):
        '''
            Função chamada através do comando /inv.

            Árvore de comandos que mostra o inventário do player, equipa itens e compartilha armas. (Note que para usar mapas, deve-se equipá-los)

        '''
        if not args:    # Se não houver args, o player deu /inv.
            s = ""
            for i in caller.inventory:  # Coleta todos os itens do player.
                n_code = i.code
                n_code = n_code.replace("*", "\\*")
                s += f"*{i}* /e_{n_code}\n" #emojize(f"*{i.name}* :crossed_swords:{i.atributos[0]} :shield:{i.atributos[1]} /e_{i.code}\n")
            if s == "":
                s = "You don't have anything"
                self.bot.send_message(text=s, chat_id=caller.chat_id, parse_mode='MARKDOWN', reply_markup=self.defkb)
                return False    # Se o player não tiver nada, a árvore morre aqui.
            else:
                s += "\nEquip a weapon using the '/e_' codes above. Use /unequip to unequip any weapon. To see the weapon description use the /d_(code) command."
                if caller.pt_code:      # Se o player estiver numa party, é possível compartilhar o equipamento.
                    s += "To add a weapon to shared inventory, /s_(code)"
                s = s.replace("_", "\\_")
                self.bot.send_message(text=s, chat_id=caller.chat_id, parse_mode='MARKDOWN', reply_markup=self.defkb)
                return self.def_wait_time*10

        else:       # Se houve args, então passamos do primeiro comando (/inv) da árvore.
            code = args[-1]
            # try:
            #     # POHA É CLARO Q VAI DAR PAU. treco NÃO ESTÁ DEFINIDO
            #     direct_join = self.server.messageman.commtrees[1].join_party(treco, caller, direct_join = True) # Mano q porra é essa?
            #     if direct_join:
            #         return self.def_wait_time
            # except:
            #     pass
            equipped = False
            is_description = False
            for item in caller.inventory:       # Inicialmente, é tentado equipar o item com o código dado, mesmo se o código não for de item.
                if f"/e_{item.code}" == code:
                    if caller.pt_code and isinstance(item, items.dg_map):       # Checa se o item tentado é uma mapa e se o player está em party.
                        text = "You are in a party! To use the map you should share it with your teammates!"
                        self.bot.send_message(text=text,chat_id=caller.chat_id)
                    else:
                        # print(type(item))
                        item.action(caller)     # Equipa o item.
                    caller.calc_attributes()    # Atualiza os status do player.
                    equipped = True
                    break
                if f"/d_{item.code}" == code:
                    new_name = copy.copy(item.name)
                    new_name.replace("_", "\\_")
                    new_name.replace("*", "\\*")
                    text = emojize(f"{new_name}\n"
                                    f"Original weapon stats: {item.atributos[0]} :crossed_swords: {item.atributos[1]} :shield:\n"
                                    f"Weapon type: {item.type2}\n\n"
                                    f"Weapon Talismans: {item.talisman_list()}\n\n"
                                    f"Weapon Powers: {item.power_list()}\n\n"
                                    f"Description:\n\n"
                                    f"{item.description}")
                    self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode = "MARKDOWN")
                    is_description = True
                    break

            if equipped:
                s = "Successfully equipped"
                self.bot.send_message(text=s, chat_id=caller.chat_id, reply_markup=self.defkb)
            elif code == "/unequip":
                if caller.weapon:       # Checa se o player possui qualquer arma equipado.
                    if caller.weapon.is_shared_and_equipped:        # Checa se o item equipado é compartilhado.
                        for item in self.server.playersdb.players_and_parties[caller.pt_code].inventory:
                            if item.code == caller.weapon.code and item.owner == caller.weapon.owner:
                                item.is_shared_and_equipped = False

                    caller.weapon.unequip(caller)
                    caller.weapon = None        # Desequipa o item.
                    caller.calc_attributes()        # Atualiza os status do player
                    s = "Successfully unequipped"
                    self.bot.send_message(text=s, chat_id=caller.chat_id, reply_markup=self.defkb)


            elif caller.pt_code:        # Em última caso, o player irá compartilhar o item.
                found = False
                for i in range(len(caller.inventory)):      # Procura o item a ser compartilhado.
                    item = caller.inventory[i]
                    item.owner = caller.chat_id         # Marca o item com o chat id do dono.
                    if f"/s_{item.code}" == code:       # Checa o código do item a ser compartilhado.
                        if caller.weapon and item.code == caller.weapon.code:       # Checa se o item a ser compartilhado está equipada pelo player.
                            caller.weapon.unequip(caller)
                            caller.weapon = None        # Se estiver ela é desequipada.
                            caller.calc_attributes()
                        found = True
                        item.flag = len(self.server.playersdb.players_and_parties[caller.pt_code].inventory)
                        number = 0
                        for arma in self.server.playersdb.players_and_parties[caller.pt_code].inventory:    # Para evitar que dois itens tenham o mesmo código, números serão adicionados no código para diferenciar os itens.

                            if arma.ac_code == item.ac_code:
                                number += 1
                        if number == 0:
                            number = ""
                        item.ac_code = item.code + f"{number}"
                        item.ac_code = item.code + f"{number}"
                        temp_ac = item.ac_code
                        item.ac_code = item.code
                        item.code = temp_ac
                        self.server.playersdb.players_and_parties[caller.pt_code].inventory.append(copy.deepcopy(item))     # Faz uma cópia verdadeira do item no inventário da party.

                        del caller.inventory[i]         # Exclui o item do inventário do player.
                        if caller.weapon and caller.weapon.code == item.code:       # Redundante?
                            caller.weapon = None
                        break
                if found:       # Checa o item foi encontrado ou não (isto é, se o código inserido é válido).
                    s = f"Succesfully shared {item.name}"
                    self.bot.send_message(text=s, chat_id=caller.chat_id, reply_markup=self.defkb)
                else:
                    if not is_description:
                        s = f"Weapon code not found"
                        self.bot.send_message(text=s, chat_id=caller.chat_id, reply_markup=self.defkb)
                    # for jog in self.server.playersdb.players_and_parties[caller.pt_code].players:
                    #     self.server.playersdb.players_and_parties[caller.pt_code][chat] = self.server.playersdb.players_and_parties[chat]
                return False
            else:
                if not is_description:
                    s = "You don't have that weapon"
                    self.bot.send_message(text=s, chat_id=caller.chat_id, reply_markup=self.defkb)
                return False
            # if caller.pt_code:
                # for jog in self.server.playersdb.players_and_parties[caller.pt_code].players:
                #     self.server.playersdb.players_and_parties[caller.pt_code][chat] = self.server.playersdb.players_and_parties[chat]
            return self.def_wait_time*10

    def show_pokedex(self, caller, target=None):
        '''
            Mostra o bestiário do jogador. Também pode ser utilizada por adms do DW para ver o bestiário do player alvo.
        '''
        if not target or caller.admlevel < 1:
            target = caller

        s = ""
        if len(target.pokedex) > 0:
            for i in range(0, len(target.pokedex)):
                s += emojize(f"{target.pokedex[i]}\n")
        else:
            s = "You haven't seen any beasts yet"

        self.bot.send_message(text=s, chat_id=caller.chat_id, reply_markup=self.defkb)
        return False

    def show_health(self, caller, target=None):
        '''
            Mostra os membros do jogador. Também pode ser utilizada por adms do DW para ver os membros do jogador alvo.
        '''
        if not target or caller.admlevel < 1:
            target = caller

        s = ""
        for limb in target.hp:
            if target == caller:
                try:
                    last = limb.states[limb.health][-1]
                    t_check = [ emojize(":cross_mark:"),
                                emojize(":red_heart:"),
                                emojize(":yellow_heart:"),
                                emojize(":green_heart:"),]
                    if not last in t_check:
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
                        for i in range(len(limb.states)):
                            limb.states[i] += f" {health_icons[i]}"
                    s += emojize(f"Your {limb.name} is {limb.states[limb.health]}\n")
                except:
                    # Can happen with some badly formed druids
                    limb.states = caller.limb_states_generator(limb.health)
                    last = limb.states[limb.health][-1]
                    t_check = [ emojize(":cross_mark:"),
                                emojize(":red_heart:"),
                                emojize(":yellow_heart:"),
                                emojize(":green_heart:"),]
                    if not last in t_check:
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
                        for i in range(len(limb.states)):
                            limb.states[i] += f" {health_icons[i]}"

                    s += emojize(f"Your {limb.name} is {limb.states[limb.health]}\n")

            else:
                s += emojize(f"{target.name}'s {limb.name} is {limb.states[limb.health]}\n")


        self.bot.send_message(text=s, chat_id=caller.chat_id)
        return False

    def show_name_change(self, caller, *args):
        '''
            Função que troca o nome do jogador.
        '''
        if caller.chat_id in self.server.bl_controller.ban_dic:     # Checa se o player está banido. Caso esteja, ele não poderá trocar o nome.
            if self.server.bl_controller.ban_dic[caller.chat_id].is_banned:
                text = f"Once you had an offensive name. Now you are locked with this name for {self.server.bl_controller.ban_dic[caller.chat_id].ban_time} days"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return False
        if not args:
            text = "Please tell me your name"
            self.bot.send_message(text=text, chat_id=caller.chat_id)
            return self.def_wait_time
        else:
            name = args[-1]
            if len(name) > 2048:
                name = name[:2048]
            caller.set_name(name)
            text = "Hooray, changing your name was never that easy!"
            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
            return False

    def show_haunt_menu(self, caller, *args):
        '''
            Allows the player to haunt the player who found your weapon
        '''
        if not args:
            if (caller.weapon.name.startswith(emojize(":jack-o-lantern: Hallowed")) or caller.weapon.name.startswith(emojize(":ghost::alien_monster: Ghostly"))) and not caller.weapon in caller.inventory:
                text = emojize(f"You can haunt the player who found your equipped weapon. Beware, any blacksmith modifications will turn the weapon unhautable as it is not the same weapon anymore.\n\n")
                text += "Here is the player who got you weapon (if list is empty it means that the weapon has already been modified or anyone has found it) (click /hnt_ to haunt that player):\n\n"
                if caller.weapon.name.startswith(emojize(":jack-o-lantern: Hallowed")):
                    red_name = caller.weapon.name[11:-2]
                else:
                    red_name = caller.weapon.name[11:]
                wep_tals = caller.weapon.talismans
                found = False
                for chat,pl in self.server.playersdb.players_and_parties.items():
                    if chat[0] == "/":
                        for wep in pl.inventory:
                            if wep.name == red_name and wep.talismans == wep_tals:
                                found = True
                                text += emojize(f":busts_in_silhouette: Party inventory: {pl.pt_name}: /hnt_{chat[1:]}")
                                break
                    else:
                        for wep in pl.inventory:
                            if wep.name == red_name and wep.talismans == wep_tals:
                                found = True
                                text += emojize(f":bust_in_silhouette: Player inventory: {pl.name}: /hnt_{chat}")
                                break
                    if found:
                        break
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                text = "You do not own a ghostly weapon. Please die then come back to use this menu."
                self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                return False
        else:
            if caller.weapon.name.startswith(emojize(":jack-o-lantern: Hallowed")):
                red_name = caller.weapon.name[11:-2]
            else:
                red_name = caller.weapon.name[11:]
            is_pl = False
            try:
                int(args[-1][5:])
                is_pl = True
            except:
                is_pl = False
            if is_pl:
                target = args[-1][5:]

                self.server.helper.append_command("haunted", target)
                text = "Attempting to haunt. If the player does not respond, you will regain your weapon."

            else:
                target = "/"+args[-1][5:]
                self.server.helper.append_command("haunted", target)
                text = "Attempting to haunt. If no one in the party does not respond, you will regain your weapon."

            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
            return False





    def level_up(self, caller, caller_id = None):
        '''
            Função que administra o level up do player.
        '''
        if caller.level < self.server.levelcap:     # Checa se o level do player é menor que o level cap global.
            caller.exp -= caller.levels[caller.level]       # Subtrai a exp acumulada necessária para level up.
            caller.level += 1
            caller.att_points["unspent"] += 1
            if caller.level != self.server.class_change_lv:     # Checa se o player pode mudar de classe no novo level.
                text = "Hooray, you leveled up! Remember to spend your talent points with /lvlup"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
            else:

                text = "Hooray, you leveled up! You can now choose a specialization class with /lvlup"
                self.bot.send_message(text=text, chat_id=caller.chat_id)

            caller.calc_attributes()    # Atualiza os status do player.
            return False
        else:       # Se o level do player já for o level cap, então toda sua exp é resetada.
            caller.exp = 0
            caller.level = self.server.levelcap
            text = "You feel a strange force pulling all your experience out of your soul. As if someone or something took it from you"
            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
            return False

    def spend_points(self, caller, *args):
        '''
            Função que administra os pontos de atributo do player. Também muda a classe do player.
        '''
        if caller.location == "camp":       # O player só poderá gastar os pontos se estiver no camp.
            if not args:
                if caller.level >= self.server.class_change_lv and caller.classe == caller.vanilla_class:       # Checa se o player atingiu o level de mudar de classe.
                    text = "You have trained hard and learned a lot. The time has come to choose your specialization:"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.choose_class_markup)

                    return self.def_wait_time

                else:       # Se o player já tiver classe, ele poderá aumentar os atributos referentes à própria classe.
                    if caller.att_points["unspent"] > 0:
                        keyboard = self.server.keyboards.lvl_up_vanilla_reply_markup
                        if caller.classe != caller.vanilla_class:
                            keyboard = self.server.keyboards.lvl_up_class_kb
                        # if caller.classe == "Knight":
                        #     keyboard = self.server.keyboards.lvl_up_knight_reply_markup
                        # if caller.classe == "Druid":
                        #     keyboard = self.server.keyboards.lvl_up_druid_reply_markup
                        # if caller.classe == "Explorer":
                        #     keyboard = self.server.keyboards.lvl_up_explorer_reply_markup
                        # if caller.classe == "Wizard":
                        #     keyboard = self.server.keyboards.lvl_up_wizard_reply_markup

                        text = caller.lvl_up_text
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=keyboard)

                        return self.def_wait_time

                    else:
                        text = "You don't have any talent points remaining!"
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)

                        return False

            else:
                if caller.level >= self.server.class_change_lv and caller.classe == caller.vanilla_class:
                    # if caller.pt_code:
                    #     b4_c = caller.pt_code
                    #     b4_n = caller.pt_name
                    global player # R E T A R D O (Sim, esta linha é necessária caso contrário, ele buga tudo e acha q player é uma variável local [pq? n sei])
                    classed_player = player.Player(caller.chat_id)      # O player que mudar de classe, terá a sua classe objeto reescrita.

                    if args[-1] == emojize(":crossed_swords: Knight :crossed_swords:"):
                        classed_player = player.Knight(caller.chat_id)
                    elif args[-1] == emojize(":deciduous_tree: Druid :deciduous_tree:"):
                        classed_player = player.Druid(caller.chat_id)
                    elif args[-1] == emojize(":telescope: Explorer :telescope:"):
                        classed_player = player.Explorer(caller.chat_id)
                    elif args[-1] == emojize(":mage: Wizard :mage:"):
                        classed_player = player.Wizard(caller.chat_id)
                    else:
                        del self.waiting_from[caller.chat_id]["comms"][1:]      # Deleta o comando inserido caso o comando seja inválido.
                        return self.def_wait_time

                    classed_player.new_from_player(caller)

                    classed_player.att_points["unspent"] = caller.level - 1
                    # classed_player.pt_code = b4_c
                    # classed_player.pt_name = b4_n

                    caller = self.server.playersdb.players_and_parties[classed_player.chat_id]
                    if caller.referal and caller.referal in self.server.playersdb.players_and_parties:      # Se o jogador que mudou a classe foi convidado por outro jogador, o que convidou ganhará um bonus.
                        self.server.playersdb.players_and_parties[caller.referal].suc_refs += 1
                        text = f"{caller.name} just reached level 5 and is choosing a class! Here is your bonus time!"
                        self.bot.send_message(text=text,chat_id = caller.referal)


                    self.server.playersdb.players_and_parties[caller.chat_id] = classed_player      # O jogador é reescrito na datebase do DW.
                    if classed_player.pt_code:      # Se o player estava numa party, o objeto indexado pelo chat id do player é atualizado.
                        for jog in self.server.playersdb.players_and_parties[classed_player.pt_code].players:
                            if jog.chat_id == classed_player.chat_id:
                                code = classed_player.pt_code
                                self.server.playersdb.players_and_parties[classed_player.pt_code].leave_pt(jog)

                                self.server.playersdb.players_and_parties[code].join_pt(self.server.playersdb.players_and_parties[classed_player.chat_id])
                                del jog
                                break
                    old_weapon = None
                    if classed_player.weapon:
                        old_weapon = classed_player.weapon
                        self.server.playersdb.players_and_parties[caller.chat_id].weapon = None
                        old_weapon.equip(self.server.playersdb.players_and_parties[caller.chat_id])

                else:       # Se o player resolver não gastar os pontos, ele é guardado.
                    try:
                        if caller.att_points["unspent"] > 0:
                            if args[-1] in caller.att_points:
                                caller.att_points[args[-1]] += 1
                                caller.att_points["unspent"] -= 1
                            else:
                                self.bot.send_message(text = "Attribute not found", chat_id = caller.chat_id)

                    except:
                        self.server.helper.remove_command("/lvlup", caller.chat_id)
                        return False

                caller.calc_attributes()        # Atualiza os status do player
                self.show_stats(caller)         # Mostra os status do player para ele mesmo.
                return False
        else:
            text = "You need to be at camp to master new skills"
            self.bot.send_message(text = text, chat_id = caller.chat_id)
            return False


#           Party codes

    def promo(self, caller, *args):
        '''
            Comando que serve para propagandear o DW.
        '''
        text1 = f"Hey, You can forward the text below to your friends to play this game with them! If your referred players reach level 5 you will recieve a bonus 1 minute per referral to answer the blacksmith and dungeons in solo! You also gain 1% stats increase to a maximum of 100%! Also 1 extra arena per day!\n\n players invited: {caller.suc_refs}"
        self.bot.send_message(text = text1, chat_id = caller.chat_id)
        text2 = f"Dark Woods MMO\n\n A text-based MMORPG where you explore a forest where you can find extraordinary beasts and dungeons.\n\nYou can join this adventure by clicking on the link below!\n\nhttps://telegram.me/DWRPGbot?start={caller.chat_id}\n Using this link You will be granted with a starter weapon!"
        self.bot.send_message(text = text2, chat_id = caller.chat_id)

        return False


    # def party_code_generator(self):
    #     '''
    #         Função que gera um código para a criação de parties.
    #     '''
    #     code_len = 8
    #     cd = "/"
    #     while True:
    #         cd += self.helper_man.randomnamegenerator(code_len)
    #         if not cd in self.server.parties_codes:
    #             return cd
    #
    # def join_party(self, code, caller, direct_join = False):
    #     '''
    #         Método usado para colocar o player numa party.
    #
    #         Parâmetros:
    #             - code (str): código da party na qual o jogador irá entrar;
    #             - caller (class): o jogador que irá entrar numa party.
    #             - direct_join (boolean): Uma forma de se juntar a uma party é dando forward no código
    #             direto. Essa variável checa se o join dado foi direto ou não.
    #     '''
    #     if code in self.server.parties_codes:       # Checa se o código usado existe no DW, isto é, checa se a party a ser entrada existe.
    #         if not caller.is_at_forest:         # Para o jogador entrar numa party, ele precisa estar no camp.
    #             temp = "name"
    #             if not self.server.parties_codes[code]["is_at_forest"]:         # A party também precisa estar no camp.
    #                 caller.has_died = False     # Se o jogador acabou de morrer e se juntar numa party, ele não poderá se juntar numa party.
    #                 if caller.pt_code:          # Checa se o player já estava em uma party. Caso sim, todos os seus itens compartilhados serão colhidos e ele sairá da party atual.
    #                     if len(self.server.parties_codes[code]) < 18:           # Checa se a party a ser entrada está cheia.
    #                         s = "You just lost your equipped weapon because owner left party."
    #                         self.scoop(caller, s)
    #
    #                         del self.server.parties_codes[caller.pt_code][caller.chat_id]       # Deleta o jogador da party antiga.
    #                         old_pt_name = caller.pt_name
    #                         self.server.parties_codes[code][caller.chat_id] = caller        # Insere o jogador na party nova.
    #                         caller.pt_code = code
    #                         caller.pt_name = self.server.parties_codes[code][temp]
    #
    #                         text = f"You just left {old_pt_name} to join {self.server.parties_codes[code][temp]}!"
    #                         for chat_id,jogador in self.server.parties_codes[code].items():
    #                             if isinstance(jogador, player.Player):
    #                                 if chat_id == caller.chat_id:
    #                                     self.bot.send_message(text = text, chat_id = chat_id)
    #                                 else:
    #                                     self.bot.send_message(text = f"{caller.name} just entered {self.server.parties_codes[code][temp]}", chat_id = chat_id)
    #
    #                     else:
    #                         text = "Party is full, aborting"
    #                         self.bot.send_message(text = text, chat_id = chat_id)
    #
    #                 else:
    #                     if len(self.server.parties_codes[code]) < 18:
    #                         self.server.parties_codes[code][caller.chat_id] = caller
    #                         pt_name = self.server.parties_codes[code][temp]
    #                         caller.pt_code = code
    #                         caller.pt_name = self.server.parties_codes[code][temp]
    #                         for chat_id,jogador in self.server.parties_codes[code].items():
    #                             if isinstance(jogador, player.Player):
    #                                 if chat_id == caller.chat_id:
    #                                     text = f"Congratulations, you just joined {pt_name}"
    #                                     self.bot.send_message(text = text, chat_id = caller.chat_id)
    #                                 else:
    #                                     self.bot.send_message(text = f"{caller.name} just entered {self.server.parties_codes[code][temp]}", chat_id = chat_id)
    #
    #                     else:
    #                         text = "Party is full, aborting"
    #                         self.bot.send_message(text = text, chat_id = caller.chat_id)
    #             else:
    #                 # text = f"{self.server.parties_codes[code][temp]} is currently at the forest, this party need to be at camp for it to be joinable!"
    #                 text = f"The {self.server.parties_codes[code][temp]} are currently out exploring the forest. The party must be at camp for you to join them!"
    #                 self.bot.send_message(text = text, chat_id = caller.chat_id)
    #         else:
    #             text = "You need to be at camp to create or join a party"
    #             self.bot.send_message(text = text, chat_id = caller.chat_id)
    #         return True             # Um True é retornado aqui, para indicar que o código inserido é válido. Usado no MessageMan para o caso de join direto.
    #     elif not direct_join:       # Esta linha é pulada em caso de join direto, para que o bot não responda toda hora que o jogador insere comandos inválidos.
    #         text = f"Party code {code} not found!"
    #         self.bot.send_message(text = text, chat_id = caller.chat_id)
    #     return False
    #
    #
    # def new_party(self, caller, name, codigo):
    #     '''
    #         Função que cria uma nova party.
    #
    #         Por algum motivo, as parties são dicionários, com os player e atributos misturados.
    #
    #         Parâmetros:
    #             - caller (class): player que irá criar uma nova party;
    #             - name (str): nome da party;
    #             - codigo (str): código da party (utilizado para outros jogadores poder entrar).
    #     '''
    #     if not caller.is_at_forest:     # Para criar uma party é necessário que o player esteja no camp.
    #         if caller.pt_code:      # Checa se o player está numa party.
    #             self.leave_party_comm(caller, "yes")
    #         caller.has_died = False
    #         new_dic = {}
    #         new_dic["name"] = name      # Nome da party.
    #         new_dic["code"] = codigo    # Código da party.
    #         new_dic["is_at_forest"] = False     # Variável que indica se a party está na floresta.
    #         new_dic["active"] = False       # Variável que indica se a party está ativa no jogo.
    #         new_dic["entered_dg"] = False   # Variável que indica se a party está numa dungeon.
    #         new_dic["time_to_next_encounter"] = 0       # Variável que indica o tempo de próximo encontro.
    #         new_dic["time_to_leave"] = 0    # Tempo restante para a volta da party para o camp.
    #         new_dic["stay_time"] = 0        # Quanto tempo a party ficará na floresta.
    #         new_dic["is_travelling"] = False        # Variável que indica se a party está viajando para algum lugar através de um mapa, ou do explorer.
    #         new_dic["travel_time"] = 0      # Tempo de chegada para a localização que a party está viajando.
    #         new_dic["travelling_loc"] = ""  # A localização de chegada da viagem (ex: dungeon, blacksmith, world boss, etc).
    #         new_dic["pt_inv"] = []          # Inventário da party.
    #         new_dic["location"] = "camp"    # Localização atual da party.
    #         new_dic[caller.chat_id] = caller        # A party começa com o player que a criou.
    #         caller.pt_code = codigo         # Indica o código da party na qual o player faz parte.
    #         caller.pt_name = name           # Indica o nome da party na qual o player faz parte.
    #         self.bot.send_message(text = f"You have founded the {name}!\n Share the following code to recruit new member:", chat_id  = caller.chat_id)
    #         self.bot.send_message(text = codigo, chat_id = caller.chat_id)
    #         return new_dic
    #
    #     else:
    #         text = "You need to be at camp to create or join a party"
    #         self.bot.send_message(text = text, chat_id = caller.chat_id)
    #
    # def print_pt_inv(self, caller):
    #     '''
    #         Mostra o inventário da party. Retorna um string.
    #     '''
    #     s = ""
    #     for i in self.server.parties_codes[caller.pt_code]["pt_inv"]:       # Printa o inventário.
    #         s += emojize(f"*{i.name}* :crossed_swords:{i.atributos[0]} :shield:{i.atributos[1]} /e_{i.code}\n")
    #     if s == "":
    #         s = "The party inventory is empty"
    #
    #     else:
    #         s += "\nBorrow a weapon using the '/e_' codes above. To add an item to the shared invetory, /inv then /s_(code). /scoop to scoop all items owned by you. /distribute will evenly distribute the item stats amongst members."
    #         s = s.replace("_", "\\_")
    #     return s
    #
    # def print_pt(self, caller):
    #     '''
    #         Exibe os status da party, seus jogadores e seu inventário.
    #     '''
    #     grupo = self.server.parties_codes[caller.pt_code]
    #     temp1 = "name"
    #     temp2 = "code"
    #     text = emojize(f":party_popper: *Party members* from {grupo[temp1]}, {grupo[temp2]}: \n\n")
    #     tt_hp = 0
    #     txt2 = ""
    #     for chat_id,jogador in self.server.parties_codes[caller.pt_code].items():       # Printa os jogadores e seus status.
    #         if isinstance(jogador, player.Player):
    #             # jogador = self.server.playersdb.players[chat_id]
    #             emoji = ":green_heart:"
    #             j_hp = 0
    #             for limb in jogador.hp:
    #                 j_hp += limb.health
    #             if j_hp < 5:
    #                 emoji = ":yellow_heart:"
    #             if j_hp < 2:
    #                 emoji = ":red_heart:"
    #             txt2 += emojize(f"{jogador.name}, {jogador.chat_id}:\nHealth: {j_hp}{emoji} {jogador.classe}\n")
    #             txt2 += f"*Buff*: {jogador.buff_man.states_list[jogador.buff_man.buff_state]}\n"
    #             txt2 += emojize(f"*Stats*: {jogador.atk} :crossed_swords: {jogador.defense} :shield:\n\n")
    #             tt_hp += j_hp
    #     txt2 = txt2.replace("_", "\\_")
    #     text = text + txt2
    #     text += f"*Total health*: {tt_hp} \n"
    #
    #     text += f"Check shared inventory: /ptinv\n\n"
    #
    #
    #     return text
    #
    # def party(self, caller, *args):
    #     '''
    #         Esta função é basicamente um party_comms.py. Ela possui a maioria dos comandos possíveis para o jogador numa party.
    #         Segue a lista de comandos gerenciado por este método:
    #             - /party: printa os comandos de party e/ou aciona o "print_pt". Este é o primeiro comando da árvore de comandos. Todo o resto é secundário;
    #             - /join: entra numa party;
    #             - /create: cria uma party;
    #             - /leave: sai de uma party;
    #             - /shout: manda uma mensagem para todos os membros da party;
    #             - /scoop: coleta todos itens compartilhados pelo jogador;
    #             - /ptname: troca o nome da party;
    #             - /distribute: distribui todos os itens do inventário da party, que não possuem dono.
    #             - código do item a ser equipado: equipa o item cujo código está no inventário da party.
    #     '''
    #     if not args:        # Se não tiver args, o comando inserido é um /party.
    #         #if not caller.chat_id.startswith("-"):
    #             text = "Do you want to /join a party ,/create one or /leave your current party?\n  to join use /join (party\_code) like: /join /hujiugui\n to create, use /create (name) like: /create the company of the chicken axe. /shout (message) to send a message to members. /ptname (name) to change party name.\n\n"
    #             if caller.pt_code:
    #                 text += self.print_pt(caller)       # Printará a party se o jogador estiver em uma.
    #             self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode = 'MARKDOWN')
    #             # return self.def_wait_time
    #             return False
    #         #else:
    #             text = "You are some sort of alt. Would be unfair if you could join parties..."
    #             self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode = 'MARKDOWN')
    #             return False
    #     else:
    #         treco = args[-1]
    #
    #         if treco[:5] == "/join":
    #             codigo = treco[6:]
    #             self.join_party(codigo, caller)
    #             return False
    #         elif treco[:7] == "/create":
    #             cod = self.party_code_generator()
    #             pt_name = treco[8:]
    #             if not pt_name:
    #                 pt_name = "Nameless party"
    #             self.server.parties_codes[cod] = self.new_party(caller, pt_name, cod)
    #             return False
    #         elif treco == "/leave":         # A complicação de sair da party é recolher todos os itens do jogador do inventário da party. Basicamente, o player dá um /scoop antes de sair. Veja /scoop e "join_party".
    #             self.leave_party_comm(caller, "yes")
    #
    #         elif treco[:6] == "/shout":
    #             if caller.pt_code:
    #                 for chat_id,jogador in self.server.parties_codes[caller.pt_code].items():
    #                     if isinstance(jogador, player.Player):
    #                         text = f"{caller.name} said: {treco[7:]}"
    #                         self.bot.send_message(text = text, chat_id = chat_id)
    #             else:
    #                 self.bot.send_message(text=f"You shouted {treco[7:]} but nothing happened.", chat_id=caller.chat_id)
    #
    #         elif treco[:7] == "/ptname":
    #             if caller.pt_code:
    #                 self.server.parties_codes[caller.pt_code]["name"] = treco[8:]
    #                 for chat_id,jogador in self.server.parties_codes[caller.pt_code].items():
    #                     if isinstance(jogador, player.Player):
    #                         jogador.pt_name = treco[8:]
    #                         text = f"{caller.name} changed the party name to: {treco[8:]}"
    #                         self.bot.send_message(text = text, chat_id = chat_id)
    #             else:
    #                 text = "You do not belong to party."
    #                 self.bot.send_message(text=text,chat_id = caller.chat_id)
    #
    #         elif treco == "/scoop":         # Recolhe os itens compartilhados do jogador. O código é o mesmo que em join_party.
    #             self.bot.send_message(text="You claimed items owned by you.", chat_id = caller.chat_id)
    #             s = "You just lost your equipped weapon because owner have taken it from you."
    #             self.scoop(caller, s)
    #
    #         elif treco == "a":
    #             pass
    #
    #         elif treco == "/distribute":
    #             self.distribute(caller)
    #
    #         else:       # Se o comando inserido não é nenhum dos anteriores, então o player está equipando um item.
    #             text = ""
    #             in_use = False      # Checaremos se o item está em uso ou não.
    #             for item in self.server.parties_codes[caller.pt_code]["pt_inv"]:
    #                 if f"/e_{item.code}" == treco:
    #                     if isinstance(item, items.dg_map):      # Marca se o item é um mapa.
    #                         is_map = True
    #                     else:
    #                         is_map = False
    #
    #                     if not is_map and item.is_shared_and_equipped:
    #                         in_use = True
    #
    #                     else:
    #                         if not is_map and not item.owner:       # Se o item não for um mapa e não tiver dono, o novo dono da arma será o player que irá equipá-la.
    #                             item.owner = caller.chat_id
    #                             text = emojize(f"You claimed {item.name}!\n")
    #                         if caller.weapon and caller.weapon.is_shared_and_equipped:      # Para um item ser equipado, o atual deve ser desequipado. O problema é que o item pode voltar para o inv da party com o mesmo código de outra.
    #                             caller.weapon.is_shared_and_equipped = False
    #                             index = 0
    #                             for item2 in self.server.parties_codes[caller.pt_code]["pt_inv"]:       # Então, iremos adicionar mais índices ao item para diferenciá-lo de outro item de mesmo código.
    #
    #                                 if caller.weapon.code == item2.code:
    #                                     break
    #                                 index += 1
    #                             self.server.parties_codes[caller.pt_code]["pt_inv"][index].is_shared_and_equipped = False
    #
    #                             # self.server.parties_codes[caller.pt_code]["pt_inv"]
    #                         if is_map:
    #                             item.action(self.server.parties_codes[caller.pt_code])      # Usa o mapa.
    #                         else:
    #                             item.is_shared_and_equipped = True
    #                             item.action(caller)         # Equipa o item.
    #                             caller.calc_attributes()
    #                             text += emojize(f"Succesfully borrowed {item.name}!")
    #                             in_use = False
    #
    #                         break
    #             if in_use:
    #                 text += "This weapon is already in use by other party member."
    #             if text:
    #                 self.bot.send_message(text = text, chat_id = caller.chat_id)
    #             return self.def_wait_time
    #
    # def pt_inv(self, caller, *args):
    #     if caller.pt_code:
    #         if args:
    #             treco = args[-1]
    #             if treco == "/distribute":
    #                 self.distribute(caller)
    #
    #             elif treco == "/scoop":         # Recolhe os itens compartilhados do jogador. O código é o mesmo que em join_party.
    #                 self.bot.send_message(text="You claimed items owned by you.", chat_id = caller.chat_id)
    #                 s = "You just lost your equipped weapon because owner have taken it from you."
    #                 self.scoop(caller, s)
    #
    #             else:       # Se o comando inserido não é nenhum dos anteriores, então o player está equipando um item.
    #                 try:
    #                     self.join_party(treco, caller, direct_join = True)
    #                     return self.def_wait_time
    #                 except:
    #                     pass
    #                 text = ""
    #                 in_use = False      # Checaremos se o item está em uso ou não.
    #                 for item in self.server.parties_codes[caller.pt_code]["pt_inv"]:
    #                     if f"/e_{item.code}" == treco:
    #                         if isinstance(item, items.dg_map):      # Marca se o item é um mapa.
    #                             is_map = True
    #                         else:
    #                             is_map = False
    #
    #                         if not is_map and item.is_shared_and_equipped:
    #                             in_use = True
    #
    #                         else:
    #                             if not is_map and not item.owner:       # Se o item não for um mapa e não tiver dono, o novo dono da arma será o player que irá equipá-la.
    #                                 item.owner = caller.chat_id
    #                                 text = emojize(f"You claimed {item.name}!\n")
    #                             if caller.weapon and caller.weapon.is_shared_and_equipped:      # Para um item ser equipado, o atual deve ser desequipado. O problema é que o item pode voltar para o inv da party com o mesmo código de outra.
    #                                 caller.weapon.is_shared_and_equipped = False
    #                                 index = 0
    #                                 for item2 in self.server.parties_codes[caller.pt_code]["pt_inv"]:       # Então, iremos adicionar mais índices ao item para diferenciá-lo de outro item de mesmo código.
    #
    #                                     if caller.weapon.code == item2.code:
    #                                         break
    #                                     index += 1
    #                                 self.server.parties_codes[caller.pt_code]["pt_inv"][index].is_shared_and_equipped = False
    #
    #                                 # self.server.parties_codes[caller.pt_code]["pt_inv"]
    #                             if is_map:
    #                                 item.action(self.server.parties_codes[caller.pt_code])      # Usa o mapa.
    #                             else:
    #                                 item.is_shared_and_equipped = True
    #                                 item.action(caller)         # Equipa o item.
    #                                 caller.calc_attributes()
    #                                 text += emojize(f"Succesfully borrowed {item.name}!")
    #                                 in_use = False
    #
    #                             break
    #                 if in_use:
    #                     text += "This weapon is already in use by other party member."
    #                 if text:
    #                     self.bot.send_message(text = text, chat_id = caller.chat_id)
    #                 return self.def_wait_time
    #         else:
    #             text = self.print_pt_inv(caller)
    #             self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode='MARKDOWN')
    #             return self.def_wait_time
    #     else:
    #         text = "You do not belong to party to look at its shared inventory, create a party first with /party, then /create (name)"
    #         self.bot.send_message(text = text, chat_id = caller.chat_id, parse_mode='MARKDOWN')
    #         return False
    #
    # def scoop(self, caller, text):
    #     done = False
    #     if len(self.server.parties_codes[caller.pt_code]["pt_inv"]):        # Nas linhas abaixo, os itens do jogador serão colhidos.
    #         while not done:
    #             if len(self.server.parties_codes[caller.pt_code]["pt_inv"]) == 0:           # Checa se o inv da party não é vazio.
    #                 done = True
    #             for i in range(len(self.server.parties_codes[caller.pt_code]["pt_inv"])):   # Percorre todos os itens da party.
    #                 item = self.server.parties_codes[caller.pt_code]["pt_inv"][i]
    #                 if item.owner == caller.chat_id:            # Checa se o dono do item é o player que irá sair da party.
    #
    #                     if item.is_shared_and_equipped:         # Checa se o item está equipado por um outro player da party.
    #                         for chat,jog in self.server.parties_codes[caller.pt_code].items():      # Procura o jogador que está com o item equipado.
    #                             if isinstance(jog,player.Player):
    #                                 if jog.weapon and jog.weapon.code == item.code:
    #                                     jog.weapon = None                                           # Desequipa o item do player que o estava usando.
    #                                     # item.is_shared_and_equipped = False
    #                                     jog.calc_attributes()                                       # Atualiza os status do jogador que perdeu o item equipado.
    #                                     self.bot.send_message(text = text, chat_id = jog.chat_id)
    #                                     break
    #                         item.is_shared_and_equipped = False
    #                     number = 0
    #                     for arma in caller.inventory:
    #
    #                         if arma.ac_code == item.ac_code:
    #                             number += 1
    #                     if number == 0:
    #                         number = ""
    #                     item.ac_code = item.code + f"{number}"
    #                     item.ac_code = item.code + f"{number}"
    #                     temp_ac = item.ac_code
    #                     item.ac_code = item.code
    #                     item.code = temp_ac
    #                     caller.inventory.append(copy.deepcopy(item))                    # Cria uma cópia verdadeira do item para o inv do caller.
    #                     del self.server.parties_codes[caller.pt_code]["pt_inv"][i]      # Deleta o item do inv da party.
    #                     break
    #                 if i == len(self.server.parties_codes[caller.pt_code]["pt_inv"])-1:  # Checa se percorremos todos os itens da party.
    #                     done = True
    #
    # def distribute(self, caller):
    #     att = {}
    #     better_list = {}
    #     for chat,jog in self.server.parties_codes[caller.pt_code].items():
    #         if isinstance(jog, player.Player):
    #             att[chat] = 0
    #     for item in self.server.parties_codes[caller.pt_code]["pt_inv"]:
    #         if not isinstance(item, items.dg_map) and not item.owner:
    #             stats = item.atributos[0]+item.atributos[1]
    #             better_list[item.code] = [stats,item]
    #
    #     # for stats,item in better_list.items():
    #     #     print(stats)
    #
    #     for codes,tup in sorted(better_list.items(), key=lambda item: item[1][0], reverse = True):
    #             stats = tup[0]
    #             # stats = item.atributos[0]+item.atributos[1]
    #             chos,vel = caller.chat_id,att[caller.chat_id]
    #             for chat,val in att.items():
    #                 if val<=vel:
    #                     vel = val
    #                     chos = chat
    #
    #
    #
    #
    #             att[chos] += stats
    #             tup[1].owner = chos
    #     text = emojize(f"*Stats claimed*:\n\n")
    #     s = "You just lost your equipped weapon because owner have taken it from you."
    #     for chat, val in att.items():
    #         text += emojize(f"*{self.server.playersdb.players[chat].name}* owned :crossed_swords:️:shield: *{val}* total stats!\n")
    #
    #     for chat,jog in self.server.parties_codes[caller.pt_code].items():
    #         if isinstance(jog, player.Player):
    #             self.bot.send_message(text = text, chat_id = chat, parse_mode = "MARKDOWN")
    #             self.scoop(jog, s)
    #
    # def create_party_comm(self, caller, *args):
    #     if caller.is_at_forest == True:
    #         text = "You need to be at camp to create or join a party"
    #         self.bot.send_message(text = text, chat_id = caller.chat_id)
    #         return False
    #
    #     pt_name = self.server.messages[caller.chat_id][-1][8:]
    #     if not pt_name and not args:
    #         text = "Type a name for your party."
    #         self.bot.send_message(text = text, chat_id = caller.chat_id)
    #         return self.def_wait_time
    #
    #     if args:
    #         if args[-1] == "":
    #             pt_name = "Nameless party"
    #         else:
    #             pt_name = args[-1]
    #     cod = self.party_code_generator()
    #     self.server.parties_codes[cod] = self.new_party(caller, pt_name, cod)
    #
    #     return False
    #
    # def join_party_comm(self, caller, *args):
    #     '''
    #         Esta função é o comando do player para ingressar numa party.
    #
    #         Parâmetros:
    #         caller (class): player que entrará numa party;
    #         args (tuple): argumento que conterá o código da party.
    #     '''
    #     if not args:
    #         text = "Forward here or type the party's code you want to join"
    #         self.bot.send_message(text = text, chat_id = caller.chat_id)
    #         return self.def_wait_time
    #
    #     else:
    #         code = args[-1]
    #         self.join_party(code, caller)
    #     return False
    #
    # def leave_party_comm(self, caller, *args):
    #     if caller.pt_code:
    #         if not self.server.parties_codes[caller.pt_code]["is_at_forest"]:
    #             if not args:
    #                 text = "Do you want to leave current party?"
    #                 self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.forest_return_reply_markup)
    #                 return self.def_wait_time
    #
    #             elif args[-1] == "yes":
    #                 s = "You just lost your equipped weapon because owner left party."
    #                 temp = "name"
    #                 self.scoop(caller, s)
    #                 if caller.weapon:
    #                     if caller.weapon.is_shared_and_equipped:
    #                         caller.weapon.is_shared_and_equipped = False
    #                         caller.weapon = None
    #
    #                 for chat_id,jogador in self.server.parties_codes[caller.pt_code].items():
    #                     if isinstance(jogador, player.Player):
    #                         if chat_id == caller.chat_id:
    #                             #text = f"You just left {self.server.parties_codes[caller.pt_code][temp]}"
    #                             text = emojize(f"Your teammates from {self.server.parties_codes[caller.pt_code][temp]} wave goodbye as you go your separate ways. Everyone will miss you :frowning_face:")
    #                             self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.class_main_menu_reply_markup)
    #                         else:
    #                             text = f"{caller.name} just left {self.server.parties_codes[caller.pt_code][temp]}"
    #                             self.bot.send_message(text = text, chat_id = chat_id)
    #                 if caller.chat_id in self.server.parties_codes[caller.pt_code]:
    #                     del self.server.parties_codes[caller.pt_code][caller.chat_id]
    #                 if len(self.server.parties_codes[caller.pt_code]) < 14:
    #                     del self.server.parties_codes[caller.pt_code]
    #                 caller.pt_code = ""
    #                 caller.pt_name = ""
    #
    #             else:
    #                 text = f"You decided to stay in your party."
    #                 self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.server.keyboards.class_main_menu_reply_markup)
    #
    #         else:
    #             text = f"You need to be at camp to leave parties!"
    #             self.bot.send_message(text = text, chat_id = caller.chat_id)
    #
    #     else:
    #         text = f"You do not belong to a party yet! try /join or /create first!"
    #         self.bot.send_message(text = text, chat_id = caller.chat_id)
    #     return False
    #
    # def shout_comm(self, caller, *args):
    #     message = self.server.messages[caller.chat_id][-1][7:]
    #     if caller.pt_code:
    #         for chat_id, jogador in self.server.parties_codes[caller.pt_code].items():
    #             if isinstance(jogador, player.Player):
    #                 text = f"{caller.name} said: {message}"
    #                 self.bot.send_message(text = text, chat_id = chat_id)
    #     else:
    #         self.bot.send_message(text=f"You shouted but nothing happened.", chat_id=caller.chat_id)
    #     return False
    #
    # def pt_name_comm(self, caller, *args):
    #     if caller.pt_code:
    #         if not args:
    #             text = "Type the new party name."
    #             self.bot.send_message(text = text, chat_id = caller.chat_id)
    #             return self.def_wait_time
    #         else:
    #             pt_name = args[-1]
    #             self.server.parties_codes[caller.pt_code]["name"] = pt_name
    #             for chat_id,jogador in self.server.parties_codes[caller.pt_code].items():
    #                 if isinstance(jogador, player.Player):
    #                     jogador.pt_name = pt_name
    #                     text = f"{caller.name} changed the party name to: {pt_name}"
    #                     self.bot.send_message(text = text, chat_id = chat_id)
    #     else:
    #         text = "You do not belong to party."
    #         self.bot.send_message(text=text,chat_id = caller.chat_id)
    #     return False

    def to(self, caller):
        pass
