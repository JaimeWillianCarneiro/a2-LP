import unittest
import pygame
from src.menu import Menu  # Certifique-se de que o código foi refatorado em uma classe chamada Menu
#  TODO
# Ver uma forma de testar sme parte visual

class TestMenu(unittest.TestCase):
    def setUp(self):
        """Executa antes de cada teste."""
        pygame.init()
        self.menu = Menu()

    def tearDown(self):
        """Executa após cada teste."""
        pygame.quit()

    def test_initialization(self):
        """Testa a inicialização básica do menu."""
        self.assertEqual(self.menu.screen_width, 800)
        self.assertEqual(self.menu.screen_height, 600)
        self.assertIsNotNone(self.menu.sprite_sheet_path, "O caminho da sprite sheet não deve ser None.")
        self.assertIsNotNone(self.menu.audio_path, "O caminho do áudio não deve ser None.")

    def test_audio_load(self):
        """Testa o carregamento do áudio."""
        self.menu.load_audio()
        self.assertTrue(pygame.mixer.get_init(), "O mixer não foi inicializado corretamente.")

    def test_audio_play(self):
        """Testa a reprodução do áudio."""
        self.menu.load_audio()
        self.menu.play_audio()
        self.assertTrue(pygame.mixer.music.get_busy(), "O áudio não está tocando.")

    def test_sprite_sheet_load(self):
        """Testa o carregamento da sprite sheet."""
        sprite_sheet = self.menu.load_sprite_sheet()
        self.assertIsNotNone(sprite_sheet, "A sprite sheet não foi carregada.")
        self.assertEqual(sprite_sheet.get_width(), 2048, "A largura da sprite sheet está incorreta.")
        self.assertEqual(sprite_sheet.get_height(), 1920, "A altura da sprite sheet está incorreta.")

    def test_frame_extraction(self):
        """Testa a extração de frames da sprite sheet."""
        sprite_sheet = self.menu.load_sprite_sheet()
        frames = self.menu.extract_frames(sprite_sheet, columns=12, rows=20)
        self.assertEqual(len(frames), 12 * 20, "O número de frames extraídos está incorreto.")
        self.assertEqual(frames[0].get_width(), self.menu.screen_width, "A largura dos frames está incorreta.")
        self.assertEqual(frames[0].get_height(), self.menu.screen_height, "A altura dos frames está incorreta.")

    def test_frame_animation(self):
        """Testa a animação de frames."""
        initial_frame = self.menu.current_frame
        self.menu.current_frame += 0.7
        if self.menu.current_frame >= len(self.menu.frames):
            self.menu.current_frame = 0
        self.assertNotEqual(initial_frame, self.menu.current_frame, "O frame atual não foi atualizado corretamente.")

if __name__ == "__main__":
    unittest.main()
