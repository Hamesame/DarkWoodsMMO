from emoji import emojize

class Talisman:
    def __init__(self):
        self.code = ""
        self.name = ""
        self.rarity = 0
        self.description = ""
        self.powers = {}

    def __str__(self):
        rarity = [
            emojize(":zzz:"),
            emojize(":pile_of_poo:"),
            emojize(":OK_hand:"),
            emojize(":flexed_biceps:"),
            emojize(":angry_face_with_horns:"),
            emojize(":smiling_face_with_halo:"),
            emojize(":bright_button:"),
        ]
        return f"|{rarity[self.rarity]}| {self.name}"

    def generate_description(self):
        rarity = [          emojize(":zzz: Natural :zzz:"),
                            emojize(":pile_of_poo: Slightly :pile_of_poo:"),
                            emojize(":OK_hand: Normally :OK_hand:"),
                            emojize(":flexed_biceps: Strongly :flexed_biceps:"),
                            emojize(":angry_face_with_horns: Satanic :angry_face_with_horns:"),
                            emojize(":smiling_face_with_halo: Godly :smiling_face_with_halo:"),
                            emojize(":bright_button: Cosmic :bright_button:")]
        text = emojize( f"{self}\n\n"
                        f"Rarity: {rarity[self.rarity]}\n"
                        f"Description: {self.description}\n\n"
                        f"Effects:\n"
                        )
        for ef,power in self.powers.items():
            text += f"{ef}: {power}\n"
        return text


