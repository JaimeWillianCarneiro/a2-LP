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
        return self.x_position+SCREEN_DIMENSIONS[0], self.y_position+SCREEN_DIMENSIONS[1]  
    
    def get_shape(self):
        return self.width, self.height
    
    def get_position(self):
        return self.x_position, self.y_position
        
    def set_position(self, x_new, y_new):
        self.x_position = x_new
        self.y_position = y_new
        
    def center(self, x_player, y_player):
       # Centraliza a câmera no personagem
        try:
            x_new, y_new = self.position_controller.to_frame(x_player, y_player)
            x_new -= SCREEN_DIMENSIONS[0] // 2
            y_new -= SCREEN_DIMENSIONS[1] // 2
            self.set_position(x_new, y_new)
            self.image = self.sprite.subsurface((*self.get_position(), *SCREEN_DIMENSIONS))
        except Exception as e:
            print(f"Erro ao centralizar a câmera: {e}")
            
    def play_music(self):
        pg.mixer.music.play(-1)
    
    def stop_music(self):
        pg.mixer.music.stop()
        
    def set_volume(self, volume):
        self.volume = volume
        pg.mixer.music.set_volume(self.volume)
    
    def draw_background_image(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self, x_player, y_player):
        self.center(x_player, y_player)
        self.position_controller.set_origin(*self.get_position())
        self.draw_background_image()
        

class Interface():
    
    def __init__(self, screen, phase_atual, interface_elements):
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
        self.phase_atual = new_phase
        
    def draw_interface(self):
        # Desenha os atributos do player no canto superior esquerdo
        # self.screen.blit(self.player_name, self.player_name_location)
        # self.screen.blit(self.player_life, self.player_life_location)
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
        if self.phase_atual.collide_controller.current_mandatory_event:
            if self.phase_atual.collide_controller.current_mandatory_event.in_execution:
                if self.phase_atual.collide_controller.current_mandatory_event.out_zone:
                    self.screen.blit(self.event_warning, self.event_warning_location)
                # self.event_time = self.phase_atual.current_mandatory_event.time
                # self.event_time = Fonts.EVENT_TIME.value.render('Time: '+str(self.event_time), True, (123, 173, 223))
                # self.screen.blit(self.event_time, self.event_time_location)
        
        # Desenha o minimapa e as configuracoes no canto superior direito
        
    def update(self):
        try:
            self.player_life = Fonts.PLAYER_LIFE.value.render('Life: '+str(int(self.phase_atual.player.life)), True, (123, 173, 223))
            self.draw_interface()
        except Exception as e:
            print(f"Erro ao atualizar a interface: {e}")
    
class PositionController:
    x_origin = 0
    y_origin = 0
    def __init__(self, map_limits_sup, width, height):
        self.map_limits_inf = [width/2, height/2]
        self.map_limits_sup = map_limits_sup.copy()
        self.map_limits_sup[0] -= width/2
        self.map_limits_sup[1] -= height/2
        self.map = pg.Rect(*self.map_limits_inf, *self.map_limits_sup)
        
    @classmethod
    def set_origin(cls, x_new, y_new):
        cls.x_origin = x_new
        cls.y_origin = y_new  

    @staticmethod
    def normalize_movement(movement, speed):
        movement = np.array(movement, dtype=float) 
        norma = np.linalg.norm(movement)
        
        if norma:
            movement /= norma
        movement *= speed
        return movement
    
    def to_frame(self, x_position, y_position):
        # Enquadra objeto para que ele nao ultrapasse nenhum limite do mapa
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
        if not self.map.contains(object.rect):
            object.kill()
    
    def apply_translation(self, x_position, y_position):
        # Aplica uma translacao no plano, considerando o sistema de coordenadas na qual o jogo sera desenhado
        x_new = x_position - self.x_origin
        y_new = y_position - self.y_origin
        return x_new, y_new
    
    
class CollideController:
    @staticmethod
    def locate_collide(sprite_1: pg.sprite.Sprite, sprite_2: pg.sprite.Sprite) -> np.array:
        """ Identifica a posicao relativa da sprite_2 em relacao a sprite 1.

        Args:
            sprite_1 (pg.sprite.Sprite): Sprite de interesse.
            sprite_2 (pg.sprite.Sprite): Sprite tomada como referencial.

        Returns:
            np.array: Array de entradas 0 caso esteja no sentido negativo do eixo, 1 caso positivo
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
        signal = distance/abs_distance
        comeback = min_distance*np.array([collide_x_axis, not collide_x_axis])*signal
        return comeback
            
    def __init__(self, player, npcs, villains, game_objects, collectibles, ammus, mandatory_events, optional_events, scooby_snacks, weapons):
        """ Classe que gerencia as colisoes entre os elementos da fase, atualizando os estados dos elementos que colidiram entre si.

        Args:
            player (Protagonist): Protagonista da fase.
            npcs (pg.sprite.Group): NPC's da fase.
            villains (pg.sprite.Group): Monstros da fase.
            game_objects (pg.sprite.Group): Objetos da fase.
            collectibles (pg.sprite.Group): Coletaveis da fase.
            ammus (pg.sprite.Group): Municoes disparadas na fase.
            mandatory_events (pg.sprite.Group): Eventos obrigatorios da fase.
            optional_events (pg.sprite.Group): Eventos opcionais da fase.
            scooby_snacks (Collectible): Caixa de biscoitos scooby da fase.
            weapons (pg.sprite.Group): Armas usadas na fase.
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
        """ Processa as colisoes do player com os elementos da fase.
        """
        # Atualizacao do evento obrigatorio atual
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
            each_npc.apply_movement(self.player.movement)
            
        # Colisao com os monstros
        Villains_collided = pg.sprite.spritecollide(self.player, self.villains, False)
        for each_villain in Villains_collided:
            limits = self.locate_collide(self.player, each_villain)
            self.player.x_position = each_villain.x_position + each_villain.width * (-1)**limits[0]
            self.player.y_position = each_villain.y_position + each_villain.height * (-1)**limits[1]
    
    
    def ammus_collide_with(self):
        # Colisao com personagens
        character_hit_by_ammu = pg.sprite.groupcollide(self.ammus, self.characters, False, False)
        print(character_hit_by_ammu)
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
        # Colisao com objetos (empurra-os, caso consiga)
        object_pushed_by_character = pg.sprite.groupcollide(self.characters, self.game_objects, False, False)
        for each_character in object_pushed_by_character.keys():
            for each_object in object_pushed_by_character[each_character]:
                if each_object.is_static:
                    comeback = self.locate_collide(each_character, each_object)
                    print(comeback)
                        # new_position = np.array([each_character.x_position, each_character.y_position])
                        # shape = np.array([each_object.width, each_object.height])*limits
                        # each_character.x_position, each_character.y_position = new_position + shape
                        # comeback = -each_character.movement*limits
                        # each_character.apply_movement(comeback)
                    print(each_character.movement)
                    each_character.apply_movement(-comeback)
                        
                else:
                    each_object.apply_movement(each_character.movement)    
    
    def monsters_collide_with(self):
        # Colisao com objetos
        pass
    
    def npcs_collide_with(self):
        pass
    
    def update(self):
        self.player_collide_with()
        self.ammus_collide_with()
        self.game_objects_collide_with()
        self.monsters_collide_with()
        self.npcs_collide_with()
        
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