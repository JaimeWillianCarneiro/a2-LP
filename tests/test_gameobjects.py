import unittest
from unittest.mock import MagicMock
from src.classes.gameobjects import GameObject, Ammo, Weapon, Collectible
import pygame as pg

class TestGameObject(unittest.TestCase):
    
    def setUp(self):
        # Passando um valor de map_limits_sup que não seja None
        self.map_limits_sup = {}  # Ou qualquer valor adequado para os testes
        self.game_object = GameObject(
            x_position=50,
            y_position=50,
            width=32,
            height=32,
            map_limits_sup=self.map_limits_sup,
            spritesheet='test_sprite.png',
            sprite_actual_x=0,
            sprite_actual_y=0,
            sprites_quantity=4
        )
    
    # Resto dos testes como estavam...

    def test_get_position(self):
        # Test if the position is correctly returned
        self.game_object.get_position = MagicMock(return_value=(50, 50))
        self.assertEqual(self.game_object.get_position(), (50, 50))

    def test_set_position(self):
        # Test setting a new position
        self.game_object.set_position(200, 200)
        self.assertEqual(self.game_object.x_position, 200)
        self.assertEqual(self.game_object.y_position, 200)

    def test_apply_movement(self):
        # Test if the movement is applied correctly
        self.game_object.apply_movement([10, 10])
        self.game_object.set_position.assert_called_with(110, 110)
        
    def test_copy(self):
        # Test copying the ammo object
        ammo = Ammo(10, 10, 10, 10, None, 'ammo.png', 0, 0, 4, 5, 'fire', [0, 1], False, 5)
        copied_ammo = ammo.copy()
        self.assertEqual(copied_ammo.x_position, ammo.x_position)
        self.assertEqual(copied_ammo.y_position, ammo.y_position)
        
    def test_check_load(self):
        # Test check_load function
        weapon = Weapon(100, 100, 10, 10, None, 'weapon.png', 0, 0, 5, 10, 'physical', None, 5, None, None)
        weapon.reload = 4
        self.assertTrue(weapon.check_load())  # Expect True because reload is less than reload_time
    
    def test_fire(self):
        # Test fire function in Weapon class
        weapon = Weapon(100, 100, 10, 10, None, 'weapon.png', 0, 0, 5, 10, 'physical', None, 5, 0, None)
        weapon.check_load = MagicMock(return_value=True)
        ammo = weapon.fire([1, 0])  # Fire in a certain direction
        self.assertIsInstance(ammo, Ammo)  # It should return an Ammo instance

class TestCollectible(unittest.TestCase):
    
    def setUp(self):
        self.collectible = Collectible(
            x_position=100,
            y_position=100,
            width=32,
            height=32,
            map_limits_sup=None,
            spritesheet='collectible.png',
            sprite_actual_x=0,
            sprite_actual_y=0,
            sprites_quantity=4,
            visible=True,
            description="A collectible item"
        )
        
    def test_get_visible(self):
        # Test the getter for the 'visible' property
        self.assertTrue(self.collectible.visible)
    
    def test_set_visible(self):
        # Test the setter for the 'visible' property
        self.collectible.visible = False
        self.assertFalse(self.collectible.visible)


if __name__ == '__main__':
    unittest.main()
