import pygame, sys, random
from spritesheet import Spritesheet
import time

pygame.init()
#finish moving bird to class
#https://graphicriver.net/item/flying-bugs-2d-game-chracter-sprites-148/13698892
#enemies
#need to make it back to the nest
screen_width = 1500
screen_height = 696
win = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Birdzees")
clock = pygame.time.Clock()  
def redrawGameWindow():
    #win.blit(bg, (0,0))
    pygame.display.update()
 
#main loop
index = 0
run = True
class bat(object):
    def __init__(self,x,y):
        self.mask = pygame.mask
        self.hit = 0
        my_spritesheet = Spritesheet('images/bat-sprite.png')
        sprite = [
            my_spritesheet.parse_sprite('bat1.png'),
            my_spritesheet.parse_sprite('bat2.png'),
            my_spritesheet.parse_sprite('bat3.png'),
            my_spritesheet.parse_sprite('bat4.png'),
        ]
            
        self.x = x
        self.y = y
        self.index = 0
        self.sprite = sprite
        
    def __setattr__(self, name, value):
        if name == 'hit':
            super().__setattr__(name, value)
            if value > 0:
                hit_sound = pygame.mixer.Sound('sounds/bump.mp3')
                hit_sound.play()
        else:
            super().__setattr__(name, value)
            
    def draw(self,win,dt):
        if self.hit:
            self.y = screen_height
            self.x = random.randint(1, screen_width)
            self.hit = 0
            
        self.x = self.x -5
        self.y = self.y - 8
        if self.y <= 32:
            self.y = screen_height
            self.x = random.randint(1, screen_width)
        if self.hit == 0:
            self.index += 1
            if self.index == len(self.sprite):
                self.index = 0
            self.mask = pygame.mask.from_surface(self.sprite[self.index])
            win.blit(self.sprite[self.index],(self.x,self.y))
            
class healthBar(object):
    def __init__(self,x,y):
        self.mask = pygame.mask
        self.hit = 0
        my_spritesheet = Spritesheet('images/health-bar.png')
        sprite = [
            my_spritesheet.parse_sprite('health-bar1.png'),
            my_spritesheet.parse_sprite('health-bar2.png'),
            my_spritesheet.parse_sprite('health-bar3.png'),
            my_spritesheet.parse_sprite('health-bar4.png'),
            my_spritesheet.parse_sprite('health-bar5.png'),
            my_spritesheet.parse_sprite('health-bar6.png'),
            my_spritesheet.parse_sprite('health-bar7.png'),
            my_spritesheet.parse_sprite('health-bar8.png'),
            my_spritesheet.parse_sprite('health-bar9.png'),
            my_spritesheet.parse_sprite('health-bar10.png'),
        ]
            
        self.x = x
        self.y = y
        self.index = 0
        self.sprite = sprite
  
    def draw(self,win,dt):
        if self.hit == 1:
            self.index += 1
            self.hit = 0

        if self.index == len(self.sprite):
            self.index = 0
        self.mask = pygame.mask.from_surface(self.sprite[self.index])
        win.blit(self.sprite[self.index],(self.x,self.y))

