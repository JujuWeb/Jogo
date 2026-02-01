import pygame, random
from pygame.locals import *
from pontuacao import Pontuacao
from fase import Fase
from inicio import Inicio, INICIO, JOGANDO, MORTE, VITORIA
from transicao import Transicao
from sys import exit
import os

# ================= CONFIGURAÇÕES =================
tela_w = 960
tela_h = 540
velocidade_inicial = 15
gravidade = 1.7
vel_jogo = 20

chao_largura = tela_w
chao_altura = 1

cano_w = 160
cano_h = 600
cano_gap = 180


# ================= CLASSES DO JOGO =================
class Passaro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [
            pygame.transform.scale(pygame.image.load('alto.png').convert_alpha(), (78, 54)),
            pygame.transform.scale(pygame.image.load('medio.png').convert_alpha(), (78, 54)),
            pygame.transform.scale(pygame.image.load('baixo.png').convert_alpha(), (78, 54))
        ]
        self.vel = 0
        self.current_image = 0
        self.image = self.images[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(tela_w // 2, tela_h // 2))

    def update(self, estado_jogo):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)

        if estado_jogo == JOGANDO:
            self.vel += gravidade
            self.rect.y += self.vel

    def subir(self):
        self.vel = -velocidade_inicial


class Cano(pygame.sprite.Sprite):
    def __init__(self, invertido, xpos, ysize, imagem_cano):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(imagem_cano).convert_alpha(),
            (cano_w, cano_h)
        )
        self.rect = self.image.get_rect()
        self.rect.x = xpos

        if invertido:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.y = -(self.rect.height - ysize)
        else:
            self.rect.y = tela_h - ysize

        self.mask = pygame.mask.from_surface(self.image)
        self.pontuado = False

    def update(self, estado_jogo):
        if estado_jogo == JOGANDO:
            self.rect.x -= vel_jogo


class Chao(pygame.sprite.Sprite):
    def __init__(self, xpos):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load('base.png').convert_alpha(),
            (chao_largura, chao_altura)
        )
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(x=xpos, y=tela_h - chao_altura)

    def update(self, estado_jogo):
        if estado_jogo == JOGANDO:
            self.rect.x -= vel_jogo


def Fora_tela(sprite):
    return sprite.rect.right < 0


def Gerar_canos(xpos, imagem_cano):
    tamanho = random.randint(75, 350)
    return (
        Cano(False, xpos, tamanho, imagem_cano),
        Cano(True, xpos, tela_h - tamanho - cano_gap, imagem_cano)
    )


