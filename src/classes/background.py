import pygame as pg
from src.settings import SCREEN_DIMENSIONS, Fonts, FULL_HEART, HALF_HEART, EMPTY_HEART
from src.settings import SHAGGY_PROFILE, DAPHNE_PROFILE, SCOOBY_PROFILE, VELMA_PROFILE, FRED_PROFILE
import numpy as np


class Background(pg.sprite.Sprite):
    """
    Represents a scrolling background in the game, including its position, dimensions, and music control.

    Parameters
    ----------
    screen : pygame.Surface
        The game screen where the background is rendered.
    sprite : str
        Path to the image file used as the background sprite.
    x_position : int
        Initial x-coordinate of the background.
    y_position : int
        Initial y-coordinate of the background.
    width : int
        Width of the background image.
    height : int
        Height of the background image.
    music : str
        Path to the music file played for this background.
    volume : float
        Volume level for the background music (0.0 to 1.0).
    sounds : list
        List of sound effects associated with the background.

    Attributes
    ----------
    screen : pygame.Surface
        The game screen for rendering.
    sprite : pygame.Surface
        The scaled image surface of the background.
    x_position : int
        Current x-coordinate of the background's top-left corner.
    y_position : int
        Current y-coordinate of the background's top-left corner.
    width : int
        Width of the background.
    height : int
        Height of the background.
    music : str
        Path to the background music file.
    volume : float
        Volume of the background music.
    sounds : list
        Sound effects linked to the background.
    image : pygame.Surface
        The subsurface of the sprite displayed as the visible area.
    rect : pygame.Rect
        The rectangle defining the position and dimensions of the visible background.
    x_limit_sup : int
        Maximum x-coordinate for scrolling.
    y_limit_sup : int
        Maximum y-coordinate for scrolling.

    Methods
    -------
    get_origin():
        Returns the coordinates of the background's origin.
    get_shape():
        Returns the dimensions of the background.
    get_position():
        Returns the current top-left position of the background.
    set_position(x_new, y_new):
        Updates the top-left position of the background.
    center(x_player, y_player):
        Centers the camera on the player's position.
    play_music():
        Starts playing the background music.
    stop_music():
        Stops the background music.
    set_volume(volume):
        Sets the volume level of the background music.
    draw_background_image():
        Draws the current view of the background onto the screen.
    update(x_player, y_player):
        Updates the background's position and renders it on the screen.
    """

    def __init__(self, screen, sprite, x_position, y_position, width, height, music, volume, sounds):
        """
        Inicializa a classe que gerencia o background e os recursos do jogo, como sprite, música e sons.

        Parâmetros
        ----------
        screen : pygame.Surface
            A superfície da tela onde o jogo será renderizado.

        sprite : str
            O caminho para o arquivo de imagem que será usado como o sprite da câmera.

        x_position : int
            A posição inicial da câmera no eixo x.

        y_position : int
            A posição inicial da câmera no eixo y.

        width : int
            A largura da câmera.

        height : int
            A altura da câmera.

        music : str
            O caminho para o arquivo de música que será reproduzido no fundo.

        volume : float
            O volume da música, variando de 0.0 (silencioso) a 1.0 (volume máximo).

        sounds : list
            Lista de sons que serão usados no jogo (não utilizado diretamente no construtor, mas armazenado).

        Exceções
        ---------
        pg.error
            Levantada caso ocorra um erro ao carregar a imagem ou a música.

        ValueError
            Levantada se houver erro ao criar a subsuperfície da imagem.

        Atributos
        ---------
        screen : pygame.Surface
            A superfície da tela onde a câmera será renderizada.

        sprite : pygame.Surface
            A imagem do sprite redimensionada ou um placeholder caso o carregamento falhe.

        position_controller : PositionController
            O controlador de posição que gerencia os limites de movimentação da câmera.

        x_position : int
            A posição ajustada da câmera no eixo x, levando em consideração as dimensões da tela.

        y_position : int
            A posição ajustada da câmera no eixo y, levando em consideração as dimensões da tela.

        width : int
            A largura da câmera.

        height : int
            A altura da câmera.

        music : str
            O caminho para o arquivo de música que será tocado.

        volume : float
            O volume da música.

        sounds : list
            Lista de sons que podem ser usados no jogo.

        image : pygame.Surface
            A imagem que será usada para renderizar a visão da câmera (subsuperfície).

        rect : pygame.Rect
            O retângulo delimitador da imagem da câmera, usado para colisões e posicionamento.

        x_limit_sup : int
            O limite superior de movimentação da câmera no eixo x.

        y_limit_sup : int
            O limite superior de movimentação da câmera no eixo y.
        """

        super().__init__()
        self.screen = screen
        
        # Tratamento de exceção no carregamento da imagem
        try:
            self.sprite = pg.image.load(sprite)
            self.sprite = pg.transform.scale(self.sprite, (width, height))
        except pg.error as e:
            print(f"Erro ao carregar a imagem: {sprite}. Detalhes: {e}")
            self.sprite = pg.Surface((width, height))  # Usar um "placeholder" se falhar

    
        self.position_controller = PositionController([width, height], SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1])
        self.x_position = x_position - SCREEN_DIMENSIONS[0]//2
        self.y_position = y_position - SCREEN_DIMENSIONS[1]//2
        self.width = width
        self.height = height
        self.music = music
        self.volume = volume
        self.sounds = sounds
        
        try:
            pg.mixer.music.load(self.music)
            pg.mixer.music.set_volume(self.volume)
        except pg.error as e:
            print(f"Erro ao carregar a música: {self.music}. Detalhes: {e}")
        
        
        try:
            self.image = self.sprite.subsurface((self.x_position, self.y_position, *SCREEN_DIMENSIONS))
        except ValueError as e:
            print(f"Erro ao criar subsurface da imagem. Detalhes: {e}")
            self.image = pg.Surface(SCREEN_DIMENSIONS)  # Usar uma superfície em branco
    
        self.rect = self.image.get_rect()

        # Limites, ate aonde a camera vai
        self.x_limit_sup = self.width - SCREEN_DIMENSIONS[0]
        self.y_limit_sup = self.height - SCREEN_DIMENSIONS[1]
        
    def get_origin(self):
        """
        Returns the current top-left coordinates of the background's visible area.

        Returns
        -------
        tuple
            A tuple (x, y) representing the coordinates of the background's origin.
        """
        return self.x_position+SCREEN_DIMENSIONS[0], self.y_position+SCREEN_DIMENSIONS[1]  
    
    def get_shape(self):
        """
        Returns the current dimensions (width, height) of the background.

        Returns
        -------
        tuple
            A tuple (width, height) representing the dimensions of the background.
        """
        return self.width, self.height
    
    def get_position(self):
        """
        Returns the current top-left position of the background.

        Returns
        -------
        tuple
            A tuple (x_position, y_position) representing the position of the background.
        """        
        return self.x_position, self.y_position
        
    def set_position(self, x_new, y_new):
        """
        Updates the position of the background by setting new top-left coordinates.

        Parameters
        ----------
        x_new : int
            The new x-coordinate for the background's position.
        y_new : int
            The new y-coordinate for the background's position.
        """
        self.x_position = x_new
        self.y_position = y_new
        
    def center(self, x_player, y_player):
        """
        Centers the background on the player's position by adjusting the background's view.

        Parameters
        ----------
        x_player : int
            The x-coordinate of the player.
        y_player : int
            The y-coordinate of the player.
        """
        try:
            x_new, y_new = self.position_controller.to_frame(x_player, y_player)
            x_new -= SCREEN_DIMENSIONS[0] // 2
            y_new -= SCREEN_DIMENSIONS[1] // 2
            self.set_position(x_new, y_new)
            self.image = self.sprite.subsurface((*self.get_position(), *SCREEN_DIMENSIONS))
        except Exception as e:
            print(f"Erro ao centralizar a câmera: {e}")
            
    def play_music(self):
        """
        Starts playing the background music in a loop.
        """
        pg.mixer.music.play(-1)
    
    def stop_music(self):
        """
        Stops the background music.
        """
        pg.mixer.music.stop()
        
    def set_volume(self, volume):
        """
        Sets the volume level for the background music.

        Parameters
        ----------
        volume : float
            The volume level, ranging from 0.0 (silent) to 1.0 (maximum volume).
        """
        self.volume = volume
        pg.mixer.music.set_volume(self.volume)
    
    def draw_background_image(self):
        """
        Draws the current view of the background onto the screen.

        This method blits the background image onto the game screen.
        """
        self.screen.blit(self.image, self.rect)
    
    def update(self, x_player, y_player):
        """
        Updates the background's position and renders it on the screen, keeping the player centered.

        Parameters
        ----------
        x_player : int
            The x-coordinate of the player.
        y_player : int
            The y-coordinate of the player.
        """
        self.center(x_player, y_player)
        self.position_controller.set_origin(*self.get_position())
        self.draw_background_image()
        

