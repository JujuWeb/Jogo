import os
import pygame

from aparencia import LARGURA, ALTURA, AZUL, BRANCO, PRETO, CHAO, FONT_NAME, FONT_TUTORIAL, DIRETORIO_IMAGENS
pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Caos IFinito")

spritesheet = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "spritesheet.png")).convert_alpha()
img_menu = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "capa.png")).convert()

img_inicioI = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "floresta.png")).convert()
img_teclas_e = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "esquerda.png")).convert_alpha()
img_teclas_d = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "direita.png")).convert_alpha()
img_teclas_p = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "pulo.png")).convert_alpha()

img_inicioII = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "floresta(2).png")).convert()
img_virus = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "virus.png")).convert_alpha()
img_cobrama = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "cobramarela.png")).convert_alpha()
img_cobraz = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "cobrazul.png")).convert_alpha()

img_blocobaixo = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "blocobaixo.png")).convert_alpha()
img_blocoalto = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "blocoalto.png")).convert_alpha()

img_go = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "go.png")).convert_alpha()
img_dino = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "dino.png")).convert_alpha()