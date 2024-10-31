from emoji import emojize
from emoji import demojize
import bot
import items
import player
import time

class ForestComms:
    '''
        O único comando em forest é o próprio "/forest"

        A partir dele, podem ter vários argumentos. Como se quer voltar ou não ou quantas horas vc quer ficar lá.

    '''
    def __init__(self, server):
        '''
            Ele carrega o server, o keyboard padrão, o tempo padrão de espera, que é 1 minuto, o bot pra mandar mensagens, e o único comando, que é o forest.

        '''
        self.server = server
        self.defkb = server.defkb           # Keyboard padrão
        self.def_wait_time = 60
        self.bot = bot.TGBot()
        self.actions = {
            emojize(":deciduous_tree: Forest :deciduous_tree:"): self.forest,
            "/forest": self.forest
        }
        self.internal = {

        }

    def forest(self, caller, *args):
        '''
            Comando executado quando o jogador da um "/forest"
        '''
        self.server.woods.process()         # Toda vez que este comando for chamado, ele irá processar as florestas.
        self.server.deep_forest_manager.process()
        if caller.location == "arena":
            text = "You are battling in the arena now, to enter the forest please finish your fight."
            self.bot.send_message(text=text, chat_id=caller.chat_id)
            return False

        if not args:
# -------------------------- Is not at forest ----------------------------------
            if caller.code not in self.server.woods.players:
                text = emojize("There are many resources available for those who dare venture into the hungry woods... however, the forest :deciduous_tree: will not remain passive at your intrusion. How long will you stay?")
                self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.time_reply_markup)
                return self.def_wait_time

# -------------------------- Is at forest --------------------------------------
            else:
                remtime = int(self.server.woods.players[caller.code]["rem_time"]/60)
                hours, minutes = divmod(remtime, 60)            # Calcula o tempo que falta pra voltar da floresta em minutos e com isto, calcula os minutos e horas restantes
                if hours != 0:
                    text = f"You'll return in {hours} hours and {minutes} minutes. Should you head back early?"
                else:
                    text = f"You'll return in {minutes} minutes. Should you head back early?"
                self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.forest_return_reply_markup)
                return self.def_wait_time

        else:
# ------------------------- Is not at forest -----------------------------------

            if not caller.code in self.server.woods.players:
                time_s = args[-1]
# -------------- Choices from entering the forest ------------------------------
                if time_s == "Back":
                    text = "You decided to step back and remain in the camp."
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

                else:
                    time2 = 3600
                    if time_s == "1 hour":
                        pass
                    elif time_s == "4 hours":
                        time2 = time2*4
                    elif time_s == "8 hours":
                        time2 = time2*8
                    elif time_s == "12 hours":
                        time2 = time2 * 12
                    else:


                        text = "This is not a valid time. Choose again!"
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.time_reply_markup)
                        return self.def_wait_time*5

                    timeh = int(time2/3600)

                    if caller.pt_code:
                        chat_ids = self.server.playersdb.players_and_parties[caller.pt_code].chat_ids
                        self.server.woods.add_to_woods(self.server.playersdb.players_and_parties[caller.pt_code], time2)     # Neste caso, ele adicona a party à floresta ao invés do objeto jogador
                        text = (f"You prepared for a {timeh} hour trip. Maybe your party finds something useful in that time.")
                        self.bot.send_message(text = text, chat_id = chat_ids, reply_markup = self.defkb)      # Neste caso, ele amnda a mensagem pra td mundo na party

                    else:
                        self.server.woods.add_to_woods(self.server.playersdb.players_and_parties[caller.chat_id], time2)
                        text = (f"You prepared for a {timeh} hour trip. Maybe you'll find something useful in that time.")
                        self.bot.send_message(text = text, chat_id = caller.chat_id, reply_markup = self.defkb)

