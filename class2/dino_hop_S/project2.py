import pygame
import random
import sys

pygame.init()


def draw_dino(player,x,y):
    #  color=BLUE if is_flying else GRAY
    #  return pygame.draw.rect(win, color, (x,y, dino_width, dino_height))
    screen.blit(player,(x,y))
    

 
def create_obstacle():
    return pygame.Rect(WIDTH, HEIGHT-70-50, 30, 50)


def create_powerup():
    return pygame.Rect(WIDTH, HEIGHT-70-30, 20, 20)

def game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, BLACK)
    win.blit(text, (WIDTH//2-140, HEIGHT//2-40))

# 初始化Pygame
pygame.init()
#窗口大小
resolution = pygame.display.Info()
WIDTH, HEIGHT = resolution.current_w-100,resolution.current_h-100
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Dino Game")
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption


# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# GRAY = (83, 83, 83)
BLUE = (0, 0, 255)


#绘制一个小恐龙


head_center=(400,200)
# pygame.draw.circle(screen,BLUE,head_center,
player=pygame.image.load("dinosaur.png")


# 游戏参数
FPS = 80
GRAVITY = 1
JUMP_FORCE = -20
MAX_JUMPS = 2  # 二段跳限制
OBSTACLE_SPEED = 10
FLYING_DURATION = 750 # 飞行时间3秒

# 恐龙属性
dino_width = 105
dino_height = 150
dino_x = 50
dino_y = HEIGHT - 70 - dino_height
dino_vel_y = 0
jumps_remaining = MAX_JUMPS
is_flying = False
flight_start_time = 0

# 障碍物和道具
obstacles = []
powerups = []

clock = pygame.time.Clock()
score = 0
game_active = True

running = True
while running:
    delta_time = clock.get_time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    # 飞行状态时按住空格保持上升
                    if is_flying:
                        dino_vel_y = JUMP_FORCE
                    # 正常跳跃和二段跳
                    elif jumps_remaining > 0:
                        dino_vel_y = JUMP_FORCE
                        jumps_remaining -= 1

                else:
                    game_active = True
                    obstacles.clear()
                    powerups.clear()
                    score = 0
                    is_flying = False

    if game_active:
        # 物理更新
        if not is_flying:
            dino_vel_y += GRAVITY
        dino_y += dino_vel_y

        # 地面检测
        if dino_y >= HEIGHT-70-dino_height:
            dino_y = HEIGHT-70-dino_height
            dino_vel_y = 0
            jumps_remaining = MAX_JUMPS

        # 生成障碍物和道具
        if random.random() < 0.02:
            obstacles.append(create_obstacle())
        if random.random() < 0.001:  # 000.1% 生成道具
            powerups.append(create_powerup())

        # 更新物体位置
        for obj in obstacles + powerups:
            obj.x -= OBSTACLE_SPEED

        # 碰撞检测
        dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
        
        # 障碍物碰撞
        for obj in obstacles:
            if obj.colliderect(dino_rect):
                game_active = False
        
        # 道具获取
        for pwr in powerups[:]:
            if pwr.colliderect(dino_rect):
                powerups.remove(pwr)
                is_flying = True
                flight_start_time = pygame.time.get_ticks()

        # 检查飞行时间
        if is_flying:
            if pygame.time.get_ticks() - flight_start_time > FLYING_DURATION:
                is_flying = False

        # 移除屏幕外物体
        obstacles = [obj for obj in obstacles if obj.right > 0]
        powerups = [pwr for pwr in powerups if pwr.right > 0]

        score += 1

    # 绘制画面
    win.fill(WHITE)
    pygame.draw.line(win, BLACK, (0, HEIGHT-70), (WIDTH, HEIGHT-70), 3)
    
    #绘制恐龙
    # draw_dino(dino_x,dino_y)
    screen.blit(player,(dino_x,dino_y))
    # 绘制障碍物和道具
    for obj in obstacles:
        pygame.draw.rect(win, BLACK, obj)
    for pwr in powerups:
        pygame.draw.circle(win, BLUE, pwr.center, 10)
    
    # 显示信息
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score//10}", True, BLACK)
    win.blit(text, (10, 10))
    
    if is_flying:
        remaining = FLYING_DURATION - (pygame.time.get_ticks() - flight_start_time)
        text = font.render(f"Fly: {max(0, remaining//1000)}s", True, BLUE)
        win.blit(text, (WIDTH-120, 10))
    
    if not game_active:
        game_over()
        
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
print("quited.....................................................")