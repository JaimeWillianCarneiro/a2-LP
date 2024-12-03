import pygame as pg
from src.settings import SCREEN_DIMENSIONS, FRAME_RATE
from src.classes.background import PositionController
import numpy as np

class GameObject(pg.sprite.Sprite):
    def __init__(self, x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity):
        super().__init__()
        self.position_controller = PositionController(map_limits_sup, width, height)
        self.x_position = x_position
        self.y_position = y_position
        self.width = width
        self.height = height
        self.movement = np.zeros(2)
        self.spritesheet_path = spritesheet
        self.spritesheet = pg.image.load(spritesheet)
        self.spritesheet = pg.transform.scale(self.spritesheet, (self.width*sprites_quantity, self.height))
        self.sprite_actual_x = sprite_actual_x
        self.sprite_actual_y = sprite_actual_y
        self.sprites_quantity = sprites_quantity
        self.image = self.spritesheet.subsurface((self.sprite_actual_x*self.width, self.sprite_actual_y*self.height, width, height))
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.x_position, self.y_position
    
    def set_position(self, x_new, y_new):
        self.x_position = x_new
        self.y_position = y_new
        
    def get_position(self):
        return self.x_position, self.y_position

    def set_position_rect(self, x_new, y_new):
        self.rect.center = (x_new, y_new)
        
    def apply_movement(self, movement):
        x_new = self.x_position + movement[0]
        y_new = self.y_position + movement[1]
        x_new_corrected, y_new_corrected = self.position_controller.to_frame(x_new, y_new)
        
        # Devolve a parte do movimento que nao foi aplicado
        comeback = np.array([x_new, y_new]) - np.array([x_new_corrected, y_new_corrected])
        
        self.set_position(x_new_corrected, y_new_corrected)
        self.movement = movement
        
        return -comeback
        
    
    def animate(self):
        if self.sprites_quantity > 1:
            self.sprite_actual_x += 0.2
            self.sprite_actual_x %= self.sprites_quantity
            self.image = self.spritesheet.subsurface((int(self.sprite_actual_x), self.sprite_actual_y, self.width, self.height))
    
    def update(self):
        self.movement = np.zeros(2)
        x_position, y_position = self.get_position()
        x_new, y_new = self.position_controller.apply_translation(x_position, y_position)
        self.set_position_rect(x_new, y_new)
        self.animate()


class Collectible(GameObject):
    def __init__(self, x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity, visible, description):
        super().__init__(x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity)
        self._visible = visible
        self.description = description
    
    @property
    def visible(self):
        return self._visible
    
    @visible.setter
    def visible(self, new_value):
        self._visible = new_value
        
class Ammo(GameObject):
    def __init__(self, x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity, damage, effects, direction, recochet, speed):
        super().__init__(x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity)
        self._damage = damage
        self._effects = effects
        self.direction = direction
        self.recochet = recochet
        self.speed = speed
        
    @property
    def damage(self):
        return self._damage
    
    @property
    def effects(self):
        return self._effects
    
    @property
    def bullets(self):
        return self._bullets
    
    @bullets.setter
    def bullets(self, bullets_new):
        self._bullets = bullets_new
        
    def copy(self):
        return Ammo(self.x_position, self.y_position, self.width, self.height, self.position_controller.map_limits_sup, self.spritesheet_path, self.sprite_actual_x, self.sprite_actual_y, self.sprites_quantity, self.damage, self.effects, self.direction, self.recochet, self.speed)
        
    def update(self):
        position = np.array(self.get_position(), dtype=float)
        position += self.direction*self.speed*10/FRAME_RATE
        self.position_controller.out_game(self)
        self.set_position(position[0], position[1])
        super().update()
        
# class Weapon:
#     Atributos:
#     Dano
#     Se é de arremesso ou corpo a corpo
#     Efeito especial (cool down): elemental, se empurra, imobiliza o personagem
    
#     Métodos:
#     Atacar 
#     AtaqueEspecial
#     Defender
    
    

class Weapon(GameObject):
    def __init__(self, x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity, damage, kind_damage, attack_field, reload_time, ammo, scope, special_effect = None):
        # TODO tirar dano de personagens
        super().__init__(x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity)
        self.damage = damage
        self.kind_damage = kind_damage
        self.special_effect = special_effect
        self.attack_field = pg.Rect(x_position - attack_field, y_position - attack_field, 2*attack_field, 2*attack_field)
        self.reload = reload_time
        self.reload_time = reload_time
        self._reloading = False
        self._ammo = ammo
        self.scope = scope
    
    @property
    def reloading(self):
        return self._reloading
    
    @reloading.setter
    def reloading(self, new_reloading):
        self._reloading = new_reloading
     
    @property
    def ammo(self):
        return self._ammo
    
    @ammo.setter
    def ammo(self, new_ammo):
        self._ammo = new_ammo
        
    def set_position_rect_attack(self, x_new, y_new):
        self.attack_field.center = (x_new, y_new)
        
    def instanciate_bullet(self, direction):
        bullet = self.ammo.copy()
        bullet.x_position = self.x_position
        bullet.y_position = self.y_position
        bullet.direction = direction
        return bullet
        
    def check_load(self):
        if self.reload_time <= self.reload:
            return True
        return False
    
    def fire(self, direction: np.array) -> Ammo:
        """ Dispara uma municao numa direcao dada.

        Args:
            direction (np.array): Direcao na qual a municao sera disparada.

        Returns:
            Ammo: Nova instancia de municao disparada.
        """
        fired = None
        # Condicoes do disparo
        if self.check_load():
            self.reload = 0
            self.reloading = True
            # Instancia uma nova municao, copia da municao dada
            fired = self.instanciate_bullet(direction)
            
        return fired
    
    def update(self):
        super().update()
        # Atualiza a zona de ataque
        self.set_position_rect_attack(*self.rect.center)
        
        # Recarrega caso o player solicite
        if self.reloading:
            self.reload += 1
            # Para de recarregar ao terminar
            if self.check_load():
                self.reloading = False