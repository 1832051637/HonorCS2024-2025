import tkinter as tk
import random

GRID_LEN = 4

class Game2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title('2048')
        self.grid()
        self.master.bind("<Key>", self.key_down)
        self.commands = {
            "Up": self.move_up,
            "Down": self.move_down,
            "Left": self.move_left,
            "Right": self.move_right
        }
        self.grid_cells = []
        self.score = 0
        self.won = False

        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()
        self.mainloop()

    def init_grid(self):
        #创建分数显示
        self.score_label = tk.Label(self, text=f"Score: {self.score}", font=(18))
        self.score_label.grid(row=0, column=0, columnspan=4)
        #创建游戏背景
        background = tk.Frame(self, bg="#92877d", width=1000, height=1000)
        background.grid(row=1, column=0, columnspan=4)
        #创建游戏重新开始按钮
        restart_btn = tk.Button(self, text="Restart", font=(14), command=self.restart_game)
        restart_btn.grid(row=0, column=2, columnspan=2)
        #创建4x4的游戏网格
        for i in range(GRID_LEN):
            row = []
            for j in range(GRID_LEN):
                cell = tk.Frame(
                    background,
                    bg="#9e948a",
                    width=100,
                    height=100
                )
                cell.grid(row=i, column=j, padx=10, pady=10)#设置每个单元格并添加间距
                t = tk.Label(
                    master=cell,
                    text="",
                    bg="#9e948a",
                    justify=tk.CENTER,
                    font=("Helvetica", 24, "bold"),
                    width=4,
                    height=2
                )
                t.grid()
                row.append(t)
            self.grid_cells.append(row)
    #初始化游戏数据矩阵
    def init_matrix(self):
        self.matrix = [[0] * GRID_LEN for _ in range(GRID_LEN)]
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        #收集所有空白单元格的坐标
        empty_cells = [(i, j) for i in range(GRID_LEN) for j in range(GRID_LEN) if self.matrix[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)#随机选择一个空白位置
            self.matrix[i][j] = 2 if random.random() < 0.9 else 4

    def update_grid_cells(self):#更新界面显示
        self.score_label.config(text=f"Score: {self.score}")
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                value = self.matrix[i][j]
                if value == 0:
                    self.grid_cells[i][j].configure(text="", bg="#9e948a")
                else:
                    self.grid_cells[i][j].configure(
                        text=str(value),
                        bg="#f2b179" if value == 2 else "#f59563"
                    )
        self.update_idletasks()
    
    def key_down(self, event):
        key = event.keysym
        if key in self.commands and not self.is_game_over():
            moved = self.commands[key]()
            if moved:
                self.add_new_tile()
                self.update_grid_cells()
                if self.has_won() and not self.won:
                    self.won = True
                    self.show_message("You Win!")
                elif self.is_game_over():
                    self.show_message("Game Over")
    #建立弹窗
    def show_message(self, text):
        popup = tk.Toplevel()
        popup.title("2048")
        msg = tk.Label(popup, text=text, font=("Helvetica", 24, "bold"))
        msg.pack(padx=20, pady=20)
        ok = tk.Button(popup, text="OK", command=popup.destroy)
        ok.pack(pady=(0, 20))
    #移除空格 检测有没有合并成功 矩阵有没有发生改变
    def compress(self, mat):
        new_mat = [[0] * GRID_LEN for _ in range(GRID_LEN)]
        changed = False
        for i in range(GRID_LEN):
            pos = 0
            for j in range(GRID_LEN):
                if mat[i][j] != 0:
                    new_mat[i][pos] = mat[i][j]
                    if j != pos:
                        changed = True
                    pos += 1
        return new_mat, changed
    #合并相邻相同的方块
    def merge(self, mat):
        changed = False
        for i in range(GRID_LEN):
            for j in range(GRID_LEN - 1):
                if mat[i][j] != 0 and mat[i][j] == mat[i][j + 1]:
                    mat[i][j] *= 2
                    self.score += mat[i][j]
                    mat[i][j + 1] = 0
                    changed = True
        return mat, changed

    def reverse(self, mat):
        return [row[::-1] for row in mat]

    def transpose(self, mat):
        return [list(row) for row in zip(*mat)]

    def move_left(self):
        mat, changed1 = self.compress(self.matrix)
        mat, changed2 = self.merge(mat)
        mat, _ = self.compress(mat)
        self.matrix = mat
        return changed1 or changed2

    def move_right(self):
        self.matrix = self.reverse(self.matrix)
        moved = self.move_left()
        self.matrix = self.reverse(self.matrix)
        return moved

    def move_up(self):
        self.matrix = self.transpose(self.matrix)
        moved = self.move_left()
        self.matrix = self.transpose(self.matrix)
        return moved

    def move_down(self):
        self.matrix = self.transpose(self.matrix)
        moved = self.move_right()
        self.matrix = self.transpose(self.matrix)
        return moved
    #检查游戏是否结束
    def is_game_over(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                if self.matrix[i][j] == 0:
                    return False
                if j < GRID_LEN - 1 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    return False
                if i < GRID_LEN - 1 and self.matrix[i][j] == self.matrix[i + 1][j]:
                    return False
        return True
    #检查是否获胜
    def has_won(self):
        return any(any(cell >= 2048 for cell in row) for row in self.matrix)
    #重新开始游戏
    def restart_game(self):
        self.matrix = [[0] * GRID_LEN for _ in range(GRID_LEN)]
        self.score = 0
        self.won = False
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid_cells()

#程序入口
if __name__ == '__main__':
    Game2048()