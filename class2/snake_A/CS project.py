import pygame
import random

def play_game():
    # 初始化pygame
    pygame.init()
    
    # 游戏窗口设置
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("贪吃蛇游戏")
    
    # 颜色定义
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)  # 新增蓝色定义
    RED = (255, 0, 0)
    
    # 游戏参数
    BLOCK_SIZE = 20
    SNAKE_SPEED = 10
    
    # 初始化蛇和食物
    snake = [[WIDTH // 2, HEIGHT // 2], 
             [WIDTH // 2 - BLOCK_SIZE, HEIGHT // 2], 
             [WIDTH // 2 - 2 * BLOCK_SIZE, HEIGHT // 2]]
    direction = "RIGHT"
    food = [random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
            random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
    score = 0
    
    # 设置字体
    font = pygame.font.SysFont(None, 36)
    
    # 游戏主循环
    game_over = False
    clock = pygame.time.Clock()
    
    while not game_over:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
        
        # 移动蛇
        head = list(snake[0])
        if direction == "RIGHT":
            head[0] += BLOCK_SIZE
        elif direction == "LEFT":
            head[0] -= BLOCK_SIZE
        elif direction == "UP":
            head[1] -= BLOCK_SIZE
        elif direction == "DOWN":
            head[1] += BLOCK_SIZE
        
        # 检查是否撞墙
        if (head[0] >= WIDTH or head[0] < 0 or 
            head[1] >= HEIGHT or head[1] < 0):
            game_over = True
            continue
        
        # 检查是否撞到自己
        snake.insert(0, head)
        if head in snake[1:]:
            game_over = True
            continue
        
        # 检查是否吃到食物
        if head == food:
            score += 10
            food = [random.randrange(1, (WIDTH // BLOCK_SIZE)) * BLOCK_SIZE,
                    random.randrange(1, (HEIGHT // BLOCK_SIZE)) * BLOCK_SIZE]
        else:
            snake.pop()
        
        # 绘制游戏
        screen.fill(WHITE)  # 将背景改成白色
        
        # 绘制蛇
        for segment in snake:
            pygame.draw.rect(screen, BLUE, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])  # 将蛇的颜色改成蓝色
        
        # 绘制食物
        pygame.draw.rect(screen, RED, [food[0], food[1], BLOCK_SIZE, BLOCK_SIZE])
        
        # 显示分数
        score_text = font.render(f"Score: {score}", True, BLACK)  # 分数文字颜色改成黑色
        screen.blit(score_text, [10, 10])
        
        pygame.display.update()
        clock.tick(SNAKE_SPEED)
    
    # 游戏结束界面
    screen.fill(WHITE)  # 结束界面背景也改成白色
    game_over_text = font.render("Game over!", True, BLACK)  # 文字颜色改成黑色
    score_text = font.render(f"Final score: {score}", True, BLACK)  # 文字颜色改成黑色
    restart_text = font.render("Press R to restart, press ESC to exit.", True, BLACK)  # 文字颜色改成黑色
    
    screen.blit(game_over_text, [WIDTH // 2 - 100, HEIGHT // 2 - 50])
    screen.blit(score_text, [WIDTH // 2 - 100, HEIGHT // 2])
    screen.blit(restart_text, [WIDTH // 2 - 150, HEIGHT // 2 + 50])
    
    pygame.display.update()
    
    # 等待用户选择
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
    
    # 重新开始游戏
    pygame.quit()
    play_game()

# 启动游戏
if __name__ == "__main__":
    play_game()