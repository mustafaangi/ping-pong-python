import pygame
import random

# Constants
SCREEN_SIZE = (800, 600)
BALL_SPEED = 8  # Ball speed
PADDLE_SPEED = 15  # Player paddle speed
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 10
AI_SPEED = 7  # AI paddle

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Ping Pong')

# Game variables
ball_x, ball_y = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2
ball_dx, ball_dy = BALL_SPEED, BALL_SPEED
paddle1_y, paddle2_y = SCREEN_SIZE[1] // 2 - PADDLE_HEIGHT // 2, SCREEN_SIZE[1] // 2 - PADDLE_HEIGHT // 2
score1, score2 = 0, 0

# Control variables
left_paddle_active = True  # True for left paddle, False for right paddle

# Font for rendering scores
font = pygame.font.Font(None, 36)

# Frame rate control
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                left_paddle_active = not left_paddle_active  # Switch active paddle

    # Get keyboard state
    keys = pygame.key.get_pressed()

    # Handle paddle movement based on active paddle
    if left_paddle_active:
        # Control left paddle
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= PADDLE_SPEED
        if keys[pygame.K_s] and paddle1_y < SCREEN_SIZE[1] - PADDLE_HEIGHT:
            paddle1_y += PADDLE_SPEED
        
        # AI controls right paddle
        paddle_center = paddle2_y + PADDLE_HEIGHT / 2
        if paddle_center < ball_y - 10:
            paddle2_y += AI_SPEED
        elif paddle_center > ball_y + 10:
            paddle2_y -= AI_SPEED
    else:
        # Control right paddle
        if keys[pygame.K_w] and paddle2_y > 0:
            paddle2_y -= PADDLE_SPEED
        if keys[pygame.K_s] and paddle2_y < SCREEN_SIZE[1] - PADDLE_HEIGHT:
            paddle2_y += PADDLE_SPEED
            
        # AI controls left paddle
        paddle_center = paddle1_y + PADDLE_HEIGHT / 2
        if paddle_center < ball_y - 10:
            paddle1_y += AI_SPEED
        elif paddle_center > ball_y + 10:
            paddle1_y -= AI_SPEED

    # Keep paddles in bounds
    paddle1_y = max(0, min(SCREEN_SIZE[1] - PADDLE_HEIGHT, paddle1_y))
    paddle2_y = max(0, min(SCREEN_SIZE[1] - PADDLE_HEIGHT, paddle2_y))

    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Collision detection
    # Ball collision with top and bottom
    if ball_y <= 0 or ball_y >= SCREEN_SIZE[1] - BALL_SIZE:
        ball_dy = -ball_dy

    # Ball collision with paddles
    if (ball_x <= PADDLE_WIDTH and paddle1_y <= ball_y <= paddle1_y + PADDLE_HEIGHT) or \
       (ball_x >= SCREEN_SIZE[0] - PADDLE_WIDTH - BALL_SIZE and paddle2_y <= ball_y <= paddle2_y + PADDLE_HEIGHT):
        ball_dx = -ball_dx

    # Ball out of bounds
    if ball_x < 0:
        score2 += 1
        ball_x, ball_y = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2
        ball_dx = BALL_SPEED  # Reset ball direction
    elif ball_x > SCREEN_SIZE[0]:
        score1 += 1
        ball_x, ball_y = SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2
        ball_dx = -BALL_SPEED  # Reset ball direction

    # Debug prints for ball position
    print(f"Ball X: {ball_x}, Ball Y: {ball_y}")

    # Drawing code
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (0, paddle1_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (SCREEN_SIZE[0] - PADDLE_WIDTH, paddle2_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (ball_x, ball_y, BALL_SIZE, BALL_SIZE))
    # (Draw scores and other elements)
    score_text1 = font.render(f'Score: {score1}', True, (255, 255, 255))
    score_text2 = font.render(f'Score: {score2}', True, (255, 255, 255))
    screen.blit(score_text1, (50, 50))
    screen.blit(score_text2, (SCREEN_SIZE[0] - 150, 50))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()