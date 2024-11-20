import pygame
import moviepy.editor
# Inicializar o pygame
pygame.init()

# Configurações da janela do jogo
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tela Inicial - Jogo")



# Carregar o vídeo
video_clip = VideoFileClip("audios/video abertura.mp4")

# Redimensionar usando argumentos nomeados
video_clip = video_clip.resize(width=screen_width, height=screen_height)  # Ajusta para o tamanho da tela

# Clock para controlar o FPS do pygame
clock = pygame.time.Clock()

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Calcular o tempo atual do vídeo (loop infinito)
    current_time = pygame.time.get_ticks() / 1000  # Tempo em segundos
    video_time = current_time % video_clip.duration
    
    # Obter o quadro atual do vídeo
    frame = video_clip.get_frame(video_time)
    
    # Converter o quadro para uma superfície do Pygame
    frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    
    # Desenhar o quadro na tela
    screen.blit(frame_surface, (0, 0))
    
    # Atualizar a janela
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(30)

# Encerrar o pygame
pygame.quit()
