import pygame
import random
import sys
import math

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Type Bomb")
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
small_words = [
    "and", "are", "arm", "ask", "ate", "bad", "bag", "bar", "bat", "bed",
    "bee", "beg", "bet", "big", "bit", "box", "boy", "bus", "but", "can",
    "cap", "car", "cat", "cop", "cow", "cry", "cup", "cut", "dad", "day",
    "did", "dog", "dry", "ear", "eat", "egg", "end", "eye", "far", "fat",
    "few", "fit", "fix", "fly", "fog", "for", "fun", "gas", "get", "got",
    "gum", "guy", "had", "has", "hat", "her", "hey", "him", "his", "hot",
    "how", "ice", "ink", "its", "jam", "jar", "jet", "job", "joy", "key",
    "kid", "kit", "lab", "lad", "let", "lid", "lip", "log", "man", "map",
    "mat", "may", "men", "mix", "mom", "net", "new", "not", "now", "off",
    "oil", "old", "one", "our", "out", "pan", "pen", "pet", "pie", "pig"
]

big_words = ["python", "rocket", "banana", "galaxy", "amazing"]
town_buildings = []  # To store pre-generated layout
grounds = []  # To store ground images
current_input = ''
explosions = []
score = 0



building_images = [
    pygame.image.load("assets/building_1.png").convert_alpha(),
    pygame.image.load("assets/building_2.png").convert_alpha(),
    pygame.image.load("assets/building_3.png").convert_alpha()
]

missile_images = {
    'letter': pygame.transform.scale(pygame.image.load("assets/missile_letter.png").convert_alpha(), (40, 85)),
    'small': pygame.transform.scale(pygame.image.load("assets/missile_small_word.png").convert_alpha(), (50, 160)),
    'big': pygame.transform.scale(pygame.image.load("assets/missile_big_word.png").convert_alpha(), (50, 200))
}


ground_image=pygame.image.load("assets/ground.png").convert_alpha()


