import pygame as pg
from src.classes.fase import Fase
from src.settings import SCREEN_DIMENSIONS, GAME_TITLE
import random

class GameObject(pg.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x_position = x
        self.y_position = y
        self.width = width
        self.height = height
        self.image = pg.image.load('shaggy_right_1.png')
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.x_position, self.y_position
    
    def setPosition(self, movement):
        self.x_position -= movement['x_moved']
        self.y_position -= movement['y_moved']
        self.rect.center = self.x_position, self.y_position
    
    def update(self, movement):
        self.setPosition(movement)



pg.init()

screen = pg.display.set_mode((0, 0))
pg.display.set_caption(GAME_TITLE)
clock = pg.time.Clock()

# Variavéis fictias para testar a classe Fase
background = GameObject(SCREEN_DIMENSIONS[0]//2, SCREEN_DIMENSIONS[1]//2, *SCREEN_DIMENSIONS)
game_objects = []
npcs = []
for i in range(3):
    x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
    y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
    width = 23
    height = 40
    game_objects.append(GameObject(x,y, width, height))

    x = random.choice(range(SCREEN_DIMENSIONS[0]))
    y = random.choice(range(SCREEN_DIMENSIONS[1]))
    width = 67
    height = 100
    npcs.append(GameObject(x,y, width, height))

mandatory_events = []
optional_events = []

fase_atual = Fase(screen, background, npcs, game_objects, mandatory_events, optional_events)



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