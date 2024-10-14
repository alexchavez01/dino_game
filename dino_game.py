import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 300
GROUND_HEIGHT = SCREEN_HEIGHT - 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30
GRAVITY = 1
JUMP_POWER = 12
OBSTACLE_SPAWN_TIME = random.randint(1000, 1600)  # Time (in ms) between obstacle spawns

# Dino class
class Dino:
    def __init__(self):
        self.image = pygame.Surface((10, 20))  # Simple square for the dino
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GROUND_HEIGHT - self.rect.height
        self.is_jumping = False
        self.jump_vel = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_vel = -JUMP_POWER

    def update(self):
        if self.is_jumping:
            self.rect.y += self.jump_vel
            self.jump_vel += GRAVITY

            # Stop jumping and land on the ground
            if self.rect.y >= GROUND_HEIGHT - self.rect.height:
                self.rect.y = GROUND_HEIGHT - self.rect.height
                self.is_jumping = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Obstacle class
class Obstacle:
    def __init__(self):
        self.width = 20
        self.height = random.randint(20, 50)  # Random height for variation
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = GROUND_HEIGHT - self.height
        self.speed = 10

    def update(self):
        self.rect.x -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Main game function
def game():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dino Game with Multiple Obstacles")
    clock = pygame.time.Clock()

    # Game objects
    dino = Dino()
    obstacles = []
    pygame.time.set_timer(pygame.USEREVENT, OBSTACLE_SPAWN_TIME)  # Timer to spawn obstacles

    # Game state
    game_over = False
    score = 0
    font = pygame.font.Font(None, 36)

    # Main game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()
            if event.type == pygame.USEREVENT:
                # Spawn a new obstacle
                obstacles.append(Obstacle())

        # Update game state
        dino.update()

        for obstacle in obstacles:
            obstacle.update()

        # Remove obstacles that are off-screen
        obstacles = [obstacle for obstacle in obstacles if obstacle.rect.x + obstacle.width > 0]

        # Collision detection
        for obstacle in obstacles:
            if dino.rect.colliderect(obstacle.rect):
                game_over = True

        # Draw everything
        screen.fill(WHITE)
        dino.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Draw the score
        score += 1
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the screen
        pygame.display.flip()
        clock.tick(FPS)

    # Game over screen
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game()  # Restart the game

        screen.fill(WHITE)
        game_over_text = font.render("Game Over! Press Space to Restart", True, BLACK)
        screen.blit(game_over_text, (150, 150))
        pygame.display.flip()

if __name__ == "__main__":
    game()
