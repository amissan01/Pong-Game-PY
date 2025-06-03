import pygame, sys, random

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Bounce off the top and bottom walls
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # Restart ball if it hits left or right walls
    if ball.left <= 0:
        player_score += 1
        ball_restart()
    if ball.right >= screen_width:
        opponent_score += 1
        ball_restart()

    # Bounce off the paddles
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
        ball_speed_x *= 1.1  # Increase speed gradually
        ball_speed_y *= 1.1

def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_ai():
    if opponent.centery < ball.centery:
        opponent.centery += opponent_speed
    elif opponent.centery > ball.centery:
        opponent.centery -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y

    for i in range(3, 0, -1):  # Countdown from 3 to 1
        screen.fill(bg_color)  # Clear screen

        # Draw paddles and middle line
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

        # Display the countdown number
        countdown_text = game_font.render(str(i), True, light_grey)
        text_rect = countdown_text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(countdown_text, text_rect)

        pygame.display.flip()  # Update screen
        pygame.time.delay(1000)  # Wait 1 second

    # Reset ball position
    ball.center = (screen_width / 2, screen_height / 2)

    # Randomize new ball direction
    ball_speed_x = 7 * random.choice((1, -1))
    ball_speed_y = 7 * random.choice((1, -1))

def update_score():
    player_text = game_font.render(f"{player_score}", True, light_grey)
    opponent_text = game_font.render(f"{opponent_score}", True, light_grey)
    screen.blit(player_text, (screen_width / 2 + 20, 20))
    screen.blit(opponent_text, (screen_width / 2 - 60, 20))

def check_game_over():
    if player_score == winning_score or opponent_score == winning_score:
        game_over_text = game_font.render("Game Over", True, light_grey)
        screen.blit(game_over_text, (screen_width / 2 - 150, screen_height / 2 - 50))
        pygame.display.flip()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Define Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Speeds
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# Scores
player_score = 0
opponent_score = 0
winning_score = 10

game_font = pygame.font.Font(None, 74)  # Font for displaying scores

# Main game loop
while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            elif event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            elif event.key == pygame.K_UP:
                player_speed += 7

    ball_animation()
    player_animation()
    opponent_ai()

    # Draw visuals
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    update_score()
    check_game_over()

    # Update the window
    pygame.display.flip()
    clock.tick(60)
