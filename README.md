# minesweeper
a minesweeper game built with pygame

## usage
execute it as a package:

```$ python3 -m minesweeper```

this creates game session with a 8x8 minefield that has 10 bombs by default.

you can create custom minefields as well.


#### custom minefields
now you can create custom minefields, game sessions using:

```$ python3 -m minesweeper -c "(w, h)" mine_amount```

`w` and `h` being the width and height of the minefield and `mine_amount` being an `int` and well... no need for further explanation.

example:

```$ python3 -m minesweeper -c "(20, 15)" 30```

creates a minefield with the size 20x15 that has 30 mines.

## requirements
only pygame, run `pip install -r requirements.txt` to satisfy.
