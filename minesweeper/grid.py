# coding: utf-8

import random
import pygame

RED  = (255,   0,   0)
GRAY = (171, 174, 171)

class Cell():
    def __init__(self, status, role, num, grid, size=(50, 50)):
        self.name = f"cell{num}"

        self.num = num
        self.role = role
        self.size = size
        self.status = status

        self.surface = pygame.Surface(self.size)
        self.surface.fill(GRAY)

        self.position = (
            self.size[0] * (self.num %  grid.width),
            self.size[0] * (self.num // grid.width) + 30)

        self.rect = self.surface.get_rect()
        self.rect.move_ip(self.position)

        self.handle_neighbours(grid)

    def handle_neighbours(self, grid):

        if self.num % grid.width == 0:
            self.is_side_cell = 'left'

        elif (self.num + 1) % grid.width == 0:
            self.is_side_cell = 'right'

        else:
            self.is_side_cell = False

        if self.is_side_cell == 'left':
            neighbour_nums = [
                self.num - grid.width,
                self.num - grid.width + 1,
                self.num + 1,
                self.num + grid.width,
                self.num + grid.width + 1]

        elif self.is_side_cell == 'right':
            neighbour_nums = [
                self.num + grid.width,
                self.num + grid.width - 1,
                self.num - 1,
                self.num - grid.width - 1,
                self.num - grid.width]

        else:
            neighbour_nums = [
                self.num - grid.width - 1,
                self.num - grid.width,
                self.num - grid.width + 1,
                self.num + 1,
                self.num + grid.width + 1,
                self.num + grid.width,
                self.num + grid.width - 1,
                self.num - 1]

        self.neighbour_names = [
            f"cell{i}" for i in neighbour_nums if i > -1 and i < grid.cell_amount]

    def exist(self, surface):
        surface.blit(self.surface, self.position)
        pygame.draw.rect(surface, RED, self.rect, width=3)

    def reveal(self, cells, sprites):
        self.status = 'revealed'

        if self.role == 'mine':
            self.surface = sprites['mine']

        elif self.role == 'number':
            mine_neighbours = [
                cells[neighbour_name]
                for neighbour_name in self.neighbour_names
                if cells[neighbour_name].role == 'mine']

            self.surface = sprites[str(len(mine_neighbours))]

        elif self.role == 'empty':
            self.surface = sprites['empty']

    def handle_flagging(self, sprites):
        if self.status != 'flagged':
            self.status = 'flagged'
            self.surface = sprites['flag']

        else:
            self.status = 'unrevealed'
            self.surface = pygame.Surface(self.size)
            self.surface.fill(GRAY)


class MineFieldGrid():
    def __init__(self, size=(8, 8), cell_size=(50, 50), mine_amount=10):
        self.size = size
        self.cell_size = cell_size
        self.mine_amount = mine_amount

        self.width, self.height = size[0], size[1]
        self.cell_amount = self.height*self.width

        self.cells = {
            f"cell{i}": Cell(
                status = 'unrevealed',
                role   = None,
                num    = i,
                grid   = self,
                size   = cell_size) for i in range(self.cell_amount)}

    def generate_field(self, starting_cell):
        ints_to_choose = list(range(self.cell_amount))
        ints_to_choose.remove(starting_cell.num)

        for neighbour_name in starting_cell.neighbour_names:
            ints_to_choose.remove(self.cells[neighbour_name].num)

        try:
            rand_ints = random.sample(ints_to_choose, self.mine_amount)
        except ValueError:
            print('invalid configuration!')
            exit()

        for cell in self.cells.values():
            if cell.num in rand_ints:
                cell.role = 'mine'

        for cell in self.cells.values():
            if cell.role != 'mine':
                for neighbour_name in cell.neighbour_names:
                    if self.cells[neighbour_name].role == 'mine':
                        cell.role = 'number'

        for cell in self.cells.values():
            if cell.role != 'mine' and cell.role != 'number':
                cell.role = 'empty'