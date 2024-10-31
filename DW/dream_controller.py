import random
import pandas as pd
from time import time
import json

class Dream:

    def __init__(self, server):
            self.server = server
            self.last_process = time() - 60*60
            self.delta_t = 60*60
            self.recurrent_dreams = [
                "I'm in a gigantic library divided into hexagonal chambers. I picked one of the books from a random shelf. I could not understand anything as if the characters printed were random",
                "I dreamt that i was persuing some sort of demon in an abandoned building construction site. It would be used for some sort of ancient communication. There I found a wallet in the middle of nowhere. The identity card reads: +uahupb8HookzMmVh.",
                "We were playing hide and seek on a parking lot. It was my turn. I first looked at the section V and found one of my friends at the 9th spot. I could not find the others and the dream changed and i was not looking for my friends anymore, i was persuing a demon, could not find it.",
                "I was driving my car on a wavy road during a rain. At the kilometer 43, I saw a P sign. Not knowing what it could mean, i continued driving until my car started to burn. But i was felling a cold breeze instead.",
                "Playing my old games, i became one of my favorite characters, the S-03 Mecha and I started chasing some aliens. Could never get closer.",
                "My dream was about climbing. I was hiking with Walter. He got ahead of me, to catch up, i started to climb a cliff. At the top I saw two birds eating the corpse of my friend.",
                "We were sitting on a round table on top of a tower. However, i could not understand a single word, as if each different person were to speak a different language. I doubt if they were understanding each other. In front of me is a book opened at Genesis 11:1–9.",

                ]
            self.save_file = 'dbs\dreamers.json'
            self.d_ids = self.load()

    def process_dreams(self):
        if time() > self.last_process + self.delta_t:
            print("Processign dreams...")
            dream_messages = self.server.bot.get_messages_dict_dream(timeout=2)
            self.process_messages(dream_messages)
            dreams = pd.read_csv("clean_dreams.csv")
            for chat in self.d_ids:
                try:
                    if random.random() < 0.4:

                        # Recurrent dream
                        d = random.choice(self.recurrent_dreams)
                        self.server.bot.send_dream_message(text=d, chat_id=chat)
                    else:
                        # Random dream
                        d = random.choice(dreams['cleaned_text'])
                        self.server.bot.send_dream_message(text=d, chat_id=chat)
                except:
                    pass

            self.last_process = time()
            print("Finished processign dreams...")

    def process_messages(self, messages):
        changed = False
        for chat_id, msgs in messages.items():
            if not chat_id in self.d_ids:
                self.d_ids.append(chat_id)
                changed = True
        if changed:
            self.save()

    def save(self):
        to_s_dic = {"dreamers": self.d_ids}
        with open(self.save_file, 'w') as f:
            json.dump(to_s_dic, f)

    def load(self):
        try:
            f = open(self.save_file)
            dic = json.load(f)
            self.d_ids = dic['dreamers']
            f.close()
        except:
            self.d_ids = []
        return self.d_ids

