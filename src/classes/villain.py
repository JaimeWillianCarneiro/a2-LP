import pygame as pg
from src.classes.character import Character
from src.classes.gameobejcts import Ammunition
from src.settings import FRAME_RATE
import numpy as np


class Villain(Character):
    def __init__(self, name, speed, perception, x_position, y_position, width, height, direction, skin,
                 life, damage, mem_size, vision_field, attack_field, sprites_quantity, background, scooby_snacks, scope, ammunition, bullets, reload_time):
        super().__init__(name, speed, perception, x_position, y_position, width, height, direction, skin, sprites_quantity, list(background.get_shape()), scope, ammunition, bullets, reload_time)
        self._life = life
        self._damage = damage
        self._memories = []
        self._mem_size = mem_size
        self._vision_field = pg.Rect(x_position - vision_field, y_position - vision_field, 2*vision_field, 2*vision_field)
        self._attack_field = pg.Rect(x_position - attack_field, y_position - attack_field, 2*attack_field, 2*attack_field)
        self.scooby_snacks = scooby_snacks
        self.map_limits_sup = list(background.get_shape())

    def aim_function(self, player, movement):
        fired = []
        self.aim = movement
        # Atira no personagem caso ele esteja na mira e tenha recarregado
        self.reload += 1
        if self.aim.any():
            if player.rect.clipline(self.rect.center, np.array(self.rect.center) + self.aim*self.scope/np.linalg.norm(self.aim)) and self.check_load():
                bullet = self.instanciate_bullet(x_position=self.x_position, y_position=self.y_position, direction=self.aim)
                fired.append(bullet)
        return fired
            

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, value):
        self._life = value

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = value

    @property
    def memories(self):
        return self._memories
    
    def memories_append(self, memory):
        self._memories.append(memory)
        if len(self._memories) > self.mem_size:
            self._memories.pop(0)
    
    def memories_remove(self):
        if len(self._memories) > 0:
            self._memories.pop(0)

    @property
    def mem_size(self):
        return self._mem_size

    @mem_size.setter
    def mem_size(self, value):
        self._mem_size = value

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, value):
        self._range = value

    @property
    def vision_field(self):
        return self._vision_field

    @vision_field.setter
    def vision_field(self, value):
        self._vision_field = value

    def set_position_rect_vision(self, x_new, y_new):
        self.vision_field.center = (x_new, y_new)
        
    @property
    def attack_field(self):
        return self._attack_field

    @attack_field.setter
    def attack_field(self, value):
        self._attack_field = value
    
    def set_position_rect_attack(self, x_new, y_new):
        self.attack_field.center = (x_new, y_new)

    def define_direction(self):
        valid_memories = [memorie for memorie in self.memories]
        vector = [0, 0]
        if valid_memories:
            x_sum = 0
            y_sum = 0
            for x, y in valid_memories:
                x_sum += x
                y_sum += y
            x_mean = x_sum/len(valid_memories)
            y_mean = y_sum/len(valid_memories)
                
            vector = [x_mean - self.x_position, y_mean - self.y_position]
        else:
            vector = [self.scooby_snacks.x_position - self.x_position, self.scooby_snacks.y_position - self.y_position]
        
        # Avalia a direcao final com base no vetor
        if abs(vector[0]) < self.speed:
            vector[0] = 0
        else:
            vector[0] *= self.speed/abs(vector[0])
        if abs(vector[1]) < self.speed:
            vector[1] = 0
        else:
            vector[1] *= self.speed/abs(vector[1])
        
        return np.array(vector)
            

    def attack(self, player):
        player.life = player.life - self.damage

    def evaluate_interaction(self):
        pass
    
    def update(self, player):
        # Verifica se o player esta no campo de visao
        if self.vision_field.colliderect(player.rect):
            self.memories_append((player.x_position, player.y_position))
        else:
            self.memories_remove()
            
        # Verifica se o player esta no campo de ataque
        if self.attack_field.colliderect(player.rect):
            self.attack(player)
            
        movement = self.define_direction()
        movement = self.position_controller.normalize_movement(movement, self.speed)
        self.apply_movement(movement)
        fired = self.aim_function(player, movement)
        
        x_new, y_new = self.position_controller.apply_translation(self.x_position, self.y_position)
        self.set_position_rect(x_new, y_new)
        self.set_position_rect_vision(x_new, y_new)
        self.set_position_rect_attack(x_new, y_new)
        self.animate()
        return fired