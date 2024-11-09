import pygame as pg
from src.settings import SCREEN_DIMENSIONS, GAME_TITLE

class Fase:
    def __init__(self, screen, background, npcs, game_objects, mandatory_events, optional_events):
        self.screen = screen
        self.background = background
        self.fase_elements = pg.sprite.Group()
        
        # self.player = Character()
        self.npcs = pg.sprite.Group()
        for npc in npcs:
            self.npcs.add(npc)
            self.fase_elements.add(npc)
        # self.monster = Monster()
        # self.scooby_snacks = ScoobySnacks()
        
        self.game_objects = pg.sprite.Group()
        for game_object in game_objects:
            self.game_objects.add(game_object)
            self.fase_elements.add(game_object)
        
        self.mandatory_events = pg.sprite.Group()
        for mandatory_event in mandatory_events:
            self.mandatory_events.add(mandatory_event)
            self.fase_elements.add(mandatory_event)
        
        self.optional_events = pg.sprite.Group()
        for optional_event in optional_events:
            self.optional_events.add(optional_event)
            self.fase_elements.add(optional_event)


    def render_camera(self):
        """ Avalia quais elementos do jogo estão no campo de visão do protagonista para serem renderizados """
        objects_to_render = pg.sprite.spritecollide(self.background, self.game_objects, False)
        npcs_to_render = pg.sprite.spritecollide(self.background, self.npcs, False)
        # npcs_to_render.add(self.monster)
        sprites_to_render = objects_to_render + npcs_to_render
        to_render = pg.sprite.Group()
        for sprite in sprites_to_render:
            to_render.add(sprite)
        
        to_render.draw(self.screen)
            
    
    def check_end():
        """  Verifica se o player passou pela fase (chama a próxima fase e encerra a atual) """
        pass
    
    def check_lost():
        """ Verifica se o player falhou (seja por tempo, seja por vida, seja por falha em algum evento da fase, etc) """
        # if not player.life:
        pass
    
    def update(self, movement):
        self.screen.fill((0, 0, 0))
        pg.draw.rect(self.screen, (255,255,255), self.background)
        # Verifica se o player continua no jogo
        # if self.check_lost():
        #     pass
        
        # Atualiza as variaveis da fase que estao no campo de visao do personagem
        self.fase_elements.update(movement)
        
        self.render_camera()
        
        # Caso o player tenha passado de fase, encerra-a e inicia a proxima
        # check_end():

        return self