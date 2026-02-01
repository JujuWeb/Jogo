import pygame
from pygame.locals import *
from sys import exit
import os

from transicao import Transicao
from personagem import Personagem
from background import Background
from aparencia import LARGURA, ALTURA, AZUL, BRANCO, PRETO, CHAO, FONT_NAME, FONT_TUTORIAL, DIRETORIO_IMAGENS
from inimigo import * 
from plataforma import Plataforma
from imagens import *

pygame.init()

# ====== TELA ======
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Caos IFinito")
relogio = pygame.time.Clock()

# ====== VARIÁVEIS ======
tela_atual = "menu"
morreu = False

all_sprites = pygame.sprite.Group()
grupo_inimigos = pygame.sprite.Group()
grupo_plataformas = pygame.sprite.Group()
personagem = None
fundo = None

# ====== LOOP PRINCIPAL ======
while True:
    relogio.tick(60)
    tela.fill(AZUL)

    # ====== EVENTOS ======
    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            exit()

        # ====== MENU ======
        if tela_atual == "menu":
            if evento.type == KEYDOWN:
                tela_atual = "tutorial"
                fundo = Background(img_inicioI)
                personagem = Personagem(spritesheet)
                all_sprites = pygame.sprite.Group(fundo, personagem)
                morreu = False

                tela.fill(AZUL)
                all_sprites.draw(tela)
                pygame.display.flip()
                Transicao.fade_in(tela, tela.copy())

        # ====== TUTORIAL ======
        elif tela_atual == "tutorial":
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

        # ====== INÍCIO ======
        elif tela_atual == "inicioI":
            if evento.type == KEYDOWN:
                if evento.key == K_SPACE and not morreu:
                    personagem.pular()
                elif evento.key == K_f and not morreu:
                    personagem.morrer()
                    morreu = True
                elif evento.key == K_RETURN and morreu:
                    # Reinicia o personagem
                    personagem = Personagem(spritesheet)
                    personagem.rect.left = 0  # posição inicial

                    # Reinicia inimigos
                    virus = Virus(img_virus, 440, 160, limite_e=440, limite_d=600)
                    dinossauro = Dinossauro(img_dino, 600, 354, limite_e=340, limite_d=800)
                    grupo_inimigos.empty()
                    grupo_inimigos.add(virus, dinossauro)

                    # Reinicia plataformas
                    grupo_plataformas.empty()
                    plataforma_baixa = Plataforma(img_blocobaixo, 183, 365, 120, 70)
                    plataforma_alta = Plataforma(img_blocoalto, 450, 200, 200, 110)
                    grupo_plataformas.add(plataforma_baixa, plataforma_alta)

                    # Todos os sprites visíveis
                    all_sprites = pygame.sprite.Group(fundo, personagem, virus, dinossauro,
                                                    plataforma_baixa, plataforma_alta)

                    morreu = False


    # ====== DESENHO TELAS ======
    if tela_atual == "menu":
        tela.blit(img_menu, (0, 0))
        fonte = pygame.font.Font(FONT_NAME, 25)
        texto2 = fonte.render("Pressione qualquer tecla para começar!", True, (255, 255, 255))
        tela.blit(texto2, (510- texto2.get_width() // 2, ALTURA - 78))

    elif tela_atual == "tutorial":
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

        # ====== TUTORIAL VISUAL ======
        fonte = pygame.font.Font(FONT_TUTORIAL, 20)
        tela.blit(fonte.render("ANDAR PARA             ANDAR PARA", True, (0, 0, 0)), (230, 50))
        tela.blit(fonte.render("ESQUERDA                 DIREITA", True, (0, 0, 0)), (240, 70))
        tela.blit(fonte.render("PULAR", True, (0, 0, 0)), (700, 115))
        tela.blit(img_teclas_e, (250, 100))
        tela.blit(img_teclas_d, (410, 100))
        tela.blit(img_teclas_p, (500, 125))

        if personagem.rect.right >= LARGURA:
            tela_atual = "inicioI"
            fundo = Background(img_inicioI)
            personagem.rect.left = 0

            virus = Virus(img_virus, 440, 160, limite_e=440, limite_d=600)
            dinossauro = Dinossauro(img_dino, 600, 354, limite_e=340, limite_d=800)

            grupo_inimigos.empty()
            grupo_inimigos.add(virus, dinossauro)

            all_sprites = pygame.sprite.Group(fundo, personagem, virus, dinossauro)

            # ====== PLATAFORMAS ======
            grupo_plataformas.empty()
            plataforma_baixa = Plataforma(img_blocobaixo, 183, 365, 120, 70)
            plataforma_alta = Plataforma(img_blocoalto, 450, 200, 200, 110)
            grupo_plataformas.add(plataforma_baixa, plataforma_alta)
            all_sprites.add(plataforma_baixa, plataforma_alta)

            Transicao.fade_in(tela, tela.copy())

    elif tela_atual == "inicioI":
        teclas = pygame.key.get_pressed()
        if personagem and not personagem.morrendo:
            if teclas[K_d] or teclas[K_RIGHT]:
                personagem.vel_x = 5
            elif teclas[K_a] or teclas[K_LEFT]:
                personagem.vel_x = -5
            else:
                personagem.vel_x = 0

        personagem.na_plataforma = False
        all_sprites.update()
        all_sprites.draw(tela)

        # ====== COLISÃO INIMIGOS ======
        colisoes = pygame.sprite.spritecollide(personagem, grupo_inimigos, False)
        for inimigo in colisoes:
            # Matar pelo topo
            if personagem.vel_y > 0 and personagem.rect.bottom <= inimigo.rect.top + 15:
                inimigo.kill()
                personagem.vel_y = -15
                personagem.pulando = True
            else:
                personagem.morrer()
                morreu = True

        # ====== COLISÃO PLATAFORMAS COM MARGEM ======
        colisao_plataforma = pygame.sprite.spritecollide(personagem, grupo_plataformas, False)
        for plat in colisao_plataforma:
            dx_esq = personagem.rect.right - plat.rect.left
            dx_dir = plat.rect.right - personagem.rect.left
            dy_cima = personagem.rect.bottom - plat.rect.top
            dy_baixo = plat.rect.bottom - personagem.rect.top

            menor = min(dx_esq, dx_dir, dy_cima, dy_baixo)

            if menor == dy_cima and personagem.vel_y >= 0:
                # Margem visual sem teletransporte
                ajuste_visual = 0
                if plat == plataforma_baixa:
                    ajuste_visual = 15
                elif plat == plataforma_alta:
                    ajuste_visual = 35

                alvo_bottom = plat.rect.top + ajuste_visual
                if personagem.rect.bottom > alvo_bottom:
                    personagem.rect.bottom = alvo_bottom
                    personagem.vel_y = 0
                    personagem.pulando = False
                    personagem.na_plataforma = True

            elif menor == dy_baixo:
                personagem.rect.top = plat.rect.bottom
                personagem.vel_y = 0
            elif menor == dx_esq:
                personagem.rect.right = plat.rect.left
            elif menor == dx_dir:
                personagem.rect.left = plat.rect.right

        if personagem.rect.right >= LARGURA:
            tela_atual = "inicioII"
            fundo = Background(img_inicioII)
            personagem.rect.left = 0

            go = Go(img_go, 300, 300, limite_e=300, limite_d=1100)
            grupo_inimigos.empty()
            grupo_inimigos.add(go)

            grupo_plataformas.empty()
            all_sprites = pygame.sprite.Group(fundo, personagem, go)

            Transicao.fade_in(tela, tela.copy())

        if morreu:
            fonte = pygame.font.Font(FONT_NAME, 30)
            tela.blit(fonte.render("Você morreu", True, (0, 0, 0)),
                      (LARGURA // 2 - 100, ALTURA - 370))
            tela.blit(fonte.render("Pressione 'Enter' para reiniciar!", True, (0, 0, 0)),
                      (LARGURA // 2 - 200, ALTURA - 320))

    elif tela_atual == "inicioII":
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

        colisoes = pygame.sprite.spritecollide(personagem, grupo_inimigos, False)
        for inimigo in colisoes:
            if personagem.vel_y > 0 and personagem.rect.bottom <= inimigo.rect.top + 15:
                inimigo.kill()
                personagem.vel_y = -15
                personagem.pulando = True
            else:
                personagem.morrer()
                morreu = True

        # ====== MENSAGEM MORTE ======
        if morreu:
            fonte = pygame.font.Font(FONT_NAME, 30)
            texto1 = fonte.render("Você morreu", True, (0, 0, 0))
            texto2 = fonte.render("Pressione 'Enter' para reiniciar!", True, (0, 0, 0))
            tela.blit(texto1, (LARGURA // 2 - texto1.get_width() // 2, ALTURA - 370))
            tela.blit(texto2, (LARGURA // 2 - texto2.get_width() // 2, ALTURA - 320))

    pygame.display.flip()