###############
#  M O R T E  #
###############

import bot
import copy
import player
import party_comms
from emoji import emojize
from items import Weapon


class Death:
    def __init__(self, server):
        self.server = server
        self.useless = party_comms.PartyComms(server)
        self.bot = bot.TGBot()

    def update_att(self, chat, weapon):
        jog = self.server.playersdb.players_and_parties[chat]
        if weapon.is_shared_and_equipped:
            for wep in self.server.playersdb.players_and_parties[jog.code].inventory:
                if wep.code == weapon.code:
                    wep = weapon
                    break
        else:
            for wep in self.server.playersdb.players_and_parties[chat].inventory:
                if wep.code == weapon.code:
                    wep = weapon
                    break


    def die(self, chat_id):
        if self.server.playersdb.players_and_parties[chat_id].weapon and "death evasion" in self.server.playersdb.players_and_parties[chat_id].weapon.powers:
            if self.server.playersdb.players_and_parties[chat_id].weapon.powers["death evasion"] > 1:
                self.server.playersdb.players_and_parties[chat_id].weapon.powers["death evasion"] -= 1
                self.server.playersdb.players_and_parties[chat_id].weapon.talismans["hydra_heart"].rarity -= 1
                for limb in self.server.playersdb.players_and_parties[chat_id].hp:
                    limb.health = 3
            else:
                for limb in self.server.playersdb.players_and_parties[chat_id].hp:
                    limb.health = 3
                del self.server.playersdb.players_and_parties[chat_id].weapon.powers["death evasion"]
                del self.server.playersdb.players_and_parties[chat_id].weapon.talismans["hydra_heart"]
            self.update_att(chat_id, self.server.playersdb.players_and_parties[chat_id].weapon)
            text = "You are knocked off your feet, unable to continue fighting, but the hydra's resilience fuels a second wind. You do a sick acrobatic recovery and take up your weapon once more.\n\nThe strength of the heart wanes..."
            self.bot.send_message(text=text, chat_id=chat_id)
        else:
            self.kill_player(chat_id)

    def die_event(self, chat_id):
        for limb in self.server.playersdb.players_and_parties[chat_id].hp:
            limb.health = 3
        if self.server.playersdb.players_and_parties[chat_id].weapon:
            eq_weapon = copy.deepcopy(self.server.playersdb.players_and_parties[chat_id].weapon)
            eq_weapon.name = emojize(f":jack-o-lantern: Hallowed {eq_weapon.name} :jack-o-lantern:")
            eq_weapon.og_attr[0], eq_weapon.og_attr[1] = eq_weapon.og_attr[0]*3, eq_weapon.og_attr[1]*3
            eq_weapon.update_stats()
        else:
            if not len(self.server.playersdb.players_and_parties[chat_id].inventory):
                eq_weapon = Weapon(emojize(":jack-o-lantern: Hallowed :dog: Alileb's Sword :dog::jack-o-lantern:"), False, "alileb_sword2", 3, [120*3, 70*3])
            else:
                eq_weapon = None
        for weapon in self.server.playersdb.players_and_parties[chat_id].inventory:
            if weapon.is_legendary:
                self.server.itemsdb.add_weapon_to_pool(copy.deepcopy(weapon))
                self.server.playersdb.players_and_parties[chat_id].inventory.remove(weapon)         # Remove a arma lendária do inv do player para podermos ghostiar o resto de seu inv.


        self.server.playersdb.players_and_parties[chat_id].ghost_inv.extend(self.server.playersdb.players_and_parties[chat_id].inventory)      # Ghosteia o inv do jogador. O ghost inv poderá ser recuperado pelo player via retrace.
        del self.server.playersdb.players_and_parties[chat_id].inventory
        self.server.playersdb.players_and_parties[chat_id].inventory = []
        self.server.playersdb.players_and_parties[chat_id].weapon.unequip(self.server.playersdb.players_and_parties[chat_id])
        eq_weapon.equip(self.server.playersdb.players_and_parties[chat_id])
        self.server.playersdb.players_and_parties[chat_id].has_died = True

    def kill_player(self, chat_id):
        '''
            Mata um jogador com este chat_id.

            Se o jogador estiver numa party, a party é forçada a voltar para o camp, um /leave é forçado no jogador e a party volta à floresta com todos os outros status intactos.

            Parâmetros:
                chat_id (str): chat_id do jogador que vai morrer

        '''
        text = "Laying motionless on the ground, you feel a pull towards the light. As you come closer, the beams start washing away your pain... "
        self.bot.send_message(text=text, chat_id=chat_id)
        if self.server.playersdb.players_and_parties[chat_id].pt_code:
            code = self.server.playersdb.players_and_parties[chat_id].pt_code
            if code in self.server.playersdb.players_and_parties:
                self.server.playersdb.players_and_parties[code].leave_pt(self.server.playersdb.players_and_parties[chat_id])
                text = emojize(f"{self.server.playersdb.players_and_parties[chat_id].name} has died :skull_and_crossbones:")

                # self.server.playersdb.players_and_parties[code].location = "camp"
                # do_other_thing = True
                # self.useless.leave_party_comm(self.server.playersdb.players_and_parties[chat_id], "yes")
                if not self.server.playersdb.players_and_parties[code].players:
                    if code in self.server.woods.players:
                        self.server.woods.to_remove["remove"].append(code)
                    if code in self.server.deep_forest_manager.jogs:
                        self.server.deep_forest_manager.to_remove.append(code)
                    if code in self.server.caverns_manager.jogs:
                        self.server.caverns_manager.to_remove.append(code)
                    del self.server.playersdb.players_and_parties[code]
                    print(f"Party {code} died.")
                else:
                    self.bot.send_message(text = text, chat_id = self.server.playersdb.players_and_parties[code].chat_ids)

            #     do_other_thing = False
            #
            # if do_other_thing:
            #     self.server.playersdb.players_and_parties[code].location = "forest"
            #     self.server.woods.players[code]["player"] = self.server.playersdb.players_and_parties[code]
            #
            # if not do_other_thing:                  # Deletes the player at the forest
            #     del self.server.woods.players[code]
            #     del self.server.playersdb.players_and_parties[code]
            #     print(f"Party {code} died.")

        if self.server.playersdb.players_and_parties[chat_id].weapon:
            eq_weapon = copy.deepcopy(self.server.playersdb.players_and_parties[chat_id].weapon)
            if not (eq_weapon.name.startswith(emojize(":ghost::alien_monster: Ghostly")) or eq_weapon.name == emojize(":dog: Alileb's Sword :dog:")):
                eq_weapon.name = emojize(f":ghost::alien_monster: Ghostly {eq_weapon.name}")

        else:
            if not len(self.server.playersdb.players_and_parties[chat_id].inventory):
                eq_weapon = Weapon(emojize(":dog: Alileb's Sword :dog:"), False, "alileb_sword", 3, [120, 70])
            else:
                eq_weapon = None
        for weapon in self.server.playersdb.players_and_parties[chat_id].inventory:
            if weapon.is_legendary:
                self.server.itemsdb.add_weapon_to_pool(copy.deepcopy(weapon))
                self.server.playersdb.players_and_parties[chat_id].inventory.remove(weapon)         # Remove a arma lendária do inv do player para podermos ghostiar o resto de seu inv.


        self.server.playersdb.players_and_parties[chat_id].ghost_inv.extend(self.server.playersdb.players_and_parties[chat_id].inventory)      # Ghosteia o inv do jogador. O ghost inv poderá ser recuperado pelo player via retrace.
        del self.server.playersdb.players_and_parties[chat_id].inventory
        self.server.playersdb.players_and_parties[chat_id].inventory = []

            # done = False
            # while not done:
            #     if len(self.server.parties_codes[code]["pt_inv"]):
            #         for i in range(len(self.server.parties_codes[code]["pt_inv"])):
            #             item = self.server.parties_codes[code]["pt_inv"][i]
            #             if self.server.parties_codes[code]["pt_inv"][i].owner == chat_id:
            #                 for chat,jog in self.server.parties_codes[code].items():
            #                     if isinstance(jog, player.Player):
            #                         if jog.weapon and jog.weapon.code == self.server.parties_codes[code]["pt_inv"][i].code:
            #                             jog.weapon = None
            #                             item.is_shared_and_equipped = False
            #                             item.owner = ""
            #                             jog.calc_attributes()
            #                             s = "You just lost your equipped weapon beacuse owner left party."
            #                             self.bot.send_message(text = s, chat_id = jog.chat_id)
            #
            #                 self.server.itemsdb.add_weapon_to_pool(copy.deepcopy(item))
            #                 del self.server.parties_codes[code]["pt_inv"][i]
            #                 break
            #             if i == len(self.server.parties_codes[code]["pt_inv"])-1:
            #                 done = True
            #     else:
            #         done = True
            # if chat_id in self.server.parties_codes[code]:
            #     do_not_remove = False
            #     if len(self.server.parties_codes[code]) < 14:
            #         if code in self.server.woods.players:
            #             self.server.woods.players[code]["active"] = False
            #             self.server.woods.to_remove.append(code)
            #             do_not_remove = True
            #     if do_not_remove == False:
            #         del self.server.parties_codes[code][chat_id]
            #         self.server.playersdb.players[chat_id].pt_code = ""
            #         self.server.playersdb.players[chat_id].pt_name = ""


        # self.server.messageman.waiting_from[chat_id] = {}
        if chat_id in self.server.messageman.waiting_from:
            del self.server.messageman.waiting_from[chat_id]
        self.server.playersdb.players_and_parties[chat_id].reset_stats()
        # del self.server.playersdb.players[chat_id].weapon
        # self.server.playersdb.players[chat_id].weapon = None


        if chat_id in self.server.woods.players:
            self.server.woods.to_remove["remove"].append(chat_id)
            # self.server.woods.players[chat_id]["active"] = False
            # self.server.playersdb.players[chat_id].is_at_forest = False
            # self.server.woods.to_remove.append(chat_id)
            print(f"Player {chat_id} was removed from forest")
        elif chat_id in self.server.deep_forest_manager.jogs:
            self.server.deep_forest_manager.to_remove.append(chat_id)
            print(f"Player {chat_id} was removed from deep forest")
        # if self.server.playersdb.players[chat_id].location == 'forest':
        # self.server.playersdb.players_and_parties[chat_id].location = 'camp'
        self.server.playersdb.players_and_parties[chat_id].weapon = eq_weapon
        self.server.playersdb.players_and_parties[chat_id].has_died = True
        text = emojize("Your soul was guided back to safety by the spirit Alileb :dog:, leaving all your items at the forest. You could only remember your name. Alileb gave you a :ghost::alien_monster: ghostly gift. Try not to unequip.")
        self.bot.send_message(text=text, chat_id=chat_id)
