import pygame
from settings import *

class UI:
    def __init__(self):

        # GENERAL
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # BAR SETUP
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)

        # CONVERTIR LE DICTIONNAIRE D'ARMES
        self.weapon_graphics = [] # création d'une liste pour pouvoir avoir accès aux images
        for weapon in weapon_data.values():
            path = weapon['graphics'] # On vient chercher uniquement le chemin de l'image de l'arme
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon) # ajouter l'image à la liste

        #  CONVERTIR LE DICTIONNAIRE DE MAGIE
        self.magic_graphics = [] # création d'une liste pour pouvoir avoir accès aux images
        for magic in magic_data.values():
            path = magic['graphic'] # On vient chercher uniquement le chemin de l'image de la magie
            magic = pygame.image.load(path).convert_alpha()
            self.magic_graphics.append(magic) # ajouter l'image à la liste



    def show_bar(self, current_amount, max_amount, bg_rect, color):

        # DRAW BACKGROUND
        pygame.draw.rect(self.screen, UI_BG_COLOR, bg_rect)

        # CONVERTIR LES STATS EN PIXELS
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # DRAWING THE BAR
        pygame.draw.rect(self.screen,color, current_rect)
        pygame.draw.rect(self.screen,UI_BORDER_COLOR, bg_rect,3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.screen.get_size()[0] - 20
        y = self.screen.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.screen, UI_BG_COLOR, text_rect.inflate(20,20))
        self.screen.blit(text_surf,text_rect)
        pygame.draw.rect(self.screen, UI_BORDER_COLOR, text_rect.inflate(20,20), 3)

    def selection_box(self, left, top, has_switched): # AFFICHAGE DES RECTANGLES
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.screen, UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.screen, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.screen, UI_BORDER_COLOR, bg_rect, 3)

        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10,980, has_switched) # Rectangle pour affichage de l'arme
        weapon_surf = self.weapon_graphics[weapon_index] # On va chercher l'image de l'arme correspondante (actuelle)
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center) # On affiche l'image dans le rectangle prévu
        self.screen.blit(weapon_surf, weapon_rect)

    def magic_overlay(self,magic_index, has_switched):
        bg_rect = self.selection_box(80,985, has_switched) # MAGIC
        magic_surf = self.magic_graphics[magic_index] # On va chercher l'image de la magie correspondante (actuelle)
        magic_rect = magic_surf.get_rect(center = bg_rect.center)
        self.screen.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR) # Affichage de la barre santé
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR) # Affichage de la barre énergie

        self.show_exp(player.exp) # Affichage de l'expérience
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon) # Affichage de l'arme
        self.magic_overlay(player.magic_index, not player.can_switch_magic) # Affichage de la magie
