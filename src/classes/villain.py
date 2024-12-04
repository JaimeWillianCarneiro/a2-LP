import pygame as pg
from src.classes.character import Character
from src.classes.gameobjects import Ammo
from src.settings import FRAME_RATE
import numpy as np


class Villain(Character):
    """
    Representa um vilão no jogo, herdando da classe `Character`.
    Este vilão tem habilidades de percepção, memorização de posições, visão de campo e interação com o personagem jogador.

    Atributos:
        life (int): Quantidade de vida do vilão.
        memories (list): Lista de memórias de posições anteriores do vilão.
        mem_size (int): Tamanho máximo da memória do vilão.
        vision_field (pygame.Rect): Área de visão do vilão no mapa.
        scooby_snacks (GameObject): Referência ao objeto "Scooby Snacks", que o vilão persegue.
        map_limits_sup (list): Limites superiores do mapa em que o vilão pode se mover.

    Métodos:
        update: Atualiza o estado do vilão, incluindo movimento, interação com o jogador, ataque e animação.
        attack: Realiza um ataque contra o jogador.
        evaluate_interaction: Avalia interações adicionais (não implementado).
        carry_weapon: Atualiza a posição da arma com base no movimento do vilão.
        define_direction: Define a direção do vilão com base nas memórias ou no alvo (scooby_snacks).
        set_position_rect_vision: Define a posição do campo de visão do vilão.
        memories_append: Adiciona uma nova memória à lista de memórias do vilão.
        memories_remove: Remove a primeira memória da lista de memórias do vilão.
    """
    def __init__(self, name, speed, perception, x_position, y_position, width, height, direction, skin,
                 life, sprites_quantity, map_limits_sup, bullets, weapon, mem_size, vision_field, background, scooby_snacks):
        """
        Inicializa um objeto do tipo Villain.

        Parâmetros:
            name (str): Nome do vilão.
            speed (int): Velocidade do vilão.
            perception (int): Percepção do vilão.
            x_position (float): Posição horizontal do vilão no mapa.
            y_position (float): Posição vertical do vilão no mapa.
            width (int): Largura do vilão.
            height (int): Altura do vilão.
            direction (str): Direção para a qual o vilão está voltado.
            skin (str): Identificador da skin do vilão.
            life (int): Quantidade de vida do vilão.
            sprites_quantity (int): Quantidade de sprites associadas ao vilão.
            map_limits_sup (tuple): Limites superiores do mapa.
            bullets (int): Quantidade de balas que o vilão possui.
            weapon (Weapon): A arma que o vilão usa.
            mem_size (int): Tamanho máximo da memória do vilão.
            vision_field (int): O campo de visão do vilão, em pixels.
            background (Surface): Superfície de fundo usada para definir os limites do mapa.
            scooby_snacks (GameObject): Referência ao objeto que o vilão persegue.
        """
        super().__init__(name, speed, perception, x_position, y_position, width, height, direction, skin, life, sprites_quantity, map_limits_sup, bullets, weapon)
        self._life = life
        self._memories = []
        self._mem_size = mem_size
        self._vision_field = pg.Rect(x_position - vision_field, y_position - vision_field, 2*vision_field, 2*vision_field)
        self.scooby_snacks = scooby_snacks
        self.map_limits_sup = list(background.get_shape())

    @property
    def life(self):
        """
        Obtém a quantidade de vida do vilão.

        Retorno:
            float: Quantidade de vida do vilão.
        """
        return self._life

    @life.setter
    def life(self, value):
        """
        Define a quantidade de vida do vilão.

        Parâmetros:
            value (float): Novo valor da vida do vilão.
        """
        self._life = value

    @property
    def memories(self):
        """
        Obtém a lista de memórias do vilão.

        Retorno:
            list: Lista contendo as memórias de posições do vilão.
        """
        return self._memories

    @property
    def mem_size(self):
        """
        Obtém o tamanho máximo da memória do vilão.

        Retorno:
            int: Tamanho máximo da memória do vilão.
        """
        return self._mem_size

    @mem_size.setter
    def mem_size(self, value):
        """
        Define o tamanho máximo da memória do vilão.

        Parâmetros:
            value (int): Novo tamanho máximo da memória.
        """
        self._mem_size = value

    @property
    def range(self):
        """
        Obtém o alcance de ataque do vilão.

        Retorno:
            int: O alcance de ataque do vilão.
        """
        return self._range

    @range.setter
    def range(self, value):
        """
        Define o alcance de ataque do vilão.

        Parâmetros:
            value (int): Novo alcance de ataque.
        """
        self._range = value

    @property
    def vision_field(self):
        """
        Obtém o campo de visão do vilão.

        Retorno:
            pygame.Rect: O campo de visão do vilão.
        """
        return self._vision_field

    @vision_field.setter
    def vision_field(self, value):
        """
        Define o campo de visão do vilão.

        Parâmetros:
            value (pygame.Rect): Novo campo de visão.
        """
        self._vision_field = value

    def set_position_rect_vision(self, x_new, y_new):
        """
        Atualiza o centro do campo de visão do vilão de acordo com a nova posição.

        Parâmetros:
            x_new (float): Nova posição horizontal.
            y_new (float): Nova posição vertical.
        """
        self.vision_field.center = (x_new, y_new)
    
    def memories_append(self, memory):
        """
        Adiciona uma nova memória à lista de memórias do vilão. Se a memória exceder o tamanho máximo, remove a mais antiga.

        Parâmetros:
            memory (tuple): Memória representada por uma tupla (x, y) da posição do vilão.
        """
        self._memories.append(memory)
        if len(self._memories) > self.mem_size:
            self._memories.pop(0)
    
    def memories_remove(self):
        """
        Remove a primeira memória da lista de memórias do vilão, se houver memórias armazenadas.
        """
        if len(self._memories) > 0:
            self._memories.pop(0)
            
    def define_direction(self):
        """
        Define a direção do vilão, com base nas suas memórias ou no objeto de interesse (scooby_snacks).

        Retorno:
            numpy.ndarray: Vetor de direção do vilão, normalizado de acordo com a velocidade.
        """
        valid_memories = [memorie for memorie in self.memories]
        vector = [0, 0]
        if valid_memories:
            x_sum = 0
            y_sum = 0
            for x, y in valid_memories:
                x_sum += x
                y_sum += y
            x_mean = x_sum/len(valid_memories)
            y_mean = y_sum/len(valid_memories)
                
            vector = [x_mean - self.x_position, y_mean - self.y_position]
        else:
            vector = [self.scooby_snacks.x_position - self.x_position, self.scooby_snacks.y_position - self.y_position]
        
        # Avalia a direcao final com base no vetor
        if abs(vector[0]) < self.speed:
            vector[0] = 0
        else:
            vector[0] *= self.speed/abs(vector[0])
        if abs(vector[1]) < self.speed:
            vector[1] = 0
        else:
            vector[1] *= self.speed/abs(vector[1])
        
        return np.array(vector)
            

    def attack(self, player):
        """
        Realiza um ataque contra o jogador, reduzindo sua vida com base no dano da arma do vilão.

        Parâmetros:
            player (Player): O jogador a ser atacado.
        """
        print('Dano corpo\n')
        player.life = player.life - self.weapon.damage

    def evaluate_interaction(self):
        pass
    

    
    def carry_weapon(self):
        """
        Atualiza a posição da arma do vilão com base no seu movimento e na animação atual.

        Este método ajusta a posição da arma dependendo da direção do vilão.
        """
        # Move a arma junto do vilao
        out_shape = [0, 0]
        if self.current_sprite_y == 0:
            out_shape[1] = self.height/2
        elif self.current_sprite_y == 1:
            out_shape[1] = -self.height/2
        elif self.current_sprite_y == 2:
            out_shape[0] = self.width/2
        else:
            out_shape[0] = -self.width/2
            
        self.weapon.set_position(self.x_position + out_shape[0], self.y_position+ out_shape[1])
        
    
    def update(self, player):
        """
        Atualiza o estado do vilão, verificando se o jogador está dentro do campo de visão ou de ataque,
        movendo o vilão em direção ao jogador ou ao seu objetivo, e atualizando a animação e a posição.

        Parâmetros:
            player (Player): O jogador com o qual o vilão interage.
        """
        # Verifica se o player esta no campo de visao
        if self.vision_field.colliderect(player.rect):
            self.memories_append((player.x_position, player.y_position))
        else:
            self.memories_remove()
            
        # Verifica se o player esta no campo de ataque
        if self.weapon.attack_field.colliderect(player.rect):
            self.attack(player)
            
        movement = self.define_direction()
        movement = self.position_controller.normalize_movement(movement, self.speed)
        self.apply_movement(movement)
        self.aim = self.movement
        
        x_new, y_new = self.position_controller.apply_translation(self.x_position, self.y_position)
        self.set_position_rect(x_new, y_new)
        self.set_position_rect_vision(x_new, y_new)

        self.carry_weapon()
        
        self.animate()
