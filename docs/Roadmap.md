# Development Roadmap

## Overview
This roadmap describes a practical, staged delivery plan for the Yahtzee product defined in the PRD. The focus is on getting a complete and reliable MVP first, then expanding quality and capabilities.

## Phase 1 — Foundation
Objective: establish the core domain and basic gameplay loop.

Deliverables:
- Project structure and documentation baseline
- Game creation flow
- Player registration and seat assignment
- Initial scorecard model
- Basic turn and round progression

Success criteria:
- A game can be created.
- Players can be registered.
- A turn can start and complete.

## Phase 2 — Core gameplay
Objective: complete the real game experience.

Status: Implemented in the current milestone.

Included capabilities:
- turn initialization on game start
- dice roll tracking up to three rolls
- score submission and turn completion
- automatic progression to the next player
- game completion when every score category has been used

Deliverables:
- Dice rolling with up to three rolls per turn
- Keeper selection during a turn
- Score category selection and scoring rules
- Upper and lower section totals
- Game completion and final result calculation

Success criteria:
- A full game can be played from start to finish.
- Scoring rules behave correctly.
- A player can finish all required categories.

## Phase 3 — Leaderboards and persistence
Objective: make the product reliable and useful beyond a single session.

Deliverables:
- Persistent storage for active games
- Repository and ORM layer for game, player, scorecard, turn, and leaderboard data
- Current game leaderboard
- Weekly leaderboard
- All-time leaderboard
- Game state recovery and audit-safe updates
- Snapshot generation for leaderboard history

Success criteria:
- Completed games are stored and reportable.
- Rankings are available after game completion.
- The gameplay state can be reloaded from persistence without loss.

## Phase 4 — Product quality
Objective: improve reliability, usability, and maintainability.

Deliverables:
- Validation and error handling for invalid actions
- Responsive UI improvements
- Realtime updates for turns and leaderboard changes
- Automated testing for core game rules

Success criteria:
- Core scenarios are protected by tests.
- The experience is stable across common screen sizes.

## Phase 5 — Expansion
Objective: extend the product beyond the MVP.

Possible enhancements:
- User accounts and saved profiles
- Historical game replay
- Better multiplayer session sharing
- Advanced analytics and stat tracking

Success criteria:
- The system supports future growth without major rework.
