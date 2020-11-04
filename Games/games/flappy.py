import shelve
import time
import pygame, sys, random
from .settings import *
import RPi.GPIO as GPIO


def draw_pillars(pillars):
    global pillar_surface
    for pillar in pillars:
        if pillar.bottom >= HEIGHT - 124:
            screen.blit(pillar_surface, pillar)
        else:
            flip_pillar = pygame.transform.flip(pillar_surface, False, True)
            screen.blit(flip_pillar, pillar)


def draw_floor():
    global floor_surface
    global floor_x_pos
    screen.blit(floor_surface, (floor_x_pos, HEIGHT/1.2))
    screen.blit(floor_surface, (floor_x_pos + WIDTH, HEIGHT/1.2))


def create_pillar():
    global pillar_surface
    global pillar_height
    random_dividedPillar = random.randint(13, 30)
    random_dividedPillar = float(random_dividedPillar / 10)
    random_pillar_height = HEIGHT / random_dividedPillar
    #random_pillar_height = random.choice(pillar_height)
    bottom_pillar = pillar_surface.get_rect(midtop=(WIDTH + 124, random_pillar_height))
    top_pillar = pillar_surface.get_rect(midbottom=(WIDTH + 124, random_pillar_height - HEIGHT/3.5))
    return bottom_pillar, top_pillar


def move_pillars(pillars):
    for pillar in pillars:
        pillar.centerx -= 5
    return pillars


def check_collision(pillars):
    global bird_rectangle
    collision = False
    for pillar in pillars:
        if bird_rectangle.colliderect(pillar):
            hit_sound.play()
            collision = True
    if bird_rectangle.top <= -HEIGHT/10 or bird_rectangle.bottom >= HEIGHT/1.23:
        hit_sound.play()
        collision = True
    return collision


def rotate_bird(bird):
    global bird_movement
    new_bird = pygame.transform.rotozoom(bird, bird_movement * 3, 1)
    return new_bird


def bird_animation():
    global bird_frames
    global bird_index
    global bird_rectangle
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(WIDTH/5, bird_rectangle.centery))
    return new_bird, new_bird_rect


def score_display(game_status):
    if game_status == "ongoing":
        show_score(game_status)





def show_score(game_status):
    global score
    if game_status == "over":
        score_type = f'Score: {int(score)}'
    else:
        score_type = f'{int(score)}'
    global game_font
    score_surface = game_font.render(score_type, True, (255, 255, 255))
    score_rectangular = score_surface.get_rect(center=(WIDTH, HEIGHT/1.7))
    screen.blit(score_surface, score_rectangular)




