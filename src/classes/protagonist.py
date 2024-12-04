import pygame as pg
from abc import ABC, abstractmethod
from src.classes.character import Character


class Protagonist(Character, ABC):
    """
    Representa um personagem protagonista no jogo, herdando de `Character` e implementando comportamentos específicos 
    para o protagonista, como controle de vida, inventário e habilidade.

    Atributos:
        life (int): A quantidade de vida do protagonista.
        inventory (list): O inventário do protagonista, contendo itens que ele possui.
        ability (str): A habilidade especial do protagonista.
        name (str): Nome do protagonista.
        speed (int): Velocidade do protagonista.
        perception (int): Percepção do protagonista.
        x_position (float): Posição horizontal do protagonista no mapa.
        y_position (float): Posição vertical do protagonista no mapa.
        width (int): Largura do protagonista.
        height (int): Altura do protagonista.
        direction (str): Direção para a qual o protagonista está voltado.
        skin (str): Identificador da skin do protagonista.
        sprites_quantity (int): Quantidade de sprites associadas ao protagonista.
        map_limits_sup (tuple): Limites superiores do mapa em que o protagonista pode se mover.
        bullets (int): Quantidade de balas que o protagonista possui.
        weapon (Weapon): A arma que o protagonista usa.

    Métodos:
        update: Método abstrato para atualizar o estado do protagonista.
        check_objective: Verifica o objetivo do protagonista.
        check_ability: Verifica a habilidade especial do protagonista.
    """
    def __init__(self, name, speed, perception, x_position, y_position, width, height, direction, skin,
                 life, inventory, ability, sprites_quantity, map_limits_sup, bullets, weapon):
        """
        Inicializa um objeto do tipo Protagonist.

        Parâmetros:
            name (str): Nome do protagonista.
            speed (int): Velocidade do protagonista.
            perception (int): Percepção do protagonista.
            x_position (float): Posição horizontal do protagonista no mapa.
            y_position (float): Posição vertical do protagonista no mapa.
            width (int): Largura do protagonista.
            height (int): Altura do protagonista.
            direction (str): Direção para a qual o protagonista está voltado.
            skin (str): Identificador da skin do protagonista.
            life (int): Quantidade de vida do protagonista.
            inventory (list): O inventário do protagonista.
            ability (str): A habilidade especial do protagonista.
            sprites_quantity (int): Quantidade de sprites associadas ao protagonista.
            map_limits_sup (tuple): Limites superiores do mapa.
            bullets (int): Quantidade de balas que o protagonista possui.
            weapon (Weapon): A arma que o protagonista usa.
        """        
        super().__init__(name, speed, perception, x_position, y_position, width, height, direction, skin, life, sprites_quantity, map_limits_sup, bullets, weapon)
        self._inventory = inventory
        self._ability = ability

    @property
    def life(self):
        """
        Retorna a quantidade de vida do protagonista.

        Retorno:
            float: A quantidade de vida do protagonista.
        """
        return self._life

    @life.setter
    def life(self, value):
        """
        Define a quantidade de vida do protagonista.

        Parâmetros:
            value (float): O novo valor de vida do protagonista.
        """
        self._life = value

    @property
    def inventory(self):
        """
        Retorna o inventário do protagonista.

        Retorno:
            list: O inventário do protagonista.
        """
        return self._inventory

    @inventory.setter
    def inventory(self, value):
        """
        Define o inventário do protagonista.

        Parâmetros:
            value (list): O novo inventário do protagonista.
        """
        self._inventory = value

    @property
    def ability(self):
        """
        Retorna a habilidade especial do protagonista.

        Retorno:
            str: A habilidade especial do protagonista.
        """
        return self._ability

    @ability.setter
    def ability(self, value):
        """
        Define a habilidade especial do protagonista.

        Parâmetros:
            value (str): A nova habilidade especial do protagonista.
        """
        self._ability = value

    @abstractmethod
    def update(self):
        """
        Método abstrato para atualizar o estado do protagonista. Deve ser implementado pelas subclasses.

        Este método será responsável por aplicar as atualizações necessárias no estado do protagonista.
        """
        pass
    
    def check_objective(self):
        """
        Verifica o objetivo do protagonista.

        Este método pode ser usado para verificar se o protagonista alcançou seu objetivo ou status no jogo.
        """
        print("Checking objective...")

    def check_ability(self):
        """
        Verifica a habilidade especial do protagonista.

        Este método pode ser usado para verificar o status ou o uso de uma habilidade especial do protagonista.
        """
        print("Checking ability...")

