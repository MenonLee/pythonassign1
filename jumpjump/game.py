import pygame
import time
import sys
import random

WINDOW_WIDTH = 1366
WINDOW_HEIGHT = 768
GROUND = 630
GRAVITY = 5
FPS = 60

BLACK = (0,0,0)
WHITE = (255,255,255)

pygame.init()
pygame.display.set_caption("팀플 게임")
screen = pygame.display.set_mode((1366,768))
clock = pygame.time.Clock()
font = pygame.font.Font("jumpjump/Maplestory Bold.ttf",60)
jump_sound = pygame.mixer.Sound("jumpjump/jump_sound.ogg")
gamequit = False

def title():
    titleimg = pygame.image.load("jumpjump/title.png")
    logo_img = pygame.image.load("jumpjump/logo.png")

    titleimg = pygame.transform.scale(titleimg, (WINDOW_WIDTH,WINDOW_HEIGHT))
    logo_img = pygame.transform.scale(logo_img, (550, 300))
    
    pygame.mixer.music.load("jumpjump/Title.ogg")
    
    if pygame.mixer.music.get_busy() == False:
        pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()
                    
        txt = font.render("시작하려면 Enter키를 누르세요", True, BLACK)
        
        screen.blit(titleimg,[0,0])
        screen.blit(logo_img,[400,10])
        screen.blit(txt,[320,550])
        pygame.display.update()
        clock.tick(FPS)

        pygame.display.update() 

class Player(pygame.sprite.Sprite):

    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        size = (39,65)
        
        images = []
        # 0~2 기본상태
        images.append(pygame.image.load("jumpjump/ch_default1.png"))
        images.append(pygame.image.load("jumpjump/ch_default2.png"))
        images.append(pygame.image.load("jumpjump/ch_default3.png"))
        # 3~5 걷기상태
        images.append(pygame.image.load("jumpjump/ch_walk1.png"))
        images.append(pygame.image.load("jumpjump/ch_walk2.png"))
        images.append(pygame.image.load("jumpjump/ch_walk3.png"))
        # 6 점프상태
        images.append(pygame.image.load("jumpjump/ch_jump.png"))
        
        self.rect = pygame.Rect(position,size)
        self.images = [pygame.transform.scale(image, size) for image in images]

        self.images_left = images
        self.images_right = [pygame.transform.flip(image, True, False) for image in images]
         
        self.state = 0
        self.direction = 'left'
        self.velocity_x = 0
        self.velocity_y = 0
        self.jump = False

        self.index = 0
        self.image = images[self.index]
        
        # 1초에 보여줄 1장의 이미지 시간
        self.animation_time = round(100 / len(self.images * 100), 2)
        self.current_time = 0
    
    def update(self,mt):

        if self.state == 0:         # 정지상태
                count = 3
                start_Index = 0
                self.velocity_x = 0

        elif self.state == 1:       # 걷기상태
                count = 3
                start_Index = 3
                self.velocity_x = 4
                
        if self.direction == 'right':
                self.images = self.images_right
        elif self.direction == 'left':
                self.images = self.images_left
                self.velocity_x = abs(self.velocity_x) * -1

        self.current_time += mt

        if self.current_time >= self.animation_time:
            self.current_time = 0

            if self.jump == True:
                self.index = 6
                self.image = self.images[self.index]
            else:
                self.index = (self.index % count) + start_Index
            
                self.image = self.images[self.index]            
                self.index += 1

                if self.index >= len(self.images):
                    self.index = 0
        
        self.rect.x += self.velocity_x
        
        if self.rect.y < GROUND:
            self.rect.y += self.velocity_y
        else:
            self.rect.y = GROUND
                   
    def check_screen(self):
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.x -= 4
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.y -= 4

class Life:
    def __init__(self):
        self.heart_img = pygame.image.load("jumpjump/heart.png")
        self.life = 3
        
    def draw(self):
        if self.life == 3:
            screen.blit(self.heart_img, (10,70))
            screen.blit(self.heart_img, (70,70))
            screen.blit(self.heart_img, (130,70))
        elif self.life == 2:
            screen.blit(self.heart_img, (10,70))
            screen.blit(self.heart_img, (70,70))
        elif self.life == 1:
            screen.blit(self.heart_img, (10,70))
        else:
            self.gameover()
    
    def damage(self):
        self.life -= 1
    
    def gameover(self):
        global gamequit
        if self.life == 0:
            txt = font.render('Game Over',True,BLACK)
            screen.blit(txt,[200,350])
            gamequit = True

