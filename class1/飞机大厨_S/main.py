
import random

import pygame
from pygame.locals import *
import sys
from pygame.sprite import Sprite
# 定义类  ，子弹类，敌机类，玩家类 （子类与敌机会产生碰撞，敌机和玩家产生碰撞）
class Bullet(Sprite): # 创建一个精灵类
    def __init__(self,bullet_img,init_pos):
        Sprite.__init__(self)  # 调用父类的初始化方法
        self.image=bullet_img
        self.rect=self.image.get_rect() #
        self.rect.midbottom=init_pos
        self.speed=10 # 子弹的运行速度
    def move(self): # 子弹是向上移动，还是向下移动
        self.rect.top-=self.speed # 子弹向上移动，修改的是y坐标，
# 玩家类
class Player(Sprite):
    def __init__(self,play_rect,init_pos):
        Sprite.__init__(self)
        self.image=[] # 存储玩家飞机图片
        for i in range(len(play_rect)):
            self.image.append(play_rect[i].convert_alpha())
        self.rect=play_rect[0].get_rect() # 每个图片的大小都是一致,获取一个就可以
        self.rect.topleft=init_pos
        self.speed=8
        self.bullets=pygame.sprite.Group() # 精灵组
        self.img_index=0
        self.is_hit=False # 是否被击中

    #玩家的飞机，可以发射子弹
    def shoot(self,bullet_img):  # self.rect是玩家飞机的矩形
        bullet=Bullet(bullet_img,self.rect.midbottom)
        self.bullets.add(bullet) # 子弹要放到精灵组中
    # 玩家的移动方向有哪些？上，下，左，右
    def move_up(self):
        if self.rect.top<=0: # 飞机的矩形距离y轴已经小于等于0
            self.rect.top=0
        else:
            self.rect.top-=self.speed # 否则就继续向上运行

    def move_down(self):
        if self.rect.top>=HEIGHT-self.rect.height:
            self.rect.top=HEIGHT-self.rect.height
        else:
            self.rect.top+=self.speed
    def move_left(self):
        if self.rect.left<=0:
            self.rect.left=0
        else:
            self.rect.left-=self.speed
    def move_right(self):
        if self.rect.left>=WIDTH-self.rect.width:
            self.rect.left=WIDTH-self.rect.width
        else:
            self.rect.left+=self.speed

# 敌机类
class  Enemy(Sprite):
    def __init__(self,enemy_img,enemy_down_imgs,init_pos):
        Sprite.__init__(self)
        self.image=enemy_img # 敌机的图片
        self.rect=self.image.get_rect()
        self.rect.topleft=init_pos # topleft左上角
        self.down_imgs=enemy_down_imgs
        self.speed=2 # 如果希望游戏的刺激性增加，设置speed的值大点
        self.down_index=0
    def move(self): # 敌机向下移动，距离y轴的0点，越来越大
        self.rect.top+=self.speed

def write_txt(path,content):
    with open(path,'w',encoding='utf-8') as file:
        file.write(content)

SIZE=WIDTH,HEIGHT=480,700
pygame.init() # 初始化
screen=pygame.display.set_mode(SIZE)
pygame.display.set_caption('飞机大战')
# 设置小图标
icon=pygame.image.load('image/red_logo.png').convert_alpha()
pygame.display.set_icon(icon)
bg=pygame.image.load('image/background.png').convert_alpha()
# 加载图片
#加载gameover
game_over=pygame.image.load('image/gameover.png').convert_alpha()
#加载子弹图片
plane_bullet=pygame.image.load('image/bullet.png').convert_alpha()
#加载玩家飞机
player_img1=pygame.image.load('image/player1.png').convert_alpha()
player_img2=pygame.image.load('image/player2.png').convert_alpha()
player_img3=pygame.image.load('image/player_off1.png').convert_alpha()
player_img4=pygame.image.load('image/player_off2.png').convert_alpha()
player_img5=pygame.image.load('image/player_off3.png').convert_alpha()
#加载敌机的图片
enemy_img1=pygame.image.load('image/enemy1.png').convert_alpha()
enemy_img2=pygame.image.load('image/enemy2.png').convert_alpha()
enemy_img3=pygame.image.load('image/enemy3.png').convert_alpha()
enemy_img4=pygame.image.load('image/enemy4.png').convert_alpha()

# 创建时间管理对象
click=pygame.time.Clock()
FPS=60

