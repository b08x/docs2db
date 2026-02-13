# PROJECT KNOWLEDGE BASE

**Generated:** 2026-02-13
**Stack:** Python 3.12, Typer, Docling, PostgreSQL/pgvector

## OVERVIEW
Docs2DB builds a RAG database from documents. It processes documents into chunks and embeddings, loads them into PostgreSQL with pgvector, and produces portable SQL dumps.

## STRUCTURE
```
docs2db/
├── src/docs2db/    # Core processing logic (ingest, chunk, embed, load)
├── tests/          # Pytest suite with database integration
├── scripts/        # Demo and utility scripts
└── docs2db_content/ # (Local) Intermediate processing artifacts
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| CLI Entry | `src/docs2db/docs2db.py` | Typer application defining all commands |
| Ingestion | `src/docs2db/ingest.py` | Document conversion using Docling |
| Chunking | `src/docs2db/chunks.py` | Text splitting with LLM context generation |
| Embedding | `src/docs2db/embed.py` | Vector generation (Granite/E5 models) |
| DB Logic | `src/docs2db/database.py` | Pgvector loading and schema management |
| DB Lifecycle | `src/docs2db/db_lifecycle.py` | Podman/Docker container management |

## CODE MAP
| Symbol | Type | Location | Role |
|--------|------|----------|------|
| `ingest` | Command | `src/docs2db/docs2db.py` | Main ingestion entry |
| `chunk` | Command | `src/docs2db/docs2db.py` | Chunking entry |
| `embed` | Command | `src/docs2db/docs2db.py` | Embedding entry |
| `pipeline` | Command | `src/docs2db/docs2db.py` | Full workflow execution |

## CONVENTIONS
- **UV Managed**: Use `uv run` or `uv sync` for dev.
- **Idempotency**: All stages check file hashes/timestamps to skip existing work.
- **Logging**: Uses `structlog` for structured, machine-readable logs.
- **DB Management**: Automatically manages a temporary PG instance via Podman/Docker.

## ANTI-PATTERNS (THIS PROJECT)
- **Direct DB interaction**: Use `db_lifecycle.py` and `database.py` abstractions.
- **Manual pip/npm**: Use `uv` for all dependency management.
- **Git Interactive**: Avoid `git commit -i` or similar interactive flags.

## COMMANDS
```bash
make test               # Run all tests
docs2db pipeline <path> # Run full RAG build
docs2db db-start        # Start development database
```
