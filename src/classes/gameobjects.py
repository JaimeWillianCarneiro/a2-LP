import pygame as pg
from src.settings import SCREEN_DIMENSIONS, FRAME_RATE
from src.classes.background import PositionController
import numpy as np

class GameObject(pg.sprite.Sprite):
    """
    Representa um objeto no jogo que pode ser animado, movido e atualizado dentro do mapa. 
    Pode ser um objeto estático ou dinâmico e interagir com o ambiente.

    Parameters
    ----------
    x_position : float
        A posição inicial do objeto no eixo X.
    y_position : float
        A posição inicial do objeto no eixo Y.
    width : int
        A largura da imagem do objeto.
    height : int
        A altura da imagem do objeto.
    map_limits_sup : tuple
        Limite superior do mapa para restrição de movimento.
    spritesheet : str
        O caminho para o arquivo de spritesheet que contém as animações do objeto.
    sprite_actual_x : int
        O índice inicial da sprite no eixo X.
    sprite_actual_y : int
        O índice inicial da sprite no eixo Y.
    sprites_quantity : int
        A quantidade total de sprites no eixo X do spritesheet.
    is_static : bool
        Um valor booleano que indica se o objeto é estático ou não.

    Attributes
    ----------
    x_position : float
        A posição X do objeto no jogo.
    y_position : float
        A posição Y do objeto no jogo.
    width : int
        A largura da imagem do objeto.
    height : int
        A altura da imagem do objeto.
    movement : np.ndarray
        O vetor de movimento aplicado ao objeto.
    spritesheet_path : str
        O caminho para o arquivo de spritesheet.
    spritesheet : pg.Surface
        A imagem carregada do spritesheet.
    sprite_actual_x : int
        O índice atual da sprite no eixo X.
    sprite_actual_y : int
        O índice atual da sprite no eixo Y.
    sprites_quantity : int
        A quantidade total de sprites na animação.
    is_static : bool
        Um valor booleano que indica se o objeto é estático.
    image : pg.Surface
        A imagem atual do objeto.
    rect : pg.Rect
        O retângulo de colisão que envolve o objeto.
    """
    def __init__(self, x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity, is_static):
        """
        Inicializa um novo objeto do jogo com as propriedades fornecidas, incluindo 
        o spritesheet e os parâmetros de posição e tamanho.

        Parameters
        ----------
        x_position : float
            A posição inicial do objeto no eixo X.
        y_position : float
            A posição inicial do objeto no eixo Y.
        width : int
            A largura da imagem do objeto.
        height : int
            A altura da imagem do objeto.
        map_limits_sup : tuple
            Limite superior do mapa para restrição de movimento.
        spritesheet : str
            O caminho para o arquivo de spritesheet que contém as animações do objeto.
        sprite_actual_x : int
            O índice inicial da sprite no eixo X.
        sprite_actual_y : int
            O índice inicial da sprite no eixo Y.
        sprites_quantity : int
            A quantidade total de sprites no eixo X do spritesheet.
        is_static : bool
            Um valor booleano que indica se o objeto é estático ou não.
        """
        super().__init__()
        self.position_controller = PositionController(map_limits_sup, width, height)
        self.x_position = x_position
        self.y_position = y_position
        self.width = width
        self.height = height
        self.movement = np.zeros(2)
        self.spritesheet_path = spritesheet
        self.spritesheet = pg.image.load(spritesheet)
        self.spritesheet = pg.transform.scale(self.spritesheet, (self.width*sprites_quantity, self.height))
        self.sprite_actual_x = sprite_actual_x
        self.sprite_actual_y = sprite_actual_y
        self.sprites_quantity = sprites_quantity
        self.is_static = is_static
        self.image = self.spritesheet.subsurface((self.sprite_actual_x*self.width, self.sprite_actual_y*self.height, width, height))
        self.image = pg.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.x_position, self.y_position
    
    def set_position(self, x_new, y_new):
        """
        Define a nova posição do objeto.

        Parameters
        ----------
        x_new : float
            A nova posição X do objeto.
        y_new : float
            A nova posição Y do objeto.
        """
        self.x_position = x_new
        self.y_position = y_new
        
    def get_position(self):
        """
        Retorna a posição atual do objeto no formato (x, y).

        Returns
        -------
        tuple
            A posição atual do objeto, composta por (x_position, y_position).
        """
        return self.x_position, self.y_position

    def set_position_rect(self, x_new, y_new):
        """
        Atualiza a posição do retângulo de colisão do objeto.

        Parameters
        ----------
        x_new : float
            A nova posição X do retângulo.
        y_new : float
            A nova posição Y do retângulo.
        """
        self.rect.center = (x_new, y_new)
        
    def apply_movement(self, movement, sla=True):
        """
        Aplica o movimento ao objeto e atualiza sua posição, respeitando os limites do mapa.

        Parameters
        ----------
        movement : np.ndarray
            O vetor de movimento (dx, dy) que define a movimentação do objeto.
        sla : bool, opcional
            Parâmetro não utilizado, mas mantido por compatibilidade. Por padrão é True.

        Returns
        -------
        np.ndarray
            O vetor de movimento que não pôde ser aplicado devido a limitações de movimento.
        """
        x_new = self.x_position + movement[0]
        y_new = self.y_position + movement[1]
        x_new_corrected, y_new_corrected = self.position_controller.to_frame(x_new, y_new)
        
        # Devolve a parte do movimento que nao foi aplicado
        comeback = np.array([x_new, y_new]) - np.array([x_new_corrected, y_new_corrected])
        
        self.set_position(x_new_corrected, y_new_corrected)
        self.movement = movement
        
        return -comeback
        
    
    def animate(self):
        """
        Atualiza a animação do objeto, trocando a sprite atual.

        Esse método altera a sprite de acordo com a quantidade de sprites no eixo X do spritesheet.
        A animação é cíclica e reinicia quando o índice de sprite ultrapassa a quantidade disponível.
        """
        if self.sprites_quantity > 1:
            self.sprite_actual_x += 0.2
            self.sprite_actual_x %= self.sprites_quantity
            self.image = self.spritesheet.subsurface((int(self.sprite_actual_x), self.sprite_actual_y, self.width, self.height))
    
    def update(self):
        """
        Atualiza o estado do objeto.

        Esse método é chamado a cada ciclo do jogo para atualizar a posição do objeto e sua animação. 
        O objeto também ajusta sua posição conforme a movimentação e os limites do mapa.
        """
        self.movement = np.zeros(2)
        x_position, y_position = self.get_position()
        x_new, y_new = self.position_controller.apply_translation(x_position, y_position)
        self.set_position_rect(x_new, y_new)
        self.animate()


