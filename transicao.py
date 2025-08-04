import pygame
from aparencia import PRETO

class Transicao:
    @staticmethod
    def fade_in_from_black(tela, novo_cenario, cor = PRETO, duracao=800):
        clock = pygame.time.Clock()
        fade = pygame.Surface(tela.get_size()).convert()
        fade.fill(cor)
        alpha = 255
        decremento = 255 / (duracao / 16.67) 

        while alpha > 0:
            tela.blit(novo_cenario, (0, 0))      
            fade.set_alpha(int(alpha))
            tela.blit(fade, (0, 0))       
            pygame.display.update()
            clock.tick(60)
            alpha -= decremento