# ================= EASTER EGG =================
def rodar_easter_egg():
    LARGURA, ALTURA, CHAO = 960, 540, 385
    relogio = pygame.time.Clock()

    base = os.path.dirname(__file__)
    sprites = os.path.join(base, "sprite")

    fundo = pygame.transform.scale(
        pygame.image.load(os.path.join(sprites, "lua.png")).convert(),
        (LARGURA, ALTURA)
    )

    sheet_player = pygame.image.load(os.path.join(sprites, "spritesheet.png")).convert_alpha()
    sheet_npc = pygame.image.load(os.path.join(sprites, "npc.png")).convert_alpha()

    class Personagem(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.dir = [sheet_player.subsurface((i*85,0),(85,95)) for i in range(4)]
            self.esq = [sheet_player.subsurface((i*85,0),(85,95)) for i in range(4,8)]
            self.index = 0
            self.image = self.dir[0]
            self.rect = self.image.get_rect(midbottom=(300, CHAO))
            self.vel_x = 0
            self.vel_y = 0
            self.pulando = False
            self.gravidade = 0.2
            self.forca_pulo = -11

        def update(self):
            self.rect.x += self.vel_x
            self.vel_y += self.gravidade
            self.rect.y += self.vel_y

            if self.rect.bottom >= CHAO:
                self.rect.bottom = CHAO
                self.vel_y = 0
                self.pulando = False

            if self.vel_x != 0:
                self.index = (self.index + 0.25) % 4
                self.image = self.dir[int(self.index)] if self.vel_x > 0 else self.esq[int(self.index)]
            else:
                self.image = self.dir[0]

        def pular(self):
            if not self.pulando:
                self.vel_y = self.forca_pulo
                self.pulando = True

    class NPC(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            w = sheet_npc.get_width() // 7
            h = sheet_npc.get_height()
            self.frames = [
                pygame.transform.scale(
                    sheet_npc.subsurface((i*w,0),(w,h)), (240,240)
                ) for i in range(3)
            ]
            self.index = 0
            self.image = self.frames[0]
            self.rect = self.image.get_rect(midbottom=(650, CHAO))

        def update(self):
            self.index = (self.index + 0.1) % len(self.frames)
            self.image = self.frames[int(self.index)]

    personagem = Personagem()
    npc = NPC()
    grupo = pygame.sprite.Group(npc, personagem)

    while True:
        relogio.tick(60)
        tela.blit(fundo, (0, 0))

        for e in pygame.event.get():
            if e.type == QUIT:
                pygame.quit()
                exit()

            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    personagem.pular()

                elif e.key == K_RETURN:
                    Transicao.fade_in(tela, tela.copy())  # ✨ FADE NA SAÍDA
                    return

        keys = pygame.key.get_pressed()
        if keys[K_d] or keys[K_RIGHT]:
            personagem.vel_x = 5
        elif keys[K_a] or keys[K_LEFT]:
            personagem.vel_x = -5
        else:
            personagem.vel_x = 0

        grupo.update()
        grupo.draw(tela)
        pygame.display.update()


# ================= INICIALIZAÇÃO =================
pygame.init()
tela = pygame.display.set_mode((tela_w, tela_h))
clock = pygame.time.Clock()

pontuacao = Pontuacao()
fase = Fase()
inicio = Inicio(tela_w, tela_h)

fundo_jogo = pygame.transform.scale(fase.fundo, (tela_w, tela_h))

gameover_img = pygame.transform.scale(
    pygame.image.load("gameover.png").convert_alpha(),
    (tela_w, tela_h)
)

passaro = Passaro()
passaro_group = pygame.sprite.Group(passaro)

cano_group = pygame.sprite.Group()
for i in range(2):
    cano_group.add(*Gerar_canos(tela_w * i + 1000, fase.cano_img))

chao_group = pygame.sprite.Group(Chao(0), Chao(chao_largura))


# ================= LOOP PRINCIPAL =================
while True:
    clock.tick(20)

    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            exit()

        if e.type == KEYDOWN and e.key == K_SPACE:
            if inicio.estado == INICIO:
                inicio.estado = JOGANDO
                passaro.subir()

            elif inicio.estado == JOGANDO:
                passaro.subir()

            elif inicio.estado == MORTE:
                pontuacao.pontos = 0
                inicio.estado = INICIO
                passaro.rect.center = (tela_w // 2, tela_h // 2)
                passaro.vel = 0

                cano_group.empty()
                for i in range(2):
                    cano_group.add(*Gerar_canos(tela_w * i + 1000, fase.cano_img))

            elif inicio.estado == VITORIA:
                pygame.quit()
                exit()

    if inicio.estado == JOGANDO and passaro.rect.top < -60:
        inicio.estado = MORTE
        Transicao.fade_in(tela, tela.copy())
        rodar_easter_egg()

        # 🔹 RESET AO VOLTAR DO EASTER EGG
        pontuacao.pontos = 0
        inicio.estado = INICIO
        passaro.rect.center = (tela_w // 2, tela_h // 2)
        passaro.vel = 0

        cano_group.empty()
        for i in range(2):
            cano_group.add(*Gerar_canos(tela_w * i + 1000, fase.cano_img))

    pontuacao.atualizar(passaro, cano_group)

    resultado = fase.atualizar(int(pontuacao.pontos), tela)

    if resultado == "FASE":
        fundo_jogo = pygame.transform.scale(fase.fundo, (tela_w, tela_h))
        cano_group.empty()
        for i in range(3):
            cano_group.add(*Gerar_canos(tela_w + i * 550, fase.cano_img))

    elif resultado == "VITORIA":
        inicio.estado = VITORIA

    tela.blit(fundo_jogo, (0, 0))

    if len(cano_group) > 0 and Fora_tela(cano_group.sprites()[0]):
        cano_group.remove(cano_group.sprites()[0])
        cano_group.remove(cano_group.sprites()[0])
        cano_group.add(*Gerar_canos(tela_w * 2, fase.cano_img))

    for grupo in (passaro_group, cano_group, chao_group):
        grupo.update(inicio.estado)
        grupo.draw(tela)

    if inicio.estado == JOGANDO:
        if (
            pygame.sprite.groupcollide(passaro_group, chao_group, False, False, pygame.sprite.collide_mask)
            or pygame.sprite.groupcollide(passaro_group, cano_group, False, False, pygame.sprite.collide_mask)
        ):
            inicio.estado = MORTE
            Transicao.fade_in(tela, tela.copy())

    if inicio.estado == MORTE:
        tela.blit(gameover_img, (0, 0))

    elif inicio.estado == VITORIA:
        fase.desenhar_vitoria(tela, tela_w, tela_h)

    else:
        pontuacao.desenhar(tela)
        inicio.desenhar(tela)

    pygame.display.update()
