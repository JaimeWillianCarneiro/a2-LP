import unittest
from unittest.mock import patch, MagicMock
import pygame as pg
import numpy as np
from src.classes.character import Character
from src.classes.background import PositionController  # Para garantir que o mock da PositionController seja feito corretamente
from src.settings import SCOOBY_PROFILE  # Para verificar o uso do sprite

class TestCharacter(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        cls.screen = pg.display.set_mode((800, 600))  # Configurando a tela para os testes

    @patch('pygame.image.load')  # Mockando o carregamento da imagem
    def test_init(self, mock_load):
        # Criando um mock para a superfície que seria carregada pela função image.load
        mock_surface = pg.Surface((64, 64))  # Exemplo de tamanho de sprite
        mock_load.return_value = mock_surface  # Retorna a superfície mockada

        # Criando uma instância do Character (a classe abstrata não pode ser instanciada, então substituímos com uma classe concreta)
        class TestCharacterConcrete(Character):
            def update(self):
                pass

        # Criando o objeto de teste
        character = TestCharacterConcrete("TestName", 10, 15, 100, 100, 50, 50, 0, SCOOBY_PROFILE, 100, 10, 500, [], "sword")

        # Verificando se as propriedades iniciais estão corretas
        self.assertEqual(character.name, "TestName")
        self.assertEqual(character.speed, 10)
        self.assertEqual(character.perception, 15)
        self.assertEqual(character.x_position, 100)
        self.assertEqual(character.y_position, 100)
        self.assertEqual(character.width, 50)
        self.assertEqual(character.height, 50)
        self.assertEqual(character.weapon, "sword")

    @patch('pygame.image.load')  # Mockando o carregamento da imagem
    def test_speed_setter(self, mock_load):
        # Mocking the sprite image load
        mock_surface = pg.Surface((64, 64))
        mock_load.return_value = mock_surface
        
        class TestCharacterConcrete(Character):
            def update(self):
                pass

        character = TestCharacterConcrete("TestName", 10, 15, 100, 100, 50, 50, 0, SCOOBY_PROFILE, 100, 10, 500, [], "sword")
        
        # Modificando o speed através do setter
        character.speed = 20
        self.assertEqual(character.speed, 20)

    @patch('pygame.image.load')  # Mockando o carregamento da imagem
    def test_x_position_setter(self, mock_load):
        # Mocking the sprite image load
        mock_surface = pg.Surface((64, 64))
        mock_load.return_value = mock_surface
        
        class TestCharacterConcrete(Character):
            def update(self):
                pass

        character = TestCharacterConcrete("TestName", 10, 15, 100, 100, 50, 50, 0, SCOOBY_PROFILE, 100, 10, 500, [], "sword")
        
        # Modificando a posição x através do setter
        character.x_position = 150
        self.assertEqual(character.x_position, 150)

    @patch('pygame.image.load')  # Mockando o carregamento da imagem
    def test_y_position_setter(self, mock_load):
        # Mocking the sprite image load
        mock_surface = pg.Surface((64, 64))
        mock_load.return_value = mock_surface
        
        class TestCharacterConcrete(Character):
            def update(self):
                pass

        character = TestCharacterConcrete("TestName", 10, 15, 100, 100, 50, 50, 0, SCOOBY_PROFILE, 100, 10, 500, [], "sword")
        
        # Modificando a posição y através do setter
        character.y_position = 200
        self.assertEqual(character.y_position, 200)

    @patch('pygame.image.load')  # Mockando o carregamento da imagem
    def test_width_setter(self, mock_load):
        # Mocking the sprite image load
        mock_surface = pg.Surface((64, 64))
        mock_load.return_value = mock_surface
        
        class TestCharacterConcrete(Character):
            def update(self):
                pass

        character = TestCharacterConcrete("TestName", 10, 15, 100, 100, 50, 50, 0, SCOOBY_PROFILE, 100, 10, 500, [], "sword")
        
        # Modificando a largura através do setter
        character.width = 75
        self.assertEqual(character.width, 75)

    @patch('pygame.image.load')  # Mockando o carregamento da imagem
    def test_height_setter(self, mock_load):
        # Mocking the sprite image load
        mock_surface = pg.Surface((64, 64))
        mock_load.return_value = mock_surface
        
        class TestCharacterConcrete(Character):
            def update(self):
                pass

        character = TestCharacterConcrete("TestName", 10, 15, 100, 100, 50, 50, 0, SCOOBY_PROFILE, 100, 10, 500, [], "sword")
        
        # Modificando a altura através do setter
        character.height = 100
        self.assertEqual(character.height, 100)

    @patch('pygame.image.load')  # Mockando o carregamento da imagem
    def test_aim_setter(self, mock_load):
        # Mocking the sprite image load
        mock_surface = pg.Surface((64, 64))
        mock_load.return_value = mock_surface
        
        class TestCharacterConcrete(Character):
            def update(self):
                pass

        character = TestCharacterConcrete("TestName", 10, 15, 100, 100, 50, 50, 0, SCOOBY_PROFILE, 100, 10, 500, [], "sword")
        
        # Modificando o alvo através do setter
        character.aim = [1.0, 1.0]
        np.testing.assert_array_equal(character.aim, np.array([1.0, 1.0]))  # Comparando arrays numpy

if __name__ == '__main__':
    unittest.main()
