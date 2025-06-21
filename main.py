import pygame
from pygame.locals import *
from sys import exit
import os

from personagem import Personagem
from background import Background

pygame.init()

LARGURA = 960
ALTURA = 540
AZUL = (135, 206, 235)
CHAO = 385

diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, "sprite")

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo do IF")

spritesheet = pygame.image.load(os.path.join(diretorio_imagens, "spritesheet.png")).convert_alpha()
imagem_fundo = pygame.image.load(os.path.join(diretorio_imagens, "floresta.png"))

all_sprites = pygame.sprite.Group()
fundo = Background(imagem_fundo)
personagem = Personagem(spritesheet)

all_sprites.add(fundo)
all_sprites.add(personagem)

relogio = pygame.time.Clock()
morreu = False
font_name = pygame.font.match_font('arial')

while True:
    tela.fill(AZUL)
    relogio.tick(60)

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()

        elif evento.type == KEYDOWN:
            if evento.key == K_SPACE and not morreu:
                personagem.pular()
            elif evento.key == K_f and not morreu:
                personagem.morrer()
                morreu = True
            elif evento.key == K_r and morreu:
                personagem = Personagem(spritesheet)
                all_sprites = pygame.sprite.Group()
                all_sprites.add(fundo)
                all_sprites.add(personagem)
                morreu = False

    teclas = pygame.key.get_pressed()
    if not personagem.morrendo:
        if teclas[K_d]:
            personagem.vel_x = 5
        elif teclas[K_a]:
            personagem.vel_x = -5
        else:
            personagem.vel_x = 0

    all_sprites.update()
    all_sprites.draw(tela)

    if morreu:
        fonte_menor = pygame.font.Font(font_name, 60)
        texto1 = fonte_menor.render("Você morreu", True, (0, 0, 0))
        texto2 = fonte_menor.render("Pressione 'R' para reiniciar", True, (0, 0, 0))
        tela.blit(texto1, (LARGURA // 2 - texto1.get_width() // 2, ALTURA // 2 - 80))
        tela.blit(texto2, (LARGURA // 2 - texto2.get_width() // 2, ALTURA // 2))

    pygame.display.flip()
