from app.models.common import MongoModel, PyObjectId
from pydantic import EmailStr, Field
from typing import Optional


# Shared properties
class PlayerBase(MongoModel):
    username: str
    email: Optional[EmailStr]


# Properties to receive via API on creation
class PlayerCreate(PlayerBase):
    email: EmailStr


# Properties to receive via API on update
class PlayerUpdate(PlayerBase):
    name: Optional[str] = None


class PlayerInDBBase(PlayerBase):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias='_id')


# Additional properties to return via API
class Player(PlayerInDBBase):
    pass


# Additional properties stored in DB
class PlayerInDB(PlayerInDBBase):
    # hashed_password: str
    pass
