import pygame as pg
import numpy as np
from src.classes.phase import PhaseManager
from src.settings import SCREEN_DIMENSIONS, GAME_TITLE, FRAME_RATE, WASD_Keys

pg.init()
screen = pg.display.set_mode((0, 0))
pg.display.set_caption(GAME_TITLE)
clock = pg.time.Clock()


phase_manager = PhaseManager(screen)

movement = np.zeros(2)
attack = np.zeros(2)

while True:
    movement = np.zeros(2)
    attack = np.zeros(2)
    clock.tick(FRAME_RATE)
    
    for event in pg.event.get():
        # Usuario parou o jogo
        if event.type == pg.QUIT:
            pg.quit()
            exit()
            
        if event.type == pg.KEYDOWN:
            # Usuario parou o jogo
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit() 
            # Tela cheia e sair de tela cheia
            if event.key == pg.K_F11:
                pg.display.toggle_fullscreen()
    
    # print(np.array(pg.key.get_pressed()))
    # movement = 
    if pg.key.get_pressed()[WASD_Keys.LEFT.value]:
        movement[0] -= 1
    if pg.key.get_pressed()[WASD_Keys.RIGHT.value]:
        movement[0] += 1
    if pg.key.get_pressed()[WASD_Keys.TOP.value]:
        movement[1] -= 1
    if pg.key.get_pressed()[WASD_Keys.DOWN.value]:
        movement[1] += 1
        
    if pg.key.get_pressed()[pg.K_LEFT]:
        attack[0] -= 1
    if pg.key.get_pressed()[pg.K_RIGHT]:
        attack[0] += 1
    if pg.key.get_pressed()[pg.K_UP]:
        attack[1] -= 1
    if pg.key.get_pressed()[pg.K_DOWN]:
        attack[1] += 1
    
    phase_manager.update(movement, attack)
    pg.display.flip()