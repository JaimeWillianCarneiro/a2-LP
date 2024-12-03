import unittest
import pygame as pg
import numpy as np
from src.classes.background import Background, PositionController
from src.settings import SCREEN_DIMENSIONS, VELMA_PROFILE


class TestBackground(unittest.TestCase):
    def setUp(self):
        # Inicializando o pygame e criando objetos de teste
        pg.init()
        self.screen = pg.Surface(SCREEN_DIMENSIONS)
        self.sprite = VELMA_PROFILE # Criando uma superfície fictícia
        # self.sprite.fill((255, 255, 255))
        self.bg = Background(
            self.screen, 
            self.sprite, 
            500, 400, 
            1000, 800, 
            "assets/sounds/backmusic.mp3", 
            0.5, 
            []
        )
    
    # def test_get_origin(self):
    #     expected_origin = (500 + SCREEN_DIMENSIONS[0], 400 + SCREEN_DIMENSIONS[1])
    #     self.assertEqual(self.bg.get_origin(), expected_origin)
    
    def test_get_shape(self):
        expected_shape = (1000, 800)
        self.assertEqual(self.bg.get_shape(), expected_shape)
    
    def test_get_position(self):
        expected_position = (500 - SCREEN_DIMENSIONS[0] // 2, 400 - SCREEN_DIMENSIONS[1] // 2)
        self.assertEqual(self.bg.get_position(), expected_position)


class TestPositionController(unittest.TestCase):
    def setUp(self):
        # Inicializando o controlador com limites fictícios
        self.controller = PositionController([1000, 800], 200, 150)
    
    def test_normalize_movement(self):
        movement = np.array([3, 4])  # Vetor de teste
        speed = 5
        expected = np.array([3, 4]) / 5 * speed
        np.testing.assert_array_almost_equal(
            self.controller.normalize_movement(movement, speed),
            expected
        )
    
    # def test_to_frame(self):
    #     # Posição dentro dos limites
    #     x, y = 300, 400
    #     self.assertEqual(self.controller.to_frame(x, y), (300, 400))
        
    #     # Posição fora dos limites (abaixo)
    #     x, y = 50, 50
    #     expected = (100, 75)  # Limite inferior do mapa
    #     self.assertEqual(self.controller.to_frame(x, y), expected)
        
    #     # Posição fora dos limites (acima)
    #     x, y = 1100, 900
    #     expected = (800, 650)  # Limite superior do mapa
    #     self.assertEqual(self.controller.to_frame(x, y), expected)
    
    def test_apply_translation(self):
        # Origem configurada para (100, 100)
        PositionController.set_origin(100, 100)
        x, y = 300, 400
        expected = (200, 300)  # Subtração da origem
        self.assertEqual(self.controller.apply_translation(x, y), expected)


if __name__ == "__main__":
    unittest.main()
