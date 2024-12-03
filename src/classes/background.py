import pygame as pg
from src.settings import SCREEN_DIMENSIONS, Fonts, FULL_HEART, HALF_HEART, EMPTY_HEART
import numpy as np


class Background(pg.sprite.Sprite):
    def __init__(self, screen, sprite, x_position, y_position, width, height, music, volume, sounds):
        super().__init__()
        self.screen = screen
        self.sprite = pg.image.load(sprite)
        self.sprite = pg.transform.scale(self.sprite, (width, height))
        self.position_controller = PositionController([width, height], SCREEN_DIMENSIONS[0], SCREEN_DIMENSIONS[1])
        self.x_position = x_position - SCREEN_DIMENSIONS[0]//2
        self.y_position = y_position - SCREEN_DIMENSIONS[1]//2
        self.width = width
        self.height = height
        self.music = music
        self.volume = volume
        self.sounds = sounds
        self.image = self.sprite.subsurface((self.x_position, self.y_position, *SCREEN_DIMENSIONS))
        self.rect = self.image.get_rect()
        pg.mixer.music.load(self.music)
        pg.mixer.music.set_volume(self.volume)
        
        # Limites, ate aonde a camera vai
        self.x_limit_sup = self.width - SCREEN_DIMENSIONS[0]
        self.y_limit_sup = self.height - SCREEN_DIMENSIONS[1]
        
    def get_origin(self):
        return self.x_position+SCREEN_DIMENSIONS[0], self.y_position+SCREEN_DIMENSIONS[1]  
    
    def get_shape(self):
        return self.width, self.height
    
    def get_position(self):
        return self.x_position, self.y_position
        
    def set_position(self, x_new, y_new):
        self.x_position = x_new
        self.y_position = y_new
        
    def center(self, x_player, y_player):
        # Centraliza a camera no personagem
        x_new, y_new = self.position_controller.to_frame(x_player, y_player)
        x_new -= SCREEN_DIMENSIONS[0]/2
        y_new -= SCREEN_DIMENSIONS[1]/2
        self.set_position(x_new, y_new)
        self.image = self.sprite.subsurface((*self.get_position(), *SCREEN_DIMENSIONS))
        
    def play_music(self):
        pg.mixer.music.play(-1)
        
    def set_volume(self, volume):
        self.volume = volume
        pg.mixer.music.set_volume(self.volume)
    
    def draw_background_image(self):
        self.screen.blit(self.image, self.rect)
    
    def update(self, x_player, y_player):
        self.center(x_player, y_player)
        self.position_controller.set_origin(*self.get_position())
        self.draw_background_image()
        

