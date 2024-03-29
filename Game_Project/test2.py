import pygame
import os
import time
import random

pygame.font.init()

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
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                            self.score += 1
                        

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

    def move(self, vel):
        self.y += vel

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
                quit()

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

def main_menu():
    title_font = pygame.font.SysFont("comicsans",100)
    word_font =pygame.font.SysFont("comicsans",60)
    name_font =pygame.font.SysFont("comicsans",15)
    
    run = True
    while run :
        WIN.blit(BG, (0,0))
        title_label = title_font.render("SPACE SHOOTER", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 100))
        title_label = word_font.render("Press the mouse to begin...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 400))
        title_label = name_font.render("65010437 THANANPHON BUATHONG", 1, (255,255,255))
        WIN.blit(title_label, (800, 675))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
    
main_menu()
