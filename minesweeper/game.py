
from .timer import Timer
from .grid import *
from time import sleep

import sys








class Minesweepergame():
	def __init__(self, minefield):

		self.minefield = minefield

		self.clicks = 0

		self.sprites = {


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

        	'icon': pygame.image.load('minesweeper/sprites/icon.png'),

        	'shown': pygame.image.load('minesweeper/sprites/shown.jpg')

        	}



		self.screen = pygame.display.set_mode(size=(minefield.width*minefield.cell_size[0], minefield.height*minefield.cell_size[1]+30))

		pygame.display.set_caption('minesweeper')
		pygame.display.set_icon(self.sprites['icon'])


		self.timer = Timer(0)

		self.game_over = False

	
	def check_if_player_won(self):
		flagged_mines = len([cell for cell in self.minefield.cells.values() if cell.status == 'flagged' and cell.role == 'mine'])
		false_flags = len([cell for cell in self.minefield.cells.values() if cell.status == 'flagged' and cell.role != 'mine'])

		if false_flags == 0 and flagged_mines == self.minefield.mine_amount:
			self.game_over = True

			self.player_won()



	def handle_drawing(self):
		for cell in self.minefield.cells.values():
			cell.exist(self.screen)



	def on_left_click(self):
		self.clicks += 1

		pos = pygame.mouse.get_pos()

		for cell in self.minefield.cells.values():
				
			if cell.rect.collidepoint(pos):

				if self.clicks == 1:
					first_cell = cell
					self.minefield.generate_field(first_cell)

				else:

					if cell.role == 'number' and cell.status != 'flagged':
						cell.reveal(self.minefield.cells, self.sprites)

					elif cell.role == 'empty' and cell.status != 'flagged':
						self.explore(cell)

					elif cell.role == 'mine' and cell.status != 'flagged':
						self.game_over = True

						self.player_lost()



	def on_right_click(self):
		pos = pygame.mouse.get_pos()

		for cell in self.minefield.cells.values():
			if cell.rect.collidepoint(pos) and (cell.status == 'unrevealed' or cell.status == 'flagged'):
				cell.handle_flagging(self.sprites)

		sleep(0.15)




	def player_won(self):
		surface_width = self.screen.get_size()[0]

		self.screen.blit(pygame.font.SysFont('you win', 25).render("You Win!", False, GRAY), (surface_width-90, 5))

		for cell in self.minefield.cells.values():
			if cell.role == 'mine':
				cell.surface = self.sprites['shown']
				cell.exist(self.screen)


	def player_lost(self):
		surface_width = self.screen.get_size()[0]

		self.screen.blit(pygame.font.SysFont('you lose', 25).render("You Lose!", False, GRAY), (surface_width-90, 5))

		for cell in self.minefield.cells.values():
			if cell.role == 'mine':
				cell.reveal(self.minefield.cells, self.sprites)


	def explore(self, clicked_cell):

		clicked_cell.reveal(self.minefield.cells, self.sprites)
	
		starting_num = clicked_cell.num

		explored_cells = []

		for neighbour_name in clicked_cell.neighbour_names:
			explored_cells.append(self.minefield.cells[neighbour_name])

		for cell in explored_cells:
			cell.reveal(self.minefield.cells, self.sprites)



		recursiveness = 30

		for _ in range(recursiveness):

			for cell in explored_cells:

				if cell.role != 'number':
					for neighbour_name in cell.neighbour_names:
				
						neighbour_cell = self.minefield.cells[neighbour_name]

						if neighbour_cell.role != 'mine':
							explored_cells.append(neighbour_cell)

							explored_cells = list(set(explored_cells))

							neighbour_cell.reveal(self.minefield.cells, self.sprites)




	def main_loop(self):

		self.timer.start(self.screen, (0,5), 1)
		
		while not self.game_over:
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			if pygame.mouse.get_pressed()[0]:
				self.on_left_click()
			
			elif pygame.mouse.get_pressed()[2]:
				self.on_right_click()

			self.handle_drawing()

			self.check_if_player_won()


			if self.game_over:
				pygame.display.flip()
				sleep(2)

			pygame.display.flip()


