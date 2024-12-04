import unittest
from unittest.mock import Mock
import pygame as pg
from src.classes.protagonist import Group1Protagonist, Group2Protagonist

class TestProtagonist(unittest.TestCase):
    def setUp(self):
        # Configurar mocks e objetos iniciais
        self.map_limits = [800, 600]
        self.group1_protagonist = Group1Protagonist(
            name="Shaggy",
            speed=5,
            perception=100,
            x_position=50,
            y_position=50,
            width=64,
            height=64,
            direction=0,
            skin="default",
            life=100,
            inventory=["sword", "shield"],
            ability="trap",
            sprites_quantity=4,
            map_limits_sup=self.map_limits,
            bullets=[],
            weapon="sword",
            trap_power=50
        )

        self.group2_protagonist = Group2Protagonist(
            name="Daphne",
            speed=4,
            perception=80,
            x_position=100,
            y_position=100,
            width=64,
            height=64,
            direction=1,
            skin="dialogue",
            life=120,
            inventory=["dagger"],
            ability="deceive",
            sprites_quantity=4,
            map_limits_sup=self.map_limits,
            bullets=[],
            weapon="dagger",
            deceive_power=30
        )

    def test_group1_protagonist_attributes(self):
        self.assertEqual(self.group1_protagonist.name, "Shaggy")
        self.assertEqual(self.group1_protagonist.trap_power, 50)
        self.assertEqual(self.group1_protagonist.inventory, ["sword", "shield"])

    def test_group1_protagonist_trap_power_setter(self):
        self.group1_protagonist.trap_power = 75
        self.assertEqual(self.group1_protagonist.trap_power, 75)

    def test_group2_protagonist_attributes(self):
        self.assertEqual(self.group2_protagonist.name, "Daphne")
        self.assertEqual(self.group2_protagonist.deceive_power, 30)
        self.assertEqual(self.group2_protagonist.inventory, ["dagger"])

    def test_group2_protagonist_deceive_power_setter(self):
        self.group2_protagonist.deceive_power = 45
        self.assertEqual(self.group2_protagonist.deceive_power, 45)


if __name__ == "__main__":
    unittest.main()
