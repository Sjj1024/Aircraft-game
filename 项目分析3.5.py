"""
3.只产生爆炸效果,
3.1 敌人飞机发射子弹（但是敌军飞机消失后，子弹也消失了）
3.2 敌人飞机消失后，敌军子弹继续飞(敌军子弹只能再创建一个单独的类，不然和敌军分不开
3.4 开始界面的选择等
3.5 敌人飞机子弹和玩家飞机碰撞
项目分析：
1.项目组成：窗体，背景，玩家飞机，敌人飞机，子弹
2.动作分析：背景移动，玩家跟随鼠标移动，敌人飞机向下移动，子弹向上移动，敌人死亡后爆炸，开始的时候选项
3.业务分析，制作阶段：游戏如何结束，敌人飞机数，子弹飞行速度
"""
import sys
import random
import os
import time

import pygame
import pygame.locals

# TODO 设置公共的图片常量，方便管理
# 管理窗口出现的位置
pygame.init()  # 初始化
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (660, 30)

IMG_ICON = "res/app.ico"  # 窗体图标
ING_BACKGROUND = "res/img_bg_level_3.jpg"  # 背景图标
# IMG_ENEMYPLAN = "res/img-plane_4.png"
IMG_ENEMYPLAN = ("res/img-plane_1.png", "res/img-plane_2.png", "res/img-plane_3.png",
                 "res/img-plane_4.png", "res/img-plane_5.png", "res/img-plane_6.png",
                 "res/img-plane_7.png")  # 敌军飞机图标
IMG_PLAYER = "res/hero2.png"  # 玩家飞机图标
IMG_BUTTLE = "res/bullet_11.png"  # 玩家子弹图标
COUNT = 20  # 默认产生多少架敌机
LOCAL = 200  # 子弹默认出现的高度，默认是1到200


# TODO 将背景类、飞机、敌机、子弹等类共有的方法或属性单独提取出来，放到一个类中，让他们继承极好
class BeginTu:
    window = None  # 每次都需要有一个窗口

    def __init__(self, img_path, x, y):
        self.img = pygame.image.load(img_path)  # 图片路径,返回的是图片对象
        self.x = x
        self.y = y

    def display(self):
        BeginTu.window.blit(self.img, (self.x, self.y))


# TODO 设置背景类
class BackGround(BeginTu):
    """
    window = None

    # TODO 制作背景的构造方法，设置默认图片，x，y坐标
    def __init__(self, img_path, x, y):
        self.img = pygame.image.load(img_path)   # 图片路径,返回的是图片对象
        self.x = x
        self.y = y
    """

    def display(self):  # 设置背景显示方法
        self.window.blit(self.img, (self.x, self.y))  # 将背景对象和位置添加到窗体中

        # 再贴一个背景图片到原背景图上面，形成两张图片组合为一张，
        self.window.blit(self.img, (self.x, self.y - 768))

    def move(self):  # 设置背景移动方法

        if self.y <= Game.WINDOW_HIGHT:  # 判断背景的y轴是否大于窗体的高，是的话，重新开始
            self.y += 1
        else:
            self.y = 0


