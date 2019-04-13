import random
from typing import Optional, List

from .cell import Cell, CellDirection, CellType


class Board:
    MIN_PART_OF_BLOCKS = 0.3
    MAX_PART_OF_BLOCKS = 0.6

    def __init__(self, size: int):
        self.size = size

        self.board = [[Cell(x, y, CellType.EMPTY, CellDirection.UP) for x in range(size)] for y in range(size)]

        min_block_count = int(self.MIN_PART_OF_BLOCKS * size * size)
        max_block_count = int(self.MAX_PART_OF_BLOCKS * size * size)
        block_count = random.randint(min_block_count, max_block_count)
        blocks = [1] * block_count + [0] * (size * size - block_count)
        random.shuffle(blocks)
        for i, value in enumerate(blocks):
            if value:
                block_y = i // size
                block_x = i % size
                self.board[block_y][block_x].type = CellType.BLOCK

        self.board[0][0].type = CellType.FIRST_PLAYER
        self.board[0][0].direction = CellDirection.DOWN

        self.board[-1][-1].type = CellType.SECOND_PLAYER
        self.board[-1][-1].direction = CellDirection.UP

        self.last_changes = [self.board[y][x] for x in range(size) for y in range(size)]

    def get(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.board[y][x].copy()
        return None

    def get_type(self, x: int, y: int) -> Optional[str]:
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.board[y][x].type
        return None

    def set(self, x: int, y: int, cell: Cell) -> None:
        if 0 <= x < self.size and 0 <= y < self.size:
            self.board[y][x] = cell
            self.last_changes.append(cell)

    def get_last_changes(self) -> List[Cell]:
        temp_list_of_changes = self.last_changes
        self.last_changes = []
        return temp_list_of_changes
