from PyQt5.QtCore import *
from PyQt5.QtWebSockets import *
import ujson as json

from .message import ChangedCell, Player, PlayerInfo


class WebSocketClient(QObject):
    def __init__(self, parent, url: str, on_connect=None, on_receive_player_info=None, on_receive_changes=None):
        super().__init__(parent)

        self.client = QWebSocket("", QWebSocketProtocol.VersionLatest, None)

        self.client.error.connect(self.on_error)
        self.client.textMessageReceived.connect(self.on_receive_message)
        if callable(on_connect):
            self.client.connected.connect(on_connect)

        self.on_receive_player_info = on_receive_player_info
        self.on_receive_changes = on_receive_changes

        self.client.open(QUrl(url))

    def on_error(self, error_code):
        print("error code: {}".format(error_code))
        print(self.client.errorString())

    def on_receive_message(self, p_str: str):
        data = json.loads(p_str)
        if type(data) == dict:
            if callable(self.on_receive_player_info):
                personal_player = Player(**data['personal'])
                enemy_player = Player(**data['enemy'])
                player_info = PlayerInfo(personal_player, enemy_player)
                self.on_receive_player_info(player_info)
        elif type(data) == list:
            if callable(self.on_receive_changes):
                changed_cells = [ChangedCell(**cell) for cell in data]
                self.on_receive_changes(changed_cells)

    def send(self, action: str, direction: str):
        msg = dict(action=action,
                   direction=direction)
        self.client.sendTextMessage(json.dumps(msg))

    def close(self):
        self.client.close()