# TODO 设置玩家飞机
class PlayPlane(BeginTu):
    def __init__(self, img_path, x, y):  # 在玩家飞机属性里增加子弹属性，
        super().__init__(img_path, x, y)  # 需要重新调用父类里的构造方法
        self.buttle = []  # 添加玩家飞机子弹属性，为空列表

    def display(self, enemylist,
                enebul):  # 1.3 将子弹和敌军飞机形成的字典传入，1.2重写玩家飞机显示，传入敌军飞机，判断碰撞监测。# 1.需要用飞机类的显示方法，调用子弹类的显示方法，所以重写一下
        super().display()

        # 添加敌军飞机的子弹显示的判断
        for enebull in range(COUNT):
            if enemylist[enebull].y == enebul[enebull].y:  # 判断敌军飞机的位置是否达到子弹默认显示的位置
                if enebul[enebull].bulltdisply == False:  # 判断敌军飞机的子弹是否是显示的
                    enebul[enebull].bulltdisply = True  # 如果是不显示，改为显示状态
                    enebul[enebull].x = enemylist[enebull].x + 35  # 敌人飞机和子弹位置校准
                    enebul[enebull].y = enemylist[enebull].y + 24  # 敌人飞机子弹位置校准

            if enebul[enebull].bulltdisply:  # 判断敌军飞机子弹显示状态是否是显示
                enebul[enebull].y += 3  # 敌军飞机子弹的飞行速度
                enebul[enebull].display()  # 敌军飞机子弹显示

            # 判断敌军子弹是否超过了窗口边界，是的话，位置重新恢复，状态改为不显示
            if enebul[enebull].y > Game.WINDOW_HIGHT:
                enebul[enebull].y = random.randint(1, LOCAL)  # 敌军子弹显示位置初始化
                enebul[enebull].bulltdisply = False  # 敌军子弹默认不显示

        # 循环判断敌机子弹和玩家飞机是否碰撞
        for enbu in enebul:
            # 设置敌机子弹分矩形方位
            enemy_rect = pygame.locals.Rect(enbu.x, enbu.y, 15, 46)  # 创建敌机子弹矩形对象
            player_rect = pygame.locals.Rect(self.x, self.y, 70, 50)  # 创建玩家矩形对象
            if pygame.Rect.colliderect(enemy_rect, player_rect):
                # 如果敌机个玩家给你碰撞，则敌人飞机消失
                enbu.bulltdisply = False  # 敌人飞机设置为被击中状态
                pygame.mixer.music.load("res/gameover.wav")  # 添加死亡后背景音乐路径
                pygame.mixer.music.play()  # 播放音乐文件

                return 2  # 设置一个返回值，表示游戏状态为游戏结束

        # 判断敌军子弹和玩家子弹是否碰撞


        # 判断玩家子弹和敌军飞机是否碰撞
        for but in self.buttle:
            but.move()
            but.display()
            # 飞机和子弹碰撞监测，先创建子弹矩形，再创建敌军飞机矩形
            buttle_rect = pygame.locals.Rect(but.x, but.y, 10, 30)

            # 如果子弹飞出去了显示边界，则不作判断监测了
            if but.y > -40:
                for enemy in enemylist:  # 循环遍历出敌军飞机列表中的敌人飞机，因为传进来的参数是enemylist，则可以直接使用这个字符
                    enemy_rect = pygame.locals.Rect(enemy.x, enemy.y, 100, 48)
                    # 判断子弹击中敌军飞机没有，
                    if pygame.Rect.colliderect(buttle_rect, enemy_rect):
                        # print("击中了敌军飞机")
                        enemy.hite = True  # 设置敌机的击中状态为被击中，则敌机的移动方法就会失效，开始运行初始化状态，并将击中状态设为未击中
                        enemy.bomb.show = True
                        enemy.bomb.x = enemy.x
                        enemy.bomb.y = enemy.y
                        # 如果子弹击中了飞机，则子弹消失
                        self.buttle.remove(but)
                        # 如果敌人飞机消失了，则退出此次循环
                        # 播放击中后的音效
                        sound = pygame.mixer.Sound("res/bomb.wav")
                        sound.play()
                        break

        # 循环判断敌机和玩家飞机是否碰撞
        for enemy in enemylist:
            # 设置敌机分矩形方位
            enemy_rect = pygame.locals.Rect(enemy.x, enemy.y, 100, 68)  # 创建敌机矩形对象
            player_rect = pygame.locals.Rect(self.x, self.y, 70, 50)  # 创建玩家矩形对象
            if pygame.Rect.colliderect(enemy_rect, player_rect):
                # 如果敌机个玩家给你碰撞，则敌人飞机消失
                enemy.hite = True  # 敌人飞机设置为被击中状态
                pygame.mixer.music.load("res/gameover.wav")  # 添加死亡后背景音乐路径
                pygame.mixer.music.play()  # 播放音乐文件

                return 2  # 设置一个返回值，表示游戏状态为游戏结束

        # 判断子弹列表不为空，并且子弹列表最后一位子弹小于y轴坐标，则清空子弹列表即可
        if self.buttle != [] and self.buttle[len(self.buttle) - 1].y < -20:
            self.buttle.clear()

        return 1  # 设置一个返回值，表示游戏正在进行中


