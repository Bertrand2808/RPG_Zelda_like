import pygame
from player import *
from settings import *


class Potion:
    def __init__(self, amount=10, heal_amount=10):
        self.name = 'Potion'
        self.sound = list(items_data.keys())[0]
        self.item_sound = pygame.mixer.Sound('E:/Développement/RPG/0.83/assets/audio/heal.mp3')
        self.amount = amount #nombre d'item
        self.heal_amount = heal_amount


    def activate(self):
        self.item_sound.play()

class SuperPotion:
    def __init__(self, amount):
        self.name = 'SuperPotion'
        self.sound = list(items_data.keys())[1]
        self.item_sound = pygame.mixer.Sound('E:/Développement/RPG/0.83/assets/audio/heal.mp3')
        self.amount = amount #nombre d'item

    def activate(self):
        self.item_sound.play()

class SuperBall:
    def __init__(self, amount):
        self.name = 'SuperBall'
        self.sound = list(items_data.keys())[2]
        self.item_sound = pygame.mixer.Sound('E:/Développement/RPG/0.83/assets/audio/SuperEffective.mp3')
        self.amount = amount #nombre d'item

    def activate(self):
        self.item_sound.play()



