from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from app.domain.game import Game, GameStatus, Player, ScoreCard, Turn
from app.repositories.game_repository import GameRepository


class SQLiteGameRepository(GameRepository):
    def __init__(self, db_path: str | Path | None = None) -> None:
        self._db_path = Path(db_path or "game_state.db")
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_schema()

    def save(self, game: Game) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO games (id, status, current_round, current_player_index, players_json, score_cards_json, current_turn_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    status = excluded.status,
                    current_round = excluded.current_round,
                    current_player_index = excluded.current_player_index,
                    players_json = excluded.players_json,
                    score_cards_json = excluded.score_cards_json,
                    current_turn_json = excluded.current_turn_json
                """,
                (
                    game.id,
                    game.status.value,
                    game.current_round,
                    game.current_player_index,
                    json.dumps([self._player_to_dict(player) for player in game.players]),
                    json.dumps([self._score_card_to_dict(score_card) for score_card in game.score_cards]),
                    json.dumps(self._turn_to_dict(game.current_turn)) if game.current_turn is not None else None,
                ),
            )
            conn.commit()

    def load(self, game_id: int) -> Game | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, status, current_round, current_player_index, players_json, score_cards_json, current_turn_json FROM games WHERE id = ?",
                (game_id,),
            ).fetchone()

        if row is None:
            return None

        game = Game(id=row[0], status=GameStatus(row[1]), current_round=row[2], current_player_index=row[3])
        game.players = [self._player_from_dict(player) for player in json.loads(row[4] or "[]")]
        game.score_cards = [self._score_card_from_dict(score_card) for score_card in json.loads(row[5] or "[]")]
        current_turn = row[6]
        if current_turn is not None:
            game.current_turn = self._turn_from_dict(json.loads(current_turn))
        return game

    def list_game_ids(self) -> list[int]:
        with self._connect() as conn:
            rows = conn.execute("SELECT id FROM games ORDER BY id").fetchall()
        return [row[0] for row in rows]

    def _initialize_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY,
                    status TEXT NOT NULL,
                    current_round INTEGER NOT NULL,
                    current_player_index INTEGER NOT NULL,
                    players_json TEXT,
                    score_cards_json TEXT,
                    current_turn_json TEXT
                )
                """
            )
            conn.commit()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _player_to_dict(self, player: Player) -> dict[str, object]:
        return {"id": player.id, "name": player.name, "seat_number": player.seat_number}

    def _player_from_dict(self, data: dict[str, object]) -> Player:
        return Player(id=int(data["id"]), name=str(data["name"]), seat_number=int(data["seat_number"]))

    def _score_card_to_dict(self, score_card: ScoreCard) -> dict[str, object]:
        return {
            "player_id": score_card.player_id,
            "used_categories": sorted(score_card.used_categories),
            "upper_section_total": score_card.upper_section_total,
            "lower_section_total": score_card.lower_section_total,
            "grand_total": score_card.grand_total,
        }

    def _score_card_from_dict(self, data: dict[str, object]) -> ScoreCard:
        return ScoreCard(
            player_id=int(data["player_id"]),
            used_categories=set(data.get("used_categories", [])),
            upper_section_total=int(data.get("upper_section_total", 0)),
            lower_section_total=int(data.get("lower_section_total", 0)),
            grand_total=int(data.get("grand_total", 0)),
        )

    def _turn_to_dict(self, turn: Turn | None) -> dict[str, object] | None:
        if turn is None:
            return None
        return {
            "id": turn.id,
            "player_id": turn.player_id,
            "round_number": turn.round_number,
            "roll_count": turn.roll_count,
            "status": turn.status,
            "selected_category": turn.selected_category,
            "dice_values": turn.dice_values,
        }

    def _turn_from_dict(self, data: dict[str, object]) -> Turn:
        return Turn(
            id=int(data["id"]),
            player_id=int(data["player_id"]),
            round_number=int(data["round_number"]),
            roll_count=int(data.get("roll_count", 0)),
            status=str(data.get("status", "in_progress")),
            selected_category=data.get("selected_category"),
            dice_values=list(data.get("dice_values", [])),
        )
