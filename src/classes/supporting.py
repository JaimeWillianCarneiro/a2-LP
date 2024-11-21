import pygame as pg
from src.classes.character import Character

class Supporting(Character):
    def __init__(self, name, speed, perception, x_position, y_position, width, height, direction, skin, sprites_quantity, map_limits_sup):
        super().__init__(name, speed, perception, x_position, y_position, width, height, direction, skin, sprites_quantity, map_limits_sup)