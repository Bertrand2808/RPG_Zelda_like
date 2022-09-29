import pygame
from debug import *
from dialog import *
from entity import Entity
from settings import *
from support import import_folder



class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, items):
        super().__init__(groups)
        self.image = pygame.image.load('E:/Développement/RPG/0.83/assets/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])

        # SETUP GRAPHICS
        self.import_player_assets()
        self.status = 'down'

        # MOUVEMENT
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites
        self.dialog_box = DialogBox()

        # ARMES
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # MAGIQUE
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        self.items = items
        
        # STATS
        self.stats = {'health' : 100, 'energy':60, 'attack' : 10, 'magic' : 4, 'speed': 5}
        self.max_stats = {'health' : 300, 'energy':140, 'attack' : 20, 'magic' : 10, 'speed': 12}
        self.upgrade_cost = {'health' : 100, 'energy':100, 'attack' : 100, 'magic' : 100, 'speed': 100}
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy'] * 0.8
        self.speed = self.stats['speed']
        self.exp = 500

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # IMPORT SOUND
        self.weapon_attack_sound = pygame.mixer.Sound('E:/Développement/RPG/0.83/assets/audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.4)

    def activate_items(self, player, heal_amount):
        if player.health >=player.stats['health']:
                player.health = player.stats['health']
        else:
            player.health += heal_amount

    def import_player_assets(self):
        character_path = 'E:/Développement/RPG/0.83/assets/graphics/player/'
        self.animations = {'up':[], 'down':[], 'left':[], 'right':[],
            'right_idle':[], 'left_idle':[], 'up_idle':[], 'down_idle':[],
            'right_attack':[], 'left_attack':[], 'up_attack':[], 'down_attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    # FONCTION DE PRISE EN COMPTE DES TOUCHES DU CLAVIER
    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # MOUVEMENT
            if keys[pygame.K_UP]:
                self.status = 'up'
                self.direction.y = -1
            elif keys[pygame.K_DOWN]:
                self.status = 'down'
                self.direction.y = 1
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.status = 'right'
                self.direction.x = 1
            elif keys[pygame.K_LEFT]:
                self.status = 'left'
                self.direction.x = -1
            else:
                self.direction.x = 0

            # ATTAQUE
            if keys[pygame.K_SPACE]:
                logSpace()
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()


            # MAGIQUE
            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strength, cost)
            # SWITCH WEAPONS
            if keys[pygame.K_a] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        # sourcery skip: de-morgan, merge-else-if-into-elif, move-assign-in-block, swap-nested-ifs

        # IDLE STATUS
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def animate(self):
        animation = self.animations[self.status]

        # LOOP OVER THE FRAME INDEX
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # SET THE IMAGE
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(256)

    # FONCTION DE DEPLACEMENT DU PERSONNAGE
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    # GESTION DES COLLISIONS
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # ALLER A DROITE
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # ALLER A GAUCHE
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # ALLER EN BAS
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # ALLER EN HAUT
                        self.hitbox.top = sprite.hitbox.bottom

    def npc_collisions(self, dialog_box):
        for sprite in self.npc_sprites:
            if self.collision('horizontal') or self.collision('vertical'):
                dialog_box.execute()

    def colldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True
        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]
    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]


    def energy_recovery(self):
        if self.energy < self.stats['energy']:
            self.energy += 0.01 * self.stats['magic']
        else:
            self.energy = self.stats['energy']

    def update(self):
        self.input()
        self.colldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()