class enemy(object):
    def __init__(self,x,y,enemy_type = 1):
        self.mask = pygame.mask
        self.x = x
        self.y = y
        self.x_original = x
        self.y_original = y
        self.direction = 'up'
        self.index = 0
        self.hit = 0
        self.dead = 0
        self.attacking = 0
        
        if enemy_type == 2:
            self.speed = 10
        else:
            self.speed = 6
            
        if enemy_type == 0:
            enemy_add = ''
        else:
            enemy_add = enemy_type
            
        self.fly = [
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Fly_000.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Fly_001.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Fly_002.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Fly_003.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Fly_004.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Fly_005.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Fly_006.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Fly_007.png')      
        ]
        
        self.attack = [
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Attack_000.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Attack_001.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Attack_002.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Attack_003.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Attack_004.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Attack_005.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Attack_006.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Attack_007.png')      
        ]
        
        self.die = [
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Die_000.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Die_001.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Die_002.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Die_003.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Die_004.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Die_005.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Die_006.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Die_007.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Die_008.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Die_009.png'),
            pygame.image.load('images/enemy_'+ str(enemy_type) +'/Die_010.png')                 
        ]
    
    def draw(self,win,dt):
        if self.hit:
            self.draw_die(win,dt)
        elif self.attacking:
            self.draw_attack(win,dt)
        else:
            self.draw_fly(win,dt)
       
    def draw_fly(self,win,dt): 
        self.x = self.x - self.speed
        
        if self.index >= len(self.fly):
            self.index = 0
        
        if self.direction == 'up':
            if self.y_original - 250 >= self.y:
                self.y = self.y + self.speed
                self.direction = 'down'
            else:
                self.y = self.y - self.speed
                self.direction = 'up'
        
        if self.direction == 'down':
            self.y = self.y + self.speed
            if self.y >= self.y_original:
                self.direction = 'up'
            
        image = pygame.transform.scale(self.fly[self.index], (100,100))
        self.mask = pygame.mask.from_surface(image)  
        win.blit(image, (self.x,self.y))
        self.index += 1
        
    def draw_die(self,win,dt):
        if self.index == 0:
            sound = pygame.mixer.Sound('sounds/died.mp3')
            sound.play()
        
        if self.index < len(self.fly): 
            image = pygame.transform.scale(self.die[self.index], (100,100))
            self.mask = pygame.mask.from_surface(image)  
            win.blit(image, (self.x,self.y))
        else:
            self.dead = 1
        
        self.index += 1
     
    def draw_attack(self,win,dt):
        #if self.index == 0:
           #coin_sound = pygame.mixer.Sound('sounds/died.mp3')
           #coin_sound.play()
        
        if self.index < len(self.attack): 
            image = pygame.transform.scale(self.attack[self.index], (100,100))
            self.mask = pygame.mask.from_surface(image)  
            win.blit(image, (self.x - 5,self.y))
        else:
            self.index = 0
            
        self.index += 1
                  
class coin(object):
    def __init__(self,x,y):
        self.mask = pygame.mask
        self.hit = 0
        my_spritesheet = Spritesheet('images/coin-sprite.png')
        sprite = [
            my_spritesheet.parse_sprite('coin1.png'),
            my_spritesheet.parse_sprite('coin2.png'),
            my_spritesheet.parse_sprite('coin3.png'),
            my_spritesheet.parse_sprite('coin4.png'),
            my_spritesheet.parse_sprite('coin5.png'),
            my_spritesheet.parse_sprite('coin6.png'),
            my_spritesheet.parse_sprite('coin7.png'),
            my_spritesheet.parse_sprite('coin8.png'),
            my_spritesheet.parse_sprite('coin9.png')
            #my_spritesheet.parse_sprite('coin10.png')
        ]
            
        self.x = x
        self.y = y
        self.index = 0
        self.sprite = sprite
  
    def draw(self,win,dt):
        if self.hit == 0:
            self.index += 1
            if self.index == len(self.sprite):
                self.index = 0
            self.mask = pygame.mask.from_surface(self.sprite[self.index])
            win.blit(self.sprite[self.index],(self.x,self.y))
        
