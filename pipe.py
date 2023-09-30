import pygame
# define game variable
p_gap = 300
groune_speed = 3
#xclass
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(r'images\pipe2.png')
        self.rect = self.image.get_rect()
        self.pipe_gap = p_gap
        # position = 1 from the top , = -1 from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y-self.pipe_gap//2]
        if position == -1:
            self.rect.topleft = [x, y+self.pipe_gap//2]
    
    def update(self):
        self.rect.x -= groune_speed
        if self.rect.right < 0:
            self.kill()


    