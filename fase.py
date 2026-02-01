import pygame
from transicao import Transicao

class Fase:
    def __init__(self):
        self.fase_atual = 1
        self.vitoria = False

        # Fundo e cano iniciais
        self.fundo = pygame.image.load("background-day.png").convert_alpha()
        self.cano_img = "pipe-red.png"

        # 🔹 imagem da vitória
        self.vitoria_img = pygame.image.load("vitoria.png").convert_alpha()

    def atualizar(self, pontos, tela, estado_jogo=None):
        # ===== RESET DO FUNDO CASO MORTE COM MAIS DE 15 PONTOS =====
        if estado_jogo == "MORTE" and pontos > 15:
            self.fundo = pygame.image.load("background-day.png").convert_alpha()
            self.cano_img = "pipe-red.png"

        # ===== FASE 2 =====
        if pontos >= 15 and self.fase_atual == 1:
            self.fase_atual = 2
            self.fundo = pygame.image.load("background-dayy.png").convert_alpha()
            self.cano_img = "po.png"
            return "FASE"

        # ===== VITÓRIA =====
        if pontos >= 30 and not self.vitoria:
            self.vitoria = True

            # fade antes da vitória
            Transicao.fade_in(tela, tela.copy())

            return "VITORIA"

        return None

    def desenhar_vitoria(self, tela, w, h):
        img = pygame.transform.scale(self.vitoria_img, (w, h))
        tela.blit(img, (0, 0))
