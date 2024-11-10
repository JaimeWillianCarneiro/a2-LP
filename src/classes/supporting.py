import pygame as pg
from character import Character


class Supporting(Character):
    def __init__(self, name, speed, perception, pos_x, pos_y, width, height, direction, sprite_sheet):
        super().__init__(name, speed, perception, pos_x, pos_y, width, height, direction, sprite_sheet)