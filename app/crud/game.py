from app.core.config import database_name, game_collection, logger
from app.crud.player import get_players
from app.db.mongodb import MongoClient
from app.models.board import Board
from app.models.dice import Dice
from app.models.game import (
    GameInDBBase,
    GameCreate,
    GameStatus,
    Game,
    Position,
    GamePosition
)
from app.models.ladder import Ladder
from app.models.snake import Snake
from bson import ObjectId, errors
from datetime import datetime
from fastapi import status, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List, Optional, Set
import random


def _get_players_in_game(conn: MongoClient) -> Set[str]:
    all_games = get_all_games(conn)
    all_players = set()
    for games in all_games:
        all_players.add(games.started_by)
        for joined_by in games.player_ids:
            all_players.add(joined_by)

    return all_players


def create_games(conn: MongoClient, game: GameCreate) -> Optional[Game]:
    # check if player exits
    player_id = game.started_by
    if get_players(conn, player_id) is None:
        logger.info(f"Invalid player provided {player_id}")
        return None
    elif player_id in _get_players_in_game(conn):
        logger.info(f"Player {player_id} already in a game")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Player {player_id} already in a game"
        )

    new_game = conn[database_name][game_collection].insert_one(jsonable_encoder(GameInDBBase(
        **game.dict(),
        status=GameStatus.CREATED.value,
        participants=1,
        player_ids=[game.started_by]
    )))
    created_game = conn[database_name][game_collection].find_one({"_id": f"{ObjectId(new_game.inserted_id)}"})
    return GameInDBBase(**created_game)


def get_games(conn: MongoClient, game_id: str) -> Optional[Game]:
    try:
        row = conn[database_name][game_collection].find_one({"_id": f"{ObjectId(game_id)}"})
        return GameInDBBase(**row)
    except errors.InvalidId:
        logger.info(f"Invalid bson id provided {game_id}")

    return None


def delete_games(conn: MongoClient, game_id: str) -> str:
    try:
        row = conn[database_name][game_collection].delete_one({"_id": f"{ObjectId(game_id)}"})
        if row.deleted_count == 1:
            return True
    except errors.InvalidId:
        logger.info(f"Invalid bson id provided {game_id}")

    return False


def get_all_games(conn: MongoClient) -> List[Game]:
    row = conn[database_name][game_collection].find()
    row_list = []
    for each_game in row:
        # board_obj = Board(**each_game['each_game'])
        row_list.append(GameInDBBase(**each_game))
    return row_list


def join_games(conn: MongoClient, game_id, game) -> Game:
    dbgame = get_games(conn, game_id)
    if dbgame.status == GameStatus.CREATED:
        if game.joined_by not in dbgame.player_ids:
            dbgame.player_ids.append(game.joined_by)
            dbgame.participants += 1
            row = conn[database_name][game_collection].update_one(
                {"_id": f"{ObjectId(game_id)}"},
                {'$set': jsonable_encoder(dbgame)}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Player {game.joined_by} already in the game"
            )
    return dbgame


def leave_games(conn: MongoClient, game_id, game) -> Game:
    dbgame = get_games(conn, game_id)
    if dbgame.status == GameStatus.CREATED:
        if game.left_by in dbgame.player_ids:
            dbgame.player_ids.remove(game.left_by)
            dbgame.participants -= 1
            row = conn[database_name][game_collection].update_one(
                {"_id": f"{ObjectId(game_id)}"},
                {'$set': jsonable_encoder(dbgame)}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Player {game.left_by} already left the game"
            )
    return dbgame


