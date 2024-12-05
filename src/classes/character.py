import pygame as pg
from abc import ABC, abstractmethod
from src.classes.background import PositionController
import numpy as np


class Character(pg.sprite.Sprite, ABC):
    def __init__(self, name, speed, perception, x_position, y_position, width, height, direction, skin, life, sprites_quantity, map_limits_sup, bullets, weapon):
        super().__init__()
        self.life = life
        self._name = name
        self._speed = speed
        self._perception = perception
        self.position_controller = PositionController(map_limits_sup, width, height)
        self._x_position = x_position
        self._y_position = y_position
        self._width = width
        self._height = height
        self.movement = np.zeros(2, dtype=float)
        self._spritesheet = pg.image.load(f'assets\\spritesheets\\{name}_{skin}.png')
        self._spritesheet = pg.transform.scale(self._spritesheet, (width*sprites_quantity, height*4))
        self.sprites_quantity = sprites_quantity 
        self._current_sprite_x = 0
        self._current_sprite_y = direction
        self.image = self.spritesheet.subsurface((self._current_sprite_x * self.width, self._current_sprite_y * self.height, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = self._x_position, self._y_position
        self._bullets = bullets
        self._aim = np.zeros(2, dtype=float)
        self._weapon = weapon
        self.steps = pg.mixer.Sound('assets\sounds\passos.wav')

    @property
    def name(self):
        return self._name

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def perception(self):
        return self._perception

    @perception.setter
    def perception(self, value):
        self._perception = value

    @property
    def x_position(self):
        return self._x_position

    @x_position.setter
    def x_position(self, value):
        self._x_position = value

    @property
    def y_position(self):
        return self._y_position

    @y_position.setter
    def y_position(self, value):
        self._y_position = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.rect.width = value
        self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self.rect.height = value
        self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def spritesheet(self):
        return self._spritesheet

    @spritesheet.setter
    def spritesheet(self, value):
        self._spritesheet = value

    @property
    def current_sprite_x(self):
        return self._current_sprite_x

    @current_sprite_x.setter
    def current_sprite_x(self, value):
        self._current_sprite_x = value

    @property
    def current_sprite_y(self):
        return self._current_sprite_y

    @current_sprite_y.setter
    def current_sprite_y(self, value):
        self._current_sprite_y = value
        
    def set_position_rect(self, x_new, y_new):
        self.rect.center = (x_new, y_new)
    
    @property
    def weapon(self):
        return self._weapon
    
    @weapon.setter
    def weapon(self, weapon_new):
        self._weapon = weapon_new
    
    @property
    def bullet(self):
        return self._bullet
    
    @bullet.setter
    def bullet(self, bullet_new):
        self._bullet = bullet_new
     
    @property
    def aim(self):
        return self._aim
    
    @aim.setter
    def aim(self, aim_new):
        self._aim = np.array(aim_new)
    
    def animate(self):
        if self.sprites_quantity > 1:
            self._current_sprite_x += 0.2
            if self._current_sprite_x >= self.sprites_quantity:
                self.current_sprite_x = 0
            current_sprite_x = int(self.current_sprite_x)
            self.image = self.spritesheet.subsurface((current_sprite_x * self.width, self._current_sprite_y * self.height, self.width, self.height))
    
    def redefine_direction(self, movement):
        if movement[0] > 0:
            current_sprite_y = 2
        elif movement[0] < 0:
            current_sprite_y = 3
        elif movement[1] < 0:
            current_sprite_y = 1
        elif movement[1] > 0:
            current_sprite_y = 0
        else:
            current_sprite_y = (self.current_sprite_y+1)%4
            self.current_sprite_y ^= current_sprite_y
            current_sprite_y ^= self.current_sprite_y
            self.current_sprite_y ^= current_sprite_y
            
        if self.current_sprite_y != current_sprite_y:
            self.current_sprite_y = current_sprite_y
            self.current_sprite_x = 0   

    def apply_movement(self, movement, redefine_direction = True):
        if redefine_direction:
            self.redefine_direction(movement)
        
        x_new = self.x_position + movement[0]
        y_new = self.y_position + movement[1]
        x_new_corrected, y_new_corrected = self.position_controller.to_frame(x_new, y_new)
        
        # Devolve a parte do movimento que nao foi aplicado
        comeback = np.array([x_new, y_new]) - np.array([x_new_corrected, y_new_corrected])
        
        self.x_position = x_new_corrected
        self.y_position = y_new_corrected
        self.movement = movement
        
        return -comeback
        
    @abstractmethod
    def update(self):
        pass
