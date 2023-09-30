import pygame
from pygame.locals import *
import sys
from plane import *
from pipe import *
from coin import *
from button import Button
import random
#fps
pygame.init()
clock = pygame.time.Clock()


# define game variable
WIDTH = 864
HEIGHT = 450
high_score = 0
#define front
game_font =pygame.font.Font(r'04B_19.TTF', 40)
    
# define colors
white = (255, 255, 255)
black = (0, 0, 0)
yellow =(255, 255, 0)
#screen 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Plane')

#load image 
bg = pygame.image.load(r'images\bg.png')
# class text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
def reset_game():
    pipe_group.empty()
    coin_group.empty()
    pla.rect.x = 100
    pla.rect.y = HEIGHT//2
    
# bird
plane_group = pygame.sprite.Group()
pla=Plane(100, HEIGHT//2)
plane_group.add(pla)

#pipe
pipe_group = pygame.sprite.Group()

# coin
coin_group = pygame.sprite.Group()
pass_coin = False


# menu
bg_menu = pygame.image.load('images/bg_nen.png')
pause_nen = pygame.image.load('images/pause_nen.png')
#load img button 
play_img = pygame.image.load('images/play.png')
settings_img = pygame.image.load('images/settings.png')
exit_img = pygame.image.load('images/exit.png')
pause_img = pygame.image.load('images/pause.png')
home_img = pygame.image.load('images/menu.png')
cotinu_img = pygame.image.load('images/con.png')
replay_img= pygame.image.load('images/re.png')
nen_img= pygame.image.load('images/pause_nen.png')
back_img = pygame.image.load('images/back.png')

#creat button
play_button = Button(WIDTH//2 +100 , 50, play_img)
settings_button = Button(WIDTH//2+100, 170, settings_img)
exit_button = Button(WIDTH//2+100, 290, exit_img)
pause_button = Button(0,0, pause_img)

home_button = Button(WIDTH//2+100, HEIGHT//2, home_img)
cotinu_button = Button(WIDTH//2-100, HEIGHT//2, cotinu_img)
replay_button =Button(WIDTH//2, HEIGHT//2, replay_img)

nen1_button = Button(200, 200, nen_img)
back_button =  Button(0, 0, back_img)
# value -> check button
# sound

hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

def menu_loop():
    menu_state = "main"
    run = True
    while run :
        
        screen.blit(bg_menu, (0, 0))
        reset_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if menu_state == "main":
            if play_button.draw(screen):
                main_loop(high_score)
                run = False
            if settings_button.draw(screen):
                settings(bg)
            if exit_button.draw(screen):
                run = False
                pygame.quit()
                sys.exit()
        pygame.display.update()
def settings(bg):
    run = True
    while run:
        screen.blit(bg,(0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if nen1_button.draw(screen):
            bg = bg_menu
        if back_button.draw(screen):
            menu_loop()
            run =False
        pygame.display.update()

def main_loop(high_score):
    fps =60
    score = 0
    time_frequen = 450
    time_last = pygame.time.get_ticks() - time_frequen

    time_last_coin = pygame.time.get_ticks() - time_frequen

    time = pygame.time.get_ticks()
    run = True
    while run:

    # chay chuong trinh chinh   
        clock.tick(fps)
        #draw bg
        
        screen.blit(bg,(0, 0))

        #draw bird
        plane_group.draw(screen)
        plane_group.update()

        #draw pipe
        pipe_group.draw(screen)
        
        #coin
        coin_group.draw(screen)
        # check pause
        if pause_button.draw(screen):
            pla.flying =False
            pause()
        
        #check the score
        if  len(coin_group) >0:
            if plane_group.sprites()[0].rect.colliderect(coin_group.sprites()[0]):
                score+=1
                score_sound.play()
                high_score = max(high_score, score)
                coin_group.sprites()[0].kill()
            
        draw_text("SCORE : "+str(score), game_font, yellow, WIDTH//2-100, 60)
        
        #check the collision
        if pygame.sprite.groupcollide(plane_group, pipe_group, False, False) or pla.rect.top < 0:
            hit_sound.play()
            pla.game_over = True
            
        # check the bird hit the ground
        if pla.rect.bottom >=500:
            pla.flying = False
            pla.game_over = True

        
        if pla.game_over == False and pla.flying == True:
            #generate pipe
            time_now = pygame.time.get_ticks()
            
            if time_now - time_last > time_frequen :
                pipe_height = random.randint(-100, 100)
                pipe_top = Pipe(WIDTH, HEIGHT//2 + pipe_height, 1)
                pipe_bmt = Pipe(WIDTH, HEIGHT//2 + pipe_height, -1)
                pipe_group.add(pipe_bmt)
                pipe_group.add(pipe_top)
                time_last = time_now
        
            if time_now - time_last_coin> random.randint(3000, 7000):
                pipe_height = random.randint(-100, 100)
                coi = coin(WIDTH + pipe_height, HEIGHT//2 + pipe_height)
                coin_group.add(coi)
                time_last_coin = time_now 
            #generate coins 
            pipe_group.update() 
            coin_group.update()  

        #check gameover and restart
        if pla.game_over == True:
            draw_text("HIGH_SCORE "+ str(high_score), game_font, yellow, WIDTH//2 - 120 , 10)
            pipe_group.empty()
            coin_group.empty()
            
            if replay_button.draw(screen) == True:
                pla.game_over = False
                pla.flying = False
                score = 0
                reset_game()
            
        #main loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.MOUSEBUTTONDOWN )and pla.flying == False and pla.game_over == False:
                pla.flying = True
                

        if pygame.time.get_ticks() - time > 20000:
            time = pygame.time.get_ticks()
            fps += 10

        pygame.display.update()

def pause():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if home_button.draw(screen) :
                run =False
                menu_loop()
            
        if replay_button.draw(screen) :
            run =False
            reset_game()
            main_loop(high_score)
            
        if cotinu_button.draw(screen):
            run = False
            pla.flying = True
            
        pygame.display.update()
    
menu_loop()