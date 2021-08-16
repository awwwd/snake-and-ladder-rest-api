from app.models.common import MongoModel
from app.models.ladder import Ladder
from app.models.snake import Snake
from typing import List


class Board(MongoModel):
    size: int = 10
    # Let's generate 7 - 10 snakes for the board
    # 7 being a easy game
    # 10 being a hard game
    # TODO: should be customizable
    snakes: List[Snake] = []
    # Let's generate 8 - 10 ladder for the board
    # 8 being a hard game
    # 10 being a easy game
    # TODO: should be customizable
    ladders: List[Ladder] = []
