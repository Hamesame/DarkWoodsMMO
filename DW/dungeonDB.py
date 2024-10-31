###################################
#  Classe que segura as dungeons  #
###################################

import items
import beastsdb
from emoji import emojize
import random as rd


class dungeon:
    def __init__(self, beasts, level, rewards, name):
        self.beasts = beasts
        self.rewards = rewards
        self.level = level
        self.name = name


class dungeonDataBase:
    def __init__(self, server):
        self.dungeons = []
        self.helperman = server.helper
        self.generate_dgs()

    def generate_dgs(self):
        dbbeasts = []
        rewards = []

        newbeast = beastsdb.Beast(emojize("Crawling spores :mushroom:"), 4, 4, 4, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        newbeast = beastsdb.Beast(emojize("Zombie :zombie:"), 2, 6, 5, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        newbeast = beastsdb.Beast(emojize("Zombie :zombie:"), 6, 6, 30, "Gravedigger", 1, 1, 1, False)
        dbbeasts.append(newbeast)

        newwep = items.Weapon(emojize("Rotten mace"), 0, "rt_mace", 1, [8, 8])
        newwep.description = "A mace made out of body parts. Its mainly a torso of an adult female tied with intestines to a femur. It smells rotten."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Body parts"), 0, "bd_prts1", 1, [1, 1])
        newwep.description = "A left leg."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Body parts"), 0, "bd_prts2", 1, [1, 1])
        newwep.description = "A right leg."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Body parts"), 0, "bd_prts3", 1, [1, 1])
        newwep.description = "A right arm."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Body parts"), 0, "bd_prts4", 1, [1, 1])
        newwep.description = "A left arm."
        rewards.append(newwep)

        newdg = dungeon(dbbeasts, 1, rewards, "cave")
        self.dungeons.append(newdg)

        # ----------------------------------------------------------------

        dbbeasts = []
        rewards = []

        newbeast = beastsdb.Beast(emojize("Shadow :black_circle:"), 50, 140, 40, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        newbeast = beastsdb.Beast(emojize("Walking thing :man_walking:"), 150, 20, 3, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        newbeast = beastsdb.Beast(emojize("Mecha witch"), 100, 120, 30, self.helperman.randomnamegenerator(5), 1, 1, 1, False)
        dbbeasts.append(newbeast)

        random_name = self.helperman.randomnamegenerator(5)
        newwep = items.Weapon("weird " + random_name, 1, random_name, 1, [rd.randint(30, 50), rd.randint(30, 50)])
        newwep.type2 = "magic"
        newwep.description = "You are not sure what a weird is."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("witchcraft"), 0, "wc1", 1, [1, 1])
        newwep.type2 = "magic"
        newwep.description = "A doll."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("witchcraft"), 0, "wc2", 1, [1, 1])
        newwep.type2 = "magic"
        newwep.description = "Some roots."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("witchcraft"), 0, "wc3", 1, [1, 1])
        newwep.type2 = "magic"
        newwep.description = "Remnants of a burnt chicken."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("witchcraft"), 0, "wc4", 1, [1, 1])
        newwep.type2 = "magic"
        newwep.description = "Remnants of a burnt chicken."
        rewards.append(newwep)

        newdg = dungeon(dbbeasts, 3, rewards, "small cottage")
        self.dungeons.append(newdg)

        # --------------------------------------------------------------

        dbbeasts = []
        rewards = []

        newbeast = beastsdb.Beast(emojize("Cultist :mage:"), 250, 50, 21, "", 1, 0, 1, True)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        newbeast = beastsdb.Beast(emojize("Exotic Imp :smiling_face_with_horns:"), 150, 150, 30, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        newbeast = beastsdb.Beast(emojize("Dark Cultist :mage:"), 500, 20, 21, "", 1, 0, 1, True)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        demon_name = self.helperman.randomnamegenerator(10)
        newbeast = beastsdb.Beast(emojize("Demon"), 1100, 300, 130, demon_name, 1, 1, 1, False)
        dbbeasts.append(newbeast)

        random_name = self.helperman.randomnamegenerator(5)
        newwep = items.Weapon("evil "+random_name, 1, random_name, 1, [rd.randint(50, 90), rd.randint(20, 30)])
        newwep.type2 = "magic"
        newwep.description = f"Whatever a {random_name} is, but it emanates a dark aura."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Demonic objects"), 0, "do1", 1, [1, 1])
        newwep.type2 = "magic"
        newwep.description = f"The heart of {demon_name}."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Demonic objects"), 0, "do2", 1, [1, 1])
        newwep.type2 = "magic"
        newwep.description = f"The wooden crown of {demon_name}."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Demonic objects"), 0, "do3", 1, [1, 1])
        newwep.type2 = "magic"
        newwep.description = f"The plopiteal artery of {demon_name}."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Demonic objects"), 0, "do4", 1, [1, 1])
        newwep.type2 = "magic"
        newwep.description = f"The kidney of {demon_name}."
        rewards.append(newwep)

        newdg = dungeon(dbbeasts, 4, rewards, "hole in the ground")
        self.dungeons.append(newdg)

        # --------------------------------------------------------------

        dbbeasts = []
        rewards = []

        for i in range(10):
            newbeast = beastsdb.Beast(emojize("Greedy adventurer :sunglasses:, floor: "+str(i+1)), 5+i, 5+i, 21, "", 1, 0, 1, False)
            dbbeasts.append(newbeast)
        for i in range(10):
            newbeast = beastsdb.Beast(emojize("Crazed adventurer, floor: "+str(11+i)), 104+i*2, 104+i*2, 21, "", 1, 0, 1, False)
            dbbeasts.append(newbeast)
        for i in range(10):
            newbeast = beastsdb.Beast(emojize("Tower abomination, floor: "+str(21+i)), 20, 20, 302+10*i, "", 1, 0, 1, False)
            dbbeasts.append(newbeast)
        for i in range(10):
            newbeast = beastsdb.Beast(emojize("forgotten ghost, floor: "+str(31+i)), 1, 202+i, 202+i, "", 1, 0, 1, False)
            dbbeasts.append(newbeast)
        for i in range(10):
            newbeast = beastsdb.Beast(emojize("Exiled Devil, floor: "+str(41+i)), 1401+i*10, 401+i*2, 401+i*2, "", 1, 0, 1, False)
            dbbeasts.append(newbeast)
        for i in range(10):
            newbeast = beastsdb.Beast(emojize("Fallen god, floor: "+str(51+i)), 2392, 592, 392+i*5, "", 1, 0, 1, False)
            dbbeasts.append(newbeast)
        for i in range(10):
            newbeast = beastsdb.Beast(emojize("Corrupted singularity, floor: "+str(61+i)), 5392, 292+i*2, 287, "", 1, 0, 1, False)
            dbbeasts.append(newbeast)
        for i in range(10):
            newbeast = beastsdb.Beast(emojize("Stranded Alien :alien:, floor: "+str(71+i)), 2392+i*10, 3382, 21, "", 1, 0, 1, False)
            dbbeasts.append(newbeast)
        for i in range(10):
            newbeast = beastsdb.Beast(emojize("Ancestral being, floor: "+str(81+i)), 3382+i*10, 382+i*3, 382+i*3, "", 1, 0, 1, False)
            dbbeasts.append(newbeast)
        for i in range(9):
            newbeast = beastsdb.Beast(emojize("Primal force, floor: "+str(91+i)), 4372+i*10, 472+i*4, 472+i*4, "", 1, 0, 1, False)
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Neutron Star, foor: 100"), 9999, 9999, 200, self.helperman.randomnamegenerator(1000), 1, 1, 1, False)
        dbbeasts.append(newbeast)

        newwep = items.Weapon("1 - Dimensional Manipulator", 1, "1dim_wep", 1, [999, 999])
        newwep.type2 = "magic"
        newwep.description = f"An artifact able to bend spacetime itself but only one dimention at a time. Found in the end of the tower ruins, the place that is closest to the heavens. No one knows by who it was crafted, how or where."
        rewards.append(newwep)

        for i in range(9):
            newwep = items.Weapon(emojize("dust"), 0, f"d{i}", 1, [rd.randint(5,15), rd.randint(5,15)])
            newwep.type2 = "magic"
            newwep.description = f"Dust that fell down in the tower ruins."
            rewards.append(newwep)

        newdg = dungeon(dbbeasts, 6, rewards, "very high tower ruins")
        self.dungeons.append(newdg)

        # --------------------------------------------------------------

        dbbeasts = []
        rewards = []

        newbeast = beastsdb.Beast(emojize("Giant insect"), 30, 1100, 50, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Kobold army"), 700, 10, 210, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        newbeast = beastsdb.Beast(emojize("CrackHead goblin"), 800, 5, 1100, "Duerf", 1, 1, 1, False)
        dbbeasts.append(newbeast)

        random_name = self.helperman.randomnamegenerator(6)
        newwep = items.Weapon("Exotic crystal of "+random_name, 1, random_name, 1, [rd.randint(70, 150), rd.randint(5, 10)])
        newwep.type2 = "magic"
        newwep.description = f"A crystal that shoots lasers."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Crystal sneakers"), 0, "cs1", 1, [10, 2])
        newwep.description = f"Some pointy shoes."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Crystal sneakers"), 0, "cs2", 1, [10, 2])
        newwep.description = f"Some pointy shoes."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Crystal sneakers"), 0, "cs3", 1, [10, 2])
        newwep.description = f"Some pointy shoes."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Crystal sneakers"), 0, "cs4", 1, [10, 2])
        newwep.description = f"Some pointy shoes."
        rewards.append(newwep)

        newdg = dungeon(dbbeasts, 5, rewards, "crystal cavern")
        self.dungeons.append(newdg)

        # --------------------------------------------------------------

        dbbeasts = []
        rewards = []

        newbeast = beastsdb.Beast(emojize("Lesser Golem"), 15, 10, 25, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Crawling object"), 3, 15, 50, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        newbeast = beastsdb.Beast(emojize("Lost Ancient"), 40, 40, 21, self.helperman.randomnamegenerator(3), 1, 1, 1, False)
        dbbeasts.append(newbeast)

        random_name = self.helperman.randomnamegenerator(2)
        newwep = items.Weapon("Ancient "+random_name, 1, random_name, 1, [rd.randint(4, 15), rd.randint(4, 15)])
        newwep.type2 = "magic"
        newwep.description = f"A very old instrument."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Unknown fragments"), 0, "unf1", 1, [4, 4])
        newwep.description = f"Unrecognizable fragments. Probrably owned by an elder civilization."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Unknown fragments"), 0, "unf2", 1, [4, 4])
        newwep.description = f"Unrecognizable fragments. Probrably owned by an elder civilization."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Unknown fragments"), 0, "unf3", 1, [4, 4])
        newwep.description = f"Unrecognizable fragments. Probrably owned by an elder civilization."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Unknown fragments"), 0, "unf4", 1, [4, 4])
        newwep.description = f"Unrecognizable fragments. Probrably owned by an elder civilization."
        rewards.append(newwep)

        newdg = dungeon(dbbeasts, 2, rewards, "Ruin")
        self.dungeons.append(newdg)



        # --------------------------------------------------------------

        # --------------------------------------------------------------

        dbbeasts = []
        rewards = []

        newbeast = beastsdb.Beast(emojize("Fat Guard :hamburger:"), 49, 49, 49, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Lost Fat Man :hamburger:"), 99, 99, 99, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Inner Fat Guard :hot_dog:"), 199, 199, 199, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize(":french_fries:"), 249, 249, 249, "", 1, 0, 1, True)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)


        newbeast = beastsdb.Beast(emojize("Walking food :pancakes:"), 297, 297, 297, self.helperman.randomnamegenerator(3), 1, 1)
        dbbeasts.append(newbeast)

        random_name = self.helperman.randomnamegenerator(3)
        newwep = items.Weapon(f"Croissant Excalibur :croissant: named {random_name}", 1, random_name, 1, [rd.randint(49, 149), rd.randint(49, 149)])
        newwep.description = f"A long and broad sword. Its hilt is made of croissant."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Food"), 0, "f1", 1, [30, 50])
        newwep.description = f"A hot dog."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Food"), 0, "f2", 1, [30, 50])
        newwep.description = f"Some fries."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Food"), 0, "f3", 1, [30, 50])
        newwep.description = f"A burger."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Food"), 0, "f4", 1, [30, 50])
        newwep.description = f"A A.A.A.A.A."
        rewards.append(newwep)

        newdg = dungeon(dbbeasts, 0, rewards, "fat dungeon")
        self.dungeons.append(newdg)



        dbbeasts = []
        rewards = []

        newbeast = beastsdb.Beast(emojize("Walking mechanism"), 999, 999, 50, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Unknown Beast"), 700, 100, 1000, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Slime"), 123, 321, 321, "", 1, 0, 1, True)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)




        newbeast = beastsdb.Beast(emojize("Floating Orb"), 249, 249, 249, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)
        dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Commander"), 7000, 614, 614, self.helperman.randomnamegenerator(3), 1, 1, 1, False)
        dbbeasts.append(newbeast)

        random_name = self.helperman.randomnamegenerator(3)
        newwep = items.Weapon(f"Brillouin Cannon {random_name}", 1, random_name, 1, [rd.randint(256, 890), rd.randint(123, 1439)])
        newwep.type2 = "ranged"
        newwep.description = f"What, never saw a cannon based of brillouin scattering?"
        rewards.append(newwep)
        random_name = self.helperman.randomnamegenerator(16)
        newwep = items.Weapon(f"Supercontinuum Femtosecond laser {random_name}", 1, random_name, 1, [rd.randint(0, 600), rd.randint(99, 199)])
        newwep.type2 = "ranged"
        newwep.description = f"Is it real? A a Supercontinuum laser be a Femtosecond laser? Well, in this game, everyting is possible!"
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Phaser"), 0, "ph1", 1, [90, 10])
        newwep.type2 = "ranged"
        newwep.description = f"A laser gun."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Phaser"), 0, "ph2", 1, [90, 10])
        newwep.type2 = "ranged"
        newwep.description = f"A laser gun."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Phaser"), 0, "ph3", 1, [90, 10])
        newwep.type2 = "ranged"
        newwep.description = f"A laser gun."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Phaser"), 0, "ph4", 1, [90, 10])
        newwep.type2 = "ranged"
        newwep.description = f"A laser gun."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Phaser"), 0, "ph5", 1, [90, 10])
        newwep.type2 = "ranged"
        newwep.description = f"A laser gun."
        rewards.append(newwep)

        newdg = dungeon(dbbeasts, 7, rewards, "Door")
        self.dungeons.append(newdg)




