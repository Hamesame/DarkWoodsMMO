###############################################
#  Classe que segura os teclados do Telegram  #
###############################################

from emoji import emojize
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class Keyboards:
    def __init__(self):
        main_menu_custom_keyboard = [           # Keyboard básico do menu principal (não mais usado)
            [
                emojize(":deciduous_tree: Forest :deciduous_tree:"), emojize(":green_heart: Health :green_heart:")
            ], [
                emojize(":trophy: Me :trophy:"), emojize(":ledger: Bestiary :ledger:")
            ], [
                emojize(":school_satchel: Inventory :school_satchel:"), emojize(":busts_in_silhouette: Party :busts_in_silhouette:")
            ]
        ]
        self.main_menu_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=main_menu_custom_keyboard, resize_keyboard=True)


        class_main_menu_custom_keyboard = [     # Keyboard básico do menu principal
            [
                emojize(":deciduous_tree: Forest :deciduous_tree:"), emojize(":green_heart: Health :green_heart:")
            ], [
                emojize(":trophy: Me :trophy:"), emojize(":fleur-de-lis: Class :fleur-de-lis:")
            ], [
                emojize(":school_backpack: Inventory :school_backpack:"), emojize(":busts_in_silhouette: Party :busts_in_silhouette:")
            ]

        ]
        self.class_main_menu_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=class_main_menu_custom_keyboard, resize_keyboard=True)

        at_camp_main_menu_custom_keyboard = [     # Keyboard básico do menu principal
            [
                emojize(":deciduous_tree: Forest :deciduous_tree:"), emojize(":green_heart: Health :green_heart:")
            ], [
                emojize(":trophy: Me :trophy:"), emojize(":fleur-de-lis: Class :fleur-de-lis:")
            ], [
                emojize(":school_backpack: Inventory :school_backpack:"), emojize(":busts_in_silhouette: Party :busts_in_silhouette:")
            ], [
                emojize(":crossed_swords: Arena :crossed_swords:")
            ]

        ]
        self.at_camp_main_menu_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=at_camp_main_menu_custom_keyboard, resize_keyboard=True)



        bs_custom_keyboard = [                  # Keyboard do blacksmith com yes ou nope (também usado em dungeons)
            [
                emojize("YES :thumbs_up:"),
                emojize("NOPE :thumbs_down:")
            ]
        ]
        self.bs_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=bs_custom_keyboard, resize_keyboard=True)


        lvl_up_vanilla_custom_keyboard = [                          # Keyboard de levelup de jogadores sem classe
            [emojize(":crossed_swords: Attack :crossed_swords:")],
            [emojize(":shield: Defense :shield:")]
        ]
        self.lvl_up_vanilla_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=lvl_up_vanilla_custom_keyboard, resize_keyboard=True)


        lvl_up_knight_custom_keyboard = [                                   # Keyboard de levelup do knight
            [emojize(":crossed_swords: Critical chance :crossed_swords:")],
            [emojize(":crossed_swords: Weapon strength boost :crossed_swords:")]
        ]
        self.lvl_up_knight_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=lvl_up_knight_custom_keyboard, resize_keyboard=True)


        lvl_up_druid_custom_keyboard = [                                   # Keyboard de levelup do druida
            [emojize(":dizzy: Max. Mana :dizzy:")],
            [emojize(":wolf_face: Max. tamed beasts :wolf_face:")]
        ]
        self.lvl_up_druid_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=lvl_up_druid_custom_keyboard, resize_keyboard=True)


        lvl_up_explorer_custom_keyboard = [                                   # Keyboard de levelup do explorer
            [emojize(":game_die: Rare chance :game_die:")],
            [emojize(":warning: More encounters :warning:")]
        ]
        self.lvl_up_explorer_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=lvl_up_explorer_custom_keyboard, resize_keyboard=True)


        lvl_up_wizard_custom_keyboard = [                                   # Keyboard de levelup do wizard
            [emojize(":dizzy: Max. Mana :dizzy:")],
            [emojize(":open_book: Spell Power :open_book:")]
        ]
        self.lvl_up_wizard_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=lvl_up_wizard_custom_keyboard, resize_keyboard=True)


        choose_class_custom_keyboard = [                            # Keyboard de escolha de classe
            [
                emojize(":crossed_swords: Knight :crossed_swords:"),
                emojize(":deciduous_tree: Druid :deciduous_tree:")
            ],
            [
                emojize(":telescope: Explorer :telescope:"),
                emojize(":mage: Wizard :mage:")
            ]
        ]
        self.choose_class_markup = telegram.ReplyKeyboardMarkup(keyboard=choose_class_custom_keyboard, resize_keyboard=True)


        forest_return_custom_keyboard = [       # Keyboard de retorna da floresta
            [
                emojize('yes'),
                emojize('no')
            ]
        ]
        self.forest_return_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=forest_return_custom_keyboard, resize_keyboard=True)


        time_custom_keyboard = [            # Keyboard com os tempos disponíveis para veiagnes na floresta
            [
                emojize('1 hour'),
                emojize('4 hours')
            ], [
                emojize('8 hours'),
                emojize('12 hours')
            ], [
                emojize('Back')
            ]
        ]
        self.time_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=time_custom_keyboard, resize_keyboard=True)

        retrace_steps_keyboard = [
            [
                emojize(':paw_prints: Retrace steps :paw_prints:'),
                emojize('Give it up')
            ]
        ]
        self.retrace_steps_markup = telegram.ReplyKeyboardMarkup(keyboard = retrace_steps_keyboard, resize_keyboard = True)


        lvl_up_class_kb = [
            [
                emojize(":flexed_biceps: Strength :flexed_biceps:")
            ], [
                emojize(":brain: Intelligence :brain:")
            ], [
                emojize(":eye: Dexterity :eye:")
            ]
        ]
        self.lvl_up_class_kb = telegram.ReplyKeyboardMarkup(keyboard = lvl_up_class_kb, resize_keyboard = True)


        bs_type_custom_keyboard = [
            [
                emojize(":crossed_swords: Melee :crossed_swords:")
            ], [
                emojize(":crystal_ball: Magic :crystal_ball:")
            ], [
                emojize(":bow_and_arrow: Ranged :bow_and_arrow:")
            ]
        ]
        self.bs_type_custom_keyboard = telegram.ReplyKeyboardMarkup(keyboard = bs_type_custom_keyboard, resize_keyboard = True)

        arena_lobby_custom_keyboard = [           # Keyboard básico do menu principal (não mais usado)
            [
                emojize(":crossed_swords: Common Arena :crossed_swords:")
            ], [
                emojize(":fire: Ranked Arena :fire:")
            ], [
                emojize(":BACK_arrow: Back :BACK_arrow:")
            ]
        ]
        self.arena_lobby_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=arena_lobby_custom_keyboard, resize_keyboard=True)

        rankings_keyboard = [
            [
                emojize(":bust_in_silhouette: :crossed_swords:️ Player Arena Rankings :crossed_swords:️ :bust_in_silhouette:")
            ], [
                emojize(":bust_in_silhouette: Global Rankings for Players :bust_in_silhouette:")
            ], [
                emojize(":busts_in_silhouette: Global Rankings for Parties :busts_in_silhouette:")
            ], [
                emojize(":incoming_envelope: Invitation Number Rankings :incoming_envelope:")
            ], [
                emojize(":BACK_arrow: Back :BACK_arrow:")
            ]
        ]

        inline_rankings_keyboard = [
            [
                InlineKeyboardButton(emojize(":bust_in_silhouette: :crossed_swords:️ Player Arena Rankings :crossed_swords:️ :bust_in_silhouette:"), callback_data = emojize(":bust_in_silhouette: :crossed_swords:️ Player Arena Rankings :crossed_swords:️ :bust_in_silhouette:"))
            ], [
                InlineKeyboardButton(emojize(":bust_in_silhouette: Global Rankings for Players :bust_in_silhouette:"), callback_data = emojize(":bust_in_silhouette: Global Rankings for Players :bust_in_silhouette:"))
            ], [
                InlineKeyboardButton(emojize(":busts_in_silhouette: Global Rankings for Parties :busts_in_silhouette:"), callback_data = emojize(":busts_in_silhouette: Global Rankings for Parties :busts_in_silhouette:"))
            ], [
                InlineKeyboardButton(emojize(":incoming_envelope: Invitation Number Rankings :incoming_envelope:"), callback_data = emojize(":incoming_envelope: Invitation Number Rankings :incoming_envelope:"))
            ], [
                InlineKeyboardButton(emojize(":evergreen_tree: Lasted longer in the deep forest :evergreen_tree:"), callback_data = emojize(":evergreen_tree: Lasted longer in the deep forest :evergreen_tree:"))
            ], [
                InlineKeyboardButton(emojize(":BACK_arrow: Back :BACK_arrow:"), callback_data = emojize(":BACK_arrow: Back :BACK_arrow:"))
            ]
        ]

        inline_sort_by_keyboard = [
            [
                InlineKeyboardButton(emojize(":crossed_swords:️ Attack :crossed_swords:️"), callback_data = emojize(":crossed_swords:️ Attack :crossed_swords:️")),
                InlineKeyboardButton(emojize(":shield: Defense :shield:"), callback_data = emojize(":shield: Defense :shield:"))
            ], [
                InlineKeyboardButton(emojize(":crossed_swords: :shield: Total Stats :shield: :crossed_swords:️"), callback_data = emojize(":crossed_swords: :shield: Total Stats :shield: :crossed_swords:️")),
                InlineKeyboardButton(emojize(":BACK_arrow: Back :BACK_arrow:"), callback_data = emojize(":BACK_arrow: Back :BACK_arrow:"))
            ]
        ]

        sort_by_keyboard = [
            [
                emojize(":crossed_swords:️ Attack :crossed_swords:️"),
                emojize(":shield: Defense :shield:")
            ], [
                emojize(":crossed_swords: :shield: Total Stats :shield: :crossed_swords:️"),
                emojize(":BACK_arrow: Back :BACK_arrow:")
            ]
        ]

        self.inline_sort_by_keyboard_reply_markup = InlineKeyboardMarkup(inline_sort_by_keyboard)

        self.inline_rankings_keyboard_reply_markup = InlineKeyboardMarkup(inline_rankings_keyboard)

        self.rankings_keyboard_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=rankings_keyboard, resize_keyboard=True)

        self.sort_by_keyboard_reply_markup = telegram.ReplyKeyboardMarkup(keyboard=sort_by_keyboard, resize_keyboard=True)
        # ----------------------------------------------------------------------
        inline_dg_keyboard = [
            [
                InlineKeyboardButton(emojize("YES :thumbs_up:"), callback_data = emojize("YES :thumbs_up:")),
                InlineKeyboardButton(emojize("NOPE :thumbs_down:"), callback_data = emojize("NOPE :thumbs_down:"))
            ]
        ]

        self.inline_dg_reply_markup = InlineKeyboardMarkup(inline_dg_keyboard)

        bs_keyboard = [
            [
                emojize("Forge Weapon"),
                emojize("Forge Armor")
            ],
            [
                emojize("Apply talismans"),
                emojize("Exit")
            ]
        ]

        self.bs_keyboard_reply_markup = telegram.ReplyKeyboardMarkup(keyboard = bs_keyboard, reize_keyboard = True)

    def return_proper_keyboard_based_on_location(self, caller):
        if caller.location == "camp":
            return self.at_camp_main_menu_reply_markup
        else:
            return self.class_main_menu_reply_markup

    def create_keyboard_from_list(self, lista):
        matrix = []
        for item in lista:
            matrix.append([emojize(str(item))])

        return telegram.ReplyKeyboardMarkup(keyboard = matrix, resize_keyboard = True)

    def create_keyboard_from_player(self, jogador):
        matrix = [[]]
        hp = jogador.hp
        i = 0
        linha = 0
        coluna = 0
        while i < len(hp):
            if coluna == 3:
                linha += 1
                coluna = 0
                matrix.append([])
            matrix[linha].append(hp[i].name)
            coluna += 1
            i += 1

        return telegram.ReplyKeyboardMarkup(keyboard = matrix, resize_keyboard = True)
