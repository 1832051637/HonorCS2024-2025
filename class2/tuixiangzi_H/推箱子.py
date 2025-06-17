import turtle

boards = [
    [
        [4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 0, 0, 0, 0, 4],
        [4, 4, 4, 1, 1, 1, 0, 4],
        [4, 0, 1, 5, 2, 2, 0, 4],
        [4, 0, 0, 2, 2, 0, 0, 4],
        [4, 4, 4, 4, 0, 0, 0, 4],
        [4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4],
    ],
    [
        [4, 4, 4, 4, 4, 4, 4, 4],
        [4, 0, 0, 0, 0, 0, 0, 4],
        [4, 0, 0, 1, 0, 2, 0, 4],
        [4, 0, 1, 5, 1, 2, 0, 4],
        [4, 0, 0, 2, 0, 0, 0, 4],
        [4, 4, 4, 4, 0, 0, 0, 4],
        [4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4],
    ],
    [
        [4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 0, 0, 4, 4, 4, 4],
        [4, 5, 0, 0, 4, 4, 4, 4],
        [4, 4, 1, 0, 4, 4, 4, 4],
        [4, 4, 0, 1, 0, 4, 4, 4],
        [4, 2, 1, 0, 0, 4, 4, 4],
        [4, 2, 2, 1, 2, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4],
    ]
]

current_level = 0
s = 60  # 每个网格单元格的边长
width = s * 8 + 2 * s  # 固定窗口大小（所有关卡均为8x8）
height = s * 8 + 2 * s
tx = -s * 4  # 地图居中计算（8列时中心在0点）
ty = s * 4

boxs = []
targets = []
walls = []
prow, pcol = 0, 0

def init():
    turtle.setup(width, height)
    turtle.tracer(0)
    turtle.hideturtle()
    turtle.up()

def draw_rect(edge, bgcolor):
    turtle.down()
    turtle.fillcolor(bgcolor)
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(edge)
        turtle.right(90)
    turtle.end_fill()
    turtle.up()

def draw_bg():
    for j in range(8):  # 固定8x8网格
        for i in range(8):
            if i % 2 == j % 2:
                color = '#F0F0F0'
            else:
                color = '#D2D2D2'
            turtle.goto(tx + i * s, ty - j * s)
            draw_rect(s, color)

def load_board():
    global prow, pcol, boxs, targets, walls
    board = boards[current_level]
    boxs = []
    targets = []
    walls = []
    for j in range(8):
        for i in range(8):
            cell = board[j][i]
            if cell == 1:
                boxs.append([j, i])
            elif cell == 2:
                targets.append([j, i])
            elif cell == 4:
                walls.append([j, i])
            elif cell == 5:
                prow, pcol = j, i

def draw_elements():
    draw_bg()
    for r, c in targets:
        turtle.goto(tx + c * s, ty - r * s)
        draw_rect(s, '#7DCEA0')
    for r, c in boxs:
        turtle.goto(tx + c * s, ty - r * s)
        draw_rect(s, '#0532ff')
    for r, c in walls:
        turtle.goto(tx + c * s, ty - r * s)
        draw_rect(s, '#000000')
    turtle.goto(tx + pcol * s, ty - prow * s)
    draw_rect(s, '#FF9900')
    turtle.update()

def check_win():
    return all(box in targets for box in boxs)

def is_out_of_bounds(r, c):
    return r < 0 or r >= 8 or c < 0 or c >= 8

def move_up():
    global prow
    new_prow = prow - 1
    if is_out_of_bounds(new_prow, pcol) or [new_prow, pcol] in walls:
        return
    box_index = next((i for i, box in enumerate(boxs) if box == [new_prow, pcol]), None)
    if box_index is not None:
        new_box_prow = new_prow - 1
        if is_out_of_bounds(new_box_prow, pcol) or [new_box_prow, pcol] in walls or [new_box_prow, pcol] in boxs:
            return
        boxs[box_index] = [new_box_prow, pcol]
    prow = new_prow
    draw_elements()
    check_level_complete()

def move_down():
    global prow
    new_prow = prow + 1
    if is_out_of_bounds(new_prow, pcol) or [new_prow, pcol] in walls:
        return
    box_index = next((i for i, box in enumerate(boxs) if box == [new_prow, pcol]), None)
    if box_index is not None:
        new_box_prow = new_prow + 1
        if is_out_of_bounds(new_box_prow, pcol) or [new_box_prow, pcol] in walls or [new_box_prow, pcol] in boxs:
            return
        boxs[box_index] = [new_box_prow, pcol]
    prow = new_prow
    draw_elements()
    check_level_complete()

def move_left():
    global pcol
    new_pcol = pcol - 1
    if is_out_of_bounds(prow, new_pcol) or [prow, new_pcol] in walls:
        return
    box_index = next((i for i, box in enumerate(boxs) if box == [prow, new_pcol]), None)
    if box_index is not None:
        new_box_pcol = new_pcol - 1
        if is_out_of_bounds(prow, new_box_pcol) or [prow, new_box_pcol] in walls or [prow, new_box_pcol] in boxs:
            return
        boxs[box_index] = [prow, new_box_pcol]
    pcol = new_pcol
    draw_elements()
    check_level_complete()

def move_right():
    global pcol
    new_pcol = pcol + 1
    if is_out_of_bounds(prow, new_pcol) or [prow, new_pcol] in walls:
        return
    box_index = next((i for i, box in enumerate(boxs) if box == [prow, new_pcol]), None)
    if box_index is not None:
        new_box_pcol = new_pcol + 1
        if is_out_of_bounds(prow, new_box_pcol) or [prow, new_box_pcol] in walls or [prow, new_box_pcol] in boxs:
            return
        boxs[box_index] = [prow, new_box_pcol]
    pcol = new_pcol
    draw_elements()
    check_level_complete()

def check_level_complete():
    if check_win():
        global current_level
        current_level += 1
        if current_level < len(boards):
            load_board()
            draw_elements()
        else:
            turtle.goto(0, 0)
            turtle.write("pass", align="center", font=("Arial", 24, "normal"))

init()
load_board()
draw_elements()

turtle.listen()
turtle.onkeypress(move_up, "Up")
turtle.onkeypress(move_down, "Down")
turtle.onkeypress(move_left, "Left")
turtle.onkeypress(move_right, "Right")

turtle.mainloop()    