class Group1Protagonist(Protagonist):
    """
    Representa um tipo específico de protagonista (Group1Protagonist), herdando da classe `Protagonist`.
    Esta classe adiciona a habilidade de manipular armadilhas, além de gerenciar e atualizar o movimento e animações 
    do personagem no jogo.

    Atributos:
        trap_power (int): Poder das armadilhas do protagonista.
        damage (int): Quantidade de dano causado pelo protagonista.
        life (int): Quantidade de vida do protagonista.
        inventory (list): Inventário do protagonista.
        ability (str): Habilidade especial do protagonista.
        name (str): Nome do protagonista.
        speed (int): Velocidade do protagonista.
        perception (int): Percepção do protagonista.
        x_position (float): Posição horizontal do protagonista no mapa.
        y_position (float): Posição vertical do protagonista no mapa.
        width (int): Largura do protagonista.
        height (int): Altura do protagonista.
        direction (str): Direção para a qual o protagonista está voltado.
        skin (str): Identificador da skin do protagonista.
        sprites_quantity (int): Quantidade de sprites associadas ao protagonista.
        map_limits_sup (tuple): Limites superiores do mapa em que o protagonista pode se mover.
        bullets (int): Quantidade de balas que o protagonista possui.
        weapon (Weapon): A arma que o protagonista usa.

    Métodos:
        update: Atualiza a posição do protagonista e executa a animação.
        damage: Define e obtém o valor do dano causado pelo protagonista.
        trap_power: Define e obtém o poder das armadilhas do protagonista.
    """
    def __init__(self, name, speed, perception, x_position, y_position, width, height, direction, skin,
                 life, inventory, ability, sprites_quantity, map_limits_sup, bullets, weapon, trap_power):
        """
        Inicializa um objeto do tipo Group1Protagonist.

        Parâmetros:
            name (str): Nome do protagonista.
            speed (int): Velocidade do protagonista.
            perception (int): Percepção do protagonista.
            x_position (float): Posição horizontal do protagonista no mapa.
            y_position (float): Posição vertical do protagonista no mapa.
            width (int): Largura do protagonista.
            height (int): Altura do protagonista.
            direction (str): Direção para a qual o protagonista está voltado.
            skin (str): Identificador da skin do protagonista.
            life (int): Quantidade de vida do protagonista.
            inventory (list): O inventário do protagonista.
            ability (str): A habilidade especial do protagonista.
            sprites_quantity (int): Quantidade de sprites associadas ao protagonista.
            map_limits_sup (tuple): Limites superiores do mapa.
            bullets (int): Quantidade de balas que o protagonista possui.
            weapon (Weapon): A arma que o protagonista usa.
            trap_power (int): O poder das armadilhas do protagonista.
        """
        super().__init__(name, speed, perception, x_position, y_position, width, height, direction, skin, life, inventory, ability, sprites_quantity, map_limits_sup, bullets, weapon)
        self._trap_power = trap_power

    @property
    def damage(self):
        """
        Obtém o valor do dano causado pelo protagonista.

        Retorno:
            float: O valor do dano causado pelo protagonista.
        """
        return self._damage

    @damage.setter
    def damage(self, value):
        """
        Define o valor do dano causado pelo protagonista.

        Parâmetros:
            value (int): O novo valor do dano.
        """
        self._damage = value

    @property
    def trap_power(self):
        """
        Obtém o poder das armadilhas do protagonista.

        Retorno:
            int: O poder das armadilhas do protagonista.
        """
        return self._trap_power

    @trap_power.setter
    def trap_power(self, value):
        """
        Define o poder das armadilhas do protagonista.

        Parâmetros:
            value (int): O novo poder das armadilhas.
        """

        self._trap_power = value

    def update(self):
        """
        Atualiza a posição do protagonista com base nas movimentações e aplica a animação correspondente.

        Este método também calcula a nova posição e chama o método de animação do protagonista.
        """
        x_new, y_new = self.position_controller.apply_translation(self.x_position, self.y_position)
        self.set_position_rect(x_new, y_new)
        self.animate()


class Group2Protagonist(Protagonist):
    def __init__(self, name, speed, perception, x_position, y_position, width, height, direction, skin,
                 life, inventory, ability, sprites_quantity, map_limits_sup, bullets, weapon, deceive_power):
        super().__init__(name, speed, perception, x_position, y_position, width, height, direction, skin, life, inventory, ability, sprites_quantity, map_limits_sup, bullets, weapon)
        self._deceive_power = deceive_power

    @property
    def deceive_power(self):
        return self._deceive_power

    @deceive_power.setter
    def deceive_power(self, value):
        self._deceive_power = value

    def update(self):
        pass