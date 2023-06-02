import pygame
import math
import textures
from maps import *

pygame.init()


class Button:
    def __init__(self, position=None, font_name='Courier', font_size=40, bold=True, smooth=True, color=(50, 150, 5),
                 text='Button', background=None):
        if position is None:
            self.position = [0, 0]
        self.font_name = font_name
        self.font_size = font_size
        self.bold = bold
        self.smooth = smooth
        self.color = color
        self.background = background
        self.button_text = text
        self.font = pygame.font.SysFont(self.font_name, self.font_size, self.bold)
        self.surface = self.font.render(self.button_text, self.smooth, self.color, self.background)
        self.size = self.surface.get_size()
        self.clicked = False

    def update(self):
        self.__init__(self.position, self.font_name, self.font_size, self.bold, self.smooth, self.color,
                      self.button_text)

    def click(self):  # нажата ли кнопка?
        mouse = pygame.mouse.get_pressed(3)
        mousePos = pygame.mouse.get_pos()
        if touched(self.position[0], self.size[0], mousePos[0], 1,
                   self.position[1], self.size[1], mousePos[1], 1):
            if mouse[0]:
                self.clicked = True
        else:
            self.clicked = False

    def create_pos(self, y):
        self.position = [(WIDTH - self.size[0]) / 2, y]


class BoolWidget:
    def __init__(self, bool_types=['yes', 'no'], position=None, font_name='Courier', font_size=40, bold=True,
                 smooth=True, color=(50, 150, 5), background=None, boolean_n=False):
        if position is None:
            self.position = [0, 0]
        self.font_name = font_name
        self.font_size = font_size
        self.bold = bold
        self.smooth = smooth
        self.color = color
        self.background = background
        self.boolean = boolean_n
        self.bool_types = bool_types
        self.button_text = bool_types[0 if self.boolean else 1]
        self.font = pygame.font.SysFont(self.font_name, self.font_size, self.bold)
        self.surface = self.font.render(self.button_text, self.smooth, self.color, self.background)
        self.size = self.surface.get_size()
        self.clicked = False
        self.d = False

    def update_text(self, qwerty):
        self.button_text = 'yes' if qwerty else 'no'
        self.font = pygame.font.SysFont(self.font_name, self.font_size, self.bold)
        self.surface = self.font.render(self.button_text, self.smooth, self.color, self.background)

    def click(self):  # нажата ли кнопка?
        mouse = pygame.mouse.get_pressed(3)
        mousePos = pygame.mouse.get_pos()
        if touched(self.position[0], self.size[0], mousePos[0], 1,
                   self.position[1], self.size[1], mousePos[1], 1):
            if mouse[0]:
                self.clicked = True
                self.d = not self.d
                pygame.time.delay(500)
            else:
                self.clicked = False
        else:
            self.clicked = False
        self.update_text(self.d)

    def create_pos(self, y):
        self.position = [(WIDTH - self.size[0]) / 2, y]

    def update(self, add_pos=[0, 0]):
        self.position = [(WIDTH - self.size[0]) / 2 + add_pos[0], self.position[1] + add_pos[1]]


class Entity:
    __count = 0

    def __init__(self, size, position, color, angle=0, name='Entity', texture_status='STATIC'):
        self.size = size
        self.position = position
        self.color = color
        self.angle = angle
        self.name = name
        if self.name == 'Entity':
            self.name = f'Entity{Entity.__count}'
        self.surface = pygame.Surface(self.size)
        self.number = Entity.__count
        self.texture_status = texture_status  # possible types: 'STATIC', 'DYNAMIC'; 'STATIC' for one texture,
        # 'DYNAMIC' for multiple textures
        self.texture_index = 0
        self.TEXTURES = []
        self.texture_direction = False
        self.counter = 0  # to use the counter you need to increase it in "move" method or
        # other method that uses every iteration
        # example:
        # def move(self):
        #   self.counter += 1
        #   if self.counter > 1000:
        #       self.counter = 0
        Entity.__count += 1

    def __del__(self):
        del self
        Entity.__count -= 1

    def __str__(self):
        return self.name

    def get_number(self):
        return self.number

    def blit_texture(self, *textures):
        if self.texture_status == 'STATIC':
            self.surface.blit(*textures, (0, 0))
            self.TEXTURES.append(*textures)
        else:
            for texture in range(len(textures)):
                self.surface.blit(textures[texture], (0, 0))
                self.TEXTURES.append(textures[texture])

    def update_texture(self, texture=None, texture_dir_property='change to 0'):
        if not texture:
            self.surface.blit(self.TEXTURES[self.texture_index], (0, 0))
            if texture_dir_property == 'change to 0':
                if self.counter % 2 == 0:
                    self.texture_index += 1
                if self.texture_index == len(self.TEXTURES):
                    self.texture_index = 0
            if texture_dir_property == 'decrease':
                if self.counter % 2 == 0:
                    if self.texture_direction:
                        self.texture_index -= 1
                    if not self.texture_direction:
                        self.texture_index += 1
                if self.texture_index == len(self.TEXTURES) - 1:
                    self.texture_direction = True
                if self.texture_index == 0:
                    self.texture_direction = False
        else:
            self.surface.blit(texture, (0, 0))

    @staticmethod
    def get_entities_count():
        return Entity.__count


class Weapon(Entity):
    # class for WEAPONS, NOT BULLETS
    def __init__(self, size, position, color, angle=0, name='Entity', texture_status='DYNAMIC'):
        self.name = name
        Entity.__init__(self, size, position, color, angle, name, texture_status)

    def shoot(self, fire_rate):
        mouse = pygame.mouse.get_pressed(3)
        if mouse[0]:
            if self.counter % fire_rate == 0:
                bullet = Bullet(9, 10, [20, 20],
                                [player.position[0] - globalCords[0], player.position[1] - globalCords[1]],
                                (255, 255, 0), 50)
                bullet.surface.set_colorkey((0, 0, 0))
                bullets.append(bullet)
        self.counter += 1
        if self.counter > 1000:
            self.counter = 0


class Bullet(Entity):
    def __init__(self, speed, damage, size, position, color, distance, angle=0, name='Entity', texture_status='STATIC'):
        Entity.__init__(self, size, position, color, angle, name, texture_status)
        mousePos = pygame.mouse.get_pos()
        self.speed = speed
        self.damage = damage
        self.surface.fill(self.color)
        self.surface.blit(textures.bulletStay, (0, 0))
        self.pos = mousePos
        self.angle = player.angle + random.randint(-10, 10)
        self.distance = distance

    def move(self):
        self.counter += 1
        if self.counter == self.distance:
            bullets.remove(self)
            del self
            return None
        self.position[0] += math.sin(deg_to_rad(self.angle)) * self.speed
        self.position[1] += math.cos(deg_to_rad(self.angle)) * self.speed
        self.surface1, b = rotate(DISPLAY, self.surface, self.position,
                                  (self.size[0] / 2, self.size[1] / 2), self.angle)
        DISPLAY.blit(self.surface1, [self.position[0] + globalCords[0], self.position[1] + globalCords[1]])
        pygame.draw.rect(SCREEN, self.color,
                         pygame.Rect([globalCords[0] + self.position[0], globalCords[1] + self.position[1]],
                                     [self.size[0] + 25, self.size[1] + 25]))


