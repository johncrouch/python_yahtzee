from __future__ import annotations

from app.domain.game import ScoreCard


class ScoringService:
    """Service for calculating YAHTZEE scores."""

    def calculate_score(self, category: str, dice_values: list[int]) -> int:
        if category in {"ones", "twos", "threes", "fours", "fives", "sixes"}:
            return self._calculate_upper_section(category, dice_values)

        if category == "three_of_a_kind":
            return self._calculate_three_of_a_kind(dice_values)
        if category == "four_of_a_kind":
            return self._calculate_four_of_a_kind(dice_values)
        if category == "full_house":
            return self._calculate_full_house(dice_values)
        if category == "small_straight":
            return self._calculate_small_straight(dice_values)
        if category == "large_straight":
            return self._calculate_large_straight(dice_values)
        if category == "yahtzee":
            return self._calculate_yahtzee(dice_values)
        if category == "chance":
            return sum(dice_values)

        raise ValueError(f"Unknown category: {category}")

    def apply_score(self, score_card: ScoreCard, category: str, dice_values: list[int]) -> int:
        if category in score_card.used_categories:
            raise ValueError(f"Category {category} has already been used")

        score = self.calculate_score(category, dice_values)
        score_card.used_categories.add(category)
        if category in {"ones", "twos", "threes", "fours", "fives", "sixes"}:
            score_card.upper_section_total += score
        else:
            score_card.lower_section_total += score
        score_card.grand_total = score_card.upper_section_total + score_card.lower_section_total
        return score

    def _calculate_upper_section(self, category: str, dice_values: list[int]) -> int:
        value_map = {
            "ones": 1,
            "twos": 2,
            "threes": 3,
            "fours": 4,
            "fives": 5,
            "sixes": 6,
        }
        target = value_map[category]
        return sum(value for value in dice_values if value == target)

    def _calculate_three_of_a_kind(self, dice_values: list[int]) -> int:
        return sum(dice_values) if self._has_n_of_kind(dice_values, 3) else 0

    def _calculate_four_of_a_kind(self, dice_values: list[int]) -> int:
        return sum(dice_values) if self._has_n_of_kind(dice_values, 4) else 0

    def _calculate_full_house(self, dice_values: list[int]) -> int:
        counts = sorted(dice_values)
        return 25 if counts[0] == counts[1] == counts[2] and counts[3] == counts[4] else 0

    def _calculate_small_straight(self, dice_values: list[int]) -> int:
        unique = sorted(set(dice_values))
        straight_sets = [
            {1, 2, 3, 4},
            {2, 3, 4, 5},
            {3, 4, 5, 6},
        ]
        for target in straight_sets:
            if target.issubset(set(unique)):
                return 30
        return 0

    def _calculate_large_straight(self, dice_values: list[int]) -> int:
        unique = sorted(set(dice_values))
        straight_sets = [
            {1, 2, 3, 4, 5},
            {2, 3, 4, 5, 6},
        ]
        for target in straight_sets:
            if target.issubset(set(unique)):
                return 40
        return 0

    def _calculate_yahtzee(self, dice_values: list[int]) -> int:
        return 50 if len(set(dice_values)) == 1 else 0

    def _has_n_of_kind(self, dice_values: list[int], count: int) -> bool:
        return any(dice_values.count(value) >= count for value in set(dice_values))
