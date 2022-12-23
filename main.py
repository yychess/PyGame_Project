import pygame
import os
import sys


FPS = 30
v = -30
pygame.init()
size = width, height = 800, 700
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        terminate()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    intro_text = ["Правила:",
                  "цель игры - пройти как можно дальше, не столкнувшись с препятствием",
                  "управление происходит за счёт клавиши пробел",
                  "преждевременный выход - esc", "",
                  "нажмите Enter для старта"]

    fon = pygame.transform.scale(load_image('вертолет.jpg'), size)
    screen.blit(fon, (0, 0))

    font = pygame.font.Font(None, 30)
    text_coord = 20
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
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
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
        pygame.display.flip()


def sprite_helicopter():
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("4.jpg", -1)
    sprite.image = pygame.transform.scale(sprite.image, (200, 100))
    sprite.rect = sprite.image.get_rect()
    sprite.rect.x = 100
    sprite.rect.y = height // 2 - 100
    return sprite


def game_cycle():
    sprite = sprite_helicopter()
    screen2 = pygame.Surface(size)
    fon = pygame.transform.scale(load_image('небо'), size)
    screen2.blit(fon, (0, 0))
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.time.set_timer(MYEVENTTYPE, 0)
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                sprite.rect = sprite.rect.move(0, v)
            if event.type == MYEVENTTYPE:
                sprite.rect = sprite.rect.move(0, 1)
            screen2.blit(sprite.image, (sprite.rect.x, sprite.rect.y))
            screen.blit(screen2, (0, 0))
            screen2.blit(fon, (0, 0))

            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Вертолёт')

    start_screen()
    game_cycle()


