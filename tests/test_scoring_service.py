from app.services.scoring_service import ScoringService


def test_upper_section_score_sums_matching_faces():
    service = ScoringService()

    score = service.calculate_score("threes", [3, 3, 3, 1, 2])

    assert score == 9


def test_three_of_a_kind_scores_total_when_present():
    service = ScoringService()

    score = service.calculate_score("three_of_a_kind", [4, 4, 4, 2, 1])

    assert score == 15


def test_three_of_a_kind_scores_zero_when_not_present():
    service = ScoringService()

    score = service.calculate_score("three_of_a_kind", [1, 2, 3, 4, 5])

    assert score == 0


def test_full_house_scores_25_when_formed():
    service = ScoringService()

    score = service.calculate_score("full_house", [2, 2, 2, 5, 5])

    assert score == 25


def test_yahtzee_scores_50_when_all_dice_match():
    service = ScoringService()

    score = service.calculate_score("yahtzee", [6, 6, 6, 6, 6])

    assert score == 50


def test_apply_score_updates_card_totals_and_blocks_reuse():
    service = ScoringService()
    from app.domain.game import ScoreCard

    score_card = ScoreCard(player_id=1)

    first_score = service.apply_score(score_card, "ones", [1, 1, 1, 2, 3])
    second_score = service.apply_score(score_card, "twos", [2, 2, 3, 4, 5])

    assert first_score == 3
    assert second_score == 4
    assert score_card.upper_section_total == 7
    assert score_card.grand_total == 7

    try:
        service.apply_score(score_card, "ones", [1, 1, 1, 1, 1])
    except ValueError as exc:
        assert "already been used" in str(exc)
    else:
        raise AssertionError("Expected duplicate category to raise ValueError")
