import pygame
import os

# Configurações básicas da cobra
COBRA_VEL = 2.5
COBRA_ANIMACAO_VEL = 0.20  # segundos entre frames

# --- Função utilitária: corta a sprite sheet ---
def cortar_sprite_sheet(caminho, linhas, colunas, escala=None):
    """Corta uma sprite sheet em várias imagens."""
    sheet = pygame.image.load(caminho).convert_alpha()
    largura_total, altura_total = sheet.get_size()
    largura_frame = largura_total // colunas
    altura_frame = altura_total // linhas

    imagens = []
    for y in range(linhas):
        for x in range(colunas):
            rect = pygame.Rect(x * largura_frame, y * altura_frame, largura_frame, altura_frame)
            frame = sheet.subsurface(rect).copy()
            if escala:
                frame = pygame.transform.scale(frame, escala)
            imagens.append(frame)
    return imagens


# --- Classe principal da cobra ---
class CobraInimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, vel=COBRA_VEL):
        super().__init__()

        caminho = os.path.join("images", "cobra_sheet.png")
        frames = cortar_sprite_sheet(caminho, linhas=2, colunas=8, escala=(80, 40))

        # Primeira linha: direita, segunda: esquerda
        self.anim_d = frames[:8]
        self.anim_e = frames[8:]

        self.vel = vel
        self.frame = 0
        self.image = self.anim_d[0]
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.tempo_animacao = 0

    def update(self, dt, limite_esquerda, limite_direita):
        # Atualiza animação
        self.tempo_animacao += dt
        if self.tempo_animacao >= COBRA_ANIMACAO_VEL * 1000:
            self.tempo_animacao = 0
            self.frame = (self.frame + 1) % len(self.anim_d)

        # Movimento
        self.rect.x += self.vel

        # Inverte direção nas bordas
        if self.rect.left <= limite_esquerda or self.rect.right >= limite_direita:
            self.vel = -self.vel

        # Atualiza sprite conforme direção
        if self.vel > 0:
            self.image = self.anim_d[self.frame]
        else:
            self.image = self.anim_e[self.frame]