class player(object):
    def __init__(self,x,y):
        my_spritesheet = Spritesheet('images/bird-sprite.png')
        sprite = [my_spritesheet.parse_sprite('bird1.png'), my_spritesheet.parse_sprite('bird2.png'),my_spritesheet.parse_sprite('bird3.png'),my_spritesheet.parse_sprite('bird4.png'),my_spritesheet.parse_sprite('bird5.png'),my_spritesheet.parse_sprite('bird6.png')]
        self.x = x
        self.y = y
        self.mask = pygame.mask.from_surface(my_spritesheet.parse_sprite('bird1.png'))
        self.last_direction = 'right'
        self.right = 0
        self.left = 0
        self.coins = 0
        self.sprite = sprite
        self.index = 0
        self.health = 1
        self.shooting = 0
        self.collision = 0
        self.score = 0
    def __setattr__(self, name, value):
        if name == 'coins':
            super().__setattr__(name, value)
            if value > 0:
                coin_sound = pygame.mixer.Sound('sounds/coin.mp3')
                coin_sound.play()
        else:
            super().__setattr__(name, value)
       
    def draw(self,win,dt):
        index = 0 
        if self.collision:
            self.x = self.x
            self.y = self.y
        else: 
            
            if self.right or self.left:
                self.index += 1
                
            if  self.health > 0:
                if self.right == 1:
                   self.x = self.x + .7 * dt
                   self.y = self.y - .2 * dt
                   self.index = (self.index  + 1) % len(self.sprite)
                elif self.left == 1:
                   index = (index + 1) % len(self.sprite)
                   self.x = self.x - .7 * dt
                   self.y = self.y - .2 * dt
                else:
                   self.y = self.y + .2 * dt
                   #index = (index + 1) % len(self.sprite)
                
                if self.index == len(self.sprite):
                    self.index = 0
                
                if self.y > (screen_height - 200):
                    self.y = screen_height - 200
                elif self.y <= 0:
                    self.y = 0
                elif self.x < 100:
                    self.x = 100
                
                if self.x >= screen_width - 500:
                    self.x = screen_width - 500
            
            # if self.shooting:
                # bullet()
                # bullet.draw(win,dt,self.x,self.y)
            
        
        if self.left == 1 or self.last_direction == 'left':
            img_copy = self.sprite[self.index].copy() 
            img_with_flip = pygame.transform.flip(img_copy, True, False) 
            self.mask = pygame.mask.from_surface(img_with_flip)
            win.blit(img_with_flip,(self.x,self.y))
        else:
            self.mask = pygame.mask.from_surface(self.sprite[self.index])
            win.blit(self.sprite[self.index], (self.x,self.y))
            
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 20)
        text_surface = my_font.render(str(self.coins), False, (66, 245, 144))
        win.blit(text_surface, (50,50))
        
        add_on = int(len(str(self.score))) * 20
        my_font = pygame.font.SysFont('Comic Sans MS', 20)
        text_surface = my_font.render('Score: '+ str(self.score), False, (66, 245, 144))
        win.blit(text_surface, (screen_width - (75 + add_on),50))
        
        single_coin =  pygame.image.load('images/single-coin.png')
        win.blit(single_coin,(-8,45))

class bullet(object):
    def __init__(self):
        self.bullet_img = pygame.transform.scale(pygame.image.load('images/Bullet-3.png'), (25,25)) 
        self.mask = pygame.mask.from_surface(self.bullet_img)
        self.x = 0
        self.y = 0
        self.direction = False
        self.mask 
    def draw(self,win,dt,player_x,player_y,direction):
        if self.direction == False:
            self.direction = direction
            
        if self.x == 0:
            hit_sound = pygame.mixer.Sound('sounds/shoot.mp3')
            hit_sound.play()
            if self.direction == 'right':
                self.x = player_x + 50 + 10
            else:
                self.x = player_x - 50 -  10               
            self.y = player_y + 40
        else:
            if self.direction == 'right':
                self.x = self.x + 15
            else:
                self.x = self.x - 15
        self.mask = pygame.mask.from_surface(self.bullet_img)
        
        if self.direction == 'left':
            img_copy = self.bullet_img.copy() 
            bullet_img = pygame.transform.flip(img_copy, True, False)
            win.blit(bullet_img, (self.x,self.y))
        else:
            win.blit(self.bullet_img, (self.x,self.y))
        
def draw_coin_line(total_coins = 1,start_x = 0,y = 0,horzonital = 1):
    CoinArray = [] 
    for i in range(total_coins):
        if horzonital:
            start_x = start_x + 60
        else:
            y = y - 60
            
        coinObj = coin(start_x ,y)   
        CoinArray.append(coinObj)
    return CoinArray

def offset(mask1, mask2):
    return int(mask2.x - mask1.x), int(mask2.y - mask1.y)
      
