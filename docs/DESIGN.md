# Docs2DB Design

## Philosophy

Docs2DB applies opinionated defaults to simplify RAG database creation. It makes sensible choices to minimize configuration requirements.

## Architecture

```
docs2db (builds databases) → docs2db-api (serves RAG queries)
```

### Separation of Concerns

- **docs2db**: Processes documents and builds PostgreSQL databases.
- **[docs2db-api](https://github.com/rhel-lightspeed/docs2db-api)**: Reads databases and provides RAG endpoints.

Self-describing databases store all retrieval metadata, including model names and embedding dimensions. Consequently, docs2db-api requires no configuration flags; it adapts to the connected database.

## Source of Truth

Files on disk, not the database, serve as the source of truth. The file structure provides:
- A processing cache for experimentation.
- An integration point for external tools.
- A disaster recovery mechanism.
- An audit trail.

The database serves as the production artifact built from these files.

## Pipeline

### 1. Ingest
Convert source documents to Docling JSON:
```bash
uv run docs2db ingest path/to/files
```
**Output**:
- `content/**/*.json` (Docling documents)
- `content/**/*.meta.json` (metadata: filesystem, content, source provenance)

### 2. Chunk
Split documents into semantic chunks with LLM-generated context:
```bash
uv run docs2db chunk
```
**Output**: `content/**/*.chunks.json` (contextual chunks)

**Features**:
- Hybrid chunking (structure and token-based).
- LLM-generated contextual enrichment.
- Map-reduce summarization for large documents.

### 3. Embed
Generate vector embeddings for each chunk:
```bash
uv run docs2db embed
```
**Output**: `content/**/*.gran.json` (embeddings and metadata)

**Defaults**: Granite embedding models (30M params, 384 dimensions).

### 4. Load
Store data in PostgreSQL with pgvector:
```bash
uv run docs2db load
```
**Output**: PostgreSQL database containing documents, chunks, embeddings, and metadata.

**Features**:
- Full-text search (tsvector and GIN indexes).
- Vector similarity search (pgvector).
- Self-describing schema with model metadata.

### 5. Dump/Restore
Share databases as SQL dumps:
```bash
uv run docs2db db-dump      # Creates ragdb_dump.sql
uv run docs2db db-restore   # Loads from SQL dump
```

### 6. Serve ([docs2db-api](https://github.com/rhel-lightspeed/docs2db-api))
Query the database via REST API:
```python
# docs2db-api reads the database
# Auto-detects models, dimensions, and configuration
# Provides hybrid search (BM25 and vector) with reranking
```

## Key Design Decisions

1. **Opinionated defaults**: Enable modern RAG techniques (contextual chunks, hybrid search, reranking) by default.
2. **Self-describing databases**: Store metadata in the schema for automatic API adaptation.
3. **File-based workflow**: Facilitate experimentation, debugging, and integration.
4. **Separation of build/serve**: Decouple different concerns into specialized tools.
5. **Reproducible builds**: Ensure identical files always produce the same database.

## Extension Points

- **Custom retrievers**: Place Docling JSONs in `content/` with optional `.meta.json` files.
- **Custom chunkers**: Generate `.chunks.json` files.
- **Custom embedders**: Provide `.gran.json` files.
- **Source tracking**: Pass a `source_metadata` dictionary to `generate_metadata()` (see `docs/METADATA.md`).
- **Multiple databases**: Build specialized subsets for different deployments.
