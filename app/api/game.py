from app.crud.game import (
    get_games,
    create_games,
    join_games,
    get_all_games,
    play_games,
    delete_games,
    leave_games
)
from fastapi import APIRouter, Depends, Body, HTTPException, status
from fastapi.responses import JSONResponse
from app.db.mongodb import get_database, MongoClient
from app.models.game import GameCreate, GameJoin, GamePlay, GameInDBBase, GameLeft
from typing import List

router = APIRouter()


@router.get("/games/{game_id}", tags=["Games"])
def get_game(
        game_id: str,
        db: MongoClient = Depends(get_database)):
    if game := get_games(db, game_id) is not None:
        return game

    raise HTTPException(status_code=404, detail=f"Player {game_id} not found")


@router.get("/games", tags=["Games"], response_model=List[GameInDBBase])
def get_all_game(db: MongoClient = Depends(get_database)):
    return get_all_games(db)


@router.delete("/games/{game_id}", tags=["Games"])
def delete_player(
        game_id: str,
        db: MongoClient = Depends(get_database)):
    if delete_games(db, game_id):
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Game with {game_id} not found")


@router.post("/games", tags=["Games"])
def create_game(
        game: GameCreate = Body(...),
        db: MongoClient = Depends(get_database)
):
    if (created_game := create_games(db, game)) is not None:
        return created_game

    raise HTTPException(status_code=404, detail=f"Player {game.started_by} not found")


@router.post("/games/{game_id}/join", tags=["JoinGames"])
def join_game(
        game_id,
        game: GameJoin = Body(...),
        db: MongoClient = Depends(get_database)
):
    return join_games(db, game_id, game)


@router.delete("/games/{game_id}/join", tags=["JoinGames"])
def leave_game(
        game_id,
        game: GameLeft = Body(...),
        db: MongoClient = Depends(get_database)
):
    return leave_games(db, game_id, game)


@router.post("/games/{game_id}/play", tags=["PlayGames"])
def play_game(
        game_id,
        game: GamePlay,
        db: MongoClient = Depends(get_database)
):
    return play_games(db, game_id, game)