# ------------------- retrace after death --------------------------------------
                    if caller.has_died:                 # Checa se o jogador morreu para ele poder dar retrace nos seus itens dropados.

                        text = emojize(f"As you struggle to regain your bearings after death, you notice "
                                        f"some familiar tracks coming out from the bushes: paw prints :paw_prints: "
                                        f"resembling a dog's paws are said to belong to Alileb, the guardian "
                                        f"spirit. She must have dragged your mercilessly beaten body "
                                        f"through here. The lingering regrets from your past life leave you "
                                        f"restless. Will you retrace her steps and attempt to reclaim what "
                                        f"you've lost? Or will you accept the fresh start you've been given?")

                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.retrace_steps_markup)
                        return self.def_wait_time*5

                return False

# ----------------- Is at the forest -------------------------------------------
            else:

                if args[-1] == "yes":               # Ele tinha perguntado se fica ou não na floresta
                    was_travelling_text = ""
                    if caller.is_travelling:
                        text = "You decided to stop your journey."
                        self.server.travelman.cancel_travel(self.server.playersdb.players_and_parties[caller.code])

                    remtime = self.server.woods.players[caller.code]["rem_time"]     # calcula o tempo q falta pra voltar
                    remtime2 = remtime
                    if remtime > self.server.woods.trip_time:
                        remtime2 = self.server.woods.trip_time
                    if remtime > self.server.woods.players[caller.code]["stay_time"] - self.server.woods.trip_time:
                        remtime2 = self.server.woods.players[caller.code]["stay_time"] - remtime

                    self.server.woods.players[caller.code]["rem_time"] = remtime2

                    remtime2 = int(remtime2/60)
                    if caller.pt_code:
                        chat_ids = self.server.playersdb.players_and_parties[caller.pt_code].chat_ids
                        if was_travelling_text:
                            self.bot.send_message(text=was_travelling_text, chat_id=chat_ids, reply_markup=self.defkb)
                        text = f"Your party will be back in {remtime2} minutes"
                        self.bot.send_message(text=text, chat_id= chat_ids, reply_markup=self.defkb)
                    else:
                        if was_travelling_text:
                            self.bot.send_message(text=was_travelling_text, chat_id=chat_ids, reply_markup=self.defkb)
                        text = f"You will be back in {remtime2} minutes"
                        self.bot.send_message(text=text, chat_id= caller.chat_id, reply_markup=self.defkb)

                    return False

                elif args[-1] == "no":
                    text = "You decide to stay in the forest a little longer."
                    self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                    return False

                elif caller.has_died:       # Se o jogador acabou de morrer, então o bot está esperando ele responder se irá dar retrace ou não.

                    if args[-1] == emojize(":paw_prints: Retrace steps :paw_prints:"):

                        text = emojize(f"Alas, unable to let go of your past achievements and riches, you take a detour to find your body.")
                        caller.has_died = False
                        self.server.travelman.set_travel(caller, "death_site")
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                        return False
                    elif args[-1] == emojize('Give it up'):
                        caller.has_died = False
                        text = emojize(f"You decide that those material goods weren't really what mattered. "
                                        f"You've got friends to adventure with and a newly unburdened heart. "
                                        f"You're happy now.\n\n"
                                        f"Your old tracks are left behind, never to be seen again. "
                                        )
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.defkb)
                        return False
                    else:
                        text = emojize("After a while thinking about your past life, the horror of your death comes to your mind "
                                        "making you start to spout nonsense shouts. Starting to regain some sanity, the paw prints "
                                        "reminds you of the difficult choice of seeing your splendid poor corpse.")
                        self.bot.send_message(text=text, chat_id=caller.chat_id, reply_markup=self.server.keyboards.retrace_steps_markup)
                        return self.def_wait_time*5

        return False


    def to(self, chat_id):
        pass

    def to2(self, chat_id):
        if chat_id[0] == "/":
            if chat_id in self.server.playersdb.players_and_parties:
                text = "It's a dangerous place, so your party decided to step back."
                chat_ids = self.server.playersdb.players_and_parties[chat_id].chat_ids
                self.bot.send_message(text=text, chat_id=chat_ids, reply_markup=self.defkb)
        else:

            text = "It's a dangerous place, so you decided to step back."
            self.bot.send_message(text=text, chat_id=chat_id, reply_markup=self.defkb)
