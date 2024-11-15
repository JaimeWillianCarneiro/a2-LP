import pygame as pg
from src.settings import SCREEN_DIMENSIONS
from src.classes.background import PositionController

class GameObject(pg.sprite.Sprite):
    def __init__(self, x_position, y_position, width, height, map_limits_sup):
        super().__init__()
        self.life = 3 # Variavel ficticia para testar o fim do jogo por life (Eliminar depois)
        self.position_controller = PositionController(map_limits_sup, width, height)
        self.x_position = x_position
        self.y_position = y_position
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
    
    def set_position(self, x_new, y_new):
        self.x_position = x_new
        self.y_position = y_new
        
    def get_position(self):
        return self.x_position, self.y_position

    def set_position_rect(self, x_new, y_new):
        self.rect.center = (x_new, y_new)
        
    def apply_movement(self, movement):
        x_new = self.x_position + movement['x_moved']
        y_new = self.y_position + movement['y_moved']
        x_new, y_new = self.position_controller.to_frame(x_new, y_new)
        self.set_position(x_new, y_new)     
    
    def animate(self):
        if self.sprites_quantity > 1:
            self.sprite_actual_x += 0.2
            self.sprite_actual_x %= self.sprites_quantity
            self.image = self.sprite_sheet.subsurface((int(self.sprite_actual_x), self.sprite_actual_y, self.width, self.height))
    
    def update(self):
        x_position, y_position = self.get_position()
        x_new, y_new = self.position_controller.apply_translation(x_position, y_position)
        self.set_position_rect(x_new, y_new)
        self.animate()


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