def _generate_board():
    # The tail of a snake should not have a ladder start
    # The end of ladder should not have a snake head
    snakes = []

    # Using set or HashSet for O(1) checks
    snake_head = set()
    snake_tail = set()
    for _ in range(random.randint(7, 10)):
        head_pos = random.randint(11, 10 * 10)
        snake_head.add(head_pos)
        tail_pos = random.randint(5, (head_pos // 10) * 10 - 1)
        snake_tail.add(tail_pos)
        snakes.append(Snake(head_pos=head_pos, tail_pos=tail_pos))

    ladders = []
    for _ in range(random.randint(8, 10)):
        max_try = 0
        while True:
            start_pos = random.randint(5, 100 - 10)
            if start_pos not in snake_tail or max_try <= 100:
                max_try += 1
                break

        max_try = 0
        while True:
            end_pos = random.randint(((start_pos // 10) + 1) * 10 - 1, 100)
            if end_pos not in snake_head or max_try <= 100:
                max_try += 1
                break

        ladders.append(Ladder(start_pos=start_pos, end_pos=end_pos))

    return Board(size=10, snakes=snakes, ladders=ladders)


def _if_snake_found_then(snakes: List[Snake], curr_position: Position) -> Position:
    for each_snake_pos in snakes:
        if each_snake_pos.head_pos == curr_position.position_to:
            return Position(
                position_to=each_snake_pos.tail_pos,
                position_from=curr_position.position_from,
                die_result=curr_position.die_result,
                snake_found=True,
                ladder_found=False
            )

    return curr_position


def _if_ladder_found_then(ladders: List[Ladder], curr_position: Position) -> Position:
    for each_ladder_pos in ladders:
        if each_ladder_pos.start_pos == curr_position.position_to:
            return Position(
                position_to=each_ladder_pos.end_pos,
                position_from=curr_position.position_from,
                die_result=curr_position.die_result,
                snake_found=False,
                ladder_found=True
            )

    return curr_position


def play_games(conn: MongoClient, game_id, player) -> GamePosition:
    dbgame = get_games(conn, game_id)
    final_eval_position = None
    if dbgame.status == GameStatus.CREATED:
        dbgame.status = GameStatus.IN_PROGRESS
        dbgame.started_at = datetime.utcnow()
        random_player = random.choice(
            [p for p in dbgame.player_ids if p != player.played_by])
        dbgame.next_turn = random_player
        dbgame.board = _generate_board()
        die_face = Dice.roll()
        new_position = Position(
            position_to=die_face,
            position_from=0,
            die_result=die_face
        )

        eval_position = _if_snake_found_then(dbgame.board.snakes, new_position)
        final_eval_position = _if_ladder_found_then(dbgame.board.ladders, eval_position)

        dbgame.moves_played[player.played_by] = [final_eval_position]

    elif dbgame.status == GameStatus.IN_PROGRESS:
        next_player_pos = dbgame.player_ids.index(dbgame.next_turn)
        if player.played_by == dbgame.player_ids[next_player_pos]:
            die_face = Dice.roll()

            # If current player had a move else initialize move to start position
            if player.played_by in dbgame.moves_played:
                last_move = dbgame.moves_played[player.played_by][-1]
            else:
                last_move = Position()

            # calculate the new position
            # If the final position exceeds 100 then stay at current location
            updated_to = int(last_move.position_to) + die_face
            new_position = Position(
                position_to=updated_to if updated_to <= 100 else int(last_move.position_to),
                position_from=int(last_move.position_to),
                die_result=die_face
            )

            eval_position = _if_snake_found_then(dbgame.board.snakes, new_position)
            final_eval_position = _if_ladder_found_then(dbgame.board.ladders, eval_position)

            # The player reaches 100 wins
            if new_position.position_to == 100:
                dbgame.status = GameStatus.COMPLETED
                dbgame.won_by = player.played_by
                dbgame.next_turn = ""
                dbgame.ended_at = datetime.utcnow()

            # If the player is playing first time or already played
            # Basically to check if the dictionary has the key already
            if player.played_by in dbgame.moves_played:
                dbgame.moves_played[player.played_by].append(final_eval_position)
            else:
                # Initialize to a singleton array if first time
                dbgame.moves_played[player.played_by] = [final_eval_position]

            # Rotate the turn between players in the game
            player_at = dbgame.player_ids.index(player.played_by)
            next_turn = (player_at + 1) % len(dbgame.player_ids)
            dbgame.next_turn = dbgame.player_ids[next_turn]

        else:
            # If same player requests again return the previous positions
            final_eval_position = dbgame.moves_played[player.played_by][-1]

    elif dbgame.status == GameStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Game already completed."
        )

    row = conn[database_name][game_collection].update_one(
        {"_id": f"{ObjectId(game_id)}"},
        {'$set': jsonable_encoder(dbgame)}
    )

    return GamePosition(
        next_turn=dbgame.next_turn,
        position=final_eval_position,
        status=dbgame.status,
        board=dbgame.board,
        won_by=dbgame.won_by
    )
