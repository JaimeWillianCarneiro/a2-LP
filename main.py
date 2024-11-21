import pygame as pg
from src.classes.fase import Fase
from src.classes.background import Interface
from src.settings import SCREEN_DIMENSIONS, GAME_TITLE, FRAME_RATE

pg.init()
print(SCREEN_DIMENSIONS)
screen = pg.display.set_mode((0, 0)) #tela cheia
pg.display.set_caption(GAME_TITLE)
clock = pg.time.Clock()


fase_atual = Fase(screen)
interface = Interface(screen, fase_atual, [])


movement = {'x_moved': 0, 'y_moved': 0}
attack = [0, 0]

while True:
    movement['x_moved'] = 0
    movement['y_moved'] = 0
    attack= [0, 0]
    clock.tick(FRAME_RATE)
    
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
        
    if pg.key.get_pressed()[pg.K_LEFT]:
        attack[0] -= 1
    if pg.key.get_pressed()[pg.K_RIGHT]:
        attack[0] += 1
    if pg.key.get_pressed()[pg.K_UP]:
        attack[1] -= 1
    if pg.key.get_pressed()[pg.K_DOWN]:
        attack[1] += 1
    
    fase_atual = fase_atual.update(movement, attack)
    interface.set_fase_atual(fase_atual)  
    interface.update()
    pg.display.flip()