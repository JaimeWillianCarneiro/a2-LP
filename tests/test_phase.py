import unittest
from unittest.mock import MagicMock
import pygame as pg
import numpy as np
from src.classes.phase import Phase, Event, Minigame, random_data, SCREEN_DIMENSIONS


class TestPhase(unittest.TestCase):
    def setUp(self):
        """ Configuração inicial para os testes """
        pg.init()
        self.screen = pg.display.set_mode(SCREEN_DIMENSIONS)
        self.phase = Phase(self.screen)

    def tearDown(self):
        """ Finaliza o Pygame após os testes """
        pg.quit()

    def test_check_end_when_collectible_collides(self):
        """ Testa se o método check_end retorna True quando o jogador coleta um item visível """
        self.phase.scooby_snacks.visible = True
        self.phase.player.rect = self.phase.scooby_snacks.rect  # Simula a colisão do jogador com o item
        self.assertTrue(self.phase.check_end())  # Espera que o método retorne True
        
    def test_check_lost_when_player_life_is_zero(self):
        """ Testa se o método check_lost retorna True quando a vida do jogador é 0 """
        self.phase.player.life = 0
        self.assertTrue(self.phase.check_lost())  # Espera que o método retorne True

    def test_check_lost_when_player_has_life(self):
        """ Testa se o método check_lost retorna False quando a vida do jogador é maior que 0 """
        self.phase.player.life = 10
        self.assertFalse(self.phase.check_lost())  # Espera que o método retorne False

    def test_check_collectibles_when_collectibles_are_collected(self):
        """ Testa se o método check_collectibles remove itens do grupo de collectibles quando coletados """
        collectible = MagicMock()
        collectible.visible = True
        collectible.rect.colliderect.return_value = True  # Simula a colisão
        self.phase.player.rect = collectible.rect  # Simula a colisão do jogador com o coletável

        # Adiciona o coletável à lista de collectibles
        self.phase.collectibles.add(collectible)

        # Testa se o método remove o coletável da fase
        self.phase.check_collectibles()
        self.assertNotIn(collectible, self.phase.collectibles)  # O item deve ser removido

if __name__ == '__main__':
    unittest.main()
