# coding: utf-8

import time
import pygame

from .grid import (
    Cell, MineFieldGrid, RED, GRAY)
from .timer import Timer

class Minesweepergame:
    pygame.font.init()

    font    = pygame.font.SysFont('mainfont', 25)
    sprites = {
        '1': pygame.image.load('minesweeper/sprites/1.jpg'),
        '2': pygame.image.load('minesweeper/sprites/2.jpg'),
        '3': pygame.image.load('minesweeper/sprites/3.jpg'),
        '4': pygame.image.load('minesweeper/sprites/4.jpg'),
        '5': pygame.image.load('minesweeper/sprites/5.jpg'),
        '6': pygame.image.load('minesweeper/sprites/6.jpg'),
        '7': pygame.image.load('minesweeper/sprites/7.jpg'),
        '8': pygame.image.load('minesweeper/sprites/8.jpg'),

        'mine' : pygame.image.load('minesweeper/sprites/mine.png'),
        'empty': pygame.image.load('minesweeper/sprites/empty.png'),
        'flag' : pygame.image.load('minesweeper/sprites/flag.png'),
        'icon' : pygame.image.load('minesweeper/sprites/icon.png'),
        'shown': pygame.image.load('minesweeper/sprites/shown.jpg')}

    def __init__(self, minefield):
        self.clicks = 0
        self.minefield = minefield

        self.timer = Timer(0, self.font)
        self.game_over = False

        pygame.display.set_caption('minesweeper')
        pygame.display.set_icon(self.sprites['icon'])

        self.screen = pygame.display.set_mode((
            minefield.width * minefield.cell_size[0],
            minefield.height * minefield.cell_size[1] + 30))

    def check_if_player_won(self):
        flagged_mines = sum([
            1 for cell in self.minefield.cells.values()
            if cell.status == 'flagged' and cell.role == 'mine'])
        false_flags = sum([
            1 for cell in self.minefield.cells.values()
            if cell.status == 'flagged' and cell.role != 'mine'])

        if false_flags == 0 and flagged_mines == self.minefield.mine_amount:
            self.game_over = True
            self.player_won()

    def handle_drawing(self):
        for cell in self.minefield.cells.values():
            cell.exist(self.screen)

    def on_left_click(self):
        self.clicks += 1
        mouse_pos = pygame.mouse.get_pos()

        for cell in self.minefield.cells.values():
            if cell.rect.collidepoint(mouse_pos):
                if self.clicks == 1:
                    first_cell = cell
                    self.minefield.generate_field(first_cell)
                    continue

                if cell.role == 'number' and cell.status != 'flagged':
                    cell.reveal(self.minefield.cells, self.sprites)

                elif cell.role == 'empty' and cell.status != 'flagged':
                    self.explore(cell)

                elif cell.role == 'mine' and cell.status != 'flagged':
                    self.game_over = True
                    self.player_lost()


    def on_right_click(self):
        mouse_pos = pygame.mouse.get_pos()

        for cell in self.minefield.cells.values():
            if not cell.rect.collidepoint(mouse_pos):
                continue

            if cell.status == 'unrevealed' or cell.status == 'flagged':
                cell.handle_flagging(self.sprites)

        time.sleep(0.15)

    def player_won(self):
        surface_width = self.screen.get_size()[0]

        text = self.font.render("You Win!", False, GRAY)
        self.screen.blit(text, (surface_width - 90, 5))

        for cell in self.minefield.cells.values():
            if cell.role == 'mine':
                cell.surface = self.sprites['shown']
                cell.exist(self.screen)

    def player_lost(self):
        surface_width = self.screen.get_size()[0]

        text = self.font.render("You Lose!", False, GRAY)
        self.screen.blit(text, (surface_width - 90, 5))

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

        for _ in range(30): # recursiveness
            for cell in explored_cells:
                if cell.role == 'number':
                    continue

                for neighbour_name in cell.neighbour_names:
                    neighbour_cell = self.minefield.cells[neighbour_name]

                    if neighbour_cell.role == 'mine':
                        continue

                    explored_cells.append(neighbour_cell)
                    explored_cells = list(set(explored_cells))
                    neighbour_cell.reveal(self.minefield.cells, self.sprites)

    def main_loop(self):
        self.timer.start(self.screen, (0,5), 1)

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(pygame.quit() or 0)

            if pygame.mouse.get_pressed()[0]:
                self.on_left_click()

            elif pygame.mouse.get_pressed()[2]:
                self.on_right_click()

            self.handle_drawing()
            self.check_if_player_won()

            pygame.display.flip()

        pygame.display.flip()
        time.sleep(2)