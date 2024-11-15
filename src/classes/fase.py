import pygame as pg
from src.settings import SCREEN_DIMENSIONS, GAME_TITLE
from src.classes.gameobejcts import GameObject, Collectible
from src.classes.background import Background, PositionController
import random

def random_data(map_limits_sup):
        # Variavéis fictias para testar a classe Fase ##############
        game_objects = []
        npcs = []
        mandatory_events = []
        optional_events = []
            
        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        width = 100
        height = 150
        
        player = GameObject(SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1], width, height, map_limits_sup)
        monster = GameObject(x, y, width, height, map_limits_sup)
        
        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        scooby_snacks = GameObject(x, y, 50, 50, map_limits_sup)
        
        for _ in range(2):
            x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
            y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
            width = 23
            height = 40
            game_objects.append(GameObject(x,y, width, height, map_limits_sup))
            x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
            y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
            mandatory_events.append(Event(player, (x, y, 100, 75), (x, y, 700, 350), (x+600, y, 100, 75), True, 30*60, map_limits_sup))


            x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
            y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
            width = 67
            height = 100
            npcs.append(GameObject(x,y, width, height, map_limits_sup))
            x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
            y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
            optional_events.append(Event(player, (x, y, 50, 25), (x, y, 150, 50), (x+50, y, 50, 25), False, 30*60, map_limits_sup))
            
        return npcs, game_objects, mandatory_events, optional_events, player, monster, scooby_snacks



class Event(pg.sprite.Sprite):
    def __init__(self, player, start_zone, event_zone, end_zone, is_obrigatory, time, map_limits_sup):
        super().__init__()
        self.in_execution = False
        self.started = False
        self.player = player
        self.position_controller = PositionController(map_limits_sup, event_zone[2], event_zone[3])
        self.x_position = start_zone[0]
        self.x_end_position = end_zone[0]
        self.y_position = start_zone[1]
        self.y_end_position = end_zone[1]
        self.rect = pg.Rect(*start_zone)
        self.event_zone_params = list(event_zone)
        self.end_zone = pg.Rect(*end_zone)
        self.is_obrigatory = is_obrigatory
        self.time = time
        self.image = pg.image.load('lua.png')
        self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.out_zone = True
        
        
    def can_start(self):
        if pg.sprite.collide_rect(self.player, self):
            return True
    
    def get_position(self):
        return self.x_position, self.y_position
        
    def get_end_position(self):
        return self.x_end_position, self.y_end_position
    
    def set_position_rect(self, x_new, y_new):
        self.rect.topleft = x_new, y_new
        
    def set_position_end_rect(self, x_new_end, y_new_end):
        self.end_zone.topleft = x_new_end, y_new_end
    
    def get_time(self):
        return self.time
    
    def set_time(self, new_time):
        self.time = new_time
        
    def pass_time(self):
        new_time = self.get_time()
        new_time -= 1
        self.set_time(new_time)
    
    def check_lost(self):
        pass
    
    def check_end(self):
        if self.player.rect.colliderect(self.end_zone):
            return True
    
    def update(self):
        x_position, y_position = self.get_position()
        x_new, y_new = self.position_controller.apply_translation(x_position, y_position)
        self.set_position_rect(x_new, y_new)
        x_end_position, y_end_position = self.get_end_position()
        x_new_end, y_new_end = self.position_controller.apply_translation(x_end_position, y_end_position)
        self.set_position_end_rect(x_new_end, y_new_end)
        # Rotina do evento
        if self.in_execution:
            self.pass_time()
            self.out_zone = False
            if self.check_lost():
                pass
            elif self.check_end():
                self.in_execution = False
            elif not self.rect.contains(self.player.rect):
                self.player.life -= 0.005
                self.out_zone = True
                
        # Avalia se o usuario entrou no evento
        elif not self.started:
            if self.can_start():
                self.out_zone = False
                self.in_execution = True
                self.started = True
                self.rect = pg.Rect(*self.event_zone_params)
                self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))
            


class Fase:
    def __init__(self, screen):
        self.screen = screen
        self.fase_elements = pg.sprite.Group()
        self.accessible_elements = pg.sprite.Group()
        
        background = Background(self.screen, 'Lua.webp', SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1], 4000, 2000, 'backmusic.mp3', 0.05, [])
        self.background = background
        
        npcs, game_objects, mandatory_events, optional_events, self.player, self.monster, self.scooby_snacks = random_data(list(self.background.get_shape()))
        
        self.fase_elements.add(self.player)
        self.fase_elements.add(self.monster)
        self.fase_elements.add(self.scooby_snacks)
        self.accessible_elements.add(self.monster)
        self.accessible_elements.add(self.scooby_snacks)
        
        
        self.npcs = pg.sprite.Group(npcs)
        self.accessible_elements.add(self.npcs)
        self.fase_elements.add(self.npcs)
            
        self.game_objects = pg.sprite.Group(game_objects)
        self.accessible_elements.add(self.game_objects)
        self.fase_elements.add(self.game_objects)
        
        self.mandatory_events = pg.sprite.Group(mandatory_events)
        self.mandatory_events.add(self.mandatory_events)
        self.fase_elements.add(self.mandatory_events)
        self.current_mandatory_event = next(iter(self.mandatory_events), None)
        self.accessible_elements.add(self.current_mandatory_event)
        self.fase_elements.add(self.current_mandatory_event)
        
        self.optional_events = pg.sprite.Group(optional_events)
        self.accessible_elements.add(self.optional_events)
        self.fase_elements.add(self.optional_events)
        
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
        # Caso o player tenha passado de fase, encerra-a e inicia a proxima
        if self.check_end():
            return Fase(self.screen)
            
        # Verifica se o player continua no jogo
        if not self.check_lost():
            # Aplica o movimento do player e atualiza o background, obtendo o centro do mapa
            movement = self.player.position_controller.normalize_movement(movement)
            self.player.apply_movement(movement)
            self.background.update(*self.player.get_position())
            
            # Atualiza todos os elementos da fase, aplicando a translacao para o novo sistema de coordenadas
            self.fase_elements.update()
            
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
            
            self.player.life -= 0.001 # Linha para limitar o tempo de jogo, somente (Eliminar depois)
        
        self.render_camera()
        
        # font = pg.font.SysFont('arial', 40, True, False)
        
        # title = font.render(GAME_TITLE, True, (123, 123, 123))
        # if self.current_mandatory_event:
        #     if self.current_mandatory_event.in_execution:
        #         if self.current_mandatory_event.out_zone:
        #             warning = font.render('Volte para a Zona', True, (255, 255, 255))
        #             self.screen.blit(warning, (SCREEN_DIMENSIONS[0]/2, 50))
        #         time = str(self.current_mandatory_event.time)
        #         time = font.render(time, True, (255, 255, 255))
        #         self.screen.blit(time, (SCREEN_DIMENSIONS[0]/2, 150))
        # self.screen.blit(title, (50, 50))
        # life = str(int(self.player.life))
        # life = font.render(life, True, (255, 255, 255))
        # self.screen.blit(life, (SCREEN_DIMENSIONS[0]-100, 150))
            
        return self