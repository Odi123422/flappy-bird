import pygame
import random

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
BIRD_X = 50
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_GAP = 150
PIPE_WIDTH = 80
PIPE_SPEED = 3

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


class Bird:
    def __init__(self):
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.width = 34
        self.height = 24

    def flap(self):
        self.velocity = JUMP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def get_rect(self):
        return pygame.Rect(BIRD_X, int(self.y), self.width, self.height)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - GROUND_HEIGHT - 50)

    def update(self):
        self.x -= PIPE_SPEED

    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

    def get_top_rect(self):
        return pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)

    def get_bottom_rect(self):
        bottom_y = self.height + PIPE_GAP
        bottom_height = SCREEN_HEIGHT - bottom_y - GROUND_HEIGHT
        return pygame.Rect(self.x, bottom_y, PIPE_WIDTH, bottom_height)


def draw_window(screen, bird, pipes, score):
    screen.fill((135, 206, 250))  # sky blue

    # Draw pipes
    for pipe in pipes:
        pygame.draw.rect(screen, (0, 255, 0), pipe.get_top_rect())
        pygame.draw.rect(screen, (0, 255, 0), pipe.get_bottom_rect())

    # Draw ground
    pygame.draw.rect(screen, (222, 184, 135), (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

    # Draw bird
    pygame.draw.rect(screen, (255, 255, 0), bird.get_rect())

    # Draw score
    score_text = font.render(str(score), True, (0, 0, 0))
    screen.blit(score_text, (SCREEN_WIDTH // 2, 20))

    pygame.display.flip()


def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + 100)]
    score = 0

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()

        # Spawn new pipes
        if pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe(SCREEN_WIDTH))

        # Update pipes
        for pipe in list(pipes):
            pipe.update()
            if pipe.is_off_screen():
                pipes.remove(pipe)
                score += 1

        # Collision detection
        bird_rect = bird.get_rect()
        if bird.y + bird.height >= SCREEN_HEIGHT - GROUND_HEIGHT:
            running = False
        for pipe in pipes:
            if bird_rect.colliderect(pipe.get_top_rect()) or bird_rect.colliderect(pipe.get_bottom_rect()):
                running = False

        draw_window(screen, bird, pipes, score)

    pygame.quit()


if __name__ == "__main__":
    main()
