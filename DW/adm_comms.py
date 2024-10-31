#########################################
# Classe que contém os comandos de ADM  #
#########################################

from emoji import emojize
import copy
import bot
import player
import player_comms
import forest_comms
import party_comms
import WB_comms
import items
import death
import deep_items
import wb_battle_simulator


class ADMComms:
    '''
        Lista de comandos que podem ser usados pelos adms pra adm o jogo.

        Existem vários níveis de adm.

    '''
    def __init__(self, server):
        self.server = server
        self.defkb = server.defkb
        self.def_wait_time = 60
        self.bot = bot.TGBot()
        self.playerComs = player_comms.PlayerComms(server)
        self.forestComs = forest_comms.ForestCommms(server)     # Ele carrega os comandos pra poder fazer coisas com os jogadores
        self.WBComms = WB_comms.WBComms(server)
        self.PartyComs = party_comms.PartyComms(server)
        self.Talismandb = deep_items.Talismandb()
        self.actions = {
            "/sd": self.shutdown,
            "/save": self.save_all,
            "/adm_inv": self.adm_show_inv,
            "/adm_st": self.adm_show_stats,
            "/adm_equip_wep_st": self.adm_show_equipped_weapon_stats,
            "/adm_hp": self.adm_show_health,
            "/adm_bst": self.adm_show_pokedex,
            "/adm_gm": self.make_gm,
            "/adm_gw": self.give_weapon,
            "/adm_forest": self.adm_forest,
            "/adm_adm": self.make_adm,
            "/adm_kill": self.kill,
            "/adm_lvlup": self.force_lvlup,
            "/adm_lv5": self.force_lvl5,
            "/adm_rsp": self.respec,
            "/adm_del": self.del_player,
            "/adm_dummy": self.new_dummy,
            "/adm_pls": self.print_players,
            "/adm_zeus": self.zeus,
            "/adm_blessing": self.adm_blessing,
            "/adm_rename_player": self.adm_rename,
            "/adm_buff": self.adm_buff,
            "/adm_heal": self.adm_heal,
            "/adm_proc_f": self.activate_forest,
            "/adm_find_player": self.player_name_finder,
            "/adm_list_gr_alts_in_pt": self.hmmmmmmmmmmm,
            "/adm_clear_wating_from": self.clear_comms,
            "/adm_remove_all": self.remove_all_from_forest,
            "/adm_sunflower": self.remove_from_sf,
            "/adm_send_global_message": self.send_message_to_all_players,
            "/adm_activate_player": self.activate_player,
            "/adm_give_arena": self.give_items,
            "/adm_infinite_arenas": self.inf_arena,
            "/adm_zero_rank": self.sefodeu,
            "/adm_multiple_party_players": self.mpp,
            "/adm_solve_multiple_party_players": self.smpp,
            "/adm_tier3": self.tier3,
            "/adm_solve_referrals": self.shit,
            "/adm_next_level": self.deep_delver,
            "/adm_back_level": self.deep_delver2,
            "/adm_encounter_f": self.force_encounter,
            "/adm_encounter_df": self.force_deep_encounter,
            "/adm_give_all_talismans": self.give_all_possibles_talismans,
            "/adm_give_talisman": self.give_a_talisman,
            "/adm_give_af": self.over_weight,
            "/adm_update_stats": self.up_all_stats,
            "/adm_d_inv": self.del_inv,
            "/adm_give_leaves": self.give_leaves,
            "/adm_give_lots_of_leaves": self.give_a_forest,
            "/adm_show_adm_list": self.adm_show_adm_list,
            "/adm_clear_probe": self.adm_clear_probe,
            "/adm_check_probe_info": self.adm_check_probe_info,
            "/adm_add_patreon": self.adm_add_patreon,
            "/adm_remove_patreon": self.adm_remove_patreon,
            "/adm_pay_patreon": self.adm_pay_patreon,
            "/adm_check_patreon": self.adm_check_patreon,
            "/adm_simulate": self.adm_simulate_battle,
            "/adm_WB_phase_2": self.adm_wb_phase2,
            "/adm_give_stat_coins": self.adm_give_stat_coins,
            "/adm_reset_wb": self.adm_reset_wb,
            "/adm_move_account": self.adm_move_acc,
            "/adm_fix_stuck_players": self.adm_fix_stuck_players,

        }
        self.internal = {}
        self.death = death.Death(self.server)
        self.commands_dict = {}     # Se um comando tiver iterações, colocar os parâmetros a ser sarvos neste dicionário organizados
                                    # pelo chat_id do adm. Exemplo: self.commands_dict[caller.chat_id]["Parâmetro a ser salvo"] = parâmetro

    def f_return(self, user):
        if user.pt_code:
            if user.pt_code in self.server.playersdb.players_and_parties:
                self.server.playersdb.players_and_parties[user.pt_code].leave_pt(user)
        if user.chat_id in self.server.deep_forest_manager.jogs:
            if user.location == "megabeast":
                if user.chat_id in self.server.megadb.players:
                    self.server.megadb.remove_user(user.chat_id)
            if user.chat_id in self.server.deep_forest_manager.jogs:
                self.server.deep_forest_manager.leave(user.chat_id)
            else:
                self.server.woods.add_to_woods(user, 60*60)
            user.calc_attributes()

        if user.chat_id in self.server.woods.players:
            self.server.woods.exit_woods(user.chat_id)

        if user.location != "camp":
            print(user.location)
            user.location = "camp"

    def adm_move_acc(self, caller, *args):
        if caller.admlevel > 4:

            if not args:
                self.commands_dict[caller.chat_id] = {}
                text = "Please enter the chat_id of the player to be tranferred"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                if args[-1] in self.server.playersdb.players_and_parties and not "transfer from" in self.commands_dict[caller.chat_id]:
                    self.commands_dict[caller.chat_id]["transfer from"] = args[-1]
                    text = "Please enter the chat_id of the destiny player."
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    return self.def_wait_time
                elif args[-1] in self.server.playersdb.players_and_parties and "transfer from" in self.commands_dict[caller.chat_id]:
                    text = f"Transfering account from {self.server.playersdb.players_and_parties[self.commands_dict[caller.chat_id]['transfer from']]} to {self.server.playersdb.players_and_parties[args[-1]]}"
                    self.f_return(self.server.playersdb.players_and_parties[args[-1]])
                    self.f_return(self.server.playersdb.players_and_parties[self.commands_dict[caller.chat_id]["transfer from"]])
                    self.server.playersdb.players_and_parties[args[-1]] = copy.copy(self.server.playersdb.players_and_parties[self.commands_dict[caller.chat_id]["transfer from"]])
                    self.server.playersdb.players_and_parties[args[-1]].chat_id = args[-1]
                    self.server.playersdb.players_and_parties[args[-1]].code = args[-1]
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    text = f"Your account has been transferred from {self.commands_dict[caller.chat_id]['transfer from']} ({self.server.playersdb.players_and_parties[self.commands_dict[caller.chat_id]['transfer from']]}) to this succesfully!"
                    self.bot.send_message(text=text, chat_id=args[-1])
                    return False
                else:
                    text = "Chat id not found"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    return False

        return False

    def adm_reset_wb(self, caller, *args):
        if caller.admlevel > 9:
            for chat,pl in self.server.playersdb.players_and_parties.items():
                pl.attacked_the_wb = False
            text = "Sucessfully set the 'attacked_the_wb' of all players to False."
            self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def adm_give_stat_coins(self, caller, *args):
        '''
            Da uma arma pro jogador alvo
        '''
        if caller.admlevel > 4:
            if not args:
                self.commands_dict[caller.chat_id] = {}
                self.commands_dict[caller.chat_id]["adm_gw_id"] = ""
                self.commands_dict[caller.chat_id]["adm_gw_stage"] = 0
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                if not self.commands_dict[caller.chat_id]["adm_gw_stage"]:
                    self.commands_dict[caller.chat_id]["adm_gw_stage"] += 1
                    if args[-1] in self.server.playersdb.players_and_parties:
                        self.commands_dict[caller.chat_id]["adm_gw_id"] = args[-1]
                        text = "Please send how much stat coins are going to be given to that player."
                        self.bot.send_message(text=text, chat_id=caller.chat_id)
                        return self.def_wait_time
                    else:
                        text = "Chat id not found. Aborting."
                        self.bot.send_message(text=text, chat_id=caller.chat_id)
                        return False
                else:
                    number = int(args[-1])
                    text = f"Sucessfully given {number} leaves to {self.server.playersdb.players_and_parties[self.commands_dict[caller.chat_id]['adm_gw_id']]}."
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    text = f"You've recieved {number} leaves from mod {caller}."
                    self.bot.send_message(text=text, chat_id=self.commands_dict[caller.chat_id]["adm_gw_id"])
                    self.server.playersdb.players_and_parties[self.commands_dict[caller.chat_id]["adm_gw_id"]].stat_points += number
                    return False

    def adm_wb_phase2(self, caller, *args):
        if caller.admlevel > 9:
            self.server.World_boss.max_recovery_rate = 5e6
            text = "Helianth is now at phase 2"
            self.server.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def adm_simulate_battle(self, caller, *args):
        if caller.admlevel > 9:
            wb_battle_simulator.generate_graph(self.server)
            self.bot.send_photo(chat_id=caller.chat_id, photo=open('tests/test.png', 'rb'))
        return False

    def adm_add_patreon(self, caller, *args):
        if caller.admlevel > 9:
            if not args:
                self.commands_dict[caller.chat_id] = {}
                self.commands_dict[caller.chat_id]["user_id"] = ""
                text = "Please enter the chat id of the user."
                self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time*2
            else:
                # if args[-1] in self.server.backers.patreon_backers:
                #     del self.server.backers.patreon_backers[args[-1]]
                if args[-1] in self.server.playersdb.players_and_parties:
                    if not self.commands_dict[caller.chat_id]["user_id"]:
                        self.commands_dict[caller.chat_id]["user_id"] = args[-1]
                        text = "Please type the value of leaves he would recieve."
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                        return self.def_wait_time*2

                else:
                    if self.commands_dict[caller.chat_id]["user_id"]:
                        print("oi")
                        self.server.backers.add_patreon(self.commands_dict[caller.chat_id]["user_id"], int(args[-1]))
                        text = f"You have sucessfully joined the official Clini Studios backers! Thanks a lot! Every start of the month you will receive {args[-1]} leaves!"
                        self.server.bot.send_message(text=text, chat_id=self.commands_dict[caller.chat_id]["user_id"])
                        text = f"Sucessfully added {self.commands_dict[caller.chat_id]['user_id']} to patreons."
                        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def adm_remove_patreon(self, caller, *args):
        if caller.admlevel > 9:
            if not args:
                text = "Please type the chat id that you want to remove from the patreons."
                self.server.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time*2
            else:
                if args[-1] in self.server.backers.patreon_backers:
                    self.server.backers.remove_patreon(args[-1])
                    text = f"Sucessfully removed {args[-1]} from the patreons list."
        return False

    def adm_pay_patreon(self, caller, *args):
        if caller.admlevel > 9:
            for user_id, value in self.server.backers.patreon_backers.items():
                self.server.playersdb.players_and_parties[user_id].leaves += value
                text = f"Thanks for being a Patreon! Here is your monthly {value} leaves!"
                self.server.bot.send_message(text=text, chat_id=user_id)
        text = "Users paid sucessfully."
        self.server.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def adm_check_patreon(self, caller, *args):
        if caller.admlevel > 9:
            text = "Patreons Backers registred:\n\n"
            for user_id, value in self.server.backers.patreon_backers.items():
                text += f"({user_id}): {self.server.playersdb.players_and_parties[user_id]}: {value}\n\n"
            self.server.bot.send_message(text=text, chat_id=caller.chat_id)
        return False


    def adm_check_probe_info(self, caller, *args):
        if caller.admlevel > 0:
            if not args:
                text = "Please type the chat id of the player or the party code of the party you want to see the probe info."
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                if args[-1] in self.server.playersdb.players_and_parties:

                    if args[-1][0] == "/":
                        pt = self.server.playersdb.players_and_parties[args[-1]]
                        text = f"Here is the probe info for {pt.name}:\n\n"
                        text += f"average_time_between_dungeons_pt: {round(pt.average_time_between_dungeons_pt)} s\n"
                        text += f"average_time_between_last_5_dungeons_pt: {round(pt.average_time_between_last_dungeons_pt)} s\n"
                        text += f"number of probes: {len(pt.average_times_taken_pt)}\n"
                        text += f"probes: {pt.average_times_taken_pt}\n"
                        text += f"average_time_between_WB_pt: {round(pt.average_time_between_WB_pt)} s\n"

                    else:
                        pt = self.server.playersdb.players_and_parties[args[-1]]
                        text = f"Here is the probe info for {pt.name}:\n\n"
                        text += f"average_time_between_dungeons: {round(pt.average_time_between_dungeons)} s\n"
                        text += f"average_time_between_last_5_dungeons: {round(pt.average_time_between_last_dungeons)} s\n"
                        text += f"number of probes: {len(pt.average_times_taken)}\n"
                        text += f"probes: {pt.average_times_taken}\n"
                        text += f"average_time_between_WB: {round(pt.average_time_between_WB)} s\n"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)

                else:
                    text = "chat_id not found"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def adm_clear_probe(self, caller, *args):
        if caller.admlevel > 9:
            for chat_id, user in self.server.playersdb.players_and_parties.items():
                if chat_id[0] == "/":
                    user.average_time_between_dungeons_pt = 0
                    user.average_time_between_last_dungeons_pt = 0
                    user.average_times_taken_pt = []
                    user.last_done_dungeon_time_pt = 0
                    user.average_time_between_WB_pt = user.average_time_between_dungeons_pt/5
                    user.last_dg_id_pt = {}
                else:
                    user.average_time_between_dungeons = 0
                    user.average_time_between_last_dungeons = 0
                    user.average_times_taken = []
                    user.last_done_dungeon_time = 0
                    user.average_time_between_WB = user.average_time_between_dungeons/5
                    user.last_dg_id = {}
            text = "Sucessfully cleared the probe cache."
            self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def adm_show_adm_list(self, caller, *args):
        text = "List of admins:\n\n"
        if caller.admlevel > 9:
            for chat_id,jog in self.server.playersdb.players_and_parties.items():
                if not chat_id.startswith("/"):
                    if jog.admlevel:
                        text += f"({chat_id}) {jog.name}, level: {jog.admlevel}\n"
            self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def give_a_forest(self, caller, *args):
        if caller.admlevel > 9:
            for chat, jog in self.server.playersdb.players_and_parties.items():
                if not chat.startswith('/'):
                    jog.leaves += 100
                    text = "You just recieved 100 leaves enjoy =)"
                    self.server.bot.send_message(text=text, chat_id=chat)
        return False

    def give_leaves(self, caller, *args):
        if caller.admlevel > 0:
            if not args:
                text = "Please type the chat id of the player you want to give  10 leaves."
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                if args[-1] in self.server.playersdb.players_and_parties:
                    self.server.playersdb.players_and_parties[args[-1]].leaves += 10
                    text = f"Sucessfully added 10 leaves to {self.server.playersdb.players_and_parties[args[-1]]}."
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    text = f"Your recieved 10 leaves by {caller}."
                    self.bot.send_message(text=text, chat_id=args[-1])
                else:
                    text = "chat_id not found"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def del_inv(self, caller, *args):
        if caller.admlevel > 0:
            if not args:
                text = "Please type the chat id of the player you want to delete the /inv."
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                if args[-1] in self.server.playersdb.players_and_parties:
                    self.server.playersdb.players_and_parties[args[-1]].inventory = []
                    text = f"Sucessfully deleted {self.server.playersdb.players_and_parties[args[-1]]}'s /inv."
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    text = f"Your /inv have been deleted by {caller}."
                    self.bot.send_message(text=text, chat_id=args[-1])
                else:
                    text = "chat_id not found"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def up_all_stats(self, caller, *args):
        if caller.admlevel > 9:
            for chat,jog in self.server.playersdb.players_and_parties.items():
                if not chat.startswith("/"):
                    for arma in jog.inventory:
                        if arma.type == "Weapon":
                            arma.update_stats()
        return False

    def over_weight(self, caller, *args):
        if caller.admlevel > 9:
            if not args:
                text = "Type the player chat id to give all possibles talismans."
                self.bot.send_message(text = text, chat_id = caller.chat_id)
                return self.def_wait_time
            else:
                chat_id = args[-1]
                text = ''
                if chat_id in self.server.playersdb.players_and_parties:
                    user = self.server.playersdb.players_and_parties[chat_id]
                    for i in range(99):
                        for talisman in self.Talismandb.talismans:
                            new_t = copy.deepcopy(self.Talismandb.talismans[talisman])
                            new_t.rarity = 6
                            user.storage.append(new_t)
                    text = "The player received all talismans in the database and a bit more."
                else:
                    text = "Player not found."

                self.bot.send_message(text = text, chat_id = caller.chat_id)
        return False

    def deep_delver2(self, caller, *args):
        if caller.admlevel > 0:
            if not args:
                text = "Please type the chat id of the player you want to push to the next tier of the deep forest."
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                if args[-1] in self.server.deep_forest_manager.jogs:
                    self.server.deep_forest_manager.jogs[args[-1]].entry_time += 3*60*60
                    text = f"Sucessfully pushed {self.server.playersdb.players_and_parties[args[-1]].name} is now at level {int(self.server.deep_forest_manager.jogs[args[-1]].stay_time/(3*3600))}"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    text = f"You have been pushed to level {int(self.server.deep_forest_manager.jogs[args[-1]].stay_time/(3*3600))} of the deep forest."
                    self.bot.send_message(text=text, chat_id=args[-1])
                else:
                    text = "chat_id not found"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def deep_delver(self, caller, *args):
        if caller.admlevel > 0:
            if not args:
                text = "Please type the chat id of the player you want to push to the next tier of the deep forest."
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                if args[-1] in self.server.deep_forest_manager.jogs:
                    self.server.deep_forest_manager.jogs[args[-1]].entry_time -= 3*60*60
                    text = f"Sucessfully pushed {self.server.playersdb.players_and_parties[args[-1]].name} is now at level {int(self.server.deep_forest_manager.jogs[args[-1]].stay_time/(3*3600))}"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    text = f"You have been pushed to level {int(self.server.deep_forest_manager.jogs[args[-1]].stay_time/(3*3600))} of the deep forest."
                    self.bot.send_message(text=text, chat_id=args[-1])
                else:
                    text = "chat_id not found"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False
    def shit(self, caller, *args):
        if caller.admlevel > 0:
            total = 0
            for chat,jog in self.server.playersdb.players_and_parties.items():
                suc_refs = 0
                fails = 0
                if not chat.startswith("/"):
                    for chat2,jog2 in self.server.playersdb.players_and_parties.items():
                        if not chat2.startswith("/"):

                            if jog2.referal == chat:
                                if jog2.classe != "Unknown":
                                    suc_refs += 1
                                else:
                                    fails += 1
                if not chat.startswith("/"):
                    print(f"chat: {chat}, suc_refs: {suc_refs}, fails: {fails}")

                    self.server.playersdb.players_and_parties[jog.chat_id].suc_refs = suc_refs
            print(f"done, all players referals have been put into place. {total}")
            return False

    def tier3(self, caller, *args):
        if caller.admlevel > 0:
            if not args:
                text = "Please type the chat id of the player you want to push to the middle of the forest."
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                if args[-1] in self.server.woods.players:
                    self.server.woods.players[args[-1]]["rem_time"] = 6*60*60
                    text = f"Sucessfully pushed {self.server.playersdb.players_and_parties[args[-1]].name} to the middle of the forest"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    text = f"You have been pushed to the middle of the forest."
                    self.bot.send_message(text=text, chat_id=args[-1])
                else:
                    text = "chat_id not found"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False
    def smpp(self, caller, *args):
        if caller.admlevel > 0:
            text = "Removed things:\n\n"
            chat_id_list = list(self.server.playersdb.players_and_parties)
            for chat in chat_id_list:
                if chat.startswith("/"):
                    jog = self.server.playersdb.players_and_parties[chat]
                    for jog2 in jog.players:
                        if self.server.playersdb.players_and_parties[jog2.chat_id].pt_code != jog.pt_code:
                            self.PartyComs.adm_leave_party_comm(jog2.chat_id, jog.pt_code)
                            text += f"{jog2} removed from {self.server.playersdb.players_and_parties[jog2.chat_id].pt_name}\n"
            self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def mpp(self, caller, *args):
        if caller.admlevel > 0:
            things = {}
            for chat,jog in self.server.playersdb.players_and_parties.items():
                if chat.startswith("/"):
                    for jog2 in jog.players:
                        if not jog2.chat_id in things:
                            things[jog2.chat_id] = 1
                        else:
                            things[jog2.chat_id] += 1
            text = "Players in 2 parties at once:\n"
            for chat,rep in things.items():
                if rep > 1:
                    text += f"{self.server.playersdb.players_and_parties[chat].name} in {rep} parties\n"
            self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def sefodeu(self, caller, *args):
        if caller.admlevel > 0:
            if not args:
                text = "Please type the chat id of the player you want to give 0 rank."
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                if args[-1] in self.server.playersdb.players_and_parties:
                    self.server.playersdb.players_and_parties[args[-1]].arena_rank = 0
                    text = f"Sucessfully given o arena rank to {self.server.playersdb.players_and_parties[args[-1]].name}"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    text = f"You have been given zero arena rank."
                    self.bot.send_message(text=text, chat_id=args[-1])
                else:
                    text = "chat_id not found"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def inf_arena(self, caller, *args):
        if caller.admlevel > 0:
            if not args:
                text = "Please type the chat id of the player you want to give infinite arenas."
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                if args[-1] in self.server.playersdb.players_and_parties:
                    self.server.playersdb.players_and_parties[args[-1]].arenas_left = -1
                    text = f"Sucessfully given infinite arenas to {self.server.playersdb.players_and_parties[args[-1]].name}"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    text = f"You have been given infinite arenas for today."
                    self.bot.send_message(text=text, chat_id=args[-1])
                else:
                    text = "chat_id not found"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
        return False

    def give_items(self, caller, *args):
        if caller.admlevel > 0:
            if not args:
                text = "Please type the chat id of the player you want to give a 100/100, a 50/50 and a 1/1."
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                if args[-1] in self.server.playersdb.players_and_parties:
                    weapon = items.Weapon("Equip This", True, "equip", 1, [100, 100])
                    self.server.playersdb.players_and_parties[args[-1]].inventory.append(weapon)
                    weapon = items.Weapon("Use this as bet", True, "bet", 1, [50, 50])
                    self.server.playersdb.players_and_parties[args[-1]].inventory.append(weapon)
                    weapon = items.Weapon("Use this as fee", True, "fee", 1, [1, 1])
                    self.server.playersdb.players_and_parties[args[-1]].inventory.append(weapon)
                    text = f"Training weapons given to {self.server.playersdb.players_and_parties[args[-1]].name}!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    text = f"You just recieved Training weapons."
                    self.bot.send_message(text=text, chat_id=args[-1])
                else:
                    text = "Chat id not found."
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                return False
        else:
            return False
    def clear_comms(self, caller, *args):
        if caller.admlevel > 9:
            self.server.messageman.waiting_from = {}
            text = "Succesfully Cleared the messageman waiting_from"
            self.bot.send_message(chat_id = caller.chat_id, text = text)
        return False

    def remove_from_sf(self, caller, *args):
        if caller.admlevel > 0:
            if not args:
                text = "Please send the player chat_id be removed from the sunflower"
                self.bot.send_message(chat_id = caller.chat_id, text = text)
                return self.def_wait_time
            else:
                target_chat = args[-1]
                if target_chat in self.server.World_boss.status["Players"]:
                    if self.server.playersdb.players_and_parties[target_chat].pt_code:
                        dic = self.server.parties_codes[self.server.playersdb.players_and_parties[target_chat].pt_code]
                        self.WBComms.pt_WB(self.server.playersdb.players_and_parties[target_chat],dic,("/run_away"))
                        text = f""
                    else:
                        self.WBComms.WB(self.server.playersdb.players_and_parties[target_chat],("/run_away"))
                else:
                    text = "Chat_id not found in the sunflower"
                    self.bot.send_message(chat_id = caller.chat_id, text = text)
                return False

    def activate_player(self, caller, *args):
        if caller.admlevel > 0:
            if not args:
                text = "Please send the player chat_id be activated"
                self.bot.send_message(chat_id = caller.chat_id, text = text)
                return self.def_wait_time
            else:
                target_chat = args[-1]
                if target_chat in self.server.woods.players:
                    self.server.woods.players[target_chat]["active"] = True
                    text = f"{self.server.playersdb.players_and_parties[target_chat].name} is now active"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)

                else:
                    text = "Chat_id not found in the forest"
                    self.bot.send_message(chat_id = caller.chat_id, text = text)
                return False

    def adm_fix_stuck_players(self, caller, *args):
        txt = ""
        if caller.admlevel > 0:
            for chat_id, jog in self.server.playersdb.players_and_parties.items():
                if jog.location == "blacksmith" or jog.location=="dungeon":
                    if chat_id in self.server.woods.players:
                        self.server.woods.players[chat_id]["active"] = True
                        self.server.playersdb.players_and_parties[chat_id].location = "forest"
                    elif chat_id in self.server.deep_forest_manager.jogs:
                        self.server.deep_forest_manager.jogs[chat_id].active = True
                        self.server.playersdb.players_and_parties[chat_id].location = "deep_forest"
                    txt += f"Player {jog.name} Unstuck\n"
            self.bot.send_message(chat_id = caller.chat_id, text = txt)
        return False

    def activate_forest(self, caller, *args):
        '''Obriga o jogo a processar as florestas'''
        if caller.admlevel > 0:
            self.server.update_woods = True
            text = f"Woods updated"
            self.bot.send_message(text = text, chat_id = caller.chat_id)
        return False

    def player_name_finder(self, caller, *args):
        '''Você da um nome do jogador e ele te da todos os chat ids com este nome'''
        if caller.admlevel > 0:
            if not args:
                text = "Please, send me the name of the player."
                self.bot.send_message(text = text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                player_name = str(args[-1])
                lista = []
                for chat_id,jogador in self.server.playersdb.players_and_parties.items():
                    if jogador.name == player_name:
                        lista.append(chat_id)
                if lista:
                    text = "Found those chats ids:\n"
                    for chat_id in lista:
                        text += str(chat_id)+"\n"
                    self.bot.send_message(text=text,chat_id = caller.chat_id)
                else:
                    text = "Player name not found"
                    self.bot.send_message(text=text,chat_id=caller.chat_id)
        return False

    def adm_show_equipped_weapon_stats(self, caller, *args):
        if caller.admlevel > 0:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                t_chat_id = str(args[-1])
                if t_chat_id in self.server.playersdb.players_and_parties:
                    pl = self.server.playersdb.players_and_parties[t_chat_id]
                    txt = pl.weapon.power_list()
                    self.bot.send_message(text=txt, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

                else:
                    text = "Player not found!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False
        return False
    def adm_show_stats(self, caller, *args):
        '''Mostra o "/me" do jogador alvo pra quem deu esse comando'''
        if caller.admlevel > 0:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                t_chat_id = str(args[-1])

                if t_chat_id in self.server.playersdb.players_and_parties:
                    if not t_chat_id[0] == "/":
                        self.playerComs.show_stats(caller, self.server.playersdb.players_and_parties[t_chat_id])
                    else:
                        try:
                            self.bot.send_message(text = self.PartyComs.adm_print_pt(self.server.playersdb.players_and_parties[t_chat_id]),chat_id = caller.chat_id, parse_mode = "MARKDOWN")
                        except:
                            self.bot.send_message(text = self.PartyComs.adm_print_pt(self.server.playersdb.players_and_parties[t_chat_id]),chat_id = caller.chat_id)
                else:
                    text = "Player not found!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False


        return False

    def zeus(self, caller, *args):
        '''Assasina um jogador'''
        if caller.admlevel > 0:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                target_chat_id = str(args[-1])
                if target_chat_id in self.server.playersdb.players_and_parties:
                    target = self.server.playersdb.players_and_parties[target_chat_id]
                    s = "You just have been struck by lightning on clear, sunny day. Now you're dead.\n\nTip: Offensive weapon names attract lightning."
                    self.bot.send_message(text=s, chat_id=target_chat_id)
                    text = "Player succesfully struck"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    self.death.die(target_chat_id)                              # Dead, not big surprise
                else:
                    text = "Player not found!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
        return False

    def adm_show_inv(self, caller, *args):
        '''
            Mostra o inventário jogador com um chat_id como parâmetro pra quem deu o comando
        '''
        if caller.admlevel > 0:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                t_chat_id = str(args[-1])
                if t_chat_id in self.server.playersdb.players_and_parties:
                    target = self.server.playersdb.players_and_parties[t_chat_id]
                    s = ""
                    for i in target.inventory:
                        n_name = i.name
                        n_name = n_name.replace("*", "\\*")
                        n_code = i.code
                        n_code = n_code.replace("*", "\\*")
                        s += emojize(f"*{n_name}* :crossed_swords:{i.atributos[0]} :shield:{i.atributos[1]} /e_{n_code}\n")
                        s += i.power_list()
                    if s == "":
                        s = "That player doesn't have anything"
                    s = s.replace("_", "\\_")
                    print(s)
                    self.bot.send_message(text=s, chat_id=caller.chat_id, parse_mode='MARKDOWN', reply_markup=self.defkb)
                else:
                    text = "Player not found!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

        return False

    def adm_show_pokedex(self, caller, *args):
        '''
            Mostra a pokedex do jogador alvo pra quem deu o comando
            (levemente inútil)
        '''
        if caller.admlevel > 0:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                t_chat_id = str(args[-1])
                if t_chat_id in self.server.playersdb.players_and_parties:
                    self.playerComs.show_pokedex(caller, self.server.playersdb.players_and_parties[t_chat_id])
                else:
                    text = "Player not found!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

        return False

    def adm_show_health(self, caller, *args):
        '''
            Mostra o hp do jogador alvo pra quem deu o comando
        '''
        if caller.admlevel > 0:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                t_chat_id = str(args[-1])
                if t_chat_id in self.server.playersdb.players_and_parties:
                    self.playerComs.show_health(caller, self.server.playersdb.players_and_parties[t_chat_id])
                else:
                    text = "Player not found!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

        return False

    def adm_rename(self, caller, *args):
        '''
            Se um jogador tiver um nome ofensivo, ele renomeia prum nome standard
        '''
        if caller.admlevel > 4:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time

            else:
                player_name = "once an offensive name, now just shame"
                chat_id = args[-1]
                self.server.bl_controller.ban_player(chat_id)
                self.server.playersdb.players_and_parties[chat_id].name = player_name
        return False

    def make_gm(self, caller, *args):
        '''
            Aumenta o nível de adm do jogador com o chat_id alvo (nível 4)
        '''
        if caller.admlevel > 4:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                t_chat_id = str(args[-1])
                if t_chat_id in self.server.playersdb.players_and_parties:
                    if self.server.playersdb.players_and_parties[t_chat_id].admlevel < 1:
                        self.server.playersdb.players_and_parties[t_chat_id].set_adm(1)
                    text = f"{self.server.playersdb.players_and_parties[t_chat_id].name} is now a GM!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                else:
                    text = "Player not found!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

        return False

    def give_weapon(self, caller, *args):
        '''
            Da uma arma pro jogador alvo
        '''
        if caller.admlevel > 4:
            if not args:
                self.commands_dict[caller.chat_id] = {}
                self.commands_dict[caller.chat_id]["adm_gw_id"] = ""
                self.commands_dict[caller.chat_id]["adm_gw_stage"] = 0
                self.commands_dict[caller.chat_id]["adm_gw_name"] = "weapon"
                self.commands_dict[caller.chat_id]["adm_gw_at"] = 1
                self.commands_dict[caller.chat_id]["adm_gw_def"] = 1
                self.commands_dict[caller.chat_id]["adm_gw_com"] = "wep"
                self.commands_dict[caller.chat_id]["talisman_list"] = []
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                if self.commands_dict[caller.chat_id]["adm_gw_stage"] == 0:          # tem vários estágios, perguntando qual o nome, ataque, defesa e código da arma, quase como se fosse um blacksmith
                    self.commands_dict[caller.chat_id]["adm_gw_id"] = args[-1]
                    t_chat_id = args[-1]
                    if t_chat_id in self.server.playersdb.players_and_parties:
                        text = "Give the weapon a name"
                        self.bot.send_message(text=text, chat_id=caller.chat_id)
                        self.commands_dict[caller.chat_id]["adm_gw_stage"] = 1
                        return self.def_wait_time
                    else:
                        text = "Player not found!"
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                        return False
                elif self.commands_dict[caller.chat_id]["adm_gw_stage"] == 1:
                    self.commands_dict[caller.chat_id]["adm_gw_name"] = args[-1]
                    text = emojize("Choose the weapon's attack :crossed_swords:")
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    self.commands_dict[caller.chat_id]["adm_gw_stage"] = 2
                    return self.def_wait_time
                elif self.commands_dict[caller.chat_id]["adm_gw_stage"] == 2:
                    try:
                        self.commands_dict[caller.chat_id]["adm_gw_at"] = int(args[-1])
                    except:
                        self.commands_dict[caller.chat_id]["adm_gw_at"] = -1
                    text = emojize("Choose the weapon's defense :shield:")
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    self.commands_dict[caller.chat_id]["adm_gw_stage"] = 3
                    return self.def_wait_time
                elif self.commands_dict[caller.chat_id]["adm_gw_stage"] == 3:
                    try:
                        self.commands_dict[caller.chat_id]["adm_gw_def"] = int(args[-1])
                    except:
                        self.commands_dict[caller.chat_id]["adm_gw_def"] = -1
                    text = "Give the weapon a code, to be appended to the /e_ command"
                    self.bot.send_message(text=text, chat_id=caller.chat_id)
                    self.commands_dict[caller.chat_id]["adm_gw_stage"] = 4
                    return self.def_wait_time

                elif self.commands_dict[caller.chat_id]["adm_gw_stage"] == 4:
                    self.commands_dict[caller.chat_id]["adm_gw_com"] = args[-1]
                    text = "Choose the talismans you would like to apply to the weapon."

                    talisman_list = ["Done"]
                    talisman_list.extend([talisman_code for talisman_code in self.Talismandb.talismans])
                    talisman_keyboard = self.server.keyboards.create_keyboard_from_list(talisman_list)

                    self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = talisman_keyboard)
                    self.commands_dict[caller.chat_id]["adm_gw_stage"] = 5
                    return self.def_wait_time

                elif self.commands_dict[caller.chat_id]["adm_gw_stage"] == 5:
                    if len(self.commands_dict[caller.chat_id]["talisman_list"]) < 5:
                        talisman_code = args[-1]
                        if talisman_code == "Done":
                            self.commands_dict[caller.chat_id]["adm_gw_stage"] = 6
                        elif talisman_code in self.Talismandb.talismans:
                            self.commands_dict[caller.chat_id]["talisman_list"].append(talisman_code)
                            text = f"Talisman list: {self.commands_dict[caller.chat_id]['talisman_list']}"
                            self.bot.send_message(text = text, chat_id = caller.chat_id)
                    else:
                        self.commands_dict[caller.chat_id]["adm_gw_stage"] = 6

                if self.commands_dict[caller.chat_id]["adm_gw_stage"] == 6:
                    text = "Now choose the weapon type."
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.bs_type_custom_keyboard)
                    self.commands_dict[caller.chat_id]["adm_gw_stage"] = 7
                    return self.def_wait_time

                if self.commands_dict[caller.chat_id]["adm_gw_stage"] == 7:
                    tipo = args[-1]
                    if tipo == emojize(":crossed_swords: Melee :crossed_swords:"):
                        tipo2 = "melee"
                    elif tipo == emojize(":crystal_ball: Magic :crystal_ball:"):
                        tipo2 = "magic"
                    elif tipo == emojize(":bow_and_arrow: Ranged :bow_and_arrow:"):
                        tipo2 = "ranged"
                    weapon = items.Weapon(emojize(self.commands_dict[caller.chat_id]["adm_gw_name"]), True, self.commands_dict[caller.chat_id]["adm_gw_com"], 1, [self.commands_dict[caller.chat_id]["adm_gw_at"], self.commands_dict[caller.chat_id]["adm_gw_def"]])
                    weapon.owner = self.commands_dict[caller.chat_id]["adm_gw_id"]
                    talisman_list = [copy.deepcopy(self.Talismandb.talismans[talisman_code]) for talisman_code in self.commands_dict[caller.chat_id]['talisman_list']]

                    for t in talisman_list:
                        r_up = 6 - t.rarity
                        t.rarity = 6
                        for power_name, power in t.powers.items():
                            t.powers[power_name] = power*(r_up + 1)
                    weapon.add_talismans(talisman_list)
                    weapon.type2 = tipo2
                    self.server.playersdb.players_and_parties[self.commands_dict[caller.chat_id]["adm_gw_id"]].inventory.append(weapon)
                    text = f"{self.commands_dict[caller.chat_id]['adm_gw_name']} given to {self.server.playersdb.players_and_parties[self.commands_dict[caller.chat_id]['adm_gw_id']].name}!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

                return self.def_wait_time
        return False

    def adm_forest(self, caller, *args):
        '''
            Tira e bota da floresta o jogador com chat_id alvo ou uma party inteira com chat_id alvo
        '''
        if caller.admlevel > 4:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time

            else:
                t_chat_id = str(args[-1])
                if t_chat_id in self.server.playersdb.players_and_parties:
                    text = ""

                    if t_chat_id in self.server.woods.players:
                        self.server.woods.exit_woods(t_chat_id)
                        if not t_chat_id.startswith("/"):
                            text = f"{self.server.playersdb.players_and_parties[t_chat_id].name} is now out of the forest!"
                        else:
                            temp = "name"
                            text = f"{self.server.playersdb.players_and_parties[t_chat_id].pt_name} is now out of the forest!"
                    elif t_chat_id in self.server.deep_forest_manager.jogs:
                        self.server.deep_forest_manager.leave(t_chat_id)
                        if not t_chat_id.startswith("/"):
                            text = f"{self.server.playersdb.players_and_parties[t_chat_id].name} is now out of the deep forest!"
                        else:
                            temp = "name"
                            text = f"{self.server.playersdb.players_and_parties[t_chat_id].pt_name} is now out of the deep forest!"


                    else:
                        if t_chat_id.startswith("/"):
                            self.server.woods.add_to_woods(self.server.playersdb.players_and_parties[t_chat_id])
                        self.server.woods.add_to_woods(self.server.playersdb.players_and_parties[t_chat_id], 3600)
                        text = ("You started wandering in the forest. You will be back in 1 hour. "
                                "During this time, you may encounter things.")
                        self.bot.send_message(text=text, chat_id=t_chat_id, reply_markup=self.defkb)
                        text = f"{self.server.playersdb.players_and_parties[t_chat_id].name} is now in the forest!"

                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)

                else:
                    text = emojize("Player not found!")
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

        return False

    def remove_all_from_forest(self, caller, *args):
        '''
            Remove all players from the forest
        '''
        if caller.admlevel > 9:
            while len(self.server.woods.players)>0:
                listed_dict = list(self.server.woods.players)
                player_or_party = self.server.woods.players[listed_dict[0]]["player"]

                player_or_party.is_travelling = False
                player_or_party.travel_time = 0
                player_or_party.travelling_loc = ""
                self.server.woods.exit_woods(listed_dict[0])
        text = "All Players removed from the forest!"
        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
        return False

    def make_adm(self, caller, *args):
        '''
            Transforma um jogador em adm (level 9)
        '''
        if caller.admlevel > 9:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                t_chat_id = str(args[-1])
                if t_chat_id in self.server.playersdb.players_and_parties:
                    if self.server.playersdb.players_and_parties[t_chat_id].admlevel < 5:
                        self.server.playersdb.players_and_parties[t_chat_id].set_adm(5)
                    text = f"{self.server.playersdb.players_and_parties[t_chat_id].name} is now an admin!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                else:
                    text = "Player not found!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

        return False

    def shutdown(self, caller):
        '''
            Fecha o joguinho
        '''
        if caller.admlevel > 9:
            self.server.helper.remove_all_commands(caller.chat_id)
            self.server.shutdown_now()
        return False

    def save_all(self, caller):
        '''
            Salva tudo ué
        '''
        if caller.admlevel > 9:
            self.server.save_all()
        return False

    def kill(self, caller, *args):
        '''
            Zera o hp do jogador alvo (função usada normalmente em testes)
        '''
        if caller.admlevel > 9:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                t_chat_id = str(args[-1])
                if t_chat_id in self.server.playersdb.players_and_parties:
                    if t_chat_id in self.server.woods.players:
                        player = self.server.playersdb.players_and_parties[t_chat_id]
                        for limb in player.hp:
                            limb.health = 0
                        text = "You snapped your fingers and that player is left incapacitated."
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    else:
                        text = emojize("Player not in the forest!")
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                else:
                    text = emojize("Player not found!")
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

        return False

    def del_player(self, caller, *args):
        '''
            Deleta o jogador com chat_id alvo

        '''
        if caller.admlevel > 9:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                t_chat_id = str(args[-1])
                if t_chat_id in self.server.playersdb.players_and_parties:
                    self.death.die(t_chat_id)
                    self.server.playersdb.remove_player(t_chat_id)
                    text = "You snapped your fingers and that player is no more."
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                else:
                    text = "Player not found!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

        return False

    def force_lvlup(self, caller, *args):
        '''
            Maximiza o exp de um jogador pra aquele nível
        '''
        if caller.admlevel > 9:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                t_chat_id = str(args[-1])
                if t_chat_id in self.server.playersdb.players_and_parties:
                    target = self.server.playersdb.players_and_parties[t_chat_id]
                    xprem = target.levels[target.level] - target.exp
                    target.exp += xprem
                    self.playerComs.level_up(target)
                    text = "You snapped your fingers and that player became stronger."
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                else:
                    text = "Player not found!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

        return False

    def force_lvl5(self, caller, *args):
        '''
            Joga um jogador no level 5 (escolha de classes)
        '''
        if caller.admlevel > 9:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                t_chat_id = str(args[-1])
                if t_chat_id in self.server.playersdb.players_and_parties:
                    if t_chat_id[0] != "/":
                        target = self.server.playersdb.players_and_parties[t_chat_id]
                        target.level = 5
                        target.exp = target.levels[5]

                        for att, pts in target.att_points.items():
                            target.att_points[att] = 0
                        target.att_points["unspent"] = target.level - 1

                        text = "You snapped your fingers and that player became 5 times stronger."
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                else:
                    text = "Player not found!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

        return False

    def respec(self, caller, *args):
        '''
            Jogador perde a classe e todos os pontos atribuidos voltam pra ele.
        '''
        if caller.admlevel > 9:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                t_chat_id = str(args[-1])
                if t_chat_id in self.server.playersdb.players_and_parties:
                    target = self.server.playersdb.players_and_parties[t_chat_id]
                    new_player = player.Player(t_chat_id)
                    new_player.new_from_player(target)
                    if self.server.playersdb.players_and_parties[t_chat_id].pt_code:
                        self.server.playersdb.players_and_parties[self.server.playersdb.players_and_parties[t_chat_id].pt_code].leave_pt(self.server.playersdb.players_and_parties[t_chat_id])
                    new_player.att_points["unspent"] = target.level - 1
                    self.server.playersdb.players_and_parties[t_chat_id] = new_player
                    if self.server.playersdb.players_and_parties[t_chat_id].pt_code:
                        self.server.playersdb.players_and_parties[self.server.playersdb.players_and_parties[t_chat_id].pt_code].join_pt(new_player)

                    text = "You snapped your fingers and that player reset."
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                else:
                    text = "Player not found!"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

        return False

    def new_dummy(self, caller):
        '''
            kk nem sei oq isso faz
        '''
        if caller.admlevel > 9:
            name = self.server.helper.randomnamegenerator(6)
            chat_id = self.server.helper.randomnamegenerator(6)
            dummy = player.Player(chat_id, name)
            self.server.playersdb.add_player(dummy)
            text = f"{name} created with chat_id = {chat_id}\n"
            self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
        return False

    def print_players(self, caller):
        '''
            Printa o nome de TODOS os jogadores no console (pf fiquem longe disso)
        '''
        if caller.admlevel > 9:
            print("-----")
            print("Players:")
            for chat_id, pl in self.server.playersdb.players_and_parties.items():
                print(f"{chat_id}: {pl.name}")
        return False

    def adm_blessing(self, caller):
        '''
            Força todos os jogadores irem pro level 5
        '''
        if caller.admlevel > 9:
            for chat_id, jogador in self.server.playersdb.players_and_parties.items():
                if chat_id[0] != "/":
                    jogador.level = 5
                    jogador.exp = jogador.levels[5]

                    for att, pts in jogador.att_points.items():
                        jogador.att_points[att] = 0
                    jogador.att_points["unspent"] = jogador.level - 1

                    text = "Alllleeeeluuuuuiiiiiiiiiiiiiaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n\nnow you're level 5"
                try:
                    self.bot.send_message(text=text, chat_id=jogador.chat_id, reply_markup=self.defkb)
                except:
                    pass
        return False

    def adm_buff(self, caller, *args):
        '''
            Buffa um jogador no nível desejado
        '''
        if caller.admlevel > 4:
            if not args:
                self.adm_buff_stage = 0
                self.adm_buff_level = 0
                self.adm_buff_id = ""
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)
                return self.def_wait_time
            else:
                if self.adm_buff_stage == 0:
                    self.adm_buff_id = args[-1]
                    t_chat_id = args[-1]
                    if t_chat_id in self.server.playersdb.players_and_parties:
                        text = "Select buff level (0-6)"
                        self.bot.send_message(text=text, chat_id=caller.chat_id)
                        self.adm_buff_stage = 1

                        return self.def_wait_time

                    else:
                        text = "Player not found!"
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)

                        return False

                elif self.adm_buff_stage == 1:
                    self.adm_buff_level = 0
                    try:
                        self.adm_buff_level = int(args[-1])
                    except:
                        pass

                    if self.adm_buff_level > 6:
                        self.adm_buff_level = 6
                    self.server.playersdb.players_and_parties[self.adm_buff_id].buff_man.buff_state = self.adm_buff_level
                    self.server.playersdb.players_and_parties[self.adm_buff_id].calc_attributes()

                    text = emojize("Player :flexed_biceps: buffed :flexed_biceps:")
                    self.bot.send_message(text=text, chat_id=caller.chat_id)

                    return False

        return False

    def adm_heal(self, caller, *args):
        '''
            Cura o jogador alvo 100%
        '''
        if caller.admlevel > 4:
            if not args:
                text = "Type player's chat_id"
                self.bot.send_message(text=text, chat_id=caller.chat_id)

                return self.def_wait_time

            else:
                t_chat_id = args[-1]
                for limb in self.server.playersdb.players_and_parties[t_chat_id].hp:
                    limb.health = len(limb.states) - 1

                text = "Player healed!"
                self.bot.send_message(text=text, chat_id=caller.chat_id)

        return False

    def to(self, caller):
        pass

    def hmmmmmmmmmmm(self, caller, *args):
        '''
            Checa se um jogador de grupo está dentro de uma party
        '''
        if caller.admlevel > 4:
            texo = ""
            for chat,jog in self.server.playersdb.players_and_parties.items():
                if chat.startswith("-") and jog.pt_code:
                    texo += f"{chat}\n"
            self.bot.send_message(text=texo, chat_id=caller.chat_id)
        return False

    def send_message_to_all_players(self, caller, *args):
        if caller.admlevel > 9:
            if not args:
                self.commands_dict[caller.chat_id] = {}
                self.commands_dict[caller.chat_id]["global_messages"] = []
                text = "Type the global message starting with /text. \n\nWARNING: this message will be sent to all active player in the game. Write carefully."
                self.bot.send_message(text = text, chat_id = caller.chat_id)
                return self.def_wait_time
            elif args[-1][:5] == "/text":
                self.commands_dict[caller.chat_id]["global_messages"].append(args[-1][6:])
                text = "Are you sure you want to send the following message to all active player?\n\n"
                text += self.commands_dict[caller.chat_id]["global_messages"][0]
                self.bot.send_message(text = emojize(text), chat_id = caller.chat_id, reply_markup = self.server.keyboards.forest_return_reply_markup)
                return self.def_wait_time
            else:
                if args[-1] == "yes":
                    global_text = self.commands_dict[caller.chat_id]["global_messages"][0]
                    global_text += "\n\nIf you have any problem or question, you can seek help from the adms and players in the campfire: https://t.me/DWcommchat"
                    for p_chat_id, time in self.server.playersdb.players_and_parties.items():
                        self.bot.send_message(text=emojize(global_text), chat_id=p_chat_id)
                    self.commands_dict[caller.chat_id]["global_messages"] = []
                else:
                    text = "Aborting"
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    self.commands_dict[caller.chat_id]["global_messages"] = []
        return False

    def force_encounter(self, caller, *args):
        ''' Método usado para forçar um encontro na floresta para player e party'''
        if caller.admlevel > 9:
            if not args:
                self.commands_dict[caller.chat_id] = {}
                self.commands_dict[caller.chat_id]["f_encounter_iteration"] = 0
                self.commands_dict[caller.chat_id]["f_encounter_id"] = ""
                text = "Type the players chat ID or the party's code."
                self.bot.send_message(text = text, chat_id = caller.chat_id)
                return self.def_wait_time
            else:
                encounters_list = [encounter for encounter in self.server.woods.encounters]
                if self.commands_dict[caller.chat_id]["f_encounter_iteration"] == 0:

                    self.commands_dict[caller.chat_id]["f_encounter_id"] = args[-1]
                    self.commands_dict[caller.chat_id]["f_encounter_iteration"] = 1
                    text = "what kind of encounter you want to force?"

                    encounter_keyboard = self.server.keyboards.create_keyboard_from_list(encounters_list)

                    self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = encounter_keyboard)

                    return self.def_wait_time

                if self.commands_dict[caller.chat_id]["f_encounter_iteration"] == 1:
                    encounter = args[-1]
                    text = "The encounter was successfully forced."
                    try:
                        if self.commands_dict[caller.chat_id]["f_encounter_id"][0] == "/":
                            self.server.woods.pt_encounters[encounter][1](self.commands_dict[caller.chat_id]["f_encounter_id"])
                        else:
                            self.server.woods.encounters[encounter][1](self.commands_dict[caller.chat_id]["f_encounter_id"])
                    except KeyError:
                        text = "Encounter not valid"
                    except ValueError:
                        text = "Code not valid"
                    self.commands_dict[caller.chat_id] = {}
                    self.bot.send_message(text = text, chat_id = caller.chat_id)
        return False

    def force_deep_encounter(self, caller, *args):
        ''' Método usado para forçar um encontro na floresta para player e party'''
        if caller.admlevel > 9:
            if not args:
                self.commands_dict[caller.chat_id] = {}
                self.commands_dict[caller.chat_id]["f_encounter_iteration"] = 0
                self.commands_dict[caller.chat_id]["f_encounter_id"] = ""
                text = "Type the players chat ID or the party's code."
                self.bot.send_message(text = text, chat_id = caller.chat_id)
                return self.def_wait_time
            else:
                encounters_list = [encounter for encounter in self.server.deep_forest_manager.deep_encounters.keys()]
                if self.commands_dict[caller.chat_id]["f_encounter_iteration"] == 0:

                    self.commands_dict[caller.chat_id]["f_encounter_id"] = args[-1]
                    self.commands_dict[caller.chat_id]["f_encounter_iteration"] = 1
                    text = "what kind of encounter you want to force?"

                    encounter_keyboard = self.server.keyboards.create_keyboard_from_list(encounters_list)

                    self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = encounter_keyboard)

                    return self.def_wait_time

                if self.commands_dict[caller.chat_id]["f_encounter_iteration"] == 1:
                    encounter = args[-1]
                    text = "The encounter was successfully forced."
                    try:
                        self.server.deep_forest_manager.deep_encounters[encounter][1](self.commands_dict[caller.chat_id]["f_encounter_id"])
                    except KeyError:
                        text = "Encounter not valid"
                    except ValueError:
                        text = "Code not valid"
                    self.commands_dict[caller.chat_id] = {}
                    self.bot.send_message(text = text, chat_id = caller.chat_id)
        return False

    def give_all_possibles_talismans(self, caller, *args):
        if caller.admlevel > 9:
            if not args:
                text = "Type the player chat id to give all possibles talismans."
                self.bot.send_message(text = text, chat_id = caller.chat_id)
                return self.def_wait_time
            else:
                chat_id = args[-1]
                text = ''
                if chat_id in self.server.playersdb.players_and_parties:
                    user = self.server.playersdb.players_and_parties[chat_id]
                    for talisman in self.Talismandb.talismans:
                        user.storage.append(self.Talismandb.talismans[copy.deepcopy(talisman)])
                    text = "The player received all talismans in the database."
                else:
                    text = "Player not found."

                self.bot.send_message(text = text, chat_id = caller.chat_id)
        return False


    def give_a_talisman(self, caller, *args):
        if caller.admlevel > 9:
            if not args:
                self.commands_dict[caller.chat_id] = {}
                self.commands_dict[caller.chat_id]["talisman"] = None
                self.commands_dict[caller.chat_id]["talisman_iteration"] = 0
                self.commands_dict[caller.chat_id]["t_player_id"] = ""
                text = "Type the player chat id to give a talisman."
                self.bot.send_message(text = text, chat_id = caller.chat_id)
                return self.def_wait_time
            else:
                if self.commands_dict[caller.chat_id]["talisman_iteration"] == 0:
                    chat_id = args[-1]
                    if chat_id in self.server.playersdb.players_and_parties:
                        self.commands_dict[caller.chat_id]["t_player_id"] = chat_id
                        talisman_list = [talisman_code for talisman_code in self.Talismandb.talismans]
                        talisman_keyboard = self.server.keyboards.create_keyboard_from_list(talisman_list)
                        text = "Choose a talisman to give."
                        self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = talisman_keyboard)
                        self.commands_dict[caller.chat_id]["talisman_iteration"] = 1
                        return self.def_wait_time
                    else:
                        text = "Player not found."
                        self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.defkb)
                        self.commands_dict[caller.chat_id] = {}
                        return False
                if self.commands_dict[caller.chat_id]["talisman_iteration"] == 1:
                    talisman_code = args[-1]
                    if talisman_code in self.Talismandb.talismans:
                        self.commands_dict[caller.chat_id]["talisman"] = copy.deepcopy(self.Talismandb.talismans[talisman_code])
                        text = f"Choose a rarity up for the talisman. Original: {self.commands_dict[caller.chat_id]['talisman'].rarity}"
                        rarity_list = list(range(7))
                        rarity_keyboard = self.server.keyboards.create_keyboard_from_list(rarity_list)
                        self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = rarity_keyboard)
                        self.commands_dict[caller.chat_id]["talisman_iteration"] = 2
                        return self.def_wait_time
                    else:
                        text = "Talisman not valid."
                        self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.defkb)
                        self.commands_dict[caller.chat_id] = {}
                        return False
                if self.commands_dict[caller.chat_id]["talisman_iteration"] == 2:
                    rarity = args[-1]
                    text = ""
                    if rarity in str(list(range(7))):   # Dá certo, pois ele vai procurar o string dado dentro do string.
                        rarity_up = int(rarity)
                        if self.commands_dict[caller.chat_id]["talisman"].rarity + rarity_up > 6:
                            rarity_up = 6 - self.commands_dict[caller.chat_id]["talisman"].rarity

                        self.commands_dict[caller.chat_id]["talisman"].rarity += rarity_up
                        for power_name, power in self.commands_dict[caller.chat_id]["talisman"].powers.items():
                            self.commands_dict[caller.chat_id]["talisman"].powers[power_name] = power*(rarity_up + 1)
                        talisman = self.commands_dict[caller.chat_id]["talisman"]
                        chat_id = self.commands_dict[caller.chat_id]["t_player_id"]
                        self.server.playersdb.players_and_parties[chat_id].storage.append(copy.deepcopy(talisman))
                        text = "Player received the talisman successfully."
                        self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.defkb)

                        for_text_player = f"You received an {talisman.name} from GM {caller.name}! Check your /sto "
                        self.bot.send_message(text = for_text_player, chat_id = chat_id)
                    else:
                        text = "Not a valid rarity."

                    self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.defkb)
                    self.commands_dict[caller.chat_id] = {}
        return False
