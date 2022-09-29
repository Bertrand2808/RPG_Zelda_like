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
from startmenu import StartMenu
import logging

#############################################
# Formattage des logs sous la forme :       #
# DEBUG: 2022-04-25 14:14:02,373 : + texte  #
#############################################

logging.basicConfig(format='%(levelname)s: %(asctime)s : %(message)s', level=logging.DEBUG)

class GamePreset:
    def __init__(self):
        # INITIALISATION DE LA FENETRE
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # TITRE DU JEU
        pygame.display.set_caption('TITRE DU JEU')
        self.clock = pygame.time.Clock() # VARIABLE POUR FIXER LES FPS

    def run(self):
        start_menu = StartMenu(self.clock, self.screen)
        logLancement()
        # BOUCLE DE LA FENETRE DU JEU
        while True:
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

            pygame.display.update() # RAFRAICHISSEMENT DE LA FENETRE
            self.clock.tick(FPS)
            start_menu.main_menu()

    def run_test(self):
        while True:
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

            pygame.display.update() # RAFRAICHISSEMENT DE LA FENETRE
            self.clock.tick(FPS)

