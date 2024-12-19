import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Exciting Android Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)
LIGHT_PINK = (255, 182, 193)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Clock for frame rate
clock = pygame.time.Clock()

# Player settings
player_size = 50
player_x = SCREEN_WIDTH // 2 - player_size // 2
player_y = SCREEN_HEIGHT - player_size - 10
player_speed = 7
player_lives = 3
shield_active = False
speed_boost_active = False
invisibility_active = False
invisibility_timer = 0
speed_boost_timer = 0
shield_timer = 0

# Enemy settings
enemy_size = 50
enemy_speed = 5
enemies = []

# Game variables
score = 0
high_score = 0
level = 1
level_up_score = 10

# Power-up settings
power_up_size = 30
power_up_speed = 3
power_ups = []

# Sound effects
pygame.mixer.init()
score_sound = pygame.mixer.Sound("score.wav")
level_up_sound = pygame.mixer.Sound("level_up.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
background_music = pygame.mixer.music.load("background_music.mp3")

# Play background music
pygame.mixer.music.play(-1, 0.0)

# Sound state (default is on)
sound_on = True

# Function to draw text
def draw_text(text, font, color, x, y):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

# Function to toggle sound
def toggle_sound():
    global sound_on
    if sound_on:
        pygame.mixer.music.stop()  # Stop music if sound is off
        sound_on = False
    else:
        pygame.mixer.music.play(-1, 0.0)  # Restart music if sound is on
        sound_on = True

# Main menu
def main_menu():
    global running
    menu_running = True
    while menu_running:
        screen.fill(LIGHT_BLUE)
        font = pygame.font.SysFont(None, 75)
        draw_text("Exciting Android Game", font, BLACK, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 3 - 50)
        
        font = pygame.font.SysFont(None, 50)
        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50)
        options_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        exit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)

        # Just draw the text directly without the blue box
        draw_text("Start Game", font, WHITE, start_button.x + 50, start_button.y + 10)
        draw_text("Options", font, WHITE, options_button.x + 50, options_button.y + 10)
        draw_text("Exit", font, WHITE, exit_button.x + 50, exit_button.y + 10)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if start_button.collidepoint(mouse_x, mouse_y):
                    menu_running = False
                    start_game()
                elif options_button.collidepoint(mouse_x, mouse_y):
                    menu_running = False
                    options_menu()
                elif exit_button.collidepoint(mouse_x, mouse_y):
                    menu_running = False
                    running = False

# Options menu
def options_menu():
    global sound_on  # Use the global sound_on variable
    options_running = True
    while options_running:
        screen.fill(LIGHT_BLUE)
        font = pygame.font.SysFont(None, 75)
        draw_text("Options", font, BLACK, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 - 50)
        
        font = pygame.font.SysFont(None, 50)
        
        back_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        sound_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)

        sound_text = "Sound: On" if sound_on else "Sound: Off"
        draw_text(sound_text, font, WHITE, sound_button.x + 50, sound_button.y + 10)
        draw_text("Back", font, WHITE, back_button.x + 50, back_button.y + 10)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                options_running = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if back_button.collidepoint(mouse_x, mouse_y):
                    options_running = False
                    main_menu()
                elif sound_button.collidepoint(mouse_x, mouse_y):
                    toggle_sound()  # Toggle sound on button click

# Create enemy and power-up
def create_enemy():
    x_pos = random.randint(0, SCREEN_WIDTH - enemy_size)
    y_pos = -enemy_size
    # Enemies are either "normal" or "boss", with more "boss" enemies appearing as the level increases
    enemy_type = random.choice(["normal", "boss"] if level > 5 else ["normal"])
    enemies.append([x_pos, y_pos, enemy_type])

def create_power_up():
    x_pos = random.randint(0, SCREEN_WIDTH - power_up_size)
    y_pos = -power_up_size
    power_ups.append([x_pos, y_pos])

def increase_level():
    global level, enemy_speed, level_up_score
    level += 1
    enemy_speed += 1  # Increase speed of normal enemies as the level increases
    level_up_score += 10
    level_up_sound.play()

