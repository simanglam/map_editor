import pygame

class BaseMapObject(pygame.sprite.Sprite):

    def __init__(self, position: tuple ,image = None) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image)

        self.rect = self.image.get_rect()
        self.rect.width = self.image.get_width() / 50
        self.rect.height = self.image.get_height()/ 50
        self.rect.x, self.rect.y = position
        self.type = None

    def update(self, shift):
        self.rect.x += shift
    
    def set_type(self, _type):
        self.type = _type
        return self

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