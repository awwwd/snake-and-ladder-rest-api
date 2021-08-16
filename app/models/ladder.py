from app.models.common import MongoModel
import random


class Ladder(MongoModel):
    # Since we are expecting 10x10 board
    # Let's assume that start_pos will starts from 5 (atleast)
    start_pos: int = random.randint(5, 100 - 10)
    # Write a logic to generate end_pos so that it's not in the same row as start_pos
    end_pos: int = random.randint(((start_pos // 10) + 1) * 10 - 1, 100)
