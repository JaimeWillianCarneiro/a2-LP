import pygame as pg
from src.settings import SCREEN_DIMENSIONS, FRAME_RATE
from src.classes.gameobjects import GameObject, Collectible, Ammo, Weapon
from src.classes.protagonist import Group1Protagonist
from src.classes.background import Background, PositionController, Interface, CollideController
from src.classes.villain import Villain
import random
import numpy as np
import json

def random_data(background):
    # Variavéis fictias para testar a classe phase ##############
    map_limits_sup = list(background.get_shape())
    collectibles = []
    npcs = []
    game_objects = []
    mandatory_events = []
    optional_events = []
        
    x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
    y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
    # width = 75
    # height = 100
    width = 95
    height = 75
    
    ammunition = Ammo(x_position=x, y_position=y, width=20, height=20, map_limits_sup=map_limits_sup, spritesheet='assets\\backgrounds\\lua.png', sprite_actual_x=0, sprite_actual_y=0, sprites_quantity=1, is_static=False, damage=1, effects=[], direction=np.zeros(2, dtype=float), recochet=False, speed=7)
    
    weapon = Weapon(x_position=x, y_position=y, width=100, height=20, map_limits_sup=map_limits_sup, spritesheet='assets\\backgrounds\\shaggy_right_1.png', sprite_actual_x=0, is_static=False, sprite_actual_y=0, sprites_quantity=1, damage=0.007, kind_damage=None, attack_field=50, reload_time=2*FRAME_RATE, ammo=ammunition, scope=250, special_effect=None)
    
    player = Group1Protagonist(name='Scooby', speed=10, perception=23, x_position=SCREEN_DIMENSIONS[0], y_position=SCREEN_DIMENSIONS[1], width=width, height=height, direction=0, skin='default', life=5, inventory=[], ability=1, sprites_quantity=4, map_limits_sup=map_limits_sup, bullets=100, weapon=weapon, trap_power=3)
    
    x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
    y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
    scooby_snacks = Collectible(x, y, 50, 50, map_limits_sup, spritesheet='assets\\backgrounds\\shaggy_right_1.png', sprite_actual_x=0, sprite_actual_y=0, sprites_quantity=1, is_static=True, visible=False, description='Scooby Snacks')
    
    width = 75
    height = 100
    x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
    y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
    monster = Villain(name='Fred', speed=8, perception=3, x_position=x, y_position=y, width=width, height=height, direction=0, skin='default', life=5, sprites_quantity=4, map_limits_sup=map_limits_sup, bullets=100, weapon=weapon, mem_size=60, vision_field=400, background=background, scooby_snacks=scooby_snacks)

    
    
    for description in ['Moeda de Nero', 'Candelabro']:
        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        width = 23
        height = 40
        collectibles.append(Collectible(x_position=x, y_position=y, width=width, height=height, map_limits_sup=map_limits_sup, spritesheet='assets\\backgrounds\\shaggy_right_1.png', sprite_actual_x=0, sprite_actual_y=0, sprites_quantity=1, is_static=False, visible=True, description=description))
        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        mandatory_events.append(Minigame(id_event=1, player=player, start_zone=(x, y, 100, 75), event_zone=(x, y, 700, 350), end_zone=(x+600, y, 100, 75), is_obrigatory=True, map_limits_sup=map_limits_sup, villains=monster, npcs=npcs, time=4*FRAME_RATE))

        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        width = 67
        height = 100
        npcs.append(GameObject(x,y, width, height, map_limits_sup, spritesheet='assets\\backgrounds\\shaggy_right_1.png', sprite_actual_x=0, sprite_actual_y=0, sprites_quantity=1, is_static=False))
        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        optional_events.append(Event(1, player=player, start_zone=(x, y, 50, 25), event_zone=(x, y, 150, 50), end_zone=(x+50, y, 50, 25), is_obrigatory=False, map_limits_sup=map_limits_sup))
        
        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        game_objects.append(GameObject(x, y, 100, 20, map_limits_sup, 'assets\\backgrounds\\shaggy_right_1.png', 0, 0, 1, True))
        
        
    return npcs, collectibles, game_objects, mandatory_events, optional_events, player, monster, scooby_snacks

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
                print('Cabou tempo\n')
                self.player.life = 0
            elif not pg.sprite.collide_rect(self, self.player):
                self.player.life -= 0.005
                self.out_zone = True

