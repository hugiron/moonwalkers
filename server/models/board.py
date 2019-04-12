import random
from typing import Optional, List

from .cell import Cell, CellDirection, CellType


class Board:
    MIN_PART_OF_BLOCKS = 0.1
    MAX_PART_OF_BLOCKS = 0.5

    def __init__(self, size: int):
        self.size = size
        self.min_block_count = int(self.MIN_PART_OF_BLOCKS * size * size)
        self.max_block_count = int(self.MAX_PART_OF_BLOCKS * size * size)

        self.board = [[Cell(x, y, CellType.EMPTY, CellDirection.UP) for x in range(size)] for y in range(size)]

        self.board[0][0].type = CellType.FIRST_PLAYER
        self.board[0][0].direction = CellDirection.DOWN

        self.board[-1][-1].type = CellType.SECOND_PLAYER
        self.board[-1][-1].direction = CellDirection.UP

        block_count = random.randint(self.min_block_count, self.max_block_count)
        block_positions = set()
        while len(block_positions) < block_count:
            block_position = (random.randint(0, size - 1), random.randint(0, size - 1))
            if block_position != (0, 0) and block_position != (size - 1, size - 1):
                block_positions.add(block_position)

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
