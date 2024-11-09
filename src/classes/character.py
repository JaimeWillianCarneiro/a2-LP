import pygame as pg
from abc import ABC, abstractmethod


class Character(pg.sprite.Sprite, ABC):
    def __init__(self, name, speed, perception, pos_x, pos_y, width, height, direction, sprite_sheet):
        super().__init__()
        self._name = name
        self._speed = speed
        self._perception = perception
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._width = width
        self._height = height
        self._direction = direction
        self._rect = pg.Rect(self._pos_x, self._pos_y, self._width, self._height).center(()) # Como pegar o tamanho da tela? Essa é a melhor abordagem?
        self._sprite_sheet = sprite_sheet
        self._current_sprite_x = 0
        self._current_sprite_y = 0
        self.image = self.sprite_sheet.subsurface(pg.Rect(self.sprite_current_x * self.width, 
                                                          self.sprite_current_y * self.height, 
                                                          self.width, self.height))
        

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def perception(self):
        return self._perception

    @perception.setter
    def perception(self, value):
        self._perception = value

    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, value):
        self._pos_x = value
        self._rect.x = value

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, value):
        self._pos_y = value
        self._rect.y = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self._rect.width = value
        self.image = pg.transform.scale(self.image, (self._rect.width, self._rect.height))

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self._rect.height = value
        self.image = pg.transform.scale(self.image, (self._rect.width, self._rect.height))

    @property
    def rect(self):
        return self._rect

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def sprite_sheet(self):
        return self._sprite_sheet

    @sprite_sheet.setter
    def sprite_sheet(self, value):
        self._sprite_sheet = value

    @property
    def current_sprite_x(self):
        return self._current_sprite_x

    @current_sprite_x.setter
    def current_sprite_x(self, value):
        self._current_sprite_x = value

    @property
    def current_sprite_y(self):
        return self._current_sprite_y

    @current_sprite_y.setter
    def current_sprite_y(self, value):
        self._current_sprite_y = value

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def set_position(self, x, y):
        self.pos_x = x
        self.pos_y = y