class Collectible(GameObject):
    """
    Representa um objeto colecionável no jogo, derivado de `GameObject`, que pode ser visível ou invisível 
    e contém uma descrição. Pode ser coletado ou interagido pelo jogador, dependendo da visibilidade.

    Parameters
    ----------
    x_position : float
        A posição inicial do objeto colecionável no eixo X.
    y_position : float
        A posição inicial do objeto colecionável no eixo Y.
    width : int
        A largura da imagem do objeto colecionável.
    height : int
        A altura da imagem do objeto colecionável.
    map_limits_sup : tuple
        Limite superior do mapa para restrição de movimento.
    spritesheet : str
        O caminho para o arquivo de spritesheet que contém as animações do objeto.
    sprite_actual_x : int
        O índice inicial da sprite no eixo X.
    sprite_actual_y : int
        O índice inicial da sprite no eixo Y.
    sprites_quantity : int
        A quantidade total de sprites no eixo X do spritesheet.
    is_static : bool
        Um valor booleano que indica se o objeto colecionável é estático ou não.
    visible : bool
        Um valor booleano que determina se o objeto colecionável é visível no jogo.
    description : str
        A descrição do objeto colecionável, que pode ser exibida quando o jogador interage com ele.

    Attributes
    ----------
    visible : bool
        A visibilidade atual do objeto colecionável.
    description : str
        A descrição do objeto colecionável.
    """
    def __init__(self, x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity, is_static, visible, description):
        """
        Inicializa um novo objeto colecionável com as propriedades fornecidas, incluindo a visibilidade 
        e a descrição, além das propriedades herdadas de `GameObject`.

        Parameters
        ----------
        x_position : float
            A posição inicial do objeto colecionável no eixo X.
        y_position : float
            A posição inicial do objeto colecionável no eixo Y.
        width : int
            A largura da imagem do objeto colecionável.
        height : int
            A altura da imagem do objeto colecionável.
        map_limits_sup : tuple
            Limite superior do mapa para restrição de movimento.
        spritesheet : str
            O caminho para o arquivo de spritesheet que contém as animações do objeto.
        sprite_actual_x : int
            O índice inicial da sprite no eixo X.
        sprite_actual_y : int
            O índice inicial da sprite no eixo Y.
        sprites_quantity : int
            A quantidade total de sprites no eixo X do spritesheet.
        is_static : bool
            Um valor booleano que indica se o objeto colecionável é estático ou não.
        visible : bool
            Um valor booleano que determina se o objeto colecionável é visível no jogo.
        description : str
            A descrição do objeto colecionável.
        """
        super().__init__(x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity, is_static)
        self._visible = visible
        self.description = description
    
    @property
    def visible(self):
        """
        Retorna a visibilidade atual do objeto colecionável.

        Returns
        -------
        bool
            O estado atual da visibilidade do objeto colecionável (True para visível, False para invisível).
        """
        return self._visible
    
    @visible.setter
    def visible(self, new_value):
        """
        Define a nova visibilidade do objeto colecionável.

        Parameters
        ----------
        new_value : bool
            O valor booleano que define a visibilidade do objeto colecionável (True para visível, False para invisível).
        """
        self._visible = new_value
        
