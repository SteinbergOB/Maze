import pygame as pg


colors = {'grass': pg.Color(0, 0, 0), 'stone_wall': pg.Color(0, 0, 100), 'exit': pg.Color(0, 200, 200),
          'apple': pg.Color(200, 0, 0), 'red_key': pg.Color(200, 0, 0), 'red_gate': pg.Color(200, 0, 0),
          'teleport': pg.Color(100, 0, 100)}

images = {'apple': pg.image.load('img/apple.png'), 'cherry': pg.image.load('img/cherry.png')}


class Block:
    def __init__(self, class_name, name, rect):
        self.class_name = class_name
        self.name = name
        self.rect = rect
        self.color = colors[name]

    def draw(self, game):
        pg.draw.rect(game.lvl.window, self.color, self.rect)


class Gate(Block):
    def __init__(self, class_name, name, rect):
        super().__init__(class_name, name, rect)
        self.open = False

    def draw(self, game):
        if self.open:
            x, y, w, h = self.rect
            pg.draw.rect(game.lvl.window, colors[self.name], (x-1, y-1, w//4, h//4))
            pg.draw.rect(game.lvl.window, colors[self.name], ((3*w)//4 + x-1, y-1, w//4, h//4))
            pg.draw.rect(game.lvl.window, colors[self.name], (x-1, (3*h)//4 + y-1, w//4, h//4))
            pg.draw.rect(game.lvl.window, colors[self.name], ((3*w)//4 + x-1, (3*h)//4 + y-1, w//4, h//4))
        else:
            super().draw(game)


class Teleport(Block):
    def __init__(self, class_name, name, rect, destination):
        super().__init__(class_name, name, rect)
        self.destination = destination


class Food:
    def __init__(self, class_name, name, position):
        self.class_name = class_name
        self.name = name
        self.pos = position
        self.img = images[name]

    def draw(self, game):
        game.lvl.window.blit(self.img, self.pos)
