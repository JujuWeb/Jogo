import pygame
from pygame.locals import *
from sys import exit
import os

from transicao import Transicao
from personagem import Personagem
from background import Background
from aparencia import LARGURA, ALTURA, AZUL, BRANCO, PRETO, CHAO, FONT_NAME, DIRETORIO_IMAGENS

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Caos IFinito")

spritesheet = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "spritesheet.png")).convert_alpha()
img_menu = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "menu.png")).convert()
img_jogo = pygame.image.load(os.path.join(DIRETORIO_IMAGENS, "floresta.png")).convert()

relogio = pygame.time.Clock()

tela_atual = "menu"
morreu = False

all_sprites = pygame.sprite.Group()
personagem = None
fundo = None

while True:
    relogio.tick(60)
    tela.fill(AZUL)

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()

        if tela_atual == "menu":
            if evento.type == KEYDOWN:
                tela_atual = "jogo"
                fundo = Background(img_jogo)
                personagem = Personagem(spritesheet)
                all_sprites = pygame.sprite.Group(fundo, personagem)
                morreu = False

                tela.fill(AZUL)
                all_sprites.draw(tela)
                pygame.display.flip()

                novo_cenario = tela.copy()
                Transicao.fade_in_from_black(tela, novo_cenario)

        elif tela_atual == "jogo":
            if evento.type == KEYDOWN:
                if evento.key == K_SPACE and not morreu:
                    personagem.pular()
                elif evento.key == K_f and not morreu:
                    personagem.morrer()
                    morreu = True
                elif evento.key == K_RETURN and morreu:
                    personagem = Personagem(spritesheet)
                    all_sprites = pygame.sprite.Group(fundo, personagem)
                    morreu = False

    if tela_atual == "menu":
        tela.blit(img_menu, (0, 0))
        fonte = pygame.font.Font(FONT_NAME, 25)
        texto2 = fonte.render("Pressione qualquer tecla para começar!", True, (10, 205, 28))
        tela.blit(texto2, (LARGURA // 2 - texto2.get_width() // 2, ALTURA - 100))

    elif tela_atual == "jogo":
        teclas = pygame.key.get_pressed()
        if personagem and not personagem.morrendo:
            if teclas[K_d] or teclas[K_RIGHT]:
                personagem.vel_x = 5
            elif teclas[K_a] or teclas[K_LEFT]:
                personagem.vel_x = -5
            else:
                personagem.vel_x = 0

        all_sprites.update()
        all_sprites.draw(tela)

        if morreu:
            fonte = pygame.font.Font(FONT_NAME, 30)
            texto1 = fonte.render("Você morreu", True, (0, 0, 0))
            texto2 = fonte.render("Pressione 'Enter' para reiniciar!", True, (0, 0, 0))
            tela.blit(texto1, (LARGURA // 2 - texto1.get_width() // 2, ALTURA - 370))
            tela.blit(texto2, (LARGURA // 2 - texto2.get_width() // 2, ALTURA - 320))

    pygame.display.flip()
