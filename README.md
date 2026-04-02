# Items API

A minimal FastAPI service that manages a collection of items. Provides health
checking, item listing, and item creation over HTTP.

---

## Project structure

```
.
├── pyproject.toml       # Build config, dependencies, ruff + pytest settings
├── src/
│   ├── main.py          # FastAPI app factory
│   └── api.py           # Router: /health, /items
└── tests/
    └── test_api.py      # Pytest suite (httpx TestClient)
```

---

## Setup

Requires **Python 3.11+**.

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install runtime + dev dependencies
pip install -e ".[dev]"
```

---

## Running the server

```bash
uvicorn src.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.  
Interactive docs: `http://127.0.0.1:8000/docs`

---

## API endpoints

### `GET /health`

Returns service health and version.

**Response `200 OK`**
```json
{"status": "ok", "version": "1.0.0"}
```

---

### `GET /items`

Returns the full list of items.

**Response `200 OK`**
```json
[
  {"id": 1, "name": "Widget",    "description": "A standard widget", "price": 9.99},
  {"id": 2, "name": "Gadget",    "description": "A useful gadget",   "price": 24.99},
  {"id": 3, "name": "Doohickey", "description": null,                "price": 4.49}
]
```

---

### `POST /items`

Creates a new item. `description` is optional.

**Request body**
```json
{"name": "Thingamajig", "description": "A thingamajig", "price": 14.99}
```

**Response `201 Created`**
```json
{"id": 4, "name": "Thingamajig", "description": "A thingamajig", "price": 14.99}
```

---

## Running tests

```bash
pytest                  # run all tests
pytest -v               # verbose output
pytest tests/test_api.py -v --tb=short   # target specific file
```

The test suite uses FastAPI's `TestClient` (backed by `httpx`) — no running
server required.

---

## Linting and formatting

```bash
ruff check src/ tests/          # lint
ruff check src/ tests/ --fix    # lint + auto-fix
ruff format src/ tests/         # format
```

Ruff is configured in `pyproject.toml` with the following rule sets enabled:
`E/W` (pycodestyle), `F` (pyflakes), `I` (isort), `UP` (pyupgrade),
`B` (bugbear), `C4` (comprehensions), `RUF` (ruff-native).

---

## Development workflow (Gas Town / Beads)

This repo is part of a **Gas Town** workspace and uses **Beads (`bd`)** for
issue tracking instead of GitHub Issues or markdown TODO lists.

```bash
# Orientation
gt prime          # load full agent context and identity
bd prime          # load beads workflow and command reference

# Day-to-day
bd ready          # find available work
bd show <id>      # view issue details
bd update <id> --claim   # claim an issue
bd close <id>     # mark work complete
bd remember       # persist knowledge to beads (not MEMORY.md)

# Session close — all steps are mandatory
git pull --rebase
bd dolt push
git push
git status        # must show "up to date with origin"
```

### Communication hygiene

| Situation | Tool |
|---|---|
| Routine agent-to-agent message | `gt nudge` (ephemeral, no DB write) |
| Handoff / structured protocol / escalation | `gt mail send` (permanent bead) |
| Dolt trouble | Collect diagnostics first, then `gt escalate` |

### Dolt (data plane)

Beads data lives in **Dolt** on port 3307. If `bd` commands hang or return
empty results unexpectedly:

```bash
# Diagnose before restarting
kill -QUIT $(cat ~/gt/.dolt-data/dolt.pid)   # goroutine dump to Dolt stderr
gt dolt status 2>&1 | tee /tmp/dolt-hang-$(date +%s).log
gt escalate -s HIGH "Dolt: <describe symptom>"
```

Never run `rm -rf` on `~/.dolt-data/`. Use `gt dolt cleanup` to remove orphan
test databases.
