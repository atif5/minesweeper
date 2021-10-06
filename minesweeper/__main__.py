# coding: utf-8

import sys

from .game import (
    Minesweepergame, MineFieldGrid)


def main():
    minefield = MineFieldGrid()

    if len(sys.argv) > 1 and sys.argv[1] in ['-c', '--custom']:
        try:
            minefield = MineFieldGrid(
                size=eval(sys.argv[2]),
                mine_amount=int(sys.argv[3]))
        except IndexError:
            exit('please specify the mine amount!')

        if minefield.mine_amount >= minefield.cell_amount - 8:
            sys.exit('invalid configuration!')

    game = Minesweepergame(minefield)
    game.main_loop()


if __name__ == '__main__':
    main()
