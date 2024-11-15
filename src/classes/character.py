import pygame as pg
from abc import ABC, abstractmethod


class Character(pg.sprite.Sprite, ABC):
    def __init__(self, name, speed, perception, x_position, y_position, width, height, direction, sprite_sheet):
        super().__init__()
        self._name = name
        self._speed = speed
        self._perception = perception
        self._x_position = x_position
        self._y_position = y_position
        self._width = width
        self._height = height
        self._direction = direction
        self._sprite_sheet = sprite_sheet
        self._current_sprite_x = 0
        self._current_sprite_y = 0
        self.image = self.sprite_sheet.subsurface((self._current_sprite_x * self.width, self._current_sprite_y * self.height, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = self._x_position, self._y_position      

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
    def x_position(self):
        return self._x_position

    @x_position.setter
    def x_position(self, value):
        self._x_position = value
        self._rect.x = value

    @property
    def y_position(self):
        return self._y_position

    @y_position.setter
    def y_position(self, value):
        self._y_position = value
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

        
    def apply_movement(self, movement, map_limits_inf, map_limits_sup):
        x_new = self.x_position + movement['x_moved']
        y_new = self.y_position + movement['y_moved']
        x_new, y_new = self.to_frame(x_new, y_new, map_limits_inf, map_limits_sup)
        self.set_position(x_new, y_new)

    @abstractmethod
    def update(self):
        pass
