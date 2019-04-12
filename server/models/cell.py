class CellType:
    EMPTY = 'empty'
    FIRST_PLAYER = 'first_player'
    SECOND_PLAYER = 'second_player'
    BLOCK = 'block'


class CellDirection:
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    @staticmethod
    def validate_direction(direction: str):
        return direction == CellDirection.UP or direction == CellDirection.DOWN or \
               direction == CellDirection.LEFT or direction == CellDirection.RIGHT


class Cell:
    def __init__(self, x: int, y: int, type: str, direction: str):
        self.x = x
        self.y = y
        self.type = type
        self.direction = direction

    def copy(self):
        return Cell(self.x, self.y, self.type, self.direction)

    def to_dict(self):
        return dict(x=self.x,
                    y=self.y,
                    type=self.type,
                    direction=self.direction)
