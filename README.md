# FluxoX

**Multi-agent flow orchestration platform**

FluxoX is an API-first platform that runs automated pipelines using specialized agents: research, processing, approval, and optimization. Define flows, run them via REST, and optionally plug in LangGraph for graph-based execution.

**Author:** [theyashdhiman04](https://github.com/theyashdhiman04)

---

## Quick start

```bash
# Clone the repo
git clone https://github.com/theyashdhiman04/FluxoX.git
cd FluxoX

# Optional: copy and edit env
cp backend/.env.sample backend/.env

# One-shot setup and run
make setup-and-run
```

API docs: **http://localhost:8000/docs**

---

## Features

- **Flow engine** – Pipeline execution with configurable mock or LangGraph backend
- **REST API** – FastAPI with `/flows`, `/agents`, `/execute`, `/metrics`, `/health`
- **Agents** – Researcher, Processor, Approver, Optimizer with clear roles
- **Persistence** – SQLite store for flows and execution metrics
- **Auth** – JWT-based auth and optional rate limiting
- **Tests** – Pytest suite for API and flow engine
- **Docker** – Dockerfile and docker-compose for deployment

---

## API overview

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/flows` | List flows |
| POST | `/flows` | Create and run a flow |
| GET | `/flows/{id}` | Get flow by ID |
| GET | `/flows/templates` | List flow templates |
| GET | `/agents` | List agents |
| POST | `/execute` | Execute a flow by ID + input |
| GET | `/metrics` | Execution and system metrics |
| GET | `/health` | Health check |

---

## Local development

1. **Environment**

   ```bash
   make create-env
   # Then: conda activate fluxox  (or use your shell’s activate)
   ```

2. **Database**

   ```bash
   make init-db
   ```

3. **Run server**

   ```bash
   make run-backend
   ```

4. **Demo**

   ```bash
   make run-demo
   ```

---

## Docker

```bash
make docker-build
make docker-up
# API at http://localhost:8000/docs
make docker-down   # stop
```

---

## Configuration

Use `backend/.env` or environment variables. Examples:

- `ENVIRONMENT` – `development` | `testing` | `production`
- `USE_MOCK_WORKFLOW` – `true` (default) for mock execution, `false` for LangGraph
- `DATABASE_URL` – SQLite path (e.g. `fluxox.db`)
- `LOG_LEVEL` – `DEBUG` | `INFO` | `WARNING` | `ERROR`
- `SECRET_KEY` – Required in production
- `CORS_ALLOWED_ORIGINS` – Comma-separated origins

See `backend/.env.sample` for more options.

---

## Project layout

```
FluxoX/
├── backend/
│   ├── app/
│   │   ├── agents/       # Researcher, Processor, Approver, Optimizer
│   │   ├── api/          # flows, agents, execute, metrics
│   │   ├── auth/         # JWT and auth routes
│   │   ├── flow/         # FlowEngine (flow execution)
│   │   ├── database/     # DB connection and init
│   │   ├── config.py
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   └── environment.yml
├── docs/
├── docker-compose.yml
└── Makefile
```

---

## Makefile commands

| Command | Description |
|---------|-------------|
| `make create-env` | Create conda env from environment.yml |
| `make update-env` | Update conda env |
| `make init-db` | Initialize DB |
| `make run-backend` | Start API server |
| `make run-demo` | Run demo script |
| `make test-backend` | Run all tests |
| `make test-api` | Run API tests |
| `make test-workflow` | Run flow engine tests |
| `make format` | Black + isort |
| `make lint` | Flake8 |
| `make docker-build` / `docker-up` / `docker-down` | Docker lifecycle |
| `make setup-and-run` | Setup + run backend |

---

## LangGraph

By default FluxoX uses a **mock** flow execution (no LangGraph runtime). To use LangGraph:

- Set `USE_MOCK_WORKFLOW=false`.
- If LangGraph fails at runtime, the engine falls back to mock execution.

---

## License

MIT
