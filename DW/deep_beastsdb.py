from emoji import emojize
import copy

class DeepBeast:
    def __init__(self):
        self.name = "blob"
        self.powers = {}
        self.stats = 300
        self.drop = {"nothing": 40}

class Megabeast:
    def __init__(self):
        self.name = "blob"
        self.limbs = {}
        self.original_limb = {}
        self.habilities = {}
        self.attack = 10
        self.traces = "scratches on the trees and remains of green scales on the grounds."
        self.drop = {"nothing": 100}
        self.is_legendary = False

    def take_damage(self, target):
        if self.limbs[target] > 0:
            self.limbs[target] -= 1
        return self.limbs[target]

    def select_live_limb(self):
        for limb,health in self.limbs.items():
            if health > 0:
                return limb
        return -1


class DeepBeastsdb:
    def __init__(self):
        self.beasts = []
        self.night_beasts = []
        self.megabeasts = []
        self.create_base()
        self.create_mega()

    def create_base(self):
        new_beast = DeepBeast()
        new_beast.name = "Forest stalker"
        new_beast.drop["fur"] = 5
        new_beast.drop["eye"] = 2
        self.beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = "Werewolf"
        new_beast.powers["life steal"] = 1
        new_beast.drop["fur"] = 5
        new_beast.drop["wolf_blood"] = 2
        self.beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = "Gryphon"
        new_beast.powers["evasion"] = 1
        new_beast.drop["feather"] = 5
        new_beast.drop["claw"] = 2
        self.beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = "Beetle Man"
        new_beast.powers["hard_skin"] = 1
        new_beast.drop["chitin"] = 5
        new_beast.drop["insect_brain"] = 5
        self.beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Slime :custard:")
        new_beast.powers["hard_skin"] = 1
        new_beast.powers["evasion"] = 1
        new_beast.drop["gelatine"] = 4
        self.beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Elder tree ent :evergreen_tree:")
        new_beast.powers["hard_skin"] = 2
        new_beast.drop["ligninite"] = 4
        self.beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = "Whispers"
        new_beast.powers["life steal"] = 2
        new_beast.drop["essence"] = 4
        self.beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = "Lurking shadow"
        new_beast.powers["life steal"] = 1
        new_beast.powers["evasion"] = 1
        new_beast.drop["ligninite"] = 4
        self.beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Fat :hamburger: Cow")
        new_beast.powers["hard_skin"] = 2
        new_beast.drop["leather"] = 4
        self.beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Fire Elemental")
        new_beast.powers["evasion"] = 2
        new_beast.drop["fire_core"] = 2
        self.beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Solar Cult Fanatic")
        new_beast.powers["life steal"] = 1
        new_beast.drop["fire_core"] = 1
        new_beast.drop["dark_aura"] = 1
        self.beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Fire Gryphon")
        new_beast.powers["evasion"] = 3
        new_beast.drop["fire_core"] = 2
        new_beast.drop["dark_aura"] = 1
        self.beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Phoenix")
        new_beast.powers["evasion"] = 4
        new_beast.powers["life steal"] = 2
        new_beast.drop["fire_core"] = 2
        new_beast.drop["essence"] = 1
        self.beasts.append(new_beast)

        # Specials

        # new_beast = DeepBeast()
        # new_beast.name = emojize("Ice Slime :custard: :snowflake:")
        # new_beast.powers["hard_skin"] = 1
        # new_beast.powers["life steal"] = 1
        # new_beast.powers["evasion"] = 1
        # new_beast.drop["gelatine"] = 3
        # new_beast.drop["ice_shards"] = 3
        # self.beasts.append(new_beast)

        # new_beast = DeepBeast()
        # new_beast.name = emojize("Frost :snowflake: Troll")
        # new_beast.powers["hard_skin"] = 1
        # new_beast.powers["life steal"] = 1
        # new_beast.powers["evasion"] = 1
        # new_beast.drop["fur"] = 3
        # new_beast.drop["ice_shards"] = 3
        # self.beasts.append(new_beast)

        # Night

        new_beast = DeepBeast()
        new_beast.name = emojize("Áillen :musical_note::fire:")
        new_beast.powers["hard_skin"] = 1
        new_beast.powers["life steal"] = 2
        new_beast.powers["evasion"] = 3
        new_beast.drop["dark_aura"] = 1
        new_beast.drop["essence"] = 1
        self.night_beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Dullahan :face_with_head-bandage::horse_face:")
        new_beast.powers["hard_skin"] = 1
        new_beast.powers["life steal"] = 2
        new_beast.drop["eye"] = 1
        new_beast.drop["essence"] = 1
        self.night_beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Ellén Trechend :fire::ogre::ogre::ogre:")
        new_beast.powers["hard_skin"] = 2
        new_beast.drop["eye"] = 3
        new_beast.drop["dark_aura"] = 1
        new_beast.drop["essence"] = 1
        self.night_beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Fachen :elephant:")
        new_beast.powers["hard_skin"] = 3
        new_beast.drop["eye"] = 1
        new_beast.drop["essence"] = 1
        new_beast.drop["dark_aura"] = 1
        self.night_beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Fear gorta :hamburger:")
        new_beast.powers["hard_skin"] = 3
        new_beast.powers["life steal"] = 3
        new_beast.drop["eye"] = 2
        new_beast.drop["dark_aura"] = 1
        new_beast.drop["essence"] = 1
        self.night_beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Am Fear Liath Mòr :snow-capped_mountain:")
        new_beast.powers["hard_skin"] = 3
        new_beast.drop["eye"] = 2
        new_beast.drop["dark_aura"] = 1
        new_beast.drop["essence"] = 1
        self.night_beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Púca")
        new_beast.powers["hard_skin"] = 1
        new_beast.powers["life steal"] = 2
        new_beast.powers["evasion"] = 3
        new_beast.drop["dark_aura"] = 1
        new_beast.drop["essence"] = 1
        self.night_beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("The Morrígan :bird:‍:black_large_square:️")
        new_beast.powers["life steal"] = 3
        new_beast.powers["evasion"] = 3
        new_beast.drop["dark_aura"] = 2
        new_beast.drop["essence"] = 1
        self.night_beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("Wicker Man :red_heart:️‍:fire:")
        new_beast.powers["evasion"] = 3
        new_beast.drop["dragon_heart"] = 1
        new_beast.drop["essence"] = 1
        self.night_beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize("John Barleycorn :sheaf_of_rice:")
        new_beast.powers["life steal"] = 3
        new_beast.powers["evasion"] = 3
        new_beast.drop["dragon_heart"] = 1
        new_beast.drop["essence"] = 1
        self.night_beasts.append(new_beast)

        new_beast = DeepBeast()
        new_beast.name = emojize(":ghost: Sílvio")
        new_beast.powers["evasion"] = 1
        new_beast.drop["essence"] = 1
        self.night_beasts.append(new_beast)

        #new_beast = DeepBeast()
        #new_beast.name = emojize(":skull_and_crossbones: ️Dark Santa :snowflake:")
        #new_beast.powers["hard_skin"] = 3
        #new_beast.powers["life steal"] = 2
        #new_beast.powers["evasion"] = 1
        #new_beast.drop["ice_shards"] = 3
        #new_beast.drop["fur"] = 5
        #new_beast.drop["eye"] = 2
        #new_beast.drop["claw"] = 2
        #new_beast.drop["essence"] = 4
        #new_beast.drop["dark_aura"] = 1
        #new_beast.drop["reverse_entropy_shard"] = 1
        #self.beasts.append(new_beast)

        #new_beast = DeepBeast()
        #new_beast.name = emojize("Normal Santa :Santa_Claus:")
        #new_beast.powers["hard_skin"] = 1
        #new_beast.powers["life steal"] = 1
        #new_beast.powers["evasion"] = 1
        #new_beast.drop["ice_shards"] = 1
        #new_beast.drop["fur"] = 1
        #new_beast.drop["eye"] = 1
        #new_beast.drop["claw"] = 1
        #new_beast.drop["essence"] = 1
        #self.beasts.append(new_beast)

        #new_beast = DeepBeast()
        #new_beast.name = emojize("Corrupted Elf :goblin:")
        #new_beast.powers["life steal"] = 1
        #new_beast.powers["evasion"] = 1
        #new_beast.drop["ice_shards"] = 1
        #new_beast.drop["fur"] = 1
        #new_beast.drop["eye"] = 1
        #new_beast.drop["claw"] = 1
        #new_beast.drop["dark_aura"] = 1
        #self.beasts.append(new_beast)

    def create_mega(self):
        new_mega = Megabeast()
        new_mega.name = emojize("Dragon :dragon_face: Hatchling")
        new_mega.traces = "ash traces"
        new_mega.limbs = {
            "Head": 3,
            "Body": 3,
            "Tail": 3,
            "Left wing": 3,
            "Right wing": 3,
            "Front left paw": 3,
            "Front right paw": 3,
            "Back left paw": 3,
            "Back righ paw": 3,
        }
        new_mega.original_limb = {
            "Head": 1,
            "Body": 1,
            "Tail": 1,
            "Left wing": 1,
            "Right wing": 1,
            "Front left paw": 1,
            "Front right paw": 1,
            "Back left paw": 1,
            "Back righ paw": 1,
        }
        new_mega.habilities = {
            "Head": "perception",
            "Body": "None",
            "Tail": "damage",
            "Left wing": "fight",
            "Right wing": "fight",
            "Front left paw": "standing",
            "Front right paw": "standing",
            "Back left paw": "standing",
            "Back righ paw": "standing",
        }
        new_mega.attack = 2
        new_mega.drop["dragon_eye"] = 10
        new_mega.drop["dragon_claw"] = 10
        new_mega.drop["dragon_scale"] = 10
        new_mega.drop["dragon_heart"] = 2
        self.megabeasts.append(new_mega)

        new_mega = Megabeast()
        new_mega.name = emojize("Dragon :dragon_face: Adult")
        new_mega.traces = "burnt leaves traces"
        new_mega.limbs = {
            "Head": 4,
            "Body": 4,
            "Tail": 4,
            "Left wing": 4,
            "Right wing": 4,
            "Front left paw": 4,
            "Front right paw": 4,
            "Back left paw": 4,
            "Back righ paw": 4,
        }
        new_mega.original_limb = {
            "Head": 2,
            "Body": 2,
            "Tail": 2,
            "Left wing": 2,
            "Right wing": 2,
            "Front left paw": 2,
            "Front right paw": 2,
            "Back left paw": 2,
            "Back righ paw": 2,
        }
        new_mega.habilities = {
            "Head": "perception",
            "Body": "None",
            "Tail": "damage",
            "Left wing": "fight",
            "Right wing": "fight",
            "Front left paw": "standing",
            "Front right paw": "standing",
            "Back left paw": "standing",
            "Back righ paw": "standing",
        }
        new_mega.attack = 3
        new_mega.drop["dragon_eye"] = 20
        new_mega.drop["dragon_claw"] = 20
        new_mega.drop["dragon_scale"] = 20
        new_mega.drop["dragon_heart"] = 4
        self.megabeasts.append(new_mega)

        new_mega = Megabeast()
        new_mega.name = emojize("Dragon :dragon_face: Lord")
        new_mega.traces = "lacerated trees and a path with glowing firebrands"
        new_mega.limbs = {
            "Head": 5,
            "Body": 5,
            "Tail": 5,
            "Left wing": 5,
            "Right wing": 5,
            "Front left paw": 5,
            "Front right paw": 5,
            "Back left paw": 5,
            "Back righ paw": 5,
        }
        new_mega.original_limb = {
            "Head": 3,
            "Body": 3,
            "Tail": 3,
            "Left wing": 3,
            "Right wing": 3,
            "Front left paw": 3,
            "Front right paw": 3,
            "Back left paw": 3,
            "Back righ paw": 3,
        }
        new_mega.habilities = {
            "Head": "perception",
            "Body": "None",
            "Tail": "damage",
            "Left wing": "fight",
            "Right wing": "fight",
            "Front left paw": "standing",
            "Front right paw": "standing",
            "Back left paw": "standing",
            "Back righ paw": "standing",
        }
        new_mega.attack = 4
        new_mega.drop["dragon_eye"] = 30
        new_mega.drop["dragon_claw"] = 30
        new_mega.drop["dragon_scale"] = 30
        new_mega.drop["dragon_heart"] = 5
        self.megabeasts.append(new_mega)

        new_mega = Megabeast()
        new_mega.name = emojize("Solar Dragon :bright_button::dragon_face::sun:")
        new_mega.traces = "burning trees with a magma river"
        new_mega.limbs = {
            "Head": 6,
            "Body": 6,
            "Tail": 6,
            "Left wing": 6,
            "Right wing": 6,
            "Front left paw": 6,
            "Front right paw": 6,
            "Back left paw": 6,
            "Back righ paw": 6,
        }
        new_mega.original_limb = {
            "Head": 4,
            "Body": 4,
            "Tail": 4,
            "Left wing": 4,
            "Right wing": 4,
            "Front left paw": 4,
            "Front right paw": 4,
            "Back left paw": 4,
            "Back righ paw": 4,
        }
        new_mega.habilities = {
            "Head": "perception",
            "Body": "None",
            "Tail": "damage",
            "Left wing": "fight",
            "Right wing": "fight",
            "Front left paw": "standing",
            "Front right paw": "standing",
            "Back left paw": "standing",
            "Back righ paw": "standing",
        }
        new_mega.attack = 5
        new_mega.drop["dragon_eye"] = 30
        new_mega.drop["dragon_claw"] = 30
        new_mega.drop["dragon_scale"] = 30
        new_mega.drop["dragon_heart"] = 5
        new_mega.drop["fire_core"] = 5
        new_mega.drop["sunflower_seed"] = 1
        self.megabeasts.append(new_mega)

        new_mega = Megabeast()
        new_mega.name = emojize("Spider :spider: Queen")
        new_mega.traces = emojize("many cobwebs :spider_web:")
        new_mega.limbs = {
            "Abdomen": 5,
            "Cephalothorax": 8,
            "Front left leg": 3,
            "Front right leg": 3,
            "Back left leg": 3,
            "Back righ leg": 3,
            "Center back left leg": 3,
            "Center back right leg": 3,
            "Center front left leg": 3,
            "Center front right leg": 3,
        }
        new_mega.original_limb = {
            "Abdomen": 2,
            "Cephalothorax": 3,
            "Front left leg": 1,
            "Front right leg": 1,
            "Back left leg": 1,
            "Back righ leg": 1,
            "Center back left leg": 1,
            "Center back right leg": 1,
            "Center front left leg": 1,
            "Center front right leg": 1,
        }
        new_mega.habilities = {
            "Abdomen": "perception",
            "Cephalothorax": "damage",
            "Front left leg": "standing",
            "Front right leg": "standing",
            "Back left leg": "standing",
            "Back righ leg": "standing",
            "Center back left leg": "standing",
            "Center back right leg": "standing",
            "Center front left leg": "standing",
            "Center front right leg": "standing",
        }
        new_mega.attack = 2
        new_mega.drop["cobweb"] = 50
        new_mega.drop["venom_gland"] = 10
        new_mega.drop["silk_gland"] = 5
        new_mega.drop["spider_brain"] = 5
        self.megabeasts.append(new_mega)

        new_mega = Megabeast()
        new_mega.name = emojize("Giant :bug: Snake Louse")
        new_mega.traces = "an open path with felled trees"
        new_mega.limbs["Head"] = 3
        for segment_number in range(100):
            new_mega.limbs[f"Left leg number {segment_number}"] = 1
            new_mega.limbs[f"Right leg number {segment_number}"] = 1
            new_mega.limbs[f"Body segment number {segment_number}"] = 3
        new_mega.original_limb = {}
        for segment_number in range(10):
            new_mega.original_limb[f"Left leg number {segment_number}"] = 1
            new_mega.original_limb[f"Right leg number {segment_number}"] = 1
            new_mega.original_limb[f"Body segment number {segment_number}"] = 3
        new_mega.habilities["Head"] = "perception"
        for segment_number in range(100):
            new_mega.habilities[f"Left leg number {segment_number}"] = "standing"
            new_mega.habilities[f"Right leg number {segment_number}"] = "standing"
            new_mega.habilities[f"Body segment number {segment_number}"] = "standing"
        new_mega.attack = 1
        new_mega.drop["hard_chitin"] = 50
        new_mega.drop["antennae"] = 10
        new_mega.drop["giant_snake_louse_brain"] = 5
        new_mega.drop["giant_snake_louse_heart"] = 5
        new_mega.drop["repugnatorial_glands"] = 50
        self.megabeasts.append(new_mega)

        new_mega = Megabeast()
        new_mega.name = emojize("Giant :bug: Centipede")
        new_mega.traces = "an open path with felled trees"
        new_mega.limbs["Head"] = 3
        for segment_number in range(15):
            new_mega.limbs[f"Left leg number {segment_number}"] = 3
            new_mega.limbs[f"Right leg number {segment_number}"] = 3
            new_mega.limbs[f"Body segment number {segment_number}"] = 3
        new_mega.original_limb = {}
        for segment_number in range(15):
            new_mega.original_limb[f"Left leg number {segment_number}"] = 3
            new_mega.original_limb[f"Right leg number {segment_number}"] = 3
            new_mega.original_limb[f"Body segment number {segment_number}"] = 3
        new_mega.habilities["Head"] = "perception"
        for segment_number in range(5):
            new_mega.habilities[f"Left leg number {segment_number}"] = "standing"
            new_mega.habilities[f"Right leg number {segment_number}"] = "standing"
            new_mega.habilities[f"Body segment number {segment_number}"] = "standing"
        new_mega.attack = 15
        new_mega.drop["hard_chitin"] = 50
        new_mega.drop["antennae"] = 10
        new_mega.drop["giant_centipede_brain"] = 5
        new_mega.drop["giant_centipede_heart"] = 5
        new_mega.drop["venom_gland"] = 20
        self.megabeasts.append(new_mega)

        for number_of_heads in range(1, 12):
            new_mega = Megabeast()
            new_mega.name = f"{number_of_heads}-headed Hydra"
            new_mega.limbs = {
                "Body": 3,
                "Tail": 3,
                "Front left paw": 3,
                "Front right paw": 3,
                "Back left paw": 3,
                "Back righ paw": 3,
            }
            for head in range(number_of_heads):
                new_mega.limbs[f"Head {head + 1}"] = 3
            new_mega.original_limb = {
                "Body": 1,
                "Tail": 1,
                "Front left paw": 1,
                "Front right paw": 1,
                "Back left paw": 1,
                "Back righ paw": 1,
            }
            for head in range(number_of_heads):
                new_mega.original_limb[f"Head {head + 1}"] = 1
            new_mega.habilities = {
                "Body": "None",
                "Tail": "damage",
                "Front left paw": "standing",
                "Front right paw": "standing",
                "Back left paw": "standing",
                "Back righ paw": "standing",
            }
            for head in range(number_of_heads):
                new_mega.habilities[f"Head {head + 1}"] = "perception"
            new_mega.attack = number_of_heads
            new_mega.drop["hydra_eye"] = 5*number_of_heads
            new_mega.drop["hydra_blood"] = 5*number_of_heads
            new_mega.drop["hydra_claw"] = 5*number_of_heads
            new_mega.drop["hydra_heart"] = 5*number_of_heads
            self.megabeasts.append(new_mega)