# -----------------------------------------

        # dbbeasts = []
        # rewards = []

        # newbeast = beastsdb.Beast(emojize("Large imp :smiling_face_with_horns:"), 69, 69, 30, "", 1, 0)
        # dbbeasts.append(newbeast)
        # newbeast = beastsdb.Beast(emojize("Ancient ritual object"), 10, 10, 10, "", 1, 0)
        # dbbeasts.append(newbeast)
        # newbeast = beastsdb.Beast(emojize("Bloodthisty cultist :mage:"), 100, 100, 100, "", 1, 0)
        # dbbeasts.append(newbeast)
        # newbeast = beastsdb.Beast(emojize("Demons :angry_face_with_horns: horde"), 1000, 1000, 200, "", 1, 0)
        # dbbeasts.append(newbeast)
        # newbeast = beastsdb.Beast(emojize("Spawn of Lesser Demonlord Ogaitnas"), 1500, 1000, 1000, "", 1, 0)
        # dbbeasts.append(newbeast)
        # newbeast = beastsdb.Beast(emojize("Spawn of Greater Demonlord Idlarab"), 2000, 2500, 2000, self.helperman.randomnamegenerator(3), 1, 1)
        # dbbeasts.append(newbeast)

        # random_name = self.helperman.randomnamegenerator(2)
        # newwep = items.Weapon("Demonic "+random_name, 1, random_name, 1, [rd.randint(400, 500), rd.randint(20, 50)])
        # rewards.append(newwep)
        # newwep = items.Weapon(emojize(":black_circle:"), 1, "bug", 1, [123, 321])
        # rewards.append(newwep)
        # rewards.append(newwep)
        # rewards.append(newwep)
        # rewards.append(newwep)

        # newdg = dungeon(dbbeasts, 5, rewards, "Pentagram")
        # self.dungeons.append(newdg)

        # --------------------------------------------------------------

        dbbeasts = []
        rewards = []

        newbeast = beastsdb.Beast(emojize("Major earth elemental :pile_of_poo:"), 300, 250, 500, "", 1, 0, 1, True)
        n1 = rd.randint(2,5)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Major fire elemental :fire:"), 2000, 400, 500, "", 1, 0, 1, True)
        n1 = rd.randint(1,10)
        for i in range(n1):
            dbbeasts.append(newbeast)
        newbeast = beastsdb.Beast(emojize("Magma Elemental :pile_of_poo: :fire:"), 4000, 4000, 40, "", 1, 0, 1, True)
        n1 = rd.randint(10,20)
        for i in range(n1):
            dbbeasts.append(newbeast)
        newbeast = beastsdb.Beast(emojize(":red_heart:Heart of the mountain:red_heart:"), 9999, 9999, 59, self.helperman.randomnamegenerator(3), 1, 1, 1, True)
        dbbeasts.append(newbeast)

        random_name = self.helperman.randomnamegenerator(5)
        newwep = items.Weapon(emojize("Hell Sword :fire: named ")+random_name, 1, random_name, 1, [rd.randint(600, 700), rd.randint(100, 800)])
        newwep.type2 = "magic"
        newwep.description = f"A flaming sword. Its temperature keeps you warm. Its blade is red hot. (Probrably hotter than the forge it was made)"
        rewards.append(newwep)
        random_name = self.helperman.randomnamegenerator(5)
        newwep = items.Weapon(emojize("Glowing Shield :fire: named ")+random_name, 1, random_name, 1, [rd.randint(300, 400), rd.randint(1000, 2500)])
        newwep.description = f"A flaming shield. Its temperature keeps you warm. It is red hot. (Probrably hotter than the forge it was made)"
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Sharp molten rocks"), 0, "spmoro1", 1, [100, 10])
        newwep.description = f"How can a rock be molten and sharp at the same time?"
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Sharp molten rocks"), 0, "spmoro2", 1, [100, 10])
        newwep.description = f"How can a rock be molten and sharp at the same time?"
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Sharp molten rocks"), 0, "spmoro3", 1, [100, 10])
        newwep.description = f"How can a rock be molten and sharp at the same time?"
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Sharp molten rocks"), 0, "spmoro4", 1, [100, 10])
        newwep.description = f"How can a rock be molten and sharp at the same time?"
        rewards.append(newwep)

        newdg = dungeon(dbbeasts, 8, rewards, emojize("Volcano :volcano:"))
        self.dungeons.append(newdg)

        # --------------------------------------------------------------
        # --------------------------------------------------------------

        dbbeasts = []
        rewards = []

        newbeast = beastsdb.Beast(emojize("Mangava :honeybee:"), 99, 49, 29, "", 1, 0, 1, False)
        n1 = rd.randint(2,2)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Large Hornet :honeybee:"), 50, 100, 50, "", 1, 0, 1, False)
        n1 = rd.randint(5,5)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Royal soldiers :honeybee:"), 100, 100, 100, "", 1, 0, 1, False)
        n1 = rd.randint(5,5)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Hive king"), 120, 80, 300, self.helperman.randomnamegenerator(3), 1, 1, 1, False)
        dbbeasts.append(newbeast)

        random_name = self.helperman.randomnamegenerator(2)
        newwep = items.Weapon(emojize("Mangava hive :honeybee: of ")+random_name, 1, random_name, 1, [rd.randint(50,60), rd.randint(10,20)])
        newwep.type2 = "ranged"
        newwep.description = f"A portable mangava hive, can cast a swarm of mangavas at the opponent. What, you don't know what a mangava is? Google it, but don't be scared, its a bee the size of a bird. Usually its a very peacefull animal, it will hardly attack anyone. But when it does, IT DOES. On this game mangavas are agressive."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("hornet stinger :honeybee:"), False, "hr_str1", 1, [6, 3])
        newwep.type2 = "ranged"
        newwep.description = "A machine gun of hornets."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("hornet stinger :honeybee:"), False, "hr_str2", 1, [6, 3])
        newwep.type2 = "ranged"
        newwep.description = "A machine gun of hornets."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("hornet stinger :honeybee:"), False, "hr_str3", 1, [6, 3])
        newwep.type2 = "ranged"
        newwep.description = "A machine gun of hornets."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("hornet stinger :honeybee:"), False, "hr_str4", 1, [6, 3])
        newwep.type2 = "ranged"
        newwep.description = "A machine gun of hornets."
        rewards.append(newwep)

        newdg = dungeon(dbbeasts, 3, rewards, emojize("Hive :honeybee:"))
        self.dungeons.append(newdg)

        # --------------------------------------------------------------

        # --------------------------------------------------------------

        dbbeasts = []
        rewards = []

        newbeast = beastsdb.Beast(emojize("Roots"), 15, 5, 30, "", 1, 0, 1, False)
        n1 = rd.randint(2,2)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Fungus"), 30, 1, 100, "", 1, 0, 1, True)
        n1 = rd.randint(5,5)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Weird Fragment"), 1, 1, 1, "", 1, 0, 1, False)
        n1 = rd.randint(5,5)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Wood Elemental"), 10, 50, 50, self.helperman.randomnamegenerator(3), 1, 1, 1, False)
        dbbeasts.append(newbeast)

        random_name = self.helperman.randomnamegenerator(2)
        newwep = items.Weapon(emojize("Oaken log ")+random_name, 1, random_name, 1, [rd.randint(5,10), rd.randint(40,50)])
        newwep.description = "A log with the format of a shield. Can be used as a shield. Its wood is very heavy."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("branch"), False, "branch331", 1, [1, 2])
        newwep.description = "A branch whose shape resembles a shield with spikes. Not a real weapon."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("branch"), False, "branch332", 1, [1, 2])
        newwep.description = "A branch whose shape resembles a shield with spikes. Not a real weapon."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("branch"), False, "branch333", 1, [1, 2])
        newwep.description = "A branch whose shape resembles a shield with spikes. Not a real weapon."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("branch"), False, "branch334", 1, [1, 2])
        newwep.description = "A branch whose shape resembles a shield with spikes. Not a real weapon."
        rewards.append(newwep)

        newdg = dungeon(dbbeasts, 2, rewards, emojize("Oak :deciduous_tree:"))
        self.dungeons.append(newdg)

        # --------------------------------------------------------------

        # --------------------------------------------------------------

        dbbeasts = []
        rewards = []

        newbeast = beastsdb.Beast(emojize("Lost spirit, it started whispering something, most words didn't make any sense but, out of that you could understand the word Asmeria, as the spirit noticed you couldn't understand, it touched you"), 1, 1, 1, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Being able to understand it, he told you a story about how everything was once part of one thing named Asmeria and how it shattered into fragments, creating nearly everything we know"), 1, 1, 1, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("You pondered about what the spirt said, but first of all, how does he know the name \"Asmeria\" and all that? So, Unsure of what are the spirt intentions, you tried to kill it"), 1, 1, 1, "", 1, 0, 1, False)
        dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Spirit"), 1, 1, 1, "?", 1, 1, 1, False)
        dbbeasts.append(newbeast)

        random_name = self.helperman.randomnamegenerator(2)
        newwep = items.Weapon(random_name, 1, random_name, 1, [rd.randint(1,3), rd.randint(1,3)])
        newwep.type2 = "magic"
        newwep.description = random_name
        rewards.append(newwep)
        newwep = items.Weapon(emojize("empty"), False, "01", 1, [0, 0])
        rewards.append(newwep)
        newwep = items.Weapon(emojize("empty"), False, "02", 1, [0, 0])
        rewards.append(newwep)
        newwep = items.Weapon(emojize("empty"), False, "03", 1, [0, 0])
        rewards.append(newwep)
        newwep = items.Weapon(emojize("empty"), False, "04", 1, [0, 0])
        rewards.append(newwep)

        newdg = dungeon(dbbeasts, 0, rewards, emojize("Cave of Erol"))
        self.dungeons.append(newdg)

        # --------------------------------------------------------------

        # --------------------------------------------------------------

        dbbeasts = []
        rewards = []

        newbeast = beastsdb.Beast(emojize("Cricket"), 5, 5, 30, "", 1, 0, 1, False)
        n1 = rd.randint(10,10)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Giant Cockroach"), 10, 10, 100, "", 1, 0, 1, True)
        n1 = rd.randint(10,10)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Spelunker"), 20, 20, 100, "", 1, 0, 1, False)
        n1 = rd.randint(10,10)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Crazed Spelunker"), 50, 50, 50, "", 1, 0, 1, False)
        n1 = rd.randint(10,10)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Wispy Shadow"), 100, 100, 50, "", 1, 0, 1, False)
        n1 = rd.randint(10,10)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Black Specter"), 200, 200, 50, "", 1, 0, 1, False)
        n1 = rd.randint(10,10)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Witch"), 500, 500, 50, "", 1, 0, 1, False)
        n1 = rd.randint(10,10)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Crazed Witch"), 1000, 1000, 50, "", 1, 0, 1, False)
        n1 = rd.randint(10,10)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Swarm of Undead Bats"), 2000, 2000, 50, "", 1, 0, 1, False)
        n1 = rd.randint(9,9)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Necromancer"), 5000, 5000, 5000, self.helperman.randomnamegenerator(3), 1, 1, 1, False)
        dbbeasts.append(newbeast)

        random_name = self.helperman.randomnamegenerator(2)
        newwep = items.Weapon(emojize("Necromancer Staff")+random_name, 1, random_name, 1, [rd.randint(200,250), rd.randint(100,200)])
        newwep.description = "A log with the format of a shield. Can be used as a shield. Its wood is very heavy."
        newwep.type2 = "magic"
        rewards.append(newwep)
        newwep = items.Weapon(emojize("bones"), False, "bones331", 1, [1, 2])
        newwep.description = "Some bones. Not a real weapon."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("bones"), False, "bones332", 1, [1, 2])
        newwep.description = "Some bones. Not a real weapon."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("bones"), False, "bones333", 1, [1, 2])
        newwep.description = "Some bones. Not a real weapon."
        rewards.append(newwep)
        newwep = items.Weapon(emojize("bones"), False, "bones334", 1, [1, 2])
        newwep.description = "Some bones. Not a real weapon."
        rewards.append(newwep)

        newdg = dungeon(dbbeasts, 3, rewards, emojize("Almost Bottomless Hole"))
        self.dungeons.append(newdg)

        # --------------------------------------------------------------

        # --------------------------------------------------------------

        dbbeasts = []
        rewards = []

        newbeast = beastsdb.Beast(emojize("Ancient Bear"), 40, 130, 10, "", 1, 0, 1, False)
        n1 = rd.randint(2,3)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Temporary Ghost"), 70, 100, 10, "", 1, 0, 1, True)
        n1 = rd.randint(1,2)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Hippogriff"), 200, 20, 10, "", 1, 0, 1, False)
        n1 = rd.randint(1,3)
        for i in range(n1):
            dbbeasts.append(newbeast)

        newbeast = beastsdb.Beast(emojize("Mage"), 210, 150, 50, "Brok the ruthless", 1, 1, 1, False)
        dbbeasts.append(newbeast)

        random_name = self.helperman.randomnamegenerator(2)
        pos_weps = []
        newwep = items.Weapon(emojize("Time Orb"), 1, "Tob02", 1, [78, 15])
        newwep.description = "If handled by the right hands, can manipulate time itself."
        newwep.type2 = "magic"
        pos_weps.append(newwep)
        newwep = items.Weapon(emojize("Windbreak bow"), 1, "Wdb03", 1, [80, 32])
        newwep.description = "If handled by the right hands, can manipulate time itself."
        newwep.type2 = "ranged"
        pos_weps.append(newwep)
        newwep = items.Weapon(emojize("Sword end of time"), 1, "Seot04", 1, [73, 90])
        newwep.description = "If handled by the right hands, can manipulate time itself."
        newwep.type2 = "melee"
        pos_weps.append(newwep)
        rewards.append(rd.choices(pos_weps)[0])

        newwep = items.Weapon(emojize("Temporary cut"), False, "Tmp01", 1, [3, 7])
        newwep.description = ""
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Temporary cut"), False, "Tmp02", 1, [3, 7])
        newwep.description = ""
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Temporary cut"), False, "Tmp03", 1, [3, 7])
        newwep.description = ""
        rewards.append(newwep)
        newwep = items.Weapon(emojize("Temporary cut"), False, "Tmp04", 1, [3, 7])
        newwep.description = ""
        rewards.append(newwep)

        newdg = dungeon(dbbeasts, 3, rewards, emojize("Caverns of Time"))
        self.dungeons.append(newdg)

        # --------------------------------------------------------------

        return self.dungeons


        # --------------------------------------------------------------
