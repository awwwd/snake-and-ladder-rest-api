from fastapi import APIRouter

from app.api.player import router as player_routes
from app.api.game import router as game_routes

router = APIRouter()
router.include_router(player_routes)
router.include_router(game_routes)
