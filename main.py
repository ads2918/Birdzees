import pygame, sys, random
from spritesheet import Spritesheet
import time
import tkinter as tk
from tkinter import simpledialog
import json
import time
import csv
import pandas as pd

window = tk.Tk()
window.withdraw()
pygame.init()

screen_width = 1700
screen_height = 696
win = pygame.display.set_mode((screen_width,screen_height))

BLACK = (0,0,0)
black_area_height = 400  # Example: 50 pixels tall
# black_area_rect = pygame.Rect(0, screen_height,win.get_width(), black_area_height)
pygame.display.set_caption("Birdzees")
game_config_file = "game.json"
clock = pygame.time.Clock()  
def redrawGameWindow():
    #win.blit(bg, (0,0))
    pygame.display.update()
 

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
    def __init__(self,x,y,enemy_type = 1,block_active = 0,boss = 0):
        self.mask = False
        self.x = x
        self.y = y
        self.x_original = x
        self.y_original = y
        self.direction = 'up'
        self.index = 0
        self.hit = 0
        self.dead = 0
        self.attacking = 0
        self.boss = boss
        self.hit_count = 0
        self.boss_dir = 'left'
        self.block_active = block_active
        self.enemy_type = enemy_type
        self.healthBar = False 
        self.hide_boss_health_bar = False
        
        if self.boss:
            self.healthBar = healthBar((screen_width/2) - 30,35)  
            
        if enemy_type == 2:
            self.speed = 10
        elif enemy_type == 3:
            self.speed = 15
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
        if self.boss and self.hide_boss_health_bar == False:
            self.healthBar.y = self.y - 20
            self.healthBar.x = self.x
            self.healthBar.draw(win,dt)
            
        if self.hit:
            self.hit_count  += 1
            self.speed += .3
            
            if self.boss:
                if self.hit_count % 3 == 0:
                    self.healthBar.hit = 1
                
            if (self.hit_count >= 27 and self.boss) or not self.boss:
                self.draw_die(win,dt)
                self.hide_boss_health_bar = True
            elif self.attacking:
                self.draw_attack(win,dt)
            else:
                self.hit = 0
                self.draw_fly(win,dt)
       
        elif self.attacking:
            self.draw_attack(win,dt)
        else:
            self.draw_fly(win,dt)
       
    def draw_fly(self,win,dt): 
        
        if self.boss:
            if self.x <= 0:
               self.x = self.x + self.speed
               self.boss_dir = 'right'
            elif self.x >= screen_width - 250 :
               self.x = self.x - self.speed
               self.boss_dir = 'left'
            elif self.boss_dir == 'left':
              self.x = self.x - self.speed
            elif self.boss_dir == 'right':
              self.x = self.x + self.speed
        else:
            self.x = self.x - self.speed
        if self.index >= len(self.fly):
            self.index = 0

        if self.enemy_type != 3:
            if self.direction == 'up':
                if self.y_original - 250 >= self.y:
                    self.y = self.y + self.speed
                    self.direction = 'down'
                else:
                    self.y = self.y - self.speed
                    self.direction = 'up'
        else:
            if self.direction == 'up':
                if self.y_original - 350 >= self.y:
                    self.y = self.y + self.speed
                    self.direction = 'down'
                else:
                    self.y = self.y - self.speed
                    self.direction = 'up'
                    
        if self.direction == 'down':
            self.y = self.y + self.speed
            if self.y >= self.y_original:
                self.direction = 'up'
        
        if self.boss:
            x_scale = 300
            y_scale = 300
        else:
            x_scale = 100
            y_scale = 100
        
        if self.boss and self.boss_dir == 'right':
            img_copy = self.fly[self.index].copy() 
            image = pygame.transform.flip(img_copy, True, False) 
            image = pygame.transform.scale(image, (x_scale,y_scale))
        else:  
            image = pygame.transform.scale(self.fly[self.index], (x_scale,y_scale))
            
        self.mask = pygame.mask.from_surface(image)  
        win.blit(image, (self.x,self.y))
        self.index += 1
        
    def draw_die(self,win,dt):

        if self.index == 0:
            sound = pygame.mixer.Sound('sounds/enemy-die.mp3')
            sound.set_volume(0.5)
            sound.play()
        
        if self.boss:
            x_scale = 300
            y_scale = 300
        else:
            x_scale = 100
            y_scale = 100
            
        if self.index < len(self.fly): 
            image = pygame.transform.scale(self.die[self.index], (x_scale,y_scale))
            self.mask = pygame.mask.from_surface(image)  
            win.blit(image, (self.x,self.y))
        else:
            self.dead = 1
        
        self.index += 1
     
    def draw_attack(self,win,dt):
        #if self.index == 0:
           #coin_sound = pygame.mixer.Sound('sounds/died.mp3')
           #coin_sound.play()
        
        if self.boss:
            x_scale = 300
            y_scale = 300
        else:
            x_scale = 100
            y_scale = 100
            
        if self.index < len(self.attack): 
            image = pygame.transform.scale(self.attack[self.index], (x_scale,y_scale))
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
        self.freeze = 0
        self.dead = 0
        self.dead_animation_complete = 0
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
        if not self.freeze:
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

        if self.dead:
            self.y += 20
            if self.y > screen_height:
                self.dead_animation_complete = 1

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
        text_surface = my_font.render(str(self.coins), False, (255, 255, 255))
        win.blit(text_surface, (60,50))
        
        add_on = int(len(str(self.score))) * 20
        my_font = pygame.font.SysFont('Comic Sans MS', 20)
        text_surface = my_font.render('Score: '+ str(self.score), False, (255, 255, 255))
        win.blit(text_surface, (screen_width - (75 + add_on),50))
        
        single_coin =  pygame.image.load('images/single-coin.png')
        win.blit(single_coin,(0,39))
        
    def die(self):
        self.left = 0
        self.right = 0
        self.dead = 1
        self.my_spritesheet = Spritesheet('images/bird-sprite-died.png')
        self.sprite = [self.my_spritesheet.parse_sprite('bird1.png'),self.my_spritesheet.parse_sprite('bird2.png'),self.my_spritesheet.parse_sprite('bird3.png'),self.my_spritesheet.parse_sprite('bird4.png'),self.my_spritesheet.parse_sprite('bird5.png'),self.my_spritesheet.parse_sprite('bird6.png')]
        tweat = pygame.mixer.Sound('sounds/tweet.mp3')
        tweat.play()
        
