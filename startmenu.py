"""
Fichier contenant un prototype de menu démarrer

par Bertrand RENAUDIN
fait le 22/04/22

"""
##############################
# Importation des librairies #
##############################

import pygame, sys
import pygame.draw
import logging

#############################################
# Formattage des logs sous la forme :       #
# DEBUG: 2022-04-25 14:14:02,373 : + texte  #
#############################################

logging.basicConfig(format='%(levelname)s: %(asctime)s : %(message)s', level=logging.DEBUG)

#################################
# Héritages des autres fichiers #
#################################
from settings import *
from debug import *
from startmenu import *
from game import Game
from options import Option


class StartMenu:
    def __init__(self, clock, screen):
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock() # VARIABLE POUR FIXER LES FPS

        # INITIALISATION DES PARAMETRES DES TEXTES DU BOUTONS
        self.color = (255, 255, 255)
        self.color_light = (170,170,170)
        self.color_dark = (100, 100, 100)
        self.font = pygame.font.SysFont('Corbel', 35)

        # RECTANGLE DES BOUTONS DU MENU
        self.play_button = pygame.Rect(640, 210, 200, 50)
        self.options_button = pygame.Rect(640, 410, 200, 50)
        self.escap_button = pygame.Rect(640, 610, 200, 50)


        # TEXTES DES BOUTONS DU MENU
        self.text_demarrer = self.font.render('demarrer', True, self.color)
        self.text_option = self.font.render('options', True, self.color)
        self.text_quit = self.font.render('quitter', True, self.color)

        # ETAT DU CLIQUE (BOOLEEN)
        self.click = False

        # sounds
        self.title_sound = pygame.mixer.Sound('E:/Développement/RPG/0.83/assets/audio/titlescreen.ogg')
        self.title_sound.set_volume(0.1)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        print("Pos souris : ", mouse_pos)

    # AJOUT DE TEXTE INDICATIF (EN HAUT A GAUCHE DE L'ECRAN)
    def draw_text(self, text, font, color, surface, x, y):
        font = pygame.font.SysFont(None, 20)  # type: ignore
        textobj = font.render(text, 1, color)  # type: ignore
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):
        game = Game(self.clock, self.screen)
        option = Option(self.clock, self.screen)

        # BOUCLE DE LA FENETRE DU JEU
        while True:
            # RECUPERATION DE LA POSITION DU CURSEUR EN X, Y
            mx, my = pygame.mouse.get_pos()

        # CONDITIONS RENDANT LES BOUTONS CLIQUABLES
            # BOUTON DEMARRER
            if self.play_button.collidepoint((mx, my)):
                if self.click:
                    self.title_sound.stop()
                    logBoutonDemarrer()
                    game.loop_game()
            # BOUTON OPTIONS
            elif self.options_button.collidepoint((mx, my)):
                if self.click:
                    logBoutonOption()
                    option.loop_options()
            # BOUTON QUITTER
            elif self.escap_button.collidepoint((mx, my)):
                if self.click:
                    logBoutonQuitter()
                    pygame.quit()
                    sys.exit()

            # AJOUT DE L'IMAGE DU BACKGROUND
            self.screen.blit(background, (0,0))
            # AFFICHAGE D'UN TEXTE DE CONFIRMATION "MAIN MENU"
            self.draw_text('main menu', self.font, (255, 255, 255), self.screen, 20, 20)
            self.title_sound.play()

            pygame.draw.rect(self.screen, (255, 0, 0), self.play_button)        #####################################
            self.screen.blit(self.text_demarrer, self.play_button)              #                                   #
            pygame.draw.rect(self.screen, (255, 0, 0), self.options_button)     #      AFFICHAGE DES BOUTONS        #
            self.screen.blit(self.text_option, self.options_button)             #      ET DES TEXTES DES BOUTONS    #
            pygame.draw.rect(self.screen, (255, 0, 0), self.escap_button)       #                                   #
            self.screen.blit(self.text_quit, self.escap_button)                 #####################################

            # ETAT DU CLIQUE (BOOLEEN) SUR FAUX
            self.click = False

            #  CONDITION DE FIN DE BOUCLE
            for event in pygame.event.get():
                if event.type == pygame.QUIT:      # SI ON CLIQUE SUR LA CROIX
                    logOk()                 # ENVOIE LA CONFIRMATION AU TERMINAL
                    logCroix()              # ENVOIE LA CONFIRMATION DE LA CROIX AU TERMINAL
                    pygame.quit()           # ON QUITTE
                    sys.exit()
                if event.type == pygame.KEYDOWN:        # SI ON APPUIE SUR UNE TOUCHE...
                    if event.key == pygame.K_ESCAPE:    # SI C'EST LA TOUCHE ECHAP
                        logEchap()                      # ENVOIE LA CONFIRMATION DE TOUCHE ECHAP AU TERMINAL
                        pygame.quit()                   # ON QUITTE
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:        # CONDITION POUR CAPTER LE CLIQUE
                    if event.button == 1:
                        self.click = True

            pygame.display.update() # RAFRAICHISSEMENT DE LA FENETRE
            self.clock.tick(FPS)