class Interface():
    def __init__(self, screen, phase_atual, interface_elements):
        self.screen = screen
        self.phase_atual = phase_atual
        self.interface_elements = interface_elements
        self.player_name = Fonts.PLAYER_NAME.value.render('Player :'+str(self.phase_atual.player.name), True, (123, 173, 123))
        # self.player_life = Fonts.PLAYER_LIFE.value.render('Life: '+str(self.phase_atual.player.life), True, (123, 173, 223))
        self.event_warning =  Fonts.EVENT_WARNING.value.render('Volte para a Zona!', True, (255, 255, 255))
        # self.event_time = Fonts.EVENT_TIME.value.render('Time: '+str(self.phase_atual.current_mandatory_event.time), True, (123, 173, 223))
        
        #  Localizações
        self.player_name_location = (50, 50)
        # self.player_life_location = (300, 50)
        self.event_warning_location = ((SCREEN_DIMENSIONS[0]*2)//5, 100)
        self.event_time_location = (SCREEN_DIMENSIONS[0]//2-50, 50)
        
        self.full_heart_image = pg.image.load(FULL_HEART)
        self.full_heart_image = pg.transform.scale(self.full_heart_image, (50, 50)) 
        self.empty_heart_image = pg.image.load(EMPTY_HEART)
        self.empty_heart_image = pg.transform.scale(self.empty_heart_image, (50, 50)) 
        self.half_heart_image = pg.image.load(HALF_HEART)
        self.half_heart_image = pg.transform.scale(self.half_heart_image, (50, 50))
        
        
        self.heart_location = (50, 100)  # Local inicial para os corações

        # Coração
        
    def set_phase_atual(self, new_phase):
        self.phase_atual = new_phase
        
    def draw_interface(self):
        # Desenha os atributos do player no canto superior esquerdo
        self.screen.blit(self.player_name, self.player_name_location)
        # self.screen.blit(self.player_life, self.player_life_location)
        
                # Desenha a quantidade de vidas como corações
        for num in range(1, 6):
            x = self.heart_location[0] + (num-1) * 60  # Espaçamento entre corações
            y = self.heart_location[1]
            if num <=self.phase_atual.player.life:
                self.screen.blit(self.full_heart_image, (x, y))
            elif num-1 < self.phase_atual.player.life  and self.phase_atual.player.life < num:
                self.screen.blit(self.half_heart_image, (x,y))
            elif num >self.phase_atual.player.life:
                self.screen.blit(self.empty_heart_image, (x,y))      
        
        # for i in range(int(self.phase_atual.player.life)):
        #     x = self.heart_location[0] + i * 60  # Espaçamento entre corações
        #     y = self.heart_location[1]
        #     self.screen.blit(self.full_heart_image, (x, y))
        

        
        # Desenha avisos e informacoes da phase no centro superior da tela
        if self.phase_atual.collide_controller.current_mandatory_event:
            if self.phase_atual.collide_controller.current_mandatory_event.in_execution:
                if self.phase_atual.collide_controller.current_mandatory_event.out_zone:
                    self.screen.blit(self.event_warning, self.event_warning_location)
                # self.event_time = self.phase_atual.current_mandatory_event.time
                # self.event_time = Fonts.EVENT_TIME.value.render('Time: '+str(self.event_time), True, (123, 173, 223))
                # self.screen.blit(self.event_time, self.event_time_location)
        
        # Desenha o minimapa e as configuracoes no canto superior direito
        
    def update(self):
        self.player_life = Fonts.PLAYER_LIFE.value.render('Life: '+str(int(self.phase_atual.player.life)), True, (123, 173, 223))
        self.draw_interface()
    
class PositionController:
    x_origin = 0
    y_origin = 0
    def __init__(self, map_limits_sup, width, height):
        self.map_limits_inf = [width/2, height/2]
        self.map_limits_sup = map_limits_sup.copy()
        self.map_limits_sup[0] -= width/2
        self.map_limits_sup[1] -= height/2
        self.map = pg.Rect(*self.map_limits_inf, *self.map_limits_sup)
        
    @classmethod
    def set_origin(cls, x_new, y_new):
        cls.x_origin = x_new
        cls.y_origin = y_new  

    @staticmethod
    def normalize_movement(movement, speed):
        norma = np.linalg.norm(movement)
        if norma:
            movement /= norma
        movement *= speed
        return movement
    
    def to_frame(self, x_position, y_position):
        # Enquadra objeto para que ele nao ultrapasse nenhum limite do mapa
        if x_position < self.map_limits_inf[0]:
            x_position = self.map_limits_inf[0]
        elif x_position > self.map_limits_sup[0]:
            x_position = self.map_limits_sup[0]
            
        if y_position < self.map_limits_inf[1]:
            y_position = self.map_limits_inf[1]
        if y_position > self.map_limits_sup[1]:
            y_position = self.map_limits_sup[1]
        
        return x_position, y_position
    
    def out_game(self, object):
        if not self.map.contains(object.rect):
            object.kill()
    
    def apply_translation(self, x_position, y_position):
        # Aplica uma translacao no plano, considerando o sistema de coordenadas na qual o jogo sera desenhado
        x_new = x_position - self.x_origin
        y_new = y_position - self.y_origin
        return x_new, y_new
    
    
class CollideController:
    @staticmethod
    def locate_collide(sprite_1: pg.sprite.Sprite, sprite_2: pg.sprite.Sprite) -> np.array:
        """ Identifica a posicao relativa da sprite_2 em relacao a sprite 1.

        Args:
            sprite_1 (pg.sprite.Sprite): Sprite de interesse.
            sprite_2 (pg.sprite.Sprite): Sprite tomada como referencial.

        Returns:
            np.array: Array de entradas 0 caso esteja no sentido negativo do eixo, 1 caso positivo
        """
        # Toma os centros das sprites
        center_1 = np.array([sprite_1.x_position, sprite_1.y_position])
        center_2 = np.array([sprite_2.x_position, sprite_2.y_position])
        distance = center_2 - center_1
        abs_distance = np.absolute(distance)
        abs_movement = np.absolute(sprite_1.movement)
        min_distance = np.array([sprite_1.width+sprite_2.width, sprite_1.height+sprite_2.height])/2
        print(f'D: {distance}, Abs: {abs_distance}\nMin: {min_distance} - Abs_movement: {abs_movement}')
        
        min_distance -= abs_distance
        
        # Avalia se eles colidem nos eixos
        # collide = abs_distance - min_distance
        # print(f'C: {collide}')
        # collide = collide < 0
        # print(f'C pos: {collide}\n\n')
        
        # Angulo entre os vetores define em qual eixo foi a colisao
        e1 = np.array([1, 0])
        cos_movement = np.dot(e1, abs_movement)/np.linalg.norm(abs_movement)
        cos_min_distance = np.dot(e1, min_distance)/np.linalg.norm(min_distance)
        print(f'Cos_mov: {cos_movement}, cos_min: {cos_min_distance}')
        
        # Retira parte do movimento que causou a colisao
        collide_x_axis  = cos_movement > cos_min_distance
        abs_distance[abs_distance == 0] = 1 # Nao divir zero por zero, por favor
        signal = distance/abs_distance
        comeback = min_distance*np.array([collide_x_axis, not collide_x_axis])*signal
        return -comeback
            
    def __init__(self, player, npcs, villains, game_objects, collectibles, ammus, mandatory_events, optional_events, scooby_snacks, weapons, phase_elements):
        """ Classe que gerencia as colisoes entre os elementos da fase, atualizando os estados dos elementos que colidiram entre si.

        Args:
            player (Protagonist): Protagonista da fase.
            npcs (pg.sprite.Group): NPC's da fase.
            villains (pg.sprite.Group): Monstros da fase.
            game_objects (pg.sprite.Group): Objetos da fase.
            collectibles (pg.sprite.Group): Coletaveis da fase.
            ammus (pg.sprite.Group): Municoes disparadas na fase.
            mandatory_events (pg.sprite.Group): Eventos obrigatorios da fase.
            optional_events (pg.sprite.Group): Eventos opcionais da fase.
            scooby_snacks (Collectible): Caixa de biscoitos scooby da fase.
            weapons (pg.sprite.Group): Armas usadas na fase.
        """
        
        self.player = player
        self.npcs = npcs
        self.villains = villains
        self.game_objects = game_objects
        self.collectibles = collectibles
        self.ammus = ammus
        self.mandatory_events = mandatory_events
        self.current_mandatory_event = next(iter(self.mandatory_events), None)
        self.optional_events = optional_events
        self.scooby_snacks = scooby_snacks
        self.weapons = weapons
        self.phase_elements = phase_elements
        self.characters = pg.sprite.Group(self.villains)
        self.characters.add(self.npcs)
        self.characters.add(self.player)
        
        self.accessible_elements = pg.sprite.Group()
        for each_monster in self.villains.sprites():
            self.accessible_elements.add(each_monster.weapon)

        self.accessible_elements.add(self.villains)
        self.accessible_elements.add(self.npcs)
        self.accessible_elements.add(self.game_objects)
        self.accessible_elements.add(self.collectibles)
        self.accessible_elements.add(self.current_mandatory_event)
        self.accessible_elements.add(self.optional_events)
        
    def player_collide_with(self):
        """ Processa as colisoes do player com os elementos da fase.
        """
        # Atualizacao do evento obrigatorio atual
        if self.current_mandatory_event.started:
            if not self.current_mandatory_event.in_execution:
                self.current_mandatory_event.kill()
                self.current_mandatory_event = next(iter(self.mandatory_events), None)
                if self.current_mandatory_event:
                    self.accessible_elements.add(self.current_mandatory_event)
        if len(self.mandatory_events.sprites()) == 1:
            self.scooby_snacks.visible = True
            self.accessible_elements.add(self.scooby_snacks)
            
        # Atualizacao dos eventos opcionais
        for optional_event in self.optional_events.sprites():
            if optional_event.started and not optional_event.in_execution:
                optional_event.kill()
        
        # Colisao com coletaveis
        to_collectible = pg.sprite.spritecollide(self.player, self.collectibles, False)
        for each_collectible in to_collectible:
            if each_collectible.visible:
                # Adiciona ao inventario
                
                # Remove todas as referencias
                each_collectible.kill()
            
        # Colisao com npcs
        npcs_to_push = pg.sprite.spritecollide(self.player, self.npcs, False)
        for each_npc in npcs_to_push:
            comeback = -self.locate_collide(self.player, each_npc)
            comeback = each_npc.apply_movement(comeback)
            if comeback.any():
                self.player.apply_movement(comeback, False)
    
    def ammus_collide_with(self):
        # Colisao com personagens
        character_hit_by_ammu = pg.sprite.groupcollide(self.ammus, self.characters, False, False)
        for ammu  in self.ammus.sprites():
            for each_ammu in character_hit_by_ammu.keys():
                for each_character in character_hit_by_ammu[each_ammu]:
                    # Atinge o personagem
                    print('Dano longo\n')
                    each_character.life -= each_ammu.damage
                    # Remove todas as referencias
                    each_ammu.kill()

        # Colisao com objetos
        destroyed_ammus = pg.sprite.groupcollide(self.ammus, self.game_objects, False, False).keys()
        for each_ammu in destroyed_ammus:
            each_ammu.kill()
        
    
    def game_objects_collide_with(self):
        # Colisao com objetos (empurra-os, caso consiga)
        object_pushed_by_character = pg.sprite.groupcollide(self.characters, self.game_objects, False, False)
        for each_character in object_pushed_by_character.keys():
            for each_object in object_pushed_by_character[each_character]:
                if each_object.is_static:
                    comeback = self.locate_collide(each_character, each_object)
                    comeback = each_character.apply_movement(comeback, False)
                    if comeback.any():
                        _ = each_object.apply_movement(comeback)
                    
                else:
                    comeback = each_object.apply_movement(each_character.movement)
                    if comeback.any():
                        _ = each_character.apply_movement(comeback, False)
    
    def monsters_collide_with(self):
        fired = []
        # Colisao com algum personagem
        characters_to_push = pg.sprite.groupcollide(self.villains, self.characters, False, False)
        for each_villain in characters_to_push.keys():
            for each_character in characters_to_push[each_villain]:
                # Nao se empurra
                if each_villain != each_character and each_villain.movement.any():
                    comeback = -self.locate_collide(each_villain, each_character)
                    comeback = each_character.apply_movement(comeback)
                    if comeback.any():
                        _ = each_villain.apply_movement(comeback, False)
        
        # Atira no personagem caso ele esteja na mira e tenha recarregado
        for each_villain in self.villains.sprites():
            if each_villain.aim.any():
                if self.player.rect.clipline(each_villain.weapon.rect.center, np.array(each_villain.weapon.rect.center) + each_villain.aim*each_villain.weapon.scope/np.linalg.norm(each_villain.aim)) and each_villain.weapon.check_load():
                    print('pow')
                    bullet = each_villain.weapon.fire(each_villain.aim)
                    fired.append(bullet)
                    
        self.accessible_elements.add(fired)
        self.ammus.add(fired)
        
        return fired
    
    def npcs_collide_with(self):
        # npcs empurram uns aos outros
        npcs_pushed_by_npcs = pg.sprite.groupcollide(self.npcs, self.npcs, False, False)
        for each_npc1 in npcs_pushed_by_npcs.keys():
            for each_npc2 in npcs_pushed_by_npcs[each_npc1]:
                # Nao se empurram
                if each_npc1 != each_npc2 and each_npc1.movement.any():
                    # Separa o npc2 do npc1
                    comeback = -self.locate_collide(each_npc1, each_npc2)
                    comeback = each_npc2.apply_movement(comeback)
                    if comeback.any():
                        _ = each_npc1.apply_movement(comeback)
                        
                    # Nao precisa tratar a mesma colisao depois
                    npcs_pushed_by_npcs[each_npc2].remove(each_npc1)
    
    
    def update(self, phase_elements):
        fired = []
        self.player_collide_with()
        self.ammus_collide_with()
        self.game_objects_collide_with()
        fired_by_villains = self.monsters_collide_with()
        self.npcs_collide_with()
        fired.extend(fired_by_villains)
        
        if fired:
            phase_elements.add(fired)
        
        """
        Colisoes:
        player - monstro (atacado)
        player - coletavel (coleta)
        player - game object (empurra)
        player - npcs (para)
        player - event (inicia)
        player - ammu (destroi ou recocheteia)
        
        monstro - player
        monstro - ammu (destroi ou recocheteia)
        monstro - game object (empurra)
        
        npc - player ou game object (empurra)
        """