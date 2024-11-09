import pygame as pg
from abc import ABC, abstractmethod
from character import Character


class Protagonist(Character, ABC):
    def __init__(self, name, speed, perception, pos_x, pos_y, width, height, direction, sprite_sheet,
                 life, inventory, ability, movement):
        super().__init__(name, speed, perception, pos_x, pos_y, width, height, direction, sprite_sheet)
        self._life = life
        self._inventory = inventory
        self._ability = ability
        self._movement = movement

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, value):
        self._life = value

    @property
    def inventory(self):
        return self._inventory

    @inventory.setter
    def inventory(self, value):
        self._inventory = value

    @property
    def ability(self):
        return self._ability

    @ability.setter
    def ability(self, value):
        self._ability = value

    @property
    def movement(self):
        return self._movement

    @movement.setter
    def movement(self, value):
        self._movement = value

    @abstractmethod
    def update(self):
        pass
    
    def check_objective(self):
        print("Checking objective...")

    def check_ability(self):
        print("Checking ability...")


class Group1Protagonist(Protagonist):
    def __init__(self, name, speed, perception, pos_x, pos_y, width, height, direction, sprite_sheet,
                 life, inventory, ability, movement, damage, trap_power):
        super().__init__(name, speed, perception, pos_x, pos_y, width, height, direction, sprite_sheet,
                         life, inventory, ability, movement)
        self._damage = damage
        self._trap_power = trap_power

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = value

    @property
    def trap_power(self):
        return self._trap_power

    @trap_power.setter
    def trap_power(self, value):
        self._trap_power = value

    def update(self):
        pass


class Group2Protagonist(Protagonist):
    def __init__(self, name, speed, perception, pos_x, pos_y, width, height, direction, sprite_sheet,
                 life, inventory, ability, movement, deceive_power):
        super().__init__(name, speed, perception, pos_x, pos_y, width, height, direction, sprite_sheet,
                         life, inventory, ability, movement)
        self._deceive_power = deceive_power

    @property
    def deceive_power(self):
        return self._deceive_power

    @deceive_power.setter
    def deceive_power(self, value):
        self._deceive_power = value

    def update(self):
        pass