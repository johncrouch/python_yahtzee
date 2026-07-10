from app.services.game_service import GameService
from app.services.scoring_service import ScoringService


def test_start_game_initializes_first_turn():
    service = GameService()
    game = service.create_game()
    service.add_player(game.id, "Ada", 1)
    service.add_player(game.id, "Grace", 2)

    service.start_game(game.id)

    assert game.current_turn is not None
    assert game.current_turn.player_id == game.players[0].id
    assert game.current_turn.roll_count == 0


def test_roll_dice_increments_roll_count_and_returns_values():
    service = GameService()
    game = service.create_game()
    service.add_player(game.id, "Ada", 1)
    service.start_game(game.id)

    dice_values = service.roll_dice(game.id, dice_values=[1, 2, 3, 4, 5])

    assert dice_values == [1, 2, 3, 4, 5]
    assert game.current_turn.roll_count == 1


def test_submit_score_completes_turn_and_advances_to_next_player():
    service = GameService()
    game = service.create_game()
    service.add_player(game.id, "Ada", 1)
    service.add_player(game.id, "Grace", 2)
    service.start_game(game.id)

    service.submit_score(game.id, "ones", [1, 1, 1, 2, 3])

    assert game.current_turn is not None
    assert game.current_turn.player_id == game.players[1].id
    assert game.current_player_index == 1
    assert game.get_current_player().name == "Grace"


def test_game_completes_when_all_score_categories_are_used():
    service = GameService()
    game = service.create_game()
    service.add_player(game.id, "Ada", 1)
    service.start_game(game.id)

    scoring_service = ScoringService()
    for category in [
        "ones",
        "twos",
        "threes",
        "fours",
        "fives",
        "sixes",
        "three_of_a_kind",
        "four_of_a_kind",
        "full_house",
        "small_straight",
        "large_straight",
        "yahtzee",
        "chance",
    ]:
        dice_values = [1, 1, 1, 1, 1] if category == "yahtzee" else [1, 2, 3, 4, 5]
        service.submit_score(game.id, category, dice_values)

    assert game.status.name == "COMPLETED"
