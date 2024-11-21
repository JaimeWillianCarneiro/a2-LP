import pygame as pg
from src.settings import SCREEN_DIMENSIONS, FRAME_RATE
from src.classes.gameobejcts import GameObject, Collectible, Ammunition
from src.classes.protagonist import Group1Protagonist
from src.classes.background import Background, PositionController
from src.classes.villain import Villain
import random
import numpy as np

def random_data(background):
    # Variavéis fictias para testar a classe Fase ##############
    map_limits_sup = list(background.get_shape())
    collectibles = []
    npcs = []
    mandatory_events = []
    optional_events = []
        
    x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
    y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
    # width = 75
    # height = 100
    width = 95
    height = 75
    
    ammunition = Ammunition(x_position=x, y_position=y, width=30, height=30, map_limits_sup=map_limits_sup, spritesheet='assets/backgrounds/lua.png', sprite_actual_x=0, sprite_actual_y=0, sprites_quantity=1, damage=1, effects=[], direction=np.zeros(2, dtype=float), recochet=False, speed=7)
    player = Group1Protagonist(name='Scooby', speed=10, perception=23, x_position=SCREEN_DIMENSIONS[0], y_position=SCREEN_DIMENSIONS[1], width=width, height=height, direction=0, skin='default', life=5, inventory=[], ability=1, damage=0.003, trap_power=5, sprites_quantity=4, map_limits_sup=map_limits_sup, scope=300, ammunition=ammunition, bullets=100, reload_time=3)
    
    x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
    y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
    scooby_snacks = Collectible(x, y, 50, 50, map_limits_sup, spritesheet='assets/backgrounds/lua.png', sprite_actual_x=0, sprite_actual_y=0, sprites_quantity=1, visible=False, description='Scooby Snacks')
    
    width = 75
    height = 100
    x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
    y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
    monster = Villain(name='Fred', speed=8, perception=3, x_position=x, y_position=y, width=width, height=height, direction=0, skin='default', life=5, damage=0.007, mem_size=60, vision_field=400, attack_field=50, sprites_quantity=4, background=background, scooby_snacks=scooby_snacks, scope=300, ammunition=ammunition, bullets=100, reload_time=0.1*FRAME_RATE)
    
    for description in ['Moeda de Nero', 'Candelabro']:
        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        width = 23
        height = 40
        collectibles.append(Collectible(x_position=x, y_position=y, width=width, height=height, map_limits_sup=map_limits_sup, spritesheet='assets/backgrounds/lua.png', sprite_actual_x=0, sprite_actual_y=0, sprites_quantity=1, visible=True, description=description))
        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        # mandatory_events.append(Event(1, player=player, start_zone=(x, y, 100, 75), event_zone=(x, y, 700, 350), end_zone=(x+600, y, 100, 75), is_obrigatory=True, map_limits_sup=map_limits_sup))
        mandatory_events.append(Minigame(id_event=1, player=player, start_zone=(x, y, 100, 75), event_zone=(x, y, 700, 350), end_zone=(x+600, y, 100, 75), is_obrigatory=True, map_limits_sup=map_limits_sup, villains=monster, npcs=npcs, time=4*FRAME_RATE))


        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        width = 67
        height = 100
        npcs.append(GameObject(x,y, width, height, map_limits_sup, spritesheet='assets/backgrounds/lua.png', sprite_actual_x=0, sprite_actual_y=0, sprites_quantity=1))
        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        # optional_events.append(Event(player, (x, y, 50, 25), (x, y, 150, 50), (x+50, y, 50, 25), False, 30*60, map_limits_sup))
        optional_events.append(Event(1, player=player, start_zone=(x, y, 50, 25), event_zone=(x, y, 150, 50), end_zone=(x+50, y, 50, 25), is_obrigatory=False, map_limits_sup=map_limits_sup))
        
    return npcs, collectibles, mandatory_events, optional_events, player, monster, scooby_snacks

