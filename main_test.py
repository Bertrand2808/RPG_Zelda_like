from tkinter import E
import pygame

from menu_test import MENU_TEST
from settings import *

class Game:
    def __init__(self):
        #créer la fenetre du jeu
        screen_largeur = 720
        screen_hauteur = 1280
        self.screen = pygame.display.set_mode((screen_hauteur, screen_largeur))
        self.game_paused = False



    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        clock = pygame.time.Clock()

            #boucle du jeu
        self.running = True
        self.menu_test = MENU_TEST()

        while self.running:

            if self.game_paused:
                self.menu_test.display()
                self.menu_test.render(self.screen)
                    #  CONDITION DE FIN DE BOUCLE
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                            self.game_paused = False # REPASSER game_paused = FALSE
                        # if event.key == pygame.K_SPACE:
                        #     self.menu_test.execute()
            else:
                self.screen.fill('green')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_m:
                        self.toggle_menu()
            clock.tick(60)
            pygame.display.flip()

if __name__ == '__main__':
    #Initialise Pygame
    pygame.init()
    #Initialise note Game.py
    game = Game()
    game.run()

