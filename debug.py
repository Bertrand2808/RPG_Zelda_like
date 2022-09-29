"""
Fichier qui va nous servir de journal des bugs en quelques sortes

(je ne maitrise pas trop la mécanique encore)

"""
##############################
# Importation des librairies #
##############################
import pygame
import logging

pygame.init()
font = pygame.font.Font(None,30)

def debug (info,y = 10, x = 10):
    display_surface = pygame.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(display_surface,'Black', debug_rect)
    display_surface.blit(debug_surf,debug_rect)

def logLancement():
    logging.info(" Lancement du programme ")
def logOk():
    logging.debug(" La fonction a bien été exécutée")

def logBoutonDemarrer():
    logging.debug(" bouton demarrer ")

def logInterfaceDemarrer():
    logging.debug(" J'veux juste game la en fait ")

def logCroix():
    logging.info(" Quitter par la croix ")

def logEchap():
    logging.info(" ECHAP ")
def logSpace():
    logging.info(" ESPACE ")

def logBoutonOption():
    logging.info(" bouton option ")

def logInterfaceOption():
    logging.info(" Bienvenue dans l'interface des options ")

def logBoutonQuitter():
    logging.info(" bouton quitter ")
