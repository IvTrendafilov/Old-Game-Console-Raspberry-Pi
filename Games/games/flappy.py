import shelve
import time
import pygame, sys, random
from .settings import *
#import RPi.GPIO as GPIO


def draw_pillars(pillars):
    global pillar_surface
    for pillar in pillars:
        if pillar.bottom >= HEIGHT:
            screen.blit(pillar_surface, pillar)
        else:
            flip_pillar = pygame.transform.flip(pillar_surface, False, True)
            screen.blit(flip_pillar, pillar)


def draw_floor():
    global floor_surface
    global floor_x_pos
    screen.blit(floor_surface, (floor_x_pos, HEIGHT - 124))
    screen.blit(floor_surface, (floor_x_pos + WIDTH, HEIGHT - 124))


def create_pillar():
    global pillar_surface
    global pillar_height
    random_pillar_height = random.choice(pillar_height)
    bottom_pillar = pillar_surface.get_rect(midtop=(WIDTH + 124, random_pillar_height))
    top_pillar = pillar_surface.get_rect(midbottom=(WIDTH + 124, random_pillar_height - 300))
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
            collision = True
    if bird_rectangle.top <= -100 or bird_rectangle.bottom >= 900:
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
    new_bird_rect = new_bird.get_rect(center=(100, bird_rectangle.centery))
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
    score_rectangular = score_surface.get_rect(center=(288, 100))
    screen.blit(score_surface, score_rectangular)




def main():
    # Game initialization
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

    ##############################SURFACES############################

    # Background surface
    background_surface = pygame.image.load('./games/assets/background-day.png').convert()
    background_surface = pygame.transform.scale2x(background_surface)

    # Game Over surface
    gameOver_surface = pygame.image.load('./games/assets/gameover.png').convert_alpha()
    gameOver_surface = pygame.transform.scale2x(gameOver_surface)
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
    bird_rectangle = bird_surface.get_rect(center=(100, 512))

    BIRDFLAP = pygame.USEREVENT + 1

    bird_flap_interval = 200
    pygame.time.set_timer(BIRDFLAP, bird_flap_interval)

    # Pillar Surface
    global pillar_surface
    pillar_surface = pygame.image.load('./games/assets/pipe-green.png').convert()
    pillar_surface = pygame.transform.scale2x(pillar_surface)
    pillar_list = []
    SPAWNPILLAR = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPILLAR, pillar_spawn_interval)
    global pillar_height
    pillar_height = [400, 600, 800]
    passed_pillars = []

    while True:

        # GPIO.setup(15, GPIO.OUT)
        # GPIO.output(15, GPIO.LOW)
        # GPIO.setup(15, GPIO.IN)  # ARROW UP
        # if GPIO.input(15) and game_active:
        #     bird_movement = 0
        #     bird_movement -= 10
        #     time.sleep(0.1)
        # if GPIO.input(15) and game_active==False:
        #     game_active = True
        #     pillar_list.clear()
        #     score = 0
        #     passed_pillars.clear()
        #     bird_rectangle.center = (100, 512)
        #     bird_movement = 0
        #     time.sleep(0.1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= 10

                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    pillar_list.clear()
                    score = 0
                    passed_pillars.clear()
                    bird_rectangle.center = (100, 512)
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

