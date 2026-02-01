import pygame
import os

class Pontuacao:
    def __init__(self):
        self.pontos = 0

        # Carrega as sprites dos números (0 a 9)
        self.numeros = {}
        for i in range(10):
            imagem = pygame.image.load(
                os.path.join(f"{i}.png")
            ).convert_alpha()
            imagem = pygame.transform.scale(imagem, (24*2 , 36*2))
            self.numeros[str(i)] = imagem



        # Espaçamento entre os números
        self.espaco = 5

    def atualizar(self, passaro, canos):
        """
        Soma pontos quando o pássaro passa pelos canos
        """
        for cano in canos:
            if not cano.pontuado and cano.rect.right < passaro.rect.left:
                cano.pontuado = True
                self.pontos += 0.5  # 2 canos = 1 ponto

    def desenhar(self, tela):
        # Converte a pontuação para inteiro e depois para string
        texto_pontos = str(int(self.pontos))

        x = 465
        y = 25

        # Desenha cada dígito como sprite
        for digito in texto_pontos:
            imagem = self.numeros[digito]
            tela.blit(imagem, (x, y))
            x += imagem.get_width() + self.espaco

    def resetar(self):
        self.pontos = 0

