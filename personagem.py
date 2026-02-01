import pygame
from aparencia import CHAO

class Personagem(pygame.sprite.Sprite):
    def __init__(self, spritesheet):
        super().__init__()
        self.andar_direita = []
        self.andar_esquerda = []
        self.anim_morte = []

        # Animação direita
        for i in range(4):
            img = spritesheet.subsurface((i * 85, 0), (85, 95))
            img = pygame.transform.scale(img, (85, 95))
            self.andar_direita.append(img)

        # Animação esquerda
        for i in range(4, 8):
            img = spritesheet.subsurface((i * 85, 0), (85, 95))
            img = pygame.transform.scale(img, (85, 95))
            self.andar_esquerda.append(img)

        # Animação morte
        for i in range(5, 8):
            img = spritesheet.subsurface((i * 85, 2 * 95), (85, 95))
            img = pygame.transform.scale(img, (85, 95))
            self.anim_morte.append(img)

        self.index_lista = 0
        self.image = self.andar_direita[0]
        self.rect = self.image.get_rect()
        self.rect.center = (90, 381)
        self.vel_y = 0
        self.vel_x = 0
        self.pulando = False
        self.direcao = "direita"
        self.morrendo = False
        self.morto = False
        self.na_plataforma = False

    def update(self):
        if self.morrendo:
            self.vel_y += 1
            self.rect.y += self.vel_y
            if self.rect.bottom >= CHAO + 47:
                self.rect.bottom = CHAO + 47
                self.vel_y = 0
            if not self.morto:
                self.index_lista += 0.10
                if int(self.index_lista) >= len(self.anim_morte):
                    self.index_lista = len(self.anim_morte) - 1
                    self.morto = True
                self.image = self.anim_morte[int(self.index_lista)]
            return

        # Animação andando
        if self.vel_x > 0:
            self.direcao = "direita"
            self.index_lista += 0.25
            if self.index_lista >= len(self.andar_direita):
                self.index_lista = 0
            self.image = self.andar_direita[int(self.index_lista)]

        elif self.vel_x < 0:
            self.direcao = "esquerda"
            self.index_lista += 0.25
            if self.index_lista >= len(self.andar_esquerda):
                self.index_lista = 0
            self.image = self.andar_esquerda[int(self.index_lista)]
        else:
            self.image = self.andar_direita[0] if self.direcao == "direita" else self.andar_esquerda[0]

        # Movimento horizontal
        self.rect.x += self.vel_x
        if self.rect.left < 0:
            self.rect.left = 0

        # Gravidade só se não estiver em plataforma
        if not self.na_plataforma:
            self.vel_y += 1
            self.rect.y += self.vel_y
        else:
            self.vel_y = 0

        # Checa chão
        if not self.na_plataforma and self.rect.bottom >= CHAO + 47:
            self.rect.bottom = CHAO + 47
            if self.vel_y > 0:
                self.vel_y = 0
                self.pulando = False

    def pular(self):
        if not self.pulando and not self.morrendo:
            self.vel_y = -20
            self.pulando = True
            self.na_plataforma = False  # sai da plataforma ao pular

    def morrer(self):
        if not self.morrendo:
            self.morrendo = True
            self.index_lista = 0