"""
Fichier qui va contenir toutes nos fonctions de lancement de la fenêtre
pour soulager le fichier main.py

#version 0.2
#25/04/22

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
from consommable import *
from debug import *
from dialog import DialogBox
from enemy import Enemy
from entity import Entity
from inventaire import Inventaire
from magic import MagicPlayer
from npc import NPC
from particles import AnimationPlayer
from player import Player
from random import choice, randint
from settings import *
from startmenu import *
from support import *
from tile import Tile
from ui import *
from upgrade import Upgrade
from weapon import Weapon


################
#  Classe Game #
################
class Game:

    def __init__(self, clock, screen):
        pygame.init()
        self.screen = screen
        self.clock = clock
        self.game_paused = False
        self.pause_inventory = False

        # SETUP SPRITE GROUP
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()

        # ATTACK SPRITES
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # USER INTERFACE
        self.ui = UI()
        self.dialog_box = DialogBox()
        self.inventaire = Inventaire()


        # SPRITE SETUP
        self.create_map()

        # PARTICLES
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        # SOUND
        self.main_sound = pygame.mixer.Sound('E:/Développement/RPG/0.83/assets/audio/main.ogg')
        self.main_sound.set_volume(0.1)
        self.title_sound = pygame.mixer.Sound('E:/Développement/RPG/0.83/assets/audio/titlescreen.ogg')
        self.title_sound.set_volume(0.1)

    # CREATION DE LA MAP
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('E:/Développement/RPG/0.83/assets/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('E:/Développement/RPG/0.83/assets/map/map_Grass.csv'),
            'object': import_csv_layout('E:/Développement/RPG/0.83/assets/map/map_Objects.csv'),
            'entities': import_csv_layout('E:/Développement/RPG/0.83/assets/map/map_Entities.csv'),
            #'terrain' : import_csv_layout('E:/Développement/RPG/0.83/assets/levels/0/level0_terrain.csv'),
        }
        graphics = {
            'grass' : import_folder('E:/Développement/RPG/0.83/assets/graphics/Grass'),
            'objects' : import_folder('E:/Développement/RPG/0.83/assets/graphics/Objects'),
            # 'terrain' : import_cut_graphics('E:/Développement/RPG/0.83/assets/graphics/tilemap/test.png'),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        # AJOUTE SUR LA MAP LES SPRITES DE MURS INVISIBLES
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        # AJOUTE SUR LA MAP LES HERBES ET LES ARBRES
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile(
                                (x,y),
                                [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites],
                                'grass',
                                random_grass_image)
                        if style == 'terrain':
                            terrain_tile_list = import_cut_graphics('E:/Développement/RPG/0.83/assets/graphics/tilemap/test.png')
                            tile_surface = terrain_tile_list[int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'terrain', tile_surface)
                        # AJOUTE SUR LA MAP LES OBJETS
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites,self.obstacle_sprites], 'object', surf )

                        # AJOUTE LES ENNEMIES
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                (x,y),
                                [self.visible_sprites],
                                self.obstacle_sprites,
                                self.create_attack,
                                self.destroy_attack,
                                self.create_magic,
                                self.items)
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name ='raccoon'
                                else: monster_name = 'squid'

                                Enemy(
                                    monster_name,
                                    (x,y),
                                    [self.visible_sprites,self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp)

                                NPC('paul', (1950,1400), [self.visible_sprites, self.npc_sprites, self.obstacle_sprites])
                                NPC('robin', (2100,1400), [self.visible_sprites, self.npc_sprites, self.obstacle_sprites])

    # AFFICHAGE DES ARMES LORS D'UNE ATTAQUE
    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])
        elif style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    # SUPPRESSION DES SPRITES APRES ATTAQUE
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])

    def add_exp(self, amount):
        self.player.exp += amount


    def toggle_menu(self):
        self.game_paused = not self.game_paused
    def inventory_menu(self):
        self.pause_inventory = not self.pause_inventory

        #####################################
        # FONCTION DU LANCEMENT DU JEU       #
        #   APRES AVOIR CLIQUER SUR DEMARRER  #
        ########################################

    def loop_game(self):
        logInterfaceDemarrer() # ENVOIE LA CONFIRMATION AU TERMINAL
        self.running = True # ON PASSE L'ETAT RUNNING = TRUE
        self.upgrade = Upgrade(self.player)
        if self.running:
            self.main_sound.play(loops = -1)

        while self.running:
            # BOUCLE PRINCIPALE DU JEU
            self.screen.fill(WATER_COLOR)
            self.visible_sprites.custom_draw(self.player)
            self.ui.display(self.player)

            # MENU PAUSE
            if self.game_paused:
                self.upgrade.display()

                #  CONDITION DE FIN DE BOUCLE
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # QUITTER LE PROGRAMME
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_m:
                            # QUITTER LE MENU PERSONNAGE
                            self.game_paused = False
            # MENU INVENTAIRE
            if self.pause_inventory:
                self.inventaire.display()
                self.inventaire.render(self.screen)
                #  CONDITION DE FIN DE BOUCLE
                for event in pygame.event.get():
                    # QUITTER LE PROGRAMME
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                            # QUITTER LE MENU INVENTAIRE
                            self.pause_inventory = False
            else:
                # BOUCLE DU JEU
                self.visible_sprites.update()
                self.visible_sprites.enemy_update(self.player)
                self.player_attack_logic()
                self.dialog_box.render(self.screen)


            #  CONDITION DE FIN DE BOUCLE
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    logOk()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        self.inventory_menu()
                    if event.key == pygame.K_m:
                        self.toggle_menu()
                    if event.key == pygame.K_ESCAPE:
                        logEchap()
                        self.running = False # REPASSER RUNNING = FALSE
                        self.main_sound.stop()
                    if event.key == pygame.K_RETURN:
                        Entity.test_npc_collisions(self)

            pygame.display.update() # RAFRAICHISSEMENT DE LA FENETRE
            self.clock.tick(FPS)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        print("Pos souris : ", mouse_pos)

##################
#  Classe CAMERA #
##################
class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # GENERAL SETUP
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.half_width = self.screen.get_size()[0] // 2
        self.half_height = self.screen.get_size()[1] // 2

        # CREATING THE FLOOR
        self.floor_surf = pygame.image.load('E:/Développement/RPG/0.83/assets/graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))


    def custom_draw(self, player):

        # GETTING THE OFFSET
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # DRAWING THE FLOOR
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.screen.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_pos)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
