import pygame
import sys
import os

# 初始化Pygame
pygame.init()

# 游戏参数
BOARD_SIZE = 15       # 棋盘15x15格
CELL_SIZE = 40        # 每格像素大小
WINDOW_SIZE = (BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
FPS = 60              # 帧率

# 创建窗口
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("五子棋游戏")
clock = pygame.time.Clock()

# 加载图片（需与代码同目录）
def load_image(name, size=None):
    try:
        image = pygame.image.load(name).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error:
        print(f"图片 {name} 加载失败，使用默认样式")
        return None

# 加载棋子和棋盘图片
black_piece = load_image("black.png", (CELL_SIZE-10, CELL_SIZE-10))
white_piece = load_image("white.png", (CELL_SIZE-10, CELL_SIZE-10))
board_image = load_image("board.png", WINDOW_SIZE)  # 可选棋盘背景

# 游戏状态
board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]  # 0:空 1:黑 2:白
current_player = 1       # 1黑棋先手
game_over = False
winner = 0

# 绘制棋盘（若没有图片则绘制网格）
def draw_board():
    if board_image:
        screen.blit(board_image, (0, 0))  # 显示棋盘图片
    else:
        screen.fill((200, 160, 80))  # 棕色背景
        # 绘制网格线
        for i in range(BOARD_SIZE):
            pygame.draw.line(screen, (0, 0, 0), (0, i * CELL_SIZE), 
                            (BOARD_SIZE * CELL_SIZE, i * CELL_SIZE), 2)
            pygame.draw.line(screen, (0, 0, 0), (i * CELL_SIZE, 0), 
                            (i * CELL_SIZE, BOARD_SIZE * CELL_SIZE), 2)
        # 绘制星位（五子棋标记点）
        star_pos = [4, 7, 10]
        for x in star_pos:
            for y in star_pos:
                pygame.draw.circle(screen, (0, 0, 0), (x * CELL_SIZE, y * CELL_SIZE), 5)

# 绘制棋子
def draw_pieces():
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 1:  # 黑棋
                if black_piece:
                    screen.blit(black_piece, (j * CELL_SIZE + 5, i * CELL_SIZE + 5))
                else:
                    pygame.draw.circle(screen, (0, 0, 0), 
                                      (j * CELL_SIZE + CELL_SIZE//2, i * CELL_SIZE + CELL_SIZE//2), 
                                      CELL_SIZE//2 - 5)
            elif board[i][j] == 2:  # 白棋
                if white_piece:
                    screen.blit(white_piece, (j * CELL_SIZE + 5, i * CELL_SIZE + 5))
                else:
                    pygame.draw.circle(screen, (255, 255, 255), 
                                      (j * CELL_SIZE + CELL_SIZE//2, i * CELL_SIZE + CELL_SIZE//2), 
                                      CELL_SIZE//2 - 5, 0)
                    pygame.draw.circle(screen, (0, 0, 0), 
                                      (j * CELL_SIZE + CELL_SIZE//2, i * CELL_SIZE + CELL_SIZE//2), 
                                      CELL_SIZE//2 - 5, 2)

# 检查胜利
def check_win(row, col, player):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 横、竖、主副对角线
    for dx, dy in directions:
        count = 1
        # 正方向
        for k in range(1, 5):
            nx, ny = row + k * dx, col + k * dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[nx][ny] == player:
                count += 1
            else:
                break
        # 反方向
        for k in range(1, 5):
            nx, ny = row - k * dx, col - k * dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[nx][ny] == player:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            # 获取鼠标点击位置并转换为棋盘坐标
            x, y = event.pos
            col = x // CELL_SIZE
            row = y // CELL_SIZE
            # 检查是否在棋盘内且位置为空
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == 0:
                board[row][col] = current_player
                # 检查胜利
                if check_win(row, col, current_player):
                    game_over = True
                    winner = current_player
                # 切换玩家
                current_player = 3 - current_player  # 1和2互换
    
    # 绘制界面
    draw_board()
    draw_pieces()
    
    # 显示游戏状态
    font = pygame.font.SysFont(None, 30)
    if game_over:
        win_text = font.render(f"玩家 {'黑' if winner == 1 else '白'} 获胜！", True, (255, 0, 0))
        screen.blit(win_text, (WINDOW_SIZE[0]//2 - win_text.get_width()//2, 
                              WINDOW_SIZE[1]//2 - 30))
        restart_text = font.render("点击屏幕重新开始", True, (0, 0, 0))
        screen.blit(restart_text, (WINDOW_SIZE[0]//2 - restart_text.get_width()//2, 
                                  WINDOW_SIZE[1]//2 + 30))
    else:
        turn_text = font.render(f"current player: {'black' if current_player == 1 else 'white'}", 
                               True, (0, 0, 0))
        screen.blit(turn_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(FPS)
    
    # 游戏结束后点击屏幕重新开始
    if game_over and pygame.mouse.get_pressed()[0]:
        board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        current_player = 1
        game_over = False
        winner = 0

pygame.quit()
sys.exit()