class Player(Entity):
    def __init__(self, size, position, color, speed, health, angle=180, name='Entity', texture_status='STATIC',
                 backpack={'wood': [], 'metal': [], 'rubber': [], 'stone': []}, health_bar=100):
        self.name = name
        Entity.__init__(self, size, position, color, angle, name, texture_status)
        self.speed = speed
        self.health = health
        self.touchedBarrier = False
        self.direction = 'up'
        self.surface.fill(self.color)
        self.backpack = backpack
        self.backpack_length = 50
        self.max_health = health
        self.health_bar = health_bar

    def move(self, texture_dir_property_):
        global LOSE
        self.surface1, a = rotate(DISPLAY, self.surface, self.position,
                                  (self.size[0] / 2, self.size[1] / 2), self.angle)
        DISPLAY.blit(self.surface1, a)
        # player movement:
        if not self.touchedBarrier:
            keys = pygame.key.get_pressed()
            mousePos = pygame.mouse.get_pos()
            if keys[pygame.K_w]:
                globalCords[0] -= math.sin(deg_to_rad(self.angle)) * self.speed
                globalCords[1] -= math.cos(deg_to_rad(self.angle)) * self.speed
                self.direction = 'up'
            if keys[pygame.K_s]:
                globalCords[0] += math.sin(deg_to_rad(self.angle)) * self.speed
                globalCords[1] += math.cos(deg_to_rad(self.angle)) * self.speed
                self.direction = 'down'
            if keys[pygame.K_a]:
                globalCords[0] -= math.cos(deg_to_rad(self.angle)) * self.speed
                globalCords[1] += math.sin(deg_to_rad(self.angle)) * self.speed
            if keys[pygame.K_d]:
                globalCords[0] += math.cos(deg_to_rad(self.angle)) * self.speed
                globalCords[1] -= math.sin(deg_to_rad(self.angle)) * self.speed
            # if keys[pygame.K_a]:
            #     self.angle += self.speed / 1.5
            # if keys[pygame.K_d]:
            #     self.angle -= self.speed / 1.5
            x_distance = player.position[0] - mousePos[0]
            y_distance = player.position[1] - mousePos[1]
            if not x_distance:
                x_distance = 1
            if not y_distance:
                y_distance = 1
            a = math.atan(x_distance / y_distance)
            a = rad_to_deg(a)
            if self.position[1] < mousePos[1]:
                self.angle = a
            else:
                self.angle = a + 180
            # if abs(self.angle) >= 360:
            #     self.angle = 0

            if keys[pygame.K_w]:
                if self.texture_status == 'DYNAMIC':
                    self.update_texture(texture_dir_property=texture_dir_property_)
            elif keys[pygame.K_s]:
                if self.texture_status == 'DYNAMIC':
                    self.update_texture(texture_dir_property=texture_dir_property_)
            elif keys[pygame.K_a]:
                if self.texture_status == 'DYNAMIC':
                    self.update_texture(texture_dir_property=texture_dir_property_)
            elif keys[pygame.K_d]:
                if self.texture_status == 'DYNAMIC':
                    self.update_texture(texture_dir_property=texture_dir_property_)
            else:
                self.update_texture(textures.playerStay)
        else:
            if self.direction == 'down':
                globalCords[0] -= math.sin(deg_to_rad(self.angle)) * self.speed
                globalCords[1] -= math.cos(deg_to_rad(self.angle)) * self.speed
            else:
                globalCords[0] += math.sin(deg_to_rad(self.angle)) * self.speed
                globalCords[1] += math.cos(deg_to_rad(self.angle)) * self.speed
            self.touchedBarrier = False
        # draw health bar
        if self.health < self.max_health:
            pygame.draw.line(DISPLAY, (255, 0, 0),
                             [self.position[0] - self.size[0] / 2, self.position[1]],
                             [self.position[0] - self.size[0] / 2 + self.max_health * (
                                     self.health_bar / self.max_health),
                              self.position[1]], 10)
            pygame.draw.line(DISPLAY, (0, 255, 0),
                             [self.position[0] - self.size[0] / 2, self.position[1]],
                             [self.position[0] - self.size[0] / 2 + self.health * (self.health_bar / self.max_health),
                              self.position[1]], 10)
        # death
        if self.health <= 0:
            LOSE = True

        self.counter += 1
        if self.counter >= 1000:
            self.counter = 0


