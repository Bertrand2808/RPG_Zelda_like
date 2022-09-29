import pygame, sys
from support import import_csv_layout
from debug import *
from settings import *

class Option:
    def __init__(self,clock, screen):
        self.screen = screen
        self.clock = clock

        ######################################
        #   FONCTION DU MENU OPTIONS          #
        #    APRES AVOIR CLIQUER SUR OPTIONS   #
        #########################################
    def loop_options(self):

        logInterfaceOption() # ENVOIE LA CONFIRMATION AU TERMINAL
        self.running = True # ON PASSE L'ETAT RUNNING = TRUE

        while self.running:
            self.screen.fill((0,0,0))

            #  CONDITION DE FIN DE BOUCLE
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logOk()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        logEchap()
                        self.running = False # REPASSER RUNNING = FALSE

            pygame.display.update() # RAFRAICHISSEMENT DE LA FENETRE
            self.clock.tick(FPS)
