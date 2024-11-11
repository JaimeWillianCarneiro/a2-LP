import pygame as pg
from src.settings import SCREEN_DIMENSIONS, GAME_TITLE
from src.classes.gameobejcts import GameObject, Collectible
from src.classes.background import Background
import random

class Event(pg.sprite.Sprite):
    def __init__(self, player, start_zone, event_zone, end_zone, is_obrigatory, time):
        super().__init__()
        self.in_execution = False
        self.started = False
        self.player = player
        self.x_position = start_zone[0]
        self.y_position = start_zone[1]
        self.rect = pg.Rect(*start_zone)
        self.event_zone_params = list(event_zone)
        self.end_zone = pg.Rect(*end_zone)
        self.is_obrigatory = is_obrigatory
        self.time = time
        self.image = pg.image.load('lua.png')
        self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))
        
        
    def can_start(self):
        if pg.sprite.collide_rect(self.player, self):
            return True
    
    def set_position(self, movement):
        self.x_position -= movement['x_moved']
        self.y_position -= movement['y_moved']
        end_params = list(self.end_zone.topleft)
        for idx, axis in zip(range(2), movement.keys()):
            self.event_zone_params[idx] -= movement[axis]
            end_params[idx] -= movement[axis]
        
        self.end_zone.topleft = end_params
        self.rect.topleft = self.x_position, self.y_position
        
    def check_lost(self):
        pass
    
    def check_end(self):
        if self.player.rect.colliderect(self.end_zone):
            return True
    
    def update(self, movement):
        self.set_position(movement)
        # Rotina do evento
        if self.in_execution:
            if self.check_lost():
                pass
            elif self.check_end():
                self.in_execution = False
        
        # Avalia se o usuario entrou no evento
        elif not self.started:
            if self.can_start():
                self.in_execution = True
                self.started = True
                self.rect = pg.Rect(*self.event_zone_params)
                self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))
            


class Fase:
    def __init__(self, screen):
        self.screen = screen
        self.immobile_elements = pg.sprite.Group()
        self.mobile_elements = pg.sprite.Group()
        self.accessible_elements = pg.sprite.Group()
        
        # Variavéis fictias para testar a classe Fase ##############
        background = Background(self.screen, 'Lua.webp', SCREEN_DIMENSIONS[0]//2, SCREEN_DIMENSIONS[1]//2, 4000, 2000, 'backmusic.mp3', 0.05, [])
        # background = GameObject(SCREEN_DIMENSIONS[0]//2, SCREEN_DIMENSIONS[1]//2, *SCREEN_DIMENSIONS)
        game_objects = []
        npcs = []
        mandatory_events = []
        optional_events = []
            
        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        width = 100
        height = 150
        self.player = GameObject(SCREEN_DIMENSIONS[0]//2, SCREEN_DIMENSIONS[1]//2, width, height)
        self.monster = GameObject(x,y, width, height)
        
        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        self.scooby_snacks = GameObject(x, y, 50, 50)
        self.background = background
        
        self.mobile_elements.add(self.monster)
        self.accessible_elements.add(self.monster)
        self.mobile_elements.add(self.scooby_snacks)
        self.accessible_elements.add(self.scooby_snacks)
        
        
        for i in range(2):
            x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
            y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
            width = 23
            height = 40
            game_objects.append(GameObject(x,y, width, height))
            x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
            y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
            mandatory_events.append(Event(self.player, (x, y, 100, 75), (x, y, 300, 150), (x+100, y+75, 100, 75), True, 30*60))


            x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
            y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
            width = 67
            height = 100
            npcs.append(GameObject(x,y, width, height))
            x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
            y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
            optional_events.append(Event(self.player, (x, y, 50, 25), (x, y, 150, 50), (x+50, y, 50, 25), False, 30*60))
        #################################################
        
        self.npcs = pg.sprite.Group(npcs)
        self.mobile_elements.add(self.npcs)
        self.accessible_elements.add(self.npcs)
            
        self.game_objects = pg.sprite.Group(game_objects)
        self.mobile_elements.add(self.game_objects)
        self.accessible_elements.add(self.game_objects)
        
        self.mandatory_events = pg.sprite.Group(mandatory_events)
        self.mandatory_events.add(self.mandatory_events)
        self.immobile_elements.add(self.mandatory_events)
        
        self.optional_events = pg.sprite.Group(optional_events)
        self.immobile_elements.add(self.optional_events)
        self.accessible_elements.add(self.optional_events)

        self.current_mandatory_event = next(iter(self.mandatory_events), None)
        
        self.accessible_elements.add(self.current_mandatory_event)
        
        self.background.play_music()

    def render_camera(self):
        """ Avalia quais elementos do jogo sao acessiveis e estao no campo de visao do protagonista para serem renderizados """
        objects_to_render = pg.sprite.spritecollide(self.background, self.accessible_elements, False)
        to_render = pg.sprite.Group()
        to_render.add(self.player)
        for sprite in objects_to_render:
            to_render.add(sprite)
        
        to_render.draw(self.screen)
         
    
    def check_end(self):
        """  Verifica se o player passou pela fase (chama a próxima fase e encerra a atual) """
        if pg.sprite.collide_rect(self.player, self.scooby_snacks) or not self.current_mandatory_event:
            return True
        return False
    
    
    def check_lost(self):
        """ Verifica se o player falhou (seja por tempo, seja por vida, seja por falha em algum evento da fase, etc) """
        if self.player.life <= 0:
            return True
        return False
            
    
    def update(self, movement):
        self.screen.fill((0, 0, 0))
                    
        # Caso o player tenha passado de fase, encerra-a e inicia a proxima
        if self.check_end():
            return Fase(self.screen)
            
            
        # Verifica se o player continua no jogo
        if not self.check_lost():
            non_player_movement, player_movement, map_limits_inf, map_limits_sup = self.background.update(movement)
            
            # Atualiza as variaveis da fase que estao no campo de visao do personagem
            self.mobile_elements.update(non_player_movement, map_limits_inf, map_limits_sup)
            self.immobile_elements.update(non_player_movement)
            self.player.apply_movement(player_movement, map_limits_inf, map_limits_sup)
            
            # Atualizacao do evento obrigatorio atual
            if self.current_mandatory_event.started:
                if not self.current_mandatory_event.in_execution:
                    self.mandatory_events.remove(self.current_mandatory_event)
                    self.accessible_elements.remove(self.current_mandatory_event)
                    self.current_mandatory_event = next(iter(self.mandatory_events), None)
                    if self.current_mandatory_event:
                        self.accessible_elements.add(self.current_mandatory_event)
            
            # Atualizacao dos eventos opcionais
            for optional_event in self.optional_events.sprites():
                if optional_event.started and not optional_event.in_execution:
                    self.optional_events.remove(optional_event)
                    self.accessible_elements.remove(optional_event)
            
            self.player.life -= 0.001
        
        self.render_camera()
            
            
        return self