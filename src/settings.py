import pygame as pg
from enum import Enum

pg.init()
SCREEN_DIMENSIONS = (pg.display.Info().current_w, pg.display.Info().current_h)
GAME_TITLE = 'SCOOBY DOO'

START_SOUND_MENU =  'assets/sounds/backmusic.mp3'
START_BACKGROUNG_MENU= 'assets/title screen/title screen.png'
class Fonts(Enum):
    PLAYER_NAME = pg.font.SysFont('comicsansms', 30, True, False)
    PLAYER_LIFE = pg.font.SysFont('franklingothicheavy', 25, True, False)
    EVENT_WARNING = pg.font.SysFont('impact', 50, False, True)
    EVENT_TIME = pg.font.SysFont('showcardgothic', 25, False, False)
    
FRAME_RATE = 30