# TODO 设置敌军飞机
class EnemyPlane(BeginTu):
    def __init__(self):
        self.img = pygame.image.load(IMG_ENEMYPLAN[random.randint(0, 6)])  # 图片路径,返回的是图片对象
        self.x = random.randint(0, Game.WINDOW_WIDE - 100)  # 敌军飞机产生时，默认的x轴位置随机
        self.y = random.randint(-2000, -60)  # 敌军飞机产生时，默认的y轴位置随机
        self.mx = random.randint(-1, 1)  # 敌军飞机产生时，默认随机左右移动属性
        self.hite = False  # 设置敌人飞机被子弹击中状态为未击中
        self.bomb = Bomb()  # 为敌机添加爆炸属性
        # [pygame.image.load("res/bullet_6.png") for i in range(1, 4)]  # 为敌人飞机添加发射子弹属性

    # 设置敌军飞机移动方法
    def move(self):
        if self.y <= Game.WINDOW_HIGHT and not self.hite:  # 1.2并且飞机状态为未击中才做下面的飞行，判断背景的y轴是否大于窗体的高，是的话，重新开始
            self.y += 2  # 敌机的飞行速度
            if -10 < self.x < Game.WINDOW_WIDE - 90:
                self.x += self.mx
            elif self.x == -10:  # 飞机碰到左边边缘后，返回
                self.mx = -self.mx
                self.x = self.x + 1
            elif self.x == Game.WINDOW_WIDE - 90:  # 飞机碰到右边边缘后返回
                self.mx = -self.mx
                self.x = self.x - 1
                # if random.randint(0, 5) in range(1, 3):
                #     self.x += 2
                # # else:
                # #     self.x -= 1
        else:  # 敌人飞机超过窗口边界，或者被击中后，所有属性初始化
            self.y = random.randint(-2000, -60)  # 敌机的初始坐标应该y轴的上面，敌机的高是68，所以应该让敌机从最高处往下飞
            self.x = random.randint(0, Game.WINDOW_WIDE - 100)  # 敌人飞机的x轴位置初始化
            self.img = pygame.image.load(IMG_ENEMYPLAN[random.randint(0, 6)])  # 图片路径,返回的是图片对象
            self.mx = random.randint(-1, 1)  # 敌人飞机左右移动初始化
            self.hite = False  # 敌人被击中状态初始化

    # 敌军显示的操作，并且添加爆炸显示效果
    def display(self):
        super().display()
        if self.bomb.show:
            self.bomb.display()


# TODO 设置子弹类
class Bullent(BeginTu):
    def move(self):
        self.y -= 5


# TODO 设置敌人子弹的类
class EnemyBull(BeginTu):
    def __init__(self, img_path, x, y):
        super().__init__(img_path, x, y)
        # 判断子弹是否开始显示并且移动的波尔类型，
        self.bulltdisply = False
        self.sby = random.randint(1, LOCAL)  # 产生子弹随机出现的y轴坐标


