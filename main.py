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
pygame.display.set_caption("Caos IFinito")

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

telas = ""

jogo = True
while jogo:
    tela.fill(AZUL)
    relogio.tick(60)

    if telas == "menu":
        for evento in pygame.event.get():
            if evento.type == QUIT:
                jogo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    telas = "inicio"

        pygame.display.fill((0, 0, 0))
        fonte_menor = pygame.font.Font(font_name, 60)
        texto_menu1 = fonte_menor.render("Caos IFinito", True, (0, 0, 0))
        texto_menu2 = fonte_menor.render("Pressione 'Enter' para jogar", True, (0, 0, 0))
        tela.blit(texto1, (LARGURA // 2 - texto1.get_width() // 2, ALTURA // 2 - 80))
        tela.blit(texto2, (LARGURA // 2 - texto2.get_width() // 2, ALTURA // 2))

    elif telas == "inicio":
        for evento in pygame.event.get():
            if evento.type == QUIT:
                jogo = False
            elif evento.type == KEYDOWN:
                if evento.key == K_SPACE and not morreu:
                    personagem.pular()
            elif evento.key == K_f and not morreu:
                personagem.morrer()
                morreu = True
            elif evento.key == K_RETURN and morreu:
                personagem = Personagem(spritesheet)
                all_sprites = pygame.sprite.Group()
                all_sprites.add(fundo)
                all_sprites.add(personagem)
                morreu = False

    teclas = pygame.key.get_pressed()
    if not personagem.morrendo:
        if teclas[K_d] or teclas[K_RIGHT]:
            personagem.vel_x = 5
        elif teclas[K_a] or teclas[K_LEFT]:
            personagem.vel_x = -5
        else:
            personagem.vel_x = 0

    all_sprites.update()
    all_sprites.draw(tela)
    
    if telas == "gameover":
        if morreu:
            fonte_menor = pygame.font.Font(font_name, 60)
            texto1 = fonte_menor.render("Você morreu", True, (0, 0, 0))
            texto2 = fonte_menor.render("Pressione 'Enter' para reiniciar", True, (0, 0, 0))
            tela.blit(texto1, (LARGURA // 2 - texto1.get_width() // 2, ALTURA // 2 - 80))
            tela.blit(texto2, (LARGURA // 2 - texto2.get_width() // 2, ALTURA // 2))
    
    pygame.display.flip()