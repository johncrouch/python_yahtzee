from __future__ import annotations

from random import randint

from app.domain.game import Game, GameStatus, Player, Turn
from app.services.scoring_service import ScoringService


class GameService:
    """Service for managing the lifecycle of a Yahtzee game."""

    def __init__(self) -> None:
        self._games: dict[int, Game] = {}
        self._next_id = 1
        self._next_turn_id = 1
        self._scoring_service = ScoringService()

    def create_game(self) -> Game:
        game = Game(id=self._next_id)
        self._games[game.id] = game
        self._next_id += 1
        return game

    def add_player(self, game_id: int, name: str, seat_number: int) -> Player:
        game = self._get_game_or_raise(game_id)
        if game.status != GameStatus.CREATED:
            raise ValueError("Players can only be added before the game starts")
        player = Player(id=self._next_id, name=name, seat_number=seat_number)
        game.add_player(player)
        self._next_id += 1
        return player

    def start_game(self, game_id: int) -> Game:
        game = self._get_game_or_raise(game_id)
        game.start()
        self._start_turn(game)
        return game

    def abort_game(self, game_id: int) -> Game:
        game = self._get_game_or_raise(game_id)
        game.status = GameStatus.ABORTED
        return game

    def roll_dice(self, game_id: int, dice_values: list[int] | None = None) -> list[int]:
        game = self._get_game_or_raise(game_id)
        if game.status != GameStatus.ACTIVE:
            raise ValueError("The game must be active before rolling")
        if game.current_turn is None:
            self._start_turn(game)
        if game.current_turn is None:
            raise ValueError("No active turn available")
        if game.current_turn.roll_count >= 3:
            raise ValueError("A turn can only have up to 3 rolls")

        if dice_values is None:
            dice_values = [randint(1, 6) for _ in range(5)]

        game.current_turn.dice_values = list(dice_values)
        game.current_turn.roll_count += 1
        return game.current_turn.dice_values

    def submit_score(self, game_id: int, category: str, dice_values: list[int] | None = None) -> int:
        game = self._get_game_or_raise(game_id)
        if game.status != GameStatus.ACTIVE:
            raise ValueError("The game must be active before submitting a score")
        if game.current_turn is None:
            raise ValueError("No active turn available")

        if dice_values is None:
            dice_values = game.current_turn.dice_values or [0, 0, 0, 0, 0]

        score_card = game.get_score_card(game.current_turn.player_id)
        if score_card is None:
            raise ValueError("No score card available for the current player")

        score = self._scoring_service.apply_score(score_card, category, dice_values)
        game.current_turn.selected_category = category
        game.current_turn.status = "completed"
        game.current_turn = None
        game.next_turn()

        if self._is_game_complete(game):
            game.status = GameStatus.COMPLETED
        else:
            self._start_turn(game)

        return score

    def get_game(self, game_id: int) -> Game:
        return self._get_game_or_raise(game_id)

    def _start_turn(self, game: Game) -> None:
        if not game.players:
            raise ValueError("A game must have at least one player")
        current_player = game.get_current_player()
        if current_player is None:
            raise ValueError("No current player available")
        game.current_turn = Turn(
            id=self._next_turn_id,
            player_id=current_player.id,
            round_number=game.current_round,
        )
        self._next_turn_id += 1

    def _is_game_complete(self, game: Game) -> bool:
        if not game.players:
            return False
        return all(len(score_card.used_categories) >= 13 for score_card in game.score_cards)

    def _get_game_or_raise(self, game_id: int) -> Game:
        game = self._games.get(game_id)
        if game is None:
            raise KeyError(f"Game {game_id} does not exist")
        return game
