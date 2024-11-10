import pygame as pg
from src.settings import SCREEN_DIMENSIONS

class Background(pg.sprite.Sprite):
    def __init__(self, sprite, x_position, y_position, music, volume, sounds):
        super().__init__()
        self.sprite = pg.image.load(sprite)
        self.x_position = x_position
        self.y_position = y_position
        self.music = music
        self.volume = volume
        self.sounds = sounds
        self.image = self.sprite.subsurface((self.x_position, self.y_position, *SCREEN_DIMENSIONS))
        self.rect = self.image.get_rect()
        
    def set_position(self):
        pass
    
    def update(self):
        pass