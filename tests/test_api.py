from fastapi.testclient import TestClient

from app.main import app


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
