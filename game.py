import pygame
import random
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TypeBomb")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
GRAY = (150, 150, 150)

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 60)

# Game variables
letters = list("abcdefghijklmnopqrstuvwxyz")
small_words = ["cat", "run", "dog", "map", "sun", "pen"]
big_words = ["python", "rocket", "banana", "galaxy", "amazing"]

TOWN_Y = HEIGHT - 50

class Bomb:
    def __init__(self, text, x, speed):
        self.text = text
        self.x = x
        self.y = -50
        self.speed = speed
        self.active = True

    def update(self):
        self.y += self.speed
        if self.y >= TOWN_Y:
            self.active = False
            return 'hit'
        return None

    def draw(self):
        pygame.draw.ellipse(screen, GRAY, (self.x, self.y, 80, 40))
        text_surface = font.render(self.text, True, BLACK)
        screen.blit(text_surface, (self.x + 20, self.y + 10))

def draw_town():
    pygame.draw.rect(screen, GREEN, (0, TOWN_Y, WIDTH, 50))

def draw_text_center(text, y, color=BLACK):
    surface = big_font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH//2, y))
    screen.blit(surface, rect)

def difficulty_menu():
    while True:
        screen.fill(WHITE)
        draw_text_center("Select Difficulty", 100)
        draw_text_center("1. Easy", 200)
        draw_text_center("2. Medium", 280)
        draw_text_center("3. Hard", 360)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'easy'
                elif event.key == pygame.K_2:
                    return 'medium'
                elif event.key == pygame.K_3:
                    return 'hard'

def spawn_bomb(difficulty, tick):
    x = random.randint(50, WIDTH - 100)

    if difficulty == 'easy':
        text = random.choice(letters)
        speed = 2
    elif difficulty == 'medium':
        if random.random() < 0.6:
            text = random.choice(letters)
            speed = 3 #2 + tick // 500
        else:
            text = random.choice(small_words)
            speed = 2
    else:  # hard
        if random.random() < 0.5:
            text = random.choice(small_words)
        else:
            text = random.choice(big_words)
        speed =  3 #random.uniform(2, 5)

    return Bomb(text, x, speed)

def game_loop(difficulty):
    bombs = []
    current_input = ''
    score = 0
    lives = 5
    tick = 0
    spawn_interval = 60

    running = True
    while running:
        screen.fill(WHITE)
        tick += 1

        if tick % spawn_interval == 0:
            bombs.append(spawn_bomb(difficulty, tick))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                elif event.key == pygame.K_RETURN:
                    current_input = ''
                elif event.unicode.isprintable():
                    current_input += event.unicode.lower()

        for bomb in bombs:
            result = bomb.update()
            if result == 'hit':
                lives -= 1

        for bomb in bombs:
            if bomb.active and current_input == bomb.text:
                bomb.active = False
                current_input = ''
                score += len(bomb.text)

        bombs = [b for b in bombs if b.active]

        for bomb in bombs:
            bomb.draw()

        draw_town()
        draw_text_center(f"Score: {score} | Lives: {lives}", 30)
        input_surface = font.render(f"> {current_input}", True, RED)
        screen.blit(input_surface, (20, HEIGHT - 80))

        pygame.display.flip()
        clock.tick(60)

        if lives <= 0:
            return

def main():
    while True:
        difficulty = difficulty_menu()
        game_loop(difficulty)
        screen.fill(WHITE)
        draw_text_center("Game Over! Press any key to return to menu", HEIGHT//2)
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False

main()