class Event(pg.sprite.Sprite):
    def __init__(self, id_event, player, start_zone, event_zone, end_zone, is_obrigatory, map_limits_sup):
        super().__init__()
        self.id_event = id_event
        self.completed = False
        self._in_execution = False
        self._started = False
        self.out_zone = True
        self.player = player
        self._position_controller = PositionController(map_limits_sup, event_zone[2], event_zone[3])
        self._x_position = start_zone[0]
        self._x_end_position = end_zone[0]
        self._y_position = start_zone[1]
        self._y_end_position = end_zone[1]
        self.rect = pg.Rect(*start_zone)
        self.event_zone_params = list(event_zone)
        self.end_zone = pg.Rect(*end_zone)
        self.is_obrigatory = is_obrigatory
        self.image = pg.image.load('assets\\backgrounds\\lua.png')
        self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))
    
    @property
    def position_controller(self):
        return self._position_controller
    
    @property
    def in_execution(self):
        return self._in_execution
    
    @in_execution.setter
    def in_execution(self, in_execution_new):
        self._in_execution = in_execution_new
        
    @property
    def started(self):
        return self._started
    
    @started.setter
    def started(self, started_new):
        self._started = started_new
    
    @property
    def x_position(self):
        return self._x_position
    
    @property
    def y_position(self):
        return self._y_position
    
    def get_position(self):
        return self.x_position, self.y_position
    
    @property
    def x_end_position(self):
        return self._x_end_position
    
    @property
    def y_end_position(self):
        return self._y_end_position
        
    def get_end_position(self):
        return self.x_end_position, self.y_end_position
        
    def set_position_rect(self, x_new, y_new):
        self.rect.topleft = (x_new, y_new)
        
    def set_position_end_rect(self, x_new_end, y_new_end):
        self.end_zone.topleft = (x_new_end, y_new_end)
    
    def check_end(self):
        if self.player.rect.colliderect(self.end_zone):
            return True
    
    def can_start(self):
        if pg.sprite.collide_rect(self.player, self):
            return True
    
    def start_event(self):
        self.out_zone = False
        self.in_execution = True
        self.started = True
        self.rect = pg.Rect(*self.event_zone_params)
        self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))
    
    def end_event(self):
        self.in_execution = False
        self.completed = True
    
    def update(self):
        x_position, y_position = self.get_position()
        x_new, y_new = self.position_controller.apply_translation(x_position, y_position)
        self.set_position_rect(x_new, y_new)
        x_end_position, y_end_position = self.get_end_position()
        x_new_end, y_new_end = self.position_controller.apply_translation(x_end_position, y_end_position)
        self.set_position_end_rect(x_new_end, y_new_end)
        # Avalia se o usuario iniciou ou finalizou o evento
        if not self.started:
            if self.can_start():
                self.start_event()
        elif self.in_execution:
            self.out_zone = False
            if self.check_end():
                self.end_event()
                
            
class Minigame(Event):
    def __init__(self, id_event, player, start_zone, event_zone, end_zone, is_obrigatory, map_limits_sup, villains, npcs, time):
        super().__init__(id_event, player, start_zone, event_zone, end_zone, is_obrigatory, map_limits_sup)
        self._time = time
        self.npcs = pg.sprite.Group(npcs)
        self.villains = pg.sprite.Group(villains)
        self._out_zone = True
        self.event_config = {}
    
    @property
    def out_zone(self):
        return self._out_zone
    
    @out_zone.setter
    def out_zone(self, out_zone_new):
        self._out_zone = out_zone_new
        
    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, time_new):
        self._time = time_new
        
    def pass_time(self):
        new_time = self.time
        new_time -= 1
        self.time = new_time
    
    def check_lost(self):
        if self.time <= 0:
            return True
        return False
    
    def start_event(self):
        super().start_event()
        # Faz as alteracoes do inicio do evento
        
        # Muda a skin dos personagens
        
        # Muda o armamento e as posicoes
        
        # Define o comportamento dos npcs
        
        
    def end_event(self):
        super().end_event()
        # Faz as alteracoes do fim do evento
        
        # Muda a skin dos personagens
        
        # Muda o armamento e as posicoes
        
        # Restaura o comportamento dos npcs
        pass
    
    
    def update(self):
        super().update()
        # Rotina do minigame
        if self.in_execution:
            self.pass_time()
            self.out_zone = False
            if self.check_lost():
                self.player.life = 0
            elif not pg.sprite.collide_rect(self, self.player):
                self.player.life -= 0.005
                self.out_zone = True
                