class Ammo(GameObject):
    """
    Representa um objeto de munição no jogo, derivado de `GameObject`, que possui propriedades como dano, 
    efeitos, direção de movimento, ricochete e velocidade. A munição pode se mover de acordo com a direção 
    e a velocidade definidas, e pode ter efeitos específicos ao colidir com outros objetos.

    Parameters
    ----------
    x_position : float
        A posição inicial do objeto de munição no eixo X.
    y_position : float
        A posição inicial do objeto de munição no eixo Y.
    width : int
        A largura da imagem do objeto de munição.
    height : int
        A altura da imagem do objeto de munição.
    map_limits_sup : tuple
        Limite superior do mapa para restrição de movimento.
    spritesheet : str
        O caminho para o arquivo de spritesheet que contém as animações do objeto.
    sprite_actual_x : int
        O índice inicial da sprite no eixo X.
    sprite_actual_y : int
        O índice inicial da sprite no eixo Y.
    sprites_quantity : int
        A quantidade total de sprites no eixo X do spritesheet.
    is_static : bool
        Um valor booleano que indica se o objeto de munição é estático ou não.
    damage : int
        O dano que a munição causa ao atingir um alvo.
    effects : list
        Efeitos adicionais que a munição pode ter (ex.: explosão, fogo, etc.).
    direction : numpy.ndarray
        A direção do movimento da munição, representada como um vetor unitário.
    recochet : bool
        Um valor booleano que indica se a munição pode ricochetear após atingir um alvo ou superfície.
    speed : float
        A velocidade com que a munição se move.

    Attributes
    ----------
    damage : int
        O dano causado pela munição.
    effects : list
        Os efeitos adicionais causados pela munição.
    bullets : int
        O número de munições restantes.
    """
    def __init__(self, x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity, is_static, damage, effects, direction, recochet, speed):
        """
        Inicializa um novo objeto de munição com as propriedades fornecidas, incluindo dano, efeitos, 
        direção de movimento, ricochete e velocidade, além das propriedades herdadas de `GameObject`.

        Parameters
        ----------
        x_position : float
            A posição inicial do objeto de munição no eixo X.
        y_position : float
            A posição inicial do objeto de munição no eixo Y.
        width : int
            A largura da imagem do objeto de munição.
        height : int
            A altura da imagem do objeto de munição.
        map_limits_sup : tuple
            Limite superior do mapa para restrição de movimento.
        spritesheet : str
            O caminho para o arquivo de spritesheet que contém as animações do objeto.
        sprite_actual_x : int
            O índice inicial da sprite no eixo X.
        sprite_actual_y : int
            O índice inicial da sprite no eixo Y.
        sprites_quantity : int
            A quantidade total de sprites no eixo X do spritesheet.
        is_static : bool
            Um valor booleano que indica se o objeto de munição é estático ou não.
        damage : int
            O dano que a munição causa ao atingir um alvo.
        effects : list
            Efeitos adicionais que a munição pode ter (ex.: explosão, fogo, etc.).
        direction : numpy.ndarray
            A direção do movimento da munição, representada como um vetor unitário.
        recochet : bool
            Um valor booleano que indica se a munição pode ricochetear após atingir um alvo ou superfície.
        speed : float
            A velocidade com que a munição se move.
        """
        super().__init__(x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity, is_static)
        self._damage = damage
        self._effects = effects
        self.direction = direction
        self.recochet = recochet
        self.speed = speed
        
    @property
    def damage(self):
        """
        Retorna o dano causado pela munição.

        Returns
        -------
        int
            O dano causado pela munição.
        """
        return self._damage
    
    @property
    def effects(self):
        """
        Retorna os efeitos adicionais causados pela munição.

        Returns
        -------
        list
            Os efeitos adicionais causados pela munição (ex.: explosão, fogo, etc.).
        """
        return self._effects
    
    @property
    def bullets(self):
        """
        Retorna o número de munições restantes.

        Returns
        -------
        int
            O número de munições restantes.
        """
        return self._bullets
    
    @bullets.setter
    def bullets(self, bullets_new):
        """
        Define o número de munições restantes.

        Parameters
        ----------
        bullets_new : int
            O novo número de munições restantes.
        """
        self._bullets = bullets_new
        
    def copy(self):
        """
        Cria uma cópia do objeto de munição atual com os mesmos atributos.

        Returns
        -------
        Ammo
            Uma nova instância de `Ammo` com os mesmos atributos da munição atual.
        """
        return Ammo(self.x_position, self.y_position, self.width, self.height, self.position_controller.map_limits_sup, self.spritesheet_path, self.sprite_actual_x, self.sprite_actual_y, self.sprites_quantity, self.is_static, self.damage, self.effects, self.direction, self.recochet, self.speed)
        
    def update(self):
        """
        Atualiza a posição da munição com base em sua direção e velocidade. Verifica se a munição sai da área do jogo 
        e atualiza sua posição no jogo. Além disso, chama a função `update` de `GameObject` para animar e realizar outras atualizações.

        A posição da munição é ajustada com base no tempo (controlado por `FRAME_RATE`), e a função `out_game` é chamada 
        para garantir que a munição permaneça dentro dos limites do jogo.
        """
        position = np.array(self.get_position(), dtype=float)
        position += self.direction*self.speed*10/FRAME_RATE
        self.position_controller.out_game(self)
        self.set_position(position[0], position[1])
        super().update()
        
