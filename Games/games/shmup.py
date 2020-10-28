import os
import random
import time
import RPi.GPIO as GPIO
import pygame
from pygame import mixer

dir_path = os.path.dirname(os.path.realpath(__file__))
img_folder = os.path.join(dir_path, "./Sprites")
WIDTH = 600
HEIGHT = 600
FPS = 60

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)




class Player(pygame.sprite.Sprite):
    # Sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 22
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.speed_y = 0
        self.shield = 100
        self.shoot_delay = 300
        self.last_time_shot = pygame.time.get_ticks()

    def update(self):
        self.speed_x = 0
        #GPIO CONTROLLERS SETUP
        GPIO.setup(13,GPIO.OUT)
        GPIO.output(13,GPIO.LOW)
        GPIO.setup(15, GPIO.OUT)
        GPIO.output(15, GPIO.LOW)
        GPIO.setup(40, GPIO.OUT)
        GPIO.output(40, GPIO.LOW)
        GPIO.setup(15,GPIO.IN) #ARROW UP
        GPIO.setup(13,GPIO.IN) #ARROW DOWN
        GPIO.setup(40,GPIO.IN) #ARROW DOWN
        if GPIO.input(15):
            self.speed_x = 9
        if GPIO.input(13):
            self.speed_x = -9
        if GPIO.input(40):
            self.shoot()
    

#         if keys[pygame.K_LEFT]:
#             self.speed_x = -9
#         if keys[pygame.K_RIGHT]:
#             self.speed_x = 9
#         if keys[pygame.K_SPACE]:
#             self.shoot()
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_time_shot > self.shoot_delay:
            self.last_time_shot = time_now
            laser_sound = mixer.Sound(os.path.join(img_folder, "Sounds/laser_sound.ogg"))
            laser_sound.set_volume(0.3)
            laser_sound.play()
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = random.choice(loaded_meteors)
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-160, -100)
        self.speed_x = random.randrange(-4, 4)
        self.speed_y = random.randrange(4, 9)
        self.rotation = 0
        self.rotation_speed = random.randrange(-7, 7)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 55:
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            self.image = pygame.transform.rotate(self.image_original, self.rotation)

    def update(self):
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 20 or self.rect.left < -30 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-160, -100)
            self.speed_x = random.randrange(-5, 5)
            self.speed_y = random.randrange(5, 10)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (8, 25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()


# Sprite class for explosion
class Explosion(pygame.sprite.Sprite):
    # Constructor takes as a parameter center and size, in order to make the explosion appear in the right place
    # --> center of meteor
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animations[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.frame_rate = 60
        self.last_update = pygame.time.get_ticks()

    def update(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > self.frame_rate:
            self.last_update = time_now
            self.frame += 1
            if self.frame == len(explosion_animations[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_animations[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


font_name = pygame.font.match_font('roboto')


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    # figure out what pixels you need to use in order to draw them in the used font
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_shield_bar(surface, x, y, shield_percentage):
    if shield_percentage < 0:
        shield_percentage = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 12
    bar = (shield_percentage / 100) * BAR_LENGTH
    rect_outline = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    rect_fill = pygame.Rect(x, y, bar, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, rect_fill)
    pygame.draw.rect(surface, WHITE, rect_outline, 3)


def spawn_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)


def display_game_over():
    timeRemaining = 3
    wait = True
    while wait:
        screen.blit(background, background_rect)
        draw_text(screen, "SHOOT 'EM ALL!", 64, WIDTH / 2, HEIGHT / 4)
        draw_text(screen, "Arrow keys for movement, Space to shoot", 30, WIDTH / 2, HEIGHT / 2)
        draw_text(screen, "Your game will begin in " + str(timeRemaining), 25, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if timeRemaining == 0:
            wait = False
        timeRemaining=timeRemaining-1
        time.sleep(1)





def main():
    # Set up assets folders


    # Initialize the game and create window
    pygame.init()
    mixer.init()
    mixer.music.load(os.path.join(img_folder, "Sounds/background.wav"))
    mixer.music.set_volume(0.02)
    mixer.music.play(-1)
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SHOOT EM' UP!")
    pygame.display.set_icon(pygame.image.load(os.path.join(img_folder, "PNG/Enemies/spaceship.png")))
    global clock
    clock = pygame.time.Clock()
    # Load all graphics
    global background
    background = pygame.image.load(os.path.join(img_folder, "Backgrounds/space_background.png")).convert()
    global background_rect
    background_rect = background.get_rect()
    global player_img
    player_img = pygame.image.load(os.path.join(img_folder, "PNG/player.png")).convert()
    global bullet_img
    bullet_img = pygame.image.load(os.path.join(img_folder, "PNG/Lasers/my_laser.png")).convert()
    meteors_path = os.path.join(img_folder, "PNG/Meteors")
    global loaded_meteors
    loaded_meteors = []
    meteors_sprites = ["meteorBrown_med1.png", "meteorBrown_med3.png", "meteorBrown_big3.png", "meteorBrown_small1.png"]
    for img in meteors_sprites:
        loaded_meteors.append(pygame.image.load(os.path.join(meteors_path, img)).convert())

    # Load explosions
    explosions_path = os.path.join(img_folder, "Explosions")
    global explosion_animations
    explosion_animations = {'lg': [], 'sm': []}
    for i in range(9):
        file = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(os.path.join(explosions_path, file)).convert()
        img.set_colorkey(BLACK)
        img_lg = pygame.transform.scale(img, (60, 60))
        explosion_animations['lg'].append(img_lg)
        img_sm = pygame.transform.scale(img, (30, 30))
        explosion_animations['sm'].append(img_sm)

    # Game loop
    is_running = True
    is_game_over = True
    while is_running:
        if is_game_over:
            display_game_over()
            is_game_over = False
            global all_sprites
            all_sprites = pygame.sprite.Group()
            global enemies
            enemies = pygame.sprite.Group()
            global bullets
            bullets = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            score = ['Score: ', 0]
            for i in range(10):
                spawn_enemy()

        # Keep clock running at a constant speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mixer.quit()
                pygame.display.set_caption("Main Menu!")
                pygame.display.set_icon(pygame.image.load("images/retroIcon.png"))
                is_running = False

        # Update
        all_sprites.update()

        # Check for collision between player and enemies (Game over when player is hit)
        hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= hit.radius * 1.2
            if player.shield <= 0:
                explosion_sound = mixer.Sound(os.path.join(img_folder, "Sounds/explosion_player.wav"))
                explosion_sound.set_volume(0.1)
                explosion_sound.play()
                screen.blit(background, background_rect)
                mixer.quit()
                pygame.display.set_caption("Main Menu!")
                pygame.display.set_icon(pygame.image.load("images/retroIcon.png"))
                return score[1]

        # Check for collision between player's bullets and enemies
        # Hits is used as a list for all sprites that hit the player (thus reducing the shield)
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score[1] += 1
            explosion_sound = mixer.Sound(os.path.join(img_folder, "Sounds/explosion.wav"))
            explosion_sound.set_volume(0.01)
            explosion_sound.play()
            explosion = Explosion(hit.rect.center, 'lg')
            all_sprites.add(explosion)
            spawn_enemy()

        # Draw/render
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        draw_text(screen, str(score[0] + str(score[1])), 27, WIDTH - 50, 15)
        draw_shield_bar(screen, 8, 8, player.shield)
        pygame.display.flip()


