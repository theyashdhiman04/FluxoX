# FluxoX

Multi-agent flow orchestration platform. Define flows, run them via REST, and optionally use LangGraph for graph-based execution.

---

## Author

**Yash Dhiman**  
GitHub: [theyashdhiman04](https://github.com/theyashdhiman04)

---

## Quick start

```bash
git clone https://github.com/theyashdhiman04/FluxoX.git
cd FluxoX
cp backend/.env.sample backend/.env   # optional
make setup-and-run
```

API docs: **http://localhost:8000/docs**

---

## Features

- Flow engine with configurable mock or LangGraph backend
- REST API: `/flows`, `/agents`, `/execute`, `/metrics`, `/health`
- Agents: Researcher, Processor, Approver, Optimizer
- SQLite persistence for flows and metrics
- JWT auth and optional rate limiting
- Pytest suite and Docker deployment

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
| POST | `/execute` | Execute a flow |
| GET | `/metrics` | Metrics |
| GET | `/health` | Health check |

---

## Local development

```bash
make create-env
conda activate fluxox
make init-db
make run-backend
make run-demo
```

---

## Docker

```bash
make docker-build
make docker-up
make docker-down
```

---

## Configuration

Use `backend/.env` or environment variables: `ENVIRONMENT`, `USE_MOCK_WORKFLOW`, `DATABASE_URL`, `LOG_LEVEL`, `SECRET_KEY`, `CORS_ALLOWED_ORIGINS`. See `backend/.env.sample`.

---

## Project layout

```
FluxoX/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── flow/
│   │   ├── database/
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
| `make create-env` | Create conda env |
| `make init-db` | Initialize DB |
| `make run-backend` | Start API server |
| `make run-demo` | Run demo script |
| `make test-backend` | Run tests |
| `make docker-build` / `docker-up` / `docker-down` | Docker lifecycle |
| `make setup-and-run` | Setup and run backend |

---

## LangGraph

Default is mock execution. Set `USE_MOCK_WORKFLOW=false` to use LangGraph; the engine falls back to mock if LangGraph fails.

---

## License

MIT
