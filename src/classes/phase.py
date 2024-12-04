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
    mandatory_events = []
    optional_events = []
        
    x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
    y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
    # width = 75
    # height = 100
    width = 95
    height = 75
    

    ammunition = Ammo(x_position=x, y_position=y, width=20, height=20, map_limits_sup=map_limits_sup, spritesheet='assets\\backgrounds\\shaggy_right_1.png', sprite_actual_x=0, sprite_actual_y=0, sprites_quantity=1, is_static=False, damage=1, effects=[], direction=np.zeros(2, dtype=float), recochet=False, speed=7)
    
    weapon = Weapon(x_position=x, y_position=y, width=100, height=20, map_limits_sup=map_limits_sup, spritesheet='assets\\backgrounds\\shaggy_right_1.png', sprite_actual_x=0, is_static=False, sprite_actual_y=0, sprites_quantity=1, damage=0.007, kind_damage=None, attack_field=50, reload_time=2*FRAME_RATE, ammo=ammunition, scope=250, special_effect=None)

    player = Group1Protagonist(name='Scooby', speed=10, perception=23, x_position=SCREEN_DIMENSIONS[0], y_position=SCREEN_DIMENSIONS[1], width=width, height=height, direction=0, skin='default', life=5, inventory=[], ability=1, sprites_quantity=4, map_limits_sup=map_limits_sup, bullets=100, weapon=weapon, trap_power=3)
    
    x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
    y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
    scooby_snacks = Collectible(x, y, 50, 50, map_limits_sup, spritesheet='assets\\backgrounds\\shaggy_right_1.png', sprite_actual_x=0, sprite_actual_y=0, sprites_quantity=1, visible=False, description='Scooby Snacks')
    
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
        collectibles.append(Collectible(x_position=x, y_position=y, width=width, height=height, map_limits_sup=map_limits_sup, spritesheet='assets\\backgrounds\\shaggy_right_1.png', sprite_actual_x=0, sprite_actual_y=0, sprites_quantity=1, visible=True, description=description))
        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        mandatory_events.append(Minigame(id_event=1, player=player, start_zone=(x, y, 100, 75), event_zone=(x, y, 700, 350), end_zone=(x+600, y, 100, 75), is_mandatory=True, map_limits_sup=map_limits_sup, villains=monster, npcs=npcs, time=4*FRAME_RATE))


        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        width = 67
        height = 100
        npcs.append(GameObject(x,y, width, height, map_limits_sup, spritesheet='assets\\backgrounds\\shaggy_right_1.png', sprite_actual_x=0, sprite_actual_y=0, sprites_quantity=1))
        x = random.choice(range(SCREEN_DIMENSIONS[0]*2))
        y = random.choice(range(SCREEN_DIMENSIONS[1]*2))
        optional_events.append(Event(1, player=player, start_zone=(x, y, 50, 25), event_zone=(x, y, 150, 50), end_zone=(x+50, y, 50, 25), is_mandatory=False, map_limits_sup=map_limits_sup))
        
    return npcs, collectibles, mandatory_events, optional_events, player, monster, scooby_snacks
    
