import pygame as pg
from maze_game import Game


def main():
    pg.init()
    game = Game()

    while True:
        game.count += 1
        game.change_all()
        game.draw_frame()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                game.lvl.mask.is_path = True

                x, y = pg.mouse.get_pos()
                row, col = y // game.square_size, x // game.square_size
                goal = row*game.lvl.cell_cols + col
                if game.lvl.mask.goal != goal:
                    game.lvl.mask.goal = goal
                else:
                    game.lvl.mask.goal = None
                    game.lvl.mask.is_path = False

        game.clock.tick(game.fps)


main()
