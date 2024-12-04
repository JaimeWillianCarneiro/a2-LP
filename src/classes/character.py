import pygame as pg
from abc import ABC, abstractmethod
from src.classes.background import PositionController
import numpy as np

class Character(pg.sprite.Sprite, ABC):
    """
    Representa um personagem jogável ou inimigo em um jogo, controlando suas propriedades, animações, movimento, direção e interações com armas.

    Parameters
    ----------
    name : str
        O nome do personagem, usado para carregar a sprite.
    speed : float
        A velocidade de movimento do personagem.
    perception : float
        O alcance de percepção do personagem.
    x_position : float
        A posição inicial do personagem no eixo X.
    y_position : float
        A posição inicial do personagem no eixo Y.
    width : int
        A largura da imagem do personagem.
    height : int
        A altura da imagem do personagem.
    direction : int
        A direção inicial do personagem (0 a 3, correspondendo a baixo, esquerda, cima e direita).
    skin : str
        A aparência (skin) do personagem, usada para carregar o spritesheet correspondente.
    life : int
        A quantidade de vida do personagem.
    sprites_quantity : int
        A quantidade de sprites na animação do personagem.
    map_limits_sup : tuple
        Limite superior do mapa para restrição de movimento.
    bullets : int
        O número inicial de balas ou munições do personagem.
    weapon : Weapon
        A arma equipada pelo personagem.

    Attributes
    ----------
    name : str
        O nome do personagem.
    speed : float
        A velocidade de movimento do personagem.
    perception : float
        O alcance de percepção do personagem.
    x_position : float
        A posição X do personagem.
    y_position : float
        A posição Y do personagem.
    width : int
        A largura da imagem do personagem.
    height : int
        A altura da imagem do personagem.
    image : pg.Surface
        A imagem atual do personagem, extraída do spritesheet.
    spritesheet : pg.Surface
        O spritesheet contendo as animações do personagem.
    current_sprite_x : int
        O índice da sprite atual no eixo X.
    current_sprite_y : int
        O índice da sprite atual no eixo Y, que indica a direção do movimento.
    weapon : Weapon
        A arma equipada ao personagem.
    aim : np.ndarray
        A direção do disparo da arma.
    """
    def __init__(self, name, speed, perception, x_position, y_position, width, height, direction, skin, life, sprites_quantity, map_limits_sup, bullets, weapon):
        """
        Inicializa um novo personagem com as propriedades fornecidas.

        Parameters
        ----------
        name : str
            O nome do personagem.
        speed : float
            A velocidade de movimento do personagem.
        perception : float
            O alcance de percepção do personagem.
        x_position : float
            A posição inicial do personagem no eixo X.
        y_position : float
            A posição inicial do personagem no eixo Y.
        width : int
            A largura da imagem do personagem.
        height : int
            A altura da imagem do personagem.
        direction : int
            A direção inicial do personagem (0 a 3, correspondendo a baixo, esquerda, cima e direita).
        skin : str
            A aparência (skin) do personagem, usada para carregar o spritesheet correspondente.
        life : int
            A quantidade de vida do personagem.
        sprites_quantity : int
            A quantidade de sprites na animação do personagem.
        map_limits_sup : tuple
            Limite superior do mapa para restrição de movimento.
        bullets : int
            O número inicial de balas ou munições do personagem.
        weapon : Weapon
            A arma equipada pelo personagem.
        """
        super().__init__()
        self.life = life
        self._name = name
        self._speed = speed
        self._perception = perception
        self.position_controller = PositionController(map_limits_sup, width, height)
        self._x_position = x_position
        self._y_position = y_position
        self._width = width
        self._height = height
        self.movement = np.zeros(2, dtype=float)
        self._spritesheet = pg.image.load(f'assets\\spritesheets\\{name}_{skin}.png')
        self._spritesheet = pg.transform.scale(self._spritesheet, (width*sprites_quantity, height*4))
        self.sprites_quantity = sprites_quantity 
        self._current_sprite_x = 0
        self._current_sprite_y = direction
        self.image = self.spritesheet.subsurface((self._current_sprite_x * self.width, self._current_sprite_y * self.height, self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = self._x_position, self._y_position
        self._bullets = bullets
        self._aim = np.zeros(2, dtype=float)
        self._weapon = weapon

    @property
    def name(self):
        """
        Retorna o nome do personagem.

        Returns
        -------
        str
            O nome do personagem.
        """
        return self._name

    @property
    def speed(self):
        """
        Retorna a velocidade do personagem.

        Returns
        -------
        float
            A velocidade do personagem.
        """
        return self._speed

    @speed.setter
    def speed(self, value):
        """
        Define a velocidade do personagem.

        Parameters
        ----------
        value : float
            A nova velocidade do personagem.
        """
        self._speed = value

    @property
    def perception(self):
        """
        Retorna a percepção do personagem.

        Returns
        -------
        float
            O alcance de percepção do personagem.
        """
        return self._perception

    @perception.setter
    def perception(self, value):
        """
        Define a percepção do personagem.

        Parameters
        ----------
        value : float
            O novo valor de percepção do personagem.
        """
        self._perception = value

    @property
    def x_position(self):
        """
        Retorna a posição X do personagem.

        Returns
        -------
        float
            A posição X do personagem.
        """
        return self._x_position

    @x_position.setter
    def x_position(self, value):
        """
        Define a posição X do personagem.

        Parameters
        ----------
        value : float
            A nova posição X do personagem.
        """
        self._x_position = value

    @property
    def y_position(self):
        """
        Retorna a posição Y do personagem.

        Returns
        -------
        float
            A posição Y do personagem.
        """
        return self._y_position

    @y_position.setter
    def y_position(self, value):
        """
        Define a posição Y do personagem.

        Parameters
        ----------
        value : float
            A nova posição Y do personagem.
        """
        self._y_position = value

    @property
    def width(self):
        """
        Retorna a largura da imagem do personagem.

        Returns
        -------
        int
            A largura da imagem do personagem.
        """
        return self._width

    @width.setter
    def width(self, value):
        """
        Define a largura da imagem do personagem e ajusta o tamanho da sprite.

        Parameters
        ----------
        value : int
            A nova largura da imagem do personagem.
        """
        self._width = value
        self.rect.width = value
        self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))

    @property
    def height(self):
        """
        Retorna a altura da imagem do personagem.

        Returns
        -------
        int
            A altura da imagem do personagem.
        """
        return self._height

    @height.setter
    def height(self, value):
        """
        Define a altura da imagem do personagem e ajusta o tamanho da sprite.

        Parameters
        ----------
        value : int
            A nova altura da imagem do personagem.
        """
        self._height = value
        self.rect.height = value
        self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))

    @property
    def image(self):
        """
        Retorna a imagem atual do personagem.

        Returns
        -------
        pg.Surface
            A imagem atual do personagem.
        """
        return self._image

    @image.setter
    def image(self, value):
        """
        Define a imagem atual do personagem.

        Parameters
        ----------
        value : pg.Surface
            A nova imagem do personagem.
        """
        self._image = value

    @property
    def spritesheet(self):
        """
        Retorna o spritesheet do personagem.

        Returns
        -------
        pg.Surface
            O spritesheet do personagem.
        """
        return self._spritesheet

    @spritesheet.setter
    def spritesheet(self, value):
        """
        Define o spritesheet do personagem.

        Parameters
        ----------
        value : pg.Surface
            O novo spritesheet do personagem.
        """
        self._spritesheet = value

    @property
    def current_sprite_x(self):
        """
        Retorna o índice da sprite atual no eixo X.

        Returns
        -------
        int
            O índice da sprite atual no eixo X.
        """
        return self._current_sprite_x

    @current_sprite_x.setter
    def current_sprite_x(self, value):
        self._current_sprite_x = value

    @property
    def current_sprite_y(self):
        return self._current_sprite_y

    @current_sprite_y.setter
    def current_sprite_y(self, value):
        self._current_sprite_y = value
        
    def set_position_rect(self, x_new, y_new):
        """
        Atualiza a posição do retângulo de colisão do personagem.

        Parameters
        ----------
        x_new : float
            A nova posição X do retângulo.
        y_new : float
            A nova posição Y do retângulo.
        """
        self.rect.center = (x_new, y_new)
    
    @property
    def weapon(self):
        """
        Retorna a arma equipada pelo personagem.

        Returns
        -------
        Weapon
            A arma equipada ao personagem.
        """
        return self._weapon
    
    @weapon.setter
    def weapon(self, weapon_new):
        """
        Define a arma equipada pelo personagem.

        Parameters
        ----------
        weapon_new : Weapon
            A nova arma a ser equipada ao personagem.
        """
        self._weapon = weapon_new
    
    @property
    def bullet(self):
        """
        Retorna a munição atual do personagem.

        Returns
        -------
        Bullet
            A munição atual do personagem.
        """
        return self._bullet
    
    @bullet.setter
    def bullet(self, bullet_new):
        """
        Define a munição do personagem.

        Parameters
        ----------
        bullet_new : Bullet
            A nova munição do personagem.
        """
        self._bullet = bullet_new
     
    @property
    def aim(self):
        """
        Retorna a direção do disparo da arma.

        Returns
        -------
        np.ndarray
            A direção do disparo da arma.
        """
        return self._aim
    
    @aim.setter
    def aim(self, aim_new):
        """
        Define a direção do disparo da arma.

        Parameters
        ----------
        aim_new : list or np.ndarray
            A nova direção de disparo da arma.
        """
        self._aim = np.array(aim_new)
    
    def animate(self):
        """
        Atualiza a animação do personagem, trocando a sprite atual.

        Esse método altera o índice da sprite para a próxima na animação, 
        se houver mais de uma sprite disponível.
        """
        if self.sprites_quantity > 1:
            self._current_sprite_x += 0.2
            if self._current_sprite_x >= self.sprites_quantity:
                self.current_sprite_x = 0
            current_sprite_x = int(self.current_sprite_x)
            self.image = self.spritesheet.subsurface((current_sprite_x * self.width, self._current_sprite_y * self.height, self.width, self.height))
    
    def redefine_direction(self, movement):
        """
        Atualiza a direção do personagem com base no movimento.

        O movimento é um vetor 2D, e a direção é determinada pelas coordenadas desse vetor. 

        Parameters
        ----------
        movement : np.ndarray
            O vetor de movimento (x, y) que determina a direção do personagem.
        """
        if movement[0] > 0:
            current_sprite_y = 2
        elif movement[0] < 0:
            current_sprite_y = 3
        elif movement[1] < 0:
            current_sprite_y = 1
        elif movement[1] > 0:
            current_sprite_y = 0
        else:
            current_sprite_y = (self.current_sprite_y+1)%4
            self.current_sprite_y ^= current_sprite_y
            current_sprite_y ^= self.current_sprite_y
            self.current_sprite_y ^= current_sprite_y
            
        if self.current_sprite_y != current_sprite_y:
            self.current_sprite_y = current_sprite_y
            self.current_sprite_x = 0   

    def apply_movement(self, movement, redefine_direction = True):
        """
        Aplica o movimento ao personagem, atualizando sua posição e a animação.

        Esse método também corrige a posição do personagem de acordo com os limites do mapa e a colisão.

        Parameters
        ----------
        movement : np.ndarray
            O vetor de movimento (dx, dy) que define a movimentação do personagem.
        redefine_direction : bool, opcional
            Se True, a direção será redefinida com base no movimento. Por padrão é True.

        Returns
        -------
        np.ndarray
            O vetor de movimento que não pôde ser aplicado devido a limitações de movimento.
        """
        if redefine_direction:
            self.redefine_direction(movement)
        
        x_new = self.x_position + movement[0]
        y_new = self.y_position + movement[1]
        x_new_corrected, y_new_corrected = self.position_controller.to_frame(x_new, y_new)
        
        # Devolve a parte do movimento que nao foi aplicado
        comeback = np.array([x_new, y_new]) - np.array([x_new_corrected, y_new_corrected])
        
        self.x_position = x_new_corrected
        self.y_position = y_new_corrected
        self.movement = movement
        
        return -comeback
        
    @abstractmethod
    def update(self):
        """
        Método abstrato que deve ser implementado pelas subclasses para atualizar o estado do personagem.

        Esse método será chamado a cada ciclo de jogo para atualizar o personagem, 
        como a movimentação, a animação e a interação com o ambiente.
        """
        pass