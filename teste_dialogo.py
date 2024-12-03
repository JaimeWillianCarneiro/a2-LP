import json

with open("dialogs.json", "r") as file:
    dialogs = json.load(file)["dialogs"]


import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font("assets/font.ttf", 18)  # Fonte Arial


def draw_dialog_box(screen, x, y, width, height, bg_color=(50, 50, 50), border_color=(255, 255, 255), border_width=2):
    """Desenha um retângulo padrão para o diálogo."""
    pygame.draw.rect(screen, bg_color, (x, y, width, height))
    pygame.draw.rect(screen, border_color, (x, y, width, height), border_width)


def wrap_text(text, font, max_width):
    """Divide o texto em linhas que cabem na largura máxima."""
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        # Testa se a linha atual mais a próxima palavra cabe na largura
        if font.size(current_line + word)[0] <= max_width:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    # Adiciona a última linha
    if current_line:
        lines.append(current_line.strip())

    return lines
def display_dialog(dialog, screen, font, max_width, start_y, line_spacing, box_height=150):
    """Renderiza o diálogo com altura fixa para o retângulo de fundo."""
    screen.fill((0, 0, 0))  # Fundo da tela (opcional)

    # Largura fixa com margem
    box_width = max_width + 40
    box_x = 30  # Margem esquerda
    box_y = start_y - 20  # Margem superior

    # Desenha o retângulo de fundo com altura fixa
    draw_dialog_box(screen, box_x, box_y, box_width, box_height)

    # Divide o texto em múltiplas linhas
    wrapped_lines = wrap_text(dialog["text"], font, max_width)

    # Renderiza o nome do personagem
    speaker_text = font.render(dialog["speaker"] + ":", True, (255, 255, 255))
    screen.blit(speaker_text, (box_x + 10, start_y))

    # Renderiza o texto dentro do retângulo, até a altura máxima
    y_offset = start_y + 40
    for i, line in enumerate(wrapped_lines):
        # Limita as linhas para caberem no espaço fixo
        if y_offset + line_spacing > box_y + box_height:
            break
        rendered_line = font.render(line, True, (255, 255, 255))
        screen.blit(rendered_line, (box_x + 10, y_offset))
        y_offset += line_spacing

    pygame.display.flip()

current_dialog = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Avança com Enter
                current_dialog += 1
                if current_dialog >= len(dialogs):
                    running = False

    if current_dialog < len(dialogs):
        display_dialog(
            dialog=dialogs[current_dialog],
            screen=screen,
            font=font,
            max_width=700,  # Largura máxima do texto
            start_y=400,  # Posição inicial do texto
            line_spacing=40,  # Espaçamento entre as linhas
            box_height=150  # Altura fixa do retângulo
        )
