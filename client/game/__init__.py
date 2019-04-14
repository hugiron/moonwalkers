from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from .board import Board
from .info_panel import InfoPanel
from .websocket import WebSocketClient
from .message import ChangedCell, PlayerInfo


class Game(QWidget):
    BOARD_SIZE = 8
    WS_URL = "ws://188.246.227.39:9090/ws"

    CONTROL_ACTION = {
        Qt.Key_W: 'move',
        Qt.Key_S: 'move',
        Qt.Key_D: 'move',
        Qt.Key_A: 'move',
        Qt.Key_Up: 'shoot',
        Qt.Key_Down: 'shoot',
        Qt.Key_Right: 'shoot',
        Qt.Key_Left: 'shoot',
        Qt.Key_Space: 'finish'
    }

    CONTROL_DIRECTION = {
        Qt.Key_W: 'up',
        Qt.Key_S: 'down',
        Qt.Key_D: 'right',
        Qt.Key_A: 'left',
        Qt.Key_Up: 'up',
        Qt.Key_Down: 'down',
        Qt.Key_Right: 'right',
        Qt.Key_Left: 'left',
        Qt.Key_Space: 'up'
    }

    ws_client = None
    board = None
    info_panel = None

    def __init__(self):
        super().__init__()
        self.init_connection()
        self.init_ui()

    def init_ui(self):
        hbox = QHBoxLayout()

        self.board = Board(self, size=self.BOARD_SIZE)
        hbox.addWidget(self.board)

        self.info_panel = InfoPanel(self, on_new_game=self.init_connection)
        hbox.addWidget(self.info_panel)

        self.setLayout(hbox)
        self.show()

    def init_connection(self) -> None:
        if self.ws_client is not None:
            self.ws_client.close()
        self.ws_client = WebSocketClient(self,
                                         url=self.WS_URL,
                                         on_receive_changes=self.on_receive_changes,
                                         on_receive_player_info=self.on_receive_player_info)

    def on_receive_player_info(self, player_info: PlayerInfo) -> None:
        if self.info_panel:
            self.info_panel.set_personal_info(player_info.personal)
            self.info_panel.set_enemy_info(player_info.enemy)
            if not (player_info.personal.is_alive and player_info.enemy.is_alive):
                self.ws_client.close()
                self.ws_client = None

    def on_receive_changes(self, changed_cells: List[ChangedCell]) -> None:
        if self.board:
            for changed_cell in changed_cells:
                self.board.change_cell(changed_cell)

    def keyReleaseEvent(self, event):
        if self.ws_client:
            key = event.key()
            action = self.CONTROL_ACTION.get(key)
            direction = self.CONTROL_DIRECTION.get(key)
            if action is not None and direction is not None:
                self.ws_client.send(action, direction)
        event.accept()
