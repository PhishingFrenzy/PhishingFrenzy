import pygame
import random
    
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
LINE_WIDTH = 4
LINE_COLOR = (0, 0, 0)
HOOK_WIDTH = 54
HOOK_HEIGHT = 100
HOOK_RING_OFFSET_X = 13
FONT_SIZE = 24

pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.mouse.set_visible(False)
font = pygame.font.SysFont("Arial", FONT_SIZE, True)

bg = pygame.image.load("assets/background.webp")
hook = pygame.image.load("assets/hook_100h.png").convert_alpha()


def draw_hook_and_line(win, x, y):
    win.blit(hook, (x, y))
    ring_x = x + (HOOK_WIDTH // 2) + HOOK_RING_OFFSET_X
    pygame.draw.line(win, LINE_COLOR, (ring_x, y), (ring_x, 0), LINE_WIDTH)

def draw_bounding_rect(win, msg_rect):
    padding_x = 10
    padding_y = 10
    bounding_rect = pygame.draw.rect(
        win,
        (0, 0, 0), 
        [msg_rect.left - padding_x // 2, msg_rect.top - padding_y // 2, msg_rect.width + padding_x, msg_rect.height + padding_y],
        width=2
    )
    return bounding_rect

def validate_rect(rect):
    return (rect.top >= 0) and (rect.bottom <= SCREEN_HEIGHT) and (rect.left >= 0) and (rect.right <= SCREEN_WIDTH)


clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    win.blit(bg, (0, 0))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    draw_hook_and_line(win, mouse_x, mouse_y)

    msg = font.render("This is sentence 1", True, (0, 0, 0))
    msg_pos = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    msg_rect = win.blit(msg, msg_pos)
    draw_bounding_rect(win, msg_rect)

    msg = font.render("This is sentence 2", True, (0, 0, 0))
    msg_pos = (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4)
    msg_rect = win.blit(msg, msg_pos)
    draw_bounding_rect(win, msg_rect)

    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

