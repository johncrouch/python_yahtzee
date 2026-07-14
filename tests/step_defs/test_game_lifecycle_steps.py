import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenario, then, when

from app.main import app


@pytest.fixture
def api_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def scenario_state():
    return {}


scenario = scenario


@scenario("../features/game_lifecycle.feature", "Creating a game and adding a player")
def test_creating_game_and_adding_player():
    pass


@scenario("../features/game_lifecycle.feature", "Starting a game and rolling dice")
def test_starting_game_and_rolling_dice():
    pass


@given("a new game", target_fixture="scenario_state")
def new_game(scenario_state, api_client):
    response = api_client.post("/games")
    assert response.status_code == 200
    scenario_state["client"] = api_client
    scenario_state["game_id"] = response.json()["id"]
    return scenario_state


@given(parsers.parse('a new game with player "{name}" in seat {seat_number}'), target_fixture="scenario_state")
def new_game_with_player(scenario_state, api_client, name, seat_number):
    response = api_client.post("/games")
    assert response.status_code == 200
    game_id = response.json()["id"]
    player_response = api_client.post(
        f"/games/{game_id}/players",
        json={"name": name, "seat_number": int(seat_number)},
    )
    assert player_response.status_code == 200
    scenario_state["client"] = api_client
    scenario_state["game_id"] = game_id
    return scenario_state


@when(parsers.parse('I add a player named "{name}" in seat {seat_number}'))
def add_player(scenario_state, name, seat_number):
    response = scenario_state["client"].post(
        f"/games/{scenario_state['game_id']}/players",
        json={"name": name, "seat_number": int(seat_number)},
    )
    scenario_state["last_response"] = response


@when("I start the game")
def start_game(scenario_state):
    response = scenario_state["client"].post(f"/games/{scenario_state['game_id']}/start")
    scenario_state["last_response"] = response


@when("I roll the dice")
def roll_dice(scenario_state):
    response = scenario_state["client"].post(f"/games/{scenario_state['game_id']}/roll")
    scenario_state["last_response"] = response


@then("the player should be created successfully")
def player_created(scenario_state):
    assert scenario_state["last_response"].status_code == 200


@then(parsers.parse("the game should contain {count:d} player"))
def game_contains_players(scenario_state, count):
    response = scenario_state["client"].get(f"/games/{scenario_state['game_id']}")
    assert response.status_code == 200
    assert len(response.json()["players"]) == count


@then(parsers.parse("the response should contain {count:d} dice values"))
def response_contains_dice(scenario_state, count):
    assert scenario_state["last_response"].status_code == 200
    payload = scenario_state["last_response"].json()
    assert len(payload["dice_values"]) == count
