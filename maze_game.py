import pygame as pg
from maze_map import map_dig_to_map_obj
from maze_creatures import Mosquito, Ghost, Ant
from maze_map import maps_, masks_, ghosts_, teleports_


class Game:
    def __init__(self):
        self.square_size = 50

        self.lvl = Lvl(self, maps_, masks_, ghosts_, teleports_)

        self.menu = Menu(pg.Color((20, 50, 20)), self.lvl.cell_cols*self.square_size, 0,
                         4*self.square_size, (self.lvl.cell_rows + 2)*self.square_size)
        self.footer = Footer(pg.Color((0, 100, 100)), 0, self.lvl.cell_rows*self.square_size,
                             self.lvl.cell_cols*self.square_size, 2*self.square_size)

        self.clock = pg.time.Clock()
        self.fps = 100
        self.count = 0

    def new_lvl(self):
        self.lvl.new_lvl(self)

    def draw_cell(self):
        for row in range(self.lvl.cell_rows):
            for col in range(self.lvl.cell_cols):
                for obj in self.lvl.map[self.lvl.mask.square[0]][self.lvl.mask.square[1]][row][col]:
                    obj.draw(self)

        for bullet in self.lvl.mask.bullets:
            bullet.draw(self)

    def change_all(self):
        if self.count % 20 == 0:
            self.lvl.mask.key_pressed(self)
            if self.lvl.mask.is_collide(self):
                if self.lvl.mask.lives > 1:
                    self.lvl.mask.lives -= 1
                else:
                    self.new_lvl()
        for bullet in self.lvl.mask.bullets:
            bullet.move(self)

        if self.count % 50 == 0:
            for ghost in self.lvl.ghosts:
                if (ghost.square[0], ghost.square[1]) == (self.lvl.mask.square[0], self.lvl.mask.square[1]):
                    ghost.move(self, self.lvl.mask.square[2], self.lvl.mask.square[3])
            if self.lvl.mask.is_collide(self):
                if self.lvl.mask.lives > 1:
                    self.lvl.mask.lives -= 1
                else:
                    self.new_lvl()

    def draw_frame(self):
        self.lvl.window.fill((0, 0, 0))
        self.draw_cell()
        self.footer.draw(self)
        self.menu.draw(self)

        pg.display.update()

    def remove_object(self):
        pass


class Footer:
    def __init__(self, color, x, y, width, height):
        self.font = pg.font.Font('freesansbold.ttf', 32)
        self.rect = pg.Rect((x, y, width, height))
        self.color = color

    def draw(self, game):
        pg.draw.rect(game.lvl.window, pg.Color(20, 20, 20), self.rect)

        txt = self.font.render('Lvl: ' + str(game.lvl.lvl_number + 1), True, (0, 0, 0))
        game.lvl.window.blit(txt, (self.rect.x + 35, self.rect.y + 30))

        txt = self.font.render('Lives: ' + str(game.lvl.mask.lives), True, (0, 0, 0))
        game.lvl.window.blit(txt, (self.rect.x + 3*game.square_size, self.rect.y + 30))

        txt = self.font.render('Bullets: ' + str(len(game.lvl.mask.bullets)), True, (0, 0, 0))
        game.lvl.window.blit(txt, (self.rect.x + 6*game.square_size, self.rect.y + 30))


class Menu:
    def __init__(self, color, x, y, width, height):
        self.font = pg.font.Font('freesansbold.ttf', 32)
        self.rect = pg.Rect((x, y, width, height))
        self.color = color

    def draw(self, game):
        pg.draw.rect(game.lvl.window, self.color, self.rect)

        for i, obj in enumerate(game.lvl.mask.bag):
            txt = self.font.render(obj + ': ' + str(game.lvl.mask.bag[obj]), True, (0, 0, 0))
            game.lvl.window.blit(txt, (self.rect.x + 15, self.rect.y + 30 + i*40))


class Map:
    def __init__(self, window, color, x, y, width, height):
        self.window = window
        self.rect = pg.Rect((x, y, width, height))
        self.color = color

    def draw(self):
        pg.draw.rect(self.window, self.color, self.rect)


class Lvl:
    def __init__(self, game, maps, masks, all_ghosts, all_teleports):
        self.lvl_number = 0
        self.maps = maps
        self.masks = masks
        self.all_ghosts = all_ghosts
        self.all_teleports = all_teleports

        self.map = map_dig_to_map_obj(self.maps[0], game.square_size)
        self.map_rows = len(self.maps[0])
        self.map_cols = len(self.maps[0][0])
        self.cell_rows = len(self.maps[0][0][0])
        self.cell_cols = len(self.maps[0][0][0][0])
        self.window = pg.display.set_mode(((self.cell_cols + 4)*game.square_size,
                                           (self.cell_rows + 2)*game.square_size))
        pg.display.set_caption('Maze lvl: ' + str(1))

        mask_square = self.masks[0]
        mask_radius = game.square_size // 6
        (mr, mc, cr, cc) = mask_square
        self.mask = Mosquito(mask_radius, mask_square)
        self.map[mr][mc][cr][cc].append(self.mask)

        self.ghosts = []
        for ghost_square in self.all_ghosts[0]:
            ghost_radius = game.square_size // 3
            ghost = Ghost(ghost_radius, ghost_square)
            (mr, mc, cr, cc) = ghost_square
            self.ghosts.append(ghost)
            self.map[mr][mc][cr][cc].append(ghost)

    def new_lvl(self, game):
        self.map = map_dig_to_map_obj(self.maps[self.lvl_number], game.square_size)
        self.map_rows = len(self.maps[self.lvl_number])
        self.map_cols = len(self.maps[self.lvl_number][0])
        self.cell_rows = len(self.maps[self.lvl_number][0][0])
        self.cell_cols = len(self.maps[self.lvl_number][0][0][0])
        self.window = pg.display.set_mode(((self.cell_cols + 4)*game.square_size,
                                           (self.cell_rows + 2)*game.square_size))
        pg.display.set_caption('Maze lvl: ' + str(self.lvl_number + 1))

        mask_square = self.masks[self.lvl_number]
        mask_radius = game.square_size//6
        (mr, mc, cr, cc) = mask_square
        self.mask = Mosquito(mask_radius, mask_square)
        self.map[mr][mc][cr][cc].append(self.mask)

        self.ghosts = []
        for ghost_square in self.all_ghosts[self.lvl_number]:
            ghost_radius = game.square_size // 3
            ghost = Ghost(ghost_radius, ghost_square)
            (mr, mc, cr, cc) = ghost_square
            self.ghosts.append(ghost)
            self.map[mr][mc][cr][cc].append(ghost)
