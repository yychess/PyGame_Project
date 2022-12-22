import pygame, os
import sys


FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_screen():
    intro_text = ["Правила:",
                  "цель игры - пройти как можно дальше, не столкнувшись с препятствием",
                  "управление происходит за счёт клавиши пробел",
                  "преждевременный выход - esc", "",
                  "нажмите Enter для старта"]

    fon = pygame.transform.scale(load_image('вертолет.jpg'), (800, 700))
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


pygame.init()
pygame.display.set_caption('Вертолёт')
screen = pygame.display.set_mode((800, 700))
start_screen()
