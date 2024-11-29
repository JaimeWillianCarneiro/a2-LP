import pygame as pg
import numpy as np
from enum import Enum

pg.init()
SCREEN_DIMENSIONS = np.array([pg.display.Info().current_w, pg.display.Info().current_h])
GAME_TITLE = 'SCOOBY DOO'

START_SOUND_MENU =  'audios/abertura_inicial.wav'
START_BACKGROUND_MENU= 'assets/menus/title screen.png'
START_COLUMNS_MENU = 12
START_ROWS_MENU = 20


FULL_HEART = 'assets/menus/full heart.png'
EMPTY_HEART = 'assets/menus/empty heart.png'
HALF_HEART = 'assets/menus/half heart.png'

class Fonts(Enum):
    PLAYER_NAME = pg.font.SysFont('comicsansms', 30, True, False)
    PLAYER_LIFE = pg.font.SysFont('franklingothicheavy', 25, True, False)
    EVENT_WARNING = pg.font.SysFont('impact', 50, False, True)
    EVENT_TIME = pg.font.SysFont('showcardgothic', 25, False, False)
    
FRAME_RATE = 30

# SAIR = pg.K_ESCAPE
class WASD_Keys(Enum):
    TOP = pg.K_w
    LEFT = pg.K_a
    DOWN = pg.K_s
    RIGHT = pg.K_d
    
    
    