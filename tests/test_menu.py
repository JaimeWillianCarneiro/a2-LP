import unittest
from unittest.mock import Mock, patch
import pygame
from src.classes.menu import Menu, Button, get_font

class TestGetFont(unittest.TestCase):
    """Testa a função get_font para retornar uma fonte válida do pygame."""
    
    def test_get_font(self):
        """Verifica se a função retorna uma fonte válida."""
        font = get_font(30)
        self.assertIsInstance(font, pygame.font.Font)  # Verifica se é uma fonte válida
        # Testa se a função consegue renderizar texto sem erros
        rendered_text = font.render("Test", True, (0, 0, 0))
        self.assertIsInstance(rendered_text, pygame.Surface)  # Verifica se renderiza corretamente

class TestButton(unittest.TestCase):
    """Testa a funcionalidade da classe Button."""
    
    def setUp(self):
        """Configura um botão para os testes."""
        pygame.init()
        self.font = pygame.font.Font(None, 30)
        self.button = Button(
            image=None,
            pos=(100, 100),
            text_input="Test",
            font=self.font,
            base_color="Black",
            hovering_color="White"
        )

    def test_check_for_input_inside(self):
        """Testa se o clique dentro do botão retorna True."""
        self.assertTrue(self.button.check_for_input((100, 100)))

    def test_check_for_input_outside(self):
        """Testa se o clique fora do botão retorna False."""
        self.assertFalse(self.button.check_for_input((200, 200)))

class TestMenu(unittest.TestCase):
    """Testa a funcionalidade da classe Menu."""
    
    def setUp(self):
        """Configura um objeto Menu para os testes."""
        pygame.init()
        self.mock_level = Mock()  # Cria um mock para substituir a dependência de level
        self.menu = Menu(level=self.mock_level)

    @patch("src.classes.menu.pygame.image.load")
    def test_extract_frames(self, mock_load):
        """
        Testa a extração de frames de uma sprite sheet.
        
        Verifica se a quantidade de frames extraídos corresponde ao esperado
        com base no número de colunas e linhas da sprite sheet.
        """
        mock_load.return_value = pygame.Surface((200, 100))
        self.menu.columns = 2
        self.menu.rows = 1
        frames = self.menu.extract_frames()
        self.assertEqual(len(frames), 2)  # Deve haver 2 frames: 2 colunas x 1 linha

if __name__ == "__main__":
    unittest.main()
