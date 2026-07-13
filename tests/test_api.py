from fastapi.testclient import TestClient

from app.main import app
import app.services.game_service as game_service_module


client = TestClient(app)


def test_create_game_and_add_player():
    response = client.post("/games")
    assert response.status_code == 200
    game_id = response.json()["id"]

    player_response = client.post(
        f"/games/{game_id}/players",
        json={"name": "Ada", "seat_number": 1},
    )

    assert player_response.status_code == 200
    assert player_response.json()["name"] == "Ada"


def test_start_game_and_roll_dice():
    response = client.post("/games")
    game_id = response.json()["id"]
    client.post(f"/games/{game_id}/players", json={"name": "Ada", "seat_number": 1})
    start_response = client.post(f"/games/{game_id}/start")
    assert start_response.status_code == 200

    roll_response = client.post(f"/games/{game_id}/roll")
    assert roll_response.status_code == 200
    assert len(roll_response.json()["dice_values"]) == 5


def test_submit_score_accepts_repeated_dice_query_params():
    response = client.post("/games")
    game_id = response.json()["id"]
    client.post(f"/games/{game_id}/players", json={"name": "Ada", "seat_number": 1})
    client.post(f"/games/{game_id}/start")

    score_response = client.post(
        f"/games/{game_id}/score",
        params={"category": "twos", "dice_values": [1, 1, 1, 2, 3]},
    )

    assert score_response.status_code == 200
    assert score_response.json()["score"] == 2


def test_roll_dice_can_keep_selected_indices():
    response = client.post("/games")
    game_id = response.json()["id"]
    client.post(f"/games/{game_id}/players", json={"name": "Ada", "seat_number": 1})
    client.post(f"/games/{game_id}/start")

    first_roll = client.post(f"/games/{game_id}/roll")
    assert first_roll.status_code == 200
    first_values = first_roll.json()["dice_values"]

    second_roll = client.post(
        f"/games/{game_id}/roll",
        json={"keep_indices": [0, 2]},
    )
    assert second_roll.status_code == 200
    second_values = second_roll.json()["dice_values"]

    assert second_values[0] == first_values[0]
    assert second_values[2] == first_values[2]
    assert len(second_values) == 5


def test_roll_dice_rerolls_non_kept_dice(monkeypatch):
    response = client.post("/games")
    game_id = response.json()["id"]
    client.post(f"/games/{game_id}/players", json={"name": "Ada", "seat_number": 1})
    client.post(f"/games/{game_id}/start")

    first_roll_response = client.post(f"/games/{game_id}/roll")
    first_values = first_roll_response.json()["dice_values"]

    monkeypatch.setattr(game_service_module, "randint", lambda a, b: 9)

    reroll_response = client.post(
        f"/games/{game_id}/roll",
        json={"keep_indices": [0, 2]},
    )

    assert reroll_response.status_code == 200
    rerolled_values = reroll_response.json()["dice_values"]
    assert rerolled_values[0] == first_values[0]
    assert rerolled_values[2] == first_values[2]
    assert rerolled_values[1] == 9
    assert rerolled_values[3] == 9
    assert rerolled_values[4] == 9
