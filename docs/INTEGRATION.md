# Integration Guide: Using Docs2DB as a Library

External tools use Docs2DB as a library for ingestion and metadata generation.

## Key Function: `ingest_from_content()`

`ingest_from_content()` ingests in-memory content without saving intermediate files.

### Function Signature

```python
def ingest_from_content(
    content: str | bytes,
    content_path: Path,
    stream_name: str,
    source_metadata: dict[str, Any] | None = None,
    content_encoding: str = "utf-8",
) -> bool:
    """Convert in-memory content to Docling JSON and generate metadata.

    Args:
        content: The content to convert (HTML, markdown, etc.).
        content_path: Directory path for storage (creates source.json inside).
        stream_name: Stream name with extension for format detection (e.g., "doc.html").
        source_metadata: Optional source metadata (URL, ETag, license).
        content_encoding: Encoding for string content. Defaults to "utf-8".

    Returns:
        bool: True if successful.
    """
```

### Usage Example

```python
from pathlib import Path
from docs2db.ingest import ingest_from_content

# Prepare content
html_content = "<html><body><h1>My Document</h1></body></html>"

# Build source metadata (recommended)
source_metadata = {
    "source_type": "graphql",
    "source_url": "https://docs.example.com/...",
    "source_etag": "abc123",
    "retrieved_at": "2025-10-23T10:30:00Z",
    "retriever": "example-graphql-v1.0",
    "license": "CC-BY-SA-4.0",
}

# Ingest content
success = ingest_from_content(
    content=html_content,
    content_path=Path("content/documentation/exampletech/9/guide"),
    stream_name="guide.html",  # Extension defines format as HTML
    source_metadata=source_metadata,
)

if success:
    print("✅ Document ingested successfully!")
```

## What Gets Created

`ingest_from_content()` creates two files in the specified directory:

### 1. Docling JSON (`source.json`)
The structured document representation created by Docling contains:
- Document text and structure.
- Layout information.
- Extracted metadata (title, language).

### 2. Metadata file (`meta.json`)
A sparse, versioned metadata file:

```json
{
  "metadata_version": "1.0",
  "filesystem": {
    "original_path": "documentation/example/9/guide.json",
    "size_bytes": 12540
  },
  "content": {
    "title": "ExampleTech Installation Guide",
    "language": "en"
  },
  "source": {
    "source_type": "graphql",
    "source_url": "https://docs.example.com/...",
    "source_etag": "abc123",
    "retrieved_at": "2025-10-23T10:30:00Z",
    "retriever": "example-graphql-v1.0",
    "license": "CC-BY-SA-4.0"
  },
  "processing": {
    "source_hash": "xxh64:a1b2c3d4e5f6...",
    "ingested_at": "2025-10-23T10:31:00Z",
    "docling_version": "2.44.0"
  }
}
```

## Source Metadata Fields

The `source_metadata` dictionary tracks various fields. Common examples include:

| Field | Description | Example |
|-------|-------------|---------|
| `source_type` | Type of retrieval system | `"graphql"`, `"web_scrape"`, `"filesystem"` |
| `source_url` | Original document URL | `"https://docs.example.com/..."` |
| `source_etag` | HTTP ETag for changes | `"abc123"` |
| `retrieved_at` | Retrieval timestamp | `"2025-10-23T10:30:00Z"` |
| `retriever` | Retrieval tool version | `"example-graphql-v1.0"` |
| `license` | Content license | `"CC-BY-SA-4.0"`, `"MIT"` |

## Setting Up as a Dependency

### Option 1: Local Development (editable)

In `pyproject.toml`:

```toml
[project]
dependencies = [
    "docs2db",
]

[tool.uv.sources]
docs2db = { path = "../docs2db", editable = true }
```

### Option 2: Git Repository

```toml
[project]
dependencies = [
    "docs2db @ git+https://github.com/rhel-lightspeed/docs2db.git",
]
```

### Option 3: PyPI

```toml
[project]
dependencies = [
    "docs2db>=0.1.0",
]
```
