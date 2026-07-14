from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class PlayerCreateRequest(BaseModel):
    name: str
    seat_number: int


class GameCreateResponse(BaseModel):
    id: int
    status: str
    current_round: int
    current_player_index: int


class PlayerResponse(BaseModel):
    id: int
    name: str
    seat_number: int


class ScoreCardResponse(BaseModel):
    player_id: int
    used_categories: List[str]
    upper_section_total: int
    lower_section_total: int
    grand_total: int


class TurnResponse(BaseModel):
    id: int
    player_id: int
    round_number: int
    roll_count: int
    status: str
    selected_category: Optional[str] = None
    dice_values: List[int]


class GameStateResponse(BaseModel):
    id: int
    status: str
    current_round: int
    current_player_index: int
    players: List[PlayerResponse]
    score_cards: List[ScoreCardResponse]
    current_turn: Optional[TurnResponse] = None
