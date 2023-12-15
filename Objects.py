import pygame

tile_size = 50


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
