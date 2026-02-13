# DOCS2DB CORE PACKAGE

**OVERVIEW**: Core Python package containing the RAG pipeline logic, CLI, and database management.

## STRUCTURE
```
src/docs2db/
├── docs2db.py         # Typer CLI application (entry point)
├── ingest.py          # Document conversion (Docling)
├── chunks.py          # Text chunking & LLM context generation
├── embeddings.py      # Vector model logic (Granite/E5/etc)
├── database.py        # pgvector & PostgreSQL operations
├── db_lifecycle.py    # Podman/Docker container management
└── multiproc.py       # Parallel batch processing engine
```

## WHERE TO LOOK
| Task | Module | Description |
|------|--------|-------------|
| CLI Commands | `docs2db.py` | Command definitions and CLI-specific logic |
| Ingestion | `ingest.py` | Converts various formats to standard Docling JSON |
| Contextual Chunking | `chunks.py` | Hybrid chunking with LLM-generated context |
| Database Schema | `database.py` | pgvector schema, indexing, and loading logic |
| Batch Work | `multiproc.py` | Handles parallel execution for heavy tasks |

## CONVENTIONS
- **Idempotency**: All processing stages must check `meta.json` (hashes/timestamps) to avoid redundant work.
- **Batch Processing**: Use `BatchProcessor` from `multiproc.py` for operations involving many documents.
- **Structured Logging**: Use `structlog` for all logs to ensure machine-readability.
- **Configuration**: Use `docs2db.config.settings` for global configuration.

## ANTI-PATTERNS
- **Direct SQL**: Do not write raw SQL outside of `database.py`.
- **Manual File Loading**: Always use the paths and patterns defined in `embed.py` or `chunks.py`.
- **Sync DB calls**: Use `psycopg` async connections for database interactions.
