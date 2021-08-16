from app.models.board import Board
from app.models.common import MongoModel, PyObjectId
from datetime import datetime
from pydantic import BaseModel, conint, Field
from typing import Optional, List, Dict
import enum


class GameStatus(str, enum.Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Position(MongoModel):
    position_to: int = 0
    position_from: int = 0
    die_result: int = 0
    snake_found: bool = False
    ladder_found: bool = False


# Shared properties
class GameBase(MongoModel):
    started_by: str


# Properties to receive via API on creation
class GameCreate(GameBase):
    pass


class GameInDBBase(GameBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')
    player_ids: Optional[List[str]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    participants: conint(ge=1, le=3)
    status: GameStatus
    board: Optional[Board] = None
    moves_played: Optional[Dict[str, List[Position]]] = {}
    next_turn: Optional[str]
    won_by: Optional[str] = None


# Additional properties to return via API
class Game(GameInDBBase):
    pass


# Additional properties stored in DB
class GameInDB(GameInDBBase):
    pass


class GameJoin(BaseModel):
    joined_by: str


class GameLeft(BaseModel):
    left_by: str


class GamePlay(BaseModel):
    played_by: str


class GamePosition(MongoModel):
    next_turn: Optional[str]
    position: Optional[Position]
    status: GameStatus
    board: Optional[Board] = None
    won_by: Optional[str] = None
