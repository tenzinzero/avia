import pygame
import random
import os

WIDTH = 1300
HEIGHT = 650
FPS = 60

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
    render = front.render(display_fps, 0, (255, 0, 0))
    screen.blit(render, (WIDTH - 60, 30))


class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.sostoniye = ''
        self.tim_down = 1
        self.tim_up = 1
        self.speeding_up = 1
        self.speeding_down = 2
        # self.pozitsiya = self.rect.y
        # self.mask_bird = pygame.mask.from_surface(self.image2)
        self.fly_or_not_fly = True

    def update(self, collision):
        if pygame.sprite.collide_mask(self, collision):
            self.fly_or_not_fly = False
        if self.fly_or_not_fly:
            self.movement()


    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= 2
        if keys[pygame.K_a]:
            self.rect.x -= 2
        if keys[pygame.K_d]:
            self.rect.x += 2
        if keys[pygame.K_s]:
            self.rect.y += 2


class Radar(pygame.sprite.Sprite):
    def __init__(self, radarich, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = radarich
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        pass


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, obstac, pos_x, pos_y):
        super().__init__(obstac_sprites)
        self.image = obstac
        self.rect = self.image.get_rect().move(pos_x, pos_y)

    def update(self):
        self.rect.x += -1




# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#fps
time = pygame.time.Clock()
pygame.display.set_caption("OVD")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
obstac_sprites = pygame.sprite.Group()
#main samolet
main_obj = 'somalet.png'
player = Player(load_image(main_obj, 150, 75), 300, 300)
# препятствия
obst = 'another_somalet.png'
obstacles = Obstacles(load_image(obst, 200, 100), WIDTH - 300, HEIGHT - 600)

#радар
radar = 'radar.png'
#radar_blit = load_image(radar, 200, 200)
obj_rad = Radar(load_image(radar, 200, 200), 0, HEIGHT - 200)
#all_sprites.add(player)

fon = load_image('fon_sky.jpg', WIDTH, HEIGHT)
main_obj = 'somalet.png'



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
    #player.movement()
    if player.fly_or_not_fly:
        player.update(obstacles) #!!!!!!!!!!!
        obstac_sprites.update()
    # Рендеринг
    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)
    obstac_sprites.draw(screen)
    fps(screen, time, WIDTH)
    #screen.blit(radar_blit, (0, HEIGHT - 200))

    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

