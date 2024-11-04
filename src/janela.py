import pygame
from pygame.locals import *
from sys import exit


pygame.init()

LARGURA = 640
ALTURA = 480

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Scooby Doo e A Caçada Cibernética')

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    pygame.draw.rect(tela, (255, 0, 0), (200, 300, 40, 50))
    pygame.display.update()