import pygame
import os

FPS = 60
VELOCITY = 2
VELOCITY_BIRD = 4
WIDTH, HEIGHT = 288, 512
IS_PLAYING = False
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background.png")), (WIDTH, HEIGHT))
BASE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "base.png")), (WIDTH, HEIGHT // 3))
BIRD = pygame.image.load(os.path.join("Assets", "bird.png"))
pygame.font.init()
HEALTH_FONT = pygame.font.SysFont("comicsans", 25)
FONT = pygame.font.SysFont("comicsans", 30)
FINAL_FONT = pygame.font.SysFont("comicsans", 30)
PIPE = pygame.image.load(os.path.join("Assets", "pipe.png"))
PIPE = pygame.transform.scale(PIPE, (52, 200))
pipes = []
SCORE = 0


def draw_window(bird):
    WINDOW.blit(BACKGROUND, (0, 0))
    WINDOW.blit(BASE, (0, 450))
    if not IS_PLAYING:
        WINDOW.blit(BIRD, (10, 356))
        text = FONT.render("Press Enter to start", False, (255, 255, 255))
        WINDOW.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    elif IS_PLAYING:
        WINDOW.blit(BIRD, (bird.x, bird.y))
        score = HEALTH_FONT.render(f"Score : {SCORE}", False, (255, 255, 255))
        for pipe in pipes:
            if pipes.index(pipe) == 0:
                WINDOW.blit(pygame.transform.rotate(PIPE, 180), (pipe.x, pipe.y))
            else:
                WINDOW.blit(PIPE, (pipe.x, pipe.y))
        WINDOW.blit(score, (10, 10))
    pygame.display.update()


def start_game():
    pipe_top = pygame.Rect(75, 0, 52, 200)
    pipe_bottom = pygame.Rect(175, 258, 52, 200)
    clock = pygame.time.Clock()  # defines clock object that controls FPS
    bird = pygame.Rect(10, 256, 34, 24)
    run = True
    pipes.append(pipe_top)
    pipes.append(pipe_bottom)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_RETURN]:
                    global IS_PLAYING
                    IS_PLAYING = True
                    run = False
            draw_window(bird)


def draw_winner():
    print_text = FINAL_FONT.render(f"Score : {SCORE}", False, (255, 255, 255))
    WINDOW.blit(print_text, (WIDTH / 2 - print_text.get_width() / 2, HEIGHT / 2 - print_text.get_height() / 2))
    pygame.time.delay(2000)


def main():
    global SCORE
    global VELOCITY
    clock = pygame.time.Clock()
    run = True
    bird = pygame.Rect(10, 256, 34, 24)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP]:
            bird.y -= VELOCITY_BIRD
        elif key_pressed[pygame.K_DOWN]:
            bird.y += VELOCITY_BIRD
        else:
            bird.y += 1
        for pipe in pipes:
            pipe.x -= VELOCITY
            if pipe.x < -50 and pipe.y == 0:
                pipes[0] = pygame.Rect(288, 0, 52, 200)
                SCORE += 1
            elif pipe.x < -50 and pipe.y == 258:
                pipes[1] = pygame.Rect(288, 258, 52, 200)
                SCORE += 1
        if SCORE == 10:
            VELOCITY = 8
        if SCORE == 50:
            VELOCITY = 10
        if SCORE == 100:
            VELOCITY = 15
        is_over = False
        for pipe in pipes:
            if pipe.colliderect(bird):
                run = False
                is_over = True
                draw_winner()
                break
        if is_over:
            pass
            break
        else:
            draw_window(bird)
    pygame.quit()


if __name__ == "__main__":
    start_game()
    if IS_PLAYING:
        main()
