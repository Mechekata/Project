import pygame

# from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton)
# from PyQt5.QtCore import Qt

from map import *
from time import time

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('best_m.mp3')
pygame.mixer.music.load('music_t.mp3')
pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)

# window2 = QWidget()
# window2.setLayout(main_line)

# app = QApplication([])

# main_line = QHBoxLayout()

# play_btn = QPushButton('Грати')
# main_line.addWidget(play_btn)

#висота та ширина
w_win = 700
h_win = 500
level_width = 2800

#кольори
blue = (125, 249, 255)
green = (62, 218, 148)
red = (255, 0, 0)
bleck = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 228, 107)
blue2 = (0, 1, 49)

#створи вікно гри
pygame.display.set_caption('platformer')
window = pygame.display.set_mode((w_win, h_win))

FPS = 55
clock = pygame.time.Clock()

gravity_speed = 3
blocks = []
blocks2 = []
block_size = 20
block_size2 = 40
y = 0
x = 0
blocks_update = True

jump_count = 40

# # изночяльное время
# start_time = time()

# #задай фон сцени
img_load = pygame.image.load('block_wall.png')
img_load = pygame.transform.scale(img_load, (w_win, h_win))
G_menu = pygame.image.load('block_wall.png')
G_Menu = pygame.transform.scale(G_menu, (w_win, h_win))

#музика
# music = pygame.mixer_music.load("music.mp3")
# music = pygame.mixer_music.play(-1)