class Interface():
    """
    Representa a interface gráfica do jogo, incluindo elementos como o nome do jogador, vida, imagem de perfil e outros avisos.

    Parameters
    ----------
    screen : pygame.Surface
        A superfície onde a interface será desenhada.
    phase_atual : object
        A fase atual do jogo, contendo informações sobre o jogador e o estado do jogo.
    interface_elements : dict
        Dicionário contendo os elementos gráficos e fontes usados na interface.

    Attributes
    ----------
    screen : pygame.Surface
        A superfície onde a interface será renderizada.
    phase_atual : object
        A fase atual do jogo.
    interface_elements : dict
        Dicionário de elementos gráficos da interface.
    player_name : pygame.Surface
        Superfície contendo o nome do jogador renderizado.
    event_warning : pygame.Surface
        Superfície contendo o aviso "Volte para a Zona!".
    player_name_location : tuple
        Coordenadas para a posição do nome do jogador.
    event_warning_location : tuple
        Coordenadas para a posição do aviso de evento.
    event_time_location : tuple
        Coordenadas para a posição do tempo do evento.
    full_heart_image : pygame.Surface
        Imagem do coração cheio (vida plena).
    empty_heart_image : pygame.Surface
        Imagem do coração vazio (sem vida).
    half_heart_image : pygame.Surface
        Imagem do coração meio cheio (meia vida).
    heart_location : tuple
        Coordenadas para a posição dos corações (vidas) do jogador.
    shaggy_profile : str
        Caminho para a imagem de perfil do personagem Shaggy.
    dapnhe_profile : str
        Caminho para a imagem de perfil do personagem Daphne.
    velma_profile : str
        Caminho para a imagem de perfil do personagem Velma.
    scooby_profile : str
        Caminho para a imagem de perfil do personagem Scooby.
    fred_profile : str
        Caminho para a imagem de perfil do personagem Fred.

    Methods
    -------
    set_phase_atual(new_phase)
        Atualiza a fase atual do jogo com uma nova fase.
    draw_interface()
        Desenha os elementos gráficos da interface no jogo.
    update()
        Atualiza a interface, renderizando a vida do jogador e outros elementos gráficos.
    """    
    def __init__(self, screen, phase_atual, interface_elements):
        """
        Inicializa a interface gráfica do jogo, incluindo a configuração dos elementos e imagens.

        Parameters
        ----------
        screen : pygame.Surface
            A superfície onde a interface será desenhada.
        phase_atual : object
            A fase atual do jogo, que contém informações do jogador e o estado da fase.
        interface_elements : dict
            Dicionário contendo os elementos gráficos e fontes usadas na interface.

        Exceptions
        ----------
        AttributeError
            Se houver um erro ao acessar o nome do jogador.
        pg.error
            Se houver um erro ao carregar as imagens de coração ou perfil.
        KeyError
            Se houver um erro ao carregar a imagem de perfil do jogador.
        """
        self.screen = screen
        self.phase_atual = phase_atual
        self.interface_elements = interface_elements
        
        # Tratamento de exceção na criação do nome do player
        try:
            self.player_name = Fonts.PLAYER_NAME.value.render('Player :' + str(self.phase_atual.player.name), True, (123, 173, 123))
        except AttributeError as e:
            print(f"Erro ao acessar o nome do player: {e}")
            self.player_name = Fonts.PLAYER_NAME.value.render('Player :Unknown', True, (123, 173, 123))
        
        self.event_warning =  Fonts.EVENT_WARNING.value.render('Volte para a Zona!', True, (255, 255, 255))
        
        #  Localizações
        self.player_name_location = (50, 50)
        # self.player_life_location = (300, 50)
        self.event_warning_location = ((SCREEN_DIMENSIONS[0]*2)//5, 100)
        self.event_time_location = (SCREEN_DIMENSIONS[0]//2-50, 50)
        
        # Sprite de Vida do Personagem  
        try:
            self.full_heart_image = pg.image.load(FULL_HEART)
            self.full_heart_image = pg.transform.scale(self.full_heart_image, (50, 50)) 
            self.empty_heart_image = pg.image.load(EMPTY_HEART)
            self.empty_heart_image = pg.transform.scale(self.empty_heart_image, (50, 50)) 
            self.half_heart_image = pg.image.load(HALF_HEART)
            self.half_heart_image = pg.transform.scale(self.half_heart_image, (50, 50))
        except pg.error as e:
            print(f"Erro ao carregar as imagens de coração: {e}")
            self.full_heart_image = pg.Surface((50, 50))
            self.empty_heart_image = pg.Surface((50, 50))
            self.half_heart_image = pg.Surface((50, 50))
            
        self.heart_location = (115, 45)  # Local inicial para os corações

        # Sprite de Foto de Perfil do personagem
        self.shaggy_profile = SHAGGY_PROFILE
        self.dapnhe_proflle = DAPHNE_PROFILE
        self.velma_profile = VELMA_PROFILE
        self.scooby_profile = SCOOBY_PROFILE
        self.fred_profile = FRED_PROFILE
        
        
    def set_phase_atual(self, new_phase):
        """
        Atualiza a fase atual do jogo com uma nova fase.

        Parameters
        ----------
        new_phase : object
            A nova fase que será definida como a fase atual do jogo.
        """
        self.phase_atual = new_phase
        
    def draw_interface(self):
        """
        Desenha os elementos gráficos da interface no jogo, incluindo o nome do jogador, imagem de perfil, vida e outros avisos.

        Este método renderiza o nome do jogador, o número de corações representando a vida, a imagem do perfil 
        e o aviso de evento caso esteja ocorrendo.
        """
        try:
                
            if self.phase_atual.player.name == "Scooby":
                player_image = pg.image.load(self.scooby_profile)  # Carrega a imagem de perfil do Scooby
            
                # Desenha a imagem no canto superior esquerdo (10, 10)
            elif self.phase_atual.player.name =="Velma":
                player_image = pg.image.load(self.velma_profile)  # Carrega a imagem de perfil do Scooby
            
            elif self.phase_atual.player.name == "Daphne":
                player_image = pg.image.load(self.dapnhe_proflle)
            
            elif self.phase_atual.player.name == "Fred":
                player_image = pg.image.load(self.fred_profile)
            
            elif self.phase_atual.player.name == "Shaggy":
                player_image = pg.image.load(self.shaggy_profile)
            
            if player_image:
                player_image = pg.transform.sczale(player_image, (100, 100))  # Redimensiona para caber na interface
                self.screen.blit(player_image, (10, 10))            
        
        except KeyError as e:
                print(f"Erro ao carregar a imagem de perfil do personagem: {e}")
        
        # Desenha a quantidade de vidas como corações
        for num in range(1, 6):
            x = self.heart_location[0] + (num-1) * 60  # Espaçamento entre corações
            y = self.heart_location[1]
            if num <=self.phase_atual.player.life:
                self.screen.blit(self.full_heart_image, (x, y))
            elif num-1 < self.phase_atual.player.life  and self.phase_atual.player.life < num:
                self.screen.blit(self.half_heart_image, (x,y))
            elif num >self.phase_atual.player.life:
                self.screen.blit(self.empty_heart_image, (x,y))      
        

        
        # Desenha avisos e informacoes da phase no centro superior da tela
        # if self.phase_atual.current_mandatory_event:
        #     if self.phase_atual.current_mandatory_event.in_execution:
        #         if self.phase_atual.current_mandatory_event.out_zone:
        #             self.screen.blit(self.event_warning, self.event_warning_location)
                # self.event_time = self.phase_atual.current_mandatory_event.time
                # self.event_time = Fonts.EVENT_TIME.value.render('Time: '+str(self.event_time), True, (123, 173, 223))
                # self.screen.blit(self.event_time, self.event_time_location)
        
        # Desenha o minimapa e as configuracoes no canto superior direito
        
    def update(self):
        """
        Atualiza a interface, renderizando a vida do jogador e outros elementos gráficos.

        Este método é chamado para atualizar a interface, desenhando informações atualizadas como a vida do jogador.
        """
        try:
            self.player_life = Fonts.PLAYER_LIFE.value.render('Life: '+str(int(self.phase_atual.player.life)), True, (123, 173, 223))
            self.draw_interface()
        except Exception as e:
            print(f"Erro ao atualizar a interface: {e}")
    
class PositionController:
    """
    Controla o posicionamento de objetos dentro de um mapa, garantindo que esses objetos não ultrapassem os limites do mapa e realizando operações de normalização e tradução.

    Parameters
    ----------
    map_limits_sup : list
        Limites superiores do mapa, fornecidos como uma lista com dois valores [x, y].
    width : float
        Largura da área de visualização.
    height : float
        Altura da área de visualização.

    Attributes
    ----------
    x_origin : int
        Coordenada X da origem do sistema de coordenadas.
    y_origin : int
        Coordenada Y da origem do sistema de coordenadas.
    map_limits_inf : list
        Limites inferiores do mapa, calculados a partir da largura e altura fornecidas.
    map_limits_sup : list
        Limites superiores do mapa, ajustados pela largura e altura da área de visualização.
    map : pygame.Rect
        Retângulo representando o mapa, com limites calculados com base nas informações fornecidas.
    """
    x_origin = 0
    y_origin = 0
    
    def __init__(self, map_limits_sup, width, height):
        """
        Inicializa o controlador de posição com os limites do mapa e a área de visualização.

        Parameters
        ----------
        map_limits_sup : list
            Limites superiores do mapa, fornecidos como uma lista com dois valores [x, y].
        width : float
            Largura da área de visualização.
        height : float
            Altura da área de visualização.
        """
        self.map_limits_inf = [width/2, height/2]
        self.map_limits_sup = map_limits_sup.copy()
        self.map_limits_sup[0] -= width/2
        self.map_limits_sup[1] -= height/2
        self.map = pg.Rect(*self.map_limits_inf, *self.map_limits_sup)
        
    @classmethod
    def set_origin(cls, x_new, y_new):
        """
        Define a origem do sistema de coordenadas do mapa.

        Parameters
        ----------
        x_new : int
            A nova coordenada X da origem.
        y_new : int
            A nova coordenada Y da origem.
        """
        cls.x_origin = x_new
        cls.y_origin = y_new  

    @staticmethod
    def normalize_movement(movement, speed):
        """
        Normaliza o movimento, ajustando a direção e aplicando a velocidade.

        Parameters
        ----------
        movement : list or np.array
            Movimento desejado, fornecido como uma lista ou array com as coordenadas [x, y].
        speed : float
            A velocidade do movimento.

        Returns
        -------
        np.array
            O movimento normalizado multiplicado pela velocidade.
        """
        movement = np.array(movement, dtype=float) 
        norma = np.linalg.norm(movement)
        
        if norma:
            movement /= norma
        movement *= speed
        return movement
    
    def to_frame(self, x_position, y_position):
        """
        Ajusta a posição de um objeto para que ele não ultrapasse os limites do mapa.

        Parameters
        ----------
        x_position : float
            A posição X do objeto.
        y_position : float
            A posição Y do objeto.

        Returns
        -------
        tuple
            As novas coordenadas ajustadas (x_position, y_position).
        """
        if x_position < self.map_limits_inf[0]:
            x_position = self.map_limits_inf[0]
        elif x_position > self.map_limits_sup[0]:
            x_position = self.map_limits_sup[0]
            
        if y_position < self.map_limits_inf[1]:
            y_position = self.map_limits_inf[1]
        if y_position > self.map_limits_sup[1]:
            y_position = self.map_limits_sup[1]
        
        return x_position, y_position
    
    def out_game(self, object):
        """
        Verifica se um objeto está fora dos limites do mapa e, caso esteja, o remove do jogo.

        Parameters
        ----------
        object : pygame.sprite.Sprite
            O objeto que será verificado.

        Notes
        -----
        Este método usa o método `kill()` do objeto para removê-lo do jogo se ele estiver fora dos limites do mapa.
        """
        if not self.map.contains(object.rect):
            object.kill()
    
    def apply_translation(self, x_position, y_position):
        """
        Aplica uma tradução no plano, considerando a origem do sistema de coordenadas.

        Parameters
        ----------
        x_position : float
            A posição X do objeto.
        y_position : float
            A posição Y do objeto.

        Returns
        -------
        tuple
            As novas coordenadas (x_position, y_position) após a tradução.
        """
        x_new = x_position - self.x_origin
        y_new = y_position - self.y_origin
        return x_new, y_new
    

class CollideController:
    """
    Controla as colisões entre diversos elementos da fase, processando interações entre o protagonista, NPCs, vilões, objetos do jogo, munições, eventos e coletáveis.

    Methods
    -------
    locate_collide(sprite_1, sprite_2)
        Identifica a posição relativa de duas sprites (sprite_1 e sprite_2) em relação a um eixo, verificando se há colisão.
    __init__(player, npcs, villains, game_objects, collectibles, ammus, mandatory_events, optional_events, scooby_snacks, weapons, phase_elements)
        Inicializa o controlador de colisões com todos os elementos da fase.
    player_collide_with()
        Processa as colisões do protagonista (player) com os elementos da fase, como NPCs, coletáveis e eventos.
    ammus_collide_with()
        Processa as colisões das munições com os personagens e objetos do jogo.
    game_objects_collide_with()
        Processa as colisões entre personagens e objetos do jogo, empurrando ou interagindo conforme necessário.
    monsters_collide_with()
        Processa as colisões entre vilões e personagens, além de disparar munições quando apropriado.
    npcs_collide_with()
        Processa as colisões entre NPCs, empurrando-os uns aos outros quando necessário.
    update(phase_elements)
        Atualiza o estado dos elementos da fase, processando todas as colisões e ações associadas.
    """
    @staticmethod
    def locate_collide(sprite_1: pg.sprite.Sprite, sprite_2: pg.sprite.Sprite) -> np.array:
        """
        Identifica a posição relativa da `sprite_2` em relação à `sprite_1`, verificando se elas colidem.

        Parameters
        ----------
        sprite_1 : pg.sprite.Sprite
            A sprite de interesse, geralmente o personagem.
        sprite_2 : pg.sprite.Sprite
            A sprite tomada como referencial para a colisão.

        Returns
        -------
        np.array
            Um array com valores 0 ou 1, dependendo da direção da colisão nos eixos (X, Y).
        """
        # Toma os centros das sprites
        center_1 = np.array([sprite_1.x_position, sprite_1.y_position])
        center_2 = np.array([sprite_2.x_position, sprite_2.y_position])
        distance = center_2 - center_1
        abs_distance = np.absolute(distance)
        abs_movement = np.absolute(sprite_1.movement)
        min_distance = np.array([sprite_1.width+sprite_2.width, sprite_1.height+sprite_2.height])/2
        print(f'D: {distance}, Abs: {abs_distance}\nMin: {min_distance} - Abs_movement: {abs_movement}')
        
        min_distance -= abs_distance
        
        # Avalia se eles colidem nos eixos
        # collide = abs_distance - min_distance
        # print(f'C: {collide}')
        # collide = collide < 0
        # print(f'C pos: {collide}\n\n')
        
        # Angulo entre os vetores define em qual eixo foi a colisao
        e1 = np.array([1, 0])
        cos_movement = np.dot(e1, abs_movement)/np.linalg.norm(abs_movement)
        cos_min_distance = np.dot(e1, min_distance)/np.linalg.norm(min_distance)
        print(f'Cos_mov: {cos_movement}, cos_min: {cos_min_distance}')
        
        # Retira parte do movimento que causou a colisao
        collide_x_axis  = cos_movement > cos_min_distance
        abs_distance[abs_distance == 0] = 1 # Nao divir zero por zero, por favor
        signal = distance/abs_distance
        comeback = min_distance*np.array([collide_x_axis, not collide_x_axis])*signal
        return -comeback
            
    def __init__(self, player, npcs, villains, game_objects, collectibles, ammus, mandatory_events, optional_events, scooby_snacks, weapons, phase_elements):
        """
        Inicializa o controlador de colisões com os elementos da fase, definindo os grupos de sprites e acessibilidade.

        Parameters
        ----------
        player : Protagonist
            O protagonista da fase, geralmente o personagem controlado pelo jogador.
        npcs : pg.sprite.Group
            Grupo de sprites dos NPCs da fase.
        villains : pg.sprite.Group
            Grupo de sprites dos vilões da fase.
        game_objects : pg.sprite.Group
            Grupo de sprites de objetos do jogo.
        collectibles : pg.sprite.Group
            Grupo de sprites de itens colecionáveis.
        ammus : pg.sprite.Group
            Grupo de sprites de munições disparadas.
        mandatory_events : pg.sprite.Group
            Grupo de eventos obrigatórios que o jogador deve completar.
        optional_events : pg.sprite.Group
            Grupo de eventos opcionais que podem ser acionados durante a fase.
        scooby_snacks : Collectible
            O item especial "Scooby Snacks" coletável na fase.
        weapons : pg.sprite.Group
            Grupo de sprites de armas disponíveis na fase.
        phase_elements : pg.sprite.Group
            Grupo de todos os elementos da fase que são monitorados para colisões.
        """
        
        self.player = player
        self.npcs = npcs
        self.villains = villains
        self.game_objects = game_objects
        self.collectibles = collectibles
        self.ammus = ammus
        self.mandatory_events = mandatory_events
        self.current_mandatory_event = next(iter(self.mandatory_events), None)
        self.optional_events = optional_events
        self.scooby_snacks = scooby_snacks
        self.weapons = weapons
        self.phase_elements = phase_elements
        self.characters = pg.sprite.Group(self.villains)
        self.characters.add(self.npcs)
        self.characters.add(self.player)
        
        self.accessible_elements = pg.sprite.Group()
        for each_monster in self.villains.sprites():
            self.accessible_elements.add(each_monster.weapon)

        self.accessible_elements.add(self.villains)
        self.accessible_elements.add(self.npcs)
        self.accessible_elements.add(self.game_objects)
        self.accessible_elements.add(self.collectibles)
        self.accessible_elements.add(self.current_mandatory_event)
        self.accessible_elements.add(self.optional_events)
        
    def player_collide_with(self):
        """
        Processa as colisões do protagonista (player) com os elementos da fase, como NPCs, coletáveis e eventos.

        Atualiza o evento obrigatório atual, executa ações relacionadas a coletáveis e interage com NPCs.
        """
        if self.current_mandatory_event.started:
            if not self.current_mandatory_event.in_execution:
                self.current_mandatory_event.kill()
                self.current_mandatory_event = next(iter(self.mandatory_events), None)
                if self.current_mandatory_event:
                    self.accessible_elements.add(self.current_mandatory_event)
        if len(self.mandatory_events.sprites()) == 1:
            self.scooby_snacks.visible = True
            self.accessible_elements.add(self.scooby_snacks)
            
        # Atualizacao dos eventos opcionais
        for optional_event in self.optional_events.sprites():
            if optional_event.started and not optional_event.in_execution:
                optional_event.kill()
        
        # Colisao com coletaveis
        to_collectible = pg.sprite.spritecollide(self.player, self.collectibles, False)
        for each_collectible in to_collectible:
            if each_collectible.visible:
                # Adiciona ao inventario
                
                # Remove todas as referencias
                each_collectible.kill()
            
        # Colisao com npcs
        npcs_to_push = pg.sprite.spritecollide(self.player, self.npcs, False)
        for each_npc in npcs_to_push:
            comeback = -self.locate_collide(self.player, each_npc)
            comeback = each_npc.apply_movement(comeback)
            if comeback.any():
                self.player.apply_movement(comeback, False)
    
    def ammus_collide_with(self):
        """
        Processa as colisões das munições com personagens e objetos do jogo.

        Colide com personagens e objetos, aplicando dano aos personagens ou destruindo munições e objetos.
        """
        character_hit_by_ammu = pg.sprite.groupcollide(self.ammus, self.characters, False, False)
        for ammu  in self.ammus.sprites():
            for each_ammu in character_hit_by_ammu.keys():
                for each_character in character_hit_by_ammu[each_ammu]:
                    # Atinge o personagem
                    print('Dano longo\n')
                    each_character.life -= each_ammu.damage
                    # Remove todas as referencias
                    each_ammu.kill()

        # Colisao com objetos
        destroyed_ammus = pg.sprite.groupcollide(self.ammus, self.game_objects, False, False).keys()
        for each_ammu in destroyed_ammus:
            each_ammu.kill()
        
    

    def game_objects_collide_with(self):
        """
        Processa as colisões entre personagens e objetos do jogo.

        Empurra objetos ou interage com eles conforme a natureza da colisão.
        """
        object_pushed_by_character = pg.sprite.groupcollide(self.characters, self.game_objects, False, False)
        for each_character in object_pushed_by_character.keys():
            for each_object in object_pushed_by_character[each_character]:
                if each_object.is_static:
                    comeback = self.locate_collide(each_character, each_object)
                    comeback = each_character.apply_movement(comeback, False)
                    if comeback.any():
                        _ = each_object.apply_movement(comeback)
                    
                else:
                    comeback = each_object.apply_movement(each_character.movement)
                    if comeback.any():
                        _ = each_character.apply_movement(comeback, False)

    
    def monsters_collide_with(self):
        """
        Processa as colisões entre vilões e personagens, além de disparar munições quando apropriado.

        Colide com personagens, atira em direção ao protagonista e gerencia disparos.
        """
        fired = []
        # Colisao com algum personagem
        characters_to_push = pg.sprite.groupcollide(self.villains, self.characters, False, False)
        for each_villain in characters_to_push.keys():
            for each_character in characters_to_push[each_villain]:
                # Nao se empurra
                if each_villain != each_character and each_villain.movement.any():
                    comeback = -self.locate_collide(each_villain, each_character)
                    comeback = each_character.apply_movement(comeback)
                    if comeback.any():
                        _ = each_villain.apply_movement(comeback, False)
        
        # Atira no personagem caso ele esteja na mira e tenha recarregado
        for each_villain in self.villains.sprites():
            if each_villain.aim.any():
                if self.player.rect.clipline(each_villain.weapon.rect.center, np.array(each_villain.weapon.rect.center) + each_villain.aim*each_villain.weapon.scope/np.linalg.norm(each_villain.aim)) and each_villain.weapon.check_load():
                    print('pow')
                    bullet = each_villain.weapon.fire(each_villain.aim)
                    fired.append(bullet)
                    
        self.accessible_elements.add(fired)
        self.ammus.add(fired)
        
        return fired
    
    def npcs_collide_with(self):
        """
        Processa as colisões entre NPCs, empurrando-os uns aos outros quando necessário.

        Garante que NPCs não se empurrem repetidamente e trata colisões.
        """
        npcs_pushed_by_npcs = pg.sprite.groupcollide(self.npcs, self.npcs, False, False)
        for each_npc1 in npcs_pushed_by_npcs.keys():
            for each_npc2 in npcs_pushed_by_npcs[each_npc1]:
                # Nao se empurram
                if each_npc1 != each_npc2 and each_npc1.movement.any():
                    # Separa o npc2 do npc1
                    comeback = -self.locate_collide(each_npc1, each_npc2)
                    comeback = each_npc2.apply_movement(comeback)
                    if comeback.any():
                        _ = each_npc1.apply_movement(comeback)
                        
                    # Nao precisa tratar a mesma colisao depois
                    npcs_pushed_by_npcs[each_npc2].remove(each_npc1)
    
    
    def update(self, phase_elements):
        """
        Atualiza o estado da fase, processando todas as colisões e interações entre os elementos da fase.

        Parameters
        ----------
        phase_elements : pg.sprite.Group
            O grupo de todos os elementos da fase que serão atualizados e verificados para colisões.
        """
        fired = []
        self.player_collide_with()
        self.ammus_collide_with()
        self.game_objects_collide_with()
        fired_by_villains = self.monsters_collide_with()
        self.npcs_collide_with()
        fired.extend(fired_by_villains)
        
        if fired:
            phase_elements.add(fired)
        
        """
        Colisoes:
        player - monstro (atacado)
        player - coletavel (coleta)
        player - game object (empurra)
        player - npcs (para)
        player - event (inicia)
        player - ammu (destroi ou recocheteia)
        
        monstro - player
        monstro - ammu (destroi ou recocheteia)
        monstro - game object (empurra)
        
        npc - player ou game object (empurra)
        """