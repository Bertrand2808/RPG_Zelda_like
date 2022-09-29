"""
Première version du fichier principal du RPG

Par RENAUDIN Bertrand et LEDUC Quentin

Commencé le 21/04/2022

PENSER A BIEN COMMENTER LE TEXTE POUR FACILITER LA COMPREHENSION

"""

##############################
# Importation des librairies #
##############################

#################################
# Héritages des autres fichiers #
#################################

from game_preset import *

#################################
#     LANCEMENT DU JEU          #
#################################
if __name__ == '__main__':
    windows = GamePreset()
    windows.run()


