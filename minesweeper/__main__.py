# coding: utf-8

import sys

from .game import (
    Minesweepergame, MineFieldGrid)


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ['-c', '--custom']:
        try:
            x = int(sys.argv[2])
            y = int(sys.argv[3])
            mines = int(sys.argv[4])

        except IndexError:
            sys.exit('please specify the mine amount!')

        if x > 38 or y > 19:
            det = max(x, y)
            minefield = MineFieldGrid(
                size=(x, y),
                mine_amount=mines, cell_size=(int((9/det)*110), int((9/det)*110)))

        else:
            minefield = MineFieldGrid(
                size=(x, y),
                mine_amount=mines)

        if minefield.mine_amount >= minefield.cell_amount - 8:
            sys.exit('invalid configuration!')

    else:
        minefield = MineFieldGrid()

    game = Minesweepergame(minefield)
    game.main_loop()


if __name__ == '__main__':
    main()
