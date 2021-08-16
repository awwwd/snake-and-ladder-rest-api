from app.models.common import BaseModel


class Snake(BaseModel):
    # Since we are expecting 10x10 board
    # Let's fix the head position of a snake can not be the first row
    # hence head_pos starts from 11
    head_pos: int
    # Write a logic to generate tail_pos so that it's not in the same row as head
    tail_pos: int
