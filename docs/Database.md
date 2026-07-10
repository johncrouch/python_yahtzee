# Database Design

## Overview
The application requires persistent storage for active games, player progress, scorecards, turns, and leaderboard history. A relational database is the best fit because the data model is structured and transactional.

## Recommended database
- PostgreSQL for production
- SQLite for local development and testing

## Core entities

### games
Stores the lifecycle of a single Yahtzee session.

| Column | Type | Notes |
|---|---|---|
| id | UUID / integer | Primary key |
| status | varchar | created, active, completed, aborted |
| current_round | integer | Current round number |
| current_player_index | integer | Index of active player |
| created_at | timestamp | Record creation time |
| completed_at | timestamp | Nullable |
| created_by | varchar | Optional, for tracking origin |

### players
Represents a participant in a specific game.

| Column | Type | Notes |
|---|---|---|
| id | UUID / integer | Primary key |
| game_id | UUID / integer | Foreign key to games |
| seat_number | integer | 1 to 4 |
| name | varchar | Player display name |
| is_active | boolean | Whether the player remains in the game |
| joined_at | timestamp | Registration time |

### score_cards
Stores the score sheet for one player in one game.

| Column | Type | Notes |
|---|---|---|
| id | UUID / integer | Primary key |
| player_id | UUID / integer | Foreign key to players |
| upper_section_total | integer | Computed total |
| lower_section_total | integer | Computed total |
| grand_total | integer | Final total |
| version | integer | For optimistic concurrency control |

### score_entries
Records each category used by a player.

| Column | Type | Notes |
|---|---|---|
| id | UUID / integer | Primary key |
| score_card_id | UUID / integer | Foreign key to score_cards |
| category_code | varchar | Upper/lower category key |
| score_value | integer | Numeric score |
| is_used | boolean | Whether the category has been claimed |
| recorded_at | timestamp | Time of scoring |

### turns
Stores one turn attempt for a player within the active game.

| Column | Type | Notes |
|---|---|---|
| id | UUID / integer | Primary key |
| game_id | UUID / integer | Foreign key to games |
| player_id | UUID / integer | Foreign key to players |
| round_number | integer | Current round |
| roll_count | integer | Number of rolls used |
| status | varchar | in_progress, completed |
| selected_category | varchar | Nullable |
| created_at | timestamp | Turn start time |
| completed_at | timestamp | Nullable |

### turn_rolls
Captures each roll and its resulting dice state.

| Column | Type | Notes |
|---|---|---|
| id | UUID / integer | Primary key |
| turn_id | UUID / integer | Foreign key to turns |
| roll_number | integer | 1 to 3 |
| dice_values_json | json | Dice values for that roll |
| keepers_json | json | Kept dice values |
| cup_state_json | json | Optional representation of the current cup state |
| keep_state_json | json | Optional representation of which dice were held |

### leaderboard_snapshots
Stores rankings for current, weekly, and all-time histories.

| Column | Type | Notes |
|---|---|---|
| id | UUID / integer | Primary key |
| player_id | UUID / integer | Foreign key to players |
| game_id | UUID / integer | Nullable, for game-specific snapshot |
| score_value | integer | Total score at snapshot time |
| period_type | varchar | current, weekly, all_time |
| recorded_at | timestamp | Snapshot time |

## Relationships
- One game has many players.
- One player has one score card.
- One score card has many score entries.
- One game has many turns.
- One turn has many roll records.
- One player may appear in many leaderboard snapshots across time.

## Constraints and integrity rules
- A player cannot claim the same category twice.
- Each turn belongs to a valid player in the active game.
- A turn can only be completed once a category is chosen.
- A game can contain between 1 and 4 players.

## Indexing recommendations
- Index on game_id for all game-scoped entities.
- Index on player_id for score and leaderboard lookups.
- Index on status and created_at for active and completed game queries.
- Index on recorded_at for leaderboard historical queries.

## Migration approach
Use versioned migrations so schema changes remain explicit and reversible. Each milestone should include:
- schema migration scripts
- seed data where needed
- data validation checks