class bullet(object):
    def __init__(self):
        self.bullet_img = pygame.transform.scale(pygame.image.load('images/Bullet-3.png'), (25,25)) 
        self.mask = pygame.mask.from_surface(self.bullet_img)
        self.x = 0
        self.y = 0
        self.direction = False
        self.dead = 0
    def draw(self,win,dt,player_x,player_y,direction):
        if not self.dead:
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

class scroll(object):
    def __init__(self,x,y,txt):
        self.x = x
        self.y = y
        self.txt = txt
        
    def draw(self,win):
        self.y -= 1
        my_font = pygame.font.SysFont('Comic Sans MS', 20)
        text_surface = my_font.render(self.txt, False, (255, 255, 255))
        center = text_surface.get_rect(center=(screen_width/2, self.y))
        win.blit(text_surface,center)
     
class game(object):
    def __init__(self):
        self.level = 0
        self.level_shown = 0
        self.bg_w= screen_width
        self.bg_h = screen_height
        self.bg = 1 #setting to 1 as placeholder until set in set_level
        self.total_levels = 2 #count starts at zero
        self.coins = []
        self.bats = []
        self.enemies = []
        self.screen_total_blocks = 0
        self.screen_block = 0
        self.config_file = game_config_file
        self.game_configs  = []

    def get_configs(self):
        with open(self.config_file) as f:
           game_configs = json.load(f)
        f.close()
        return game_configs
        
    def reset_game(self):
        self.level = 0
        self.level_shown = 0
        self.bg_w= screen_width
        self.bg_h = screen_height
        self.bg = 1 #setting to 1 as placeholder until set in set_level
        self.total_levels = 2 #count starts at zero
        self.coins = []
        self.bats = []
        self.enemies = []
        self.screen_total_blocks = 0
        self.screen_block = 0
        self.set_level()
        
    def set_level(self):
        self.screen_block = 0
        self.level += 1 
        self.level_shown = 0
        self.game_configs = self.get_configs()
        total_levels = len(self.game_configs["levels"])
        level_config = self.game_configs["levels"][str(self.level)]  
        coin_lines = level_config["coin_lines"]
        
        #sets coins from config 
        for key in coin_lines.keys():
            self.coins += draw_coin_line(coin_lines[key]["total_coins"],coin_lines[key]["start_x"],coin_lines[key]["y"],coin_lines[key]["horizontal"])
            
        #set level bg
        self.bg =  pygame.transform.smoothscale(pygame.image.load(level_config["background_path"]), (self.bg_w,self.bg_h))
        
        #level music
        music = pygame.mixer.music.load(level_config["music_path"])
        pygame.mixer.music.play(-1)
        
        #set block totals for iteration of background for length of level
        self.screen_total_blocks = level_config["total_blocks"]
        
        bat1 = bat(screen_width - 32,250)
        self.bats.append(bat1)
        bat2 = bat(250,screen_height)
        self.bats.append(bat2)
        bat3 = bat(250,screen_height)
        self.bats.append(bat3)
        bat4 = bat(250,screen_height)
        self.bats.append(bat4)
        bat5 = bat(55,screen_height)
        
        #set enemies to pull from config as well
        self.set_enemies() 
         
    def set_enemies(self):
        self.enemies = []
        total_levels = len(self.game_configs["levels"])
        level_config = self.game_configs["levels"][str(self.level)]  
        enemy_lines = level_config["enemies"]
        boss_lines = level_config["boss"]
        
        for key in enemy_lines.keys():
            self.enemies.append(enemy(enemy_lines[key]["x"],enemy_lines[key]["y"],enemy_lines[key]["enemy_type"],enemy_lines[key]["block_active"]))
            
        for key in boss_lines.keys():
            self.enemies.append(enemy(boss_lines[key]["x"],boss_lines[key]["y"],boss_lines[key]["enemy_type"],boss_lines[key]["block_active"],1))    
 
    def display_level(self,win):
        level = pygame.font.SysFont('Comic Sans MS', 30)
        level = level.render('Level '+ str(self.level), False, (0, 0, 0))
        level =  pygame.image.load('images/level_' + str(self.level) +'.png')
        level_1_center = level.get_rect(center=(screen_width/2, screen_height/2))
        
        if self.level_shown == 0:
            win.blit(level,level_1_center)
            pygame.display.update()       

            time.sleep(2)
            self.level_shown = 1
            return False
        else:
            return True
    
    def game_over(self,win):
        my_font = pygame.font.SysFont('Comic Sans MS', 30) 
        text_surface = my_font.render('GAME OVER BIRDMASTER', False, (66, 245, 144))
        center = text_surface.get_rect(center=(screen_width/2, screen_height/2))
        win.blit(text_surface, center)

        text_surface2 = my_font.render('Press Space to Retry', False, (66, 245, 144))
        center = text_surface2.get_rect(center=(screen_width/2, (screen_height/2) + 100))
        win.blit(text_surface2, center)
        
