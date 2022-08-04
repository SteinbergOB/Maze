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

        game.clock.tick(game.fps)


main()