class game(object):
    def __init__(self):
        self.level = 1
        self.level_shown = 0
        self.bg_w= screen_width
        self.bg_h = screen_height
        self.bg = 1 #setting to 1 as placeholder until set in set_level
        self.coins = []
        self.bats = []
        self.enemies = []
        self.screen_total_blocks = 0
        self.screen_block = 0
        #self.healthBar = healthBar(screen_width - 280,35)
    def set_level(self):
        if self.level == 1:
            self.bg =  pygame.transform.smoothscale(pygame.image.load('images/vecteezy_alien-planet-game-background_6316482.jpg'), (self.bg_w,self.bg_h))
            self.screen_total_blocks = 2
            music = pygame.mixer.music.load('sounds/Three-Little-Birds.mid')
            pygame.mixer.music.play(-1)
            coinObjs = draw_coin_line(3,250,screen_height - 500,1)
            coinObjs2 = draw_coin_line(3,125,250,1)
            coinObjs3 = draw_coin_line(3,700,400,0)
            coinObjs4 = draw_coin_line(3,750,400,0)
            coinObjs5 = draw_coin_line(3,900,250,1)
            coinObjs5 = draw_coin_line(9,1500,250,1)
            coinObjs6 = draw_coin_line(5,2500,500,0)
            self.coins = coinObjs + coinObjs2 + coinObjs3 + coinObjs4 + coinObjs5 + coinObjs6

            bat1 = bat(screen_width - 32,250)
            self.bats.append(bat1)
            bat2 = bat(250,screen_height)
            self.bats.append(bat2)
            bat3 = bat(250,screen_height)
            self.bats.append(bat3)
            bat4 = bat(250,screen_height)
            self.bats.append(bat4)
            bat5 = bat(55,screen_height)
            
            self.set_enemies()
            
    def set_enemies(self):
        if self.screen_block == 0:
            enemy1 = enemy(screen_width - 150,screen_height - 250)
            enemy2 = enemy(screen_width + 150,screen_height - 150)
            enemy3 = enemy(screen_width + 150,screen_height - 50)
            enemy4 = enemy(screen_width + 75,screen_height - 300)
            enemy5 = enemy(screen_width + 75,screen_height - 100)

            enemy6 = enemy(screen_width + 300,screen_height - 300)
            enemy7 = enemy(screen_width + 300,screen_height - 100)
            enemy8 = enemy(screen_width + 500,screen_height - 100,2)
            enemy9 = enemy(screen_width + 500,screen_height - 300,2)
            enemy10 = enemy(screen_width + 500,screen_height - 400,2)
            enemy11 = enemy(screen_width + 500,screen_height - 500)

            self.enemies.append(enemy1)
            self.enemies.append(enemy2)
            self.enemies.append(enemy3)

            self.enemies.append(enemy7)
            self.enemies.append(enemy8)
            self.enemies.append(enemy9)
            self.enemies.append(enemy10)
            self.enemies.append(enemy11)
            
        if self.screen_block == 1:
            enemy4 = enemy( 25, screen_height - 250)
            enemy5 = enemy((screen_width * self.screen_block) + 25, screen_height - 150)
            enemy6 = enemy((screen_width * self.screen_block) + 25, screen_height - 50)
            self.enemies.append(enemy4)
            self.enemies.append(enemy5)
            self.enemies.append(enemy6)
        
        if self.screen_block == 2:
            enemy4 = enemy( 25, screen_height - 250)
            enemy5 = enemy((screen_width * (self.screen_block + 1)) + 25, screen_height - 150)
            enemy6 = enemy((screen_width * (self.screen_block + 1)) + 25, screen_height - 50)
            self.enemies.append(enemy4)
            self.enemies.append(enemy5)
            self.enemies.append(enemy6)
            
        # if self.screen_block == 3:
            # enemy4 = enemy( 25, screen_height - 250)
            # enemy5 = enemy((screen_width * (self.screen_block + 1)) + 25, screen_height - 150)
            # enemy6 = enemy((screen_width * (self.screen_block + 1)) + 25, screen_height - 100)
            # self.enemies.append(enemy4)
            # self.enemies.append(enemy5)
            # self.enemies.append(enemy6) 
                
        # if self.screen_block == 4:
            # enemy4 = enemy( 25, screen_height - 250)
            # enemy5 = enemy((screen_width * (self.screen_block + 1)) + 25, screen_height - 150)
            # enemy6 = enemy((screen_width * (self.screen_block + 1)) + 25, screen_height - 50)
            # self.enemies.append(enemy4)
            # self.enemies.append(enemy5)
            # self.enemies.append(enemy6)   


        
    def display_level(self,win):
        level = pygame.font.SysFont('Comic Sans MS', 30)
        level = level.render('Level '+ str(self.level), False, (0, 0, 0))
        level =  pygame.image.load('images/level_1.png')
        level_1_center = level.get_rect(center=(screen_width/2, screen_height/2))
        
        if self.level_shown == 0:
            win.blit(level,level_1_center)
            pygame.display.update()   
            time.sleep(2)
            self.level_shown = 1