def main_menu(win,bg_w,bg_h,pause_flag = 0):
    start_bg =  pygame.transform.smoothscale(pygame.image.load('images/start.png'), (bg_w, bg_h))
    logo =  pygame.image.load('images/logo.png')
    press_select = pygame.font.SysFont('Comic Sans MS', 30)
    if pause_flag == 1:
        start = press_select.render('Paused', False, (0, 0, 0))
        start2 = press_select.render('Press Space', False, (0, 0, 0))
    else:
       start = press_select.render('Press Space', False, (0, 0, 0))
     
    music = pygame.mixer.music.load('sounds/forest.mp3')
    pygame.mixer.music.play(-1)
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                return False;
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE:
                    menu = False

        win.blit(start_bg, (0, 0))
        win.blit(logo,((screen_width/2 -194),(screen_height/2)))
        
        if pause_flag == 1:
            win.blit(start,((screen_width/2-70),(screen_height/2 + 100)))
            win.blit(start2,((screen_width/2 - 100),(screen_height/2) + 200))
        else:
            win.blit(start,((screen_width/2 - 100),(screen_height/2) + 200))
            
        pygame.display.update()
    return True
    
def myround(x, base=5):
    return base * round(x/base)
    
class nest(object):
    def __init__(self):
        self.nest_img =  pygame.image.load('images/treehouse.png')
        self.mask = pygame.mask.from_surface(self.nest_img)
        self.x = screen_width
        self.y = 0
        self.direction = False
        self.mask 
    def draw(self,win):
        win.blit(self.nest_img,(self.x,screen_height - 512))
            
