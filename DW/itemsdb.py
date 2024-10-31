#####################################################################
# Classe que segura todos os itens, especiais e fixos encontráveis  #
# Se existe o arquivo base, carrega, se não, cria um novo.          #
#####################################################################

import os
from emoji import emojize
import random as rd
import copy
import items


class ItemsDB:
    '''
        Database que guarda e gerencia todos os itens existentes na floresta (isto é, todas as instâncias da classe Item encontráveis na floresta).
    '''
    def __init__(self, server):
        self.server = server    # O server é necessário para podermos salvar as alterações.
        self.weapons = []       # Lista que conterá todas as armas (instâncias de Weapon) encontráveis na floresta.
        self.others = []        # Lista que conterá todos os outros itens (instâncias de LifePotion) encontráveis na floresta.
        self.weapons_probs = [] # Lista que guardará todas as probabilidades de encontro associadas de cada arma.
        self.others_probs = []  # Lista que guardará todas as probabilidades de encontro associadas de item que não é arma.
        self.items_file = "dbs/items.dat"       # Arquivo que salva todos os dados das instâncias de item.

        self.possible_armors = {}  # Dicionário que conterá tuplas com o nome/descrição/etc das possíveis armaduras do jogo. O item de fato será criado no Blacksmith.
        self.generate_armor()
        loaded = self.server.helper.load_pickle(self.items_file)    # Carrega a database.
        if loaded:
            self.weapons = loaded[0]
            self.others = loaded[1]
        else:       # Se o arquivo é vazio, um novo é criado.
            self.regenerate()

        self.weapons_probs = [weapon.prob for weapon in self.weapons]
        self.others_probs = [other.prob for other in self.others]

    def regenerate(self):
        '''
            Cria um núcleo de itens iniciais que poderão ser encontrados na floresta.
            O núcleo funciona da seguinte forma: toda vez que um jogador encontra um item listado abaixo,
            ele recebe uma cópia deste item no seu inventário e o item original não desaparecerá da floresta.
            Um item só irá desaparecer da floresta (apagado de dbs/items.dat), quando ele for um item lendário.

            Veja o método Encounters.item(chat_id) em forest_encounters.py.
        '''
        # Armas normais.
        newwep = items.Weapon(emojize("wooden sword"), False, "wd_s", 3, [1, 1])
        newwep.description = "A basic sword used for training, don't use this in a real fight."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("branch"), False, "branch1", 4, [1, 2])
        newwep.description = "A branch whose shape resembles a shield with spikes. Not a real weapon."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("branch"), False, "branch2", 4, [2, 1])
        newwep.description = "A branch whose shape resembles a broad sword. Not a real weapon."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("branch"), False, "branch3", 4, [3, 0])
        newwep.description = "A branch whose shape resembles a sharp spike. Not a real weapon."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("branch"), False, "branch4", 4, [0, 3])
        newwep.description = "A branch whose shape resembles a kite shield. Not a real weapon."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("sharp leaf"), False, "sharp", 7, [1, 0])
        newwep.description = "A floppy leaf that looks sharp. Not a real weapon."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("tough bone"), False, "bone", 10, [1, 2])
        newwep.description = "Someone or something died long ago and droped this. Not a real weapon."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("iron sword"), False, "ir_s", 3, [2, 2])
        newwep.description = "A rusty blunt sword. Can be used as a weapon."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("club :baguette_bread:"), False, "club", 3, [1, 2])
        newwep.description = "A heavy club. Barbarians would use this as a weapon."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("fossilized banana :banana:"), False, "bnn", 1, [3, 1])
        newwep.description = "A banana that someone forgot in the bag."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("axe"), False, "a", 2, [4, 0])
        newwep.description = "An old weapon used by the dwarves."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("spear"), False, "sp", 1, [1, 4])
        newwep.description = "Its reach makes it somewhat defensive."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("meteor sword :comet:"), False, "mt_s", 1, [20, 20])
        newwep.description = "A sword crafted long ago with the ore that came from a fallen meteor."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("crossbow"), False, "cr_b", 1, [3, 0])
        newwep.type2 = "ranged"
        newwep.description = "A ranged weapon with high piercing power."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("pickaxe"), False, "pk", 1, [2, 1])
        newwep.description = "A rusty pickaxe used by the dwarves to dig their tunnels in the mountains."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("warhammer"), False, "wh", 1, [3, 3])
        newwep.description = "A heavy weapon."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("dagger"), False, "dg", 1, [2, 0])
        newwep.description = "A short blade used to finish off your opponent."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("leaf sword :leaf_fluttering_in_wind:"), False, "ls", 1, [10, 5])
        newwep.description = "A well crafted sword. Its made of the hardest and sharpest leaves found in the woods."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("fireball launcher :fire:"), False, "fb_l", 1, [25, 9])
        newwep.type2 = "ranged"
        newwep.description = "A magical artifact able to shoot fire projectiles."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("glimmer blade :sparkles:"), False, "Gb", 1, [25, 30])
        newwep.description = "A short blade that glimmers, blinding your opponent."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("flute :musical_notes:"), False, "f", 1, [0, 1])
        newwep.type2 = "magic"
        newwep.description = "A musical instrument. Don't use this as a weapon."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("bow"), False, "bow", 1, [2, 2])
        newwep.type2 = "ranged"
        newwep.description = "A simple bow made of wood."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("mace"), False, "mac", 1, [5, 3])
        newwep.description = "A short melee weapon that can cause a lot of damage. But on this game its just weak."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("morningstar"), False, "m_s", 1, [3, 5])
        newwep.description = "A mace with a chain."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("acid sword"), False, "ac_s", 1, [7, 5])
        newwep.description = "A sword whose blade is made of an acidic ore."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("short sword"), False, "s_s", 1, [2, 4])
        newwep.description = ("A short sword. What, you need more description? Ok!"
                                " It's blade is made of iron and its hilt is made of maple wood. "
                                "The blade is slightly rusted and you see carvings on the hilt."
                                " You don't recognize it's language and it's art style. "
                                "You guess its some sort of dwarven as it got sharp curves"
                                " and a lot of straight lines as the dwarven was a civilization "
                                "that the only remnants of it was its war instruments left of the woods. "
                                "The blade is also carved with runes you don't know the meaning.")
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("very long sword"), False, "vl_s", 1, [5, 0])
        newwep.description = "A short sword but slightly longer."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("needle"), False, "needle", 1, [1, 0])
        newwep.description = "A pin used to sew."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("kite shield"), False, "k_s", 1, [0, 6])
        newwep.description = "A weapon used to defend yourself."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("buckler"), False, "buc", 1, [1, 5])
        newwep.description = "A shield that got a spike in its front. Can hurt someone you just want to defend youserlf."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("protective sphere"), False, "p_s", 1, [0, 40])
        newwep.description = "A giant sphere made of transparent steel you enter inside. Be careful, if you fall down a hill you can get hurt, or very dizzy."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("steam jet"), False, "s_j", 1, [5, 10])
        newwep.type2 = "ranged"
        newwep.description = "A ranged weapon that shots hot steam at its enemies. Can also be a combat airplane. But what is an airplane?"
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("lightning cutlass :high_voltage:"), False, "lght_s", 1, [40, 30])
        newwep.type2 = "magic"
        newwep.description = "A magical sword that casts static."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("frost scimitar :snowflake:"), False, "frt_s", 1, [5, 20])
        newwep.type2 = "magic"
        newwep.description = "A magical artifact that freezes its enemies."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("rainbow cutter :rainbow:"), False, "rb_s", 1, [50, 1])
        newwep.type2 = "magic"
        newwep.description = "A magical weapon able to cut rainbows. Or is it a sword made of rainbow?"
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("full tower shield :shield:"), False, "ft", 1, [0, 10])
        newwep.description = "A large and sturdy defensive shield."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("angelic Excalibur :sunrise_over_mountains:"), False, "exca", 1, [30, 40])
        newwep.description = "A sword crafted in the heavens, no one knows how it was crafted or by who."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("angelic shield :sunrise_over_mountains:"), False, "ang_shd", 1, [0, 70])
        newwep.description = "A shield crafted in the heavens, no one knows how it was crafted or by who."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("demonic spike :angry_face_with_horns:"), False, "dem_sp", 1, [40, 30])
        newwep.description = "An evil looking (weapon?). Can cause a lot of damage. Crafted by devils but no one knows where it was crafted. Only devils knows how it was crafted."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("demonic whip :angry_face_with_horns:"), False, "dem_wp", 1, [70, 0])
        newwep.description = "An evil looking whip. Causes a lot of damage. Crafted by devils but no one knows where it was crafted. Only devils knows how it was crafted."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("cursed ring of rage :ring:"), False, "ring_rage", 1, [2, 0])
        newwep.type2 = "magic"
        newwep.description = "A ring that makes its user very angry."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("cursed ring of protection :ring:"), False, "ring_pro", 1, [-1, 3])
        newwep.type2 = "magic"
        newwep.description = "A ring that makes its user defensive."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("bacon dagger :bacon:"), False, "bacon_dagger", 1, [99, 99])
        newwep.description = "A weapon used by the fat folk. The strongest that can be found at the forest that is not player made."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("alien puzzle :alien_monster:"), False, "al_pz", 1, [0, 0])
        newwep.description = "A puzzle that does not look to belong to this world. (its incredibly hard to solve)."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("cursed toy"), False, "toy", 1, [0, 0])
        newwep.description = "A toy that is embued with an evil aura."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("giant beetle horn :lady_beetle:"), False, "bet_horn", 1, [3, 6])
        newwep.description = "A bettle horn the size of a broad sword. A fossil of a creature that lived on this woods long ago."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("hornet stinger :honeybee:"), False, "hr_str", 1, [6, 3])
        newwep.type2 = "ranged"
        newwep.description = "A machine gun of hornets."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("mosquito swarmer"), False, "msq_swrm", 1, [10, 10])
        newwep.type2 = "ranged"
        newwep.description = "This thing spawns mosquitoes at it's target"
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize("spyglass"), False, "spy_gl", 1, [0, 0])
        newwep.description = "An item used by explorers. But wielding it as a weapon is not a good idea."
        self.weapons.append(newwep)
        newwep = items.Weapon(emojize(":banana: Banana Hammock :banana:"), False, "Lazar", 1, [30, 10])
        newwep.type2 = "ranged"
        newwep.description = "An ancient weapon wielded by etintrof people"
        self.weapons.append(newwep)
        # self.weapons.append(items.Weapon(emojize("Hand of Fate :oncoming_fist:"), False, "punch", 1, [30, 30]))
        # self.weapons.append(items.Weapon(emojize("Fat gun covered in blood :syringe:"), True, "fat_man_leg_wep", 1, [110, 110]))

        # Outros
        self.others.append(items.LifePotion(emojize("Life Potion :wine_glass:"), False, "hp_pot", 1))

        self.save_items()


    def generate_armor(self):
        new_armor = items.Armor(emojize("Simple Clothes"), True, "cloth", 1, {"cold": 1})
        new_armor.description = "Very simple clothing, can warm you just a little bit."
        self.possible_armors[emojize("Simple Clothes")] = new_armor
        new_armor = items.Armor(emojize("Winter Clothes"), True, "w_cloth", 1, {"cold": 2})
        new_armor.description = "Can cut the wind out and warms you, but still no enough to face the deep forest cold."
        self.possible_armors[emojize("Winter Clothes")] = new_armor
        new_armor = items.Armor(emojize("Waterproof Winter Clothes"), True, "w_w_cloth", 1, {"cold": 3})
        new_armor.description = "This one saves you from water from snow that can enter inside your clothes and freeze."
        self.possible_armors[emojize("Waterproof Winter Clothes")] = new_armor
        new_armor = items.Armor(emojize("Full Sweatshirt Set"), True, "swtshirt", 1, {"cold": 4})
        new_armor.description = "The state of the art of warming, with this you can withstand any weather."
        self.possible_armors[emojize("Full Sweatshirt Set")] = new_armor
