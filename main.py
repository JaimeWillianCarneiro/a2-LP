import pygame as pg
from src.classes.fase import Fase
from src.settings import SCREEN_DIMENSIONS, GAME_TITLE

import random

pg.init()

screen = pg.display.set_mode((0, 0))
pg.display.set_caption(GAME_TITLE)
clock = pg.time.Clock()


fase_atual = Fase(screen)



movement = {'x_moved': 0, 'y_moved': 0}

while True:
    movement['x_moved'] = 0
    movement['y_moved'] = 0
    clock.tick(30)
    
    
    for event in pg.event.get():
        # Usuario parou o jogo
        if event.type == pg.QUIT:
            pg.quit()
            exit()
            
        
        # Controle de personagem
        if event.type == pg.KEYDOWN:
            # Usuario parou o jogo
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
                
            # Tela cheia e sair de tela cheia
            if event.key == pg.K_F11:
                pg.display.toggle_fullscreen()
        
        
    if pg.key.get_pressed()[pg.K_a]:
        movement['x_moved'] -= 10
    if pg.key.get_pressed()[pg.K_d]:
        movement['x_moved'] += 10
    if pg.key.get_pressed()[pg.K_w]:
        movement['y_moved'] -= 10
    if pg.key.get_pressed()[pg.K_s]:
        movement['y_moved'] += 10
    
    fase_atual = fase_atual.update(movement)    
    
    pg.display.flip()