class Fase:
    def __init__(self, screen):
        self.screen = screen
        self.fase_elements = pg.sprite.Group()
        self.accessible_elements = pg.sprite.Group()
        self.collectibles = pg.sprite.Group()
        self.fired = pg.sprite.Group()
        
        background = Background(self.screen, 'assets\\backgrounds\\Lua.webp', SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1], 4000, 2000, 'assets//sounds//backmusic.mp3', 0.05, [])
        self.background = background
        
        npcs, collectibles, mandatory_events, optional_events, self.player, self.monster, self.scooby_snacks = random_data(background)
        
        self.fase_elements.add(self.player)
        # self.fase_elements.add(self.monster)
        self.fase_elements.add(self.scooby_snacks)
        self.accessible_elements.add(self.monster)
        # self.accessible_elements.add(self.scooby_snacks)
        
        
        self.npcs = pg.sprite.Group(npcs)
        self.accessible_elements.add(self.npcs)
        self.fase_elements.add(self.npcs)
            
        self.collectibles = pg.sprite.Group(collectibles)
        self.accessible_elements.add(self.collectibles)
        self.fase_elements.add(self.collectibles)
        
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
        if pg.sprite.collide_rect(self.player, self.scooby_snacks) and self.scooby_snacks.visible:
            return True
        if not self.current_mandatory_event:
            return True
        return False
    
    
    def check_lost(self):
        """ Verifica se o player falhou (seja por tempo, seja por vida, seja por falha em algum evento da fase, etc) """
        if self.player.life <= 0:
            return True
        return False
            
    def check_collectibles(self):
        to_collectible = pg.sprite.spritecollide(self.player, self.collectibles, False)
        for each_collectible in to_collectible:
            if each_collectible.visible:
                # Adiciona ao inventario
                
                # Remove todas as referencias
                each_collectible.kill()
                del each_collectible
                
    def check_fired(self):
        to_fire = pg.sprite.spritecollide(self.player, self.fired, False)
        for each_fired in to_fire:
            # Atinge o jogador
            self.player.life = self.player.life - each_fired.damage
            # Remove todas as referencias
            each_fired.kill()
            del each_fired
    
    def update(self, movement, attack):    
        # Caso o player tenha passado de fase, encerra-a e inicia a proxima
        if self.check_end():
            return Fase(self.screen)
            
        # Verifica se o player continua no jogo
        if not self.check_lost():
            fired = []
            self.player.aim = np.array(attack)
            # print(self.player.aim)
            # Aplica o movimento do player e atualiza o background, obtendo o centro do mapa
            movement = self.player.position_controller.normalize_movement(movement)
            self.player.apply_movement(movement)
            self.background.update(self.player.x_position, self.player.y_position)
            monster_bullets = self.monster.update(self.player)
            fired.extend(monster_bullets)
            self.fase_elements.add(fired)
            self.accessible_elements.add(fired)
            self.fired.add(fired)
            
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
            if len(self.mandatory_events.sprites()) == 1:
                self.scooby_snacks.visible = True
                self.accessible_elements.add(self.scooby_snacks)
            
            # Atualizacao dos eventos opcionais
            for optional_event in self.optional_events.sprites():
                if optional_event.started and not optional_event.in_execution:
                    self.optional_events.remove(optional_event)
                    self.accessible_elements.remove(optional_event)
                    
            # Coleta os coletaveis possiveis
            self.check_collectibles()
            
            # Verifa colisao com projeteis
            self.check_fired()
        
        self.render_camera()
        pg.draw.line(self.screen, (0, 0, 0), self.player.rect.center, (np.array(self.player.rect.center)+self.player.aim*50))
        if self.monster.aim.any():
            pg.draw.line(self.screen, (0, 0, 0), self.monster.rect.center, np.array(self.monster.rect.center) + self.monster.aim*self.monster.scope/np.linalg.norm(self.monster.aim))
            
        return self