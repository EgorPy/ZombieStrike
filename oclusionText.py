import pygame
from maps import *

DISPLAY = pygame.display.set_mode((600, 600))
WIDTH, HEIGHT = DISPLAY.get_size()

FPS = 60
RUN = True
CLOCK = pygame.time.Clock()

pos = [300, 300]
p = pygame.Surface((100, 100))
p.fill((0, 0, 255))

map_size = 120

while RUN:
    DISPLAY.fill((255, 255, 255))

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            RUN = False

    DISPLAY.blit(p, [300, 300])
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        pos[1] -= 10
    if keys[pygame.K_s]:
        pos[1] += 10
    if keys[pygame.K_a]:
        pos[0] -= 10
    if keys[pygame.K_d]:
        pos[0] += 10

    print(pos)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size, 250 + pos[1] % map_size], [map_size, map_size]), 1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size - map_size, 250 + pos[1] % map_size],
                                 [map_size, map_size]), 1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size - map_size, 250 + pos[1] % map_size - map_size],
                                 [map_size, map_size]), 1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size, 250 + pos[1] % map_size - map_size], [map_size, map_size]),
                     1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size, 250 + pos[1] % map_size + map_size], [map_size, map_size]),
                     1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size - map_size, 250 + pos[1] % map_size + map_size],
                                 [map_size, map_size]), 1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size + map_size, 250 + pos[1] % map_size - map_size],
                                 [map_size, map_size]), 1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size + map_size, 250 + pos[1] % map_size], [map_size, map_size]),
                     1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size + map_size, 250 + pos[1] % map_size + map_size],
                                 [map_size, map_size]), 1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size - map_size * 2, 250 + pos[1] % map_size + map_size],
                                 [map_size, map_size]), 1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size - map_size * 2, 250 + pos[1] % map_size],
                                 [map_size, map_size]), 1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size - map_size * 2, 250 + pos[1] % map_size - map_size],
                                 [map_size, map_size]), 1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size - map_size * 2, 250 + pos[1] % map_size - map_size * 2],
                                 [map_size, map_size]), 1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size - map_size, 250 + pos[1] % map_size - map_size * 2],
                                 [map_size, map_size]), 1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size, 250 + pos[1] % map_size - map_size * 2],
                                 [map_size, map_size]), 1)
    pygame.draw.rect(DISPLAY, (255, 0, 0),
                     pygame.Rect([250 + pos[0] % map_size + map_size, 250 + pos[1] % map_size - map_size * 2],
                                 [map_size, map_size]), 1)

    pygame.display.update()
    CLOCK.tick(FPS)
