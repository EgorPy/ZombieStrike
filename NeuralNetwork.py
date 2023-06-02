import pygame
import math
import random


pygame.init()


class MyObject:
    def __init__(self, size, position, color, angle=random.randint(-180, 180)):
        self.size = size
        self.position = position
        self.angle = angle
        self.needed_angle = angle
        self.color = color
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)
        self.surface.set_colorkey((0, 0, 0))
        self.direction = True
        self.counter = 0

    def move(self):
        DISPLAY.blit(self.surface, self.position)
        FOV = 360
        mousePos = pygame.mouse.get_pos()
        pygame.draw.rect(DISPLAY, (255, 0, 0), pygame.Rect(mousePos, [100, 100]))
        for i in range(FOV):
            mousePos = pygame.mouse.get_pos()
            if in_screen([self.position[0] + self.size[0] // 2 + math.sin(deg_to_rad(self.angle)) * 100,
                          self.position[1] + self.size[1] // 2 + math.cos(deg_to_rad(self.angle)) * 100], [100, 100],
                         WIDTH, HEIGHT) and not touched(
                self.position[0] + self.size[0] // 2 + math.sin(deg_to_rad(self.angle)) * 100, 100, mousePos[0], 100,
                self.position[1] + self.size[1] // 2 + math.cos(deg_to_rad(self.angle)) * 100, 100, mousePos[1], 100):
                pygame.draw.line(DISPLAY, (255, 0, 0),
                                 [self.position[0] + self.size[0] // 2, self.position[1] + self.size[1] // 2],
                                 [self.position[0] + self.size[0] // 2 + math.sin(deg_to_rad(self.angle)) * 100,
                                  self.position[1] + self.size[1] // 2 + math.cos(deg_to_rad(self.angle)) * 100])
                # if self.angle == 90 or self.angle == -90:
                #     self.angle = random.randint(-180, 180)
                if self.counter % 6000 == 0:
                    self.needed_angle = random.randint(-180, 180)
                self.position[0] += math.sin(deg_to_rad(self.angle)) / FOV * 10
                self.position[1] += math.cos(deg_to_rad(self.angle)) / FOV * 10
            else:
                if self.direction:
                    self.angle -= 1
                else:
                    self.angle += 1
                if self.angle > FOV / 2:
                    self.direction = False
                if self.angle < -FOV / 2:
                    self.direction = True
            self.counter += 1
            if self.counter > 10000:
                self.counter = 0


def deg_to_rad(degree):
    return degree * math.pi / 180


def rad_to_deg(radian):
    return radian * 180 / math.pi


def in_screen(position, size, width_of_screen, height_of_screen):
    if 0 < position[0] < (width_of_screen - size[0]):
        if 0 < position[1] < (height_of_screen - size[1]):
            return True
        else:
            return False
    else:
        return False


def touched(x1, weight1, x2, weight2, y1, height1, y2, height2):
    if (x1 <= x2 and x2 <= (x1 + weight1)
        and y1 <= y2 and y2 <= (y1 + height1)) \
            or (x1 <= (x2 + weight2) and (x1 + weight1) >= x2
                and y1 <= (y2 + height2) and (y1 + height1) >= y2):
        return True
    else:
        return False


DISPLAY = pygame.display.set_mode((1000, 800))
pygame.display.set_caption('Neural Network by Egor')
WIDTH, HEIGHT = DISPLAY.get_size()
CLOCK = pygame.time.Clock()
FPS = 60
RUN = True
o = MyObject([100, 100], [200, 100], (0, 0, 0))
pygame.draw.circle(o.surface, (0, 0, 255), [50, 50], 50)

while RUN:
    DISPLAY.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    o.move()

    pygame.display.update()
    CLOCK.tick(FPS)
