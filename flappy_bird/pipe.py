import pygame
import random

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,img,top):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.speedx  = 4
        self.bird_pass = False
        if top:
            self.rect.bottomleft = (x,y)
        else:
            self.rect.topleft = (x,y)



    def update(self):
        self.rect.x -= 4
        if self.rect.right < 0:
            self.kill()