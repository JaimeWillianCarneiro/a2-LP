import pygame as pg
from src.settings import SCREEN_DIMENSIONS

class Background(pg.sprite.Sprite):
    def __init__(self, screen, sprite, x_position, y_position, width, height, music, volume, sounds):
        super().__init__()
        self.screen = screen
        self.sprite = pg.image.load(sprite)
        self.sprite = pg.transform.scale(self.sprite, (width, height))
        self.x_position = x_position
        self.y_position = y_position
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
        self.x_limit_inf = 0
        self.x_limit_sup = self.width - SCREEN_DIMENSIONS[0]
        self.y_limit_inf = 0
        self.y_limit_sup = self.height - SCREEN_DIMENSIONS[1]
        
    def set_position(self, movement):
        self.x_position += movement['x_moved']
        self.y_position += movement['y_moved']
        
        # Verificacao dos limites
        if self.x_position < self.x_limit_inf:
            self.x_position = self.x_limit_inf
        elif self.x_position > self.x_limit_sup:
            self.x_position = self.x_limit_sup
        
        if self.y_position < self.y_limit_inf:
            self.y_position = self.y_limit_inf
        elif self.y_position > self.y_limit_sup:
            self.y_position = self.y_limit_sup
        
        self.image = self.sprite.subsurface((self.x_position, self.y_position, *SCREEN_DIMENSIONS))
        
    def play_music(self):
        pg.mixer.music.play(-1)
        
    def set_volume(self, volume):
        self.volume = volume
        pg.mixer.music.set_volume(self.volume)
    
    def draw_background_image(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self, movement):
        self.set_position(movement)
        self.draw_background_image()