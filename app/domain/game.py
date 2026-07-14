from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List


class GameStatus(str, Enum):
    CREATED = "created"
    ACTIVE = "active"
    COMPLETED = "completed"
    ABORTED = "aborted"


@dataclass
class Player:
    id: int
    name: str
    seat_number: int


@dataclass
class ScoreCard:
    player_id: int
    used_categories: set[str] = field(default_factory=set)
    upper_section_total: int = 0
    lower_section_total: int = 0
    grand_total: int = 0


@dataclass
class Turn:
    id: int
    player_id: int
    round_number: int
    roll_count: int = 0
    status: str = "in_progress"
    selected_category: str | None = None
    dice_values: List[int] = field(default_factory=list)


@dataclass
class Game:
    id: int
    players: List[Player] = field(default_factory=list)
    status: GameStatus = GameStatus.CREATED
    current_round: int = 1
    current_player_index: int = 0
    score_cards: List[ScoreCard] = field(default_factory=list)
    current_turn: Turn | None = None

    def add_player(self, player: Player) -> None:
        if len(self.players) >= 4:
            raise ValueError("A game can have at most 4 players")
        self.players.append(player)
        self.score_cards.append(ScoreCard(player_id=player.id))

    def start(self) -> None:
        if not self.players:
            raise ValueError("A game must have at least one player")
        self.status = GameStatus.ACTIVE

    def next_turn(self) -> None:
        if not self.players:
            return
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        if self.current_player_index == 0:
            self.current_round += 1
        self.current_turn = None

    def get_current_player(self) -> Player | None:
        if not self.players:
            return None
        return self.players[self.current_player_index]

    def get_score_card(self, player_id: int) -> ScoreCard | None:
        for score_card in self.score_cards:
            if score_card.player_id == player_id:
                return score_card
        return None
