import pygame
import os
import time
import random
import sys
import json
from operator import itemgetter
from button import Button


pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1100,720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter ")
score = 0

# Load image
RED_SPACE_SHIP = pygame.image.load(os.path.join("draw","Red_ship.PNG"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("draw","Green_ship.PNG"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("draw","Blue_ship.PNG"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("draw","Yellow_ship.PNG"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("draw","Red_laser.PNG"))
GREEN_LASER = pygame.image.load(os.path.join("draw","Green_laser.PNG"))
BLUE_LASER = pygame.image.load(os.path.join("draw","Blue_laser.PNG"))
YELLOW_LASER = pygame.image.load(os.path.join("draw","Yellow_laser.PNG"))

# Background
BG = pygame.image.load(os.path.join("draw","Background_black.PNG"))

# Sound BG
SOUND_BG = pygame.mixer.music.load(os.path.join("draw","tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.play(-1)

# Sound 
SOUND_LASER = pygame.mixer.Sound(os.path.join("draw","sounds_Laser_Shoot6.wav"))
SOUND_TOOM = pygame.mixer.Sound(os.path.join("draw","sounds_Explosion5.wav"))
SOUND_TOOM2 = pygame.mixer.Sound(os.path.join("draw","sounds_expl6.wav"))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)  

    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 20

    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y 
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(objs):
                objs.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1 

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            SOUND_LASER.play()

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score = 0

    def move_lasers(self, vel, objs):
        self.cooldown()
        global score
        
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)
                        self.score += 1
                        SOUND_TOOM.play()
                        

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
                    
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() , self.ship_img.get_width() , 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() , self.ship_img.get_width() * ( self.health/self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
                "red":(RED_SPACE_SHIP,RED_LASER),
                "green":(GREEN_SPACE_SHIP,GREEN_LASER),
                "blue":(BLUE_SPACE_SHIP,BLUE_LASER)
                }
    def __init__(self, x, y, color, health = 100): 
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.direction = 1

    def move(self, vel):
        self.y += vel
        if (self.x +self.get_width() + vel <= WIDTH and self.direction == 1):
            self.x += vel
        else:
            self.direction = 0

        if (self.x + vel >= 0 and self.direction == 0):
            self.x -= vel
        else:
            self.direction = 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
        

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x 
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) !=None 



def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    score = 0
    main_font = pygame.font.SysFont("comicsans", 50)
    title_font = pygame.font.SysFont("comicsans",100)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 7

    player = Player(450,475)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0 

    def redraw_window(player):
        WIN.blit(BG, (0,0))
        #drawtext
        lives_label = main_font.render(f"lives:{lives}", 1 ,(255,255,255))
        level_label = main_font.render(f"level:{level}", 1 ,(255,255,255)) 
        score_label = main_font.render(f"score: {player.score}", 1, (255,255,255))
      
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label, (WIDTH - score_label.get_width() - 10, 55))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            """ Show game over WIN """

            name = ''

            while 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                        elif event.key == pygame.K_RETURN:
                            if name != '':

                                with open('score.json', 'r') as file:
                                    playerScore = json.load(file)

                                playerScore.append([name.upper(),int(player.score)])
                                playerScore = sorted(playerScore,reverse = True, key = itemgetter(1))
                                if len(playerScore) > 5:
                                    playerScore.pop()

                                with open('score.json', 'w+') as file:
                                    json.dump(playerScore,file)

                                main_menu()

                        else:
                            name += event.unicode
                            if len(name) >= 13:
                                name = name[:-1]

                WIN.blit(BG, (0,0))
                WIN.blit(title_font.render("GAME OVER", True, pygame.Color('crimson')), [250, 140]) 
                WIN.blit(main_font.render("ENTER YOUR NAME", True, pygame.Color('orange')), [300, 400])
                WIN.blit(main_font.render(name.upper(), True, pygame.Color('white')), [450, 490])
                pygame.display.flip()         

            lost_label = lost_font.render("You Lose!!", 1 , (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run: 
        clock.tick(FPS)
        redraw_window(player)

        if lives <= 0 or player.health <= 0 :
                lost = True
                lost_count += 1

        if lost:
            if lost_count > FPS * 3 :
                run = False

            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(100, WIDTH-150   ),random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed() #move
        if keys[pygame.K_a]and player.x - player_vel > 0:#left
            player.x -= player_vel
        if keys[pygame.K_d]and player.x + player_vel + player.get_width() < WIDTH:#right
            player.x += player_vel
        if keys[pygame.K_w]and player.y - player_vel > 0:#up
            player.y -= player_vel
        if keys[pygame.K_s]and player.y + player_vel + player.get_height() + 10 < HEIGHT:#down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0,2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies) 

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("draw/font.ttf", size)
         

def main_menu():
    title_font = pygame.font.SysFont("comicsans",100)
    word_font =pygame.font.SysFont("comicsans",60)
    name_font =pygame.font.SysFont("comicsans",15)

    run = True 
    while run :
        WIN.blit(BG, (0, 0))
        title_label = name_font.render("65010437 THANANPHON BUATHONG", 1, (255,255,255))
        WIN.blit(title_label, (800, 675))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("SPACE SHOOTER", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(550, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("draw/Play Rect.png"), pos=(550, 250), 
                            text_input="PLAY", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        SCORE_BUTTON = Button(image=pygame.image.load("draw/Options Rect.png"), pos=(550, 400), 
                            text_input="SCORE", font=get_font(60), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("draw/Quit Rect.png"), pos=(550, 550), 
                            text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="White")

        WIN.blit(MENU_TEXT, MENU_RECT)
    

        for button in [PLAY_BUTTON, SCORE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()
                if SCORE_BUTTON.checkForInput(MENU_MOUSE_POS):
                   
                    WIN.blit(BG, (0, 0))
                    WIN.blit(title_font.render("SCOREBOARD", True, pygame.Color('purple')), [200, 40])

                    with open('score.json', 'r') as file:
                        playerScore = json.load(file)

                    alltext = []
                    for i,data in enumerate(playerScore):
                        name = str(data[0])
                        score = str(data[1])
                        alltext.append([name,score])
                        WIN.blit(word_font.render(str(i+1)+'.', True, pygame.Color('lavender')), [350, 200+80*i])
                        WIN.blit(word_font.render(name, True, pygame.Color('white')), [480, 200+80*i])
                        WIN.blit(word_font.render(score.rjust(10), True, pygame.Color('lavender')), [560, 200+80*i])

                    pygame.display.flip()

                    while 1:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                quit()
                            if event.type == pygame.KEYDOWN:
                                keys = pygame.key.get_pressed()
                                if keys[pygame.K_q]:
                                    main_menu()

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
    pygame.quit()
    
main_menu()