# class Weapon:
#     Atributos:
#     Dano
#     Se é de arremesso ou corpo a corpo
#     Efeito especial (cool down): elemental, se empurra, imobiliza o personagem
    
#     Métodos:
#     Atacar 
#     AtaqueEspecial
#     Defender
    
    

class Weapon(GameObject):
    """
    Representa uma arma no jogo, derivada de `GameObject`, que pode disparar munições com um determinado dano,
    tipo de dano, efeitos especiais e propriedades de recarga. A arma também possui um campo de ataque que define a área 
    onde ela pode afetar inimigos ou objetos, e ela é capaz de disparar munições de acordo com sua direção e tempo de recarga.

    Parameters
    ----------
    x_position : float
        A posição inicial da arma no eixo X.
    y_position : float
        A posição inicial da arma no eixo Y.
    width : int
        A largura da imagem da arma.
    height : int
        A altura da imagem da arma.
    map_limits_sup : tuple
        Limite superior do mapa para restrição de movimento.
    spritesheet : str
        O caminho para o arquivo de spritesheet que contém as animações da arma.
    sprite_actual_x : int
        O índice inicial da sprite no eixo X.
    sprite_actual_y : int
        O índice inicial da sprite no eixo Y.
    sprites_quantity : int
        A quantidade total de sprites no eixo X do spritesheet.
    is_static : bool
        Um valor booleano que indica se a arma é estática ou não.
    damage : int
        O dano que a arma causa ao atingir um alvo.
    kind_damage : str
        O tipo de dano que a arma causa (ex.: "físico", "mágico", etc.).
    attack_field : int
        O tamanho do campo de ataque da arma, determinando a área ao redor da posição da arma onde ela pode afetar alvos.
    reload_time : int
        O tempo necessário para recarregar a arma.
    ammo : Ammo
        A munição que a arma utiliza para disparos.
    scope : float
        O alcance da arma, ou a distância máxima que ela pode atingir.
    special_effect : str, optional
        Um efeito especial que a arma pode ter, como "explosão", "fogo", etc.

    Attributes
    ----------
    reloading : bool
        Um valor booleano que indica se a arma está recarregando.
    ammo : Ammo
        O número de munições restantes na arma.
    attack_field : pg.Rect
        A área onde a arma pode afetar alvos, representada como um retângulo.
    """
    def __init__(self, x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity, is_static, damage, kind_damage, attack_field, reload_time, ammo, scope, special_effect = None):
        # TODO tirar dano de personagens
        """
        Inicializa uma nova instância de `Weapon` com as propriedades fornecidas, incluindo dano, tipo de dano, campo de ataque,
        tempo de recarga, munição e efeito especial. A arma também herda as propriedades e comportamentos de `GameObject`.

        Parameters
        ----------
        x_position : float
            A posição inicial da arma no eixo X.
        y_position : float
            A posição inicial da arma no eixo Y.
        width : int
            A largura da imagem da arma.
        height : int
            A altura da imagem da arma.
        map_limits_sup : tuple
            Limite superior do mapa para restrição de movimento.
        spritesheet : str
            O caminho para o arquivo de spritesheet que contém as animações da arma.
        sprite_actual_x : int
            O índice inicial da sprite no eixo X.
        sprite_actual_y : int
            O índice inicial da sprite no eixo Y.
        sprites_quantity : int
            A quantidade total de sprites no eixo X do spritesheet.
        is_static : bool
            Um valor booleano que indica se a arma é estática ou não.
        damage : int
            O dano que a arma causa ao atingir um alvo.
        kind_damage : str
            O tipo de dano que a arma causa (ex.: "físico", "mágico", etc.).
        attack_field : int
            O tamanho do campo de ataque da arma, determinando a área ao redor da posição da arma onde ela pode afetar alvos.
        reload_time : int
            O tempo necessário para recarregar a arma.
        ammo : Ammo
            A munição que a arma utiliza para disparos.
        scope : float
            O alcance da arma, ou a distância máxima que ela pode atingir.
        special_effect : str, optional
            Um efeito especial que a arma pode ter, como "explosão", "fogo", etc.
        """
        super().__init__(x_position, y_position, width, height, map_limits_sup, spritesheet, sprite_actual_x, sprite_actual_y, sprites_quantity, is_static)
        self.damage = damage
        self.kind_damage = kind_damage
        self.special_effect = special_effect
        self.attack_field = pg.Rect(x_position - attack_field, y_position - attack_field, 2*attack_field, 2*attack_field)
        self.reload = reload_time
        self.reload_time = reload_time
        self._reloading = False
        self._ammo = ammo
        self.scope = scope
    
    @property
    def reloading(self):
        """
        Retorna se a arma está atualmente no processo de recarga.

        Returns
        -------
        bool
            True se a arma estiver recarregando, False caso contrário.
        """
        return self._reloading
    
    @reloading.setter
    def reloading(self, new_reloading):
        """
        Define se a arma está ou não recarregando.

        Parameters
        ----------
        new_reloading : bool
            O novo estado de recarga da arma.
        """
        self._reloading = new_reloading
     
    @property
    def ammo(self):
        """
        Retorna o número de munições restantes na arma.

        Returns
        -------
        Ammo
            O número de munições restantes.
        """
        return self._ammo
    
    @ammo.setter
    def ammo(self, new_ammo):
        """
        Define o número de munições restantes na arma.

        Parameters
        ----------
        new_ammo : Ammo
            O novo número de munições restantes.
        """
        self._ammo = new_ammo
        
    def set_position_rect_attack(self, x_new, y_new):
        """
        Atualiza a posição do campo de ataque com as novas coordenadas.

        Parameters
        ----------
        x_new : float
            A nova posição X do campo de ataque.
        y_new : float
            A nova posição Y do campo de ataque.
        """
        self.attack_field.center = (x_new, y_new)
        
    def instanciate_bullet(self, direction):
        """
        Instancia uma nova munição e define sua direção e posição.

        Parameters
        ----------
        direction : np.array
            A direção para a qual a munição será disparada.

        Returns
        -------
        Ammo
            A nova munição instanciada com a direção fornecida.
        """
        bullet = self.ammo.copy()
        bullet.x_position = self.x_position
        bullet.y_position = self.y_position
        bullet.direction = direction
        return bullet
        
    def check_load(self):
        """
        Verifica se a arma terminou o processo de recarga.

        Returns
        -------
        bool
            True se o tempo de recarga for menor ou igual ao tempo necessário, False caso contrário.
        """
        if self.reload_time <= self.reload:
            return True
        return False
    
    def fire(self, direction: np.array) -> Ammo:
        """
        Dispara uma munição na direção especificada.

        Parameters
        ----------
        direction : np.array
            A direção na qual a munição será disparada.

        Returns
        -------
        Ammo
            Uma nova instância de munição disparada, ou None se a arma não estiver pronta para disparar.
        """
        fired = None
        # Condicoes do disparo
        if self.check_load():
            self.reload = 0
            self.reloading = True
            # Instancia uma nova municao, copia da municao dada
            fired = self.instanciate_bullet(direction)
            
        return fired
    
    def update(self):
        """
        Atualiza a arma, incluindo a posição do campo de ataque e o estado de recarga.

        Se a arma estiver recarregando, o tempo de recarga é incrementado, e ela para de recarregar quando o tempo necessário é atingido.
        """
        super().update()
        # Atualiza a zona de ataque
        self.set_position_rect_attack(*self.rect.center)
        
        # Recarrega caso o player solicite
        if self.reloading:
            self.reload += 1
            # Para de recarregar ao terminar
            if self.check_load():
                self.reloading = False