class Event(pg.sprite.Sprite):
    """
    Representa um evento no jogo que pode ser iniciado e concluído pelo jogador. O evento possui uma zona de início, 
    uma zona de término e uma zona de execução onde o evento ocorre. O evento pode ser obrigatório ou opcional e é 
    controlado por interações com o jogador.

    Parameters
    ----------
    id_event : int
        O identificador único do evento.
    player : pg.sprite.Sprite
        O objeto jogador que interage com o evento.
    start_zone : tuple
        As coordenadas (x, y) e as dimensões (largura, altura) da zona de início do evento.
    event_zone : tuple
        As coordenadas (x, y) e as dimensões (largura, altura) da zona onde o evento é executado.
    end_zone : tuple
        As coordenadas (x, y) e as dimensões (largura, altura) da zona de término do evento.
    is_mandatory : bool
        Um valor booleano que indica se o evento é obrigatório para o progresso do jogo.
    map_limits_sup : tuple
        Limite superior do mapa para restrição de movimento.

    Attributes
    ----------
    position_controller : PositionController
        Controlador de posição que lida com as restrições de movimento do evento.
    in_execution : bool
        Indica se o evento está atualmente em execução.
    started : bool
        Indica se o evento foi iniciado.
    x_position : float
        A posição X do evento.
    y_position : float
        A posição Y do evento.
    x_end_position : float
        A posição X de término do evento.
    y_end_position : float
        A posição Y de término do evento.
    completed : bool
        Indica se o evento foi completado.
    out_zone : bool
        Indica se o jogador está fora da zona do evento.
    is_mandatory : bool
        Indica se o evento é obrigatório.
    """
    def __init__(self, id_event, player, start_zone, event_zone, end_zone, is_mandatory, map_limits_sup):
        """
        Inicializa um novo evento com as zonas de início, execução e término, além das propriedades que controlam 
        o status do evento e interações com o jogador.

        Parameters
        ----------
        id_event : int
            O identificador único do evento.
        player : pg.sprite.Sprite
            O objeto jogador que interage com o evento.
        start_zone : tuple
            As coordenadas (x, y) e as dimensões (largura, altura) da zona de início do evento.
        event_zone : tuple
            As coordenadas (x, y) e as dimensões (largura, altura) da zona onde o evento é executado.
        end_zone : tuple
            As coordenadas (x, y) e as dimensões (largura, altura) da zona de término do evento.
        is_mandatory : bool
            Um valor booleano que indica se o evento é obrigatório para o progresso do jogo.
        map_limits_sup : tuple
            Limite superior do mapa para restrição de movimento.
        """
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
        self.is_mandatory = is_mandatory
        self.image = pg.image.load('assets\\backgrounds\\lua.png')
        self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))
    
    @property
    def position_controller(self):
        """
        Retorna o controlador de posição associado ao evento, responsável por gerenciar restrições de movimento.

        Returns
        -------
        PositionController
            O controlador de posição do evento.
        """
        return self._position_controller
    
    @property
    def in_execution(self):
        """
        Retorna se o evento está em execução.

        Returns
        -------
        bool
            True se o evento está em execução, False caso contrário.
        """
        return self._in_execution
    
    @in_execution.setter
    def in_execution(self, in_execution_new):
        """
        Define o status de execução do evento.

        Parameters
        ----------
        in_execution_new : bool
            O novo status de execução do evento.
        """
        self._in_execution = in_execution_new
        
    @property
    def started(self):
        """
        Retorna se o evento foi iniciado.

        Returns
        -------
        bool
            True se o evento foi iniciado, False caso contrário.
        """
        return self._started
    
    @started.setter
    def started(self, started_new):
        """
        Define o status de início do evento.

        Parameters
        ----------
        started_new : bool
            O novo status de início do evento.
        """
        self._started = started_new
    
    @property
    def x_position(self):
        """
        Retorna a posição X do evento.

        Returns
        -------
        float
            A posição X do evento.
        """
        return self._x_position
    
    @property
    def y_position(self):
        """
        Retorna a posição Y do evento.

        Returns
        -------
        float
            A posição Y do evento.
        """
        return self._y_position
    
    def get_position(self):
        """
        Retorna a posição atual do evento.

        Returns
        -------
        tuple
            A posição X e Y do evento.
        """
        return self.x_position, self.y_position
    
    @property
    def x_end_position(self):
        """
        Retorna a posição X de término do evento.

        Returns
        -------
        float
            A posição X de término do evento.
        """
        return self._x_end_position
    
    @property
    def y_end_position(self):
        """
        Retorna a posição Y de término do evento.

        Returns
        -------
        float
            A posição Y de término do evento.
        """
        return self._y_end_position
        
    def get_end_position(self):
        """
        Retorna a posição de término do evento.

        Returns
        -------
        tuple
            A posição X e Y de término do evento.
        """

        return self.x_end_position, self.y_end_position
        
    def set_position_rect(self, x_new, y_new):
        """
        Define a posição do evento atual no mapa.

        Parameters
        ----------
        x_new : float
            A nova posição X do evento.
        y_new : float
            A nova posição Y do evento.
        """
        self.rect.topleft = (x_new, y_new)
        
    def set_position_end_rect(self, x_new_end, y_new_end):
        """
        Define a posição da zona de término do evento no mapa.

        Parameters
        ----------
        x_new_end : float
            A nova posição X da zona de término.
        y_new_end : float
            A nova posição Y da zona de término.
        """
        self.end_zone.topleft = (x_new_end, y_new_end)
    
    def check_end(self):
        """
        Verifica se o jogador entrou na zona de término do evento.

        Returns
        -------
        bool
            True se o jogador está na zona de término, False caso contrário.
        """
        if self.player.rect.colliderect(self.end_zone):
            return True
    
    def can_start(self):
        """
        Verifica se o jogador entrou na zona de início do evento, permitindo seu início.

        Returns
        -------
        bool
            True se o jogador entrou na zona de início, False caso contrário.
        """
        if pg.sprite.collide_rect(self.player, self):
            return True
    
    def start_event(self):
        """
        Inicia o evento, marcando-o como iniciado e configurando a zona de execução.

        Este método também altera o status do evento para em execução.
        """
        self.out_zone = False
        self.in_execution = True
        self.started = True
        self.rect = pg.Rect(*self.event_zone_params)
        self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))
    
    def end_event(self):
        """
        Finaliza o evento, marcando-o como concluído e removendo-o da execução.
        """
        self.in_execution = False
        self.completed = True
    
    def update(self):
        """
        Atualiza a posição do evento e verifica se o evento foi iniciado ou concluído.

        Se o evento não foi iniciado e o jogador entrou na zona de início, o evento é iniciado.
        Se o evento está em execução e o jogador entrou na zona de término, o evento é concluído.
        """
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
    """
    Representa um minijogo no qual o jogador deve cumprir um objetivo dentro de um tempo determinado, 
    enfrentando vilões e interagindo com NPCs. O evento inclui uma contagem regressiva, o que permite 
    ao jogador perder o minijogo caso o tempo acabe.

    Parameters
    ----------
    id_event : int
        O identificador único do evento.
    player : pg.sprite.Sprite
        O objeto jogador que interage com o evento.
    start_zone : tuple
        As coordenadas (x, y) e as dimensões (largura, altura) da zona de início do evento.
    event_zone : tuple
        As coordenadas (x, y) e as dimensões (largura, altura) da zona onde o evento é executado.
    end_zone : tuple
        As coordenadas (x, y) e as dimensões (largura, altura) da zona de término do evento.
    is_mandatory : bool
        Um valor booleano que indica se o evento é obrigatório para o progresso do jogo.
    map_limits_sup : tuple
        Limite superior do mapa para restrição de movimento.
    villains : list
        Lista de vilões que participam do minijogo.
    npcs : list
        Lista de NPCs que participam do minijogo.
    time : int
        O tempo inicial (em segundos) para o minijogo.

    Attributes
    ----------
    out_zone : bool
        Indica se o jogador está fora da zona do evento.
    time : int
        O tempo restante para o minijogo.
    villains : pg.sprite.Group
        Grupo de vilões que estão participando do minijogo.
    npcs : pg.sprite.Group
        Grupo de NPCs que estão participando do minijogo.
    event_config : dict
        Dicionário que contém a configuração específica do evento.
    """
    def __init__(self, id_event, player, start_zone, event_zone, end_zone, is_mandatory, map_limits_sup, villains, npcs, time):
        """
        Inicializa o minijogo, configurando o tempo, os NPCs, os vilões e a zona de interação, 
        além de definir os atributos herdados da classe `Event`.

        Parameters
        ----------
        id_event : int
            O identificador único do evento.
        player : pg.sprite.Sprite
            O objeto jogador que interage com o evento.
        start_zone : tuple
            As coordenadas (x, y) e as dimensões (largura, altura) da zona de início do evento.
        event_zone : tuple
            As coordenadas (x, y) e as dimensões (largura, altura) da zona onde o evento é executado.
        end_zone : tuple
            As coordenadas (x, y) e as dimensões (largura, altura) da zona de término do evento.
        is_mandatory : bool
            Um valor booleano que indica se o evento é obrigatório para o progresso do jogo.
        map_limits_sup : tuple
            Limite superior do mapa para restrição de movimento.
        villains : list
            Lista de vilões que participam do minijogo.
        npcs : list
            Lista de NPCs que participam do minijogo.
        time : int
            O tempo inicial (em segundos) para o minijogo.
        """
        super().__init__(id_event, player, start_zone, event_zone, end_zone, is_mandatory, map_limits_sup)
        self._time = time
        self.npcs = pg.sprite.Group(npcs)
        self.villains = pg.sprite.Group(villains)
        self._out_zone = True
        self.event_config = {}
        
    
    @property
    def out_zone(self):
        """
        Retorna se o jogador está fora da zona do minijogo.

        Returns
        -------
        bool
            True se o jogador está fora da zona, False caso contrário.
        """
        return self._out_zone
    
    @out_zone.setter
    def out_zone(self, out_zone_new):
        """
        Define o status de estar fora da zona do minijogo.

        Parameters
        ----------
        out_zone_new : bool
            O novo status de estar fora da zona.
        """        
        self._out_zone = out_zone_new
        
    @property
    def time(self):
        """
        Retorna o tempo restante para o minijogo.

        Returns
        -------
        int
            O tempo restante em segundos.
        """
        return self._time
    
    @time.setter
    def time(self, time_new):
        """
        Define o novo tempo restante para o minijogo.

        Parameters
        ----------
        time_new : int
            O novo tempo restante em segundos.
        """
        self._time = time_new
        
    def pass_time(self):
        """
        Diminui o tempo restante para o minijogo em 1 segundo.
        """
        new_time = self.time
        new_time -= 1
        self.time = new_time
    
    def check_lost(self):
        """
        Verifica se o tempo do minijogo acabou.

        Returns
        -------
        bool
            True se o tempo acabou, False caso contrário.
        """
        if self.time <= 0:
            return True
        return False
    
    def start_event(self):
        """
        Inicia o minijogo, configurando a zona de execução e realizando 
        modificações como mudar a skin dos personagens e alterar o comportamento 
        dos NPCs e vilões.
        """
        super().start_event()
        # Faz as alteracoes do inicio do evento
        
        # Muda a skin dos personagens
        
        # Muda o armamento e as posicoes
        
        # Define o comportamento dos npcs
        
        
    def end_event(self):
        """
        Finaliza o minijogo, restaurando as configurações anteriores dos personagens, 
        NPCs e vilões, e revertendo quaisquer alterações feitas durante a execução.
        """
        super().end_event()
        # Faz as alteracoes do fim do evento
        
        # Muda a skin dos personagens
        
        # Muda o armamento e as posicoes
        
        # Restaura o comportamento dos npcs
        pass
    
    
    def update(self):
        """
        Atualiza o estado do minijogo. Verifica o tempo restante, se o jogador 
        está fora da zona do evento e se o tempo acabou, causando a derrota do jogador.

        Caso o jogador saia da zona, ele perde vida progressivamente.
        """
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

