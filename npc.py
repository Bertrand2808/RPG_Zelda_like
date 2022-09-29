import pygame

from entity import Entity
from dialog_test import DialogBoxTest

class NPC(Entity):
    def __init__(self, name, pos, groups):

        # general setup
        super().__init__(groups)
        # self.npc_sprites = npc_sprites
        self.sprite_type = 'npc'
        self.name = name
        self.image = pygame.image.load(f'E:/Développement/RPG/0.83/assets/graphics/pnjs/{name}.png').convert_alpha()
        self.pos = pos
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-26)
        self.dialog_box = DialogBoxTest()




    def get_image(self, x, y):
        image = pygame.Surface([64,64])
        image.blit(self.sprite_sheet, (0,0), (x, y, 64, 64))
        return image

    def get_player_distance_direction(self,player):
        npc_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - npc_vec).magnitude()

        if distance > 0:
            direction = (player_vec - npc_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)


