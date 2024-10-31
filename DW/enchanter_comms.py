import copy
from emoji import emojize
from random import randint, random
import bot

class EnchanterComms:
    '''

    '''
    def __init__(self, server):
        '''
            Ele carrega o server, o keyboard padrão, o tempo padrão de espera, que é 1 minuto, o bot pra mandar mensagens, e o único comando, que é o /deep_forest.

        '''
        self.server = server
        self.defkb = server.defkb           # Keyboard padrão
        self.ynkb = server.keyboards.bs_reply_markup
        self.def_wait_time = 60
        self.bot = bot.TGBot()
        # self.ench_probs = [1.0, 0.5, 0.25, 0.125]
        self.actions = {
        }
        self.internal = {
            "start_enchanter": self.start_enchanter
        }

    def calc_ench_prob(self, l):
        return 1/(2**l)

    def check_individual_player_eligibility(self, jog):
        if jog.armor:
            if "hot" in jog.armor.status_protection:
                if jog.armor.status_protection["hot"] >= 10:
                    text = "The enchanter tries to enchant your armor but fails, it is already at maximum power."

                    #return False
                else:
                    suc_rate = self.calc_ench_prob(jog.armor.status_protection["hot"])
                    if random() < suc_rate:
                        jog.armor.name = jog.armor.name.split(emojize(f"+{jog.armor.status_protection['hot']}:high_voltage:"))[0] + emojize(f"+{jog.armor.status_protection['hot']+1}:high_voltage:")
                        jog.armor.status_protection["hot"] += 1
                        text = f"The enchanter touches your armor and suddenly you feel cooler, you feel better now. Success rate: {suc_rate*100:.3f}%"
                    else:
                        text = f"The enchanter tries to enchant your armor but fails. Success rate: {suc_rate*100:.3f}%"
            else:
                jog.armor.status_protection["hot"] = 1
                jog.armor.name += emojize(" +1:high_voltage:️")
                text="The enchanter touches your armor and suddenly you feel cooler, you feel better now. Succes rate: 100%"
        else:
            text = f"The enchanter could not enchant your clothes, you must wear better armor."
        self.server.bot.send_message(text=text, chat_id= jog.chat_id, reply_markup=self.defkb, parse_mode='MARKDOWN')

    def start_enchanter(self, caller, caller_id = None, *args):
        if caller.pt_code:
            code = caller.pt_code
        else:
            code = caller.chat_id
        if not args:
            text = emojize(f"You see a tall man wearing robes and a hat :mage:‍:male_sign:. You approach him and he *babbles words you can't understand*. By making a confused face, the wizard understands that he speaks a different language than you. He points a finger into his chest and then waves his hands indicating that he comes from a far away land. He points at your clothes and gestures that he could improve them. Will you accept?")

            if code[0] == "/":
                self.server.bot.send_message(text=text, chat_id= caller.chat_ids, reply_markup=self.ynkb, parse_mode='MARKDOWN')
                return self.def_wait_time*5
            else:
                self.server.bot.send_message(text=text, chat_id= caller.chat_id, reply_markup=self.ynkb, parse_mode='MARKDOWN')
                return self.def_wait_time*5+caller.suc_refs*60

        else:
            if args[-1] == emojize("YES :thumbs_up:"):
                if code[0] == "/":
                    for c_id in caller.chat_ids:
                        self.check_individual_player_eligibility(self.server.playersdb.players_and_parties[c_id])
                else:
                    self.check_individual_player_eligibility(caller)
                return False
            elif args[-1] == emojize("NOPE :thumbs_down:"):
                text = "The enchanter and you part ways. He disappears in the forest while you follow your own path."
                if code[0] == "/":
                    self.server.bot.send_message(text=text, chat_id= caller.chat_ids, reply_markup=self.defkb, parse_mode='MARKDOWN')
                else:
                    self.server.bot.send_message(text=text, chat_id= caller.chat_id, reply_markup=self.defkb, parse_mode='MARKDOWN')
                return False
            else:
                text = f"That is a very cringe situation, you just need to to point your thumb up or down."
                if code[0] == "/":
                    self.server.bot.send_message(text=text, chat_id= caller.chat_ids, reply_markup=self.ynkb, parse_mode='MARKDOWN')
                    return self.def_wait_time*5
                else:
                    self.server.bot.send_message(text=text, chat_id= caller.chat_id, reply_markup=self.ynkb, parse_mode='MARKDOWN')
                    return self.def_wait_time*5+caller.suc_refs*60

    def to(self, chat_id):
        text = f"After some minutes of *AWKWARD* starring, the enchanter, scared, runs into the forest."
        self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb, parse_mode="MARKDOWN")
