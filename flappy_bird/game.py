# from tkinter import *
import pygame
import random
from bird import Bird
from pipe import Pipe
import asyncio

pygame.init()

def generate_pipes(last_pipe_time,pipe_freequency,pipe_group):
    now = pygame.time.get_ticks()   
    if now - last_pipe_time >= pipe_freequency:
        random_height = random.randint(-60,60)
        pipe_btm = Pipe(SCREEN_WIDTH,SCREEN_HEIGHT/2 +pipe_gap/2 + random_height ,pipe_img,False)
        pipe_top = Pipe(SCREEN_WIDTH,SCREEN_HEIGHT/2 -pipe_gap/2 + random_height ,flip_pipe_img,True)
        pipe_group.add(pipe_btm)
        pipe_group.add(pipe_top)
        return now
    return last_pipe_time

def draw_score():
    score_text = score_font.render(str(score),True, WHITE)
    window.blit(score_text,(SCREEN_WIDTH/2 - score_text.get_width()/2, 20 ))
# 設定常數
FPS = 60
SCREEN_WIDTH = 780
SCREEN_HEIGHT = 600
WHITE = (255,255,255)

window = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("可愛的鳥鳥")
clock = pygame.time.Clock()

# 導入圖片
# C:/Users/user/Desktop/PYTHON練習PROJECT/pygame/bg.png
bg_img = pygame.image.load("./png/bg.png")
bg_img = pygame.transform.scale(bg_img,(780,600))
ground_img = pygame.image.load("./png/ground.png")
pipe_img = pygame.image.load("./png/pipe.png")
restart_img = pygame.image.load("./png/restart.png")
flip_pipe_img = pygame.transform.flip(pipe_img,False,True)
bird_imgs = []
for i in range(1,3):
    bird_imgs.append(pygame.image.load(f"./png/bird{i}.png"))

pygame.display.set_icon(bird_imgs[0])

# 載入字體
score_font = pygame.font.Font("微軟正黑體.ttf",60)

# 遊戲變數
ground_speed = 4
ground_x = 0
ground_top = SCREEN_HEIGHT - 100
pipe_gap = 150
pipe_freequency = 1500
last_pipe_time = pygame.time.get_ticks() - pipe_freequency
score = 0
game_over = False

bird = Bird(100,SCREEN_HEIGHT/2,bird_imgs)
bird_group = pygame.sprite.Group()
bird_group.add(bird)

pipe_group = pygame.sprite.Group()

run = True
async def main():
    global ground_speed
    global ground_x
    global ground_top
    global pipe_gap
    global pipe_freequency
    global last_pipe_time
    global score
    global game_over
    global run
    while run:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not game_over:
                    bird.jump()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    game_over = False
                    score = 0
                    last_pipe_time = pygame.time.get_ticks() - pipe_freequency
                    bird.reset()
                    pipe_group.empty() #把該群組的物件全數刪除

        # 更新遊戲
        bird_group.update(ground_top)
        if not game_over:
            pipe_group.update()
            last_pipe_time = generate_pipes(last_pipe_time,pipe_freequency,pipe_group)
            # 判斷通過管子
            first_pipe = pipe_group.sprites()[0]
            if not first_pipe.bird_pass:
                if first_pipe.rect.right < bird.rect.left:
                    score += 1
                    first_pipe.bird_pass = True
            # 移動地板
            ground_x -= ground_speed
            if ground_x < -110:
                ground_x = 0  

        # 碰撞判斷
        if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or bird.rect.top <= 0 or bird.rect.bottom >= ground_top : #第一個布林值若為TRUE，則鳥的物件就會被移除。第二個亦同
            game_over = True
            bird.game_over()

        # 畫面顯示

        window.blit(bg_img,(0,0))
        #window.blit(bird_img,(100,100))
        pipe_group.draw(window)
        window.blit(ground_img,(ground_x, ground_top))
        draw_score()
        if game_over:
            window.blit(restart_img,(SCREEN_WIDTH/2 - restart_img.get_width()/2,SCREEN_HEIGHT/2 - restart_img.get_height()/2))
        bird_group.draw(window)
        
        pygame.display.update()
        await asyncio.sleep(0)
asyncio.run(main())
pygame.quit()