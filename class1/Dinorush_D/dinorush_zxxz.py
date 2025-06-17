import pygame
import random
import sys

pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Chrome Dino Game')
clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (83, 83, 83)
BACKGROUND_COLOR = (255, 255, 255)

try:
    # 障碍物图片
    large_obstacle_img = pygame.image.load("bigger.png").convert_alpha()
    small_obstacle_img = pygame.image.load("small.png").convert_alpha()

    # 小恐龙图片
    dino_stand_img = pygame.image.load("player.png").convert_alpha()
    dino_jump_img = pygame.image.load("player.png").convert_alpha()
    dino_duck_img = pygame.image.load("duck.jpg").convert_alpha()

    # 背景
    cloud_img = pygame.image.load("cloud.jpg").convert_alpha()
    bird_img = pygame.image.load("bird.jpg").convert_alpha()

    # 调整图片大小
    large_obstacle_img = pygame.transform.scale(large_obstacle_img, (70, 80))
    small_obstacle_img = pygame.transform.scale(small_obstacle_img, (50, 60))
    dino_stand_img = pygame.transform.scale(dino_stand_img, (60, 80))
    dino_jump_img = pygame.transform.scale(dino_jump_img, (60, 80))
    dino_duck_img = pygame.transform.scale(dino_duck_img, (80, 40))  
    cloud_img = pygame.transform.scale(cloud_img, (100, 50))
    bird_img = pygame.transform.scale(bird_img, (60, 40))

except pygame.error as e:
    print(f"加载图片出错: {e}")
    print("请检查图片路径是否正确")
    sys.exit()


class Dino:
    def __init__(self):
        self.x = 50
        self.y = 400
        self.width = 60
        self.height = 80
        self.jump_velocity = 0
        self.is_jumping = False
        self.is_ducking = False
        self.is_dead = False
        self.animation_frame = 0
        self.animation_speed = 5

    def jump(self):
        if not self.is_jumping and not self.is_dead:
            self.is_jumping = True
            self.jump_velocity = -15

    def duck(self):
        if not self.is_jumping and not self.is_dead:
            self.is_ducking = True
            self.height = 40
            self.width = 80
            self.y = 420  # 让小恐龙蹲下时y坐标增加，即更低一点，不然会在中间

    def unduck(self):
        self.is_ducking = False
        self.height = 80
        self.width = 60
        self.y = 400  # 恢复站立时的y坐标

    def update(self):
        if self.is_jumping:
            self.y += self.jump_velocity
            self.jump_velocity += 0.8
            if self.y >= 400:
                self.y = 400
                self.is_jumping = False

        self.animation_frame += 1

    def draw(self):
        if self.is_dead:
            # 死亡状态
            screen.blit(dino_stand_img, (self.x, self.y))
        elif self.is_jumping:
            # 跳跃状态
            screen.blit(dino_jump_img, (self.x, self.y))
        elif self.is_ducking:
            # 蹲下状态
            screen.blit(dino_duck_img, (self.x, self.y))
        else:
            # 站立/跑步状态
            if self.animation_frame // self.animation_speed % 2 == 0:
                screen.blit(dino_stand_img, (self.x, self.y))
            else:
                screen.blit(dino_stand_img, (self.x, self.y))


class Obstacle:
    def __init__(self, obstacle_type=None):
        self.type = obstacle_type or random.choice(['large','small', 'bird'])
        self.x = SCREEN_WIDTH

        if self.type == 'large':
            self.image = large_obstacle_img
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.y = 400 + 80 - self.height
        elif self.type =='small':
            self.image = small_obstacle_img
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.y = 400 + 80 - self.height
        else:  # bird
            self.image = bird_img
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.y = random.choice([300, 350, 400])  # 这样小鸟就可以在不同高度飞行（也算障碍物了）

        self.speed = 10

    def update(self):
        self.x -= self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def collide(self, dino):
        dino_rect = pygame.Rect(dino.x, dino.y, dino.width, dino.height)
        obstacle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return dino_rect.colliderect(obstacle_rect)


class Ground:
    def __init__(self):
        self.x1 = 0
        self.x2 = SCREEN_WIDTH
        self.y = 480
        self.width = SCREEN_WIDTH
        self.height = 20
        self.speed = 10

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x1, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x2, self.y, self.width, self.height))


class Cloud:
    def __init__(self):
        self.image = cloud_img
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = SCREEN_WIDTH
        self.y = random.randint(50, 200)
        self.speed = 3

    def update(self):
        self.x -= self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


def game():
    dino = Dino()
    ground = Ground()
    obstacles = []
    clouds = []
    obstacle_timer = 0
    cloud_timer = 0
    score = 0
    game_speed = 10
    font = pygame.font.SysFont(None, 36)

    for _ in range(3):
        clouds.append(Cloud())

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    dino.jump()
                if event.key == pygame.K_DOWN:
                    dino.duck()
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                dino.unduck()

        screen.fill(BACKGROUND_COLOR)

        cloud_timer += 1
        if cloud_timer > random.randint(100, 200):
            cloud_timer = 0
            clouds.append(Cloud())

        for cloud in clouds[:]:
            cloud.update()
            if cloud.x + cloud.width < 0:
                clouds.remove(cloud)
            cloud.draw()

        # 障碍物
        obstacle_timer += 1
        if obstacle_timer > random.randint(50, 150):
            obstacle_timer = 0
            if score < 1000:
                obstacle_type = random.choice(['large','small'])
            else:
                obstacle_type = random.choice(['large','small', 'bird'])
            obstacles.append(Obstacle(obstacle_type))

        dino.update()
        ground.update()

        for obstacle in obstacles[:]:
            obstacle.update()
            if obstacle.collide(dino):
                dino.is_dead = True
                return game_over(score)
            if obstacle.x + obstacle.width < 0:
                obstacles.remove(obstacle)

        ground.draw()
        dino.draw()
        for obstacle in obstacles:
            obstacle.draw()

        # 更新分数和小恐龙奔跑速度
        score += 1
        if score % 100 == 0:
            game_speed += 0.5
            for obstacle in obstacles:
                obstacle.speed = game_speed
            ground.speed = game_speed
            for cloud in clouds:
                cloud.speed = max(1, game_speed * 0.3)

        score_text = font.render(f"Score: {score}", True, GRAY)
        screen.blit(score_text, (SCREEN_WIDTH - 150, 20))

        pygame.display.update()
        clock.tick(FPS)


def game_over(score):
    font_large = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

        screen.fill(BACKGROUND_COLOR)

        game_over_text = font_large.render("GAME OVER", True, GRAY)
        score_text = font_small.render(f"Your Score: {score}", True, GRAY)
        restart_text = font_small.render("Press SPACE to restart", True, GRAY)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 70))

        pygame.display.update()
        clock.tick(FPS)


def main():
    while True:
        if not game():
            break


if __name__ == "__main__":
    main()