import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Catch Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)

# Basket as rectangle
basket_width, basket_height = 100, 30
basket = pygame.Rect(WIDTH // 2 - basket_width // 2, HEIGHT - 50, basket_width, basket_height)
basket_speed = 10

# Load fruit images
fruit_image_paths = ["assets/apple.png", "assets/banana.png", "assets/orange.png"]
fruit_images = [pygame.image.load(path) for path in fruit_image_paths]
fruit_size = 40
fruit_images = [pygame.transform.scale(img, (fruit_size, fruit_size)) for img in fruit_images]

# Fruit list (each item is a tuple of rect and image)
fruits = []
fruit_speed = 5
spawn_delay = 30
spawn_timer = 0

# Score
score = 0

# Game loop
running = True
while running:
    screen.fill(WHITE)

    # Quit check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Basket movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket.left > 0:
        basket.x -= basket_speed
    if keys[pygame.K_RIGHT] and basket.right < WIDTH:
        basket.x += basket_speed

    # Spawn fruits
    spawn_timer += 1
    if spawn_timer >= spawn_delay:
        fruit_x = random.randint(0, WIDTH - fruit_size)
        fruit_img = random.choice(fruit_images)
        fruit_rect = pygame.Rect(fruit_x, 0, fruit_size, fruit_size)
        fruits.append((fruit_rect, fruit_img))
        spawn_timer = 0

    # Move fruits
    for fruit in fruits[:]:
        fruit_rect, fruit_img = fruit
        fruit_rect.y += fruit_speed
        if fruit_rect.colliderect(basket):
            fruits.remove(fruit)
            score += 1
        elif fruit_rect.y > HEIGHT:
            fruits.remove(fruit)

    # Draw fruits
    for fruit_rect, fruit_img in fruits:
        screen.blit(fruit_img, fruit_rect.topleft)

    # Draw basket
    pygame.draw.rect(screen, BROWN, basket)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