class Boss():
    def __init__(self,position):
        size = (560,500)
        self.boss_image = pygame.image.load("jumpjump/giant_snowman.png")
        self.image = pygame.transform.scale(self.boss_image, size)
        self.rect = pygame.Rect(position,size)
    def draw(self):
        screen.blit(self.image,(750,200))
      
def gameclear():
    global gamequit
    cleartxt = font.render('Game Clear',True,BLACK)
    screen.blit(cleartxt,[200,350])
    gamequit = True
                
def main():
    global gamequit
    img_bg = pygame.image.load("jumpjump/happyvillage.png")
    img_bg = pygame.transform.scale(img_bg, (WINDOW_WIDTH,WINDOW_HEIGHT))
    img_wall_small = pygame.image.load("jumpjump/little_snowman.png")
    img_wall_small = pygame.transform.scale(img_wall_small, (56,70))
    snowball = pygame.image.load("jumpjump/snowball.png")
    snowball = pygame.transform.scale(snowball, (700,600))

    if pygame.mixer.music.get_busy() == True:
        pygame.mixer.music.stop()
    pygame.mixer.music.load("jumpjump/happyvillage.ogg")
    if pygame.mixer.music.get_busy() == False:
        pygame.mixer.music.play(-1)
        
    start_ticks = pygame.time.get_ticks()

    toben = Player(position = (300,630))
    boss = Boss(position = (750,200))
    
    wall_x_pos = 750.0
    wall_y_pos = 630.0
    
    wall_to_x = 0
    wall_speed = 0.3

    snow_x_pos = 150
    snow_y_pos = -600
    snow_to_y = 3

    life = Life()

    all_sprites = pygame.sprite.Group(toben)
    
    running = True
        
    while running:

        mt = clock.tick(FPS) / 1000

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE]):
            if toben.jump == True:
                toben.velocity_y = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    toben.direction = "left"                    
                    toben.state = 1
                    
                if event.key == pygame.K_RIGHT:
                    toben.direction = "right"                    
                    toben.state = 1
                
                if event.key == pygame.K_SPACE and toben.rect.y == GROUND:
                   toben.jump = True
                   toben.velocity_y = -50.0
                   jump_sound.play()
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    toben.velocity_x = 0
                    toben.state = 0
                if event.key == pygame.K_SPACE:
                    toben.velocity_y = 0
                    
            if toben.velocity_y > 0 and toben.rect.y >= GROUND:
                toben.rect.y = GROUND
                toben.jump = False
                
            toben.velocity_y += GRAVITY
            toben.rect.y += toben.velocity_y

        
        if wall_x_pos < toben.rect.right and wall_y_pos < toben.rect.bottom and wall_x_pos + 56 > toben.rect.left:
            wall_to_x = 750
            life.damage()
        else:
            wall_to_x = wall_speed
            
        wall_x_pos -= wall_to_x * 30

        if (wall_x_pos + 56) < 0:
            wall_speed = 0.3
            wall_x_pos = 750

        snow_y_pos += snow_to_y
        if snow_y_pos > 1300:
            snow_y_pos = -600

        if (snow_y_pos + 600) > toben.rect.y and snow_y_pos < toben.rect.top and (snow_x_pos + 600) > toben.rect.x and snow_x_pos < toben.rect.right:
            life.damage()
            snow_y_pos = -600

        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        timer = font.render('Time: {}'.format(int(elapsed_time)), True, WHITE)
        if int(elapsed_time) == 60:
            gameclear()
            
        all_sprites.update(mt)
        screen.blit(img_bg, (0, 0))
        screen.blit(timer, (10, 10))
        screen.blit(img_wall_small,[wall_x_pos,wall_y_pos])
        screen.blit(snowball,[snow_x_pos,snow_y_pos])
        
        life.draw()
        
        all_sprites.draw(screen)
        boss.draw()
        pygame.display.update()
        toben.check_screen()
        if gamequit == True:
            pygame.time.delay(5000)
            pygame.quit()
            quit()

if __name__ == '__main__':
    title() 