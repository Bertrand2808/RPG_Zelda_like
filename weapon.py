"""
Fichier gérant les armes


Commencé le 28/04/2022


"""

##############################
# Importation des librairies #
##############################
import pygame

##################
#  Classe WEAPON #
##################
class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]

        # GRAPHICS
        full_path = f'E:/Développement/RPG/0.83/assets/graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        # PLACEMENT
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))

