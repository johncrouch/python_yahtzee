# Player Score Card
A player score card has

- Upper Section
- Lower Section
- Total Section

At the end of each round a player must indicate which category, upper or lower, they wish to use to record the score for that round.

Each category once scored on the score card instance, cannot be changed for the rest of the game

## Upper Section

When an upper section category is chosen by a player at the end of their round, then the corresponding point value is calculated.

| Category | Requirements | Point Value |
| :- | :- | :- |
| 1 | All dice with value '1' | Sum of all 1 |
| 2 | All dice with value '2' | Sum of all 2 |
| 3 | All dice with value '3' | Sum of all 3 |
| 4 | All dice with value '4' | Sum of all 4 |
| 5 | All dice with value '5' | Sum of all 5 |
| 6 | All dice with value '6' | Sum of all 6 |

## Lower Section

When a lower section category is chosen by a player at the end of their round, then the corresponding point value is calculated.

| Category | Requirements for scoring | Point value | 
 :- | :- | :- |
| 3 of a Kind | At least 3 dice with the same number.| The sum of all 5 dice. | 
| 4 of a Kind | At least 4 dice with the same number.| The sum of all 5 dice. |
| Full House | 3 dice of one number + 2 dice of another number | 25 points . |
| Small straight| 4 numbers in an uninterrupted sequence (e.g. 1-2-3-4, 2-3-4-5 or 3-4-5-6).| 30 points |
| Big straight | 5 numbers in an uninterrupted sequence (1-2-3-4-5 or 2-3-4-5-6) | 40 points |
| YAHTZEE | All 5 dice show exactly the same number (5 of a kind) | 50 points |
| Chance | No special requirements. Functions as a gathering place. | The sum of all 5 dice. |

## Card Total

At the end of the round, once a lower or upper category is chosen, the upper, lower and total 'point values' are re calculated.

| Section | Requirements | Point Value | 
 :- | :- | :- |
| Upper | The current total sum of points from upper section | Sum of Upper section points|
| Lower | The current total sum of points from lower section | Sum of Lower section points|
| Total | The current total sum of points from both upper and lower sections | Sum of Upper section points and Lower ection points |