def start_game(): # 定义函数
    #设置玩儿家不同状态图片列表
    player_rect=[]
    #玩家飞机
    player_rect.append(player_img1)
    player_rect.append(player_img2)
    #玩家飞机被炸飞的状态
    player_rect.append(player_img2)
    player_rect.append(player_img3)
    player_rect.append(player_img4)
    player_rect.append(player_img5)
    player_posi=(200,600)
    # 创建玩家类的对象
    player=Player(player_rect,player_posi)
    #子弹图片
    bullet_img=plane_bullet  # 83行加载过来的图片
    # 敌机不同的状态
    enemy1_img=enemy_img1   #91行加载的图片
    enemy1_rect=enemy1_img.get_rect() # 获取子弹的矩形
    enemy1_down_imgs=[]
    enemy1_down_imgs.append(enemy_img1)
    enemy1_down_imgs.append(enemy_img2)
    enemy1_down_imgs.append(enemy_img3)
    enemy1_down_imgs.append(enemy_img4)
    #存储敌机，精灵组
    enemies=pygame.sprite.Group()
    # 敌机被炸毁
    enemies_down=pygame.sprite.Group()
    #初始化射击及敌机移动的频率 （多长时间出现一架敌机）
    shoot_frequency=0 # 战机射击的频率
    enemy_frequency=0 # 敌机的频率
    score=0 #存储得分
    # 玩儿家飞机被击中， # 玩家飞机有6种状态，0，1，2，3，4，5
    player_down_index=16 # 为什么是16
    score_font=pygame.font.SysFont(None,36)
    running=True
    while running: # 为什么没有直接写True，因为后面会用到 running变量的值
        screen.fill((0,0,0))
        screen.blit(bg,(0,0)) # 在screen窗口中绘制背景
        #判断玩家的战机是否被击中
        if not player.is_hit: # is_hit赋的初始值为False
            #战机没有被击中时，发射子弹
            if shoot_frequency%15==0: #与15的余数为0时发射子弹
                player.shoot(bullet_img) # bullet_img子弹图片
            shoot_frequency+=1
            if shoot_frequency>=15:
                shoot_frequency=0
        #138到144是把子弹的图片放到的了精灵组中
        #遍历玩家的子弹列表
        for bullet in player.bullets:#从玩家的子弹的精灵组中遍历
            bullet.move()# 子弹要移动
            if bullet.rect.bottom<0:  #出屏幕，出的是屏幕上方，还是下方
                player.bullets.remove(bullet) # 从列表中移除数据子弹
        #显示子弹
        player.bullets.draw(screen) # 把子弹绘制到屏幕上
        #生成敌机，控制生成的频率
        if enemy_frequency%50==0:
            # 敌机的x坐标范围为0到800-敌机矩形宽度
            enempy1_pos=(random.randint(0,WIDTH-enemy1_rect.width),0)
            #创建敌机对象
            enempy1=Enemy(enemy1_img,enemy1_down_imgs,enempy1_pos)
            #把敌机对象，添加到敌机的精灵组中
            enemies.add(enempy1)
        enemy_frequency+=1
        if enemy_frequency>=50:
            enemy_frequency=0
        #遍历敌机的精灵组
        for enemy in enemies: # enemy是一个Enemy类型的对象
            enemy.move() # 敌机要移动
            #敌机与玩家飞机碰撞，两个精灵之间的碰撞
            if pygame.sprite.collide_circle(enemy,player):
                enemies_down.add(enemy) # 存的是敌机
                enemies.remove(enemy) # 从精灵组中移除
                player.is_hit=True
                break # 退出 167行for
            # 如果敌机移动出屏幕了
            if enemy.rect.top>800:
                enemies.remove(enemy)

        # 检查碰撞 ，敌机和子弹是否产生碰撞 # enemies敌机的精灵组 127行定义的
        enemies1_down=pygame.sprite.groupcollide(enemies,player.bullets,True,True)
        for enemy_down in enemies1_down:
            enemies_down.add(enemy_down) # 将被炸毁的敌机放到被炸毁的敌机的精灵组中
        #显示敌机的精灵组
        enemies.draw(screen)
        #绘制玩家战机
        if not player.is_hit: #is_hit为False时表示没有被击了
            # player.image[player.img_index]  根据索引到列表中取值
            screen.blit(player.image[player.img_index],player.rect)
            # 战机正常状态有索引有两个，一个是0，一个是1
            # 更换战机图片，产生动画的效果
            player.img_index=shoot_frequency//8
        else: # 战机被击中的情况（图片的索引是2，3，4，5
            # 战机被击中后的player.img_index=2
            player.img_index=player_down_index//8 # player_down_index的初始值为16
            # player.image[player.img_index]根据索引到列表中取值
            screen.blit(player.image[player.img_index],player.rect)
            player_down_index+=1
            if player_down_index>47:
                #游戏就该结束了
                running=False

        #敌机被子弹击中后效果显示
        for enemy_down in enemies_down: # 从碰撞的精灵组中遍历
             #  对象名，敌机对象   down_index是属性名
             # down_index 68行被定义的，敌机对象的属性
            if enemy_down.down_index==0: #down_index的值为0，敌机正常状态
                pass
            if enemy_down.down_index>7: # 敌机被击中的情况
                enemies_down.remove(enemy_down)
                score+=100
                continue
            # 敌机正常时就要绘制敌机down_imgs 66行被定义
            screen.blit(enemy_down.down_imgs[ enemy_down.down_index//2],enemy_down.rect)
            enemy_down.down_index+=1

        # 绘制当前得分
        score_text=score_font.render(str(score),True,(255,255,255))
        text_rect=score_text.get_rect()
        text_rect.topleft=(10,10)
        screen.blit(score_text,text_rect)

        for event in pygame.event.get():
            if event.type==QUIT:
                sys.exit()
        # 玩家战机上下，左右移动
        key_pressed=pygame.key.get_pressed() # 获取键盘事件
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.move_right()
        # 我方战机被炸，游戏结束
        if player.is_hit:
            screen.blit(game_over,(0,0))
            font=pygame.font.SysFont(None,48)
            text=font.render('Score:'+str(score),True,(255,255,255))
            screen.blit(text,(150,400))
            # 显示分数
            write_txt('score.txt', str(score))
            # 开始按钮
            font=pygame.font.SysFont('SimHei',48)
            text=font.render('重新开始',True,(255,255,255))
            #print(text.get_rect())
            screen.blit(text,(150,500))

        click.tick(FPS)
        pygame.display.update()
start_game() # 函数的调用
# 结束之后，程序先不关闭
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            sys.exit()
        if event.type==MOUSEBUTTONDOWN: # 判断是否点击了"重新开始"
            # 192中“重新开始”字体的宽 ,48 是高
            if 150<event.pos[0]<150+192 and  500<event.pos[1]<500+48:
                #这个范围内就是点中按钮
                start_game() # 重新开始
