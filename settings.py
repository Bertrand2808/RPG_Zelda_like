"""
Ici seront consignés tous les paramètres de notre jeu afin
de pouvoir en avoir l'accès rapidement

par Bertrand
le 21/04/2022
r
"""


#  chemin pc boulot :  C:/Users/bertr/Documents/Programmation/RPG-main/0.82/0.82/assets/
#  chemin pc maison :  E:/Développement/RPG/0.83/assets/
import pygame, sys
pygame.init()

#############
#   SETUP   #
#############

WIDTH = 1920
HEIGHT = 1080
FPS = 40
HITBOX_OFFSET = {
    'player': -26,
    'object': -40,
    'grass': -10,
    'invisible': 0
}

# IMAGE BACKGROUND
background = pygame.image.load('E:/Développement/RPG/0.83/assets/graphics/background/background01.jpg')
# MUSIQUE DU MENU
THEME = pygame.mixer.Sound('E:/Développement/RPG/0.83/assets/audio/theme.mp3')

# IMAGE IN-GAME
BANNER = pygame.image.load('E:/Développement/RPG/0.83/assets/graphics/background/background02.jpg')
# IMAGE OPTIONS
Option_background = pygame.image.load('E:/Développement/RPG/0.83/assets/graphics/background/061.PNG')


TILESIZE = 64
# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = 'E:/Développement/RPG/0.83/assets/graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# GENERAL COLORS
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# UI COLORS
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

# WEAPON DATA
weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphics': 'E:/Développement/RPG/0.83/assets/graphics/weapons/sword/full.png'},
    'lance': {'cooldown': 400, 'damage': 30, 'graphics': 'E:/Développement/RPG/0.83/assets/graphics/weapons/lance/full.png'},
    'axe': {'cooldown': 300, 'damage': 20, 'graphics': 'E:/Développement/RPG/0.83/assets/graphics/weapons/axe/full.png'},
    'rapier': {'cooldown': 50, 'damage': 8, 'graphics': 'E:/Développement/RPG/0.83/assets/graphics/weapons/rapier/full.png'},
    'sai': {'cooldown': 80, 'damage': 10, 'graphics': 'E:/Développement/RPG/0.83/assets/graphics/weapons/sai/full.png'},
}

# magic
magic_data = {
    'flame': {'strength': 5,'cost': 20,'graphic':'E:/Développement/RPG/0.83/assets/graphics/particles/flame/fire.png'},
    'heal' : {'strength': 20,'cost': 10,'graphic':'E:/Développement/RPG/0.83/assets/graphics/particles/heal/heal.png'}}

# enemy
monster_data = {
    'squid': {'health': 100,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'E:/Développement/RPG/0.83/assets/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
    'raccoon': {'health': 300,'exp':250,'damage':40,'attack_type': 'claw',  'attack_sound':'E:/Développement/RPG/0.83/assets/audio/attack/claw.wav','speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
    'spirit': {'health': 100,'exp':110,'damage':8,'attack_type': 'thunder', 'attack_sound':'E:/Développement/RPG/0.83/assets/audio/attack/fireball.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
    'bamboo': {'health': 70,'exp':120,'damage':6,'attack_type': 'leaf_attack', 'attack_sound':'E:/Développement/RPG/0.83/assets/audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}

# ITEMS DATA
items_data = {
    'Potion': {'heal': 15, 'sound':'E:/Développement/RPG/0.83/assets/audio/heal.mp3','graphics': 'E:/Développement/RPG/0.83/assets/graphics/item/Potion.png'},
    'SuperPotion': {'heal': 30, 'sound':'E:/Développement/RPG/0.83/assets/audio/heal.mp3','graphics': 'E:/Développement/RPG/0.83/assets/graphics/item/SuperPotion.png'},
    'SuperBall': {'exp': 20,'sound':'E:/Développement/RPG/0.83/assets/audio/SuperEffective.mp3' ,'graphics': 'E:/Développement/RPG/0.83/assets/graphics/item/SuperBall.png'},
    'proutprout' : {'exp': 20, 'sound':'E:/Développement/RPG/0.83/assets/audio/tackle.mp3','graphics': 'E:/Développement/RPG/0.83/assets/graphics/item/proutprout.png'},
}
npc_data ={
    'paul' : {'pos': (1950,1400), 'dialog' : ["Quoi de neuf les loulous","C'est novateck","Yo tout le monde !"]},
    'robin' :{'pos': (2100,1400), 'dialog' :["Moi ça va impecc !", "Bonjour, comment ça va ici ?"]},
}


