class Player:
    def __init__(self, id: int, name: str, score: int, is_alive: bool, is_active: bool, room_id: int):
        self.id = id
        self.name = name
        self.score = score
        self.is_alive = is_alive
        self.is_active = is_active
        self.room_id = room_id


class PlayerInfo:
    def __init__(self, personal: Player, enemy: Player):
        self.personal = personal
        self.enemy = enemy
