# Claudia Open Brain Substrate

Claudia's Open Brain layer is database-first. Structured rows in `_claudia/claudia.db` are the authority. Markdown is a compiled view for reading, sharing, and review.

## Scope

The first substrate is intentionally local and small. It adapts the OB1 idea of
one durable database with vector search to Claudia's local workspace:

- no Supabase requirement
- no MCP requirement
- no remote database
- local SQLite owned by Edgar at `_claudia/claudia.db`
- local embeddings through Ollama and `nomic-embed-text`
- local vector search through `sqlite-vec` when available
- BLOB plus NumPy fallback for runtimes that cannot load SQLite extensions

It adds append-only tables for:

- events
- memories
- claims
- concept links
- contradictions
- agent handoffs
- compiled views
- vector items
- vector embeddings

Each row carries provenance fields: creating agent, source type, source path, source reference, extra provenance JSON, creation time, and tags. The schema is created idempotently by `_claudia/brain.py init`.

## CLI

Use `_claudia/brain.py` for core operations:

```bash
python3 _claudia/brain.py init --sqlite-vec
python3 _claudia/brain.py ingest-event --event-type note --title "Example"
python3 _claudia/brain.py ingest-handoff --json handoff.json
python3 _claudia/brain.py query "concept"
python3 _claudia/brain.py audit
python3 _claudia/brain.py compile --query "concept" --out view.md
python3 _claudia/brain.py vector-status --check-sqlite-vec
python3 _claudia/brain.py vector-index --backend auto
python3 _claudia/brain.py vector-query "concept" --backend auto
```

Structured JSON input is preferred for agent handoffs because it preserves checked files, changed files, findings, blockers, memory updates, and recommended next action without forcing a prose-only summary.

## Automatic Capture

Durable write commands vectorize by default. Claudia should not ask Edgar to
remember a second indexing command after saving important work.

These commands save structured rows and immediately embed them:

```bash
python3 _claudia/brain.py ingest-event ...
python3 _claudia/brain.py ingest-memory ...
python3 _claudia/brain.py ingest-claim ...
python3 _claudia/brain.py link-concepts ...
python3 _claudia/brain.py record-contradiction ...
python3 _claudia/brain.py ingest-handoff --json handoff.json
python3 _claudia/brain.py capture-preference --text "..."
python3 _claudia/brain.py compile --query "concept" --out view.md
```

Use `--no-vectorize` only for offline writes or cases where Ollama should not
be touched. If Ollama is unavailable, the structured row still saves and the
CLI prints a warning; `vector-index` can backfill later.

## Vector Layer

`brain_vector_items` stores the canonical text that gets embedded for each
Open Brain row. `brain_vector_embeddings` stores a portable BLOB copy of each
embedding. When `sqlite-vec` is loadable, `_claudia/brain.py` also mirrors those
vectors into the `brain_vec0` virtual table for local KNN search inside SQLite.

The current local runtime uses:

- Python package: `sqlite-vec`
- SQLite runtime: `pysqlite3`
- Embedding model: `nomic-embed-text`
- Dimensions: 768
- Ollama endpoint: `http://localhost:11434/api/embeddings`

Run `ollama serve` before `vector-index` or `vector-query` if Ollama is not
already running.

## Operating Rule

Do not treat compiled Markdown as canonical memory. If a compiled view disagrees with a row in `_claudia/claudia.db`, update or supersede the structured row through a new append-only row, then recompile the view.

Do not treat vector rows as canonical memory either. Vectors are a search index
rebuilt from structured Open Brain rows. The structured row remains the source
of truth.

## Source Model

OB1's public guide uses Supabase/Postgres plus `pgvector`, metadata, content
fingerprints, and semantic search as the foundation. Claudia keeps the same
local-brain pattern but maps it to local SQLite plus `sqlite-vec` so Edgar owns
the database file directly.

---
Generated for: Edgar Agunias
Date: 2026-05-26
Model: GPT-5 Codex
Sources: `_claudia/system/CLAUDIA.md`, `_claudia/system/CODEX_WORKFLOW.md`, `_claudia/sop/`, `_claudia/embeddings.py`, `_claudia/claudia.db` schema, `https://openbrainsystem.com`, `https://github.com/NateBJones-Projects/OB1`, `https://github.com/asg017/sqlite-vec`
Agent: Hephaestus
---
