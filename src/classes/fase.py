import pygame as pg

class Fase(pg.srite.Sprite):
    """
        Classe que representa cada uma das dez fases do jogo
    """
    # protagonista = Protagonista()
    screen = pg.display.set_mode((0, 0))
    SCREEN_DIMENSIONS = screen.get_size()
    # pg.display.set_caption(GAME_TITLE)
    # background = Background()
    Game_Objects = pg.sprite.Group()   
    
    
    def __init__(self):
        pass
    
    def render_camera(self):
        pass
    
    def check_end():
        pass
    
    def check_lost():
        pass
    
    def update(self):
        pass
    
    