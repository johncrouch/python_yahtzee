from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.api.schemas import (
    GameCreateResponse,
    GameStateResponse,
    PlayerCreateRequest,
    PlayerResponse,
    ScoreCardResponse,
    TurnResponse,
)
from app.services.game_service import GameService

router = APIRouter()
service = GameService()


class RollDiceRequest(BaseModel):
    keep_indices: list[int] | None = None


@router.post("/games", response_model=GameCreateResponse)
def create_game() -> GameCreateResponse:
    game = service.create_game()
    return GameCreateResponse(
        id=game.id,
        status=game.status.value,
        current_round=game.current_round,
        current_player_index=game.current_player_index,
    )


@router.get("/games/{game_id}", response_model=GameStateResponse)
def get_game(game_id: int) -> GameStateResponse:
    try:
        game = service.get_game(game_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return GameStateResponse(
        id=game.id,
        status=game.status.value,
        current_round=game.current_round,
        current_player_index=game.current_player_index,
        players=[PlayerResponse(id=p.id, name=p.name, seat_number=p.seat_number) for p in game.players],
        score_cards=[
            ScoreCardResponse(
                player_id=score_card.player_id,
                used_categories=sorted(score_card.used_categories),
                upper_section_total=score_card.upper_section_total,
                lower_section_total=score_card.lower_section_total,
                grand_total=score_card.grand_total,
            )
            for score_card in game.score_cards
        ],
        current_turn=(
            TurnResponse(
                id=game.current_turn.id,
                player_id=game.current_turn.player_id,
                round_number=game.current_turn.round_number,
                roll_count=game.current_turn.roll_count,
                status=game.current_turn.status,
                selected_category=game.current_turn.selected_category,
                dice_values=game.current_turn.dice_values,
            )
            if game.current_turn is not None
            else None
        ),
    )


@router.post("/games/{game_id}/players", response_model=PlayerResponse)
def add_player(game_id: int, payload: PlayerCreateRequest) -> PlayerResponse:
    try:
        player = service.add_player(game_id, payload.name, payload.seat_number)
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return PlayerResponse(id=player.id, name=player.name, seat_number=player.seat_number)


@router.post("/games/{game_id}/start")
def start_game(game_id: int) -> dict[str, str]:
    try:
        service.start_game(game_id)
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"status": "started"}


@router.post("/games/{game_id}/roll")
def roll_dice(game_id: int, payload: RollDiceRequest | None = None) -> dict[str, object]:
    try:
        dice_values = service.roll_dice(
            game_id,
            keep_indices=payload.keep_indices if payload is not None else None,
        )
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"dice_values": dice_values}


@router.post("/games/{game_id}/score")
def submit_score(
    game_id: int,
    category: str,
    dice_values: list[int] = Query(default=[]),
) -> dict[str, object]:
    if not dice_values:
        dice_values = [0, 0, 0, 0, 0]
    try:
        score = service.submit_score(game_id, category, dice_values)
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"score": score}
