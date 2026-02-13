# DOCS2DB TEST SUITE

**OVERVIEW**: Pytest-based suite for verifying ingestion, chunking, embedding, and database integration.

## STRUCTURE
```
tests/
├── conftest.py                # Database fixtures and setup
├── test_high_level_integration.py # E2E pipeline tests
├── test_database.py           # SQL/pgvector specific tests
├── fixtures/                  # Test documents and data
└── test_config.py             # Test-specific configuration
```

## WHERE TO LOOK
| Goal | Location | Description |
|------|----------|-------------|
| Database Fixtures | `conftest.py` | Fresh PG instance creation for each test |
| Pipeline E2E | `test_high_level_integration.py` | Tests full flow from PDF to vector DB |
| CLI Verification | `test_cli_integration.py` | Tests the Typer CLI commands |
| Document Logic | `test_document_needs_update.py` | Verifies idempotency and hash checks |

## CONVENTIONS
- **Async Testing**: Use `pytest-asyncio` for all database tests.
- **Clean State**: `setup_clean_database` fixture in `conftest.py` ensures isolation by recreating the test DB.
- **Markers**: Use `@pytest.mark.no_ci` for tests that require Podman/Docker or heavy local setup.
- **Test DB Port**: Defaults to `5433` to avoid conflict with production databases.

## ANTI-PATTERNS
- **Prod DB Access**: NEVER run tests against a production database.
- **Fixture Bloat**: Avoid defining fixtures globally if they are only needed in one module.
- **Skipping Cleanup**: Always ensure database connections are closed and test DBs are dropped.
