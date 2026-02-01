import pygame
from aparencia import LARGURA

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, imagem, x, y, largura, altura, limite_e, limite_d, velocidade=2):
        super().__init__()
        self.image = pygame.transform.scale(imagem, (largura, altura))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.limite_e = limite_e  
        self.limite_d = limite_d  
        self.velocidade = velocidade 
        self.direcao = 1  

    def mover_horizontal(self):
        self.rect.x += self.velocidade * self.direcao

        if self.rect.x <= self.limite_e or self.rect.x >= self.limite_d:
            self.direcao *= -1 #inverte

    def update(self):
        self.mover_horizontal()

class Virus(Inimigo):
    def __init__(self, imagem, x, y, limite_e, limite_d):
        super().__init__(imagem, x, y, largura=65, altura=45, 
                         limite_e=limite_e, limite_d=limite_d, velocidade=2)

    def update(self):
        self.mover_horizontal()

    def update(self):
        self.mover_horizontal()

class Dinossauro(Inimigo):
    def __init__(self, spritesheet, x, y, limite_e, limite_d):
        self.frames = []
        self.frame_atual = 0

        self.ultimo_update = pygame.time.get_ticks()
        self.intervalo_animacao = 180  

        largura_frame = spritesheet.get_width() // 4
        altura_frame = spritesheet.get_height()

        for i in range(4):
            frame = spritesheet.subsurface(
                (i * largura_frame, 0, largura_frame, altura_frame)
            )
            frame = pygame.transform.scale(frame, (80, 80))
            self.frames.append(frame)

        super().__init__(
            self.frames[0],
            x, y,
            largura=80,
            altura=80,
            limite_e=limite_e,
            limite_d=limite_d,
            velocidade=4
        )

    def animar(self):
        agora = pygame.time.get_ticks()

        if agora - self.ultimo_update >= self.intervalo_animacao:
            self.ultimo_update = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)

            imagem = self.frames[self.frame_atual]

            if self.direcao == -1:
                imagem = pygame.transform.flip(imagem, True, False)

            self.image = imagem

    def update(self):
        self.mover_horizontal()
        self.animar()

class Go(Inimigo):
    def __init__(self, spritesheet, x, y, limite_e, limite_d):
        self.frames = []
        self.frame_atual = 0

        self.ultimo_update = pygame.time.get_ticks()
        self.intervalo_animacao = 80  

        TOTAL_FRAMES = 27 

        largura_frame = spritesheet.get_width() // TOTAL_FRAMES
        altura_frame = spritesheet.get_height() 

        for i in range(TOTAL_FRAMES):
            frame = spritesheet.subsurface(
                i * largura_frame,
                0,
                largura_frame,
                altura_frame
            )
            frame = pygame.transform.scale(frame, (260, 200))
            self.frames.append(frame)

        super().__init__(
            self.frames[0],
            x, y,
            largura=260,
            altura=200,
            limite_e=limite_e,
            limite_d=limite_d,
            velocidade=2
        )

    def animar(self):
        agora = pygame.time.get_ticks()

        if agora - self.ultimo_update >= self.intervalo_animacao:
            self.ultimo_update = agora
            self.frame_atual = (self.frame_atual + 1) % len(self.frames)

            imagem = self.frames[self.frame_atual]

            if self.direcao == -1:
                imagem = pygame.transform.flip(imagem, True, False)

            self.image = imagem

    def update(self):
        self.mover_horizontal()
        self.animar()