class Phase:
    """
    Representa uma fase do jogo, contendo todos os elementos interativos e objetos necessários para o progresso do jogo. 
    A fase gerencia a renderização dos elementos visíveis, a movimentação do jogador, a interação com objetos e eventos, 
    e verifica as condições de vitória ou derrota.

    Parameters
    ----------
    screen : pg.Surface
        A superfície de exibição onde os elementos da fase serão desenhados.
    background : Background
        O fundo da fase, que também pode controlar a música e outros efeitos relacionados ao ambiente.
    npcs : list
        Lista de NPCs que interagem com o jogador e outros elementos da fase.
    collectibles : list
        Lista de objetos colecionáveis presentes na fase.
    mandatory_events : list
        Lista de eventos obrigatórios para o progresso da fase.
    optional_events : list
        Lista de eventos opcionais que podem ser completados pelo jogador.
    player : Player
        O personagem principal controlado pelo jogador.
    monster : Monster
        O monstro que interage com o jogador durante a fase.
    game_objects : list
        Lista de objetos do jogo, como plataformas, obstáculos, etc.
    scooby_snacks : ScoobySnack
        O item de vitória que o jogador deve alcançar para completar a fase.

    Attributes
    ----------
    screen : pg.Surface
        A superfície onde a fase será renderizada.
    phase_elements : pg.sprite.Group
        Grupo contendo todos os elementos da fase, como NPCs, vilões, eventos e objetos.
    accessible_elements : pg.sprite.Group
        Grupo contendo elementos que o jogador pode acessar ou interagir.
    collectibles : pg.sprite.Group
        Grupo de itens colecionáveis.
    fired : pg.sprite.Group
        Grupo de projéteis disparados durante o jogo.
    background : Background
        O fundo da fase, incluindo música e controle de visualização.
    player : Player
        O personagem principal do jogador.
    scooby_snacks : ScoobySnack
        O item que define o fim da fase.
    monster : Monster
        O monstro que interage com o jogador.
    monsters : pg.sprite.Group
        Grupo de vilões presentes na fase.
    npcs : pg.sprite.Group
        Grupo de NPCs presentes na fase.
    game_objects : pg.sprite.Group
        Grupo de objetos do jogo.
    mandatory_events : pg.sprite.Group
        Eventos obrigatórios para completar a fase.
    optional_events : pg.sprite.Group
        Eventos opcionais que o jogador pode completar.
    collide_controller : CollideController
        Controlador de colisões que gerencia as interações entre os elementos da fase.
    
    Methods
    -------
    render_camera()
        Avalia quais elementos do jogo são acessíveis e estão no campo de visão do protagonista para serem renderizados.
    check_end()
        Verifica se o jogador passou pela fase, completando-a.
    check_lost()
        Verifica se o jogador falhou na fase devido a perda de vida ou falha em algum evento.
    update(movement, attack)
        Atualiza o estado da fase, aplicando movimento ao jogador, verificando colisões e renderizando os elementos da fase.
    """
    def __init__(self, screen, background, npcs, collectibles, mandatory_events, optional_events, player, monster, game_objects, scooby_snacks):
        """
        Inicializa a fase com todos os elementos interativos e objetos do jogo.

        Parameters
        ----------
        screen : pg.Surface
            A superfície de exibição onde os elementos da fase serão desenhados.
        background : Background
            O fundo da fase, que também pode controlar a música e outros efeitos relacionados ao ambiente.
        npcs : list
            Lista de NPCs que interagem com o jogador e outros elementos da fase.
        collectibles : list
            Lista de objetos colecionáveis presentes na fase.
        mandatory_events : list
            Lista de eventos obrigatórios para o progresso da fase.
        optional_events : list
            Lista de eventos opcionais que podem ser completados pelo jogador.
        player : Player
            O personagem principal controlado pelo jogador.
        monster : Monster
            O monstro que interage com o jogador durante a fase.
        game_objects : list
            Lista de objetos do jogo, como plataformas, obstáculos, etc.
        scooby_snacks : ScoobySnack
            O item de vitória que o jogador deve alcançar para completar a fase.
        """
        self.screen = screen
        self.phase_elements = pg.sprite.Group()
        self.accessible_elements = pg.sprite.Group()
        self.collectibles = pg.sprite.Group()
        self.fired = pg.sprite.Group()
        
        self.background = background
        self.player = player
        self.scooby_snacks = scooby_snacks
        
        self.monster = monster
        self.monsters = pg.sprite.Group(self.monster)
        
        self.phase_elements.add(self.player)
        self.phase_elements.add(self.scooby_snacks)
        self.accessible_elements.add(self.monster)
        
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
        self.collide_controller = CollideController(player=self.player, npcs=npcs, villains=self.monsters, game_objects=self.game_objects, collectibles=self.collectibles, ammus=pg.sprite.Group(), mandatory_events=self.mandatory_events, optional_events=self.optional_events, scooby_snacks=self.scooby_snacks, weapons=pg.sprite.Group(each_monster.weapon), phase_elements=self.phase_elements)

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
        """
        Atualiza o estado da fase, aplicando movimento ao jogador, verificando colisões 
        e renderizando os elementos da fase. Também realiza verificações de vitória e derrota.

        Parameters
        ----------
        movement : np.array
            Vetor de movimento do jogador.
        attack : np.array
            Vetor que representa a direção do ataque do jogador.
        """
        self.player.aim = np.array(attack)

        # Aplica o movimento do player e atualiza o background, obtendo o centro do mapa
        movement = self.player.position_controller.normalize_movement(movement, self.player.speed)
        self.player.apply_movement(movement)
        self.background.update(self.player.x_position, self.player.y_position)
        self.monsters.update(self.player)
        
        # Atualiza todos os elementos da phase, aplicando a translacao para o novo sistema de coordenadas
        self.phase_elements.update()

        self.collide_controller.update(self.phase_elements)
        self.background.update(self.player.x_position, self.player.y_position)
        self.phase_elements.update()     
        
        self.render_camera()
        pg.draw.line(self.screen, (0, 0, 0), self.player.rect.center, (np.array(self.player.rect.center)+self.player.aim*50))
        if self.monster.aim.any():
            pg.draw.line(self.screen, (0, 0, 0), self.monster.weapon.rect.center, np.array(self.monster.weapon.rect.center) + self.monster.aim*self.monster.weapon.scope/np.linalg.norm(self.monster.aim))


