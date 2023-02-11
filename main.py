import random

import nltk
import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
LINE_WIDTH = 4
LINE_COLOR = (0, 0, 0)
HOOK_WIDTH = 54
HOOK_HEIGHT = 100
HOOK_RING_OFFSET_X = 13
HOOK_OFFSET_Y = 60
HOOK_SIZE = 40
FONT_SIZE = 32
TRASH_WIDTH = 213
TRASH_HEIGHT = 321

pygame.init()
# win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
# pygame.mouse.set_visible(False)
font = pygame.font.SysFont("Arial", FONT_SIZE, True)

bg = pygame.image.load("assets/background.webp")
hook = pygame.image.load("assets/hook_100h.png").convert_alpha()
trash = pygame.image.load("assets/trash.png").convert_alpha()


def draw_hook_and_line(win, x, y):
    win.blit(hook, (x, y))
    ring_x = x + (HOOK_WIDTH // 2) + HOOK_RING_OFFSET_X
    pygame.draw.line(win, LINE_COLOR, (ring_x, y), (ring_x, 0), LINE_WIDTH)


def draw_hook_bounding_box(win, x, y):
    return pygame.draw.rect(
        win,
        (0, 0, 0),
        [x, y + HOOK_OFFSET_Y, HOOK_SIZE, HOOK_SIZE],
        width=2,
    )


def draw_bounding_rect(win, msg_rect):
    padding_x = 10
    padding_y = 10
    bounding_rect = pygame.draw.rect(
        win,
        (0, 0, 0),
        [
            msg_rect.left - padding_x // 2,
            msg_rect.top - padding_y // 2,
            msg_rect.width + padding_x,
            msg_rect.height + padding_y,
        ],
        width=2,
    )
    return bounding_rect


def validate_rect(rect):
    return (
        (rect.top >= 0)
        and (rect.bottom <= SCREEN_HEIGHT)
        and (rect.left >= 0)
        and (rect.right <= SCREEN_WIDTH)
    )


lines = nltk.sent_tokenize(
    """\
Thanks for asking. There’s a “forgot password” link on the login screen in the app. (see image beside when login).
In addition to that, there are a couple other options on the web (but not in the app).
Please Reset Your Password For your security, we are strengthening our password requirements and as a result, your existing password has been disabled."""
)

messages = []

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(60)
    win.blit(bg, (0, 0))
    win.blit(trash, (SCREEN_WIDTH - TRASH_WIDTH, SCREEN_HEIGHT - TRASH_HEIGHT))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    draw_hook_and_line(win, mouse_x, mouse_y)
    hook_bounding_box = draw_hook_bounding_box(win, mouse_x, mouse_y)

    for msg in messages:
        if hook_bounding_box.colliderect(msg[2]):
            messages.remove(msg)

    if len(messages) == 0:
        for line in lines:
            msg = font.render(line, True, (0, 0, 0))

            valid_pos = False
            while not valid_pos:
                msg_pos = (
                    random.randint(0, SCREEN_WIDTH),
                    random.randint(0, SCREEN_HEIGHT),
                )
                msg_rect = win.blit(msg, msg_pos)
                bounding_rect = draw_bounding_rect(win, msg_rect)
                valid_pos = validate_rect(bounding_rect)

            messages.append([msg, msg_rect, bounding_rect, "right", "down"])
    else:
        dx = 2
        dy = 2
        for i, msg in enumerate(messages):
            x_dir = msg[-2]
            y_dir = msg[-1]
            if x_dir == "right" and msg[1].right + dx >= SCREEN_WIDTH:
                msg[-2] = "left"
            elif x_dir == "left" and msg[1].left - dx <= 0:
                msg[-2] = "right"
            elif y_dir == "down" and msg[1].bottom + dy >= SCREEN_HEIGHT:
                msg[-1] = "up"
            elif y_dir == "up" and msg[1].top - dy <= 0:
                msg[-1] = "down"

            new_pos = (
                msg[1].left + (dx if msg[-2] == "right" else -dx),
                msg[1].top + (dy if msg[-1] == "down" else -dy),
            )
            msg[1] = win.blit(msg[0], new_pos)
            msg[2] = draw_bounding_rect(win, msg[1])

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False