# TODO 设置爆炸效果类
class Bomb:  # 定义了一个爆炸效果类
    def __init__(self):
        self.x = None  # 定义了一个爆炸效果y轴
        self.y = None  # 定义了一个爆炸效果x轴
        # 定义了一个爆炸图片显示
        self.imag = [pygame.image.load("res/bomb-" + str(i) + ".png") for i in range(1, 7)]
        self.show = False  # 定义了一个爆炸效果是否
        self.times = 0

    def display(self):
        if self.show and self.times < len(self.imag) * 10:
            BeginTu.window.blit(self.imag[self.times // 10], (self.x, self.y))
            self.times += 1
        # 如果图片显示完，就让显示从0重新开始，而且将show默认显示改为不显示
        else:
            self.times = 0
            self.show = False


# TODO 设置游戏主题
class Game:
    # 设置常量属性，窗体的宽和高x，y
    WINDOW_HIGHT = 768
    WINDOW_WIDE = 512
    window = pygame.display.set_mode((WINDOW_WIDE, WINDOW_HIGHT))  # 设置窗体大小，宽和高
    game_sate = 0  # 设置默认游戏初始状态，0表示游戏未开始，1表示游戏进行中，2表示游戏结束

    # TODO 主程序入口
    def run(self):
        pygame.init()  # 初始化pygame读取系统操作
        self.frame_init()  # 执行窗体初始化
        self.model_init()  # 执行元素初始化
        pygame.mixer.init()  # 背景音混音模式

        pygame.mixer.music.load("res/bg.wav")  # 添加背景音乐路径
        pygame.mixer.music.play()  # 播放音乐文件

        # 设置窗体持续刷新
        while True:
            self.background.move()  # 持续背景移动
            # self.myenm.display()  # 运行敌机显示的方法，如果放在这里，敌军将不会显示
            self.background.display()  # 背景移动完还需要继续显示

            if self.game_sate == 0:  # 表示游戏未开始状态
                font_over = pygame.font.Font("res/DENGB.TTF", 60)  # 选择字体对象
                text = font_over.render("飞机大战哦", 1, (255, 0, 0))  # 创建文本对象颜色等
                self.window.blit(text, pygame.locals.Rect(113, 200, 400, 400))  # 将文本对象添加到窗体中

                font_over = pygame.font.Font("res/DENGB.TTF", 40)  # 选择字体对象
                text = font_over.render("请选择难度：", 1, (3, 15, 250))  # 创建文本对象颜色等
                self.window.blit(text, pygame.locals.Rect(163, 300, 400, 400))  # 将文本对象添加到窗体中

                font_over = pygame.font.Font("res/DENGB.TTF", 40)  # 选择字体对象
                text = font_over.render("1、超级简单", 1, (0, 150, 255))  # 创建文本对象颜色等
                self.window.blit(text, pygame.locals.Rect(163, 350, 400, 400))  # 将文本对象添加到窗体中

                font_over = pygame.font.Font("res/DENGB.TTF", 40)  # 选择字体对象
                text = font_over.render("2、普通模式", 1, (246, 255, 0))  # 创建文本对象颜色等
                self.window.blit(text, pygame.locals.Rect(163, 400, 400, 400))  # 将文本对象添加到窗体中

                font_over = pygame.font.Font("res/DENGB.TTF", 40)  # 选择字体对象
                text = font_over.render("3、敌机发疯", 1, (255, 18, 0))  # 创建文本对象颜色等
                self.window.blit(text, pygame.locals.Rect(163, 450, 400, 400))  # 将文本对象添加到窗体中

            if self.game_sate == 1:  # 表示游戏进行中
                # self.myenm.display()  # 运行敌机显示的方法
                # self.myenm.move()  # 敌机的移动方法
                for enemy in range(len(self.enemylist)):  # 敌机循环显示
                    self.enemylist[enemy].move()  # 敌军飞机移动
                    self.enemylist[enemy].display()  # 敌军飞机显示

                # 将敌军飞机列表和子弹列表传入到玩家显示方法中
                # 1.2 因为子弹，玩家飞机都在玩家飞机显示中，所以将敌人飞机列表穿进去到玩家飞机显示中做碰撞监测。 # 玩家飞机刷新显示
                self.game_sate = self.hero.display(self.enemylist, self.enemybullt)

            if self.game_sate == 2:  # 表示游戏结束
                font_over = pygame.font.Font("res/DENGB.TTF", 40)  # 选择字体对象
                text = font_over.render("嗝屁了吧", 1, (255, 0, 0))  # 创建文本对象
                self.window.blit(text, pygame.locals.Rect(183, 300, 400, 400))  # 将文本对象添加到窗体中

            pygame.display.update()  # 持续刷新窗体，才会看到窗体
            self.event_init()  # 持续检测事件

    def frame_init(self):  # TODO 初始化窗体
        BeginTu.window = self.window  # 将背景类中的窗体设置为game类中一样
        img = pygame.image.load(IMG_ICON)  # 设置窗体的图标
        pygame.display.set_icon(img)  # 设置窗体的图标
        pygame.display.set_caption("飞机大战项目1.0V sjj")  # 设置设置窗体标题

    def event_init(self):  # TODO 窗体检测事件
        for event in pygame.event.get():  # 点击窗口关闭事件，持续监测
            if event.type == pygame.locals.QUIT:
                sys.exit()

            if event.type == pygame.locals.MOUSEMOTION and self.game_sate == 1:  # 玩家飞机随鼠标移动而移动的设置
                pos = pygame.mouse.get_pos()  # 获取鼠标的位置
                self.hero.x = pos[0] - 60  # 玩家飞机和鼠标显示位置微调
                self.hero.y = pos[1] - 48  # 玩家飞机和鼠标显示位置微调

            if event.type == pygame.locals.KEYDOWN and self.game_sate == 0:  # 判断键盘按下事件，并且游戏状态为未开始
                if event.key == pygame.locals.K_1:
                    COUNT = 20
                    for x in range(COUNT):  # 循环产生多少架飞机
                        randomx = random.randint(1, LOCAL)  # 随机产生一个子弹要显示的位置y轴
                        enemybull = EnemyBull("res/bullet_6.png", 0, randomx)  # 创建一个子弹对象
                        self.enemylist.append(EnemyPlane())  # 将敌人飞机添加到敌人飞机列表中
                        self.enemybullt.append(enemybull)  # 将子弹添加到子弹列表中
                        self.enebul[x] = enemybull  # 将敌军飞机和子弹配对
                        self.game_sate = 1

                elif event.key == pygame.locals.K_2:  # 判断键盘按下是不是2
                    COUNT = 100
                    for x in range(COUNT):  # 循环产生多少架飞机
                        randomx = random.randint(1, LOCAL)  # 随机产生一个子弹要显示的位置y轴
                        enemybull = EnemyBull("res/bullet_6.png", 0, randomx)  # 创建一个子弹对象
                        self.enemylist.append(EnemyPlane())  # 将敌人飞机添加到敌人飞机列表中
                        self.enemybullt.append(enemybull)  # 将子弹添加到子弹列表中
                        self.enebul[x] = enemybull  # 将敌军飞机和子弹配对
                        self.game_sate = 1

                elif event.key == pygame.locals.K_3:  # 判断键盘按下是不是3
                    COUNT = 150
                    for x in range(COUNT):  # 循环产生多少架飞机
                        randomx = random.randint(1, LOCAL)  # 随机产生一个子弹要显示的位置y轴
                        enemybull = EnemyBull("res/bullet_6.png", 0, randomx)  # 创建一个子弹对象
                        self.enemylist.append(EnemyPlane())  # 将敌人飞机添加到敌人飞机列表中
                        self.enemybullt.append(enemybull)  # 将子弹添加到子弹列表中
                        self.enebul[x] = enemybull  # 将敌军飞机和子弹配对
                        self.game_sate = 1

        if self.game_sate == 1:  # 如果游戏状态为运行中，则开始用鼠标操作飞机
            # 按下鼠标左键发射子弹的操作
            event_mouse = pygame.mouse.get_pressed()  # 获取鼠标按键事件，返回的是包含三个数据的元组。左键，中间，右键2
            if event_mouse[0] == 1:  # 判断鼠标左键等于1，说明按下去了，
                pos = pygame.mouse.get_pos()  # 获取鼠标对应的位置，即可推测子弹出现的位置
                self.hero.buttle.append(Bullent(IMG_BUTTLE, pos[0] - 10, pos[1] - 80))  # 在飞机子单属性里添加子弹对象

                # if event_mouse[0] == 0:
                #     if self.hero.buttle[len(self.hero.buttle) - 1].y < -20:
                #         self.hero.buttle.clear()

    def model_init(self):  # TODO 初始化窗体背景对象
        self.background = BackGround(ING_BACKGROUND, 0, 0)  # 产生背景对象
        # self.myenm = EnemyPlane(IMG_ENEMYPLAN, 100, 0)
        """
        self.window.blit(background.img, (background.x, background.y))

        # 因为下面这段代码会在run里面持续运行，这里就不需要了
        self.background.display()  # 调用背景显示的方法
        self.background.move()    # 调用背景移动的方法
        """
        # 循环产生多架敌机，并存放到列表对象中
        self.enemylist = []  # 敌人飞机队列
        self.enemybullt = []  # 循环产生多个敌军子弹对象，
        self.enebul = {}  # 将飞机和子弹一一对应的字典对象
        # for x in range(COUNT):  # 循环产生多少架飞机
        #     randomx = random.randint(1, LOCAL)   # 随机产生一个子弹要显示的位置y轴
        #     enemybull = EnemyBull("res/bullet_6.png", 0, randomx)  # 创建一个子弹对象
        #     self.enemylist.append(EnemyPlane())  # 将敌人飞机添加到敌人飞机列表中
        #     self.enemybullt.append(enemybull)  # 将子弹添加到子弹列表中
        #     self.enebul[x] = enemybull  # 将敌军飞机和子弹配对
        """
        self.enemylist.append(EnemyPlane(IMG_ENEMYPLAN, random.randint(0, Game.WINDOW_WIDE - 100), random.randint(-300, -60)))
        """
        self.hero = PlayPlane(IMG_PLAYER, 200, 600)  # 产生玩家飞机


# TODO 设置测试程序
if __name__ == '__main__':
    Game().run()
