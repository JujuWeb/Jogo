import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, imagem_fundo):
        super().__init__()
        self.image = imagem_fundo.subsurface((0, 0), (960, 575))
        self.image = pygame.transform.scale(self.image, (960, 540))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
