import pygame as pg
from src.settings import SCREEN_DIMENSIONS

class GameObject(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Dados Ficticios para testar a Fase
        self.life = 3
        
        self.x_position = x
        self.y_position = y
        self.width = width
        self.height = height
        self.sprite_sheet = pg.image.load('shaggy_right_1.png')
        self.sprite_dimensions = self.sprite_sheet.get_size()
        self.sprite_actual_x = 0
        self.sprite_actual_y = 0
        self.sprites_quantity = 1
        self.image = self.sprite_sheet.subsurface((self.sprite_actual_x, self.sprite_actual_y, *self.sprite_dimensions))
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.x_position, self.y_position
    
    def set_position(self, movement):
        self.x_position -= movement['x_moved']
        self.y_position -= movement['y_moved']
        self.rect.center = self.x_position, self.y_position
    
    def animate(self):
        if self.sprites_quantity > 1:
            self.sprite_actual_x += 0.2
            self.sprite_actual_x %= self.sprites_quantity
            self.image = self.sprite_sheet.subsurface((int(self.sprite_actual_x), self.sprite_actual_y, self.width, self.height))
    
    def update(self, movement):
        self.set_position(movement)


class Collectible(GameObject):
    def __init__(self, visible, description):
        super().__init__()
        self.__visible = visible
        self.description = description
    
    def set_visible(self):
        pass
    
    def get_visible(self):
        return self.__visible
    
    def collect(self):
        pass