from app.core.config import database_name, player_collection, logger
from app.db.mongodb import MongoClient
from app.models.player import PlayerInDBBase, Player, PlayerCreate
from bson import ObjectId, errors
from fastapi.encoders import jsonable_encoder
from typing import List, Optional


def create_players(conn: MongoClient, player: PlayerCreate) -> Player:
    new_player = conn[database_name][player_collection].insert_one(jsonable_encoder(PlayerInDBBase(**player.dict())))
    created_player = conn[database_name][player_collection].find_one({"_id": f"{ObjectId(new_player.inserted_id)}"})
    return created_player


def get_players(conn: MongoClient, player_id: str) -> Optional[Player]:
    collection = conn[database_name][player_collection]

    try:
        if (row := collection.find_one({"_id": f"{ObjectId(player_id)}"})) is not None:
            return Player(**row)
    except errors.InvalidId:
        logger.info(f"Invalid bson id provided {player_id}")

    return None


def delete_players(conn: MongoClient, player_id: str) -> str:
    try:
        row = conn[database_name][player_collection].delete_one({"_id": f"{ObjectId(player_id)}"})
        if row.deleted_count == 1:
            return True
    except errors.InvalidId:
        logger.info(f"Invalid bson id provided {player_id}")

    return False


def get_all_players(conn: MongoClient) -> List[Player]:
    row = conn[database_name][player_collection].find()
    row_list = []
    for each_player in row:
        row_list.append(Player(**each_player))
    return row_list
