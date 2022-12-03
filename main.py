import numpy as np
import pygame
import random
import os

#for fps
FPS = 60
sr_znach = [0, 0]


# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def load_image(name, x, y, colorkey=None):
    fullname = os.path.join('images', name)
    # если файл не существует, то выходим
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print(f"Файл с изображением '{fullname}' не найден")
        return SystemExit(message)
    if colorkey is None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return pygame.transform.scale(image, (x, y))


def fps(screen, clock, WIDTH):
    front = pygame.font.SysFont('Arial', 30, bold=True)
    display_fps = str(int(clock.get_fps()))
    sr_znach[0] += int(display_fps)
    sr_znach[1] += 1
    render = front.render(display_fps, 0, (255, 0, 0))
    screen.blit(render, (WIDTH - 60, 30))


class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, pos_x, pos_y):
        super().__init__(somalet_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        '''self.sostoniye = ''
        self.tim_down = 1
        self.tim_up = 1
        self.speeding_up = 1
        self.speeding_down = 2'''
        self.speed = 5
        # self.pozitsiya = self.rect.y
        # self.mask_bird = pygame.mask.from_surface(self.image2)
        self.fly_or_not_fly = True

    def update(self, collision):
        for i in collision:
            if pygame.sprite.collide_mask(self, i):
                self.fly_or_not_fly = False

        '''if self.fly_or_not_fly:
            self.movement()'''

    def movement(self):
        if self.fly_or_not_fly:
            keys = pygame.key.get_pressed()
            speed = self.speed
            if keys[pygame.K_w]:
                self.rect.y -= speed
            if keys[pygame.K_a]:
                self.rect.x -= speed
            if keys[pygame.K_d]:
                self.rect.x += speed
            if keys[pygame.K_s]:
                self.rect.y += speed


class Radar(pygame.sprite.Sprite):
    def __init__(self, radarich, pos_x, pos_y):
        super().__init__(somalet_sprites)
        self.image = radarich
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        pass


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, obstac, pos_x, pos_y):
        super().__init__(obstac_sprites)
        self.image = obstac
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.offset_for_obs_x = main_somal_x
        self.offset_for_obs_y = main_somal_y

    def update(self, offset_x, offset_y):   #offset = смещение
        x_offset = self.offset_for_obs_x - offset_x
        y_offset = self.offset_for_obs_y - offset_y

        #присваиваеи к прошлому смещению будущее смещение
        self.offset_for_obs_x = offset_x
        self.offset_for_obs_y = offset_y

        self.rect.x += x_offset
        self.rect.y += y_offset

        self.rect.x += -1


def draw_fon():
    global act_x
    screen.fill(BLACK)
    x = fon_x - act_x
    if act_x < fon_x:
        screen.blit(fon, (-act_x, 0), (0, 0, fon_x, fon_y))
        screen.blit(fon, (x, 0), (0, 0, act_x, fon_y))
    else:
        act_x = 0
        screen.blit(fon, (x, 0), (0, 0, fon_x, fon_y))


def draw_obs():
    kol_obs = []
    for i in obstac_sprites:
        W_H = i.rect
        kol_obs.append([W_H.x / KOF_X, W_H.y / KOF_Y])
    for i in range(KOL_OBS):
        x = kol_obs[i][0]
        y = kol_obs[i][1]
        if (x <= 0 or y >= 0) and x < kof_1_x and y < kof_2_y:
            pygame.draw.circle(screen, WHITE, (x, HEIGHT - kof_2_y + y), 5)


# Создаем игру и окно
pygame.init()
pygame.mixer.init()

#окно
infoObject = pygame.display.Info()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#fps
clock = pygame.time.Clock()

#name window
pygame.display.set_caption("OVD")

#sprite
somalet_sprites = pygame.sprite.Group()
obstac_sprites = pygame.sprite.Group()

#main samolet
main_obj = 'somalet.png'
main_somal_x = 300
main_somal_y = 300
player = Player(load_image(main_obj, 150, 75), main_somal_x, main_somal_y)

# препятствия
obst = 'another_somalet.png'
#obstacles = []

KOL_OBS = 6
for i in range(KOL_OBS):
    a = random.randint(50, 1000)
    b = random.randint(500, 1300)
    obstac_sprites.add(Obstacles(load_image(obst, 200, 100), b, a))


#радар
radar = 'radar.png'
#radar_blit = load_image(radar, 200, 200)
kof_1_x = 300
kof_2_y = 200
KOF_X = WIDTH / kof_1_x
KOF_Y = HEIGHT / kof_2_y
obj_rad = Radar(load_image(radar, kof_1_x, kof_2_y), 0, HEIGHT - 200)
#all_sprites.add(player)

#for fon
fon = load_image('fon_sky.jpg', WIDTH, HEIGHT)
fon_x = WIDTH
fon_y = HEIGHT
act_x = 0

# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости

    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Обновление
    if player.fly_or_not_fly:
        player.update(obstac_sprites) #!!!!!!!!!!!
        #проверяем движение
        player.movement()
        obstac_sprites.update(player.rect.x, player.rect.y)
        #obstac_sprites.update()
    # Рендеринг
    draw_fon()
    act_x += 5
    obstac_sprites.draw(screen)
    somalet_sprites.draw(screen)
    #Рисуем припятствия
    draw_obs()
    #Рисуем fps
    fps(screen, clock, WIDTH)
    #screen.blit(radar_blit, (0, HEIGHT - 200))

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
    clock.tick(60)
print(sr_znach)
print(sr_znach[0] / sr_znach[1])
pygame.quit()

