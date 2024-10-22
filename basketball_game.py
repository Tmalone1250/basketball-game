import pygame
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Basketball Shooting Game")

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Game variables
score = 0
timer = 60  # 60 seconds for the game
clock = pygame.time.Clock()
game_over = False

# Ball variables
ball_radius = 20
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT - 50
ball_speed_x = 0
ball_speed_y = 0
gravity = 0.1
shooting = False
ball_speed = 5  # Horizontal speed before shooting

# Basket (goal) variables
basket_width = 100
basket_height = 10
basket_x = SCREEN_WIDTH // 2 - basket_width // 2
basket_y = 150  # Basket at a reachable height

# Set up the timer event (updates every second)
TIMER_EVENT = pygame.USEREVENT - 1
pygame.time.set_timer(TIMER_EVENT, 1000)

def reset_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, shooting
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT - 50
    ball_speed_x = 0
    ball_speed_y = 0
    shooting = False

def check_goal():
    global score
    if basket_x < ball_x < basket_x + basket_width and basket_y - 5 < ball_y < basket_y + basket_height:
        score += 1
        reset_ball()

def display_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    label = font.render(text, True, BLACK)
    screen.blit(label, (x, y))

def game_over_screen():
    global score
    screen.fill(WHITE)
    display_text(f"Game Over! You scored: {score}", 72, 150, 200)
    display_text("Press R to Play Again or Q to Quit", 48, 150, 300)
    pygame.display.flip()

def game_loop():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, shooting, timer, game_over, score  # Ensure variables are global

    running = True
    while running:
        screen.fill(WHITE)
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE and not shooting:  # Shoot the ball
                    ball_speed_y = -10  # Stronger initial upward velocity
                    shooting = True
                if event.key == K_r and game_over:  # Restart game
                    reset_ball()
                    timer = 60
                    score = 0
                    game_over = False
                if event.key == K_q and game_over:  # Quit game
                    pygame.quit()
                    sys.exit()
                
        # Ball physics
        if shooting:
            ball_speed_y += gravity  # Gravity affects the ball's downward speed
            ball_y += ball_speed_y
        else:
            # Move ball left and right before shooting
            keys = pygame.key.get_pressed()
            if keys[K_LEFT] and ball_x - ball_radius > 0:
                ball_x -= ball_speed
            if keys[K_RIGHT] and ball_x + ball_radius < SCREEN_WIDTH:
                ball_x += ball_speed

        # Ball reset if it goes out of screen
        if ball_y > SCREEN_HEIGHT:
            reset_ball()

        # Check if the ball goes into the basket
        check_goal()

        # Draw basket (goal)
        pygame.draw.rect(screen, RED, (basket_x, basket_y, basket_width, basket_height))

        # Draw ball
        pygame.draw.circle(screen, BLACK, (int(ball_x), int(ball_y)), ball_radius)

        # Display score and timer
        display_text(f"Score: {score}", 36, 10, 10)
        display_text(f"Time: {timer}", 36, SCREEN_WIDTH - 120, 10)

        if game_over:
            game_over_screen()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()
