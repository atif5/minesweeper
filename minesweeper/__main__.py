

from .game import Minesweepergame, MineFieldGrid
import sys



try:
    if sys.argv[1] == '-c':

    minefield = MineFieldGrid(size=eval(sys.argv[2]), mine_amount=int(sys.argv[3]))

    if minefield.mine_amount >= minefield.cell_amount:
        print('invalid configuration!')

        sys.exit()	

except IndexError:
	minefield = MineFieldGrid()

game = Minesweepergame(minefield)

if __name__ == '__main__':
    game.main_loop()
