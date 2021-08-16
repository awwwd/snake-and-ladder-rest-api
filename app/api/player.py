from app.crud.player import (
    get_players,
    create_players,
    get_all_players,
    delete_players
)
from app.db.mongodb import get_database, MongoClient
from app.models.player import PlayerCreate, Player
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from typing import List

router = APIRouter()


@router.get("/players/{player_id}", tags=["Player"], response_model=Player)
def get_player(
        player_id: str,
        db: MongoClient = Depends(get_database)):
    if (player := get_players(db, player_id)) is not None:
        return player

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Player {player_id} not found")


@router.delete("/players/{player_id}", tags=["Player"])
def delete_player(
        player_id: str,
        db: MongoClient = Depends(get_database)):
    if delete_players(db, player_id):
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Player {player_id} not found")


@router.get("/players", tags=["Player"], response_model=List[Player])
def get_all_player(db: MongoClient = Depends(get_database)):
    return get_all_players(db)


@router.post("/players", tags=["Player"], response_model=Player)
def create_player(
        player: PlayerCreate,
        db: MongoClient = Depends(get_database)
):
    if (all_players := get_all_players(db)) is not None:
        if player.email in (p.email for p in all_players):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"A player with email {player.email} already exists."
            )

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=create_players(db, player))