def main():
    # Game initialization
    pygame.mixer.pre_init(44100, 16, 2, 512)
    pygame.init()

    clock = pygame.time.Clock()
    global score
    score = 0
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    global game_font
    font_name = pygame.font.match_font('roboto')
    game_font = pygame.font.Font(font_name, 40)
    # Game variables
    gravity = 0.25
    global bird_movement
    bird_movement = 0
    game_active = True


    # X and Y varriables
    global floor_x_pos
    floor_x_pos = 0
    bird_pos_x = 100
    bird_pos_y = 512
    pillar_spawn_interval = 1200
    ##############################SOUND##############################
    global bird_sound
    bird_sound = pygame.mixer.Sound("./games/assets/sfx_wing.wav")
    global point_sound
    point_sound = pygame.mixer.Sound("./games/assets/sfx_point.wav")
    global hit_sound
    hit_sound = pygame.mixer.Sound("./games/assets/sfx_hit.wav")

    ##############################SURFACES############################

    # Background surface
    background_surface = pygame.image.load('./games/assets/background-day.png').convert()
    background_surface = pygame.transform.rotozoom(background_surface, 0, 2.5)

    # Game Over surface
    gameOver_surface = pygame.image.load('./games/assets/gameover.png').convert_alpha()
    #gameOver_surface = pygame.transform.scale2x(gameOver_surface)
    game_over_rectangle = gameOver_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    # Floor surface
    global floor_surface
    floor_surface = pygame.image.load('./games/assets/base.png').convert()
    floor_surface = pygame.transform.scale2x(floor_surface)

    # Initial Game Display
    game_idle_image = pygame.transform.scale2x(
        pygame.image.load("./games/assets/message.png")).convert_alpha()
    game_idle_rectangle = game_idle_image.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    # Bird surface
    bird_midflap = pygame.transform.scale2x(
        pygame.image.load('./games/assets/bluebird-midflap.png').convert_alpha())
    bird_upflap = pygame.transform.scale2x(
        pygame.image.load("./games/assets/bluebird-upflap.png"))
    bird_downflap = pygame.transform.scale2x(
        pygame.image.load("./games/assets/bluebird-downflap.png"))
    global bird_frames
    bird_frames = [bird_upflap, bird_midflap, bird_downflap]
    global bird_index
    bird_index = 0
    bird_surface = bird_frames[bird_index]
    global bird_rectangle
    global bird_height
    bird_height = HEIGHT / 2.5
    global bird_width
    bird_width = WIDTH / 5.7
    bird_rectangle = bird_surface.get_rect(center=(bird_width,bird_height))

    BIRDFLAP = pygame.USEREVENT + 1

    bird_flap_interval = 200
    pygame.time.set_timer(BIRDFLAP, bird_flap_interval)

    # Pillar Surface
    global pillar_surface
    pillar_surface = pygame.image.load('./games/assets/pipe-green.png').convert()
    #pillar_surface = pygame.transform.scale2x(pillar_surface)
    pillar_list = []
    SPAWNPILLAR = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPILLAR, pillar_spawn_interval)
    global pillar_height
    #pillar_height = [400, 600, 800]
    passed_pillars = []

    while True:

        GPIO.setup(15, GPIO.OUT)
        GPIO.output(15, GPIO.LOW)
        GPIO.setup(15, GPIO.IN)  # ARROW UP
        if GPIO.input(15) and game_active:
            bird_movement = 0
            bird_movement -= 4
            time.sleep(0.1)
        if GPIO.input(15) and game_active==False:
            game_active = True
            pillar_list.clear()
            score = 0
            passed_pillars.clear()
            bird_rectangle.center = (100, 512)
            bird_movement = 0
            time.sleep(0.1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= 8

                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    pillar_list.clear()
                    score = 0
                    passed_pillars.clear()
                    bird_rectangle.center = (bird_width,bird_height)
                    bird_movement = 0

            if event.type == SPAWNPILLAR:
                pillar_list.extend(create_pillar())

            if event.type == BIRDFLAP:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0
                bird_surface, bird_rectangle = bird_animation()

        screen.blit(background_surface, (0, 0))
        if game_active:
            game_status = "ongoing"

            # Bird
            score = int(len(passed_pillars) / 2)
            bird_movement += gravity
            bird_rectangle.centery += bird_movement
            rotated_bird = rotate_bird(bird_surface)
            screen.blit(rotated_bird, bird_rectangle)
            game_active = not check_collision(pillar_list)

            # Pillars
            pillar_list = move_pillars(pillar_list)
            draw_pillars(pillar_list)
            score_display(game_status)

            for pillar in pillar_list:
                if bird_pos_x > pillar.centerx:
                    if pillar not in passed_pillars:
                        passed_pillars.append(pillar)
                        point_sound.play()
        else:
            return score
            # screen.blit(game_idle_image, game_idle_rectangle)
            # game_status = "over"
            # high_score = update_highScore(score, int(high_score))
            # save_highScore()
            # score_display(game_status)
            # if event.type == pygame.K_SPACE:
            #     screen.blit(gameOver_surface, game_idle_rectangle)

        # Floor
        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -WIDTH:
            floor_x_pos = 0

        pygame.display.update()
        clock.tick(120)

