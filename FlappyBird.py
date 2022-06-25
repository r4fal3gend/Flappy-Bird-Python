import pygame
from pygame.locals import *
from pygame import math
from os import sys
import os
import random

nome = input("Digite seu nome: ")
email = input("Digite seu e-mail: ")

registro = open('registro.txt','a')
registro.write(f'Nome: {nome}\nEmail: {email}\n')
registro.close()

pygame.init()

path_dir = os.path.dirname(__name__)
img_path = os.path.join(path_dir,'source')

os.environ['SDL_VIDEO_CENTERED'] = '1'

LARGURA, ALTURA = 400,700

tela = pygame.display.set_mode([LARGURA, ALTURA])
relogio = pygame.time.Clock()
pygame.display.set_caption('Flappy Bird')

grupo_canos = pygame.sprite.Group()

print(img_path)

pygame.font.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.velocidade = math.Vector2(0,0)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(img_path,'frame-1.png')),(30,30))
        self.rect = self.image.get_rect().move(160,ALTURA/2)
 
class BG:
    def __init__(self, indice):
        self.bg = pygame.image.load(os.path.join(img_path,'bg.png'))
        self.bg = pygame.transform.scale(self.bg,(LARGURA,ALTURA))
        self.rect = self.bg.get_rect()
        self.rect.y = 0
        self.rect.x = self.rect.x + LARGURA * indice

    def Move(self):
        if self.rect.right > 0:
            self.rect = self.rect.move(-1,0)
        else:
            self.rect.left = LARGURA

class Cano(pygame.sprite.Sprite):
    def __init__(self, *groups, flip):
        super().__init__(*groups)
        self.image = pygame.image.load(os.path.join(img_path, 'pipe.png'))
        self.image = pygame.transform.scale(self.image, (75,ALTURA))
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA+10
        if flip:
            self.image = pygame.transform.flip(self.image,False, True)
    def Move(self):
        
        if self.rect.right < -10:
            self.kill()
        else:
            self.rect = self.rect.move(-1,0)
        
bgs = [BG(0),BG(1)]

time = 0
img = 1

p = Player()
gravidade = math.Vector2(0,1)

def Draw():

    for i in bgs:
        i.Move()
        tela.blit(i.bg,i.rect)
    tela.blit(p.image,p.rect)
    grupo_canos.draw(tela)

pipes = []

def SpawnPipe():

    cano1 = Cano(grupo_canos, flip=True)
    cano2 = Cano(grupo_canos, flip=False)
    cano1.rect.bottom = random.randint(0,ALTURA-200)
    cano2.rect.top = cano1.rect.bottom + 150

    pipes.append(cano1)
    pipes.append(cano2)

    pass

pontos = 0

spawn_time = 0
spawn = 90 

def Game():
    global time, img, spawn_time,spawn, pipes
    pontos = 0
    pipes.clear()
    time = 0
    img = 1
    spawn = 90
    spawn_time = 0
    game = False
    p.rect.center = [LARGURA/2-10,ALTURA/2+10]
    if game == False :
        TelaInicial = True
        pipes = []
        while TelaInicial:

            for i in bgs:
                i.Move()
                tela.blit(i.bg,i.rect)

            image = pygame.transform.scale(pygame.image.load(os.path.join(img_path,'logo.png')), (LARGURA-20, 90))
            image_rect = image.get_rect()
            image_rect.center = [LARGURA/2,ALTURA/2-50]
            tela.blit(image,image_rect)
            play_btn = pygame.transform.scale(pygame.image.load(os.path.join(img_path,'play.png')), (100,75))
            play_btn_rect = play_btn.get_rect()
            play_btn_rect.center = [LARGURA/2,ALTURA/2+100]
            tela.blit(play_btn,play_btn_rect)
            
            fonte = pygame.font.Font(os.path.join(img_path,'Flappy-Bird.ttf'), 30)
            text = fonte.render("Pressione espaco para pular", True,[255,255,255])
            text_rect = text.get_rect()
            text_rect.center = [LARGURA//2,ALTURA//2+200]
            tela.blit(text, text_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
            mouse = pygame.mouse.get_pos()
            time += 1
            if time == 5:
                p.image = pygame.transform.scale(pygame.image.load(os.path.join(img_path,'frame-{}.png'.format(img))),(50,50))
                img += 1
                time = 0
            if img == 5:
                img = 1
            
            tela.blit(p.image,p.rect)

            if play_btn_rect.right > mouse[0] > play_btn_rect.left and play_btn_rect.bottom > mouse[1] > play_btn_rect.top:
                pressed_button = pygame.mouse.get_pressed()
                if pressed_button[0]:
                    grupo_canos.empty()
                    spawn = 90
                    spawn_time = 0
                    game = True
                    TelaInicial = False
                                   
            pygame.display.update()

    if game == True:
        
        time = 0
        img = 1
        spawn = 90
        spawn_time = 0
        p.rect.center = [LARGURA/2-10,ALTURA/2+10]
        pipes.clear()
        while game:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        p.velocidade.y = -10    
                          
            time += 1
            if time == 5:
                p.image = pygame.transform.scale(pygame.image.load(os.path.join(img_path,'frame-{}.png'.format(img))),(50,50))
                img += 1
                time = 0
            if img == 5:
                img = 1

            for cano in pipes:
                if cano.rect.centerx == p.rect.x:
                    pontos+=0.5
            
            spawn_time += 1
            if spawn_time == spawn:
                spawn_time = 0
                spawn = random.randint(200,300)
                SpawnPipe() 
            
            p.rect = p.rect.move(p.velocidade)

            colisao = pygame.sprite.spritecollide(p,grupo_canos, True)
            if colisao:
                pipes.clear()
                
                return

            if p.rect.bottom >= ALTURA - 20:
                p.velocidade.y = 0
                
            else:
                p.velocidade += gravidade
 
            for pipe in pipes:
                pipe.Move()
            
            Draw() 
            fonte = pygame.font.Font(os.path.join(img_path,'Flappy-Bird.ttf'), 50)
            text = fonte.render("SCORE:{}".format(int(pontos)), True,[255,255,255])
            text_rect = text.get_rect()
            text_rect.center = [LARGURA//2, 20]
            tela.blit(text, text_rect)
            relogio.tick(60)
            pygame.display.update()

if __name__ == '__main__':

    while True:
        Game()