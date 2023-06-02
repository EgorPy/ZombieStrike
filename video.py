import pygame
from moviepy.editor import *

screen = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
pygame.display.set_caption('Video')

clip = (VideoFileClip('2021-07-04 15-49-33.mkv').fx( vfx.resize, width=1500) # resize (keep aspect ratio)
        .fx( vfx.speedx, 30)) # double the speed
        # .fx( vfx.colorx, 0.5)) # darken the picture)
a = False
while True:
    if not a:
        clip.preview()
        a = True
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
    screen.fill((255, 0, 0))
    pygame.display.update()

pygame.quit()
