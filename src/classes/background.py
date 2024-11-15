import pygame as pg
from src.settings import SCREEN_DIMENSIONS, Fonts

class Background(pg.sprite.Sprite):
    def __init__(self, screen, sprite, x_position, y_position, width, height, music, volume, sounds):
        super().__init__()
        self.screen = screen
        self.sprite = pg.image.load(sprite)
        self.sprite = pg.transform.scale(self.sprite, (width, height))
        self.position_controller = PositionController([width, height], SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1])
        self.x_position = x_position - SCREEN_DIMENSIONS[0]//2
        self.y_position = y_position - SCREEN_DIMENSIONS[1]//2
        self.width = width
        self.height = height
        self.music = music
        self.volume = volume
        self.sounds = sounds
        self.image = self.sprite.subsurface((self.x_position, self.y_position, *SCREEN_DIMENSIONS))
        self.rect = self.image.get_rect()
        pg.mixer.music.load(self.music)
        pg.mixer.music.set_volume(self.volume)
        
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
        # Centraliza a camera no personagem
        x_new, y_new = self.position_controller.to_frame(x_player, y_player)
        x_new -= SCREEN_DIMENSIONS[0]/2
        y_new -= SCREEN_DIMENSIONS[1]/2
        self.set_position(x_new, y_new)
        self.image = self.sprite.subsurface((*self.get_position(), *SCREEN_DIMENSIONS))
        
    def play_music(self):
        pg.mixer.music.play(-1)
        
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
    def __init__(self, screen, fase_atual, interface_elements):
        self.screen = screen
        self.fase_atual = fase_atual
        self.interface_elements = interface_elements
        self.player_name = Fonts.PLAYER_NAME.value.render('Player :'+str(self.fase_atual.player.name), True, (123, 173, 123))
        self.player_life = Fonts.PLAYER_LIFE.value.render('Life: '+str(self.fase_atual.player.life), True, (123, 173, 223))
        self.event_warning =  Fonts.EVENT_WARNING.value.render('Volte para a Zona!', True, (255, 255, 255))
        self.event_time = Fonts.EVENT_TIME.value.render('Time: '+str(self.fase_atual.current_mandatory_event.time), True, (123, 173, 223))
        self.player_name_location = (50, 50)
        self.player_life_location = (300, 50)
        self.event_warning_location = ((SCREEN_DIMENSIONS[0]*2)//5, 100)
        self.event_time_location = (SCREEN_DIMENSIONS[0]//2-50, 50)
        
    def set_fase_atual(self, new_fase):
        self.fase_atual = new_fase
        
    def draw_interface(self):
        # Desenha os atributos do player no canto superior esquerdo
        self.screen.blit(self.player_name, self.player_name_location)
        self.screen.blit(self.player_life, self.player_life_location)
        
        # Desenha avisos e informacoes da fase no centro superior da tela
        if self.fase_atual.current_mandatory_event:
            if self.fase_atual.current_mandatory_event.in_execution:
                if self.fase_atual.current_mandatory_event.out_zone:
                    self.screen.blit(self.event_warning, self.event_warning_location)
                self.event_time = self.fase_atual.current_mandatory_event.time
                self.event_time = Fonts.EVENT_TIME.value.render('Time: '+str(self.event_time), True, (123, 173, 223))
                self.screen.blit(self.event_time, self.event_time_location)
        
        # Desenha o minimapa e as configuracoes no canto superior direito
        
    def update(self):
        self.player_life = Fonts.PLAYER_LIFE.value.render('Life: '+str(self.fase_atual.player.life), True, (123, 173, 223))
        self.draw_interface()
    
class PositionController():
    x_origin = 0
    y_origin = 0
    def __init__(self, map_limits_sup, width, height):
        self.map_limits_inf = [width/2, height/2]
        self.map_limits_sup = map_limits_sup.copy()
        self.map_limits_sup[0] -= width/2
        self.map_limits_sup[1] -= height/2
        
    @classmethod
    def set_origin(cls, x_new, y_new):
        cls.x_origin = x_new
        cls.y_origin = y_new  

    @staticmethod
    def normalize_movement(movement):
        if movement['x_moved'] and movement['y_moved']:
                norma = movement['x_moved']**2
                moved = (norma/2)**(1/2)
                movement['x_moved'] = moved * movement['x_moved']/abs(movement['x_moved'])
                movement['y_moved'] = moved * movement['y_moved']/abs(movement['y_moved'])
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
    
    def apply_translation(self, x_position, y_position):
        # Aplica uma translacao no plano, considerando o sistema de coordenadas na qual o jogo sera desenhado
        x_new = x_position - self.x_origin
        y_new = y_position - self.y_origin
        return x_new, y_new