"""
This module contains the class that abstrain a menu. This class have a lot of
utility functions to handle buttons and their events.
"""

from settings import  SCREEN_DIMENSIONS, START_SOUND_MENU, START_BACKGROUND_MENU, START_COLUMNS_MENU, START_ROWS_MENU

import pygame

# class InterfaceElements:
#     def 

screen = pygame.display.set_mode((0,0))

class Menu:
    """_summary_
    """
    def __init__(self, level_instance)-> None:
        
        
        # pygame.init()

        self.clock = pygame.time.Clock()
        
        
        #  Configurações de tela
        self.screen_width = SCREEN_DIMENSIONS[0]
        self.screen_height = SCREEN_DIMENSIONS[1]
        
        # Configurações do mixer (áudio)
        pygame.mixer.init()
        self.load_audio(START_SOUND_MENU)
        
    
        
        # Configurações dos frames
        self.columns = START_COLUMNS_MENU
        self.rows = START_ROWS_MENU
        
            #  Carregar  a imagem com os frames
        self.sprite_sheet = pygame.image.load(START_BACKGROUND_MENU).convert_alpha()
        self.dimensions = (self.sprite_sheet.get_width(), self.sprite_sheet.get_height())
        self.frame_width = self.dimensions[0] // self.columns
        self.frame_height = self.dimensions[1] // self.rows
        
        # Extrair frames da sprite sheet
        self.frames = self.extract_frames()
        
        #  Controle da animação
        self.current_frame = 0
        self.frame_delay = 100  # Tempo entre frames em milissegundos
        self.last_update_time = pygame.time.get_ticks()
        
        self.current_screen = "main_menu"
        self.level= level_instance
        
    def load_audio(self, audio_path):
        """Carregar e iniciar o áudio de fundo."""
        try:
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.set_volume(0.5)  # Ajustar o volume
            pygame.mixer.music.play(-1)  # Reproduzir em loop
        except pygame.error as e:
            print(f"Erro ao carregar o áudio: {e}")
    
    def extract_frames(self):
        """Extrair os frames da sprite sheet e redimensioná-los para a tela."""
        frames = []
        for row in range(self.rows):
            for col in range(self.columns):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = self.sprite_sheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
                frame = pygame.transform.scale(frame, (self.screen_width, self.screen_height))
                frames.append(frame)
        return frames
    
    def main_menu(self):  
            running = True
            print("Entro no menu principal")
            while self.current_screen == "main_menu":
                # print("entrou no running do menu")
                # Limitar a 30 FPS
                for event in pygame.event.get():
                    # print("Evento do Menu")
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        exit()
                    
                    
                    if event.type == pygame.KEYDOWN:
                        print("KEY MENU PRINCIPAL")
                        if event.key == pygame.K_ESCAPE:
                            print("ESCAPE")
                            pygame.quit()
                            exit()
                        if event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                            print("Ainda estou aqui")                  
                            self.current_screen = "start"
                            pygame.display.update()
                            print("POpular")
                            

                
                # Atualizar o frame da animação
                self.current_frame += 0.7
                if self.current_frame >= len(self.frames):
                    self.current_frame = 0

                # Desenhar na tela
                screen.blit(self.frames[int(self.current_frame)], (0, 0))
                pygame.display.flip()
                
                pygame.display.update()
                
                
    

    