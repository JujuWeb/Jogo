import pygame

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