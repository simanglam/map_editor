import pygame

class BaseMapObject(pygame.sprite.Sprite):

    def __init__(self, position: tuple, image = None) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.surface.Surface((50, 50))

        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def update(self, shift):
        self.rect.x += shift

    def on_top(self, object):
        object.air = False
        object.direction.y = 0
        object.rect.bottom = self.rect.top

    def on_side(self, object):
        if object.direction.x > 0:
            object.rect.right = self.rect.left
        else:
            object.rect.left = self.rect.right

        object.direction.x = 0
        object.abs_speed = 0