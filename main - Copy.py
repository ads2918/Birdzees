import pygame
from spritesheet import Spritesheet
pygame.init()
#finish moving bird to class
#let go of left bird turns right
#birdzees intro 
#moving background
#enemies
#need to make it back to the nest
screen_width = 1500
screen_height = 960
win = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Birdzees")
bg = pygame.image.load('images/forestBG.jpg')
bg = pygame.transform.smoothscale(bg, win.get_size())
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()



           
def redrawGameWindow():
    #win.blit(bg, (0,0))
    pygame.display.update()
 
#main loop
index = 0
run = True

class player(object):
    def __init__(self,x,y):
        my_spritesheet = Spritesheet('images/bird-sprite.png')
        sprite = [my_spritesheet.parse_sprite('bird1.png'), my_spritesheet.parse_sprite('bird2.png'),my_spritesheet.parse_sprite('bird3.png'),my_spritesheet.parse_sprite('bird4.png'),my_spritesheet.parse_sprite('bird5.png'),my_spritesheet.parse_sprite('bird6.png')]
        self.x = x
        self.y = y
        self.right = 0
        self.left = 0
        self.sprite = sprite
        
    def draw(self,win):
        index = 0
        if self.right == 1:
           self.x = self.x + 1 * dt
           self.y = self.y - .3 * dt
           index = (index + 1) % len(self.sprite)
        elif self.left == 1:
           index = (index + 1) % len(self.sprite)
           self.x = self.x - 1 * dt
           self.y = self.y - .3 * dt
        else:
           self.y = self.y + .3 * dt
        
        if self.y > (screen_height - 350):
            self.y = screen_height - 350
        elif self.y <= 0:
            self.y = 0
        
        if self.x <= 0:
            self.x = 0
            
        if self.left == 1:
            img_copy = self.sprite[index].copy() 
            img_with_flip = pygame.transform.flip(img_copy, True, False) 
            win.blit(img_with_flip,(self.x,self.y))
        else:
            win.blit(bird.sprite[index], (self.x,self.y))
            
bird = player(0,screen_height - 250) 
bird2 = player(400,screen_height - 100)      
while run:
    dt = clock.tick(20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                bird.right = 0
                bird.left = 1
            if event.key == pygame.K_RIGHT:
                bird.right = 1
                bird.left = 0
        if event.type == pygame.KEYUP:   
            if event.key == pygame.K_LEFT:
                bird.right = 0
                bird.left = 0
            if event.key == pygame.K_RIGHT:
                bird.right = 0
                bird.left = 0
                  
    win.blit(bg, (0,0))  
    bird.draw(win)
    bird2.draw(win)
    pygame.display.update()    
    
pygame.quit()