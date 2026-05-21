.PHONY: test test-ci lint db-up-test db-down-test db-destroy-test clean help

test:
	uv run pytest

test-ci:
	uv run pytest -m "not no_ci"

lint:
	uv run pre-commit run --all-files

clean:
	rm -rf .pytest_cache .ruff_cache htmlcov .coverage

# Test database targets (separate from production database)
# Uses --profile test, different port (5433), and separate volumes
db-up-test:
	podman compose -f postgres-compose.yml --profile test up -d

db-down-test:
	podman compose -f postgres-compose.yml --profile test down

db-destroy-test:
	$(MAKE) db-down-test
	podman volume rm docs2db_test_pgdata || true

help:
	@echo "Available targets:"
	@echo "  test            - Run all tests"
	@echo "  test-ci         - Run CI tests (excluding no_ci marked tests)"
	@echo "  lint            - Run all pre-commit checks (ruff, pyright, etc.)"
	@echo "  clean           - Remove generated files"
	@echo "  db-up-test      - Start test database"
	@echo "  db-down-test    - Stop test database"
	@echo "  db-destroy-test - Stop test database and remove volumes"