def on_button_click_cooldown(cooldown_seconds):
    global _last_click_time
    if not '_last_click_time' in globals():
       _last_click_time = 0
        
    current_time = time.time()
    if current_time - _last_click_time < cooldown_seconds:
        return False

    _last_click_time = current_time
    return True
    
def highscore_save(bird):           
    user_input = simpledialog.askstring("You win!", "Enter your name:")
    data = [user_input,bird.coins + bird.score]
    with open("high_scores.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(data)
    
    #reopen file and sort by highscore 
    df = pd.read_csv('high_scores.csv', header=None)
    df_sorted = df.sort_values(by=1, ascending=False)
    df_sorted.to_csv('high_scores.csv', index=False, header=False)
    
def highscores_scroll():
    scroll_y = 0
    scrolling = []
    scroll_total = screen_height
    
    with open('high_scores.csv', 'r') as file:
        reader = csv.reader(file) 
        scrolling.append(scroll(50,scroll_total,"HIGH SCORES"))
        scroll_total = scroll_total + 40
        for row in reader:
            scroll_total = scroll_total + 25
            scrolling.append(scroll(50,scroll_total,row[0] +" - "+ row[1]))
            
    return scrolling



        
game = game()
start_game = main_menu(win,game.bg_w,game.bg_h)  

if start_game:# if menu bypassed
    bird = player(0,screen_height - 250)
    game.set_level()
    finish = nest()
    bullets = []
    screen_block = 1
    bg_x = 0 
    last_x_rel = 0
    level_shown = 0
    last_shoot = 0
    user_input = ''
    highscore_scroll = 0
    reset_shoot = 0
    high_score_set = 0
    scroll_stop = False
    
while run and start_game:
    dt = clock.tick(15)
    if level_shown:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if not bird.dead:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        bird.right = 0
                        bird.left = 1
                        bird.last_direction = 'left'
                    if event.key == pygame.K_RIGHT:
                        bird.right = 1
                        bird.left = 0
                        bird.last_direction = 'right'
                    if event.key == pygame.K_ESCAPE:
                        main_menu(win,game.bg_w,game.bg_h,1)
                    if event.key == pygame.K_SPACE:
                        #can_shoot = on_button_click_cooldown(.5)
                        #if can_shoot:
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
            elif bird.dead and bird.dead_animation_complete and scroll_stop == False:
                if event.type == pygame.KEYDOWN:#resets game if player died
                    if event.key == pygame.K_SPACE:
                        game.reset_game()
                        bird = player(0,screen_height - 250)
                        finish = nest()
                        #game.set_level()
                        bullets = []
                        screen_block = 1
                        bg_x = 0 
                
                        last_x_rel = 0
                        level_shown = 0
                        last_shoot = 0
                        user_input = ''
                        highscore_scroll = 0
                        reset_shoot = 0
                        high_score_set = 0
     
    #allows coins to move as background moves 
    if scroll_stop != True:       
        if bird.right == 1 and not bird.dead:
            if game.screen_total_blocks >= game.screen_block:
                bg_x -= 10
                for coinObj in game.coins:
                    coinObj.x -= 10
 
    x_rel = bg_x % game.bg_w
    x_part2 = x_rel - game.bg_w if x_rel > 0 else x_rel + game.bg_w    
    if x_rel == 0 and last_x_rel != x_rel:
        #game.set_enemies()  
        game.screen_block += 1
    
 
    win.blit(game.bg, (x_rel, 0))
    win.blit(game.bg, (x_part2, 0))
    level_shown = game.display_level(win)
    
    #draw nest if last block for level completion
    if(game.screen_total_blocks) <= (game.screen_block - 1):
        if scroll_stop == False:
            finish.draw(win)
            if finish.mask.overlap(bird.mask, offset(finish,bird)):
                if bird.freeze == 0:
                    win_sound = pygame.mixer.Sound('sounds/brass-fanfare-with-timpani-and-winchimes-reverberated-146260.mp3')
                    win_sound.play()
                    
                bird.freeze = 1
                pygame.font.init()
                my_font = pygame.font.SysFont('Comic Sans MS', 30) 
                text_surface = my_font.render('YOU WIN', False, (66, 245, 144))
       
                center = text_surface.get_rect(center=(screen_width/2, screen_height/2))
                win.blit(text_surface, center)
        
    if bird.freeze:
        if bird.x != 1150 and bird.y != 430:
            bird.y = myround(bird.y)
            if bird.y == 430:
                bird.y = 430
            elif bird.y >= 430:
                bird.y -= 3
            elif bird.y < 430:
                bird.y += 3
            
            bird.x = myround(bird.x)        
            if bird.x == 1150:
                bird.x = 1150
            elif bird.x >= 1150:
                bird.x -= 3
            elif bird.x < 1150:
                bird.x += 3
        else:
            # level_shown = 0
            #reset and change to next level
            if game.total_levels >= game.level:
                game.set_level()
                game.set_enemies() 
                 #reset bird position/unfreeze
                bird.x = 0
                bird.y = screen_height - 250
                bird.freeze = 0
            elif(high_score_set != 1):
                highscore_save(bird)
                high_score_set = 1
                high_scores = highscores_scroll()   
            elif(high_score_set):
                for highScore in high_scores:
                    highScore.draw(win)
       
    if scroll_stop != True:         
        if not bird.freeze:
            if bird.right == 1:
                if finish.x > (screen_width  - 450):
                    finish.x -= 10

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
    
    scroll_stop = False
    for enemy_obj in game.enemies:
        if enemy_obj.block_active <= game.screen_block:
            enemy_obj.draw(win,dt)
            if enemy_obj.boss and enemy_obj.dead != 1:
                scroll_stop = True
            if enemy_obj.dead != 1:
                if enemy_obj.mask.overlap(bird.mask, offset(enemy_obj,bird)):             
                    #bird.health -= 1
                    bird.die()        
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
            if enemy_obj.dead != 1 and enemy_obj.hit != 1 and enemy_obj.mask != False:
                if enemy_obj.mask.overlap(bullet_obj.mask, offset(enemy_obj,bullet_obj)):
                    enemy_obj.hit = 1
                    bird.score += 10
                    enemy_obj.index = 0
                    
                    bullet_obj.dead = 1        
                    bullet_obj.x = 0
                    bullet_obj.y = 0        
                    
                
    #kill game
    if bird.dead and bird.dead_animation_complete:
        game.game_over(win)
        pygame.font.init()
    else:
        bird.draw(win,dt)
    
            
    # pygame.draw.rect(win, BLACK, black_area_rect)   
    #game.healthBar.draw(win,dt)             
    pygame.display.update()
    last_x_rel = x_rel
    
pygame.quit()
