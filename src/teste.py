import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animação com Frames")

# Carregar a imagem com os frames
sprite_sheet = pygame.image.load("imagens/framestest.png").convert_alpha()

# Configurações dos frames
frame_width = 61  # Largura de cada frame
frame_height = 55  # Altura de cada frame
columns = 3  # Quantidade de colunas
rows = 5  # Quantidade de linhas

# Extrair e redimensionar frames da imagem
frames = []
for row in range(rows):
    for col in range(columns):
        x = col * frame_width
        y = row * frame_height
        frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
        # Redimensionar o frame para o tamanho da tela
        frame = pygame.transform.scale(frame, (screen_width, screen_height))
        frames.append(frame)

# Variáveis de controle da animação
current_frame = 0
frame_delay = 100  # Tempo (ms) entre os frames
last_update_time = pygame.time.get_ticks()

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizar o frame da animação
    now = pygame.time.get_ticks()
    if now - last_update_time > frame_delay:
        current_frame = (current_frame + 1) % len(frames)
        last_update_time = now

    # Desenhar na tela
    screen.blit(frames[current_frame], (0, 0))  # O frame ocupa toda a tela
    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()
sys.exit()
