from aiohttp.web import route

from game_controller import GameController

game_controller = GameController()

ROUTES = [
    route('GET', r'/ws', game_controller.ws_handler)
]
