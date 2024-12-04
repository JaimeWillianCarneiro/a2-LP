import unittest
from unittest.mock import Mock, patch
import numpy as np
import pygame as pg
from src.classes.character import Character
import unittest
from unittest.mock import Mock
import numpy as np
import pygame as pg


class TestCharacterImplementation(Character):
    """Implementação vazia apenas para satisfazer o método abstrato"""
    def update(self):
        pass

class TestCharacter(unittest.TestCase):
    def setUp(self):
        # Configurar um mock para o PositionController e pygame
        self.mock_position_controller = Mock()
        self.mock_position_controller.to_frame.side_effect = lambda x, y: (x, y)

        # Configurar dados de entrada
        self.character = TestCharacterImplementation(
            name="Fred",
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
            weapon="sword"
        )
        self.character.position_controller = self.mock_position_controller
  
    def test_name_property(self):
        """Teste para verificar nome do personagem"""
        self.assertEqual(self.character.name, "Fred")

    def test_speed_property(self):
        """Teste para verificar e alterar velocidade do personagem"""
        self.assertEqual(self.character.speed, 5)
        self.character.speed = 10
        self.assertEqual(self.character.speed, 10)

    def test_perception_property(self):
        """Teste para verificar e alterar a percepção do personagem"""
        self.assertEqual(self.character.perception, 100)
        self.character.perception = 120
        self.assertEqual(self.character.perception, 120)

    def test_x_position_property(self):
        """Teste para verificar e alterar a posição x"""
        self.assertEqual(self.character.x_position, 50)
        self.character.x_position = 100
        self.assertEqual(self.character.x_position, 100)

    def test_y_position_property(self):
        """Teste para verificar e alterar a posição y"""
        self.assertEqual(self.character.y_position, 50)
        self.character.y_position = 100
        self.assertEqual(self.character.y_position, 100)

    def test_width_property(self):
        """Teste para verificar e alterar a largura"""
        self.assertEqual(self.character.width, 64)
        self.character.width = 128
        self.assertEqual(self.character.width, 128)

    def test_height_property(self):
        """Teste para verificar e alterar a altura"""
        self.assertEqual(self.character.height, 64)
        self.character.height = 128
        self.assertEqual(self.character.height, 128)

    def test_image_property(self):
        original_image = self.character.image
        new_image = Mock()
        self.character.image = new_image
        self.assertEqual(self.character.image, new_image)

    def test_spritesheet_property(self):
        original_spritesheet = self.character.spritesheet
        new_spritesheet = Mock()
        self.character.spritesheet = new_spritesheet
        self.assertEqual(self.character.spritesheet, new_spritesheet)

    def test_current_sprite_x_property(self):
        self.assertEqual(self.character.current_sprite_x, 0)
        self.character.current_sprite_x = 2
        self.assertEqual(self.character.current_sprite_x, 2)

    def test_current_sprite_y_property(self):
        self.assertEqual(self.character.current_sprite_y, 0)
        self.character.current_sprite_y = 3
        self.assertEqual(self.character.current_sprite_y, 3)

    def test_weapon_property(self):
        self.assertEqual(self.character.weapon, "sword")
        self.character.weapon = "bow"
        self.assertEqual(self.character.weapon, "bow")

    def test_aim_property(self):
        np.testing.assert_array_equal(self.character.aim, np.zeros(2, dtype=float))
        self.character.aim = [1, 1]
        np.testing.assert_array_equal(self.character.aim, np.array([1, 1]))

    def test_bullet_property(self):
        self.character.bullet = "arrow"
        self.assertEqual(self.character.bullet, "arrow")

    def test_set_position_rect(self):
        self.character.set_position_rect(200, 300)
        self.assertEqual(self.character.rect.center, (200, 300))

    def test_animate(self):
        self.character.sprites_quantity = 4
        self.character.animate()
        self.assertEqual(int(self.character.current_sprite_x), 0)

    def test_apply_movement(self):
        self.character.apply_movement([5, -5])
        self.assertEqual(self.character.x_position, 55)
        self.assertEqual(self.character.y_position, 45)

if __name__ == "__main__":
    unittest.main()
