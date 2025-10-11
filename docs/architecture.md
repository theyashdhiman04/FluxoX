# FluxoX Architecture

**Author:** theyashdhiman04

API and flow engine documentation.

## Overview

FluxoX is a flow orchestration platform that runs multi-agent pipelines via a FastAPI backend. The system is split into API routes, a flow engine (with optional LangGraph), agents, and a SQLite persistence layer.

```
┌─────────────────────────────────────────────────────────────────┐
│                         FluxoX System                            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI Backend                          │
├─────────────┬─────────────┬─────────────────┬──────────────────┤
│   Flows     │   Agents    │     Execute     │     Metrics      │
│  Endpoints  │  Endpoints  │    Endpoints   │    Endpoints     │
└─────────────┴─────────────┴─────────────────┴──────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Flow Engine                               │
│                                                                  │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  │ Researcher  │──▶│  Processor  │──▶│  Approver   │──▶│  Optimizer  │
│  │    Agent    │   │    Agent    │   │    Agent    │   │    Agent    │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Database Layer                              │
│  workflows · workflow_executions (SQLite)                        │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### FastAPI Backend

- **Flows** – CRUD and templates for flows
- **Agents** – List agents and configs
- **Execute** – Run a flow with input data
- **Metrics** – Execution counts and system stats

### Flow Engine

The engine runs a fixed pipeline: Research → Process → Approve → Optimize. It can use:

- **Mock** – In-process simulation (default)
- **LangGraph** – Graph-based execution when enabled and available

### Agents

1. **Researcher** – Gathers and structures input for the pipeline
2. **Processor** – Core processing step
3. **Approver** – Validates results; can route back to Process or to Optimizer
4. **Optimizer** – Suggests improvements from execution metrics

### Database

SQLite stores:

- Flow definitions and status
- Execution history and metrics

## Self-improvement loop

The Optimizer uses execution results and metrics to suggest improvements, which can be fed back into future runs.
