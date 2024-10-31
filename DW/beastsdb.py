#############################################################
# Classe que segura todas as bestas normais e fixas         #
# Se existe o arquivo base, carrega, se não, cria um novo.  #
#############################################################

import os
from emoji import emojize
import random as rd
import copy


class Beast:
    # Tipo = string , (atk, def, hp) = int, name = string, prob = int, is_legendary = bool
    def __init__(self, tipo="type", atk=1, defense=1, hp=1, name="Blobson", prob=1, is_legendary=False, tier = 1, area_damage = False):
        self.tipo = tipo
        self.atk = atk
        self.defense = defense
        self.hp = hp
        self.name = name
        self.prob = prob
        self.is_legendary = is_legendary
        self.tier = tier
        self.area_damage = area_damage
        self.new()

    def new(self):
        pass


class MegaBeast(Beast):
    def new(self):
        pass
        # Falta fazer


class BeastsDB:
    def __init__(self, server):
        self.server = server
        self.beasts = []
        self.night_beasts = []
        self.legbeasts = []
        self.megabeasts = []
        self.beasts_probs = []
        self.legbeasts_probs = []
        self.megabeasts_probs = []
        self.n_legbeasts = 0
        self.bestiary_file = "dbs/bestiary.dat"
        self.num_named_beasts = 5

        loaded = self.server.helper.load_pickle(self.bestiary_file)
        if loaded:
            self.beasts = loaded[0]
            self.legbeasts = loaded[1]
            self.megabeasts = loaded[2]
        else:
            self.regenerate()
        self.generate_the_night()

        self.n_legbeasts = len(self.legbeasts)
        self.create_named_beasts(self.num_named_beasts)
        self.beasts_probs = [beast.prob for beast in self.beasts]
        self.legbeasts_probs = [beast.prob for beast in self.legbeasts]
        self.megabeasts_probs = [beast.prob for beast in self.megabeasts]

    def generate_the_night(self):
        self.night_beasts.append(Beast(emojize("Áillen :musical_note::fire:"), 200, 63, 100, "", 1, False, 2, True))
        self.night_beasts.append(Beast(emojize("Caoineag"), 34, 633, 30, "", 1, False, 1, False))
        self.night_beasts.append(Beast(emojize("Banshee"), 340, 63, 20, "", 1, False, 1, True))
        self.night_beasts.append(Beast(emojize("cat-sìth :cat:‍:black_large_square:"), 3, 4, 9, "", 1, False, 1, False))
        self.night_beasts.append(Beast(emojize("Cù-sìth :dog:"), 2, 6, 1, "", 1, False, 1, False))
        self.night_beasts.append(Beast(emojize("Changeling :person_in_steamy_room:"), 90, 6, 8, "", 1, False, 2, False))
        self.night_beasts.append(Beast(emojize("Clíodhna :princess:"), 90, 60, 30, "", 1, False, 2, False))
        self.night_beasts.append(Beast(emojize("Clurichaun :fairy:"), 3, 543, 8, "", 1, False, 2, False))
        self.night_beasts.append(Beast(emojize("Dearg Due"), 332, 54, 32, "", 1, False, 2, False))
        self.night_beasts.append(Beast(emojize("Dobhar-chú :fish::dog:"), 3, 543, 8, "", 1, False, 1, False))
        self.night_beasts.append(Beast(emojize("Dullahan :face_with_head-bandage::horse_face:"), 398, 533, 89, "", 1, False, 3, False))
        self.night_beasts.append(Beast(emojize("Ellén Trechend :fire::ogre::ogre::ogre:"), 654, 53, 83, "", 1, False, 2, True))
        self.night_beasts.append(Beast(emojize("Fachen :elephant:"), 3232, 5423, 832, "", 1, False, 4, False))
        self.night_beasts.append(Beast(emojize("Far darrig :fairy:"), 32, 543, 43, "", 1, False, 3, False))
        self.night_beasts.append(Beast(emojize("Fear gorta :hamburger:"), 98654, 46573, 5290, "", 1, False, 4, True))
        self.night_beasts.append(Beast(emojize("Am Fear Liath Mòr :snow-capped_mountain:"), 33, 54, 83, "", 1, False, 2, False))
        self.night_beasts.append(Beast(emojize("Fetch :person_in_steamy_room:"), 8234, 58653, 83, "", 1, False, 3, False))
        self.night_beasts.append(Beast(emojize("Fuath :droplet:"), 387, 643, 43, "", 1, False, 2, False))
        self.night_beasts.append(Beast(emojize("Gancanagh :fairy:"), 33, 52, 8, "", 1, False, 1, False))
        self.night_beasts.append(Beast(emojize("Ghillie Dhu :fairy:"), 34, 3, 8, "", 1, False, 1, False))
        self.night_beasts.append(Beast(emojize("Glaistig :droplet::goat:"), 3337, 5433, 82, "", 1, False, 3, False))
        self.night_beasts.append(Beast(emojize("Leanan sídhe"), 33, 53, 83, "", 1, False, 2, False))
        self.night_beasts.append(Beast(emojize("Leprechaun :fairy:"), 3, 53, 8, "", 1, False, 1, False))
        self.night_beasts.append(Beast(emojize("Púca"), 34, 53, 83, "", 1, False, 3, False))
        self.night_beasts.append(Beast(emojize("Sluagh :ghost:"), 334, 533, 83, "", 1, False, 3, False))
        self.night_beasts.append(Beast(emojize("The Morrígan :bird:‍:black_large_square:️"), 386678, 536868, 88765, "", 1, False, 4, True))
        self.night_beasts.append(Beast(emojize("The Dagda"), 35223, 53234, 84234, "", 1, False, 4, False))
        self.night_beasts.append(Beast(emojize("Lugh"), 3312, 521343, 8123, "", 1, False, 4, False))
        self.night_beasts.append(Beast(emojize("Nuada Airgetlám"), 331322, 51343, 81233, "", 1, False, 4, False))
        self.night_beasts.append(Beast(emojize("Aengus"), 3422, 514343, 813, "", 1, False, 4, False))
        self.night_beasts.append(Beast(emojize("Brigid"), 332, 543, 33, "", 1, False, 4, False))
        self.night_beasts.append(Beast(emojize("Nuada Airgetlám"), 331322, 51343, 81233, "", 1, False, 4, False))
        self.night_beasts.append(Beast(emojize("Manannán mac Lir :droplet:"), 674572, 515343, 81233, "", 1, False, 4, False))
        self.night_beasts.append(Beast(emojize("Dian Cecht"), 4322, 5343, 813, "", 1, False, 4, False))
        self.night_beasts.append(Beast(emojize("Goibniu"), 43242, 53443, 44813, "", 1, False, 4, False))
        self.night_beasts.append(Beast(emojize("Wicker Man :red_heart:️‍:fire:"), 31232, 34543, 47543, "", 1, False, 3, False))
        self.night_beasts.append(Beast(emojize(":ghost: Ghost of John Barleycorn :sheaf_of_rice:"), 1, 2, 3, "", 1, False, 1, False))
        self.night_beasts.append(Beast(emojize(":ghost: Sílvio"), 7, 7, 7, "", 1, False, 1, False))

    def regenerate(self):

        '''
            Bestas de tier 1 aparecem na floresta de 1 hora, tier 2 na de 4 horas, tier 3 na de 8, e tier 4 na de 12.

            Tempo em que ele saiu da floresta e o tempo que falta para ele voltar ditam qual tier que ele ver.

            0-30 minutos: Tier 1
            30 minutos - 2 horas: Tier 2
            2 - 4 horas: Tier 3
            4 - 6 horas: Tier 4
        '''
        # Normais

        # Tier 1 No area damage
        self.beasts.append(Beast(emojize("Boar :boar:"), 2, 6, 10, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Snake :snake:"), 6, 1, 5, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Squirrel :chipmunk:"), 1, 1, 5, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Hedgehog :hedgehog:"), 4, 4, 5, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Giant spider :spider:"), 6, 10, 30, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Wurm :dragon:"), 7, 7, 25, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Rabbit :rabbit:"), 1, 3, 5, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Big Lizard :T-Rex:"), 4, 10, 30, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Earth elemental :pile_of_poo:"), 2, 10, 20, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Imp :smiling_face_with_horns:"), 7, 7, 4, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Goblin :goblin:"), 2, 2, 10, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Skeleton :skull:"), 3, 2, 7, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Ghoul :zombie:"), 1, 5, 12, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Gorilla :gorilla:"), 5, 5, 30, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Wolf :wolf_face:"), 3, 3, 25, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Giant scorpion :scorpion:"), 5, 5, 30, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Rat :rat:"), 1, 2, 3, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Koala :koala:"), 1, 1, 23, "", 1, False, 1, False))
        self.beasts.append(Beast(emojize("Pig :pig_face:"), 4, 10, 21, "", 1, False, 1, False))

        # Tier 1 Area damage
        self.beasts.append(Beast(emojize("Fire elemental :fire:"), 10, 2, 2, "", 1, False, 1, True))
        self.beasts.append(Beast(emojize("Fat man :hamburger:"), 99, 99, 99, "", 1, False, 1, True))


        # Tier 2 no area damage
        self.beasts.append(Beast(emojize("Ogre :ogre:"), 10, 10, 30, "", 1, False, 2, False))
        self.beasts.append(Beast(emojize("Unicorn :unicorn_face:"), 20, 4, 25, "", 1, False, 2, False))
        self.beasts.append(Beast(emojize("Frog :frog_face:"), 50, 5, 21, "", 1, False, 2, False))
        self.beasts.append(Beast(emojize("Flying Capybara :bat:"), 50, 5, 21, "", 1, False, 2, False))

        # Tier 2 Area damage
        self.beasts.append(Beast(emojize("Large wolf pack :wolf_face::wolf_face::wolf_face::wolf_face::wolf_face:"
                                         ":wolf_face::wolf_face::wolf_face::wolf_face::wolf_face::wolf_face::wolf_face:"
                                         ":wolf_face::wolf_face::wolf_face::wolf_face:"), 48, 48, 25, "", 1, False, 2, True))
        self.beasts.append(Beast(emojize("Wolf pack :wolf_face::wolf_face::wolf_face::wolf_face:"
                                         ":wolf_face::wolf_face::wolf_face:"), 21, 21, 25, "", 1, False, 2, True))
        self.beasts.append(Beast(emojize("Small wolf pack :wolf_face::wolf_face::wolf_face:"), 9, 9, 25, "", 1, False, 2, True))
        self.beasts.append(Beast(emojize("Tree ent :evergreen_tree:"), 15, 15, 50, "", 1, False, 2, True))
        self.beasts.append(Beast(emojize("Lost Golem :moai:"), 10, 10, 50, "", 1, False, 2, True))
        self.beasts.append(Beast(emojize("Firey fox :fox_face:"), 30, 15, 50, "", 1, False, 2, True))
        self.beasts.append(Beast(emojize("Sprite :sparkles:"), 41, 31, 41, "", 1, False, 2, True))
        # self.beasts.append(Beast(emojize("Balrog :angry_face_with_horns:"), 300, 400, 700, "", 1, False))

        # Tier 3 no area damage
        self.beasts.append(Beast(emojize("Apparition :ghost:"), 5, 100, 75, "", 1, False, 3, False))
        self.beasts.append(Beast(emojize("Battle snail :snail:"), 300, 10, 100, "", 1, False, 3, False))
        self.beasts.append(Beast(emojize(":pouting_face: Angry crab :crab:"), 150, 200, 75, "", 1, False, 3, False))
        self.beasts.append(Beast(emojize("Ancient Rock Elemental"), 150, 90, 350, "", 1, False, 3, False))
        self.beasts.append(Beast(emojize("Shadow Spectre"), 300, 10, 105, "", 1, False, 3, False))
        self.beasts.append(Beast(emojize("Mamuth Parasite"), 30, 100, 10, "", 1, False, 3, False))
        self.beasts.append(Beast(emojize("Glass Mimic"), 123, 10, 10, "", 1, False, 3, False))
        self.beasts.append(Beast(emojize("Earth hound"), 432, 103, 50, "", 1, False, 3, False))

        # Tier 3 Area damage
        self.beasts.append(Beast(emojize("Butterfly :butterfly:"), 15, 15, 500, "", 1, False, 3, True))
        self.beasts.append(Beast(emojize("Giant crab :crab:"), 20, 50, 500, "", 1, False, 3, True))
        self.beasts.append(Beast(emojize("Peaceful Behemoth :sauropod:"), 600, 40, 700, "", 1, False, 3, True))
        self.beasts.append(Beast(emojize("Mud monster :sweat_droplets:"), 100, 10, 300, "", 1, False, 3, True))
        self.beasts.append(Beast(emojize(":pouting_face: Enraged mastodon :elephant:"), 100, 10, 300, "", 1, False, 3, True))
        self.beasts.append(Beast(emojize("Mushroom monster :mushroom:"), 550, 70, 30, "", 1, False, 3, True))
        self.beasts.append(Beast(emojize("Weird Medusa"), 50, 70, 300, "", 1, False, 3, True))
        self.beasts.append(Beast(emojize("Lightning Falcon of chaos"), 310, 70, 30, "", 1, False, 3, True))

        # Tier 4 no area damage
        self.beasts.append(Beast(emojize("Chupa-cabra :goat:"), 1000, 10, 700, "", 1, False, 4, False))
        self.beasts.append(Beast(emojize("Corrupted giant spider :spider:"), 700, 100, 50, "", 1, False, 4, False))
        self.beasts.append(Beast(emojize("Mithic Basilisk"), 700, 100, 500, "", 1, False, 4, False))
        self.beasts.append(Beast(emojize("Nine-headed Serpent"), 700, 10, 50, "", 1, False, 4, False))
        self.beasts.append(Beast(emojize("Flesh Eater Unicorn :unicorn_face:"), 500, 320, 40, "", 1, False, 4, False))

        # Tier 4 Area damage
        self.beasts.append(Beast(emojize(":pouting_face: Enraged Behemoth :sauropod:"), 200, 2000, 50, "", 1, False, 4, True))
        self.beasts.append(Beast(emojize("Crystal guardian :gem_stone:"), 300, 100, 200, "", 1, False, 4, True))
        self.beasts.append(Beast(emojize("Indignant Koala :koala:"), 50, 700, 10, "", 1, False, 3, True))
        self.beasts.append(Beast(emojize("H-man clone"), 500, 70, 100, "", 1, False, 3, True))
        self.beasts.append(Beast(emojize("Swamp thing"), 50, 750, 100, "", 1, False, 3, True))
        self.beasts.append(Beast(emojize("Giant Fire Ant army"), 500, 500, 10, "", 1, False, 3, True))
        self.beasts.append(Beast(emojize("Endothermic talking fireplace :fire:"), 50, 500, 100, "", 1, False, 3, True))
        self.beasts.append(Beast(emojize("Thunder Rhino :rhinoceros:"), 50, 500, 60, "", 1, False, 3, True))

        # Especiais

        # Tier 1 no area damage
        self.beasts.append(Beast(emojize("Snowman :snowman_without_snow:️"), 10, 40, 10, "", 1, False, 1, False))

        # Tier 1 area damage
        self.beasts.append(Beast(emojize("Angry Snowman :snowman:️"), 30, 20, 10, "", 1, False, 1, True))

        # Tier 2 no area damage

        # Tier 2 area damage
        self.beasts.append(Beast(emojize("Snow elemental :snowflake:️"), 800, 80, 40, "", 1, False, 2, True))

        # Tier 3 no area damage

        # Tier 3 area damage
        self.beasts.append(Beast(emojize("Snow storm elemental :cloud_with_snow:"), 1800, 5, 1000, "", 1, False, 3, True))

        # Tier 4 no area damage
        self.beasts.append(Beast(emojize("Frost :snowflake: cursed warrior"), 1200, 2200, 220, "", 1, False, 4, False))

        # Tier 4 area damage
        self.beasts.append(Beast(emojize("Walking ice crystal :gem_stone:"), 3200, 3200, 250, "", 1, False, 4, True))
        self.beasts.append(Beast(emojize("Ice Cyclop :snowflake:"), 1200, 1600, 350, "", 1, False, 4, True))

        # self.beasts.append(Beast(emojize("Walking sunflower :sunflower:"), 40, 40, 40, "", 7, False))
        # self.beasts.append(Beast(emojize("Mushroom Man :mushroom:"), 20, 60, 150, "", 7, False))
        # self.beasts.append(Beast(emojize("Wandering carnivorous plant :shamrock: :meat_on_bone:"), 60, 20, 30, "", 7, False))
        # self.beasts.append(Beast(emojize("Shambling potato :potato:"), 10, 90, 50, "", 5, False))
        # self.beasts.append(Beast(emojize("Roaming mandrake :herb:"), 100, 5, 60, "", 5, False))
        # self.beasts.append(Beast(emojize("Fat Plant :hamburger:"), 198, 198, 198, "", 4, False))
        # self.beasts.append(Beast(emojize("Killer coconut tree :palm_tree:"), 90, 50, 300, "", 4, False))
        # self.beasts.append(Beast(emojize("Plant abomination"), 30, 1, 4200, "", 4, False))
        # self.beasts.append(Beast(emojize("Corrupted moss"), -100, -100, 4200, "", 3, False))
        # self.beasts.append(Beast(emojize("Garlic Man"), 50, 20, 210, "", 3, False))
        # self.beasts.append(Beast(emojize("Raging :pineapple:"), 210, 5, 30, "", 3, False))
        # self.beasts.append(Beast(emojize(":hot_pepper:"), 150, 40, 90, "", 3, False))




        # Lendárias
        self.legbeasts.append(Beast(emojize("Boar :boar:"), 10, 10, 20, "Pumbo", 1, True, 1, False))
        self.legbeasts.append(Beast(emojize("Snake :snake:"), 15, 16, 10, "Python", 1, True, 1, False))
        self.legbeasts.append(Beast(emojize("Squirrel :chipmunk:"), 10000, 10000, 2000000, "Ydnas", 1, True, 1, False))
        self.legbeasts.append(Beast(emojize("Hedgehog :hedgehog:"), 1, 1, 2, "Sanic", 1, True, 1, False))
        self.legbeasts.append(Beast(emojize("Spider :spider:"), 20, 20, 40, "Eugogara", 1, True, 1, False))
        self.legbeasts.append(Beast(emojize("Rabbit :rabbit:"), 300, 300, 10, "Guardian of the cave", 1, True, 1, False))
        self.legbeasts.append(Beast(emojize("Demon :angry_face_with_horns:"), 100, 100, 100, "Depohtok", 1, True, 1, False))
        self.legbeasts.append(Beast(emojize("Fat man :hamburger:"), 99, 98, 100, "Igordão", 1, True, 1, False))
        self.legbeasts.append(Beast(emojize("Rabbit :rabbit:"), 300, 300, 10, "Cueio", 1, True, 1, False))
        self.legbeasts.append(Beast(emojize("Gorilla :gorilla:"), 300, 300, 10, "Harambe", 1, True, 1, False))
        self.legbeasts.append(Beast(emojize("Wolf pack :wolf_face::wolf_face::wolf_face::wolf_face::wolf_face::wolf_face:"
                                            ":wolf_face::wolf_face::wolf_face::wolf_face::wolf_face::wolf_face::wolf_face:"
                                            ":wolf_face::wolf_face::wolf_face::wolf_face::wolf_face::wolf_face::wolf_face:"
                                            ":wolf_face::wolf_face::wolf_face::wolf_face::wolf_face::wolf_face::wolf_face:"
                                            ":wolf_face::wolf_face::wolf_face::wolf_face::wolf_face:"),
                              21, 21, 200, "Dark Moon Pack", 1, True, 1, False))
        self.legbeasts.append(Beast(emojize("Frog :frog_face:"), 100, 100, 100, "Pepe", 1, True, 1, False))
        self.legbeasts.append(Beast(emojize("Butterfly :butterfly:"), 500, 500, 500, "Atsiluap", 1, True, 1, False))
        self.n_legbeasts = len(self.legbeasts)

        # Mega
        self.megabeasts.append(MegaBeast("Hydra", 20, 20, 100, self.server.helper.randomnamegenerator(6), 1, True))
        self.megabeasts.append(MegaBeast("Dragon", 20, 20, 100, self.server.helper.randomnamegenerator(6), 1, True))


        self.save_beasts()

    def create_named_beasts(self, n):
        for i in range(self.num_named_beasts):
            self.legbeasts.append(Beast(emojize("Boar :boar:"), rd.randint(0, 10), rd.randint(0, 10),
                                        rd.randint(0, 40), self.server.helper.randomnamegenerator(3), 1, True, 1, False))
            self.legbeasts.append(Beast(emojize("Snake :snake:"), rd.randint(5, 20), rd.randint(0, 5),
                                        rd.randint(0, 20), self.server.helper.randomnamegenerator(2), 1, True, 1, False))
            self.legbeasts.append(Beast(emojize("Squirrel :chipmunk:"), rd.randint(1, 3), rd.randint(10, 20),
                                        rd.randint(2, 5), self.server.helper.randomnamegenerator(2), 1, True, 1, False))
            self.legbeasts.append(Beast(emojize("Hedgehog :hedgehog:"), rd.randint(2, 20), rd.randint(2, 20),
                                        rd.randint(0, 5), self.server.helper.randomnamegenerator(2), 1, True, 1, False))
            self.legbeasts.append(Beast(emojize("Giant spider :spider:"), rd.randint(3, 5), rd.randint(10, 20),
                                        rd.randint(20, 40), self.server.helper.randomnamegenerator(7), 1, True, 1, False))
            self.legbeasts.append(Beast(emojize("Rabbit :rabbit:"), rd.randint(5, 10), rd.randint(0, 2),
                                        rd.randint(5, 10), self.server.helper.randomnamegenerator(3), 1, True, 1, False))
            self.legbeasts.append(Beast(emojize("Demon :angry_face_with_horns:"), rd.randint(30, 50), rd.randint(0, 10),
                                        rd.randint(0, 40), self.server.helper.randomnamegenerator(8), 1, True, 1, False))
            self.legbeasts.append(Beast(emojize("Fada :fairy:"), rd.randint(1200, 1300), rd.randint(0, 500),
                                        rd.randint(0, 500), self.server.helper.randomnamegenerator(21), 1, True, 1, False))
            self.legbeasts.append(Beast(emojize("Butterfly :butterfly:"), rd.randint(400, 600), rd.randint(400, 600),
                                        rd.randint(400, 600), self.server.helper.randomnamegenerator(3), 1, True, 1, False))
            self.legbeasts.append(Beast(emojize("Fat man :hamburger:"), rd.randint(50, 150), rd.randint(50, 150),
                                        rd.randint(50, 150), self.server.helper.randomnamegenerator(10), 1, True, 1, False))

        for legbeast in self.legbeasts:
            print(legbeast.tipo + " nomeado " + legbeast.name)
        print(f"Total number of legendary beasts: {len(self.legbeasts)}")

    def save_beasts(self):
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle([self.beasts, self.legbeasts[:self.n_legbeasts], self.megabeasts], self.bestiary_file)

    def get_random_beast(self, tier):
        eligible = []
        if self.server.is_day:
            for besta in self.beasts:
                if besta.tier == tier:
                    eligible.append(copy.copy(besta))
        else:
            for besta in self.night_beasts:
                if besta.tier == tier:
                    eligible.append(copy.copy(besta))
        probs = [beast.prob for beast in eligible]
        beast = rd.choices(eligible, probs)[0]
        return copy.copy(beast)

    def get_random_legbeast(self):
        beast = rd.choices(self.legbeasts, self.legbeasts_probs)[0]
        return copy.copy(beast)

    def get_random_megabeast(self):
        beast = rd.choices(self.megabeasts, self.megabeasts_probs)[0]
        return copy.copy(beast)
