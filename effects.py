import pygame
import math
import random


class Effect:
    __count = 0
    effects = []

    def __init__(self, position=[300, 500], color=(255, 0, 0), radius=20):
        self.radius = radius
        self.position = position
        self.counter = 0
        self.color = color
        Effect.effects.append(self)
        Effect.__count += 1

    @staticmethod
    def get_count():
        return Effect.__count

    @staticmethod
    def update(effect):
        for self in Effect.effects:
            if effect == 'circle':
                self.counter += 1
                if self.counter > 100:
                    Effect.__count -= 1
                    Effect.effects.remove(self)
                    del self
                    return None
                self.radius += random.randint(-1, 6)
                self.position[1] -= 5
                pygame.draw.circle(DISPLAY, self.color, self.position, self.radius)


def effect():
    global EFFECTS_CREATED
    if not EFFECTS_CREATED:
        e = Effect(color=(100, 100, 100))
        a = Effect(position=[300, 450], color=(150, 150, 150))
        EFFECTS_CREATED = True


if __name__ == '__main__':
    DISPLAY = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
    WIDTH, HEIGHT = DISPLAY.get_size()
    RUN = True
    FPS = 60
    CLOCK = pygame.time.Clock()
    EFFECTS_CREATED = False
    DISPLAY.fill((255, 255, 255))


    def check_events():
        global RUN
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False


    while RUN:
        # DISPLAY.fill((255, 255, 255))

        check_events()

        effect()
        Effect.update('circle')
        print(Effect.get_count())

        pygame.display.update()
        CLOCK.tick(FPS)