TOWN_Y = HEIGHT-30
class Bomb:
    def __init__(self, text, x, speed, image_type, dx=0,dy=1,angle=0):
        self.text = text
        self.x = x
        self.y = -100
        self.speed = speed
        self.angle = angle  # Angle in degrees
        self.dy = dy
        self.dx = dx  # horizontal speed for diagonal movement
        self.active = True
        self.missile_type = image_type
        self.image = missile_images[image_type]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        

    def update(self):
        self.y += self.speed
        self.x += self.dx  # Apply horizontal movement
        if self.y + self.height >= TOWN_Y-90:
            self.active = False
            return 'hit'
        return None

    def draw(self):
       
        # Rotate image to match movement angle
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

        # Draw rotated image
        screen.blit(rotated_image, rotated_rect.topleft)

        # Draw text centered over the rotated bomb
        if self.dx != 0:
            if(self.dx>0):
                text_offset_x = 13
                text_offset_y = 13
                angle_offset = 270
            else:
                text_offset_x = -10
                text_offset_y = 15
                angle_offset = 90
            text_angle= (self.angle + angle_offset) % 360  # Adjust text angle to match bomb rotation
            text_surf = font.render(self.text, True, BLACK)
            rotated_surf = pygame.transform.rotate(text_surf, text_angle)
            rotated_rect = rotated_surf.get_rect(center=(self.x + self.width // 2+ text_offset_x, self.y + self.height // 2+text_offset_y))
            # pygame.draw.rect(screen, WHITE, rotated_rect.inflate(6, 6), 2)
            screen.blit(rotated_surf, rotated_rect)
        else:
            text_surf = font.render(self.text, True, BLACK)
            text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2+9))
            screen.blit(text_surf, text_rect)

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 1
        self.max_radius = 30
        self.active = True
        self.growth = 3
        self.alpha = 255

    def update(self):
        if self.active:
            self.radius += self.growth
            self.alpha -= 15
            if self.radius >= self.max_radius or self.alpha <= 0:
                self.active = False

    def draw(self, screen):
        if self.active:
            surf = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 100, 0, self.alpha), (self.max_radius, self.max_radius), self.radius)
            pygame.draw.circle(surf, (255, 255, 0, self.alpha), (self.max_radius, self.max_radius), self.radius // 2)
            screen.blit(surf, (self.x - self.max_radius, self.y - self.max_radius))



def generate_town():
    global town_buildings
    x = 0
    max_building_height = 150
    town_buildings = []

    while x < WIDTH:
        building = random.choice(building_images)
        scale_ratio = max_building_height / building.get_height()
        new_width = int(building.get_width() * scale_ratio)
        new_height = int(building.get_height() * scale_ratio)
        resized = pygame.transform.scale(building, (new_width, new_height))
        town_buildings.append((resized, x, TOWN_Y - new_height))
        x += new_width

def generate_ground():
    global grounds
    x = 0
    while x < WIDTH:
        ground = pygame.transform.scale(ground_image, (ground_image.get_width(), ground_image.get_height()))
        grounds.append((ground, x, TOWN_Y - ground.get_height()+50))
        x += ground.get_width()
    # Generate ground images

def draw_town():
    for building, x, y in town_buildings:
        screen.blit(building, (x, y))
    for ground, x, y in grounds:
        screen.blit(ground, (x, y))


def draw_background():
    screen.fill((135, 206, 235))  # Sky blue

    # Sun
    pygame.draw.circle(screen, (255, 255, 100), (WIDTH - 100, 100), 50)

    # Optional: clouds or other simple shapes later


def draw_text_center(text, y, color=BLACK):
    surface = big_font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH//2, y))
    screen.blit(surface, rect)

def difficulty_menu():
    options = ["Easy", "Medium", "Hard"]
    selected = 0

    while True:
        screen.fill(WHITE)
        draw_text_center("Select Difficulty", 100)

        option_rects = []
        for i, option in enumerate(options):
            color = BLACK
            if i == selected:
                text = f"> {option}"
            else:
                text = f"  {option}"
            text_surface = big_font.render(text, True, color)
            rect = text_surface.get_rect(topleft=(WIDTH // 2 - 100, 200 + i * 80))
            option_rects.append(rect)
            screen.blit(text_surface, rect.topleft)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected].lower()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(event.pos):
                            return options[i].lower()
                        
def spawn_bomb(difficulty, tick):
    x = random.randint(50, WIDTH - 200)
    dx = 0
    dy = 1
    angle= 0

    if difficulty == 'easy':
        text = random.choice(letters)
        speed = 3
        img_type = 'letter'
        

    elif difficulty == 'medium':
        if random.random() < 0.6:
            text = random.choice(letters)
            speed = 3
            img_type = 'letter'
            
        else:
            text = random.choice(small_words)
            speed = 2
            img_type = 'small'
            # Force diagonal direction with a strong downward component
            angle_choices = [
                random.uniform(math.radians(25), math.radians(60)),   # right-down
                random.uniform(math.radians(140), math.radians(170))  # left-down
            ]
            angle = random.choice(angle_choices)
            dx = math.cos(angle) * 2
            dy = math.sin(angle) * 2
    
            angle=math.degrees(angle)
            if(dx<0):
                angle+=180
                angle=angle%360
            if(dx==0):
                angle

    else:  # hard
        if random.random() < 0.5:
            text = random.choice(small_words)
            img_type = 'small'
        else:
            text = random.choice(big_words)
            img_type = 'big'
        speed = random.uniform(2, 5)
        dx = 0

    # Ensure bomb won't go off-screen by adjusting spawn x range
    if(img_type=='small'):
        bomb_width = font.size(text)[0]
        time_to_reach_ground = (TOWN_Y - 50) / speed  # approximate frames before hitting town
        max_dx_distance = abs(dx * time_to_reach_ground)

    # Ensure bomb stays on screen horizontally
        min_x = max(0, int(max_dx_distance))
        max_x = min(WIDTH - bomb_width, int(WIDTH - max_dx_distance))

    # Safe spawn range
        if min_x >= max_x:
            x = WIDTH // 2  # fallback to center if no safe zone
            dx = 1
        else:
            x = random.randint(min_x, max_x)

    return Bomb(text, x, speed, img_type, dx=dx, dy=dy, angle=angle)

def pause_menu():
    while True:
        screen.fill(WHITE)
        draw_text_center("Paused", HEIGHT // 2 - 50)
        draw_text_center("Press 'R' to Resume or 'Q' to Quit to Main Menu", HEIGHT // 2 + 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return  # Resume the game
                elif event.key == pygame.K_q:
                    return 'quit'  # Quit to main menu
                
def draw_rounded_rect(surface, color, rect, radius):
    # Draw the rounded corners
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    pygame.draw.circle(surface, color, (rect.left + radius, rect.top + radius), radius)
    pygame.draw.circle(surface, color, (rect.right - radius, rect.top + radius), radius)
    pygame.draw.circle(surface, color, (rect.left + radius, rect.bottom - radius), radius)
    pygame.draw.circle(surface, color, (rect.right - radius, rect.bottom - radius), radius)

def handle_input(event):
    global current_input, backspace_pressed
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            current_input = current_input[:-1]  # Remove last character
        elif event.key == pygame.K_RETURN:
            # Handle enter key action, like submitting the input
            current_input = ''  # Clear input after pressing enter
        elif event.unicode.isprintable():  # Only allow printable characters
            current_input += event.unicode.lower()
        elif event.key == pygame.K_ESCAPE:
            if pause_menu() == 'quit':
                return 'quit'

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_BACKSPACE:
            backspace_pressed = False  # Stop backspace holding action

def game_loop(difficulty):
    bombs = []
    global current_input
    current_input=''
    global score
    score = 0 
    lives = 5
    tick = 0
    if difficulty == 'easy':
        spawn_interval = 60
    elif difficulty == 'medium':
        spawn_interval = 70
    else:  # hard
        spawn_interval = 70

    running = True
    while running:
        draw_background()
        tick += 1

        if tick % spawn_interval == 0:
            bombs.append(spawn_bomb(difficulty, tick))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if handle_input(event) == 'quit':
                    return
            elif event.type == pygame.ACTIVEEVENT:
                if event.state == 2 and event.gain == 0:  # Window focus lost
                    if pause_menu() == 'quit':  # Check if user wants to quit to main menu
                        return

        for bomb in bombs:
            result = bomb.update()
            if result == 'hit':
                explosions.append(Explosion(bomb.x + bomb.width//2, bomb.y + bomb.height//2))
                lives -= 1

        for bomb in bombs:
            if bomb.active and current_input == bomb.text:
                explosions.append(Explosion(bomb.x + bomb.width//2, bomb.y + bomb.height//2))
                bomb.active = False
                current_input = ''
                score += len(bomb.text)
        
        for explosion in explosions[:]:
            explosion.update()
            explosion.draw(screen)
            if not explosion.active:
                explosions.remove(explosion)

        bombs = [b for b in bombs if b.active]

        for bomb in bombs:
            bomb.draw()

        

        draw_town()
        hud_surface = font.render(f"Score: {score}  |  Lives: {lives}", True, BLACK)
        screen.blit(hud_surface, (20, 20))
        outer_rect= pygame.Rect((WIDTH/4), TOWN_Y-5 , WIDTH/2, 30)
        
        draw_rounded_rect(screen, (225,217,209), outer_rect, 10)
        input_surface = font.render(f"{current_input}", True, RED)
        screen.blit(input_surface, ((WIDTH/4)+10, TOWN_Y))

        pygame.display.flip()
        clock.tick(60)

        if lives <= 0:
            return

def main():
    while True:
        difficulty = difficulty_menu()
        generate_town()
        generate_ground()
        game_loop(difficulty)
        screen.fill(WHITE)
        game_end = ["Game Over!",f"Score: {score}","Press any key to return to menu"]
        for i, line in enumerate(game_end):
            text_surface = big_font.render(line, True, BLACK)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
            screen.blit(text_surface, text_rect.topleft)
        # draw_text_center(game_end, HEIGHT//2)
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