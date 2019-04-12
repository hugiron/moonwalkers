import asyncio
from queue import Queue

import aiohttp
import aiohttp.web
import ujson as json

from models import Player, PlayerAction, Room, CellType, CellDirection


class GameController:
    NEXT_PLAYER_ID = 1
    NEXT_ROOM_ID = 1

    def __init__(self):
        self.waiting_players = Queue()
        self.players = dict()
        self.rooms = dict()

    async def ws_handler(self, request):
        ws = aiohttp.web.WebSocketResponse()
        await ws.prepare(request)

        player = Player(self.NEXT_PLAYER_ID, ws)
        self.NEXT_PLAYER_ID += 1
        self.waiting_players.put(player)
        self.players[player.id] = player

        if self.waiting_players.qsize() > 1:
            await self.create_room(self.waiting_players.get(), self.waiting_players.get())

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                if self.validate_message(data):
                    player.room.do_action(player.id, data['action'], data['direction'])
                    await self.send_last_changes(player.room)
                    await self.send_players_info(player.room)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                # TODO: Delete room and players
                pass

        return ws

    async def create_room(self, first_player, second_player):
        first_player.name = CellType.FIRST_PLAYER
        second_player.name = CellType.SECOND_PLAYER

        room = Room(self.NEXT_ROOM_ID, first_player, second_player)
        self.NEXT_ROOM_ID += 1
        self.rooms[room.id] = room

        first_player.room = room
        second_player.room = room

        await self.send_last_changes(room)
        await self.send_players_info(room)

    async def send_players_info(self, room: Room) -> None:
        first_player_info = room.first_player.to_dict()
        second_player_info = room.second_player.to_dict()
        first_player_msg = json.dumps({
            'personal': first_player_info,
            'enemy': second_player_info
        })
        second_player_msg = json.dumps({
            'personal': second_player_info,
            'enemy': first_player_info
        })
        broadcast = [room.first_player.ws.send_str(first_player_msg),
                     room.second_player.ws.send_str(second_player_msg)]
        await asyncio.wait(broadcast)

    async def send_last_changes(self, room: Room) -> None:
        last_changes = room.board.get_last_changes()
        serialized_changes = json.dumps([cell.to_dict() for cell in last_changes])
        broadcast = [room.first_player.ws.send_str(serialized_changes),
                     room.second_player.ws.send_str(serialized_changes)]
        await asyncio.wait(broadcast)

    def validate_message(self, data: dict) -> bool:
        action = data.get('action')
        direction = data.get('direction')
        return PlayerAction.validate_action(action) and CellDirection.validate_direction(direction)
