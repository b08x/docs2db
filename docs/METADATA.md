# Document Metadata

Docs2DB stores source, processing, and provenance metadata in `.meta.json` files alongside Docling JSON documents.

## Location and Naming

Store metadata files adjacent to their corresponding Docling JSON files:
```
content/
  docs/
    guide.json          # Docling document
    guide.meta.json     # Metadata for guide.json
```

## File Structure

Metadata files are sparse; they include only fields containing data.

### Example: Full Metadata
```json
{
  "metadata_version": "1.0",
  "filesystem": {
    "original_path": "/sources/docs/guide.html",
    "size_bytes": 245680,
    "mtime": "2025-10-23T10:30:00Z",
    "detected_mime": "text/html"
  },
  "content": {
    "title": "ExampleTech 9.4 Administration Guide",
    "language": "en"
  },
  "source": {
    "source_type": "graphql",
    "source_url": "https://docs.example.com/...",
    "source_etag": "abc123def456",
    "retrieved_at": "2025-10-23T10:30:00Z",
    "retriever": "example-documentation-v1.0",
    "license": "CC-BY-SA-4.0"
  },
  "processing": {
    "source_hash": "xxh64:a1b2c3d4e5f6...",
    "ingested_at": "2025-10-23T10:31:00Z",
    "docling_version": "2.42.1"
  }
}
```

### Example: Minimal Metadata (Auto-detected only)
```json
{
  "metadata_version": "1.0",
  "filesystem": {
    "size_bytes": 12540
  },
  "processing": {
    "ingested_at": "2025-10-23T10:31:00Z",
    "docling_version": "2.42.1"
  }
}
```

## Field Descriptions

### Top Level
- `metadata_version`: Schema version (e.g., `"1.0"`).

### `filesystem` (Auto-detected)
Source file information:
- `original_path`: Full path to the original source file.
- `size_bytes`: File size in bytes.
- `mtime`: Last modification time (ISO 8601).
- `detected_mime`: MIME type detected from the file extension.

### `content` (Auto-detected)
Extracted document information:
- `title`: Document title (from Docling `name`).
- `language`: Language code (e.g., `"en"`).

### `source` (User-supplied)
Provenance information from external tools:
- `source_type`: Source type (e.g., `"graphql"`, `"web"`, `"local"`).
- `source_url`: Retrieval URL.
- `source_etag`: ETag or version identifier.
- `retrieved_at`: Retrieval timestamp (ISO 8601).
- `retriever`: Tool or version that retrieved the document.
- `license`: Content license (e.g., `"CC-BY-SA-4.0"`).

### `processing` (Auto-generated)
Processing information:
- `source_hash`: xxHash (xxh64) of the source file.
- `ingested_at`: Ingestion timestamp (ISO 8601).
- `docling_version`: Docling version used for conversion.

## Usage

### During Ingestion

The `ingest` command generates metadata for all processed documents:
```bash
uv run docs2db ingest /path/to/sources
```

### Supplying User Metadata

External tools supply metadata by calling `generate_metadata()`:

```python
from docs2db.ingest import generate_metadata

source_metadata = {
    "source_type": "graphql",
    "source_url": "https://example.com/doc",
    "source_etag": "abc123",
    "retrieved_at": "2025-10-23T10:30:00Z",
    "retriever": "my-retriever-v1.0",
    "license": "MIT"
}

generate_metadata(
    source_file=Path("/sources/doc.html"),
    content_path=Path("content/doc.json"),
    source_metadata=source_metadata
)
```

### Auditing Metadata

The `audit` command verifies metadata files:
```bash
uv run docs2db audit
```
