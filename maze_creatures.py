import pygame as pg
from heapq import *


class Mosquito:
    def __init__(self, radius, square):
        self.class_name = 'player'
        self.name = 'maskit'

        self.start_square = square
        self.square = square
        self.radius = radius
        self.color = pg.Color(100, 100, 100)

        self.key_left = pg.K_LEFT
        self.key_right = pg.K_RIGHT
        self.key_up = pg.K_UP
        self.key_down = pg.K_DOWN
        self.key_shoot = pg.K_SPACE

        self.lives = 3
        self.score = 0
        self.bag = {}

        self.bullets = []
        self.direction = (0, 1)

        self.ancestors = None
        self.goal = None
        self.is_path = False

    def key_pressed(self, game):
        key = pg.key.get_pressed()

        mr, mc, cr, cc = self.square
        dmr, dmc, dcr, dcc = 0, 0, 0, 0
        if key[self.key_up]:
            self.direction = (0, -1)
            dcr = -1
            if cr + dcr < 0:
                if self.square[0] > 0:
                    dmr = -1
                else:
                    dcr = 0
            self.move(game, (dmr, dmc, dcr, dcc))

        elif key[self.key_down]:
            self.direction = (0, 1)
            dcr = 1
            if cr + dcr > game.lvl.cell_rows - 1:
                if self.square[0] < game.lvl.map_rows - 1:
                    dmr = 1
                else:
                    dcr = 0
            self.move(game, (dmr, dmc, dcr, dcc))

        elif key[self.key_left]:
            self.direction = (-1, 0)
            dcc = -1
            if cc + dcc < 0:
                if self.square[1] > 0:
                    dmc = -1
                else:
                    dcc = 0
            self.move(game, (dmr, dmc, dcr, dcc))

        elif key[self.key_right]:
            self.direction = (1, 0)
            dcc = 1
            if cc + dcc > game.lvl.cell_cols - 1:
                if self.square[1] < game.lvl.map_cols - 1:
                    dmc = 1
                else:
                    dcc = 0
            self.move(game, (dmr, dmc, dcr, dcc))

        if key[self.key_shoot]:
            bullet = Bullet(self.color, (self.square[0], self.square[1]),
                            (self.square[3]*50 + 25, self.square[2]*50 + 25), 3, 3, 5, self.direction)
            self.bullets.append(bullet)

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

    def build_path(self, game):
        cell_cols = game.lvl.cell_cols

        mr, mc, cr, cc = self.square
        start = cr*cell_cols + cc

        queue = []
        heappush(queue, (0, start))
        d = [1000000]*cell_cols*game.lvl.cell_rows
        d[start] = 0
        ancestors = {start: None}

        goal_r, goal_c = self.goal // cell_cols, self.goal % cell_cols

        while queue:
            cur_cost, u = heappop(queue)
            if u == self.goal:
                break

            for neighbour in game.graph[u]:
                weight_uv, v = neighbour

                if d[u] + weight_uv < d[v]:
                    d[v] = d[u] + weight_uv
                    ancestors[v] = u

                    v_r, v_c = v // cell_cols, v % cell_cols

                    heuristic = abs(v_r - goal_r) + abs(v_c - goal_c)
                    priority = d[u] + weight_uv + heuristic
                    heappush(queue, (priority, v))
        self.ancestors = ancestors

    def draw_path(self, game):
        current = self.goal
        while current and (current in self.ancestors):
            x = int((current % game.lvl.cell_cols + 0.5) * game.square_size)
            y = int((current // game.lvl.cell_cols + 0.5) * game.square_size)
            radius = 5
            pg.draw.circle(game.lvl.window, pg.Color('blue'), (x, y), radius)
            current = self.ancestors[current]

        # pg.draw.circle(self.lvl.window, pg.Color('green'), *get_circle(*start))
        # pg.draw.circle(self.lvl.window, pg.Color('magenta'), *get_circle(*goal))


class Bullet:
    def __init__(self, color, cell, position, width, height, speed, direction):
        self.color = color
        self.width = width
        self.height = height
        self.cell = cell
        self.position = position
        self.speed = speed
        self.direction = direction

    def move(self, game):
        x = self.position[0] + self.speed*self.direction[0]
        y = self.position[1] + self.speed*self.direction[1]

        if self.collide(game, self.cell, x, y):
            game.lvl.mask.bullets.remove(self)
        else:
            self.position = (x, y)

    def collide(self, game, cell, x, y):
        if (x - self.width <= 0) or (x >= game.lvl.cell_cols * game.square_size) or (y - self.height <= 0) or\
                (y >= game.lvl.cell_rows*game.square_size):
            return True

        mr, mc = cell
        cr = y // game.square_size
        cc = x // game.square_size
        for obj in game.lvl.map[mr][mc][cr][cc]:
            if obj.class_name == 'enemy':
                game.lvl.ghosts .remove(obj)
                game.lvl.map[mr][mc][cr][cc].remove(obj)
                return True

        return False

    def draw(self, game):
        pg.draw.rect(game.lvl.window, self.color, (self.position[0], self.position[1], self.width, self.height))


class Enemy:
    def __init__(self, radius, square):
        self.class_name = 'enemy'
        self.name = 'ghost'

        self.square = square
        self.d_row = 0
        self.d_col = 0

        self.radius = radius
        self.color = pg.Color(0, 200, 0)

    def is_ate(self, square):
        return self.square == square

    def draw(self, game):
        pg.draw.circle(game.lvl.window, self.color, (self.square[3]*game.square_size + game.square_size//2,
                                                     self.square[2]*game.square_size + game.square_size//2),
                       self.radius)


class Ghost(Enemy):
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


class Ant(Enemy):
    def __init__(self, radius, square, trajectory):
        super(Ant, self).__init__(radius, square)
        self.trajectory = trajectory
        self.move_idx = 0

    def move(self, game):
        self.move_idx = (self.move_idx + 1) % len(self.trajectory)
        mr, mc, cr, cc = self.trajectory[self.move_idx]

        game.lvl.map[self.square[0]][self.square[1]][self.square[2]][self.square[3]].remove(self)
        self.square = (mr, mc, cr, cc)
        game.lvl.map[self.square[0]][self.square[1]][self.square[2]][self.square[3]].append(self)
