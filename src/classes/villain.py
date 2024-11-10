import pygame as pg
from character import Character


class Villain(Character):
    def __init__(self, name, speed, perception, pos_x, pos_y, width, height, direction, sprite_sheet,
                 life, damage, mem_size, range_, vision_field, attack_field):
        super().__init__(name, speed, perception, pos_x, pos_y, width, height, direction, sprite_sheet)
        self._life = life
        self._damage = damage
        self._memories = []
        self._mem_size = mem_size
        self._range = range_
        self._vision_field = vision_field
        self._attack_field = attack_field

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, value):
        self._life = value

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = value

    @property
    def memories(self):
        return self._memories
    
    def memories_append(self, memory):
        self._memories.append(memory)

        if len(self._memories) > self.mem_size:
            self._memories.pop(0)

    @property
    def mem_size(self):
        return self._mem_size

    @mem_size.setter
    def mem_size(self, value):
        self._mem_size = value

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, value):
        self._range = value

    @property
    def vision_field(self):
        return self._vision_field

    @vision_field.setter
    def vision_field(self, value):
        self._vision_field = value

    @property
    def attack_field(self):
        return self._attack_field

    @attack_field.setter
    def attack_field(self, value):
        self._attack_field = value

    def update(self):
        pass

    def define_direction(self):
        pass

    def attack(self):
        pass

    def evaluate_interaction(self):
        pass
