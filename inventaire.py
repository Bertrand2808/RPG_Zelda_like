
import pygame
from consommable import Potion, SuperBall, SuperPotion
from player import Player
from particles import *
from numpy import full
from settings import *

class Inventaire:
    X_POSITION = 600
    Y_POSITION = 900
    def __init__(self):
        # GENERAL SETUP
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.item_names = ['Potion', 'SuperPotion', 'SuperBall', 'proutprout']
        self.item_index = 0
        self.items = list(items_data.keys())[self.item_index]
        self.item_number = len(self.item_names)

        # SELECTION SYSTEM
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.reading = False

        # ITEM DIMENSIONS
        self.height = self.screen.get_size()[1] * 0.1 # hauteur de la boite
        self.width = self.screen.get_size()[0] // 7.5 # largeur de la boite
        self.assets_height = self.screen.get_size()[1] * 0.125 # hauteur de la boite
        self.assets_width = self.screen.get_size()[0] // 7.5 # largeur de la boite
        self.description_height = self.screen.get_size()[1] * 0.2 # hauteur de la boite
        self.description_width = self.screen.get_size()[0] // 7 # largeur de la boite
        self.create_items()
        self.create_descriptions()
        self.create_assets()

        # CONVERTIR LE DICTIONNAIRE D'ITEMS
        self.items_graphics = [] # création d'une liste pour pouvoir avoir accès aux images
        for item in items_data.values():
            path = item['graphics'] # On vient chercher uniquement le chemin de l'image de l'item
            item = pygame.image.load(path).convert_alpha()
            self.items_graphics.append(item) # ajouter l'image à la liste

        # DIALOG SYSTEM
        self.box = pygame.image.load('E:/Développement/RPG/0.83/assets/graphics/dialogs/dialog_box.png')
        self.box = pygame.transform.scale(self.box, (1000, 100))
        self.text = []
        self.text_index = 0
        self.letter_index = 0
        self.dialog_font = pygame.font.Font('E:/Développement/RPG/0.83/assets/graphics/dialogs/dialog_font.ttf', 30)
        self.reading = False

        # CLASS DES ITEMS
        self.potion = Potion()
        self.superpotion = SuperPotion(amount=10)
        self.superball = SuperBall(amount=100)


    def execute(self) :
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0
            # self.text = [f"Tu utilises l'objet {self.item_names[self.selection_index]}", "Avoue c'est genial d'utiliser des objets"]
            print(f"L'objet {self.item_names[self.selection_index]} a bien été utilisé")
            if self.item_names[self.selection_index] == 'Potion':
                self.potion.activate()
                self.potion.amount -= 1
                self.text = [f"Tu utilises l'objet {self.item_names[self.selection_index]}", "Avoue c'est genial d'utiliser des objets", f"Potions restantes : {self.potion.amount}"]
                self.activate(self.player, )
            elif self.item_names[self.selection_index] == 'SuperPotion':
                self.superpotion.activate()
                self.superpotion.amount -= 1
                self.text = [f"Tu utilises l'objet {self.item_names[self.selection_index]}", "Avoue c'est genial d'utiliser des objets", f"SuperPotions restantes : {self.superpotion.amount}"]
            elif self.item_names[self.selection_index] == 'SuperBall':
                self.superball.activate()
                self.superball.amount -= 1
                self.text = [f"Tu utilises l'objet {self.item_names[self.selection_index]}", "Avoue c'est genial d'utiliser des objets", f"Superball restantes : {self.superball.amount}"]
            else:
                self.text = [f"Tu utilises l'objet {self.item_names[self.selection_index]}", "Avoue c'est genial d'utiliser des objets"]


    def render(self, screen):

        if self.reading:
            self.letter_index += 1

            if self.letter_index >= len(self.text[self.text_index]):
                self.letter_index = self.letter_index

            screen.blit(self.box, (self.X_POSITION, self.Y_POSITION))
            text = self.dialog_font.render(self.text[self.text_index][0:self.letter_index], False, (0 ,0 ,0))
            screen.blit(text, (self.X_POSITION + 60, self.Y_POSITION + 30))

    def next_text(self):
        self.text_index += 1
        self.letter_index = 0
        if self.text_index >= len(self.text):
            self.reading = False

    def display(self):
        self.input()
        self.selection_cooldown()
        self.interaction = Interaction(self.item_names, self.selection_index)

        for index, item in enumerate(self.item_list):
            # GET ATTRIBUTES
            name = self.item_names[index]
            value = 0
            max_value = 99
            item.display(self.screen, self.selection_index, name, value, max_value, 3)

        for index, item in enumerate(self.description_list):
            # GET ATTRIBUTES
            name = 'description'
            value = 0
            max_value = 99
            item.display(self.screen, self.selection_index, name, value, max_value, 3)

        for index, item in enumerate(self.assets_list):
            # GET ATTRIBUTES
            assets = self.items_graphics[index]
            value = 0
            max_value = 99
            item.display_assets(self.screen, self.selection_index, assets)



    def input(self):
        keys = pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index < self.item_number -1 :
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT]and self.selection_index >= 1 :
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.execute()


    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 600:
                self.can_move = True

    def create_assets(self):
        self.assets_list = []

        for assets, index in enumerate(range(self.item_number)):
            # horizontal pos
            full_width = self.screen.get_size()[0]
            increment = full_width // self.item_number
            left = (assets * increment) + (increment - self.assets_width) // 2
            # vertical pos
            top = self.screen.get_size()[1] * 0.25
            #create the object
            description = Item(left,top, self.assets_width,self.assets_height, index, self.font)
            self.assets_list.append(description)

    def create_descriptions(self):
        self.description_list = []

        for description, index in enumerate(range(self.item_number)):
            # horizontal pos
            full_width = self.screen.get_size()[0]
            increment = full_width // self.item_number
            left = (description * increment) + (increment - self.description_width) // 2
            # vertical pos
            top = self.screen.get_size()[1] * 0.55
            #create the object
            description = Item(left,top, self.description_width,self.description_height, index, self.font)
            self.description_list.append(description)

    def create_items(self):
        self.item_list = []

        for item, index in enumerate(range(self.item_number)):
            # horizontal pos
            full_width = self.screen.get_size()[0]
            increment = full_width // self.item_number
            left = (item * increment) + (increment - self.width) // 2
            # vertical pos
            top = self.screen.get_size()[1] * 0.4
            #create the object
            item = Item(left,top, self.width,self.height, index, self.font)
            self.item_list.append(item)

