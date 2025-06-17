import pygame
import random
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("汽车避让小游戏")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

clock = pygame.time.Clock()
FPS = 60
game_speed = 5
score = 0
game_over = False
font = pygame.font.SysFont(None, 36)

class Car:
    def __init__(self):
        self.width = 50
        self.height = 80
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = 5
        
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + 5, self.width - 10, 20))
        
    def move(self, direction):
        if direction == "left" and self.x > 50:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width - 50:
            self.x += self.speed

class Obstacle:
    def __init__(self):
        self.width = random.randint(50, 100)
        self.height = random.randint(50, 100)
        self.x = random.randint(50, WIDTH - self.width - 50)
        self.y = -self.height
        self.speed = random.randint(3, 7)
        
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        
    def move(self):
        self.y += self.speed
        return self.y > HEIGHT

player_car = Car()
obstacles = []
obstacle_frequency = 60  
frame_count = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                player_car = Car()
                obstacles = []
                score = 0
                game_over = False
                frame_count = 0
                game_speed = 5
    
    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_car.move("left")
        if keys[pygame.K_RIGHT]:
            player_car.move("right")
        
        frame_count += 1
        if frame_count >= obstacle_frequency:
            obstacles.append(Obstacle())
            frame_count = 0
            obstacle_frequency = max(20, 60 - score // 10)
        
        for obstacle in obstacles[:]:
            if obstacle.move():
                obstacles.remove(obstacle)
                score += 1
        
        for obstacle in obstacles:
            if (player_car.x < obstacle.x + obstacle.width and
                player_car.x + player_car.width > obstacle.x and
                player_car.y < obstacle.y + obstacle.height and
                player_car.y + player_car.height > obstacle.y):
                game_over = True
        

        screen.fill(GRAY) 
        
        pygame.draw.rect(screen, YELLOW, (0, 0, 50, HEIGHT))  
        pygame.draw.rect(screen, YELLOW, (WIDTH-50, 0, 50, HEIGHT))  

        for i in range(0, HEIGHT, 40):
            pygame.draw.rect(screen, WHITE, (WIDTH//2 - 5, i, 10, 20))

        player_car.draw()
        for obstacle in obstacles:
            obstacle.draw()

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (60, 10))

        speed_text = font.render(f"Speed: {game_speed}", True, WHITE)
        screen.blit(speed_text, (60, 50))

        game_speed = 1 + score // 1
    else:
        screen.fill(BLACK)
        game_over_text = font.render("Game Over!", True, WHITE)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        restart_text = font.render("Press[R]to restart", True, WHITE)
        
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
    
    pygame.display.update()
    clock.tick(FPS)