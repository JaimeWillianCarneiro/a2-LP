import unittest
import pygame as pg
import numpy as np
from src.classes.gameobjects import GameObject, Collectible, Ammo, Weapon
from src.settings import SCOOBY_PROFILE 

class TestGameObjects(unittest.TestCase):
    """Tests the functionality of the GameObjects class."""
    def setUp(self):
        pg.init()
        self.map_limits = [800, 600]
        self.spritesheet = SCOOBY_PROFILE
        self.width = 50
        self.height = 50
        self.sprites_quantity = 3

        # Mock spritesheet
        surface = pg.Surface((self.width * self.sprites_quantity, self.height))
        pg.image.save(surface, self.spritesheet)

        # Initialize objects
        self.game_object = GameObject(100, 100, self.width, self.height, self.map_limits, self.spritesheet, 0, 0, self.sprites_quantity)
        self.collectible = Collectible(200, 200, self.width, self.height, self.map_limits, self.spritesheet, 0, 0, self.sprites_quantity, True, "Test Collectible")
        self.ammo = Ammo(300, 300, self.width, self.height, self.map_limits, self.spritesheet, 0, 0, self.sprites_quantity, 10, ["explosive"], np.array([1, 0]), False, 5)
        self.weapon = Weapon(400, 400, self.width, self.height, self.map_limits, self.spritesheet, 0, 0, self.sprites_quantity, 15, "melee", 100, 10, self.ammo, 50)

    def tearDown(self):
        pg.quit()

    def test_get_position(self):
        """Tests if the `get_position` function returns the expected value."""
        self.assertEqual(self.game_object.get_position(), (100, 100))

    def test_collectible_visibility(self):
        """Tests the object's visibility"""
        self.assertTrue(self.collectible.visible)
        self.collectible.visible = False
        self.assertFalse(self.collectible.visible)

    def test_ammo_properties(self):
        "Test o valor da munição"
        self.assertEqual(self.ammo.damage, 10)
        self.assertEqual(self.ammo.effects, ["explosive"])

    def test_ammo_copy(self):
        new_ammo = self.ammo.copy()
        self.assertEqual(new_ammo.damage, self.ammo.damage)
        self.assertEqual(new_ammo.effects, self.ammo.effects)
        self.assertNotEqual(id(new_ammo), id(self.ammo))

    def test_weapon_fire(self):
        direction = np.array([0, 1])

        # Test firing when reloaded
        fired_bullet = self.weapon.fire(direction)
        self.assertIsNotNone(fired_bullet)
        self.assertIsInstance(fired_bullet, Ammo)
        self.assertTrue(np.array_equal(fired_bullet.direction, direction))

        # Test firing when not reloaded
        fired_bullet = self.weapon.fire(direction)
        self.assertIsNone(fired_bullet)

    def test_weapon_reload(self):
        self.weapon.reloading = True
        self.weapon.update()
        self.assertEqual(self.weapon.reload, 11)

        self.weapon.reload_time = 1  # Simulate full reload
        self.weapon.update()
        self.assertFalse(self.weapon.reloading)

if __name__ == "__main__":
    unittest.main()