class PhaseManager:
    """
    Classe responsável por gerenciar as fases do jogo. Controla a transição entre as fases, 
    a inicialização dos elementos de cada fase e a atualização da interface.

    Atributos:
        screen (Surface): A tela onde os elementos do jogo serão renderizados.
        _phase_counter (int): O contador da fase atual.
        _current_phase (Phase, opcional): A fase que está em andamento.
        interface (Interface): A interface do jogo, responsável pela interação com o jogador.
        current_dialogue (int): Índice do diálogo atual.
        dialogue (dict): Dicionário contendo os diálogos da fase.

    Métodos:
        start_phase: Inicia a fase atual, carregando todos os elementos do arquivo JSON correspondente.
        phase_counter: Getter e setter para o contador de fases.
        current_phase: Getter e setter para a fase atual.
        update: Atualiza a fase atual e a interface, além de verificar a transição entre fases.
        quit_phase: Encerra a fase atual e para a música de fundo.
    """
    def __init__(self, screen, phase_counter = 0):
        """
        Inicializa o gerenciador de fases.

        Parâmetros:
            screen (Surface): A tela onde os elementos do jogo serão renderizados.
            phase_counter (int, opcional): O contador da fase atual. Padrão é 0.
        """
        self.screen = screen
        self._phase_counter = phase_counter
        # Inicia a primeira fase
        self._current_phase =  None
        self.interface = None
        # self.start_phase()

        with open(f"jsons\\cutscene_dialogs.json", "r") as file:
            cutscene = json.load(file)
        self.current_dialogue = 0
        self.dialogues = cutscene['dialogs']
    
    def start_phase(self):
        """
        Inicia a fase atual, carregando os elementos e a música de fundo a partir de um arquivo JSON.

        O arquivo JSON contém dados sobre os elementos da fase, como o fundo, inimigos, objetos coletáveis,
        eventos obrigatórios e opcionais, e o personagem jogador. Todos os elementos são instanciados e
        adicionados à fase.
        """
        with open(f"jsons\\phase_{self.phase_counter}.json", "r") as file:
            phase_data = json.load(file)
            
        # Ler e criar elementos da nova fase
        background = Background(self.screen, phase_data['background']['sprite'], SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1], phase_data['background']['width'], phase_data['background']['height'], phase_data['background']['music'], phase_data['background']['volume'], phase_data['background']['sounds']) 
        map_limits_sup = list(background.get_shape())
        
        ammunition = Ammo(phase_data['ammos']['name']['x_position'], phase_data['ammos']['name']['y_position'], phase_data['ammos']['name']['width'], phase_data['ammos']['name']['height'], map_limits_sup, phase_data['ammos']['name']['spritesheet'], phase_data['ammos']['name']['sprite_actual_x'], phase_data['ammos']['name']['sprite_actual_y'], phase_data['ammos']['name']['sprites_quantity'], phase_data['ammos']['name']['is_static'], phase_data['ammos']['name']['damage'], phase_data['ammos']['name']['effects'], np.zeros(2, dtype=float), phase_data['ammos']['name']['recochet'], phase_data['ammos']['name']['speed'])

        weapon = Weapon(phase_data['weapons']['name']['x_position'], phase_data['weapons']['name']['y_position'], phase_data['weapons']['name']['width'], phase_data['weapons']['name']['height'], map_limits_sup, phase_data['weapons']['name']['spritesheet'], phase_data['weapons']['name']['sprite_actual_x'], phase_data['weapons']['name']['sprite_actual_y'], phase_data['weapons']['name']['sprites_quantity'], phase_data['weapons']['name']['is_static'], phase_data['weapons']['name']['damage'], phase_data['weapons']['name']['kind_damage'], phase_data['weapons']['name']['attack_field'], phase_data['weapons']['name']['reload_time'], ammunition, phase_data['weapons']['name']['scope'], phase_data['weapons']['name']['special_effect'])
        
        player = Group1Protagonist(phase_data['player']['name'], phase_data['player']['speed'], phase_data['player']['perception'], phase_data['player']['x_position'], phase_data['player']['y_position'], phase_data['player']['width'], phase_data['player']['height'], phase_data['player']['direction'], phase_data['player']['skin'], phase_data['player']['life'], phase_data['player']['inventory'], phase_data['player']['ability'], phase_data['player']['sprites_quantity'], map_limits_sup, phase_data['player']['bullets'], phase_data['player']['weapon'], phase_data['player']['trap_power'])
        
        scooby_snacks = Collectible(phase_data['scooby_snacks']['x_position'], phase_data['scooby_snacks']['y_position'], phase_data['scooby_snacks']['width'], phase_data['scooby_snacks']['height'], map_limits_sup, phase_data['scooby_snacks']['spritesheet'], phase_data['scooby_snacks']['sprite_actual_x'], phase_data['scooby_snacks']['sprite_actual_y'], phase_data['scooby_snacks']['sprites_quantity'], phase_data['scooby_snacks']['is_static'], phase_data['scooby_snacks']['visible'], phase_data['scooby_snacks']['description'])
        
        villains = []
        for each_villain in phase_data['monsters']:
            villains.append(Villain(each_villain['name'], each_villain['speed'], each_villain['perception'], each_villain['x_position'], each_villain['y_position'], each_villain['width'], each_villain['height'], each_villain['direction'], each_villain['skin'], each_villain['life'], each_villain['sprites_quantity'], map_limits_sup, each_villain['bullets'], weapon, each_villain['mem_size'], each_villain['vision_field'], background, scooby_snacks))

        collectibles = []
        for each_collectible in phase_data['collectibles'].keys():
            collectibles.append(Collectible(phase_data['collectibles'][each_collectible]['x_position'], phase_data['collectibles'][each_collectible]['y_position'], phase_data['collectibles'][each_collectible]['width'], phase_data['collectibles'][each_collectible]['height'], map_limits_sup, phase_data['collectibles'][each_collectible]['spritesheet'], phase_data['collectibles'][each_collectible]['sprite_actual_x'], phase_data['collectibles'][each_collectible]['sprite_actual_y'], phase_data['collectibles'][each_collectible]['sprites_quantity'], phase_data['collectibles'][each_collectible]['is_static'], phase_data['collectibles'][each_collectible]['visible'], phase_data['collectibles'][each_collectible]['description']))
        
        
        game_objects = []
        for each_game_object in phase_data['game_objects'].keys():
            game_objects.append(GameObject(phase_data['game_objects'][each_game_object]['x_position'], phase_data['game_objects'][each_game_object]['y_position'], phase_data['game_objects'][each_game_object]['width'], phase_data['game_objects'][each_game_object]['height'], map_limits_sup, phase_data['game_objects'][each_game_object]['spritesheet'], phase_data['game_objects'][each_game_object]['sprite_actual_x'], phase_data['game_objects'][each_game_object]['sprite_actual_y'], phase_data['game_objects'][each_game_object]['sprites_quantity'], phase_data['game_objects'][each_game_object]['is_static']))
    
        npcs = []
        for each_npc in phase_data['npcs'].keys():
            npcs.append(GameObject(phase_data['npcs'][each_npc]['x_position'], phase_data['npcs'][each_npc]['y_position'], phase_data['npcs'][each_npc]['width'], phase_data['npcs'][each_npc]['height'], map_limits_sup, phase_data['npcs'][each_npc]['spritesheet'], phase_data['npcs'][each_npc]['sprite_actual_x'], phase_data['npcs'][each_npc]['sprite_actual_y'], phase_data['npcs'][each_npc]['sprites_quantity'], is_static=False))
        
        mandatory_events = []
        for each_mandatory_event in phase_data['mandatory_events'].keys():
            mandatory_events.append(Minigame(phase_data['mandatory_events'][each_mandatory_event]['id_event'], player, phase_data['mandatory_events'][each_mandatory_event]['start_zone'], phase_data['mandatory_events'][each_mandatory_event]['event_zone'], phase_data['mandatory_events'][each_mandatory_event]['end_zone'], phase_data['mandatory_events'][each_mandatory_event]['is_obrigatory'], map_limits_sup, villains, npcs, phase_data['mandatory_events'][each_mandatory_event]['time']))
        optional_events = []

        for each_optional_event in phase_data['optional_events'].keys():
            optional_events.append(Event(phase_data['optional_events'][each_optional_event]['id_event'], player, phase_data['optional_events'][each_optional_event]['start_zone'], phase_data['optional_events'][each_optional_event]['event_zone'], phase_data['optional_events'][each_optional_event]['end_zone'], phase_data['optional_events'][each_optional_event]['is_obrigatory'], map_limits_sup))

        self.current_phase = Phase(self.screen, background, npcs, collectibles, mandatory_events, optional_events, player, villains[0], game_objects, scooby_snacks)
        self.interface = Interface(self.screen, self.current_phase, [])
        
        self.current_dialogue = 0
        self.dialogues = phase_data['dialogs']
    
    @property
    def phase_counter(self):
        """
        Retorna o contador da fase atual.

        Retorno:
            int: O contador da fase.
        """
        return self._phase_counter
    
    @phase_counter.setter
    def phase_counter(self, new_phase_counter):
        """
        Define o contador da fase atual.

        Parâmetros:
            new_phase_counter (int): O novo contador de fase.
        """
        self._phase_counter = new_phase_counter
    
    @property
    def current_phase(self):
        """
        Retorna a fase atual.

        Retorno:
            Phase: A fase atual do jogo.
        """
        return self._current_phase
    
    @current_phase.setter
    def current_phase(self, new_phase):
        """
        Define a fase atual.

        Parâmetros:
            new_phase (Phase): A nova fase a ser definida como a fase atual.
        """
        self._current_phase = new_phase
        
    def update(self, movement, attack):
        """
        Atualiza a fase atual e a interface, além de verificar se a fase terminou ou se houve falha.

        Parâmetros:
            movement (tuple): O movimento do jogador.
            attack (tuple): A direção do ataque do jogador.
        """
        if not self.current_phase.check_lost():
            self.current_phase.update(movement, attack) 
        
        # Verifica a passagem de fase
        if self.current_phase.check_end():
            self.phase_counter += 1
            self.start_phase()
         
        # Atualiza a interface
        self.interface.update()

    def quit_phase(self):
        """
        Encerra a fase atual e para a música de fundo.

        A fase atual é definida como None e a música de fundo é interrompida.
        """
        self.current_phase.background.stop_music()
        self.current_phase = None
