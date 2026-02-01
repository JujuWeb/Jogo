import pygame

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y, largura, altura, offset_top=0):
        super().__init__()

        # imagem (visual)
        self.image = pygame.transform.scale(imagem, (largura, altura))
        self.rect = self.image.get_rect(topleft=(x, y))

        # hitbox (colisão)
        self.hitbox = pygame.Rect(
            x,
            y + offset_top,
            largura,
            altura - offset_top
        )

        self.offset_top = offset_top