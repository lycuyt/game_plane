import pygame
from video import threadVideo
# xyz = threadVideo()
# xyz.start()
class Plane(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images =[]
        self.index = 0
        self.couter =0
        for num in range(1, 5):
            img = pygame.image.load(fr'images\plan{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center =[x, y]
        self.vel = 0
        self.clicked = False
        self.flying = False
        self.game_over = False
        self.sound = pygame.mixer.Sound('sound/sfx_wing.wav')

    def update(self):
        if self.flying == True:
            #gravity
            self.vel += 0.15
            if self.vel>8:
                self.vel =8

            if self.rect.bottom < 600:
                self.rect.y += int(self.vel)

        #jump
        if self.game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.sound.play()
                self.clicked = True
                self.vel = -4
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # if xyz.dist < 0.1 and self.clicked == False:
            #     self.clicked = True
            #     self.vel = -3
            # if xyz.dist>=0.1:
            #     self.clicked = False
            
            #handle animation
            self.couter += 1
            flap_cooldown =5

            if self.couter>flap_cooldown:
                self.couter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)