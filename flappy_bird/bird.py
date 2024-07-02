from typing import Any
import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y,imgs):
        super().__init__()
        self.origin_x = x
        self.origin_y = y
        self.imgs = imgs
        self.img_index = 0
        self.image = self.imgs[self.img_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.last_pic_time = pygame.time.get_ticks()
        self.img_frequency =  100
        self.speedy = 0
        self.fly = True
    
    def update(self,ground_top):
        # 飛翔動畫
        if self.fly:
            now = pygame.time.get_ticks()
            if now - self.last_pic_time > self.img_frequency:
                self.img_index += 1
                if self.img_index >= len(self.imgs):
                    self.img_index = 0
                self.image = pygame.transform.rotate(self.imgs[self.img_index],-self.speedy*2)
                self.last_pic_time = now

        # 引力
        self.speedy += 0.5
        if self.speedy > 9:  #限制往下墜的最大速度
            self.speedy = 9
        self.rect.y += self.speedy
        if self.rect.bottom > ground_top:
            self.rect.bottom = ground_top
    
    def jump(self):
        self.speedy = -10
    
    def game_over(self):
        self.fly = False
        self.image = pygame.transform.rotate(self.imgs[self.img_index],-90)

    def reset(self):
        self.img_index = 0
        self.image = self.imgs[self.img_index]
        self.rect.center = (self.origin_x,self.origin_y)
        self.last_pic_time = pygame.time.get_ticks()
        self.speedy = 0
        self.fly = True