class Dialog(Event):
    def __init__(self):
        pass            

class Phase:
    def __init__(self, screen):
        self.screen = screen
        self.phase_elements = pg.sprite.Group()
        self.collectibles = pg.sprite.Group()
        self.fired = pg.sprite.Group()
        self.monsters = pg.sprite.Group()
        background = Background(self.screen, 'assets\\backgrounds\\Lua.webp', SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1], 4000, 2000, 'assets//sounds//backmusic.mp3', 0.05, [])
        self.background = background
        
        npcs, collectibles, game_objects, mandatory_events, optional_events, self.player, monster, self.scooby_snacks = random_data(background)
        self.monster = monster
        self.monsters.add(monster)
        self.phase_elements.add(self.player)
        self.phase_elements.add(self.scooby_snacks)
        for each_monster in self.monsters.sprites():
            self.phase_elements.add(each_monster.weapon)
        
        self.npcs = pg.sprite.Group(npcs)
        self.phase_elements.add(self.npcs)
            
        self.collectibles = pg.sprite.Group(collectibles)
        self.phase_elements.add(self.collectibles)
        
        self.game_objects = pg.sprite.Group(game_objects)
        self.phase_elements.add(self.game_objects)
        
        self.mandatory_events = pg.sprite.Group(mandatory_events)
        self.phase_elements.add(self.mandatory_events)
        
        self.optional_events = pg.sprite.Group(optional_events)
        self.phase_elements.add(self.optional_events)

        # Gerenciador de colisoes
        self.collide_controller = CollideController(player=self.player, npcs=npcs, villains=self.monsters, game_objects=self.game_objects, collectibles=self.collectibles, ammus=pg.sprite.Group(), mandatory_events=self.mandatory_events, optional_events=self.optional_events, scooby_snacks=self.scooby_snacks, weapons=pg.sprite.Group())

        self.background.play_music()

    def render_camera(self):
        """ Avalia quais elementos do jogo sao acessiveis e estao no campo de visao do protagonista para serem renderizados """
        objects_to_render = pg.sprite.spritecollide(self.background, self.collide_controller.accessible_elements, False)
        to_render = pg.sprite.Group()
        to_render.add(self.player)
        to_render.add(objects_to_render)
        to_render.draw(self.screen)
         
    def check_end(self):
        """  Verifica se o player passou pela phase (chama a próxima phase e encerra a atual) """
        if pg.sprite.collide_rect(self.player, self.scooby_snacks) and self.scooby_snacks.visible:
            return True
        return False
    
    def check_lost(self):
        """ Verifica se o player falhou (seja por tempo, seja por vida, seja por falha em algum evento da phase, etc) """
        return self.player.life <= 0
    
    def update(self, movement, attack):            

        fired = []
        self.player.aim = np.array(attack)

        # Aplica o movimento do player e atualiza o background, obtendo o centro do mapa
        movement = self.player.position_controller.normalize_movement(movement, self.player.speed)
        self.player.apply_movement(movement)
        self.background.update(self.player.x_position, self.player.y_position)
        self.monsters.update(self.player, self.phase_elements, self.collide_controller.accessible_elements, self.fired)
        # fired.extend(monster_bullets)
        # if any(fired):
        #     self.phase_elements.add(fired)
        #     self.collide_controller.accessible_elements.add(fired) #TODO Fase gerencia colisao de player e monstro para animar o ataque
        #     self.fired.add(fired)
        
        # Atualiza todos os elementos da phase, aplicando a translacao para o novo sistema de coordenadas
        self.phase_elements.update()

        self.collide_controller.update()
        self.background.update(self.player.x_position, self.player.y_position)
        self.phase_elements.update()        
        
        self.render_camera()
        pg.draw.line(self.screen, (0, 0, 0), self.player.rect.center, (np.array(self.player.rect.center)+self.player.aim*50))
        if self.monster.aim.any():
            pg.draw.line(self.screen, (0, 0, 0), self.monster.weapon.rect.center, np.array(self.monster.weapon.rect.center) + self.monster.aim*self.monster.weapon.scope/np.linalg.norm(self.monster.aim))
            
    
