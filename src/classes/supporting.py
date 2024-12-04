import pygame as pg
from src.classes.character import Character

class Supporting(Character):
    """
    Representa um personagem de suporte no jogo, herdando da classe `Character`.
    Este tipo de personagem pode ter características similares a outros personagens, mas com habilidades ou funções de suporte específicas.

    Atributos:
        name (str): Nome do personagem de suporte.
        speed (int): Velocidade do personagem de suporte.
        perception (int): Percepção do personagem de suporte.
        x_position (float): Posição horizontal do personagem de suporte no mapa.
        y_position (float): Posição vertical do personagem de suporte no mapa.
        width (int): Largura do personagem de suporte.
        height (int): Altura do personagem de suporte.
        direction (str): Direção para a qual o personagem de suporte está voltado.
        skin (str): Identificador da skin do personagem de suporte.
        sprites_quantity (int): Quantidade de sprites associadas ao personagem de suporte.
        map_limits_sup (tuple): Limites superiores do mapa em que o personagem pode se mover.

    Métodos:
        __init__: Inicializa um objeto do tipo Supporting, configurando os parâmetros herdados da classe `Character`.
    """
    def __init__(self, name, speed, perception, x_position, y_position, width, height, direction, skin, sprites_quantity, map_limits_sup):
        """
        Inicializa um objeto do tipo Supporting.

        Parâmetros:
            name (str): Nome do personagem de suporte.
            speed (int): Velocidade do personagem de suporte.
            perception (int): Percepção do personagem de suporte.
            x_position (float): Posição horizontal do personagem de suporte no mapa.
            y_position (float): Posição vertical do personagem de suporte no mapa.
            width (int): Largura do personagem de suporte.
            height (int): Altura do personagem de suporte.
            direction (str): Direção para a qual o personagem de suporte está voltado.
            skin (str): Identificador da skin do personagem de suporte.
            sprites_quantity (int): Quantidade de sprites associadas ao personagem de suporte.
            map_limits_sup (tuple): Limites superiores do mapa.
        """
        super().__init__(name, speed, perception, x_position, y_position, width, height, direction, skin, sprites_quantity, map_limits_sup)
