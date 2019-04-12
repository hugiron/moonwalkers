import random
from typing import Optional


class PlayerAction:
    MOVE = 'move'
    SHOOT = 'shoot'
    FINISH = 'finish'

    @staticmethod
    def validate_action(action: str):
        return action == PlayerAction.MOVE or action == PlayerAction.SHOOT or action == PlayerAction.FINISH


class Player:
    MIN_SCORE = 1
    MAX_SCORE = 6

    def __init__(self,
                 id: int,
                 ws,
                 x: int = 0,
                 y: int = 0,
                 score: int = 0,
                 is_active: bool = False,
                 name: Optional[str] = None,
                 room=None):
        self.id = id
        self.ws = ws
        self.x = x
        self.y = y
        self.score = score
        self.is_active = is_active
        self.is_alive = True
        self.name = name
        self.room = room

    def new_score(self):
        self.score = random.randint(self.MIN_SCORE, self.MAX_SCORE)

    def clear_score(self):
        self.score = 0

    def to_dict(self):
        return dict(id=self.id,
                    name=self.name,
                    score=self.score,
                    is_alive = self.is_alive,
                    is_active=self.is_active,
                    room_id=self.room.id)