def game_over():
    global player_lives, score, high_score
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 75)
    game_over_text = font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))

    if score > high_score:
        high_score = score

    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()
    pygame.mixer.music.stop()
    game_over_sound.play()

    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                score = 0
                player_lives = 3
                return True
    return False

def start_game():
    global shield_timer, speed_boost_timer, invisibility_timer, running, score, level, player_lives, shield_active, speed_boost_active, invisibility_active
    if sound_on:
        pygame.mixer.music.play(-1, 0.0)  # Play background music
    else:
        pygame.mixer.music.stop()  # Stop background music if sound is off
    player_x = SCREEN_WIDTH // 2 - player_size // 2
    player_y = SCREEN_HEIGHT - player_size - 10
    score = 0
    level = 1
    player_lives = 3
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_size:
            player_x += player_speed

        if random.randint(0, 50) == 0:
            create_enemy()
        if random.randint(0, 300) == 0:
            create_power_up()

        for enemy in enemies[:]:
            enemy[1] += enemy_speed  # Normal enemies move
            # Add faster speed for boss enemies as the level increases
            if enemy[2] == "boss":
                enemy[1] += 2  # Boss enemies move faster, adjust as needed

            if (player_x < enemy[0] + enemy_size and
                player_x + player_size > enemy[0] and
                player_y < enemy[1] + enemy_size and
                player_y + player_size > enemy[1]):
                if not shield_active:
                    player_lives -= 1
                    if player_lives <= 0:
                        running = game_over()
                enemies.remove(enemy)
            if enemy[1] >= SCREEN_HEIGHT:
                enemies.remove(enemy)
                score += 1
                score_sound.play()
                if score >= level_up_score:
                    increase_level()

        for power_up in power_ups[:]:
            if player_x < power_up[0] < player_x + player_size and player_y < power_up[1] < player_y + player_size:
                power_ups.remove(power_up)
                power_type = random.choice(["shield", "speed_boost", "invisibility"])
                if power_type == "shield":
                    shield_active = True
                    shield_timer = pygame.time.get_ticks() + 5000
                    if shield_active:
                        pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, player_size, player_size))  # সবুজ রঙের শিল্ড
                    else:
                        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))
                elif power_type == "speed_boost":
                    speed_boost_active = True
                    speed_boost_timer = pygame.time.get_ticks() + 5000
                elif power_type == "invisibility":
                    invisibility_active = True
                    invisibility_timer = pygame.time.get_ticks() + 5000

        if pygame.time.get_ticks() > shield_timer and shield_active:
            shield_active = False
        if pygame.time.get_ticks() > speed_boost_timer and speed_boost_active:
            speed_boost_active = False
        if pygame.time.get_ticks() > invisibility_timer and invisibility_active:
            invisibility_active = False

        if speed_boost_active:
            player_speed = 10
            player_color = (255, 215, 0)  # Golden Yellow color when speed boost is active
        else:
            player_speed = 7
            player_color = BLUE  # Normal blue color when no speed boost

        # Draw everything
        screen.fill(LIGHT_BLUE)
        pygame.draw.circle(screen, YELLOW, (SCREEN_WIDTH - 60, 60), 50)
        if invisibility_active:
            pygame.draw.rect(screen, LIGHT_PINK, (player_x, player_y, player_size, player_size))
        else:
            pygame.draw.rect(screen, BLUE, (player_x, player_y, player_size, player_size))

        for enemy in enemies:
            if enemy[2] == "normal":
                color = RED
            elif enemy[2] == "boss":
                color = ORANGE
            pygame.draw.rect(screen, color, (enemy[0], enemy[1], enemy_size, enemy_size))

        for power_up in power_ups:
            pygame.draw.circle(screen, GREEN, (power_up[0] + power_up_size // 2, power_up[1] + power_up_size // 2), power_up_size // 2)

        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        level_text = font.render(f"Level: {level}", True, BLACK)
        screen.blit(level_text, (10, 50))

        lives_text = font.render(f"Lives: {player_lives}", True, BLACK)
        screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(30)

# Run the game
running = True
main_menu()
