import pygame
groune_speed = 3
class coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images =[]
        self.index = 0
        self.couter =0
        for num in range(1, 7):
            img = pygame.image.load(fr'images\coin{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center =[x, y]

    def update(self):
        self.couter += 1
        flap_cooldown =5

        if self.couter>flap_cooldown:
            self.couter = 0
            self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index] 
        self.image = pygame.transform.rotate(self.images[self.index], 1)    

        
        self.rect.x -= groune_speed
        if self.rect.right < 0:
            self.kill()
   