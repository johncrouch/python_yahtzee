from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.game import Game


class GameRepository(ABC):
    @abstractmethod
    def save(self, game: Game) -> None:
        raise NotImplementedError

    @abstractmethod
    def load(self, game_id: int) -> Game | None:
        raise NotImplementedError

    @abstractmethod
    def list_game_ids(self) -> list[int]:
        raise NotImplementedError
