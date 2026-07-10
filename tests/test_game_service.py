import pytest

from app.domain.game import GameStatus
from app.services.game_service import GameService


def test_create_game_initializes_new_game():
    service = GameService()

    game = service.create_game()

    assert game.id == 1
    assert game.status is GameStatus.CREATED
    assert game.current_round == 1
    assert game.current_player_index == 0


def test_add_player_registers_player_and_score_card():
    service = GameService()
    game = service.create_game()

    player = service.add_player(game.id, "Ada", 1)

    assert player.name == "Ada"
    assert len(game.players) == 1
    assert len(game.score_cards) == 1
    assert game.get_score_card(player.id) is not None


def test_start_game_marks_game_active():
    service = GameService()
    game = service.create_game()
    service.add_player(game.id, "Grace", 1)

    service.start_game(game.id)

    assert game.status is GameStatus.ACTIVE


def test_abort_game_marks_game_aborted():
    service = GameService()
    game = service.create_game()

    service.abort_game(game.id)

    assert game.status is GameStatus.ABORTED