# супер клас
class game_sprite():
    def __init__ (self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
    def update(self):
        window.blit(self.image, (self.rect.x - camera.rect.x, self.rect.y - camera.rect.y))
    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            return True
        else:
            return False

class Camera:
    def __init__(self, x, y, w, h, speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
    def move(self, player): 
            if player.rect.x > self.rect.x:
                if self.rect.right < level_width:
                    if player.rect.x > self.rect.x + int(0.7*self.rect.w):
                        self.rect.x += self.speed
            elif player.rect.x < self.rect.x:
                if self.rect.left < level_width:
                    if player.rect.x > self.rect.x - int(0.7*self.rect.w):
                        self.rect.x -= self.speed
        


camera = Camera(0, 0, w_win, h_win, 2)

#клас гравців
class Player(game_sprite):
    def __init__ (self, x, y, w, h, image, speed, gravity_speed, jump_speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.gravity_speed = gravity_speed
        self.jumping = False
        self.jump_count = 0
        self.can_jump = False
    def move(self, right, left):
        x_player = self.rect.x
        move_ = pygame.key.get_pressed()  
        if move_[right]:
            for block in blocks:
                if self.collide(block):
                    self.rect.x = x_player
                    return
            # if self.rect.x <= w_win - self.rect.width:
            # self.rect.x += self.speed
            self.rect.x += self.speed
        if move_[left]:
            for block in blocks:
                if self.collide(block):
                    self.rect.x = x_player
                    return
            # if self.rect.x >= 0:
            # self.rect.x -= self.speed
            self.rect.x -= self.speed

    # def jump(self):
    #     # up = pygame.key.get_pressed()
    #     # if up[pygame.K_SPACE]:
    #     #     self.rect.y -= 35
    def jump(self):
        if not self.jumping and self.can_jump:
            self.jumping = True
            self.jump_count = 35

    def gravity(self):
        y_player = self.rect.y
        if not self.jumping:
            self.rect.y += self.gravity_speed
            for block in blocks:
                if self.collide(block):
                    self.rect.y = y_player
                    self.can_jump = True
                    return
            self.can_jump = False
        else: 
            self.rect.y -= self.speed
            self.jump_count -= 1
            if self.jump_count == 0:
                self.jumping = False
            for block in blocks:
                if self.collide(block):
                    self.rect.y = y_player
                    return
            
            # self.rect.y += self.gravity_speed

# class Block(game_sprite):
#     def __init__ (self, x, y, w, h, image):
#         super().__init__(x, y, w, h, image)
#         self.rect = pygame.Rect(x, y, w, h)

bots = []
class Bot(game_sprite):
    def __init__ (self, x, y, w, h, image, speed, finish):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.start_x = x
        self.finish_x = finish
        bots.append(self)
        if x > finish:
            self.direction = 'left'
        else:
            self.direction = 'right'

    def move(self):
        if self.direction == "left":
            self.rect.x -= self.speed
            if self.rect.x <= self.start_x:
                self.direction = "right"
        else:
            self.rect.x += self.speed
            if self.rect.x >= self.finish_x:
                self.direction = "left"

font1 = pygame.font.Font(None, 25)
font2 = pygame.font.Font(None, 25)

# bot1_img = pygame.image.load('monster.png')
# bot1 = Bot(0, 150, 40, 80, bot1_img, 2, 300)

# bot2_img = pygame.image.load('monster2.png')
# bot2 = Bot(0, 150, 40, 80, bot2_img, 2, 50)

YOU_LOSE = font1.render("Ти програв( натисни пробіл щоб почати заново!", True, (bleck))
YOU_WIN = font1.render("Ти виграв)", True, (bleck))
new_game_lb = font2.render("Щоб розпочати нову гру натисніть на лівий <Shift>", True, (blue2))
new_game_lb2 = font2.render("Щоб вийти з гри натисніть <Esc>", True, (blue2))
new_game_lb3 = font2.render("Щоб почати гру заново натисніть <SPACE>", True, (blue2))

player_img = pygame.image.load('hero.png')
player = Player(100, 100, 40, 45, player_img, 2, 3, 25)
block_img = pygame.image.load('block.png')
block2_img = pygame.image.load('block2.png')

GOLD_IMG = pygame.image.load('best.png')
GOLD = game_sprite(0, 1000, 20, 20, GOLD_IMG)
# block = Block()

for stroka in map1:
    for bl in stroka:
        if bl == "1":
            block = game_sprite(x, y, block_size2, block_size, block_img)
            blocks.append(block)
        x += block_size
    x = 0
    y += block_size

# if player.rect.x >= 2800:
#     blocks.clear()
#     for stroka in map2:
#         for bl in stroka:
#             if bl == "1":
#                 block = game_sprite(x, y, block_size, block_size, block2_img)
#                 blocks.append(block)
#                 print(x, y)
#             x += block_size
#         x = 0
#         y += block_size
#     player = Player(2800, 100, 40, 45, player_img, 2, 3, 25)
#     camera = Camera(2800, 0, w_win, h_win, 2)
#     GOLD = game_sprite(5200, 400, 20, 20, GOLD_IMG)

#безкінечний цикл
GOLD_collide = False
game_start = False
game = True
finihs = False

while game:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    if not finihs:

        start_key = pygame.key.get_pressed()
        window.blit(G_Menu, (0, 0))
        window.blit(new_game_lb, (130, 190))
        window.blit(new_game_lb2, (210, 290))
        if start_key[pygame.K_LSHIFT]:
            game_start = True
        if start_key[pygame.K_ESCAPE]:
            game = False

        if game_start == True:
            window.blit(img_load, (0, 0))
            player.gravity()
            camera.move(player)
            player.update()
            # player.jump(pygame.K_SPACE)
            player.move(pygame.K_d, pygame.K_a)
            # player.jump(pygame.K_SPACE)
            GOLD.update()

        if blocks_update == True:
            for block in blocks:
                block.update()
                # if player.collide(block) == True:
                    # player.rect.y -= climb

        if player.rect.x >= 2800:
            x, y = 0, 0
            blocks.clear()
            for stroka in map2:
                for bl in stroka:
                    if bl == "1":
                        block = game_sprite(x, y, block_size, block_size, block2_img)
                        blocks.append(block)
                        print(x, y)
                    x += block_size
                x = 0
                y += block_size
            player = Player(50, 50, 40, 45, player_img, 2, 3, 25)
            camera = Camera(0, 0, w_win, h_win, 2)
            GOLD = game_sprite(2200, 400, 20, 20, GOLD_IMG)
            # climb == 0

        if player.collide(GOLD) == True:
            window.blit(YOU_WIN, (350, 250))
            window.blit(new_game_lb3, (180, 300))
            pygame.mixer.music.play(loops=1, start=0.0, fade_ms=0)
            GOLD_collide = True
            finihs = True

    # доделай колизию

        if player.rect.y >= 400:
            window.fill(red)
            window.blit(YOU_LOSE, (165, 150))
            finihs = True

            # for bot in bots:
            #     bot.update()
            #     bot.move()
            #     if player.collide(bot) == True:
            #         window.fill(red)
            #         window.blit(YOU_LOSE, (165, 150))
            #         finihs = True

        if blocks_update == True:
            for block in blocks:
                block.update()
                if player.collide(block) == True:
                    player.rect.y -= 3

        # if player.collide(GOLD) == True:
        #     window.blit(YOU_WIN, (165, 150))
        #     window.blit(new_game_lb, (180, 300))
        #     pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
        #     finihs = True

#оброби подію «клік за кнопкою "Закрити вікно"»
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and GOLD_collide == True:
            blocks.clear()
            x, y = 0, 0
            for stroka in map1:
                for bl in stroka:
                    if bl == "1":
                        block = game_sprite(x, y, block_size2, block_size, block_img)
                        blocks.append(block)
                    x += block_size
                x = 0
                y += block_size
            player = Player(50, 50, 40, 45, player_img, 2, 3, 25)
            camera = Camera(0, 0, w_win, h_win, 2)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.jump()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and finihs:
            finihs = False
            player = Player(50, 50, 40, 45, player_img, 2, 3, 25)
            camera = Camera(0, 0, w_win, h_win, 2)

    pygame.display.update()
    clock.tick(FPS)
