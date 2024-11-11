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
    
    
    def set_position(self, x_new, y_new):
        self.x_position = x_new
        self.y_position = y_new
        
    def get_position(self):
        return self.x_position, self.y_position
    
    
    def to_frame(self, map_limits_inf, map_limits_sup):
        # Enquadra o objeto para que ele nao ultrapasse nenhum limite do mapa
        x_position, y_position = self.get_position()
        far_left = (map_limits_inf[0] + self.width/2)
        far_right = (map_limits_sup[0] - self.width/2)
        if x_position < far_left:
            x_position = far_left
        elif x_position > far_right:
            x_position = far_right
            
        far_top = (map_limits_inf[1] + self.height/2)
        far_bottom = (map_limits_sup[1] - self.height/2)
        if y_position < far_top:
            y_position = far_top
        if y_position > far_bottom:
            y_position = far_bottom
            
        return x_position, y_position
        
    
    def apply_movement(self, movement, map_limits_inf, map_limits_sup):
        x_new = self.x_position - movement['x_moved']
        y_new = self.y_position - movement['y_moved']
        self.set_position(x_new, y_new)
        x_new, y_new = self.to_frame(map_limits_inf, map_limits_sup)
        self.set_position(x_new, y_new)
        self.rect.center = self.x_position, self.y_position
        
    
    def animate(self):
        if self.sprites_quantity > 1:
            self.sprite_actual_x += 0.2
            self.sprite_actual_x %= self.sprites_quantity
            self.image = self.sprite_sheet.subsurface((int(self.sprite_actual_x), self.sprite_actual_y, self.width, self.height))
    
    
    def update(self, movement, map_limits_inf, map_limits_sup):
        self.apply_movement(movement, map_limits_inf, map_limits_sup)
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