

from .grid import *
from time import sleep

import sys



sprites = {


        'mine': pygame.image.load('minesweeper/sprites/mine.png'), 

        'empty': pygame.image.load('minesweeper/sprites/empty.png'),

        'flag': pygame.image.load('minesweeper/sprites/flag.png'),

        '1': pygame.image.load('minesweeper/sprites/1.jpg'), 
        '2': pygame.image.load('minesweeper/sprites/2.jpg'), 
        '3': pygame.image.load('minesweeper/sprites/3.jpg'),
        '4': pygame.image.load('minesweeper/sprites/4.jpg'),
        '5': pygame.image.load('minesweeper/sprites/5.jpg'),
        '6': pygame.image.load('minesweeper/sprites/6.jpg'),
        '7': pygame.image.load('minesweeper/sprites/7.jpg'),
        '8': pygame.image.load('minesweeper/sprites/8.jpg'),

        'icon': pygame.image.load('minesweeper/sprites/icon.png')

        }




minefield = MineFieldGrid()

screen = pygame.display.set_mode(size=(minefield.size[0]*minefield.cell_size[0], minefield.size[1]*minefield.cell_size[1]))

pygame.display.set_caption('minesweeper')
pygame.display.set_icon(sprites['icon'])

def explore(starting_cell, grid):

	starting_cell.reveal(grid.cells, sprites)
	
	starting_num = starting_cell.num

	explored_cells = []

	for neighbour_name in starting_cell.neighbour_names:
		explored_cells.append(grid.cells[neighbour_name])



	recursiveness = 100

	for _ in range(recursiveness):

		for cell in explored_cells:

			if cell.role != 'number':
				for neighbour_name in cell.neighbour_names:
				
					neighbour_cell = grid.cells[neighbour_name]

					if neighbour_cell.role != 'mine':
						explored_cells.append(neighbour_cell)

						explored_cells = list(set(explored_cells))

						neighbour_cell.reveal(grid.cells, sprites)
















def game():

	clicks = 0


	game_over = False

	while not game_over:

		for event in pygame.event.get():
			pass

		
		if pygame.mouse.get_pressed()[0]:

			clicks += 1

			pos = pygame.mouse.get_pos()

			for cell in minefield.cells.values():
				
				if cell.rect.collidepoint(pos):

					if clicks == 1:
						first_cell = cell
						minefield.generate_field(first_cell)

					else:

						if cell.role == 'number' and cell.status != 'flagged':
							cell.reveal(minefield.cells, sprites)

						elif cell.role == 'empty' and cell.status != 'flagged':
							explore(cell, minefield)

						elif cell.role == 'mine' and cell.status != 'flagged':
							game_over = True

							for cell in minefield.cells.values():
								if cell.role == 'mine':
									cell.reveal(minefield.cells, sprites)

		

		elif pygame.mouse.get_pressed()[2]:
			pos = pygame.mouse.get_pos()

			for cell in minefield.cells.values():
				if cell.rect.collidepoint(pos) and (cell.status == 'unrevealed' or cell.status == 'flagged'):
					cell.handle_flagging(sprites)

					sleep(0.15)





		
		for cell in minefield.cells.values():
			cell.exist(screen)

		if game_over:
			pygame.display.flip()
			sleep(2)


		pygame.display.flip()	