# Gerenciador()
#     __init__:
#         # count_fase = 0
#         #{'vilao': {'name': 'fred', }
#         # Ler os dados da fase 0
#         self.fase_atual = Phase
#     # if Fase_Atual.check_end():
#         count_fase += 1
#         # Ler os dados da proxima fase
#         fase_atual = Phase(self.scren, #dados da fase)


class PhaseManager:
    def __init__(self, screen, phase_counter = 0):
        self.screen = screen
        self._phase_counter = phase_counter
        # Inicia a primeira fase

        self._current_phase =  None
        self.interface = None
        # self.start_phase()

    
    def start_phase(self):
        self.current_phase = Phase(self.screen)
        with open(f"jsons\\phase_{self.phase_counter}.json", "r") as file:
            phase_data = json.load(file)
            
        # Ler e criar elementos da nova fase
        background = Background(self.screen, phase_data['background']['sprite'], SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1], phase_data['background']['width'], phase_data['background']['height'], phase_data['background']['music'], phase_data['background']['volume'], phase_data['background']['sounds']) 
        map_limits_sup = list(background.get_shape())
        
        ammunition = Ammo(phase_data['ammos']['name']['x_position'], phase_data['ammos']['name']['y_position'], phase_data['ammos']['name']['width'], phase_data['ammos']['name']['height'], map_limits_sup, phase_data['ammos']['name']['spritesheet'], phase_data['ammos']['name']['sprite_actual_x'], phase_data['ammos']['name']['sprite_actual_y'], phase_data['ammos']['name']['sprites_quantity'], phase_data['ammos']['name']['damage'], phase_data['ammos']['name']['effects'], np.zeros(2, dtype=float), phase_data['ammos']['name']['recochet'], phase_data['ammos']['name']['speed'])

        weapon = Weapon(phase_data['weapons']['name']['x_position'], phase_data['weapons']['name']['y_position'], phase_data['weapons']['name']['width'], phase_data['weapons']['name']['height'], map_limits_sup, phase_data['weapons']['name']['spritesheet'], phase_data['weapons']['name']['sprite_actual_x'], phase_data['weapons']['name']['sprite_actual_y'], phase_data['weapons']['name']['sprites_quantity'], phase_data['weapons']['name']['damage'], phase_data['weapons']['name']['kind_damage'], phase_data['weapons']['name']['attack_field'], phase_data['weapons']['name']['reload_time'], ammunition, phase_data['weapons']['name']['scope'], phase_data['weapons']['name']['special_effect'])
        
        player = Group1Protagonist(phase_data['player']['name'], phase_data['player']['speed'], phase_data['player']['perception'], phase_data['player']['x_position'], phase_data['player']['y_position'], phase_data['player']['width'], phase_data['player']['height'], phase_data['player']['direction'], phase_data['player']['skin'], phase_data['player']['life'], phase_data['player']['inventory'], phase_data['player']['ability'], phase_data['player']['sprites_quantity'], map_limits_sup, phase_data['player']['bullets'], phase_data['player']['weapon'], phase_data['player']['trap_power'])
         
        scooby_snacks = Collectible(phase_data['scooby_snacks']['x_position'], phase_data['scooby_snacks']['y_position'], phase_data['scooby_snacks']['width'], phase_data['scooby_snacks']['height'], map_limits_sup, phase_data['scooby_snacks']['spritesheet'], phase_data['scooby_snacks']['sprite_actual_x'], phase_data['scooby_snacks']['sprite_actual_y'], phase_data['scooby_snacks']['sprites_quantity'], phase_data['scooby_snacks']['visible'], phase_data['scooby_snacks']['description'])
        
        villains = []
        for each_villain in phase_data['monsters']:
            villains.append(Villain(each_villain['name'], each_villain['speed'], each_villain['perception'], each_villain['x_position'], each_villain['y_position'], each_villain['width'], each_villain['height'], each_villain['direction'], each_villain['skin'], each_villain['life'], each_villain['sprites_quantity'], map_limits_sup, each_villain['bullets'], weapon, each_villain['mem_size'], each_villain['vision_field'], background, scooby_snacks))
        
        collectibles = []
        for each_collectible in phase_data['collectibles'].keys():
            collectibles.append(Collectible(phase_data['collectibles'][each_collectible]['x_position'], phase_data['collectibles'][each_collectible]['y_position'], phase_data['collectibles'][each_collectible]['width'], phase_data['collectibles'][each_collectible]['height'], map_limits_sup, phase_data['collectibles'][each_collectible]['spritesheet'], phase_data['collectibles'][each_collectible]['sprite_actual_x'], phase_data['collectibles'][each_collectible]['sprite_actual_y'], phase_data['collectibles'][each_collectible]['sprites_quantity'], phase_data['collectibles'][each_collectible]['visible'], phase_data['collectibles'][each_collectible]['description']))
            
        game_objects = []
        for each_game_object in phase_data['game_objects'].keys():
            game_objects.append(GameObject(phase_data['game_objects'][each_game_object]['x_position'], phase_data['game_objects'][each_game_object]['y_position'], phase_data['game_objects'][each_game_object]['width'], phase_data['game_objects'][each_game_object]['height'], map_limits_sup, phase_data['game_objects'][each_game_object]['spritesheet'], phase_data['game_objects'][each_game_object]['sprite_actual_x'], phase_data['game_objects'][each_game_object]['sprite_actual_y'], phase_data['game_objects'][each_game_object]['sprites_quantity']))
    
        npcs = []
        for each_npc in phase_data['npcs'].keys():
            npcs.append(GameObject(phase_data['npcs'][each_npc]['x_position'], phase_data['npcs'][each_npc]['y_position'], phase_data['npcs'][each_npc]['width'], phase_data['npcs'][each_npc]['height'], map_limits_sup, phase_data['npcs'][each_npc]['spritesheet'], phase_data['npcs'][each_npc]['sprite_actual_x'], phase_data['npcs'][each_npc]['sprite_actual_y'], phase_data['npcs'][each_npc]['sprites_quantity']))
        
        mandatory_events = []
        for each_mandatory_event in phase_data['mandatory_events'].keys():
            mandatory_events.append(Minigame(phase_data['mandatory_events'][each_mandatory_event]['id_event'], player, phase_data['mandatory_events'][each_mandatory_event]['start_zone'], phase_data['mandatory_events'][each_mandatory_event]['event_zone'], phase_data['mandatory_events'][each_mandatory_event]['end_zone'], phase_data['mandatory_events'][each_mandatory_event]['is_obrigatory'], map_limits_sup, villains, npcs, phase_data['mandatory_events'][each_mandatory_event]['time']))
        optional_events = []

        for each_optional_event in phase_data['optional_events'].keys():
            optional_events.append(Event(phase_data['optional_events'][each_optional_event]['id_event'], player, phase_data['optional_events'][each_optional_event]['start_zone'], phase_data['optional_events'][each_optional_event]['event_zone'], phase_data['optional_events'][each_optional_event]['end_zone'], phase_data['optional_events'][each_optional_event]['is_obrigatory'], map_limits_sup))

        self.current_phase = Phase(self.screen, background, npcs, collectibles, mandatory_events, optional_events, player, villains[0], scooby_snacks)
        self.interface = Interface(self.screen, self.current_phase, [])
        
        self.dialogue = phase_data['dialogs']['dialog_0']

    
    @property
    def phase_counter(self):
        return self._phase_counter
    
    @phase_counter.setter
    def phase_counter(self, new_phase_counter):
        self._phase_counter = new_phase_counter
    
    @property
    def current_phase(self):
        return self._current_phase
    
    @current_phase.setter
    def current_phase(self, new_phase):
        self._current_phase = new_phase
        
    def update(self, movement, attack):
        # Atualiza a fase atual
        if not self.current_phase.check_lost():
            self.current_phase.update(movement, attack) 
        
        # Verifica a passagem de fase
        if self.current_phase.check_end():
            self.phase_counter += 1
            self.start_phase()
         
        # Atualiza a interface
        self.interface.update()

    def quit_phase(self):
        self.current_phase.background.stop_music()
        self.current_phase = None
