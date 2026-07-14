# python_yahtzee
An agentic-engineered, web-based Yahtzee game for up to 4 players.

## Phase 1 implementation status
The initial Phase 1 foundation is now in place.

### Included capabilities
- Game creation and lifecycle management
- Player registration and score card initialization
- Core scoring rules for upper and lower sections
- Turn initialization, dice rolling, and score submission
- Automatic progression to the next player until the game is complete
- Automated tests for game, scoring, and turn-flow behavior

### Project structure
- app/domain/: domain models for the game
- app/services/: game and scoring services
- tests/: automated tests for Phase 1 behavior

### Run tests
From the repository root:

```bash
python -m pytest -q
```

### Run the web app

```bash
python -m uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/ in your browser.

### Run with Docker locally

Build and start the container:

```bash
docker compose up --build
```

Then open http://127.0.0.1:8000/ in your browser.

To stop it:

```bash
docker compose down
```

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Run security scan

```bash
python -m safety check -r requirements.txt
```
