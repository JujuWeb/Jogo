import pygame

INICIO = 0
JOGANDO = 1
MORTE = 2
VITORIA = 3


class Inicio:
    def __init__(self, tela_w, tela_h):
        self.estado = INICIO

        self.imagem = pygame.image.load("message1.png").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem,(184*2+50,2*267+50))
        self.rect = self.imagem.get_rect(center=(tela_w // 2, tela_h // 2 + 5))

    def desenhar(self, tela):
        if self.estado == INICIO:
            tela.blit(self.imagem, self.rect)