def main_menu(win,bg_w,bg_h):
    start_bg =  pygame.transform.smoothscale(pygame.image.load('images/start.png'), (bg_w, bg_h))
    logo =  pygame.image.load('images/logo.png')
    press_select = pygame.font.SysFont('Comic Sans MS', 30)
    start = press_select.render('Press Space', False, (0, 0, 0))
    music = pygame.mixer.music.load('sounds/forest.mp3')
    pygame.mixer.music.play(-1)
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    menu = False

        win.blit(start_bg, (0, 0))
        win.blit(logo,((screen_width/2 -194),(screen_height/2)))
        win.blit(start,((screen_width/2 - 100),(screen_height/2) + 200))
        pygame.display.update()

game = game()   
#main_menu(win,game.bg_w,game.bg_h)  

bird = player(0,screen_height - 250)


shoot = False
game.set_level()
bullets = []
bg_x = 0
screen_block = 1
level_shown = 0
last_x_rel = 0

nest = pygame.image.load('images/treehouse.png')
nest_x = screen_width
while run:
    dt = clock.tick(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and bird.health > 0:
            if event.key == pygame.K_LEFT:
                bird.right = 0
                bird.left = 1
                bird.last_direction = 'left'
            if event.key == pygame.K_RIGHT:
                bird.right = 1
                bird.left = 0
                bird.last_direction = 'right'
            if event.key == pygame.K_ESCAPE:
                main_menu(win)
                
            if event.key == pygame.K_SPACE:
                bird.shooting = 1
                shoot = bullet()
                bullets.append(shoot)
        if event.type == pygame.KEYUP:   
            if event.key == pygame.K_LEFT:
                bird.right = 0
                bird.left = 0
                bird.last_direction = 'left'
            if event.key == pygame.K_RIGHT:
                bird.right = 0
                bird.left = 0
                bird.last_direction = 'right'
 
    #allows coins to move as background moves 
    if bird.right == 1:
        if game.screen_total_blocks >= game.screen_block:
            bg_x -= 10
            for coinObj in game.coins:
                coinObj.x -= 10
 
    x_rel = bg_x % game.bg_w
    print(x_rel)
    x_part2 = x_rel - game.bg_w if x_rel > 0 else x_rel + game.bg_w    
    if x_rel == 0 and last_x_rel != x_rel:
        game.set_enemies()  
        game.screen_block += 1
    
 
    win.blit(game.bg, (x_rel, 0))
    win.blit(game.bg, (x_part2, 0))
    game.display_level(win)
    
    #draw nest if last block 
    if (game.screen_total_blocks) <= (game.screen_block - 1):
        win.blit(nest,(nest_x,screen_height - 512))
        if bird.right == 1:
            if nest_x > 450:
                nest_x -= 10

    #check if coin collides with player
    for coinObj in game.coins:
        coinObj.draw(win,dt)
        if coinObj.hit  != 1:
            if coinObj.mask.overlap(bird.mask, offset(coinObj,bird)):
                coinObj.hit = 1
                bird.coins += 1

    #check if bat collides with player (originally enemies but making just backgound visual)
    for batObj in game.bats:
        batObj.draw(win,dt)  
       
    for enemy_obj in game.enemies:
        enemy_obj.draw(win,dt)
        if enemy_obj.dead != 1:
            if enemy_obj.mask.overlap(bird.mask, offset(enemy_obj,bird)):             
               
                bird.health = bird.health - .40
                if bird.health <= 0 and bird.health >= -.80:
                    tweat = pygame.mixer.Sound('sounds/tweet.mp3')
                    tweat.play()
                    
                if bird.health < -15:
                    enemy_obj.attacking = 0
                else:
                    bird.collision = 1
                    enemy_obj.attacking = 1
            else: 
               enemy_obj.attacking = 0
               
    #bullet loop
    for bullet_obj in bullets:
        bullet_obj.draw(win,dt,bird.x,bird.y,bird.last_direction)
        for enemy_obj in game.enemies:
            if enemy_obj.dead != 1 and enemy_obj.hit != 1:
                if enemy_obj.mask.overlap(bullet_obj.mask, offset(enemy_obj,bullet_obj)):
                    enemy_obj.hit = 1
                    bird.score += 10
                    enemy_obj.index = 0 
                
    #kill game
    if bird.health <= 0:
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 30) 
        text_surface = my_font.render('GAME OVER BIRDMASTER', False, (66, 245, 144))
        center = text_surface.get_rect(center=(screen_width/2, screen_height/2))
        win.blit(text_surface, center)
    else:
        bird.draw(win,dt)
    
    #game.healthBar.draw(win,dt)             
    pygame.display.update()
    last_x_rel = x_rel
    
pygame.quit()
