import pygame as pg


class Mosquito:
    def __init__(self, radius, square):
        self.class_name = 'player'
        self.name = 'maskit'

        self.start_square = square
        self.square = square
        self.radius = radius
        self.color = pg.Color(100, 100, 100)

        self.lives = 3
        self.score = 0
        self.bag = {}

    def key_pressed(self, game):
        key = pg.key.get_pressed()

        mr, mc, cr, cc = self.square
        dmr, dmc, dcr, dcc = 0, 0, 0, 0
        if key[pg.K_UP]:
            dcr = -1
            if cr + dcr < 0:
                if self.square[0] > 0:
                    dmr = -1
                else:
                    dcr = 0
            self.move(game, (dmr, dmc, dcr, dcc))

        elif key[pg.K_DOWN]:
            dcr = 1
            if cr + dcr > game.lvl.cell_rows - 1:
                if self.square[0] < game.lvl.map_rows - 1:
                    dmr = 1
                else:
                    dcr = 0
            self.move(game, (dmr, dmc, dcr, dcc))

        elif key[pg.K_LEFT]:
            dcc = -1
            if cc + dcc < 0:
                if self.square[1] > 0:
                    dmc = -1
                else:
                    dcc = 0
            self.move(game, (dmr, dmc, dcr, dcc))

        elif key[pg.K_RIGHT]:
            dcc = 1
            if cc + dcc > game.lvl.cell_cols - 1:
                if self.square[1] < game.lvl.map_cols - 1:
                    dmc = 1
                else:
                    dcc = 0
            self.move(game, (dmr, dmc, dcr, dcc))

    def move(self, game, d_square):
        cr = (self.square[2] + d_square[2]) % game.lvl.cell_rows
        cc = (self.square[3] + d_square[3]) % game.lvl.cell_cols
        square_next = game.lvl.map[self.square[0] + d_square[0]][self.square[1] + d_square[1]][cr][cc]

        can_move = False
        if square_next[0].class_name == 'ground':
            can_move = True

            for obj in square_next:
                if (obj.class_name == 'food') or (obj.class_name == 'key'):
                    square_next.remove(obj)
                    if obj.name in self.bag:
                        self.bag[obj.name] += 1
                    else:
                        self.bag[obj.name] = 1

        elif square_next[0].class_name == 'gate':
            if square_next[0].open:
                can_move = True
            elif (square_next[0].name == 'red_gate') and ('red_key' in self.bag):
                square_next[0].open = True
                can_move = True
                if self.bag['red_key'] > 1:
                    self.bag['red_key'] -= 1
                else:
                    self.bag.pop('red_key')

        elif square_next[0].class_name == 'exit':
            game.lvl.lvl_number += 1
            game.new_lvl()

        if can_move:
            self.move_to_square(game, (self.square[0] + d_square[0], self.square[1] + d_square[1], cr, cc))

    def move_to_square(self, game, square):
        game.lvl.map[self.square[0]][self.square[1]][self.square[2]][self.square[3]].remove(self)
        self.square = [square[0], square[1], square[2], square[3]]
        game.lvl.map[square[0]][square[1]][square[2]][square[3]].append(self)

    def draw(self, game):
        pg.draw.circle(game.lvl.window, self.color, (self.square[3]*game.square_size + game.square_size//2,
                                                     self.square[2]*game.square_size + game.square_size//2),
                       self.radius)

    def is_collide(self, game):
        for obj in game.lvl.map[self.square[0]][self.square[1]][self.square[2]][self.square[3]]:
            if obj.class_name == 'enemy':
                return True
        return False


class Frog:
    def __init__(self, radius, square):
        self.class_name = 'enemy'
        self.name = 'frog'

        self.square = square
        self.d_row = 0
        self.d_col = 0

        self.radius = radius

        self.color = pg.Color(0, 200, 0)

    def move(self, game, row, col):
        if self.square[2] < row:
            self.d_row = 1
        elif self.square[2] == row:
            self.d_row = 0
        elif self.square[2] > row:
            self.d_row = -1

        if self.square[3] < col:
            self.d_col = 1
        elif self.square[3] == col:
            self.d_col = 0
        elif self.square[3] > col:
            self.d_col = -1

        game.lvl.map[self.square[0]][self.square[1]][self.square[2]][self.square[3]].remove(self)
        self.square = (self.square[0], self.square[1], self.square[2] + self.d_row, self.square[3] + self.d_col)
        game.lvl.map[self.square[0]][self.square[1]][self.square[2]][self.square[3]].append(self)

    def is_ate(self, square):
        return self.square == square

    def draw(self, game):
        pg.draw.circle(game.lvl.window, self.color, (self.square[3]*game.square_size + game.square_size//2,
                                                     self.square[2]*game.square_size + game.square_size//2),
                       self.radius)
