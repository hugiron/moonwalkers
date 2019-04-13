from typing import Optional

from .board import Board
from .cell import Cell, CellDirection, CellType
from .player import Player, PlayerAction


class Room:
    BOARD_SIZE = 8

    SCORE_FOR_MOVE = 1
    SCORE_FOR_SHOOT = 3

    def __init__(self, id: int, first_player: Player, second_player: Player):
        self.id = id

        self.first_player = first_player
        self.first_player.x = 0
        self.first_player.y = 0
        self.first_player.is_active = True
        self.first_player.new_score()

        self.second_player = second_player
        self.second_player.x = self.BOARD_SIZE - 1
        self.second_player.y = self.BOARD_SIZE - 1
        self.second_player.is_active = False
        self.second_player.clear_score()

        self.board = Board(self.BOARD_SIZE)

    def get_player_by_id(self, player_id: int) -> Optional[Player]:
        if player_id == self.first_player.id:
            return self.first_player
        elif player_id == self.second_player.id:
            return self.second_player
        return None

    def do_action(self, player_id: int, action: str, direction: str) -> bool:
        player = self.get_player_by_id(player_id)
        if player is None or not player.is_active:
            return False

        if action == PlayerAction.MOVE:
            if player.score < self.SCORE_FOR_MOVE:
                return False
            if self.move_player(player, direction):
                player.score -= self.SCORE_FOR_MOVE
        elif action == PlayerAction.SHOOT:
            if player.score < self.SCORE_FOR_SHOOT:
                return False
            if self.shoot_player(player, direction):
                player.score -= self.SCORE_FOR_SHOOT
        elif action == PlayerAction.FINISH:
            self.change_active_player(player)

        if player.score == 0:
            self.change_active_player(player)

        return True

    def move_player(self, player: Player, direction: str) -> bool:
        new_pos_x, new_pos_y = player.x, player.y

        if direction == CellDirection.UP:
            if player.y == 0:
                return False
            new_pos_y -= 1
        elif direction == CellDirection.DOWN:
            if player.y == self.BOARD_SIZE - 1:
                return False
            new_pos_y += 1
        elif direction == CellDirection.LEFT:
            if player.x == 0:
                return False
            new_pos_x -= 1
        elif direction == CellDirection.RIGHT:
            if player.x == self.BOARD_SIZE - 1:
                return False
            new_pos_x += 1
        else:
            return False

        next_player_cell_type = self.board.get_type(new_pos_x, new_pos_y)
        if next_player_cell_type != CellType.EMPTY:
            return False

        if not (player.x == new_pos_x and player.y == new_pos_y):
            player_cell = self.board.get(player.x, player.y)
            empty_cell = Cell(player.x, player.y, CellType.EMPTY, CellDirection.UP)
            self.board.set(player.x, player.y, empty_cell)
            player.x, player.y = new_pos_x, new_pos_y
            player_cell.x, player_cell.y = new_pos_x, new_pos_y
            player_cell.direction = direction
            self.board.set(new_pos_x, new_pos_y, player_cell)

        return True

    def shoot_player(self, player: Player, direction: str) -> bool:
        step = None
        if direction == CellDirection.UP:
            if player.y == 0:
                return False
            step = (0, -1)
        elif direction == CellDirection.DOWN:
            if player.y == self.BOARD_SIZE - 1:
                return False
            step = (0, 1)
        elif direction == CellDirection.LEFT:
            if player.x == 0:
                return False
            step = (-1, 0)
        elif direction == CellDirection.RIGHT:
            if player.x == self.BOARD_SIZE - 1:
                return False
            step = (1, 0)
        else:
            return False

        bullet_x, bullet_y = player.x, player.y
        while 0 <= bullet_x < self.BOARD_SIZE and 0 <= bullet_y < self.BOARD_SIZE:
            bullet_x += step[0]
            bullet_y += step[1]
            if self.board.get_type(bullet_x, bullet_y) == CellType.EMPTY:
                continue
            target_cell = self.board.get(bullet_x, bullet_y)

            if target_cell.type == CellType.FIRST_PLAYER:
                self.first_player.is_alive = False
            elif target_cell.type == CellType.SECOND_PLAYER:
                self.second_player.is_alive = False

            new_target_cell = Cell(bullet_x, bullet_y, CellType.EMPTY, CellDirection.UP)
            self.board.set(bullet_x, bullet_y, new_target_cell)
            break

        player_cell = self.board.get(player.x, player.y)
        player_cell.direction = direction
        self.board.set(player.x, player.y, player_cell)

        return True

    def change_active_player(self, player: Player) -> None:
        another_player = self.first_player if player.id == self.second_player.id else self.second_player
        if another_player.is_alive:
            player.clear_score()
            player.is_active = False

            another_player.new_score()
            another_player.is_active = True
