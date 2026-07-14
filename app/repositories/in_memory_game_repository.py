from __future__ import annotations

from app.domain.game import Game
from app.repositories.game_repository import GameRepository


class InMemoryGameRepository(GameRepository):
    def __init__(self) -> None:
        self._games: dict[int, Game] = {}

    def save(self, game: Game) -> None:
        self._games[game.id] = game

    def load(self, game_id: int) -> Game | None:
        return self._games.get(game_id)

    def list_game_ids(self) -> list[int]:
        return sorted(self._games)
