import pygame
import random
import os
import sys


pygame.init()
FPS = 30
v_up = -60  # скорость поднятия наверх (по нажатию пробела)
v_down = 20  # скорость снижения вниз
level = 2  # начальный уровень скорости
k_boards = 0  # количество пройденных припятствий
clash = False  # флаг окончания игры
size = width, height = 1000, 700  # размеры окна
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
record = 0  # рекорд


# выход из программы
def terminate():
    pygame.quit()
    sys.exit()


# загрузка изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        terminate()
    image = pygame.image.load(fullname)
    # удаление фона изображения
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# начальный экран
def start_screen():
    intro_text = ["Правила:",
                  "цель игры - пройти как можно дальше, не столкнувшись с препятствием",
                  "управление происходит за счёт клавиши пробел",
                  "преждевременный выход - esc", "",
                  "нажмите Enter для старта"]

    # установка фона
    fon = pygame.transform.scale(load_image('город.webp'), size)
    screen.blit(fon, (0, 0))

    # обработка текста
    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # выход из программы по нажатию на крестик или escape
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # переход от начального экрана к игре
                return
        pygame.display.flip()


# класс фоновых облачков
class Clouds(pygame.sprite.Sprite):
    image = load_image("cloud.png")
    image = pygame.transform.scale(image, (200, 120))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Clouds.image
        self.rect = self.image.get_rect()
        # рандомное расположение облаков на экране
        self.rect.x = random.randrange(width)
        self.rect.y = random.randrange(height)

    # движение облаков
    def update(self):
        if self.rect.x > -200:
            self.rect.x -= level - 1
        else:
            # если заходят за экран, то располагаются рандомно на другом конце экрана
            self.rect.x = width
            self.rect.y = random.randrange(height)


# создание анимированного спрайта вертолета
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.image_number = 0
        self.image = self.frames[self.image_number]
        self.rect = self.rect.move(100, 100)

    # разрез изображения на отдельные картинки для анимации
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    # переход на следующее изобраджение
    def update(self):
        self.image_number = (self.image_number + 1) % len(self.frames)
        self.image = self.frames[self.image_number]


# изменение флага произошедшего взрыва
def boom():
    global clash
    clash = True


# родительский класс стенок
class Boards(pygame.sprite.Sprite):
    image = load_image("стена.png")
    image = pygame.transform.scale(image, (100, height))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = BoardsDown.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = width + x * ((width + 100) / 2)
        self.rect.y = y


# класс нижних стенок
class BoardsDown(Boards):
    def __init__(self, x, y, *group):
        super().__init__(x, y, *group)

    # движение стенок, счётчик и ускорение
    def update(self, y, sprite):
        global k_boards, level
        if self.rect.x > -150:
            self.rect.x -= level
        else:
            # после ухода за экран, переход на другую сторону
            self.rect.x = width
            self.rect.y = y
            k_boards += 1  # добовление к счётчику прохождения стенок
            # каждые 5 пройденных стенок - ускорение
            if k_boards % 5 == 0:
                level += 1

        #  проверка на столкновение
        if pygame.sprite.collide_mask(self, sprite):
            boom()


# класс верхних стенок
class BoardsUp(Boards):
    def __init__(self, x, y, *group):
        super().__init__(x, y, *group)

    # движение стенок
    def update(self, y, sprite):
        if self.rect.x > -150:
            self.rect.x -= level
        else:
            # после ухода за экран, переход на другую сторону
            self.rect.x = width
            self.rect.y = y

        if pygame.sprite.collide_mask(self, sprite):
            boom()


# главный игровой класс
def game_cycle():
    global v_down

    # создание спрайта вертолёта
    helicopter_image = load_image("helicopter.png")
    helicopter_image = pygame.transform.scale(helicopter_image, (200, 400))
    helicopter = AnimatedSprite(helicopter_image, 1, 4)

    font = pygame.font.Font(None, 50)  # для показа количества пройденных стенок

    # второй экран
    screen2 = pygame.Surface(size)
    fon = pygame.transform.scale(load_image('небо'), size)
    screen2.blit(fon, (0, 0))

    # таймер для обновления
    time = pygame.USEREVENT + 1
    pygame.time.set_timer(time, 10)

    # создание спрайтов облачков
    clouds = pygame.sprite.Group()
    for _ in range(5):
        Clouds(clouds)

    # создание спрайтов стенок
    boards_up, boards_down = pygame.sprite.Group(), pygame.sprite.Group()
    for i in range(2):
        y = random.randrange(-1 * height, -200)
        BoardsUp(i, y, boards_up)
        BoardsDown(i, y + 250 + height, boards_down)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # выход из программы по нажатию на крестик или escape
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # поднятие вертолёта по пробелу
                helicopter.rect = helicopter.rect.move(0, v_up)
                v_down = 20

            if event.type == time:
                # проигрыш (врезание в стенки, выход за экран) - взрыв
                if clash or -100 > helicopter.rect.y or helicopter.rect.y > height:
                    boom_image = pygame.transform.scale(load_image('взрыв.png'), (400, 400))
                    screen.blit(boom_image, (helicopter.rect.x - 100, helicopter.rect.y - 150))
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    return

                helicopter.rect = helicopter.rect.move(0, v_down / 20)  # снижение вертолета
                v_down += 1  # для снижения по параболе

                # обновление вертолета и облаков
                clouds.update()
                helicopter.update()

                # обновление стенок
                y = random.randrange(-1 * height, -200)
                boards_up.update(y, helicopter)
                boards_down.update(y + 250 + height, helicopter)

            # отрисовка облаков, вертолёта и стенок
            clouds.draw(screen2)
            screen2.blit(helicopter.image, helicopter.rect)
            boards_up.draw(screen2)
            boards_down.draw(screen2)

            # добавление счётчика на экран
            text = font.render(str(k_boards), True, (0, 255, 0))
            screen2.blit(text, (10, 10))

            # смена экранок
            screen.blit(screen2, (0, 0))
            screen2.blit(fon, (0, 0))
            pygame.display.flip()


# экран завершения
def finish_screen():
    global record, k_boards

    # проверка на уже сохранённый рекорд
    try:
        file = open("data/record.txt", "r")
        record = int(file.read())
        file.close()
    except FileNotFoundError:
        record = 0

    # обнавление рекрда при необходимости
    if record < k_boards:
        file = open("data/record.txt", "w")
        record = str(k_boards)
        file.write(record)

    # фон
    fon = pygame.transform.scale(load_image('город2.webp'), size)
    screen.blit(fon, (0, 0))

    # обработка текста с указанием счёта и рекорда
    text = ["Конец", f"Счёт: {k_boards}", f"Рекорд: {record}"]

    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # выход из программы по нажатию на крестик или escape
                terminate()

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Helicopter')

    start_screen()
    game_cycle()
    finish_screen()
