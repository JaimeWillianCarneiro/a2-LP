import unittest
from unittest.mock import Mock
import numpy as np
import pygame as pg
from src.classes.villain import Villain

class TestVillain(unittest.TestCase):
    def setUp(self):
        # Mock para o objeto background e scooby_snacks
        self.mock_background = Mock()
        self.mock_background.get_shape.return_value = (800, 600)

        self.mock_scooby_snacks = Mock()
        self.mock_scooby_snacks.x_position = 200
        self.mock_scooby_snacks.y_position = 300
        
       
        # Instância de Villain
        self.villain = Villain(
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
            sprites_quantity=4,
            map_limits_sup=[800, 600],
            bullets=[],
            weapon=Mock(),
            mem_size=10,
            vision_field=100,
            background=self.mock_background,
            scooby_snacks=self.mock_scooby_snacks
        )
        
          # Mock da arma
        self.villain.weapon = Mock()
        self.villain.weapon.rect = Mock()
        self.villain.weapon.rect.center = (100, 200)  # Definindo valores numéricos para o center
        self.villain.weapon.check_load.return_value = True
        self.villain.weapon.scope = 100
    

    def test_life_property(self):
        self.assertEqual(self.villain.life, 100)
        self.villain.life = 80
        self.assertEqual(self.villain.life, 80)

    def test_memories_append_and_remove(self):
        self.assertEqual(len(self.villain.memories), 0)
        
        # Adicionando memória
        self.villain.memories_append((100, 200))
        self.assertEqual(len(self.villain.memories), 1)
        self.assertEqual(self.villain.memories[0], (100, 200))
        
        # Removendo memória
        self.villain.memories_remove()
        self.assertEqual(len(self.villain.memories), 0)

    def test_define_direction_with_memories(self):
        self.villain.memories_append((150, 150))
        direction = self.villain.define_direction()
        expected_direction = np.array([5, 5])  # Baseado em x_position=50, y_position=50, speed=5
        np.testing.assert_array_almost_equal(direction, expected_direction)

    def test_define_direction_without_memories(self):
        direction = self.villain.define_direction()
        expected_direction = np.array([5, 5])  # Baseado na posição de scooby_snacks
        np.testing.assert_array_almost_equal(direction, expected_direction)

    def test_attack(self):
        mock_player = Mock()
        mock_player.life = 100
        self.villain.weapon.damage = 20

        self.villain.attack(mock_player)
        self.assertEqual(mock_player.life, 80)

    def test_aim_function_hits_target(self):
        mock_player = Mock()
        mock_player.rect = Mock()
        mock_player.rect.clipline.return_value = True

        self.villain.weapon.scope = 100
        self.villain.weapon.check_load.return_value = True
        self.villain.weapon.fire.return_value = Mock()

        movement = np.array([1, 0])
        fired_bullets = self.villain.aim_function(mock_player, movement)
        self.assertEqual(len(fired_bullets), 1)

    def test_aim_function_misses_target(self):
        mock_player = Mock()
        mock_player.rect = Mock()
        mock_player.rect.clipline.return_value = False

        self.villain.weapon.scope = 100
        self.villain.weapon.check_load.return_value = False

        movement = np.array([1, 0])
        fired_bullets = self.villain.aim_function(mock_player, movement)
        self.assertEqual(len(fired_bullets), 0)

if __name__ == "__main__":
    unittest.main()
