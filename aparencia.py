import os
import pygame

LARGURA = 960
ALTURA = 540
AZUL = (135, 206, 235)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CHAO = 385

pygame.font.init()
FONT_NAME = pygame.font.match_font('mono')
FONT_TUTORIAL = pygame.font.match_font('arial')
DIRETORIO_PRINCIPAL = os.path.dirname(__file__)
DIRETORIO_IMAGENS = os.path.join(DIRETORIO_PRINCIPAL, "sprite")