class Talismandb:
    def __init__(self):
        self.talismans = {}
        self.generate()

    def generate(self):
        new_t = Talisman()
        new_t.code = "fur"
        new_t.name = emojize("Fur")
        new_t.description = "Some fur of some beast, some says it makes you feel stronger if used in a weapon."
        new_t.rarity = 0
        new_t.powers["boost str"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "eye"
        new_t.name = emojize("Eye :eye:")
        new_t.description = "This works as a third eye making you feel more perceptive of your surroundings."
        new_t.rarity = 0
        new_t.powers["boost dex"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "insect_brain"
        new_t.name = emojize("Insect Brains :brain:")
        new_t.description = "It somehow connects yourself to your weapon if its crafted with it, helping you think."
        new_t.rarity = 0
        new_t.powers["boost int"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "wolf_blood"
        new_t.name = emojize("Wolf Blood")
        new_t.description = "Imbuing your weapon with this blood you will gain regenerative habilites."
        new_t.rarity = 1
        new_t.powers["life steal"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "feather"
        new_t.name = emojize("Feather")
        new_t.description = "Makes weapons you wield more lightwheight. Making it easier to evade attacks."
        new_t.rarity = 1
        new_t.powers["boost dex"] = 1
        new_t.powers["wep damage"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "claw"
        new_t.name = emojize("Claw")
        new_t.description = "Its presense frightens your foes. Increased weapon damage."
        new_t.rarity = 1
        new_t.powers["wep damage"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "chitin"
        new_t.name = emojize("Chitin")
        new_t.description = "Extremely resistant and light."
        new_t.rarity = 1
        new_t.powers["wep defense"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "gelatine"
        new_t.name = emojize("Gelatine :custard:")
        new_t.description = "Bouncy."
        new_t.rarity = 1
        new_t.powers["wep defense"] = 1
        new_t.powers["boost str"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "ice_shards"
        new_t.name = emojize("Ice Shards :snowflake:️")
        new_t.description = "It looks like ice but doesn't melt."
        new_t.rarity = 1
        new_t.powers["wep damage"] = 1
        new_t.powers["boost dex"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "dark_aura"
        new_t.name = emojize("Dark Aura")
        new_t.description = "You can't see it. It lacks light."
        new_t.rarity = 1
        new_t.powers["boost int"] = 1
        new_t.powers["boost dex"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "essence"
        new_t.name = emojize("Essence")
        new_t.description = "You can't hold it in your hands, you just feel it."
        new_t.rarity = 2
        new_t.powers["life steal"] = 1
        new_t.powers["boost dex"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "ligninite"
        new_t.name = emojize("Ligninite")
        new_t.description = "A piece of wood as hard as iron."
        new_t.rarity = 2
        new_t.powers["wep damage"] = 1
        new_t.powers["wep defense"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "leather"
        new_t.name = emojize("Leather")
        new_t.description = "Can be used to craft armor, but also makes you feel stronger."
        new_t.rarity = 1
        new_t.powers["wep defense"] = 1
        new_t.powers["boost str"] = 1
        self.talismans[new_t.code] = new_t


        new_t = Talisman()
        new_t.code = "dragon_eye"
        new_t.name = emojize("Dragon :dragon_face: eye :eye:")
        new_t.description = "This works as a third eye making you feel more perceptive of your surroundings. Also its presence heats the blade."
        new_t.rarity = 2
        new_t.powers["boost dex"] = 1
        new_t.powers["fire"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "dragon_claw"
        new_t.name = emojize("Dragon :dragon_face: claw")
        new_t.description = "Increase weapon stats. Also makes your weapon balanced to attack stats."
        new_t.rarity = 3
        new_t.powers["wep defense"] = 2
        new_t.powers["wep damage"] = 2
        new_t.powers["rebalance attack"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "dragon_scale"
        new_t.name = emojize("Dragon :dragon_face: scale")
        new_t.description = "Increase weapon stats. Also makes your weapon balanced to defensive stats."
        new_t.rarity = 3
        new_t.powers["wep defense"] = 2
        new_t.powers["wep damage"] = 2
        new_t.powers["rebalance defense"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "dragon_heart"
        new_t.name = emojize("Dragon :dragon_face: heart")
        new_t.description = "Increase weapon stats. Also set your enemies on fire."
        new_t.rarity = 4
        new_t.powers["wep defense"] = 3
        new_t.powers["wep damage"] = 3
        new_t.powers["fire"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "cobweb"
        new_t.name = emojize("Cobweb :spider_web:")
        new_t.description = "Increase weapon defense."
        new_t.rarity = 1
        new_t.powers["wep defense"] = 2
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "venom_gland"
        new_t.name = emojize("Venom Gland")
        new_t.description = "Adds posion effect to your weapon."
        new_t.rarity = 2
        new_t.powers["poison"] = 2
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "silk_gland"
        new_t.name = emojize("Silk :spider_web: gland")
        new_t.description = "Throws webs at you opponents. (increased defense and aatack)"
        new_t.rarity = 3
        new_t.powers["wep damage"] = 4
        new_t.powers["wep defense"] = 4
        self.talismans[new_t.code] = new_t


        new_t = Talisman()
        new_t.code = "spider_brain"
        new_t.name = emojize("Spider brain :brain:")
        new_t.description = "A super computer that operates as a second brain for you. Careful to not let it control you."
        new_t.rarity = 4
        new_t.powers["boost int"] = 4
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "hydra_eye"
        new_t.name = emojize("Hydra eye :eye:")
        new_t.description = "This works as a third eye making you feel more perceptive of your surroundings. Can heal you."
        new_t.rarity = 2
        new_t.powers["boost dex"] = 1
        new_t.powers["life steal"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "hydra_blood"
        new_t.name = emojize("Hydra blood")
        new_t.description = "A blood that is always warm. It heals its user and also poisonous to your enemies."
        new_t.rarity = 3
        new_t.powers["fire"] = 1
        new_t.powers["life steal"] = 2
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "hydra_claw"
        new_t.name = emojize("Hydra claw")
        new_t.description = "A poisonous claw that increases you weapon attack and heals you."
        new_t.rarity = 3
        new_t.powers["poison"] = 1
        new_t.powers["life steal"] = 1
        new_t.powers["wep damage"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "hydra_heart"
        new_t.name = emojize("Hydra heart")
        new_t.description = "A pulsating immortal organ. Can save you from death once."
        new_t.rarity = 4
        new_t.powers["death evasion"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "hard_chitin"
        new_t.name = emojize("Hard chitin")
        new_t.description = "Extremely resistant."
        new_t.rarity = 2
        new_t.powers["wep defense"] = 2
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "repugnatorial_glands"
        new_t.name = emojize("Repugnatorial glands")
        new_t.description = "A gland that is used as a defense mechanism that expels repugnant substances."
        new_t.rarity = 2
        new_t.powers["poison"] = 2
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "antennae"
        new_t.name = emojize("Antennae")
        new_t.description = "It senses its surroundings"
        new_t.rarity = 4
        new_t.powers["boost dex"] = 4
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "giant_snake_louse_brain"
        new_t.name = emojize("Giant :bug: Snake Louse :brain:")
        new_t.description = "You need a gigantic brain to coodenate 200 limbs."
        new_t.rarity = 4
        new_t.powers["boost dex"] = 4
        new_t.powers["boost int"] = 6
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "giant_snake_louse_heart"
        new_t.name = emojize("Giant :bug: Snake Louse heart")
        new_t.description = "An extremelly long and muscular :eyes: organ Boosts your strength."
        new_t.rarity = 4
        new_t.powers["boost str"] = 4
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "giant_centipede_brain"
        new_t.name = emojize("Giant :bug: centipede brain :brain:")
        new_t.description = "You need a somewhat big brain to coodenate 30 limbs."
        new_t.rarity = 3
        new_t.powers["boost dex"] = 3
        new_t.powers["boost int"] = 5
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "giant_centipede_heart"
        new_t.name = emojize("Giant :bug: centipede heart")
        new_t.description = "An extremelly long and muscular :eyes: organ Boosts your strength."
        new_t.rarity = 4
        new_t.powers["boost str"] = 4
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "fire_core"
        new_t.name = emojize("Fire Core :red_heart:️‍:fire:")
        new_t.description = "Increase weapon attack and your strength. Also set your enemies on fire."
        new_t.rarity = 1
        new_t.powers["wep damage"] = 1
        new_t.powers["boost str"] = 1
        new_t.powers["fire"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "sunflower_seed"
        new_t.name = emojize("Sunflower Seed :sunflower:")
        new_t.description = "A glowing seed that radiates power."
        new_t.rarity = 4
        new_t.powers["boost str"] = 4
        new_t.powers["boost int"] = 4
        new_t.powers["boost dex"] = 4
        new_t.powers["poison"] = 3
        new_t.powers["wep defense"] = 8
        new_t.powers["wep damage"] = 8
        new_t.powers["life steal"] = 3
        new_t.powers["fire"] = 3
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "helios_puzzle"
        new_t.name = emojize("Helio's Puzzle :sun::bright_button::sun:")
        new_t.description = "A strange glowing artifact."
        new_t.rarity = 1
        new_t.powers["boost str"] = 1
        new_t.powers["boost int"] = 1
        new_t.powers["boost dex"] = 1
        new_t.powers["poison"] = 1
        new_t.powers["wep defense"] = 1
        new_t.powers["wep damage"] = 1
        new_t.powers["life steal"] = 1
        new_t.powers["fire"] = 1
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "helianth_petal"
        new_t.name = emojize("Sunflower Petal :sunflower:")
        new_t.description = "A glowing fragment that radiates power."
        new_t.rarity = 6
        new_t.powers["boost str"] = 10
        new_t.powers["boost int"] = 10
        new_t.powers["boost dex"] = 10
        new_t.powers["poison"] = 5
        new_t.powers["wep defense"] = 20
        new_t.powers["wep damage"] = 20
        new_t.powers["life steal"] = 5
        new_t.powers["fire"] = 5
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "reverse_entropy_shard"
        new_t.name = emojize("Glowing Shard")
        new_t.description = "It glows from heat but is freezing to the touch. Disclaimer: The second law of thermodynamics does not apply to the Dark Woods."
        new_t.rarity = 6
        new_t.powers["boost int"] = 30
        new_t.powers["wep damage"] = 40
        new_t.powers["life steal"] = 5
        new_t.powers["fire"] = 10
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "cosmic_gift"
        new_t.name = emojize("Cçuemyülfha :bright_button::squid::sparkles:")
        new_t.description = emojize("A gift from the otherworld for solving the Alien Puzzle :alien_monster:.")
        new_t.rarity = 6
        new_t.powers["boost int"] = 15
        new_t.powers["boost dex"] = 15
        new_t.powers["wep defense"] = 15
        new_t.powers["life steal"] = 4
        new_t.powers["poison"] = 6
        self.talismans[new_t.code] = new_t

        new_t = Talisman()
        new_t.code = "true_cosmic_gift"
        new_t.name = emojize("Aẽeréćlĝle :eye:‍:left_speech_bubble::cyclone::alien_monster:")
        new_t.description = emojize("A gift from the otherworld for truly solving the Alien Puzzle :alien_monster:.")
        new_t.rarity = 6
        new_t.powers["boost int"] = 27
        new_t.powers["boost dex"] = 27
        new_t.powers["wep defense"] = 17
        new_t.powers["life steal"] = 7
        new_t.powers["poison"] = 7
        self.talismans[new_t.code] = new_t
