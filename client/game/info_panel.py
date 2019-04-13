from PyQt5.QtWidgets import *

from .message import Player


class PlayerStats(QWidget):
    player_name = None
    player_score = None
    player_status = None

    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.player_name = QLabel(self)
        self.player_score = QLabel(self)
        self.player_score.move(0, 24)
        self.player_status = QLabel(self)
        self.player_status.move(0, 48)

    def set_player_name(self, name: str, color: str):
        self.player_name.setText(name)
        self.player_name.setStyleSheet('color: "{color}";'.format(color=color))
        self.player_name.adjustSize()

    def set_player_score(self, score: int):
        self.player_score.setText('Score: {}'.format(score))
        self.player_score.adjustSize()

    def set_player_status(self, status: str, color: str):
        self.player_status.setText('Status: {}'.format(status))
        self.player_status.setStyleSheet('color: "{color}";'.format(color=color))
        self.player_status.adjustSize()


class InfoPanel(QWidget):
    personal = None
    enemy = None

    PLAYER_NAMES = dict(first_player='Player 1',
                        second_player='Player 2')

    PLAYER_COLORS = dict(first_player='blue',
                         second_player='red')

    def __init__(self, parent, on_new_game=None):
        super().__init__(parent)
        self.on_new_game = on_new_game
        self.init_ui()

    def init_ui(self):
        vbox = QVBoxLayout()

        self.personal = PlayerStats(self)
        vbox.addWidget(self.personal)

        self.enemy = PlayerStats(self)
        vbox.addWidget(self.enemy)

        if callable(self.on_new_game):
            new_game_button = QPushButton('New game', self)
            new_game_button.clicked.connect(self.on_new_game)
            vbox.addWidget(new_game_button)

        self.setLayout(vbox)
        self.setFixedWidth(250)

    def set_personal_info(self, player: Player):
        player_status = 'ACTIVE' if player.is_active else 'WAIT'
        self.personal.set_player_status(player_status, 'black')

        self.personal.set_player_name('You: {}'.format(self.PLAYER_NAMES[player.name]), self.PLAYER_COLORS[player.name])
        self.personal.set_player_score(player.score)

        if not player.is_alive:
            self.lose()

    def set_enemy_info(self, player: Player):
        player_status = 'ACTIVE' if player.is_active else 'WAIT'
        self.enemy.set_player_status(player_status, 'black')

        self.enemy.set_player_name('You: {}'.format(self.PLAYER_NAMES[player.name]), self.PLAYER_COLORS[player.name])
        self.enemy.set_player_score(player.score)

        if not player.is_alive:
            self.win()

    def lose(self):
        self.personal.set_player_status('LOSE', 'red')
        self.enemy.set_player_status('WIN', 'green')

    def win(self):
        self.enemy.set_player_status('LOSE', 'red')
        self.personal.set_player_status('WIN', 'green')
