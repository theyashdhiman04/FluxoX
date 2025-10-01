# FluxoX Backend – Code Notes

**Author:** theyashdhiman04

## Structure

- **app/main.py** – FastAPI app, lifespan, CORS, rate limiting, and top-level routes for `/flows`, `/metrics`, `/health`.
- **app/flow/engine.py** – FlowEngine: builds the agent graph (mock or LangGraph), runs flows.
- **app/api/** – Routers for flows, agents, execute, metrics.
- **app/auth/** – JWT and auth routes under `/auth`.
- **app/database/** – aiosqlite usage in `__init__.py` (fluxox.db, workflows + workflow_executions). SQLAlchemy in `connection.py` / `models.py` for alternate/legacy paths.

## Design choices

- Flow endpoints are under `/flows`; execute and metrics are separate.
- Mock execution is default; LangGraph is opt-in via config.
- Tests patch `app.flow.engine.FlowEngine` and hit `/flows`, `/execute`, etc.

## Recommendations

- Prefer a single source of truth for DB (either aiosqlite in `app.database` or SQLAlchemy) to avoid drift.
- Keep route definitions in routers; minimize duplicate logic in `main.py`.
- Restrict CORS and set `SECRET_KEY` in production.