# ------------------------------------------------------------------------------
    def save_items(self):
        '''
            Salva os itens da database.
        '''
        if not os.path.exists("dbs/"):
            os.makedirs("dbs/")
        self.server.helper.save_pickle([self.weapons, self.others], self.items_file)

    def get_random_weapon(self):
        '''
            Função que escolhe uma arma aleatória da floresta.
        '''
        weapon = rd.choices(self.weapons, self.weapons_probs)[0]    # A probabilidade de encontrar uma arma depende da probabilidade associada a ela.
        # for item in self.weapons:
        #     if item.is_legendary:
        #         weapon = item
        #         print(weapon.name)
        weapon.owner = ""
        weapon.is_shared_and_equipped = False
        return copy.copy(weapon)

    def get_random_other(self):
        '''
            Função que escolhe um item aleatório da floresta.
        '''
        other = rd.choices(self.others, self.others_probs)[0]
        return copy.copy(other)

    def add_weapon_to_pool(self, weapon):
        '''
            Adiciona uma arma na floresta.

            Parâmetros:
                weapon (class): arma a ser adicionado.
        '''
        self.weapons.append(copy.copy(weapon))
        self.weapons_probs.append(weapon.prob)
        self.save_items()

    def remove_weapon_from_pool(self, weapon):
        '''
            Remove uma arma da floresta.

            Parâmetros:
                arma (class): arma a ser removido.
        '''
        i = [weap.code for weap in self.weapons].index(weapon.code)
        self.weapons.remove(self.weapons[i])
        self.weapons_probs.remove(self.weapons_probs[i])
        self.save_items()

    def add_other_to_pool(self, other):
        '''
            Adiciona um item na floresta.

            Parâmetros:
                other (class): item a ser adicionado.
        '''
        self.others.append(copy.copy(other))
        self.others_probs.append(other.prob)
        self.save_items()

    def remove_other_from_pool(self, other):
        '''
            Remove um item da floreta.

            Parâmetros:
                other (class): item a ser removido.
        '''
        i = [item.code for item in self.others].index(other.code)
        self.others.remove(self.others[i])
        self.others_probs.remove(self.others_probs[i])
        self.save_items()
