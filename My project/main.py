import pygame
from map import *
from time import time

pygame.init()

#висота та ширина
w_win = 700
h_win = 500
level_width = 1400

#кольори
blue = (125, 249, 255)
green = (62, 218, 148)
red = (255, 0, 0)
bleck = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 228, 107)

#створи вікно гри
window = pygame.display.set_mode((w_win, h_win))

FPS = 55
clock = pygame.time.Clock()

gravity_speed = 3
blocks = []
blocks2 = []
block_size = 20
y = 0
x = 0

# # изночяльное время
# start_time = time()

# #задай фон сцени
img_load = pygame.image.load('background.jpg')
img_load = pygame.transform.scale(img_load, (w_win, h_win))

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

class Camera:
    def __init__(self, x, y, w, h, speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
    def move(self, player):
        if self.rect.right < level_width:
            if player.rect.x > self.rect.x + int(0.7*self.rect.w):
                self.rect.x += self.speed

camera = Camera(0, 0, w_win, h_win, 5)

#клас гравців
class Player(game_sprite):
    def __init__ (self, x, y, w, h, image, speed, gravity_speed, jump_speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        self.gravity_speed = gravity_speed
        self.jump_speed = jump_speed
    def move(self, right, left):
        move_ = pygame.key.get_pressed()  
        if move_[right]:
            # if self.rect.x <= w_win - self.rect.width:
            # self.rect.x += self.speed
            self.rect.x += self.speed
        if move_[left]:
            # if self.rect.x >= 0:
            # self.rect.x -= self.speed
            self.rect.x -= self.speed

    def jump(self, up):
        jump_ = pygame.key.get_pressed()
        if jump_[up]:
            self.rect.y -= self.jump_speed

    def gravity(self):
        self.rect.y += self.gravity_speed

    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            return True
        else:
            return False

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

font1 = pygame.font.Font(None, 50)
font2 = pygame.font.Font(None, 25)
bot1_img = pygame.image.load('monster.png')
bot1 = Bot(30, 440, 40, 40, bot1_img, 2, 300)
YOU_LOSE = font1.render("Ти програв(", True, (bleck))
YOU_WIN = font1.render("Ти виграв)", True, (bleck))
# new_game_lb = font2.render("Щоб розпочати нову гру натисніть <пробіл>", True, (bleck))
player_img = pygame.image.load('hero.png')
player = Player(125, 60, 40, 45, player_img, 2, 3, 25)
block_img = pygame.image.load('block.png')
block2_img = pygame.image.load('block2.png')
# block = Block()

for stroka in map1:
    for bl in stroka:
        if bl == "1":
            block = game_sprite(x, y, block_size, block_size, block_img)
            blocks.append(block)
        x += block_size
    x = 0
    y += block_size

for stroka in map1:
    for bl in stroka:
        if bl == "2":
            block2 = game_sprite(x, y, block_size, block_size, block2_img)
            blocks2.append(block2)
        x += block_size
    x = 0
    y += block_size

#безкінечний цикл
game = True
finihs = False

while game:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    if not finihs:
        window.blit(img_load, (0, 0))
        player.gravity()
        camera.move(player)
        player.update()
        player.move(pygame.K_d, pygame.K_a)
        # player.jump(pygame.K_SPACE)

# доделай колизию

        for bot in bots:
            bot.update()
            bot.move()
            if player.collide(bot) == True:
                window.fill(red)
                window.blit(YOU_LOSE, (165, 250))
                finihs = True

        for block in blocks:
            block.update()
            if player.collide(block) == True:
                player.rect.y -=3
                player.jump(pygame.K_SPACE)



        # for block2 in blocks2:
        #     block2.update()
        #     if player.collide(block2) == True:
        #         player.rect.y -= 3

#оброби подію «клік за кнопкою "Закрити вікно"»
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    pygame.display.update()
    clock.tick(FPS)
