import pygame as pg
from abc import ABC, abstractmethod
from src.classes.character import Character


class Protagonist(Character, ABC):
    def __init__(self, name, speed, perception, x_position, y_position, width, height, direction, skin,
                 life, inventory, ability, sprites_quantity, map_limits_sup, bullets, weapon):
        super().__init__(name, speed, perception, x_position, y_position, width, height, direction, skin, life, sprites_quantity, map_limits_sup, bullets, weapon)
        self._inventory = inventory
        self._ability = ability

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

    @abstractmethod
    def update(self):
        pass
    
    def check_objective(self):
        print("Checking objective...")

    def check_ability(self):
        print("Checking ability...")

class Group1Protagonist(Protagonist):
    def __init__(self, name, speed, perception, x_position, y_position, width, height, direction, skin,
                 life, inventory, ability, sprites_quantity, map_limits_sup, bullets, weapon, trap_power):
        super().__init__(name, speed, perception, x_position, y_position, width, height, direction, skin, life, inventory, ability, sprites_quantity, map_limits_sup, bullets, weapon)
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
        x_new, y_new = self.position_controller.apply_translation(self.x_position, self.y_position)
        self.set_position_rect(x_new, y_new)
        self.animate()
        if not self.movement.any():
            self.steps.stop()
        elif not self.steps.get_num_channels():  # Verifica se o canal está livre
            # self.steps.stop()
            self.steps.play(0)


class Group2Protagonist(Protagonist):
    def __init__(self, name, speed, perception, x_position, y_position, width, height, direction, skin,
                 life, inventory, ability, sprites_quantity, map_limits_sup, bullets, weapon, deceive_power):
        super().__init__(name, speed, perception, x_position, y_position, width, height, direction, skin, life, inventory, ability, sprites_quantity, map_limits_sup, bullets, weapon)
        self._deceive_power = deceive_power

    @property
    def deceive_power(self):
        return self._deceive_power

    @deceive_power.setter
    def deceive_power(self, value):
        self._deceive_power = value

    def update(self):
        pass