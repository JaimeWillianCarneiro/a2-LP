import pygame as pg
from src.settings import SCREEN_DIMENSIONS

class Background(pg.sprite.Sprite):
    def __init__(self, screen, sprite, x_position, y_position, width, height, music, volume, sounds):
        super().__init__()
        self.screen = screen
        self.sprite = pg.image.load(sprite)
        self.sprite = pg.transform.scale(self.sprite, (width, height))
        self.x_position = x_position - SCREEN_DIMENSIONS[0]//2
        self.y_position = y_position - SCREEN_DIMENSIONS[1]//2
        self.width = width
        self.height = height
        self.music = music
        self.volume = volume
        self.sounds = sounds
        self.image = self.sprite.subsurface((self.x_position, self.y_position, *SCREEN_DIMENSIONS))
        self.rect = self.image.get_rect()
        pg.mixer.music.load(self.music)
        pg.mixer.music.set_volume(self.volume)
        
        # Limites, ate aonde a camera vai
        self.x_limit_sup = self.width - SCREEN_DIMENSIONS[0]
        self.y_limit_sup = self.height - SCREEN_DIMENSIONS[1]
        
    def get_origin(self):
        return self.x_position+SCREEN_DIMENSIONS[0], self.y_position+SCREEN_DIMENSIONS[1]  
    
    def get_shape(self):
        return self.width, self.height
    
    def get_position(self):
        return self.x_position, self.y_position
        
    def set_position(self, x_new, y_new):
        self.x_position = x_new
        self.y_position = y_new
        
    def to_frame(self,x_player, y_player):
        x_position = x_player - SCREEN_DIMENSIONS[0]//2
        y_position = y_player - SCREEN_DIMENSIONS[1]//2
        # Verificacao dos limites da camera
        if x_position < 0:
            x_position = 0
        elif x_position > self.x_limit_sup:
            x_position = self.x_limit_sup
        
        if y_position < 0:
            y_position = 0
        elif y_position > self.y_limit_sup:
            y_position = self.y_limit_sup
            
        return x_position, y_position
        
        
    def center(self, x_player, y_player):
        # Centraliza a camera no personagem
        x_new, y_new = self.to_frame(x_player, y_player)
        self.set_position(x_new, y_new)
        self.image = self.sprite.subsurface((*self.get_position(), *SCREEN_DIMENSIONS))
        
    def play_music(self):
        pg.mixer.music.play(-1)
        
    def set_volume(self, volume):
        self.volume = volume
        pg.mixer.music.set_volume(self.volume)
    
    def draw_background_image(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self, x_player, y_player):
        self.center(x_player, y_player)
        self.draw_background_image()