"""
This module contains the class that abstrain a menu. This class have a lot of
utility functions to handle buttons and their events.
"""

from settings import  SCREEN_DIMENSIONS, START_SOUND_MENU, START_BACKGROUND_MENU, START_COLUMNS_MENU, START_ROWS_MENU

import pygame

# class InterfaceElements:
#     def 

screen = pygame.display.set_mode((0,0))

def get_font(size):
    pass

class Menu:
    """
    Represents the menu system in the game.
    
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
                
                
    def pause(self):
        """
        Displays the pause screen with options to resume, go to the main menu, or quit the game.

        Returns
        -------
        None.
        """

        while self.current_screen == "pause":
            pause_mouse_pos = pygame.mouse.get_pos()

            screen.fill("white")

            pause_text = get_font(45).render("PAUSE", True, "Black")
            pause_rect = pause_text.get_rect(center=(640, 260))
            screen.blit(pause_text, pause_rect)

            resume_button = Button(image=None, pos=(640, 360),
                                text_input="RESUME", font=get_font(75), base_color="Black", hovering_color="Green")
            menu_button = Button(image=None, pos=(640, 460),
                                text_input="MENU", font=get_font(75), base_color="Black", hovering_color="Green")
            quit_button = Button(image=None, pos=(640, 560),
                                text_input="QUIT", font=get_font(75), base_color="Black", hovering_color="Green")

            for button in [resume_button, menu_button, quit_button]:
                button.change_color(pause_mouse_pos)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.check_for_input(pause_mouse_pos):
                        self.current_screen = "play"
                    if menu_button.check_for_input(pause_mouse_pos):
                        self.current_screen = "main_menu"
                    if quit_button.check_for_input(pause_mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()


    