from PyQt5.QtWidgets import *

from .cell import Cell
from .message import ChangedCell


class Board(QWidget):
    board = None

    def __init__(self, parent, size: int):
        super().__init__(parent)
        self.size = size
        self.init_ui()

    def init_ui(self):
        self.board = [[Cell(self, x, y, 'empty', 'up') for x in range(self.size)] for y in range(self.size)]
        board_size = self.size * (Cell.CELL_SIZE + Cell.CELL_MARGIN)
        self.setFixedSize(board_size, board_size)

    def change_cell(self, changed_cell: ChangedCell):
        self.board[changed_cell.y][changed_cell.x].set(changed_cell.type, changed_cell.direction)
