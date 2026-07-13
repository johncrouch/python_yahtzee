from pathlib import Path

from app.domain.game import GameStatus
from app.services.game_service import GameService
from app.repositories.sqlite_game_repository import SQLiteGameRepository


def test_game_service_persists_game_state_to_sqlite(tmp_path: Path) -> None:
    db_path = tmp_path / "games.db"
    repository = SQLiteGameRepository(db_path)
    service = GameService(repository=repository)

    game = service.create_game()
    service.add_player(game.id, "Alice", 1)
    service.start_game(game.id)

    reloaded_service = GameService(repository=repository)
    reloaded_game = reloaded_service.get_game(game.id)

    assert reloaded_game.id == game.id
    assert reloaded_game.status == GameStatus.ACTIVE
    assert [player.name for player in reloaded_game.players] == ["Alice"]
