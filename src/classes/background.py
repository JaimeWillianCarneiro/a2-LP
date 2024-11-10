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
        
        # Valores que o player andou para fora dos limites da camera
        self.x_rest = 0
        self.y_rest = 0
        
        
    def set_position(self, movement):
        self.x_position += movement['x_moved'] + self.x_rest
        self.y_position += movement['y_moved'] + self.y_rest
        x_limited = True
        y_limited = True
        
        non_player_movement = {'x_moved': movement['x_moved'], 'y_moved': movement['y_moved'],}
        player_movement = {'x_moved': 0, 'y_moved': 0}
        
        # Verificacao dos limites
        if self.x_position <= self.x_limit_inf:
            self.x_position = self.x_limit_inf
            self.x_rest += movement['x_moved']
        elif self.x_position >= self.x_limit_sup:
            self.x_position = self.x_limit_sup
            self.x_rest += movement['x_moved']
        else:
            x_limited = False
        
        if self.y_position <= self.y_limit_inf:
            self.y_position = self.y_limit_inf
            self.y_rest += movement['y_moved']
        elif self.y_position >= self.y_limit_sup:
            self.y_position = self.y_limit_sup
            self.y_rest += movement['y_moved']
        else:
            y_limited = False
        
        self.image = self.sprite.subsurface((self.x_position, self.y_position, *SCREEN_DIMENSIONS))
        
        # Caso tenha sido limitado, so o player se movimenta no eixo
        if x_limited:
            non_player_movement['x_moved'] = 0
            player_movement['x_moved'] = -movement['x_moved']
            
        if y_limited:
            non_player_movement['y_moved'] = 0
            player_movement['y_moved'] = -movement['y_moved']
            
        return non_player_movement, player_movement
            
            
        
    def play_music(self):
        pg.mixer.music.play(-1)
        
    def set_volume(self, volume):
        self.volume = volume
        pg.mixer.music.set_volume(self.volume)
    
    def draw_background_image(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self, movement):
        non_player_movement, player_movement = self.set_position(movement)
        self.draw_background_image()
        return non_player_movement, player_movement