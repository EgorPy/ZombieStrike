import random


class MapList:
    def __init__(self, map_):
        self.MAP = map_
        self.reverse_all_sides()

    def reverse_all_sides(self):
        self.MAP.reverse()
        reverse_string(self.MAP)

    def append_right(self, item):
        for i in range(len(self.MAP)):
            self.MAP[i] += item[i]

    def append_bottom(self, item):
        self.MAP.append(item)

    def append_top(self, item):
        self.MAP.insert(0, item)

    def append_left(self, item):
        for i in range(len(self.MAP)):
            self.MAP[i] = item[i] + self.MAP[i]

    def add_map(self, side):
        # надо сделать так,
        # чтобы карта дополнялась
        # когда игрок заходит за пределы карты,
        # чтобы генерировались "комнаты"
        # с четырьмя сторонами и с одним или двумя проходами дальше
        if side == 'top':
            for i in range(11):
                if i != 5 and i != 6:
                    map1.append_top('-          -')
                else:
                    map1.append_top('            ')
            map1.append_top('-----  -----')
        if side == 'bottom':
            for i in range(11):
                if i != 5 and i != 6:
                    map1.append_bottom('-          -')
                else:
                    map1.append_bottom('            ')
            map1.append_bottom('-----  -----')

    def __len__(self):
        return len(self.MAP)

    def __getitem__(self, item):
        return self.MAP[item]


def reverse_string(map_p):
    for i in range(len(map_p)):
        map_p[i] = map_p[i][::-1]


map1 = MapList(['-----  -----',
                '-          -',
                '-          -',
                '-          -',
                '-          -',
                '            ',
                '            ',
                '-          -',
                '-          -',
                '-          -',
                '-          -',
                '-----  -----'])

# print(*map1, sep='\n')
