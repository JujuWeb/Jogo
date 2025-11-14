import pygame
from aparencia import PRETO

class Transicao:
    @staticmethod
    def fade_in(tela, troca, cor = PRETO, duracao=800):

        clock = pygame.time.Clock()
        fade = pygame.Surface((960, 540)).convert()
        fade.fill(cor)
        alpha = 255
        transparencia = 255 / 51

        while alpha > 0:
            tela.blit(troca, (0, 0))      
            fade.set_alpha((alpha))
            tela.blit(fade, (0, 0))       
            pygame.display.update()
            clock.tick(60)
            alpha -= transparencia