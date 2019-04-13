from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QWidget, QLabel


class Cell(QWidget):
    CELL_SIZE = 64
    CELL_MARGIN = 2

    ROTATE_ANGLES = dict(up=0,
                         right=90,
                         down=180,
                         left=270)

    SPRITES = dict(block='sprites/block.png',
                   empty='sprites/empty.png',
                   first_player='sprites/first_player.png',
                   second_player='sprites/second_player.png')

    cell_label = None

    def __init__(self, parent, x: int, y: int, type: str, direction: str):
        super().__init__(parent)
        self.x = x
        self.y = y
        self.type = type
        self.direction = direction
        self.init_ui()

    def init_ui(self):
        x_position = self.x * (self.CELL_SIZE + self.CELL_MARGIN)
        y_position = self.y * (self.CELL_SIZE + self.CELL_MARGIN)
        self.cell_label = QLabel(self)
        self.cell_label.setGeometry(x_position, y_position, self.CELL_SIZE, self.CELL_SIZE)
        self.draw()

    def draw(self):
        transform = QTransform()
        transform.rotate(self.ROTATE_ANGLES[self.direction])

        pixmap = QPixmap(self.SPRITES[self.type])
        pixmap = pixmap.scaled(self.CELL_SIZE, self.CELL_SIZE)
        pixmap = pixmap.transformed(transform)
        self.cell_label.setPixmap(pixmap)

    def set(self, type: str, direction: str):
        self.type = type
        self.direction = direction
        self.draw()
