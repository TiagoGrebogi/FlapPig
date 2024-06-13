import pygame
import random

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Pig')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

try:
    bird_img = pygame.image.load('bird.png')
    bird_img = pygame.transform.scale(bird_img, (128, 128))
    background_img = pygame.image.load('background.png')
    background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    pipe_img = pygame.image.load('pipe.png')
    pipe_img = pygame.transform.scale(pipe_img, (80, 600))
    death_img = pygame.image.load('death.png')
    death_img = pygame.transform.scale(death_img, (1920, 1080))
except pygame.error as e:
    print(f"Erro ao carregar a imagem: {e}")
    pygame.quit()
    exit()

background_img.set_alpha(128)

bird_rect = bird_img.get_rect()
bird_rect.center = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)

GRAVITY = 2.5
BIRD_JUMP = -20
pipe_width = 80
pipe_height = 600
pipe_gap = 300
pipe_velocity = -20
score_points = True
bird_velocity = 0
pipes = []
score = 0
running = True
game_over = False
death_sound_played = False
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
font_end = pygame.font.Font(None, 72)

def create_pipe():
    pipe_x = SCREEN_WIDTH
    pipe_y = random.randint(-300, 0)
    return pygame.Rect(pipe_x, pipe_y, pipe_width, pipe_height)

def display_score(score):
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))
    


pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)

death_sound = pygame.mixer.Sound('death_sound.mp3')


while running:
    screen.fill(BLACK)

    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = BIRD_JUMP
            if event.key == pygame.K_ESCAPE:
                running = False

    if not game_over:
        bird_velocity += GRAVITY
        bird_rect.y += bird_velocity

        if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH // 2:
            pipes.append(create_pipe())

        for pipe in pipes:
            pipe.x += pipe_velocity
            if pipe.x < -pipe_width:
                pipes.remove(pipe)
            screen.blit(pipe_img, pipe)
            bottom_pipe = pygame.Rect(pipe.x, pipe.y + pipe_height + pipe_gap, pipe_width, 
            SCREEN_HEIGHT - pipe.y - pipe_height - pipe_gap)
            screen.blit(pygame.transform.flip(pipe_img, False, True), bottom_pipe)

        if pipes and pipes[0].x + pipe_width < bird_rect.centerx:
            score += 1
            pipes.pop(0)

        if bird_rect.y > SCREEN_HEIGHT or bird_rect.y < 0:
            game_over = True

        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                game_over = True

        screen.blit(bird_img, bird_rect)

    else:
        screen.blit(death_img, (0, 0))
        pygame.mixer.music.stop()
        final_score_text = font_end.render(f'Final Score: {score}', True, BLACK)
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 50))

        if not death_sound_played:
            death_sound.play()
            death_sound_played = True
            score_points = False

    if score_points:
        display_score(score)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()

