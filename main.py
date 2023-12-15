from random import choice
from time import sleep
from Menu import *
from Objects import *

pygame.init()

screen_width, screen_height = 1000, 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Spacewalker: Zero-G Odyssey')

# define game variables
tile_size = 50
clock = pygame.time.Clock()
game_over = False
run = True

# load
bg_img = pygame.image.load('img/map_1/background.png')

pygame.mixer.music.load("soundtrack/Spacewalker OST.wav")

pygame.mixer.music.set_volume(0.2)

pygame.mixer.music.play(-1)


def menu_game_win():
    menu_options = ["YES", "NO"]
    menu = Menu(menu_options)
    pygame.mixer.music.stop()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            selected_option = menu.handle_event(event)
            if selected_option:

                if selected_option == "YES":
                    pygame.mixer.music.load("soundtrack/Spacewalker OST.wav")
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play(-1)
                    return 0

                elif selected_option == "NO":
                    pygame.quit()
                    quit()
        screen.fill((0, 0, 0))
        menu.draw(screen)

        font = pygame.font.SysFont('Futura', 50)
        text = font.render('PLAY AGAIN?', False, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, 2 * (screen_height // 5)))
        screen.blit(text, text_rect)

        pygame.display.update()


class World:
    def __init__(self, data):
        self.tile_list = []

        # load images
        stone_img = pygame.image.load('img/tiles/stone.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if isinstance(tile, int):
                    if tile == 1:
                        img = pygame.transform.scale(stone_img, (tile_size, tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        self.tile_list.append(tile)
                    if tile == 3:
                        lava = Lava(col_count * tile_size, row_count * tile_size)
                        lava_group.add(lava)
                    if tile == 4:
                        won = Flag(col_count * tile_size, row_count * tile_size)
                        flag_group.add(won)
                    if tile == 5:
                        friend = Friend(col_count * tile_size, row_count * tile_size)
                        friend_group.add(friend)
                else:
                    alien = Enemy(col_count * tile_size, row_count * tile_size + 10, tile[1], choice([1, -1]), tile[2],
                                  tile[0])
                    alien_group.add(alien)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 1)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, velocity_scale, axis_movement_type, alien_type, ):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        if alien_type == 'G':
            self.image = pygame.image.load('img/enemies/green_alien.png')
            self.image = pygame.transform.scale(self.image, (40, 40))
        elif alien_type == 'Y':
            self.image = pygame.image.load('img/enemies/yellow_alien.png')
            self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_scale = velocity_scale
        self.axis_movement = axis_movement_type

    def update(self):
        deslocamento = self.vel_scale * self.direction
        if self.axis_movement == 'x':
            # Detectar colisão
            for tile in world.tile_list:
                # Checar colisão na direção x
                if tile[1].colliderect(self.rect.x + deslocamento, self.rect.y, self.rect.width, self.rect.height):
                    self.direction *= -1
                    deslocamento = 0
            # Checar colisão com a borda da tela
            if self.rect.left + deslocamento < 0 or self.rect.right + deslocamento > screen_width:
                self.direction *= -1
                deslocamento = 0
            # Atualizar as coordenadas do alien
            self.rect.x += deslocamento
        else:
            # Detectar colisão
            for tile in world.tile_list:
                # Checar colisão na direção y
                if tile[1].colliderect(self.rect.x, self.rect.y + deslocamento, self.rect.width, self.rect.height):
                    self.direction *= -1
                    deslocamento = 0

            # Checar colisão com a borda da tela
            if self.rect.top + deslocamento < 0 or self.rect.bottom + deslocamento > screen_height:
                self.direction *= -1
                deslocamento = 0
            # Atualizar as coordenadas do alien
            self.rect.y += deslocamento

        # Desenhar o alien
        screen.blit(self.image, self.rect)


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y, ):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/tiles/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y, ):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/tiles/flag.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Friend(pygame.sprite.Sprite):
    def __init__(self, x, y, ):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/characters/friends/friend_1.png')
        self.image = pygame.transform.scale(img, (tile_size, 2 * tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - tile_size


class Player:
    def __init__(self, x, y):
        # --->carregar imagens do jogador normal
        self.player_idle_right = pygame.image.load('img/characters/player_idle_right.png')
        self.player_idle_left = pygame.image.load('img/characters/player_idle_left.png')

        # Redimensionar imagens do jogador
        self.player_idle_right = pygame.transform.scale(self.player_idle_right, (tile_size, 2 * tile_size))
        self.player_idle_left = pygame.transform.scale(self.player_idle_left, (tile_size, 2 * tile_size))
        self.frames_right = []  # Lista de quadros da animação
        self.frames_left = []  # Lista de quadros da animação
        self.animation_speed = 10  # Ajuste isso para controlar a velocidade da animação
        self.frame_count = 0
        # Recortar os quadros da imagem
        for i in range(8):
            frame = pygame.image.load(f'img/characters/player_run_right/player_run_right_{i}.png')
            frame = pygame.transform.scale(frame, (tile_size, 2 * tile_size))
            self.frames_right.append(frame)
        for i in range(8):
            frame = pygame.image.load(f'img/characters/player_run_left/player_run_left_{i}.png')
            frame = pygame.transform.scale(frame, (tile_size, 2 * tile_size))
            self.frames_left.append(frame)

        # --->carregar imagens do jogador flipado
        self.player_idle_right_flip = pygame.image.load('img/characters/fliped_player/player_idle_right.png')
        self.player_idle_left_flip = pygame.image.load('img/characters/fliped_player/player_idle_left.png')

        # Redimensionar imagens do jogador flipado
        self.player_idle_right_flip = pygame.transform.scale(self.player_idle_right_flip, (tile_size, 2 * tile_size))
        self.player_idle_left_flip = pygame.transform.scale(self.player_idle_left_flip, (tile_size, 2 * tile_size))
        self.frames_right_flip = []  # Lista de quadros da animação
        self.frames_left_flip = []  # Lista de quadros da animação
        # Recortar os quadros da imagem
        for i in range(8):
            frame = pygame.image.load(f'img/characters/fliped_player/player_run_right/player_run_right_{i}.png')
            frame = pygame.transform.scale(frame, (tile_size, 2 * tile_size))
            self.frames_right_flip.append(frame)
        for i in range(8):
            frame = pygame.image.load(f'img/characters/fliped_player/player_run_left/player_run_left_{i}.png')
            frame = pygame.transform.scale(frame, (tile_size, 2 * tile_size))
            self.frames_left_flip.append(frame)
        # Imagem atual do jogador
        self.player = self.player_idle_right
        # Índice do quadro atual
        self.frame_index = 0
        self.image = self.player
        # Retângulo de colisão do jogador
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        # Ponto de spawn
        self.spawn_X, self.spawn_Y = worlds[current_world][1][0], worlds[current_world][1][1]
        self.vel_y = 0
        self.on_ground = False
        self.direction = 1  # 1 = direita, -1 = esquerda
        self.flip = -1  # -1 = não, 1 = sim
        self.q_key_pressed = False  # Adiciona um atributo para rastrear se a tecla 'q' está sendo pressionada
        self.friend_saved = False
        # parado quando nasce
        self.timer = 0
        self.can_move = False

    def update(self):
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        # Verificar se o jogador pode se mover após a morte
        if self.can_move:
            # Obter pressionamentos de tecla
            if key[pygame.K_SPACE] and self.on_ground:
                self.vel_y = 15 * self.flip
                self.on_ground = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.direction = 1

            # Verificar se a tecla 'q' foi pressionada
            if key[pygame.K_q] and not self.q_key_pressed:
                self.q_key_pressed = True
                self.vel_y = 0
                self.flip *= -1
            elif not key[pygame.K_q]:
                self.q_key_pressed = False

        # add gravity
        if self.flip == 1:
            self.vel_y -= 1
            if self.vel_y < -10:
                self.vel_y = -10
            dy += self.vel_y
        else:
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

        # Alternar entre imagens de movimento e imagem de repouso
        if self.flip == -1:
            if dx > 0:  # O jogador está se movendo para a direita
                self.frame_count += 1
                if self.frame_count >= self.animation_speed:
                    self.frame_index = (self.frame_index + 1) % len(self.frames_right)
                    self.image = self.frames_right[self.frame_index]
                    self.frame_count = 0  # Redefine o contador de quadros
            elif dx < 0:  # O jogador está se movendo para a esquerda
                self.frame_count += 1
                if self.frame_count >= self.animation_speed:
                    self.frame_index = (self.frame_index + 1) % len(self.frames_left)
                    self.image = self.frames_left[self.frame_index]
                    self.frame_count = 0
            else:  # O jogador não está se movendo
                if self.direction == 1:
                    self.image = self.player_idle_right
                else:
                    self.image = self.player_idle_left
        else:
            if dx > 0:
                self.frame_count += 1
                if self.frame_count >= self.animation_speed:
                    self.frame_index = (self.frame_index + 1) % len(self.frames_right_flip)
                    self.image = self.frames_right_flip[self.frame_index]
                    self.frame_count = 0
            elif dx < 0:
                self.frame_count += 1
                if self.frame_count >= self.animation_speed:
                    self.frame_index = (self.frame_index + 1) % len(self.frames_left_flip)
                    self.image = self.frames_left_flip[self.frame_index]
                    self.frame_count = 0
            else:
                if self.direction == 1:
                    self.image = self.player_idle_right_flip
                else:
                    self.image = self.player_idle_left_flip

        # Detectar colisão
        for tile in world.tile_list:
            # Checar colisão na direção x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            if self.flip == -1:
                # Checar colisão na direção y
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                    # Checa se está colidindo por baixo do solo (pulando)
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # Checa se está colidindo por cima do solo (caindo)
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.on_ground = True
            else:
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width - 1, self.rect.height - 1):
                    if self.vel_y >= 0:
                        self.rect.y = tile[1].top - self.rect.height
                        dy = 0
                        self.vel_y = 0
                    elif self.vel_y < 0:
                        self.rect.y = tile[1].bottom
                        dy = 0
                        self.vel_y = 0
                        self.on_ground = True

        # Checar colisão com a borda da tela
        if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
            dx = 0
        if self.rect.top + dy < 0 or self.rect.bottom + dy > screen_height:
            dy = 0
        # Chechar colisão com inimigos
        if pygame.sprite.spritecollide(self, alien_group, False) or pygame.sprite.spritecollide(self, lava_group,
                                                                                                False):
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont('Futura', 30)
            text = font.render('YOU DIED', False, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text, text_rect)
            pygame.display.update()
            sleep(1)
            return 1  # lose

        # Checar colisão com o amigo
        if pygame.sprite.spritecollide(self, friend_group, False) and not self.friend_saved:
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont('Futura', 30)
            text = font.render('FRIEND SAVED', False, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text, text_rect)
            pygame.display.update()
            self.friend_saved = True
            sleep(1)

        if pygame.sprite.spritecollide(self, flag_group, False) and self.friend_saved:
            screen.fill((0, 0, 0))
            font = pygame.font.SysFont('Futura', 30)
            text = font.render('STAGE FINISHED', False, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text, text_rect)
            pygame.display.update()
            sleep(1)
            return 0  # win

        # Atualizar as coordenadas do jogador
        self.rect.x += dx
        self.rect.y += dy

        # Desenhar o jogador na tela
        screen.blit(self.image, self.rect)

        if self.timer >= 120:
            self.can_move = True  # Impedir movimento após a morte
        self.timer += 2

    def reset_game(self, x=None, y=None):
        if x is None:
            x = self.spawn_X
        if y is None:
            y = self.spawn_Y

        self.spawn_X = x
        self.spawn_Y = y

        self.rect.x = self.spawn_X
        self.rect.y = self.spawn_Y
        self.vel_y = 0
        self.on_ground = True
        self.direction = 1
        self.flip = -1
        self.q_key_pressed = False
        self.friend_saved = False
        self.timer = 0
        self.can_move = False


# Adicione a chamada para mostrar o menu antes do loop principal do jogo
selected_option = show_menu(screen)

world_1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 3, 3, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, ['G', 4, 'x'], 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 5, 1],
    [1, 0, 0, 1, 1, 1, 3, 3, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, ['G', 4, 'x'], 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, ['G', 3, 'x'], 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [['G', 2, 'y'], 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 3, 3, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, ['G', 3, 'y'], 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 1, 1, 1, ['G', 4, 'y'], 1, 3, 3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
world_2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 3, 3, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [['Y', 4, 'x'], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 1, 1, 0, 0],
    [['Y', 4, 'x'], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [['Y', 4, 'x'], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ['Y', 2, 'x']],
    [3, 1, 1, 3, 3, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ['G', 2, 'x'], 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
world_3 = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, ['G', 4, 'x'], 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 5, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, ['G', 4, 'x'], 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 3, 3, 3, 1, 0, 0, 1, ['Y', 3, 'y'], 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, ['Y', 4, 'x'], 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
    [1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
world_4 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ["G", 4, 'x'], 1],
    [1, ["G", 4, 'x'], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ["Y", 5, 'x'], 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, ["Y", 5, 'x'], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1]
]
world_5 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ["G", 4, 'y']],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 4, ["Y", 6, "x"], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ["G", 4, 'x'], 1, 0, 0, 0],
    [0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 3, 3, 3, 1, 1, 1, 3, 3, 3, 1, 3, 3, 3, 3],
    [1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1]
]
world_6 = [
    [1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, ["G", 5, "x"], 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, ["G", 6, "y"], 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, ["Y", 4, "x"], 1],
    [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [5, 0, 0, 0, 1, 0, 1, 3, 3, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 3, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, ["Y", 6, "x"], 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

alien_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
friend_group = pygame.sprite.Group()

worlds = [[world_1, (tile_size, screen_height - 2 * tile_size)], [world_2, (screen_width - tile_size, 3 * tile_size)],
          [world_3, (tile_size, screen_height - 2 * tile_size)], [world_4, (tile_size, screen_height - 2 * tile_size)],
          [world_5, (tile_size, screen_height - 2 * tile_size)],
          [world_6, (10 * tile_size, screen_height - 10 * tile_size)]]

current_world = 5
world = World(worlds[current_world][0])
player = Player(worlds[current_world][1][0], worlds[current_world][1][1])

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Voltar ao menu
                selected_option = show_menu(screen)
                if selected_option == "Quit":
                    run = False
                elif selected_option == "Start Game":
                    # Limpar os grupos antes de começar um novo jogo
                    alien_group.empty()
                    lava_group.empty()
                    flag_group.empty()
                    friend_group.empty()
                    world = World(worlds[current_world][0])
                    player.reset_game(worlds[current_world][1][0], worlds[current_world][1][1])

    screen.blit(bg_img, (0, 0))
    world.draw()
    alien_group.update()
    alien_group.draw(screen)
    lava_group.draw(screen)
    flag_group.draw(screen)
    if not player.friend_saved:
        friend_group.draw(screen)
    game_over = player.update()

    if game_over == 1:  # perdeu
        player.reset_game()
    elif game_over == 0:  # ganhou
        # Limpar os grupos antes de carregar um novo mapa
        alien_group.empty()
        lava_group.empty()
        flag_group.empty()
        friend_group.empty()
        if current_world + 1 < len(worlds):
            current_world += 1
        else:
            current_world = menu_game_win()

        world = World(worlds[current_world][0])
        player.reset_game(worlds[current_world][1][0], worlds[current_world][1][1])

    pygame.display.update()