class Building(Entity):
    objects = 0

    def __init__(self, size, position, color, lvl, angle=0, name='Entity', texture_status='STATIC'):
        self.name = name
        Entity.__init__(self, size, position, color, angle, name, texture_status)
        self.level = lvl
        self.max_floors = 6
        self.objects_in_building = []
        self.zombieBuilding = True
        self.health = 1000
        self.max_health = 1000
        self.health_bar = 300
        if random.randint(1, 8) == 8:
            self.zombieBuilding = False
        # for i in range(self.max_floors):
        #     for i in range(4):
        #         if random.randint(1, 4) == 1:
        #             if self.zombieBuilding:
        #                 zombie = Zombie([50, 50], [0, 0], (0, 255, 0), 4, 150)
        #                 self.objects_in_building.append(zombie)
        #             else:
        #                 person = Person([50, 50], [0, 0], (0, 0, 255), 4, 100)
        #                 self.objects_in_building.append(person)
        if self.zombieBuilding:
            zombie = Zombie([50, 50], [0, 0], (0, 255, 0), 1, 150)
            zombie.surface.blit(textures.zombieStay, (0, 0))
            self.objects_in_building.append(zombie)
        else:
            person = Person([50, 50], [0, 0], (0, 0, 255), 1, 100)
            self.objects_in_building.append(person)
        if self.level == 1:
            self.surface.blit(textures.building1, (0, 0))
            self.surface.set_colorkey((100, 200, 55))
        Building.objects += 1

    def pop_object(self):
        # this function deletes object from self.objects_in_building list and appends it in the persons or zombies list
        objects_removed = []
        if self.zombieBuilding:
            for o in self.objects_in_building:
                o.position = [self.position[0], self.position[1]]
                zombies.append(o)
                objects_removed.append(o)
        else:
            for o in self.objects_in_building:
                o.position = [self.position[0], self.position[1]]
                persons.append(o)
                objects_removed.append(o)
        for i in objects_removed:
            self.objects_in_building.remove(i)

    def move(self, y):
        # damage take if touches bullet
        if in_screen([int(globalCords[0] + self.position[0]), int(globalCords[1] + self.position[1])],
                     self.size, WIDTH, HEIGHT):
            if SCREEN.get_at([int(globalCords[0] + self.position[0] + self.size[0] // 2),
                              int(globalCords[1] + self.position[1] + self.size[1] // 2)]) == (255, 255, 0, 255):
                self.health -= 10
                if self.health <= 0:
                    for i in range(4):
                        type = random.randint(1, 2)
                        if type == 1:
                            i = Item('stone', [50, 50], [self.position[0] + self.size[0] // 2,
                                                         self.position[1] + self.size[1] // 2],
                                     angle=random.randint(-180, 180))
                            items.append(i)
                        elif type == 2:
                            i = Item('metal', [50, 50], [self.position[0] + self.size[0] // 2,
                                                         self.position[1] + self.size[1] // 2],
                                     angle=random.randint(-180, 180))
                            items.append(i)
                    buildings[y].remove(self)
                    BREAK_CYCLE = True
                    del self
                    return None
                if bullets:
                    bullets.pop(0)
                return None
        pygame.draw.rect(SCREEN, self.color,
                         pygame.Rect([globalCords[0] + self.position[0], globalCords[1] + self.position[1]],
                                     [self.size[0] - 50, self.size[1] - 50]))


class Forge(Entity):
    def __init__(self, size, position, color=(100, 100, 100), angle=0, name='Entity', texture_status='DYNAMIC'):
        Entity.__init__(self, size, position, color, angle, name, texture_status)
        self.placed = False
        self.surface.blit(textures.forge, (0, 0))
        self.surface.set_colorkey((255, 255, 255))
        self.cost = {'wood': 30, 'metal': 10, 'stone': 50}
        self.built = False
        # приносишь ресурсы к кузнице и она достраивается как это СДЕЛАТЬ?!
        material = 'wood'
        while True:
            if not self.cost[material]:
                break
            if not len(player.backpack[material]):
                break
            player.backpack[material].pop()
            self.cost[material] -= 1
        material = 'metal'
        while True:
            if not self.cost[material]:
                break
            if not len(player.backpack[material]):
                break
            player.backpack[material].pop()
            self.cost[material] -= 1
        material = 'stone'
        while True:
            if not self.cost[material]:
                break
            if not len(player.backpack[material]):
                break
            player.backpack[material].pop()
            self.cost[material] -= 1

    def move(self):
        DISPLAY.blit(self.surface, [globalCords[0] + self.position[0], globalCords[1] + self.position[1]])
        x, y = globalCords[0] + self.position[0] - 150 + self.size[0] // 2, globalCords[1] + self.position[1] - 150 + \
               self.size[1] // 2
        w, h = 300, 300
        if SHOW_BORDERS:
            pygame.draw.rect(DISPLAY, (255, 0, 0), pygame.Rect([x, y], [w, h]), 2)
        if not self.built:
            if not self.cost['wood'] and not self.cost['metal'] and not self.cost['stone']:
                # if forge finished (this code executing only one iteration)
                self.built = True
                self.surface.blit(textures.forgeBuiltStay, (0, 0))
                # print('new texture haha yes!')
        if self.built:
            # if forge finished (this code executing every iteration)
            pass
        else:
            # достраивание кузницы
            if touched(x, w, player.position[0], player.size[0], y, h, player.position[1], player.size[1]):
                key = pygame.key.get_pressed()
                finishBuildingLabel = Button(text='Press "e" to continue construction', font_size=18)
                finishBuildingLabel.position = [x + (w - finishBuildingLabel.size[0]) // 2,
                                                y + h - self.size[1] * 2 - finishBuildingLabel.size[1]]
                DISPLAY.blit(finishBuildingLabel.surface, finishBuildingLabel.position)
                if key[pygame.K_e]:
                    material = 'wood'
                    while True:
                        if not self.cost[material]:
                            break
                        if not len(player.backpack[material]):
                            break
                        player.backpack[material].pop()
                        self.cost[material] -= 1
                    material = 'metal'
                    while True:
                        if not self.cost[material]:
                            break
                        if not len(player.backpack[material]):
                            break
                        player.backpack[material].pop()
                        self.cost[material] -= 1
                    material = 'stone'
                    while True:
                        if not self.cost[material]:
                            break
                        if not len(player.backpack[material]):
                            break
                        player.backpack[material].pop()
                        self.cost[material] -= 1


class Person(Entity):
    def __init__(self, size, position, color, speed, health, left_hand='', right_hand='', angle=0, name='Entity',
                 texture_status='STATIC'):
        self.name = name
        Entity.__init__(self, size, position, color, angle, name, texture_status)
        self.speed = speed
        self.health = health
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.surface.fill(self.color)

    def move(self):
        DISPLAY.blit(self.surface, [globalCords[0] + self.position[0], globalCords[1] + self.position[1]])


class Zombie(Entity):
    def __init__(self, size, position, color, speed, health, health_bar=100, left_hand='', right_hand='', angle=180,
                 name='Entity', damage=10, attack_speed=100,
                 texture_status='STATIC'):
        self.name = name
        Entity.__init__(self, size, position, color, angle, name, texture_status)
        self.speed = speed
        self.health = health
        self.max_health = int(health)
        self.health_bar = health_bar
        self.left_hand = left_hand
        self.right_hand = right_hand
        self.surface1 = pygame.Surface(self.size)
        self.surface.set_colorkey((0, 0, 0))
        self.randomAngle = random.randint(-180, 180)
        self.touchedBarrier = False
        self.damage = damage
        self.counter = 0
        self.attack_speed = attack_speed

    def move(self):
        global PLAYER_IN_SQUARE
        if in_screen([globalCords[0] + self.position[0], globalCords[1] + self.position[1]], self.size, WIDTH, HEIGHT):
            self.surface1, a = rotate(DISPLAY, self.surface, self.position,
                                      (self.size[0] / 2, self.size[1] / 2), self.angle)
            DISPLAY.blit(self.surface1, [globalCords[0] + a[0], globalCords[1] + a[1]])
            squareX = globalCords[0] + self.position[0] - 400
            squareY = globalCords[1] + self.position[1] - 400
            squareWidth = self.size[0] + 800
            squareHeight = self.size[1] + 800
            if SHOW_BORDERS:
                pygame.draw.rect(DISPLAY, (0, 100, 0), pygame.Rect([squareX, squareY], [squareWidth, squareHeight]), 2)

            # draw health bar
            if self.health < self.max_health:
                pygame.draw.line(DISPLAY, (255, 0, 0),
                                 [globalCords[0] + self.position[0] - self.size[0] / 2,
                                  globalCords[1] + self.position[1]],
                                 [globalCords[0] + self.position[0] - self.size[0] / 2 + self.max_health * (
                                         self.health_bar / self.max_health),
                                  globalCords[1] + self.position[1]],
                                 10)
                pygame.draw.line(DISPLAY, (0, 255, 0),
                                 [globalCords[0] + self.position[0] - self.size[0] / 2,
                                  globalCords[1] + self.position[1]],
                                 [globalCords[0] + self.position[0] - self.size[0] / 2 + self.health * (
                                         self.health_bar / self.max_health),
                                  globalCords[1] + self.position[1]],
                                 10)

            # damage take if touches bullet
            if in_screen([int(globalCords[0] + self.position[0]), int(globalCords[1] + self.position[1])],
                         self.size, WIDTH, HEIGHT):
                if SCREEN.get_at([int(globalCords[0] + self.position[0] + self.size[0] // 2),
                                  int(globalCords[1] + self.position[1] + self.size[1] // 2)]) == (255, 255, 0, 255):
                    self.health -= 10
                    try:
                        # формула: u = ((m1 * v1 + m2 * v2) / (m1 + m2))
                        m1 = self.health
                        v1 = self.speed
                        m2 = 10
                        v2 = 9
                        self.position[0] += math.sin(deg_to_rad(self.angle)) * (((m1 * v1 + m2 * v2) / (m1 + m2)) * -1)
                        self.position[1] += math.cos(deg_to_rad(self.angle)) * (((m1 * v1 + m2 * v2) / (m1 + m2)) * -1)
                    except ZeroDivisionError:
                        pass
                    if self.health <= 0:
                        if random.randint(1, 2) == 1:
                            type = random.randint(1, material_types)
                            if type == 1:
                                i = Item('wood', [50, 50], self.position)
                                items.append(i)
                            elif type == 2:
                                i = Item('metal', [50, 50], self.position)
                                items.append(i)
                            elif type == 3:
                                i = Item('rubber', [50, 50], self.position)
                                items.append(i)
                            elif type == 4:
                                i = Item('stone', [50, 50], self.position)
                                items.append(i)
                        zombies.remove(self)
                        del self
                    if bullets:
                        bullets.pop(0)
                    return None

            # moving
            if not self.touchedBarrier:
                if ASD:
                    pygame.draw.line(DISPLAY, (100, 100, 255),
                                     [player.position[0] + player.size[0] // 2,
                                      player.position[1] + player.size[1] // 2],
                                     [self.position[0] + globalCords[0], self.position[1] + globalCords[1]], 16)
                    pygame.draw.line(DISPLAY, (255, 255, 255),
                                     [player.position[0] + player.size[0] // 2,
                                      player.position[1] + player.size[1] // 2],
                                     [self.position[0] + globalCords[0], self.position[1] + globalCords[1]], 4)
                if touched(squareX, squareWidth, player.position[0], player.size[0],
                           squareY, squareHeight, player.position[1], player.size[1]):
                    PLAYER_IN_SQUARE = True
                    x_distance = player.position[0] - (globalCords[0] + self.position[0])
                    y_distance = player.position[1] - (globalCords[1] + self.position[1])
                    z_distance = math.sqrt(x_distance ** 2 + y_distance ** 2)
                    a = math.atan(x_distance / y_distance)
                    a = rad_to_deg(a)
                    direction = 'up'
                    if self.position[1] < player.position[1] - globalCords[1]:
                        self.angle = a
                    else:
                        self.angle = a + 180
                    self.position[0] += math.sin(deg_to_rad(self.angle)) * self.speed
                    self.position[1] += math.cos(deg_to_rad(self.angle)) * self.speed
                    if ASD:
                        zombies.remove(self)
                        del self
                        return None
                else:
                    PLAYER_IN_SQUARE = False
                    if self.angle == self.randomAngle:
                        self.randomAngle = random.randint(-180, 180)
                    if self.angle < self.randomAngle:
                        self.angle += 1
                        self.position[0] += math.sin(deg_to_rad(self.angle)) * self.speed * 0.5
                        self.position[1] += math.cos(deg_to_rad(self.angle)) * self.speed * 0.5
                    else:
                        self.angle -= 1
                        self.position[0] += math.sin(deg_to_rad(self.angle)) * self.speed * 0.5
                        self.position[1] += math.cos(deg_to_rad(self.angle)) * self.speed * 0.5
                    if abs(self.angle) >= 360:
                        self.angle = 0
            else:
                self.position[0] -= math.sin(deg_to_rad(self.angle)) * self.speed
                self.position[1] -= math.cos(deg_to_rad(self.angle)) * self.speed

            # damaging player
            if touched(self.position[0] + globalCords[0], self.size[0], player.position[0], player.size[0],
                       self.position[1] + globalCords[1], self.size[1], player.position[1], player.size[1]):
                if self.counter % self.attack_speed == 0:
                    player.health -= self.damage

            pygame.draw.rect(SCREEN, self.color,
                             pygame.Rect([globalCords[0] + self.position[0], globalCords[1] + self.position[1]],
                                         self.size))
            self.counter += 1
            if self.counter > 1000:
                self.counter = 0


class Item(Entity):
    def __init__(self, item, size, position, color=(255, 0, 255), angle=0, name='Entity',
                 texture_status='STATIC'):
        Entity.__init__(self, size, position, color, angle, name, texture_status)
        self.surface1 = pygame.Surface(self.size)
        self.surface.set_colorkey((0, 0, 0))
        self.item = item
        self.added_size = 0
        self.direction_size = True
        if self.item == 'metal':
            self.surface.blit(textures.metal, (0, 0))
        elif self.item == 'wood':
            self.surface.blit(textures.wood, (0, 0))
        elif self.item == 'rubber':
            self.surface.blit(textures.rubber, (0, 0))
        elif self.item == 'stone':
            self.surface.blit(textures.stone, (0, 0))

    def move(self):
        self.surface1, a = rotate(DISPLAY, self.surface, self.position,
                                  (self.size[0] / 2, self.size[1] / 2), self.angle)
        self.surface1 = pygame.transform.scale(self.surface1, [40, 40])
        DISPLAY.blit(self.surface1, (globalCords[0] + a[0], globalCords[1] + a[1]))

        if touched(player.position[0], player.size[0], globalCords[0] + self.position[0], self.size[0],
                   player.position[1], player.size[1], globalCords[1] + self.position[1], self.size[1]):
            if len(player.backpack) < player.backpack_length:
                items.remove(self)
                player.backpack[self.item].append(self.item)
                del self
                return None

        self.angle += 1
        if abs(self.angle) >= 360:
            self.angle = 0


def rotate(surf, image, pos, originPos, angle):
    # calculate the axis aligned bounding box of the rotated image
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot
    pivot = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    return rotated_image, [origin[0] + 25, origin[1] + 25]

    # draw rectangle around the image
    # pygame.draw.rect(surf, (255, 0, 0), (*origin, *rotated_image.get_size()), 2)


def deg_to_rad(degree):
    return degree * math.pi / 180


def rad_to_deg(radian):
    return radian * 180 / math.pi


def touched(x1, weight1, x2, weight2, y1, height1, y2, height2):
    if (x1 <= x2 and x2 <= (x1 + weight1)
        and y1 <= y2 and y2 <= (y1 + height1)) \
            or (x1 <= (x2 + weight2) and (x1 + weight1) >= x2
                and y1 <= (y2 + height2) and (y1 + height1) >= y2):
        return True
    else:
        return False


def in_screen(position, size, width_of_screen, height_of_screen):
    if 0 < position[0] < (width_of_screen - size[0]):
        if 0 < position[1] < (height_of_screen - size[1]):
            return True
        else:
            return False
    else:
        return False


def draw_map_(map_p):
    global player
    w = 12
    h = 12
    fieldWidth, fieldHeight = 100, 100
    for y in range(len(map_p)):
        if len(buildings) != len(map_p):
            buildings.append([])
        for x in range(len(map_p[y])):
            if map_p[y][x] == '-':
                if len(buildings[y]) != len(map_p[y]):
                    building = Building([150, 150], [(-x + 2) * fieldWidth, (-y + 2) * fieldHeight], (0, 0, 0), 1)
                    buildings[y].append(building)
                else:
                    DISPLAY.blit(buildings[y][x].surface,
                                 [globalCords[0] + buildings[y][x].position[0],
                                  globalCords[1] + buildings[y][x].position[1]])
                    if touched(buildings[y][x].position[0] + globalCords[0], fieldWidth,
                               player.position[0], player.size[0],
                               buildings[y][x].position[1] + globalCords[1], fieldHeight,
                               player.position[1], player.size[1]):
                        player.touchedBarrier = True
                    if SHOW_BORDERS:
                        pygame.draw.rect(DISPLAY, (255, 0, 0), pygame.Rect(
                            [buildings[y][x].position[0] + globalCords[0] - 200,
                             buildings[y][x].position[1] + globalCords[1] - 200],
                            [fieldWidth + 400, fieldHeight + 400]
                        ), 2)
                    if touched(buildings[y][x].position[0] + globalCords[0] - 200, fieldWidth + 400,
                               player.position[0], player.size[0],
                               buildings[y][x].position[1] + globalCords[1] - 200, fieldHeight + 400,
                               player.position[1], player.size[1]):
                        buildings[y][x].pop_object([1, 1])
            elif len(buildings[y]) != len(map_p[y]):
                buildings[y].append('')


def create_map(cords=[0, 0]):
    fieldWidth, fieldHeight = 100, 100
    for y in range(map_size // 100):
        if len(buildings) < map_size // 100:
            buildings.append([])
        for x in range(map_size // 100):
            if len(buildings) <= map_size // 100:
                if y == 11 and x != 5 and x != 6:
                    building = Building([150, 150], [(-x + 2) * fieldWidth + cords[0],
                                                     (-y + 2) * fieldHeight + cords[1]], (195, 195, 195), 1)
                    buildings[y].append(building)
                elif y != 0 and (x == 0 or x == 11):
                    if y != 5 and y != 6:
                        building = Building([150, 150], [(-x + 2) * fieldWidth + cords[0],
                                                         (-y + 2) * fieldHeight + cords[1]], (195, 195, 195), 1)
                        buildings[y].append(building)
                elif y == 0 and x != 5 and x != 6:
                    building = Building([150, 150], [(-x + 2) * fieldWidth + cords[0],
                                                     (-y + 2) * fieldHeight + cords[1]], (195, 195, 195), 1)
                    buildings[y].append(building)
                else:
                    buildings[y].append('')


def draw_map():
    global player
    fieldWidth, fieldHeight = 100, 100
    for y in range(len(buildings)):
        for x in range(len(buildings[y])):
            try:
                if buildings[y][x]:
                    if isinstance(buildings[y][x], Building):
                        if in_screen(
                                [globalCords[0] + buildings[y][x].position[0] + 150,
                                 globalCords[1] + buildings[y][x].position[1] + 150],
                                [buildings[y][x].size[0] - 300, buildings[y][x].size[1] - 300], WIDTH, HEIGHT):
                            DISPLAY.blit(buildings[y][x].surface,
                                         [globalCords[0] + buildings[y][x].position[0],
                                          globalCords[1] + buildings[y][x].position[1]])
                            if touched(buildings[y][x].position[0] + globalCords[0], fieldWidth,
                                       player.position[0], player.size[0],
                                       buildings[y][x].position[1] + globalCords[1], fieldHeight,
                                       player.position[1], player.size[1]):
                                player.touchedBarrier = True
                            if SHOW_BORDERS:
                                pygame.draw.rect(DISPLAY, (255, 0, 0), pygame.Rect(
                                    [buildings[y][x].position[0] + globalCords[0] - 200,
                                     buildings[y][x].position[1] + globalCords[1] - 200],
                                    [fieldWidth + 400, fieldHeight + 400]
                                ), 2)
                            if touched(buildings[y][x].position[0] + globalCords[0] - 200, fieldWidth + 400,
                                       player.position[0], player.size[0],
                                       buildings[y][x].position[1] + globalCords[1] - 200, fieldHeight + 400,
                                       player.position[1], player.size[1]):
                                buildings[y][x].pop_object()
                        buildings[y][x].move(y)
                    elif isinstance(buildings[y][x], Forge):
                        buildings[y][x].move()
            except IndexError:
                pass


def check_events():
    global RUN, WIDTH, HEIGHT, OBJECTS_CREATED, DISPLAY, DISPLAY_MODE, SCROLL, F3_PRESSED, SHOW_BORDERS
    global SCREEN, FIRE_RATE, TABLE_OPENED, fireRateCheatEnabled
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.WINDOWRESIZED:
            lastWidth = WIDTH
            lastHeight = HEIGHT
            WIDTH, HEIGHT = DISPLAY.get_size()
            SCREEN = pygame.Surface((WIDTH, HEIGHT))
            SCREEN.set_colorkey((0, 0, 0))
            globalCords[0] -= (lastWidth - WIDTH) * 0.5
            globalCords[1] -= (lastHeight - HEIGHT) * 0.5
            OBJECTS_CREATED = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            if DISPLAY_MODE == pygame.RESIZABLE:
                DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                DISPLAY_MODE = pygame.FULLSCREEN
                lastWidth = WIDTH
                lastHeight = HEIGHT
                WIDTH, HEIGHT = DISPLAY.get_size()
                SCREEN = pygame.Surface((WIDTH, HEIGHT))
                SCREEN.set_colorkey((0, 0, 0))
                globalCords[0] -= (lastWidth - WIDTH) * 0.5
                globalCords[1] -= (lastHeight - HEIGHT) * 0.5
                fullScreenModeBW.d = True
                OBJECTS_CREATED = False
            elif DISPLAY_MODE == pygame.FULLSCREEN:
                DISPLAY = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
                DISPLAY_MODE = pygame.RESIZABLE
                lastWidth = WIDTH
                lastHeight = HEIGHT
                WIDTH, HEIGHT = DISPLAY.get_size()
                SCREEN = pygame.Surface((WIDTH, HEIGHT))
                SCREEN.set_colorkey((0, 0, 0))
                globalCords[0] -= (lastWidth - WIDTH) * 0.5
                globalCords[1] -= (lastHeight - HEIGHT) * 0.5
                fullScreenModeBW.d = False
                OBJECTS_CREATED = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
            if not F3_PRESSED:
                showDebugInfoBW.d = True
                F3_PRESSED = True
            elif F3_PRESSED:
                showDebugInfoBW.d = False
                F3_PRESSED = False

        # table opening
        if event.type == pygame.KEYUP and event.key == pygame.K_t:
            if not TABLE_OPENED:
                TABLE_OPENED = True
            elif TABLE_OPENED:
                TABLE_OPENED = False

        # show borders
        keys = pygame.key.get_pressed()
        if keys[pygame.K_F3] and keys[pygame.K_b]:
            if not SHOW_BORDERS:
                showBordersBW.d = True
                SHOW_BORDERS = True
            elif SHOW_BORDERS:
                showBordersBW.d = False
                SHOW_BORDERS = False

        # cheat code
        if keys[pygame.K_o] and keys[pygame.K_d] and keys[pygame.K_m] and keys[pygame.K_e] and keys[pygame.K_n]:
            fireRateCheatEnabled = True
            FIRE_RATE = 1


def menu():
    global LEVEL, OBJECTS_CREATED, RUN, WIDTH, HEIGHT, DISPLAY_MODE, fullScreenModeBW, SCREEN, DISPLAY
    if not OBJECTS_CREATED:
        DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        DISPLAY_MODE = pygame.FULLSCREEN
        lastWidth = WIDTH
        lastHeight = HEIGHT
        WIDTH, HEIGHT = DISPLAY.get_size()
        SCREEN = pygame.Surface((WIDTH, HEIGHT))
        SCREEN.set_colorkey((0, 0, 0))
        globalCords[0] -= (lastWidth - WIDTH) * 0.5
        globalCords[1] -= (lastHeight - HEIGHT) * 0.5
        fullScreenModeBW.d = True
        OBJECTS_CREATED = True
    titleLabel = Button(text='Zombie Strike', font_size=50, color=(20, 120, 0))
    titleLabel.position = [(WIDTH - titleLabel.size[0]) / 2, 50]
    newGameButton = Button(text='Play')
    newGameButton.position = [(WIDTH - newGameButton.size[0]) / 2, 150]
    settingsButton = Button(text='Settings')
    settingsButton.position = [(WIDTH - settingsButton.size[0]) / 2, 250]
    infoButton = Button(text='Help')
    infoButton.position = [(WIDTH - infoButton.size[0]) / 2, 350]
    exitButton = Button(text='Exit')
    exitButton.position = [(WIDTH - exitButton.size[0]) / 2, 450]
    newGameButton.click()
    settingsButton.click()
    infoButton.click()
    exitButton.click()
    if newGameButton.clicked:
        pygame.time.delay(500)
        LEVEL = 'mode selection'
        OBJECTS_CREATED = False
        return None
    if settingsButton.clicked:
        pygame.time.delay(500)
        LEVEL = 'settings'
        OBJECTS_CREATED = False
    if infoButton.clicked:
        pygame.time.delay(500)
        LEVEL = 'info'
        OBJECTS_CREATED = False
    if exitButton.clicked:
        RUN = False
    DISPLAY.fill((100, 200, 55))
    DISPLAY.blit(titleLabel.surface, titleLabel.position)
    DISPLAY.blit(newGameButton.surface, newGameButton.position)
    DISPLAY.blit(settingsButton.surface, settingsButton.position)
    DISPLAY.blit(infoButton.surface, infoButton.position)
    DISPLAY.blit(exitButton.surface, exitButton.position)


def settings():
    global OBJECTS_CREATED, LEVEL, SHOW_FPS, DISPLAY, DISPLAY_MODE, WIDTH, HEIGHT, SHOW_BORDERS, F3_PRESSED
    DISPLAY.fill((100, 200, 55))

    settingsLabel = Button(text='Settings', font_size=50, color=(20, 120, 0))
    settingsLabel.create_pos(50)
    backButton = Button(text='Back')
    backButton.create_pos(550)
    showFpsButton = Button(text='Show fps:')
    showFpsButton.create_pos(150)
    showDebugInfoButton = Button(text='Show debug info:')
    showDebugInfoButton.create_pos(250)
    fullScreenModeButton = Button(text='Fullscreen mode:')
    fullScreenModeButton.create_pos(350)
    showBordersButton = Button(text='Show borders:')
    showBordersButton.create_pos(450)

    showFpsBW.update([140, 0])
    showDebugInfoBW.update([220, 0])
    fullScreenModeBW.update([220, 0])
    showBordersBW.update([190, 0])

    showFpsBW.click()
    showDebugInfoBW.click()
    fullScreenModeBW.click()
    showBordersBW.click()
    backButton.click()

    if showFpsBW.d:
        SHOW_FPS = True
    else:
        SHOW_FPS = False
    if showDebugInfoBW.d:
        F3_PRESSED = True
    else:
        F3_PRESSED = False
    if fullScreenModeBW.clicked:
        if fullScreenModeBW.d:
            DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            DISPLAY_MODE = pygame.FULLSCREEN
            lastWidth = WIDTH
            lastHeight = HEIGHT
            WIDTH, HEIGHT = DISPLAY.get_size()
            globalCords[0] -= (lastWidth - WIDTH) * 0.5
            globalCords[1] -= (lastHeight - HEIGHT) * 0.5
            OBJECTS_CREATED = False
        else:
            DISPLAY = pygame.display.set_mode((600, 600))
            DISPLAY_MODE = pygame.RESIZABLE
            lastWidth = WIDTH
            lastHeight = HEIGHT
            WIDTH, HEIGHT = DISPLAY.get_size()
            globalCords[0] -= (lastWidth - WIDTH) * 0.5
            globalCords[1] -= (lastHeight - HEIGHT) * 0.5
            OBJECTS_CREATED = False
    if showBordersBW.d:
        SHOW_BORDERS = True
    else:
        SHOW_BORDERS = False
    if backButton.clicked:
        LEVEL = 'menu'
        OBJECTS_CREATED = False
        pygame.time.delay(500)
        return None

    DISPLAY.blit(settingsLabel.surface, settingsLabel.position)
    DISPLAY.blit(backButton.surface, backButton.position)
    DISPLAY.blit(showFpsBW.surface, showFpsBW.position)
    DISPLAY.blit(showDebugInfoBW.surface, showDebugInfoBW.position)
    DISPLAY.blit(fullScreenModeBW.surface, fullScreenModeBW.position)
    DISPLAY.blit(showBordersBW.surface, showBordersBW.position)
    DISPLAY.blit(showFpsButton.surface, showFpsButton.position)
    DISPLAY.blit(showDebugInfoButton.surface, showDebugInfoButton.position)
    DISPLAY.blit(fullScreenModeButton.surface, fullScreenModeButton.position)
    DISPLAY.blit(showBordersButton.surface, showBordersButton.position)


def info():
    global OBJECTS_CREATED, LEVEL, SCROLL, scroll_y, RUN, WIDTH, HEIGHT, DISPLAY, DISPLAY_MODE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.WINDOWRESIZED:
            lastWidth = WIDTH
            lastHeight = HEIGHT
            WIDTH, HEIGHT = DISPLAY.get_size()
            globalCords[0] -= (lastWidth - WIDTH)
            globalCords[1] -= (lastHeight - HEIGHT)
            OBJECTS_CREATED = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            if DISPLAY_MODE == pygame.RESIZABLE:
                DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                DISPLAY_MODE = pygame.FULLSCREEN
                WIDTH, HEIGHT = DISPLAY.get_size()
                OBJECTS_CREATED = False
            elif DISPLAY_MODE == pygame.FULLSCREEN:
                DISPLAY = pygame.display.set_mode((600, 600))
                DISPLAY_MODE = pygame.RESIZABLE
                WIDTH, HEIGHT = DISPLAY.get_size()
                OBJECTS_CREATED = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_WHEELUP:
            SCROLL = 'down'
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_WHEELDOWN:
            SCROLL = 'up'
        elif event.type != pygame.MOUSEBUTTONDOWN:
            SCROLL = False
        if SCROLL == 'up':
            scroll_y -= 50
        if SCROLL == 'down':
            if scroll_y < 0:
                scroll_y += 50
    if not OBJECTS_CREATED:
        OBJECTS_CREATED = True
    backButton = Button(text='Back')
    backButton.position = [10, 10]
    titleLabel = Button(text='Zombie Strike', font_size=50, color=(20, 120, 0))
    titleLabel.position = [(WIDTH - titleLabel.size[0]) / 2, 50 + scroll_y]
    infoButton1 = Button(text='Welcome to Zombie Strike!')
    infoButton1.position = [(WIDTH - infoButton1.size[0]) / 2, 150 + scroll_y]
    infoButton2 = Button(text='In this game you need to kill or cure zombies.')
    infoButton2.position = [(WIDTH - infoButton2.size[0]) / 2, 250 + scroll_y]
    infoButton3 = Button(text='If you cured a zombie, then he will fight for you')
    infoButton3.position = [(WIDTH - infoButton3.size[0]) / 2, 300 + scroll_y]
    infoButton4 = Button(text='Movement')
    infoButton4.position = [(WIDTH - infoButton4.size[0]) / 2, 400 + scroll_y]
    infoButton5 = Button(text='Press "w" to move forward')
    infoButton5.position = [(WIDTH - infoButton5.size[0]) / 2, 500 + scroll_y]
    infoButton6 = Button(text='Press "s" to move back')
    infoButton6.position = [(WIDTH - infoButton6.size[0]) / 2, 550 + scroll_y]
    infoButton7 = Button(text='Press "a" to rotate counterclockwise')
    infoButton7.position = [(WIDTH - infoButton7.size[0]) / 2, 600 + scroll_y]
    infoButton8 = Button(text='Press "d" to rotate clockwise')
    infoButton8.position = [(WIDTH - infoButton8.size[0]) / 2, 650 + scroll_y]
    infoButton9 = Button(text='Press "b" to open backpack')
    infoButton9.create_pos(700 + scroll_y)
    infoButton10 = Button(text='Press "h" to open constructions menu')
    infoButton10.create_pos(750 + scroll_y)
    backButton.click()
    if backButton.clicked:
        pygame.time.delay(500)
        LEVEL = 'menu'
        OBJECTS_CREATED = False
    DISPLAY.fill((100, 200, 55))
    DISPLAY.blit(titleLabel.surface, titleLabel.position)
    DISPLAY.blit(infoButton1.surface, infoButton1.position)
    DISPLAY.blit(infoButton2.surface, infoButton2.position)
    DISPLAY.blit(infoButton3.surface, infoButton3.position)
    DISPLAY.blit(infoButton4.surface, infoButton4.position)
    DISPLAY.blit(infoButton5.surface, infoButton5.position)
    DISPLAY.blit(infoButton6.surface, infoButton6.position)
    DISPLAY.blit(infoButton7.surface, infoButton7.position)
    DISPLAY.blit(infoButton8.surface, infoButton8.position)
    DISPLAY.blit(infoButton9.surface, infoButton9.position)
    DISPLAY.blit(infoButton10.surface, infoButton10.position)
    DISPLAY.blit(backButton.surface, backButton.position)


def mode_selection():
    global LEVEL, OBJECTS_CREATED
    if not OBJECTS_CREATED:
        DISPLAY.fill((100, 200, 55))
        OBJECTS_CREATED = True
    modeSelectionTitle = Button(text='Select mode', color=(20, 120, 0), font_size=50)
    modeSelectionTitle.position = [(WIDTH - modeSelectionTitle.size[0]) / 2, 50]
    endlessButton = Button(text='Endless mode')
    endlessButton.position = [(WIDTH - endlessButton.size[0]) / 2, 150]
    backButton = Button(text='Back')
    backButton.position = [(WIDTH - backButton.size[0]) / 2, 250]
    backButton.click()
    endlessButton.click()
    if backButton.clicked:
        pygame.time.delay(500)
        LEVEL = 'menu'
        OBJECTS_CREATED = False
        return None
    if endlessButton.clicked:
        pygame.time.delay(500)
        LEVEL = 'endless'
        OBJECTS_CREATED = False
        return None
    DISPLAY.blit(modeSelectionTitle.surface, modeSelectionTitle.position)
    DISPLAY.blit(endlessButton.surface, endlessButton.position)
    DISPLAY.blit(backButton.surface, backButton.position)


def endless():
    global OBJECTS_CREATED, LEVEL, player, w, BUILDING, RUN, LOSE
    if not OBJECTS_CREATED:
        player = Player(size=[50, 50], position=[WIDTH / 2, HEIGHT / 2], color=(0, 0, 255), speed=4, health=100,
                        texture_status='DYNAMIC')
        player.backpack = {'wood': list(range(32)), 'metal': list(range(16)), 'rubber': [], 'stone': list(range(110))}
        w = Weapon([50, 50], player.position, (0, 0, 0))
        boss1 = Zombie([100, 100], [3300, -300], (0, 255, 0), 2, 1000, 200)
        boss1.surface.blit(textures.bossStay1, (0, 0))
        zombies.append(boss1)
        player.surface.set_colorkey((0, 0, 0))
        player.blit_texture(textures.playerWalk1)
        player.blit_texture(textures.playerWalk2)
        player.blit_texture(textures.playerWalk3)
        player.blit_texture(textures.playerWalk4)
        player.blit_texture(textures.playerWalk5)
        player.blit_texture(textures.playerWalk6)
        player.blit_texture(textures.playerWalk7)
        player.blit_texture(textures.playerWalk8)
        player.blit_texture(textures.playerWalk9)
        player.blit_texture(textures.playerWalk10)
        OBJECTS_CREATED = True

    mousePos = pygame.mouse.get_pos()
    mouse = pygame.mouse.get_pressed()
    key = pygame.key.get_pressed()
    DISPLAY.fill((100, 200, 55))
    menuButton = Button(text='Menu')
    menuButton.position = [10, 10]
    if SHOW_BORDERS:
        pos = [int(globalCords[0] + 300), int(globalCords[1] + 300)]
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size, pos[1] % map_size], [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size - map_size, pos[1] % map_size],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size - map_size, pos[1] % map_size - map_size],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size, pos[1] % map_size - map_size],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size, pos[1] % map_size + map_size],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size - map_size, pos[1] % map_size + map_size],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size + map_size, pos[1] % map_size - map_size],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size + map_size, pos[1] % map_size],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size + map_size, pos[1] % map_size + map_size],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size - map_size * 2, pos[1] % map_size + map_size],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size - map_size * 2, pos[1] % map_size],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size - map_size * 2, pos[1] % map_size - map_size],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size - map_size * 2, pos[1] % map_size - map_size * 2],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size - map_size, pos[1] % map_size - map_size * 2],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size, pos[1] % map_size - map_size * 2],
                                     [map_size, map_size]), 1)
        pygame.draw.rect(DISPLAY, (255, 0, 0),
                         pygame.Rect([pos[0] % map_size + map_size, pos[1] % map_size - map_size * 2],
                                     [map_size, map_size]), 1)
    menuButton.click()
    if menuButton.clicked:
        pygame.time.delay(500)
        LEVEL = 'menu'
        OBJECTS_CREATED = False
        return None
    if OBJECTS_CREATED:
        # background
        pos = [int(globalCords[0] + 300), int(globalCords[1] + 300)]
        # DISPLAY.blit(textures.grass, [pos[0] % map_size, pos[1] % map_size - map_size])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size - map_size, pos[1] % map_size - map_size])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size - map_size, pos[1] % map_size])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size, pos[1] % map_size])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size, pos[1] % map_size + map_size])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size - map_size, pos[1] % map_size + map_size])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size + map_size, pos[1] % map_size - map_size])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size + map_size, pos[1] % map_size])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size + map_size, pos[1] % map_size + map_size])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size - map_size * 2, pos[1] % map_size + map_size])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size - map_size * 2, pos[1] % map_size])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size - map_size * 2, pos[1] % map_size - map_size])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size - map_size * 2, pos[1] % map_size - map_size * 2])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size - map_size, pos[1] % map_size - map_size * 2])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size, pos[1] % map_size - map_size * 2])
        # DISPLAY.blit(textures.grass, [pos[0] % map_size + map_size, pos[1] % map_size - map_size * 2])
        player.move('decrease')
        w.shoot(FIRE_RATE)
        for i in items:
            i.move()
        for b in bullets:
            b.move()
        for z in zombies:
            z.move()
        for p in persons:
            p.move()
    draw_map()

    # building forge
    if touched(WIDTH - 300, 100, mousePos[0], 1, HEIGHT - 300, 100, mousePos[1], 1):
        if mouse[0] and counter % 20 == 0:
            if not BUILDING:
                BUILDING = 'forge'
                return None
            if BUILDING:
                BUILDING = None
                return None
    if BUILDING == 'forge':
        if in_screen([int(globalCords[0] % 100 + mousePos[0] // 100 * 100),
                      int(globalCords[1] % 100 + mousePos[1] // 100 * 100 - 100)], [100, 100], WIDTH, HEIGHT):
            if not SCREEN.get_at([int(globalCords[0] % 100 + mousePos[0] // 100 * 100),
                                  int(globalCords[1] % 100 + mousePos[1] // 100 * 100 - 100)]) == (195, 195, 195):
                pygame.draw.rect(DISPLAY, (0, 255, 0), pygame.Rect([globalCords[0] % 100 + mousePos[0] // 100 * 100,
                                                                    globalCords[1] % 100 + mousePos[
                                                                        1] // 100 * 100 - 100],
                                                                   [100, 100]), 2)
                if player.backpack['wood'] and player.backpack['metal'] and player.backpack['stone']:
                    if mouse[0] and counter % 20 == 0:
                        forge = Forge([100, 100], [mousePos[0] // 100 * 100 - globalCords[0] // 100 * 100,
                                                   mousePos[1] // 100 * 100 - globalCords[1] // 100 * 100 - 100])
                        buildings[-1].append(forge)
                else:
                    notEnoughResourceLabel = Button(text='Not enough resources', color=(255, 0, 0), font_size=30)
                    notEnoughResourceLabel.position = [
                        globalCords[0] % 100 + mousePos[0] // 100 * 100 - notEnoughResourceLabel.size[0] // 2 + 50,
                        globalCords[1] % 100 + mousePos[1] // 100 * 100 - 50 - notEnoughResourceLabel.size[1] // 2]
                    pygame.draw.rect(DISPLAY, (255, 0, 0),
                                     pygame.Rect([globalCords[0] % 100 + mousePos[0] // 100 * 100,
                                                  globalCords[1] % 100 + mousePos[
                                                      1] // 100 * 100 - 100], [100, 100]), 2)
                    DISPLAY.blit(notEnoughResourceLabel.surface, notEnoughResourceLabel.position)
            else:
                pygame.draw.rect(DISPLAY, (255, 0, 0), pygame.Rect([globalCords[0] % 100 + mousePos[0] // 100 * 100,
                                                                    globalCords[1] % 100 + mousePos[
                                                                        1] // 100 * 100 - 100], [100, 100]), 2)

    # draw player backpack
    if key[pygame.K_b]:
        pygame.draw.rect(DISPLAY, (226, 141, 90), pygame.Rect([0, HEIGHT // 1.3], [WIDTH, HEIGHT - HEIGHT // 1.3]))

        wood_count = Button(text=str(len(player.backpack['wood'])), color=(255, 255, 255))
        wood_image = pygame.transform.scale(textures.wood, [100, 100])
        wood_image.set_colorkey((0, 0, 0))
        DISPLAY.blit(wood_image, (50, HEIGHT - 150))
        DISPLAY.blit(wood_count.surface, (150, HEIGHT - 50))

        metal_count = Button(text=str(len(player.backpack['metal'])), color=(255, 255, 255))
        metal_image = pygame.transform.scale(textures.metal, [100, 100])
        metal_image.set_colorkey((0, 0, 0))
        DISPLAY.blit(metal_image, (250, HEIGHT - 150))
        DISPLAY.blit(metal_count.surface, (350, HEIGHT - 50))

        rubber_count = Button(text=str(len(player.backpack['rubber'])), color=(255, 255, 255))
        rubber_image = pygame.transform.scale(textures.rubber, [100, 100])
        rubber_image.set_colorkey((0, 0, 0))
        DISPLAY.blit(rubber_image, (450, HEIGHT - 150))
        DISPLAY.blit(rubber_count.surface, (550, HEIGHT - 50))

        stone_count = Button(text=str(len(player.backpack['stone'])), color=(255, 255, 255))
        stone_image = pygame.transform.scale(textures.stone, [100, 100])
        stone_image.set_colorkey((0, 0, 0))
        DISPLAY.blit(stone_image, (650, HEIGHT - 150))
        DISPLAY.blit(stone_count.surface, (750, HEIGHT - 50))

    # draw crafting table
    if TABLE_OPENED:
        pygame.draw.rect(DISPLAY, (150, 150, 150), pygame.Rect([(WIDTH - 300) // 2, 50], [300, 300]))
        pygame.draw.rect(DISPLAY, (100, 100, 100), pygame.Rect([(WIDTH - 300) // 2, 50], [300, 300]), 2)
        pygame.draw.line(DISPLAY, (100, 100, 100), [(WIDTH - 300) // 2, 250], [(WIDTH - 300) // 2 + 300, 250], 2)
        pygame.draw.line(DISPLAY, (100, 100, 100), [(WIDTH - 300) // 2, 150], [(WIDTH - 300) // 2 + 300, 150], 2)
        pygame.draw.line(DISPLAY, (100, 100, 100), [(WIDTH - 300) // 2 + 200, 50], [(WIDTH - 300) // 2 + 200, 350], 2)
        pygame.draw.line(DISPLAY, (100, 100, 100), [(WIDTH - 300) // 2 + 100, 50], [(WIDTH - 300) // 2 + 100, 350], 2)
        pygame.draw.polygon(DISPLAY, (150, 150, 150), [[(WIDTH - 300) // 2 + 300, 50], [(WIDTH - 300) // 2 + 350, 75],
                                                       [(WIDTH - 300) // 2 + 350, 225]])

    # draw constructions menu
    pygame.draw.rect(DISPLAY, (150, 150, 150), pygame.Rect([WIDTH - 300, HEIGHT - 300], [300, 300]))
    pygame.draw.rect(DISPLAY, (100, 100, 100), pygame.Rect([WIDTH - 300, HEIGHT - 300], [300, 300]), 2)
    pygame.draw.line(DISPLAY, (100, 100, 100), [WIDTH - 300, HEIGHT - 200], [WIDTH, HEIGHT - 200], 2)
    pygame.draw.line(DISPLAY, (100, 100, 100), [WIDTH - 300, HEIGHT - 100], [WIDTH, HEIGHT - 100], 2)
    pygame.draw.line(DISPLAY, (100, 100, 100), [WIDTH - 200, HEIGHT - 300], [WIDTH - 200, HEIGHT], 2)
    pygame.draw.line(DISPLAY, (100, 100, 100), [WIDTH - 100, HEIGHT - 300], [WIDTH - 100, HEIGHT], 2)

    # death
    if LOSE:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUN = False
                    return None
            mouse = pygame.mouse.get_pressed(3)
            if mouse[0] or mouse[1] or mouse[2]:
                LEVEL = 'menu'
                LOSE = False
                restart()
                pygame.time.delay(500)
                return None
            loseLabel = Button(text='You lose', font_size=50)
            loseLabel.create_pos(HEIGHT // 2 - 50)
            pressLabel = Button(text='Click to continue')
            pressLabel.create_pos(HEIGHT // 2 + 50)
            DISPLAY.blit(loseLabel.surface, loseLabel.position)
            DISPLAY.blit(pressLabel.surface, pressLabel.position)
            pygame.display.update()
            CLOCK.tick(FPS)

    DISPLAY.blit(menuButton.surface, menuButton.position)
    if SHOW_FPS:
        fpsLabel = Button(text=str(int(CLOCK.get_fps())))
        DISPLAY.blit(fpsLabel.surface, (WIDTH - fpsLabel.size[0] - 10, 10))
    if F3_PRESSED:
        info1 = Button(text=f'FPS : {int(CLOCK.get_fps())}', color=(100, 100, 100), font_size=10)
        info2 = Button(text=f'globalCords : {int(globalCords[0]), int(globalCords[1])}', color=(100, 100, 100),
                       font_size=10)
        info3 = Button(text=f'LEVEL : {LEVEL}', color=(100, 100, 100), font_size=10)
        info4 = Button(text=f'DISPLAY_MODE : {DISPLAY_MODE}', color=(100, 100, 100), font_size=10)
        info5 = Button(text=f'WIDTH : {WIDTH}', color=(100, 100, 100), font_size=10)
        info6 = Button(text=f'HEIGHT : {HEIGHT}', color=(100, 100, 100), font_size=10)
        info7 = Button(text=f'FPS_MAX_LIMIT : {FPS}', color=(100, 100, 100), font_size=10)
        info8 = Button(text=f'SHOW_FPS : {SHOW_FPS}', color=(100, 100, 100), font_size=10)
        info9 = Button(text=f'player : {player.__str__()}', color=(100, 100, 100), font_size=10)
        info10 = Button(text=f'player.angle : {player.angle}', color=(100, 100, 100), font_size=10)
        info11 = Button(text=f'player.counter : {player.counter}', color=(100, 100, 100), font_size=10)
        info12 = Button(text=f'player.texture_status : {player.texture_status}', color=(100, 100, 100), font_size=10)
        info13 = Button(text=f'player.texture_direction : {player.texture_direction}', color=(100, 100, 100),
                        font_size=10)
        info14 = Button(text=f'player.texture_index : {player.texture_index}', color=(100, 100, 100), font_size=10)
        info15 = Button(text=f'player.direction : {player.direction}', color=(100, 100, 100), font_size=10)
        info16 = Button(text=f'player.touchedBarrier : {player.touchedBarrier}', color=(100, 100, 100), font_size=10)
        info17 = Button(text=f'player.size : {player.size}', color=(100, 100, 100), font_size=10)
        info18 = Button(text=f'Entity.__count : {Entity.get_entities_count()}', color=(100, 100, 100), font_size=10)
        info100 = Button(text='Attention, the fps value may be less while the f3 key is pressed',
                         color=(255, 0, 0), font_size=10)
        DISPLAY.blit(info1.surface, (10, 60))
        DISPLAY.blit(info2.surface, (10, 70))
        DISPLAY.blit(info3.surface, (10, 80))
        DISPLAY.blit(info4.surface, (10, 90))
        DISPLAY.blit(info5.surface, (10, 100))
        DISPLAY.blit(info6.surface, (10, 110))
        DISPLAY.blit(info7.surface, (10, 120))
        DISPLAY.blit(info8.surface, (10, 130))
        DISPLAY.blit(info9.surface, (10, 140))
        DISPLAY.blit(info10.surface, (10, 150))
        DISPLAY.blit(info11.surface, (10, 160))
        DISPLAY.blit(info12.surface, (10, 170))
        DISPLAY.blit(info13.surface, (10, 180))
        DISPLAY.blit(info14.surface, (10, 190))
        DISPLAY.blit(info15.surface, (10, 200))
        DISPLAY.blit(info16.surface, (10, 210))
        DISPLAY.blit(info17.surface, (10, 220))
        DISPLAY.blit(info18.surface, (10, 230))
        DISPLAY.blit(info100.surface, (10, 240))


def restart():
    global counter, LOSE, SHOW_FPS, SCROLL, scroll_y, F3_PRESSED, SHOW_BORDERS, PLAYER_IN_SQUARE, ASD, TABLE_OPENED
    global BUILDING, globalCords, map_size, SPEED, HEALTH, FIRE_RATE, material_types, fireRateCheatEnabled, showFpsBW
    global showDebugInfoBW, fullScreenModeBW, showBordersBW, buildings, zombies, persons, bullets, items, WIDTH, HEIGHT
    global OBJECTS_CREATED
    DISPLAY = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
    pygame.display.set_caption('Zombie Strike')
    textures.zombieStay.set_colorkey((0, 0, 0))
    pygame.display.set_icon(pygame.transform.rotate(textures.zombieStay, 90))
    DISPLAY_MODE = pygame.RESIZABLE
    WIDTH, HEIGHT = DISPLAY.get_size()
    SCREEN = pygame.Surface((WIDTH, HEIGHT))
    SCREEN.set_colorkey((0, 0, 0))
    RUN = True
    LEVEL = 'menu'
    CLOCK = pygame.time.Clock()
    OBJECTS_CREATED = False
    BREAK_CYCLE = False
    FPS = 60
    counter = 0
    LOSE = False

    SHOW_FPS = False
    SCROLL = False  # possible: False, 'up', 'down'
    scroll_y = 0
    F3_PRESSED = False
    SHOW_BORDERS = False
    PLAYER_IN_SQUARE = False
    ASD = False
    TABLE_OPENED = False
    BUILDING = None

    globalCords = [550, 550]
    map_size = 1200

    # player references
    SPEED = 4
    HEALTH = 100
    FIRE_RATE = 20
    material_types = 4
    # cheats
    fireRateCheatEnabled = False

    showFpsBW = BoolWidget()
    showFpsBW.create_pos(150)
    showDebugInfoBW = BoolWidget()
    showDebugInfoBW.create_pos(250)
    fullScreenModeBW = BoolWidget()
    fullScreenModeBW.create_pos(350)
    showBordersBW = BoolWidget()
    showBordersBW.create_pos(450)

    # lists
    buildings = []
    zombies = []
    persons = []
    bullets = []
    items = []

    # map
    create_map()
    create_map([-1200, -1200])
    create_map([0, -1200])
    create_map([1200, -1200])
    create_map([1200, 0])
    create_map([1200, 1200])
    create_map([0, 1200])
    create_map([-1200, 1200])
    create_map([-1200, 0])
    # place for boss
    create_map([3600, 0])

    DISPLAY = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    DISPLAY_MODE = pygame.FULLSCREEN
    lastWidth = WIDTH
    lastHeight = HEIGHT
    WIDTH, HEIGHT = DISPLAY.get_size()
    SCREEN = pygame.Surface((WIDTH, HEIGHT))
    SCREEN.set_colorkey((0, 0, 0))
    globalCords[0] -= (lastWidth - WIDTH) * 0.5
    globalCords[1] -= (lastHeight - HEIGHT) * 0.5
    fullScreenModeBW.d = True
    OBJECTS_CREATED = False


DISPLAY = pygame.display.set_mode((600, 600), pygame.RESIZABLE)
pygame.display.set_caption('Zombie Strike')
textures.zombieStay.set_colorkey((0, 0, 0))
pygame.display.set_icon(pygame.transform.rotate(textures.zombieStay, 90))
DISPLAY_MODE = pygame.RESIZABLE
WIDTH, HEIGHT = DISPLAY.get_size()
SCREEN = pygame.Surface((WIDTH, HEIGHT))
SCREEN.set_colorkey((0, 0, 0))
RUN = True
LEVEL = 'menu'
CLOCK = pygame.time.Clock()
OBJECTS_CREATED = False
FPS = 60
counter = 0
LOSE = False

SHOW_FPS = False
SCROLL = False  # possible: False, 'up', 'down'
scroll_y = 0
F3_PRESSED = False
SHOW_BORDERS = False
PLAYER_IN_SQUARE = False
ASD = False
TABLE_OPENED = False
BUILDING = None

globalCords = [550, 550]
map_size = 1200

# player references
SPEED = 4
HEALTH = 100
FIRE_RATE = 20
material_types = 4
# cheats
fireRateCheatEnabled = False

showFpsBW = BoolWidget()
showFpsBW.create_pos(150)
showDebugInfoBW = BoolWidget()
showDebugInfoBW.create_pos(250)
fullScreenModeBW = BoolWidget()
fullScreenModeBW.create_pos(350)
showBordersBW = BoolWidget()
showBordersBW.create_pos(450)

# lists
buildings = []
zombies = []
persons = []
bullets = []
items = []

# map
create_map()
create_map([-1200, -1200])
create_map([0, -1200])
create_map([1200, -1200])
create_map([1200, 0])
create_map([1200, 1200])
create_map([0, 1200])
create_map([-1200, 1200])
create_map([-1200, 0])
# place for boss
create_map([3600, 0])

if __name__ == '__main__':
    while RUN:
        if LEVEL == 'endless':
            check_events()
            endless()
        if LEVEL == 'menu':
            check_events()
            menu()
        if LEVEL == 'mode selection':
            check_events()
            mode_selection()
        if LEVEL == 'settings':
            check_events()
            settings()
        if LEVEL == 'info':
            info()
        if SHOW_FPS and LEVEL != 'endless':
            fpsLabel = Button(text=str(int(CLOCK.get_fps())), background=(100, 200, 55))
            DISPLAY.blit(fpsLabel.surface, (WIDTH - fpsLabel.size[0] - 10, 10))

        # DISPLAY.blit(SCREEN, (0, 0))

        counter += 1
        if counter > 1000:
            counter = 0

        pygame.display.update()
        CLOCK.tick(FPS)

        SCREEN.fill((0, 0, 0))