class Item:
    def __init__(self,l,t,w,h,index,font):
        self.rect = pygame.Rect(l,t,w,h)
        self.index = index
        self.font = font
        self.screen = pygame.display.get_surface()

    def display(self, surface, selection_num, name, value, max_value, cost):
        if self.index == selection_num:
            pygame.draw.rect(surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect,4)
        else:
            pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(surface, UI_BORDER_COLOR, self.rect,4)
        self.display_names(surface, name, cost,self.index == selection_num)

    def display_assets(self, surface, selection_num, assets):
        item_surf = assets
        item_rect = item_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        pygame.draw.rect(surface, UI_BG_COLOR, self.rect)
        surface.blit(item_surf, item_rect)

    def display_names(self, surface, name, cost, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # TITRE
        title_surf = self.font.render(name, False, color)
        title_rect = title_surf.get_rect(midtop = self.rect.midtop + pygame.math.Vector2(0,20))
        surface.blit(title_surf, title_rect)

class Interaction:
    X_POSITION = 590
    Y_POSITION = 940
    def __init__(self, item_names, selection_index):
        self.item_names = item_names
        self.selection_index = selection_index
        self.box = pygame.image.load('E:/Développement/RPG/0.83/assets/graphics/hud/dialogue.png')
        self.box = pygame.transform.scale(self.box, (700, 100))
        self.font = pygame.font.Font('E:/Développement/RPG/0.83/assets/graphics/dialogs/dialog_font.ttf', 20)
        self.texts = [f"Tu utilises l'objet {self.item_names[self.selection_index]}"]
        self.text_index = 0
        self.letter_index = 0
        self.reading = False

    def execute(self):
        self.reading = True
        print("execute")
        print(self.reading)
        if self.reading:
            self.next_text()
        else:
            self.reading = True
            self.text_index = 0

    def render(self, screen):
        self.reading = True
        print("render")
        print(self.reading)
        if self.reading :
            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):
                self.letter_index = self.letter_index
            screen.blit(self.box, (self.X_POSITION , self.Y_POSITION))
            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0 ,0 ,0))
            screen.blit(text, (self.X_POSITION + 50, self.Y_POSITION + 30))

    def next_text(self):
        print("nexttext")
        print(self.reading)
        self.text_index += 1
        self.letter_index = 0
        if self.text_index >= len(self.texts):
            self.reading = False
