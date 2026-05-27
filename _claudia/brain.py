#!/usr/bin/env python3
"""
Claudia Open Brain CLI.

The database is authoritative. Markdown views are compiled from structured rows.

Usage:
    python3 _claudia/brain.py init
    python3 _claudia/brain.py ingest-event --event-type note --title "..."
    python3 _claudia/brain.py ingest-handoff --json handoff.json
    python3 _claudia/brain.py query "deadline"
    python3 _claudia/brain.py audit
    python3 _claudia/brain.py compile --query "GPCO 410" --out view.md
"""

import argparse
import hashlib
import json
import re
import struct
import sys
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib import error as urlerror
from urllib import request as urlrequest

try:
    import pysqlite3 as sqlite3
except ImportError:
    import sqlite3

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DB_PATH = SCRIPT_DIR / "claudia.db"
PREFERENCES_PATH = SCRIPT_DIR / "memory" / "preferences.md"
MANIFEST_PATH = SCRIPT_DIR / "system" / "manifest.json"
OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"
EMBED_DIM = 768
VEC_TABLE = "brain_vec0"

OPEN_BRAIN_TABLES = [
    "brain_events",
    "brain_memories",
    "brain_claims",
    "brain_concept_links",
    "brain_contradictions",
    "brain_agent_handoffs",
    "brain_compiled_views",
    "brain_vector_items",
    "brain_vector_embeddings",
]

QUERY_TABLES = {
    "events": {
        "table": "brain_events",
        "label": "event",
        "text": ["event_type", "title", "body", "subject", "tags"],
        "display": ["event_type", "title", "body", "subject"],
    },
    "memories": {
        "table": "brain_memories",
        "label": "memory",
        "text": ["memory_type", "title", "body", "tags"],
        "display": ["memory_type", "title", "body"],
    },
    "claims": {
        "table": "brain_claims",
        "label": "claim",
        "text": ["claim_text", "subject", "predicate", "object", "evidence", "tags"],
        "display": ["claim_text", "subject", "predicate", "object"],
    },
    "links": {
        "table": "brain_concept_links",
        "label": "link",
        "text": ["concept_a", "concept_b", "relation", "rationale", "tags"],
        "display": ["concept_a", "relation", "concept_b", "rationale"],
    },
    "contradictions": {
        "table": "brain_contradictions",
        "label": "contradiction",
        "text": ["summary", "details", "evidence", "tags"],
        "display": ["summary", "resolution_status", "details"],
    },
    "handoffs": {
        "table": "brain_agent_handoffs",
        "label": "handoff",
        "text": [
            "agent",
            "status",
            "task_title",
            "summary",
            "key_findings_json",
            "blockers",
            "recommended_next_action",
            "tags",
        ],
        "display": ["agent", "status", "task_title", "summary"],
    },
    "views": {
        "table": "brain_compiled_views",
        "label": "view",
        "text": ["view_type", "title", "query", "body", "output_path", "tags"],
        "display": ["view_type", "title", "query", "output_path"],
    },
}

COMPILE_TABLE_KEYS = [
    "claims",
    "memories",
    "events",
    "links",
    "contradictions",
    "handoffs",
]

SCHEMA_SQL = [
    """
    CREATE TABLE IF NOT EXISTS brain_events (
        id INTEGER PRIMARY KEY,
        uuid TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
        created_by_agent TEXT,
        source_type TEXT,
        source_path TEXT,
        source_ref TEXT,
        provenance_json TEXT NOT NULL DEFAULT '{}',
        event_type TEXT NOT NULL,
        title TEXT,
        body TEXT,
        subject TEXT,
        event_time TEXT,
        importance INTEGER DEFAULT 0,
        confidence TEXT,
        status TEXT NOT NULL DEFAULT 'active',
        tags TEXT NOT NULL DEFAULT '[]'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS brain_memories (
        id INTEGER PRIMARY KEY,
        uuid TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
        created_by_agent TEXT,
        source_type TEXT,
        source_path TEXT,
        source_ref TEXT,
        provenance_json TEXT NOT NULL DEFAULT '{}',
        memory_type TEXT NOT NULL DEFAULT 'note',
        title TEXT,
        body TEXT NOT NULL,
        importance INTEGER DEFAULT 0,
        confidence TEXT,
        status TEXT NOT NULL DEFAULT 'active',
        valid_from TEXT,
        valid_until TEXT,
        review_after TEXT,
        tags TEXT NOT NULL DEFAULT '[]'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS brain_claims (
        id INTEGER PRIMARY KEY,
        uuid TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
        created_by_agent TEXT,
        source_type TEXT,
        source_path TEXT,
        source_ref TEXT,
        provenance_json TEXT NOT NULL DEFAULT '{}',
        claim_text TEXT NOT NULL,
        subject TEXT,
        predicate TEXT,
        object TEXT,
        qualifier TEXT,
        evidence TEXT,
        importance INTEGER DEFAULT 0,
        confidence TEXT,
        status TEXT NOT NULL DEFAULT 'active',
        valid_from TEXT,
        valid_until TEXT,
        review_after TEXT,
        tags TEXT NOT NULL DEFAULT '[]'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS brain_concept_links (
        id INTEGER PRIMARY KEY,
        uuid TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
        created_by_agent TEXT,
        source_type TEXT,
        source_path TEXT,
        source_ref TEXT,
        provenance_json TEXT NOT NULL DEFAULT '{}',
        concept_a TEXT NOT NULL,
        concept_b TEXT NOT NULL,
        relation TEXT NOT NULL DEFAULT 'related_to',
        rationale TEXT,
        weight REAL DEFAULT 1.0,
        confidence TEXT,
        status TEXT NOT NULL DEFAULT 'active',
        tags TEXT NOT NULL DEFAULT '[]'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS brain_contradictions (
        id INTEGER PRIMARY KEY,
        uuid TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
        created_by_agent TEXT,
        source_type TEXT,
        source_path TEXT,
        source_ref TEXT,
        provenance_json TEXT NOT NULL DEFAULT '{}',
        claim_id_a INTEGER REFERENCES brain_claims(id),
        claim_id_b INTEGER REFERENCES brain_claims(id),
        summary TEXT NOT NULL,
        details TEXT,
        evidence TEXT,
        severity TEXT,
        confidence TEXT,
        resolution_status TEXT NOT NULL DEFAULT 'open',
        tags TEXT NOT NULL DEFAULT '[]'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS brain_agent_handoffs (
        id INTEGER PRIMARY KEY,
        uuid TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
        created_by_agent TEXT,
        source_type TEXT,
        source_path TEXT,
        source_ref TEXT,
        provenance_json TEXT NOT NULL DEFAULT '{}',
        event_id INTEGER REFERENCES brain_events(id),
        agent TEXT NOT NULL,
        status TEXT NOT NULL,
        task_title TEXT,
        summary TEXT,
        files_checked_json TEXT NOT NULL DEFAULT '[]',
        files_changed_json TEXT NOT NULL DEFAULT '[]',
        key_findings_json TEXT NOT NULL DEFAULT '[]',
        blockers TEXT,
        memory_updated_json TEXT NOT NULL DEFAULT '[]',
        recommended_next_action TEXT,
        payload_json TEXT NOT NULL DEFAULT '{}',
        tags TEXT NOT NULL DEFAULT '[]'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS brain_compiled_views (
        id INTEGER PRIMARY KEY,
        uuid TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
        created_by_agent TEXT,
        source_type TEXT,
        source_path TEXT,
        source_ref TEXT,
        provenance_json TEXT NOT NULL DEFAULT '{}',
        view_type TEXT NOT NULL DEFAULT 'markdown',
        title TEXT NOT NULL,
        query TEXT,
        body TEXT NOT NULL,
        output_path TEXT,
        source_rows_json TEXT NOT NULL DEFAULT '[]',
        status TEXT NOT NULL DEFAULT 'compiled',
        tags TEXT NOT NULL DEFAULT '[]'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS brain_vector_items (
        id INTEGER PRIMARY KEY,
        uuid TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
        updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
        source_table TEXT NOT NULL,
        source_id INTEGER NOT NULL,
        source_uuid TEXT,
        content TEXT NOT NULL,
        content_hash TEXT NOT NULL,
        metadata_json TEXT NOT NULL DEFAULT '{}',
        embedded_at TEXT,
        embedding_model TEXT,
        embedding_dim INTEGER,
        vector_backend TEXT NOT NULL DEFAULT 'blob',
        status TEXT NOT NULL DEFAULT 'active',
        UNIQUE (source_table, source_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS brain_vector_embeddings (
        item_id INTEGER PRIMARY KEY REFERENCES brain_vector_items(id) ON DELETE CASCADE,
        embedding BLOB NOT NULL,
        embedding_model TEXT NOT NULL,
        embedding_dim INTEGER NOT NULL,
        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_brain_events_type ON brain_events(event_type)",
    "CREATE INDEX IF NOT EXISTS idx_brain_events_created ON brain_events(created_at)",
    "CREATE INDEX IF NOT EXISTS idx_brain_memories_type ON brain_memories(memory_type)",
    "CREATE INDEX IF NOT EXISTS idx_brain_memories_review ON brain_memories(review_after)",
    "CREATE INDEX IF NOT EXISTS idx_brain_claims_subject ON brain_claims(subject, predicate)",
    "CREATE INDEX IF NOT EXISTS idx_brain_claims_review ON brain_claims(review_after)",
    "CREATE INDEX IF NOT EXISTS idx_brain_links_concepts ON brain_concept_links(concept_a, concept_b)",
    "CREATE INDEX IF NOT EXISTS idx_brain_contradictions_status ON brain_contradictions(resolution_status)",
    "CREATE INDEX IF NOT EXISTS idx_brain_handoffs_agent ON brain_agent_handoffs(agent, status)",
    "CREATE INDEX IF NOT EXISTS idx_brain_views_query ON brain_compiled_views(query)",
    "CREATE INDEX IF NOT EXISTS idx_brain_vector_items_source ON brain_vector_items(source_table, source_id)",
    "CREATE INDEX IF NOT EXISTS idx_brain_vector_items_hash ON brain_vector_items(content_hash)",
    "CREATE INDEX IF NOT EXISTS idx_brain_vector_items_status ON brain_vector_items(status, embedded_at)",
]


def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today_text():
    return date.today().isoformat()


def resolve_workspace_path(path):
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def load_manifest():
    if not MANIFEST_PATH.exists():
        return {}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def agent_memory_path(agent_name):
    manifest = load_manifest()
    for agent in manifest.get("agents", []):
        if agent.get("name", "").lower() == agent_name.lower():
            memory = agent.get("memory", "")
            if memory:
                return resolve_workspace_path(memory)
    return SCRIPT_DIR / "agents" / agent_name.lower()


def append_block(path, block):
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    spacer = "\n\n" if existing and not existing.endswith("\n\n") else ""
    path.write_text(existing + spacer + block.strip() + "\n", encoding="utf-8")


def connect_db(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_schema(conn):
    for sql in SCHEMA_SQL:
        conn.execute(sql)
    conn.commit()


def load_sqlite_vec(conn):
    try:
        import sqlite_vec
    except ImportError as exc:
        return False, f"sqlite_vec Python package is not installed: {exc}"
    try:
        sqlite_vec.load(conn)
    except Exception as exc:
        return False, f"sqlite_vec could not be loaded by this Python/SQLite build: {exc}"
    return True, "sqlite_vec loaded"


def ensure_sqlite_vec_schema(conn):
    loaded, message = load_sqlite_vec(conn)
    if not loaded:
        return False, message
    try:
        conn.execute(
            f"CREATE VIRTUAL TABLE IF NOT EXISTS {VEC_TABLE} "
            f"USING vec0(embedding float[{EMBED_DIM}])"
        )
        conn.commit()
    except sqlite3.Error as exc:
        return False, f"sqlite_vec vec0 table could not be created: {exc}"
    return True, f"{VEC_TABLE} ready"


def sqlite_vec_ready(conn):
    row = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (VEC_TABLE,),
    ).fetchone()
    if row is None:
        return False
    loaded, _ = load_sqlite_vec(conn)
    return loaded


def check_ollama():
    try:
        with urlrequest.urlopen("http://localhost:11434/api/tags", timeout=5):
            pass
    except (urlerror.URLError, ConnectionRefusedError, OSError) as exc:
        raise SystemExit(f"Error: Ollama is not running or reachable: {exc}")


def embed_text(text):
    payload = json.dumps({"model": EMBED_MODEL, "prompt": text}).encode("utf-8")
    req = urlrequest.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urlrequest.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    vec = data.get("embedding")
    if not isinstance(vec, list) or len(vec) != EMBED_DIM:
        raise RuntimeError(f"Expected {EMBED_DIM}-dimension embedding, got {len(vec) if isinstance(vec, list) else 'none'}")
    return [float(item) for item in vec]


def serialize_embedding(vec):
    return struct.pack(f"<{EMBED_DIM}f", *vec)


def deserialize_embedding(blob):
    if len(blob) != EMBED_DIM * 4:
        raise ValueError(f"Expected {EMBED_DIM * 4} bytes, got {len(blob)}")
    return struct.unpack(f"<{EMBED_DIM}f", blob)


def normalized_hash(text):
    compacted = re.sub(r"\s+", " ", str(text or "")).strip().lower()
    return hashlib.sha256(compacted.encode("utf-8")).hexdigest()


def vector_content_for_row(key, row):
    config = QUERY_TABLES[key]
    parts = [f"kind: {config['label']}"]
    for col in config["text"]:
        if col in row.keys() and row[col]:
            parts.append(f"{col}: {row[col]}")
    return "\n".join(parts).strip()


def vector_metadata_for_row(key, row):
    fields = {
        "kind": QUERY_TABLES[key]["label"],
        "source_table": QUERY_TABLES[key]["table"],
        "source_id": row["id"],
    }
    for col in ("uuid", "created_at", "created_by_agent", "source_type", "source_path", "source_ref"):
        if col in row.keys() and row[col]:
            fields[col] = row[col]
    return fields


def vector_select_columns(key):
    config = QUERY_TABLES[key]
    columns = ["id", "uuid", "created_at", "created_by_agent", "source_type", "source_path", "source_ref"]
    for col in config["text"]:
        if col not in columns:
            columns.append(col)
    return columns


def vector_source_rows(conn, table_key="all", limit=0):
    keys = list(QUERY_TABLES) if table_key == "all" else [table_key]
    rows = []
    for key in keys:
        config = QUERY_TABLES[key]
        table = config["table"]
        columns = vector_select_columns(key)
        sql = f"SELECT {', '.join(columns)} FROM {table} ORDER BY id"
        params = ()
        if limit:
            sql += " LIMIT ?"
            params = (limit,)
        for row in conn.execute(sql, params).fetchall():
            content = vector_content_for_row(key, row)
            if content:
                rows.append((key, row, content))
    return rows


def vector_source_row(conn, key, row_id):
    config = QUERY_TABLES[key]
    table = config["table"]
    columns = vector_select_columns(key)
    row = conn.execute(
        f"SELECT {', '.join(columns)} FROM {table} WHERE id = ?",
        (row_id,),
    ).fetchone()
    if row is None:
        return None
    content = vector_content_for_row(key, row)
    if not content:
        return None
    return key, row, content


def upsert_vector_item(conn, key, row, content, backend):
    table = QUERY_TABLES[key]["table"]
    digest = normalized_hash(content)
    metadata = vector_metadata_for_row(key, row)
    existing = conn.execute(
        """
        SELECT id, content_hash, embedded_at, embedding_model, embedding_dim
        FROM brain_vector_items
        WHERE source_table = ? AND source_id = ?
        """,
        (table, row["id"]),
    ).fetchone()
    if existing:
        conn.execute(
            """
            UPDATE brain_vector_items
            SET updated_at = ?, source_uuid = ?, content = ?, content_hash = ?,
                metadata_json = ?, vector_backend = ?, status = 'active'
            WHERE id = ?
            """,
            (
                now_utc(),
                row["uuid"] if "uuid" in row.keys() else "",
                content,
                digest,
                json_text(metadata, "{}"),
                backend,
                existing["id"],
            ),
        )
        return existing["id"], existing, digest
    cur = conn.execute(
        """
        INSERT INTO brain_vector_items
        (uuid, created_at, updated_at, source_table, source_id, source_uuid, content,
         content_hash, metadata_json, embedding_model, embedding_dim, vector_backend, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
        """,
        (
            str(uuid.uuid4()),
            now_utc(),
            now_utc(),
            table,
            row["id"],
            row["uuid"] if "uuid" in row.keys() else "",
            content,
            digest,
            json_text(metadata, "{}"),
            EMBED_MODEL,
            EMBED_DIM,
            backend,
        ),
    )
    return cur.lastrowid, None, digest


def upsert_legacy_vector_item(conn, row, backend):
    source_id = row["id"]
    source_table = "embeddings"
    source_path = row["source_path"] or ""
    source_type = row["source_type"] or ""
    course_code = row["course_code"] or ""
    chunk_index = row["chunk_index"] if row["chunk_index"] is not None else 0
    content = row["chunk_text"] or ""
    metadata = {
        "kind": "legacy_embedding",
        "source_table": source_table,
        "source_id": source_id,
        "source_path": source_path,
        "source_type": source_type,
        "course_code": course_code,
        "chunk_index": chunk_index,
        "model": row["model"] or EMBED_MODEL,
        "created_at": row["created_at"],
    }
    digest = normalized_hash(f"{source_path}\n{chunk_index}\n{content}")
    existing = conn.execute(
        """
        SELECT id, content_hash, embedded_at, embedding_model, embedding_dim
        FROM brain_vector_items
        WHERE source_table = ? AND source_id = ?
        """,
        (source_table, source_id),
    ).fetchone()
    if existing:
        conn.execute(
            """
            UPDATE brain_vector_items
            SET updated_at = ?, source_uuid = ?, content = ?, content_hash = ?,
                metadata_json = ?, vector_backend = ?, status = 'active'
            WHERE id = ?
            """,
            (
                now_utc(),
                "",
                content,
                digest,
                json_text(metadata, "{}"),
                backend,
                existing["id"],
            ),
        )
        return existing["id"], existing, digest
    cur = conn.execute(
        """
        INSERT INTO brain_vector_items
        (uuid, created_at, updated_at, source_table, source_id, source_uuid, content,
         content_hash, metadata_json, embedding_model, embedding_dim, vector_backend, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
        """,
        (
            str(uuid.uuid4()),
            now_utc(),
            now_utc(),
            source_table,
            source_id,
            "",
            content,
            digest,
            json_text(metadata, "{}"),
            row["model"] or EMBED_MODEL,
            EMBED_DIM,
            backend,
        ),
    )
    return cur.lastrowid, None, digest


def store_vector(conn, item_id, vec, backend):
    blob = serialize_embedding(vec)
    store_vector_blob(conn, item_id, blob, EMBED_MODEL, EMBED_DIM, backend, vec=vec)


def store_vector_blob(conn, item_id, blob, model, dim, backend, vec=None):
    conn.execute(
        """
        INSERT INTO brain_vector_embeddings
        (item_id, embedding, embedding_model, embedding_dim, created_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(item_id) DO UPDATE SET
            embedding = excluded.embedding,
            embedding_model = excluded.embedding_model,
            embedding_dim = excluded.embedding_dim,
            created_at = excluded.created_at
        """,
        (item_id, blob, model, dim, now_utc()),
    )
    if backend == "sqlite-vec":
        if vec is None:
            vec = deserialize_embedding(blob)
        conn.execute(f"DELETE FROM {VEC_TABLE} WHERE rowid = ?", (item_id,))
        conn.execute(
            f"INSERT INTO {VEC_TABLE}(rowid, embedding) VALUES (?, ?)",
            (item_id, json.dumps(list(vec), ensure_ascii=True)),
        )
    conn.execute(
        """
        UPDATE brain_vector_items
        SET embedded_at = ?, embedding_model = ?, embedding_dim = ?, vector_backend = ?
        WHERE id = ?
        """,
        (now_utc(), model, dim, backend, item_id),
    )


def cosine_search_blob(conn, query_vec, limit):
    try:
        import numpy as np
    except ImportError as exc:
        raise SystemExit(f"NumPy is required for BLOB vector search fallback: {exc}")
    rows = conn.execute(
        """
        SELECT i.id, i.source_table, i.source_id, i.content, i.metadata_json,
               e.embedding
        FROM brain_vector_items i
        JOIN brain_vector_embeddings e ON e.item_id = i.id
        WHERE i.status = 'active'
          AND e.embedding_model = ?
          AND e.embedding_dim = ?
        """,
        (EMBED_MODEL, EMBED_DIM),
    ).fetchall()
    if not rows:
        return []
    q = np.array(query_vec, dtype=np.float32)
    q_norm = max(float(np.linalg.norm(q)), 1e-10)
    scored = []
    for row in rows:
        vec = np.array(deserialize_embedding(row["embedding"]), dtype=np.float32)
        denom = max(float(np.linalg.norm(vec)) * q_norm, 1e-10)
        similarity = float((vec @ q) / denom)
        scored.append((similarity, row))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        {
            "score": score,
            "distance": None,
            "id": row["id"],
            "source_table": row["source_table"],
            "source_id": row["source_id"],
            "content": row["content"],
            "metadata": json.loads(row["metadata_json"] or "{}"),
        }
        for score, row in scored[:limit]
    ]


def search_sqlite_vec(conn, query_vec, limit):
    rows = conn.execute(
        f"""
        SELECT i.id, i.source_table, i.source_id, i.content, i.metadata_json,
               v.distance
        FROM {VEC_TABLE} v
        JOIN brain_vector_items i ON i.id = v.rowid
        WHERE v.embedding MATCH ?
          AND k = ?
          AND i.status = 'active'
        ORDER BY v.distance
        """,
        (json.dumps(query_vec, ensure_ascii=True), limit),
    ).fetchall()
    return [
        {
            "score": 1.0 / (1.0 + float(row["distance"])),
            "distance": float(row["distance"]),
            "id": row["id"],
            "source_table": row["source_table"],
            "source_id": row["source_id"],
            "content": row["content"],
            "metadata": json.loads(row["metadata_json"] or "{}"),
        }
        for row in rows
    ]


def choose_vector_backend(conn, requested):
    if requested == "blob":
        return "blob", ""
    ready, message = ensure_sqlite_vec_schema(conn)
    if ready:
        return "sqlite-vec", message
    if requested == "sqlite-vec":
        raise SystemExit(f"sqlite-vec requested but unavailable: {message}")
    return "blob", message


def index_vector_rows(conn, rows, requested_backend="auto", force=False):
    backend, backend_message = choose_vector_backend(conn, requested_backend)
    check_ollama()
    indexed = 0
    skipped = 0
    for key, row, content in rows:
        item_id, existing, digest = upsert_vector_item(conn, key, row, content, backend)
        if (
            existing
            and not force
            and existing["content_hash"] == digest
            and existing["embedded_at"]
            and existing["embedding_model"] == EMBED_MODEL
            and existing["embedding_dim"] == EMBED_DIM
        ):
            skipped += 1
            continue
        vec = embed_text(content)
        store_vector(conn, item_id, vec, backend)
        indexed += 1
    return indexed, skipped, backend, backend_message


def auto_vectorize(conn, sources, args, force=True):
    if getattr(args, "no_vectorize", False):
        return
    rows = []
    for key, row_id in sources:
        item = vector_source_row(conn, key, row_id)
        if item:
            rows.append(item)
    if not rows:
        return
    try:
        indexed, skipped, backend, backend_message = index_vector_rows(
            conn,
            rows,
            getattr(args, "vector_backend", "auto"),
            force=force,
        )
    except SystemExit as exc:
        print(f"Warning: Open Brain row saved but vectorization skipped: {exc}", file=sys.stderr)
        return
    except Exception as exc:
        print(f"Warning: Open Brain row saved but vectorization failed: {exc}", file=sys.stderr)
        return
    print(f"Vectorized {indexed} Open Brain row(s). Skipped {skipped}. Backend: {backend}.")
    if backend_message:
        print(f"Vector backend detail: {backend_message}")


def compact(text, limit=120):
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def json_text(value, empty="{}"):
    if value is None or value == "":
        return empty
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("{") or stripped.startswith("["):
            try:
                json.loads(stripped)
                return stripped
            except json.JSONDecodeError:
                pass
        return json.dumps(value, ensure_ascii=True)
    return json.dumps(value, ensure_ascii=True, sort_keys=True)


def parse_tags(value):
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("["):
            try:
                loaded = json.loads(stripped)
                if isinstance(loaded, list):
                    return [str(item).strip() for item in loaded if str(item).strip()]
            except json.JSONDecodeError:
                pass
        return [part.strip() for part in stripped.split(",") if part.strip()]
    return [str(value).strip()]


def list_value(value):
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("["):
            try:
                loaded = json.loads(stripped)
                if isinstance(loaded, list):
                    return loaded
            except json.JSONDecodeError:
                pass
        return [part.strip() for part in stripped.split(";") if part.strip()]
    return [value]


def load_json(path):
    if not path:
        return {}
    if path == "-":
        text = sys.stdin.read()
    else:
        text = Path(path).read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise SystemExit("JSON input must be an object.")
    return data


def read_text_arg(value, file_value):
    if file_value:
        return Path(file_value).read_text(encoding="utf-8")
    return value or ""


def first(data, keys, default=""):
    for key in keys:
        value = data.get(key)
        if value is not None and value != "":
            return value
    return default


def from_arg_or_data(args, data, arg_name, keys, default=""):
    value = getattr(args, arg_name, "")
    if value is not None and value != "":
        return value
    return first(data, keys, default)


def provenance_fields(args, data, agent_default=""):
    agent = from_arg_or_data(args, data, "agent", ["created_by_agent", "agent"], agent_default)
    return {
        "uuid": str(uuid.uuid4()),
        "created_at": now_utc(),
        "created_by_agent": agent,
        "source_type": from_arg_or_data(args, data, "source_type", ["source_type"], ""),
        "source_path": from_arg_or_data(args, data, "source_path", ["source_path", "path"], ""),
        "source_ref": from_arg_or_data(args, data, "source_ref", ["source_ref", "ref"], ""),
        "provenance_json": json_text(
            from_arg_or_data(args, data, "provenance_json", ["provenance_json", "provenance"], {}),
            "{}",
        ),
        "tags": json_text(parse_tags(from_arg_or_data(args, data, "tags", ["tags"], [])), "[]"),
    }


def require(value, label):
    if value is None or value == "":
        raise SystemExit(f"Error: {label} is required.")
    return value


def insert_row(conn, table, values):
    columns = list(values)
    placeholders = ", ".join("?" for _ in columns)
    names = ", ".join(columns)
    sql = f"INSERT INTO {table} ({names}) VALUES ({placeholders})"
    cur = conn.execute(sql, [values[name] for name in columns])
    return cur.lastrowid


def cmd_init(args):
    conn = connect_db(args.db)
    ensure_schema(conn)
    vec_message = ""
    if getattr(args, "sqlite_vec", False):
        _, vec_message = ensure_sqlite_vec_schema(conn)
    rows = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name LIKE 'brain_%'
        ORDER BY name
        """
    ).fetchall()
    conn.close()
    names = ", ".join(row["name"] for row in rows)
    print(f"Open Brain schema ready: {names}")
    if vec_message:
        print(f"sqlite-vec: {vec_message}")


def cmd_ingest_event(args):
    data = load_json(args.json)
    body = read_text_arg(
        from_arg_or_data(args, data, "body", ["body", "details", "content"], ""),
        args.body_file,
    )
    values = provenance_fields(args, data)
    values.update(
        {
            "event_type": require(
                from_arg_or_data(args, data, "event_type", ["event_type", "type"], "note"),
                "event type",
            ),
            "title": from_arg_or_data(args, data, "title", ["title", "summary"], ""),
            "body": body,
            "subject": from_arg_or_data(args, data, "subject", ["subject"], ""),
            "event_time": from_arg_or_data(args, data, "event_time", ["event_time", "time"], now_utc()),
            "importance": int(from_arg_or_data(args, data, "importance", ["importance"], 0) or 0),
            "confidence": from_arg_or_data(args, data, "confidence", ["confidence"], ""),
            "status": from_arg_or_data(args, data, "status", ["status"], "active"),
        }
    )
    conn = connect_db(args.db)
    ensure_schema(conn)
    row_id = insert_row(conn, "brain_events", values)
    auto_vectorize(conn, [("events", row_id)], args)
    conn.commit()
    conn.close()
    print(f"Inserted brain_event id={row_id}")


def cmd_ingest_memory(args):
    data = load_json(args.json)
    body = read_text_arg(from_arg_or_data(args, data, "body", ["body", "content"], ""), args.body_file)
    values = provenance_fields(args, data)
    values.update(
        {
            "memory_type": from_arg_or_data(args, data, "memory_type", ["memory_type", "type"], "note"),
            "title": from_arg_or_data(args, data, "title", ["title", "summary"], ""),
            "body": require(body, "memory body"),
            "importance": int(from_arg_or_data(args, data, "importance", ["importance"], 0) or 0),
            "confidence": from_arg_or_data(args, data, "confidence", ["confidence"], ""),
            "status": from_arg_or_data(args, data, "status", ["status"], "active"),
            "valid_from": from_arg_or_data(args, data, "valid_from", ["valid_from"], ""),
            "valid_until": from_arg_or_data(args, data, "valid_until", ["valid_until"], ""),
            "review_after": from_arg_or_data(args, data, "review_after", ["review_after"], ""),
        }
    )
    conn = connect_db(args.db)
    ensure_schema(conn)
    row_id = insert_row(conn, "brain_memories", values)
    auto_vectorize(conn, [("memories", row_id)], args)
    conn.commit()
    conn.close()
    print(f"Inserted brain_memory id={row_id}")


def cmd_ingest_claim(args):
    data = load_json(args.json)
    claim_text = from_arg_or_data(args, data, "claim_text", ["claim_text", "claim", "summary"], "")
    values = provenance_fields(args, data)
    values.update(
        {
            "claim_text": require(claim_text, "claim text"),
            "subject": from_arg_or_data(args, data, "subject", ["subject"], ""),
            "predicate": from_arg_or_data(args, data, "predicate", ["predicate"], ""),
            "object": from_arg_or_data(args, data, "object", ["object"], ""),
            "qualifier": from_arg_or_data(args, data, "qualifier", ["qualifier"], ""),
            "evidence": from_arg_or_data(args, data, "evidence", ["evidence"], ""),
            "importance": int(from_arg_or_data(args, data, "importance", ["importance"], 0) or 0),
            "confidence": from_arg_or_data(args, data, "confidence", ["confidence"], ""),
            "status": from_arg_or_data(args, data, "status", ["status"], "active"),
            "valid_from": from_arg_or_data(args, data, "valid_from", ["valid_from"], ""),
            "valid_until": from_arg_or_data(args, data, "valid_until", ["valid_until"], ""),
            "review_after": from_arg_or_data(args, data, "review_after", ["review_after"], ""),
        }
    )
    conn = connect_db(args.db)
    ensure_schema(conn)
    row_id = insert_row(conn, "brain_claims", values)
    auto_vectorize(conn, [("claims", row_id)], args)
    conn.commit()
    conn.close()
    print(f"Inserted brain_claim id={row_id}")


def cmd_link_concepts(args):
    data = load_json(args.json)
    values = provenance_fields(args, data)
    values.update(
        {
            "concept_a": require(from_arg_or_data(args, data, "concept_a", ["concept_a", "from"], ""), "concept a"),
            "concept_b": require(from_arg_or_data(args, data, "concept_b", ["concept_b", "to"], ""), "concept b"),
            "relation": from_arg_or_data(args, data, "relation", ["relation"], "related_to"),
            "rationale": from_arg_or_data(args, data, "rationale", ["rationale", "summary"], ""),
            "weight": float(from_arg_or_data(args, data, "weight", ["weight"], 1.0) or 1.0),
            "confidence": from_arg_or_data(args, data, "confidence", ["confidence"], ""),
            "status": from_arg_or_data(args, data, "status", ["status"], "active"),
        }
    )
    conn = connect_db(args.db)
    ensure_schema(conn)
    row_id = insert_row(conn, "brain_concept_links", values)
    auto_vectorize(conn, [("links", row_id)], args)
    conn.commit()
    conn.close()
    print(f"Inserted brain_concept_link id={row_id}")


def cmd_record_contradiction(args):
    data = load_json(args.json)
    values = provenance_fields(args, data)
    claim_id_a = from_arg_or_data(args, data, "claim_id_a", ["claim_id_a"], "")
    claim_id_b = from_arg_or_data(args, data, "claim_id_b", ["claim_id_b"], "")
    values.update(
        {
            "claim_id_a": int(claim_id_a) if claim_id_a else None,
            "claim_id_b": int(claim_id_b) if claim_id_b else None,
            "summary": require(from_arg_or_data(args, data, "summary", ["summary", "title"], ""), "summary"),
            "details": from_arg_or_data(args, data, "details", ["details", "body"], ""),
            "evidence": from_arg_or_data(args, data, "evidence", ["evidence"], ""),
            "severity": from_arg_or_data(args, data, "severity", ["severity"], ""),
            "confidence": from_arg_or_data(args, data, "confidence", ["confidence"], ""),
            "resolution_status": from_arg_or_data(args, data, "resolution_status", ["resolution_status", "status"], "open"),
        }
    )
    conn = connect_db(args.db)
    ensure_schema(conn)
    row_id = insert_row(conn, "brain_contradictions", values)
    auto_vectorize(conn, [("contradictions", row_id)], args)
    conn.commit()
    conn.close()
    print(f"Inserted brain_contradiction id={row_id}")


def cmd_ingest_handoff(args):
    data = load_json(args.json)
    agent = require(from_arg_or_data(args, data, "handoff_agent", ["agent"], ""), "agent")
    status = require(from_arg_or_data(args, data, "status", ["status"], ""), "status")
    task_title = from_arg_or_data(args, data, "task_title", ["task_title", "title"], "")
    summary = from_arg_or_data(args, data, "summary", ["summary", "what_was_done"], "")
    values = provenance_fields(args, data, agent_default=agent)
    conn = connect_db(args.db)
    ensure_schema(conn)
    event_values = dict(values)
    event_values.update(
        {
            "event_type": "agent_handoff",
            "title": task_title or f"{agent} handoff",
            "body": summary,
            "subject": agent,
            "event_time": now_utc(),
            "importance": int(from_arg_or_data(args, data, "importance", ["importance"], 0) or 0),
            "confidence": from_arg_or_data(args, data, "confidence", ["confidence"], ""),
            "status": status,
        }
    )
    event_id = insert_row(conn, "brain_events", event_values)
    handoff_values = dict(values)
    handoff_values.update(
        {
            "event_id": event_id,
            "agent": agent,
            "status": status,
            "task_title": task_title,
            "summary": summary,
            "files_checked_json": json_text(list_value(from_arg_or_data(args, data, "files_checked", ["files_checked"], [])), "[]"),
            "files_changed_json": json_text(list_value(from_arg_or_data(args, data, "files_changed", ["files_changed"], [])), "[]"),
            "key_findings_json": json_text(list_value(from_arg_or_data(args, data, "key_findings", ["key_findings"], [])), "[]"),
            "blockers": from_arg_or_data(args, data, "blockers", ["blockers", "blockers_or_ambiguity"], ""),
            "memory_updated_json": json_text(list_value(from_arg_or_data(args, data, "memory_updated", ["memory_updated"], [])), "[]"),
            "recommended_next_action": from_arg_or_data(args, data, "recommended_next_action", ["recommended_next_action"], ""),
            "payload_json": json_text(data, "{}"),
        }
    )
    row_id = insert_row(conn, "brain_agent_handoffs", handoff_values)
    auto_vectorize(conn, [("events", event_id), ("handoffs", row_id)], args)
    conn.commit()
    conn.close()
    print(f"Inserted brain_agent_handoff id={row_id} event_id={event_id}")


def cmd_capture_preference(args):
    data = load_json(args.json)
    text = read_text_arg(
        from_arg_or_data(args, data, "text", ["text", "body", "preference", "rule"], ""),
        args.body_file,
    )
    text = require(text.strip(), "preference text")
    title = from_arg_or_data(args, data, "title", ["title"], compact(text, 64))
    preference_type = from_arg_or_data(args, data, "preference_type", ["preference_type", "type"], "preference")
    scope = from_arg_or_data(args, data, "scope", ["scope"], args.scope)
    target_agent = from_arg_or_data(args, data, "target_agent", ["target_agent"], args.target_agent)
    target_path_arg = from_arg_or_data(args, data, "target_path", ["target_path"], args.target_path)

    if target_path_arg:
        target_path = resolve_workspace_path(target_path_arg)
    elif scope == "agent":
        if not target_agent:
            raise SystemExit("Error: --target-agent is required when --scope agent.")
        target_path = agent_memory_path(target_agent) / "FEEDBACK.md"
    else:
        target_path = PREFERENCES_PATH

    if scope == "agent":
        block = f"""### {today_text()} - {title}
**Type:** {preference_type}
**What:** {text}
**Why:** Captured as durable Edgar preference through Open Brain.
**Rule going forward:** {text}"""
    else:
        block = f"""### {today_text()} - {title}
{text}"""
    append_block(target_path, block)

    values = provenance_fields(
        args,
        {
            "agent": args.agent or "Claudia",
            "source_type": "user_preference",
            "source_path": str(target_path.relative_to(ROOT)) if target_path.is_relative_to(ROOT) else str(target_path),
            "tags": parse_tags(args.tags) + ["preference", scope],
        },
    )
    values.update(
        {
            "memory_type": "preference",
            "title": title,
            "body": text,
            "importance": int(from_arg_or_data(args, data, "importance", ["importance"], 5) or 5),
            "confidence": from_arg_or_data(args, data, "confidence", ["confidence"], "user_confirmed"),
            "status": "active",
            "valid_from": today_text(),
            "valid_until": "",
            "review_after": "",
        }
    )
    conn = connect_db(args.db)
    ensure_schema(conn)
    row_id = insert_row(conn, "brain_memories", values)
    auto_vectorize(conn, [("memories", row_id)], args)
    conn.commit()
    conn.close()
    print(f"Captured preference in {target_path}")
    print(f"Inserted brain_memory id={row_id}")


def query_table(conn, key, term="", limit=20):
    config = QUERY_TABLES[key]
    table = config["table"]
    cols = ["id", "created_at", "created_by_agent", "source_path"] + config["display"]
    seen = set()
    select_cols = []
    for col in cols:
        if col not in seen:
            select_cols.append(col)
            seen.add(col)
    params = []
    where = ""
    if term:
        clauses = [f"LOWER(COALESCE({col}, '')) LIKE LOWER(?)" for col in config["text"]]
        where = "WHERE " + " OR ".join(clauses)
        params = [f"%{term}%"] * len(config["text"])
    sql = f"SELECT {', '.join(select_cols)} FROM {table} {where} ORDER BY id DESC LIMIT ?"
    rows = conn.execute(sql, params + [limit]).fetchall()
    return rows


def row_to_dict(row):
    return {key: row[key] for key in row.keys()}


def row_label(row, display_cols):
    parts = [compact(row[col], 72) for col in display_cols if col in row.keys() and row[col]]
    return " | ".join(parts) if parts else "(no title)"


def cmd_query(args):
    conn = connect_db(args.db)
    ensure_schema(conn)
    keys = list(QUERY_TABLES) if args.table == "all" else [args.table]
    output = []
    for key in keys:
        for row in query_table(conn, key, args.term or "", args.limit):
            item = row_to_dict(row)
            item["_kind"] = QUERY_TABLES[key]["label"]
            item["_table"] = QUERY_TABLES[key]["table"]
            output.append(item)
    conn.close()
    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=True))
        return
    if not output:
        print("No Open Brain rows matched.")
        return
    for item in output:
        key = next(k for k, cfg in QUERY_TABLES.items() if cfg["table"] == item["_table"])
        label = row_label(item, QUERY_TABLES[key]["display"])
        created = compact(item.get("created_at"), 19)
        agent = compact(item.get("created_by_agent"), 18)
        print(f"{item['_kind']:<14} #{item['id']:<4} {created:<19} {agent:<18} {label}")


def cmd_audit(args):
    conn = connect_db(args.db)
    ensure_schema(conn)
    as_of = datetime.strptime(args.as_of, "%Y-%m-%d").date() if args.as_of else date.today()
    cutoff = (as_of - timedelta(days=args.stale_days)).isoformat()
    as_of_text = as_of.isoformat()
    stale_claims = conn.execute(
        """
        SELECT id, created_at, claim_text, subject, predicate, object, review_after, confidence
        FROM brain_claims
        WHERE COALESCE(status, 'active') NOT IN ('retired', 'resolved', 'superseded')
          AND (
            (review_after IS NOT NULL AND review_after != '' AND date(review_after) <= date(?))
            OR ((review_after IS NULL OR review_after = '') AND date(substr(created_at, 1, 10)) <= date(?))
          )
        ORDER BY COALESCE(NULLIF(review_after, ''), created_at), id
        LIMIT ?
        """,
        (as_of_text, cutoff, args.limit),
    ).fetchall()
    unresolved = conn.execute(
        """
        SELECT id, created_at, summary, resolution_status, severity, confidence
        FROM brain_contradictions
        WHERE COALESCE(resolution_status, 'open') NOT IN ('resolved', 'dismissed')
        ORDER BY id DESC
        LIMIT ?
        """,
        (args.limit,),
    ).fetchall()
    candidate_pairs = conn.execute(
        """
        SELECT a.id AS a_id, b.id AS b_id,
               a.subject AS subject, a.predicate AS predicate,
               a.object AS object_a, b.object AS object_b,
               a.claim_text AS claim_a, b.claim_text AS claim_b
        FROM brain_claims a
        JOIN brain_claims b
          ON a.id < b.id
         AND LOWER(COALESCE(a.subject, '')) = LOWER(COALESCE(b.subject, ''))
         AND LOWER(COALESCE(a.predicate, '')) = LOWER(COALESCE(b.predicate, ''))
         AND LOWER(COALESCE(a.object, '')) != LOWER(COALESCE(b.object, ''))
        WHERE TRIM(COALESCE(a.subject, '')) != ''
          AND TRIM(COALESCE(a.predicate, '')) != ''
          AND COALESCE(a.status, 'active') NOT IN ('retired', 'resolved', 'superseded')
          AND COALESCE(b.status, 'active') NOT IN ('retired', 'resolved', 'superseded')
        ORDER BY a.subject, a.predicate, a.id, b.id
        LIMIT ?
        """,
        (args.limit,),
    ).fetchall()
    conn.close()
    result = {
        "stale_claims": [row_to_dict(row) for row in stale_claims],
        "unresolved_contradictions": [row_to_dict(row) for row in unresolved],
        "contradiction_candidates": [row_to_dict(row) for row in candidate_pairs],
    }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return
    print(f"Audit as of {as_of_text}")
    print(f"Stale claims: {len(stale_claims)}")
    for row in stale_claims:
        print(f"- claim #{row['id']}: {compact(row['claim_text'])}")
    print(f"Unresolved contradictions: {len(unresolved)}")
    for row in unresolved:
        print(f"- contradiction #{row['id']}: {compact(row['summary'])}")
    print(f"Contradiction candidates: {len(candidate_pairs)}")
    for row in candidate_pairs:
        print(
            f"- claims #{row['a_id']} and #{row['b_id']}: "
            f"{compact(row['subject'])} / {compact(row['predicate'])}"
        )


def source_note(row):
    pieces = []
    if "created_by_agent" in row.keys() and row["created_by_agent"]:
        pieces.append(f"agent: {row['created_by_agent']}")
    if "source_path" in row.keys() and row["source_path"]:
        pieces.append(f"source: {row['source_path']}")
    if "created_at" in row.keys() and row["created_at"]:
        pieces.append(f"created: {row['created_at']}")
    return "; ".join(pieces)


def compile_markdown(title, query, rows_by_key, source_rows):
    lines = [
        f"# {title}",
        "",
        "This Markdown view is compiled from structured Open Brain rows in `_claudia/claudia.db`.",
        "Treat the database rows as authoritative if this view goes stale.",
        "",
    ]
    if query:
        lines.extend([f"Query: `{query}`", ""])
    headings = {
        "claims": "Claims",
        "memories": "Memories",
        "events": "Events",
        "links": "Concept Links",
        "contradictions": "Contradictions",
        "handoffs": "Agent Handoffs",
    }
    for key in COMPILE_TABLE_KEYS:
        rows = rows_by_key.get(key, [])
        lines.extend([f"## {headings[key]}", ""])
        if not rows:
            lines.extend(["No matching rows.", ""])
            continue
        for row in rows:
            item = row_to_dict(row)
            label = row_label(item, QUERY_TABLES[key]["display"])
            note = source_note(row)
            suffix = f" ({note})" if note else ""
            lines.append(f"- #{row['id']} {label}{suffix}")
            source_rows.append({"table": QUERY_TABLES[key]["table"], "id": row["id"]})
        lines.append("")
    lines.extend(
        [
            "---",
            "Generated for: Edgar Agunias",
            f"Date: {today_text()}",
            "Model: deterministic `_claudia/brain.py` compiler",
            "Sources: Structured Open Brain rows in `_claudia/claudia.db`",
            "Agent: Hephaestus",
            "---",
            "",
        ]
    )
    return "\n".join(lines)


def cmd_compile(args):
    conn = connect_db(args.db)
    ensure_schema(conn)
    rows_by_key = {}
    source_rows = []
    for key in COMPILE_TABLE_KEYS:
        rows_by_key[key] = query_table(conn, key, args.query or "", args.limit)
    title = args.title or ("Open Brain View" if not args.query else f"Open Brain View: {args.query}")
    markdown = compile_markdown(title, args.query or "", rows_by_key, source_rows)
    output_path = ""
    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = Path.cwd() / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown, encoding="utf-8")
        output_path = str(out_path)
    values = provenance_fields(args, {"agent": args.agent or "Hephaestus"})
    values.update(
        {
            "view_type": "markdown",
            "title": title,
            "query": args.query or "",
            "body": markdown,
            "output_path": output_path,
            "source_rows_json": json_text(source_rows, "[]"),
            "status": "compiled",
        }
    )
    row_id = insert_row(conn, "brain_compiled_views", values)
    auto_vectorize(conn, [("views", row_id)], args)
    conn.commit()
    conn.close()
    if output_path:
        print(f"Compiled Open Brain view id={row_id} to {output_path}")
    else:
        print(markdown)
        print(f"Compiled Open Brain view id={row_id}", file=sys.stderr)


def cmd_vector_status(args):
    conn = connect_db(args.db)
    ensure_schema(conn)
    vec_ready, vec_message = ensure_sqlite_vec_schema(conn) if args.check_sqlite_vec else (sqlite_vec_ready(conn), "")
    counts = {
        "brain_vector_items": conn.execute("SELECT COUNT(*) FROM brain_vector_items").fetchone()[0],
        "brain_vector_embeddings": conn.execute("SELECT COUNT(*) FROM brain_vector_embeddings").fetchone()[0],
    }
    source_counts = conn.execute(
        """
        SELECT source_table, COUNT(*) AS n
        FROM brain_vector_items
        GROUP BY source_table
        ORDER BY source_table
        """
    ).fetchall()
    vec_rows = None
    if vec_ready:
        try:
            vec_rows = conn.execute(f"SELECT COUNT(*) FROM {VEC_TABLE}").fetchone()[0]
        except sqlite3.Error:
            vec_rows = None
    conn.close()
    payload = {
        "model": EMBED_MODEL,
        "dimensions": EMBED_DIM,
        "sqlite_vec_ready": vec_ready,
        "sqlite_vec_message": vec_message,
        "sqlite_vec_rows": vec_rows,
        "counts": counts,
        "sources": {row["source_table"]: row["n"] for row in source_counts},
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=True))
        return
    print("=== Claudia Open Brain Vector Status ===")
    print(f"Model:                 {EMBED_MODEL}")
    print(f"Dimensions:            {EMBED_DIM}")
    print(f"Vector items:          {counts['brain_vector_items']}")
    print(f"BLOB embeddings:       {counts['brain_vector_embeddings']}")
    print(f"sqlite-vec ready:      {'yes' if vec_ready else 'no'}")
    if vec_message:
        print(f"sqlite-vec detail:     {vec_message}")
    if vec_rows is not None:
        print(f"sqlite-vec rows:       {vec_rows}")
    if source_counts:
        print("Sources:")
        for row in source_counts:
            print(f"  {row['source_table']}: {row['n']}")


def cmd_vector_index(args):
    conn = connect_db(args.db)
    ensure_schema(conn)
    rows = vector_source_rows(conn, args.table, args.limit)
    if args.dry_run:
        backend, backend_message = choose_vector_backend(conn, args.backend)
        conn.close()
        print(f"Would index {len(rows)} Open Brain rows with backend={backend}.")
        if backend_message:
            print(f"Backend detail: {backend_message}")
        return
    indexed, skipped, backend, backend_message = index_vector_rows(
        conn,
        rows,
        args.backend,
        force=args.force,
    )
    conn.commit()
    conn.close()
    print(f"Indexed {indexed} Open Brain rows. Skipped {skipped}. Backend: {backend}.")
    if backend_message:
        print(f"Backend detail: {backend_message}")


def cmd_migrate_legacy_embeddings(args):
    conn = connect_db(args.db)
    ensure_schema(conn)
    backend, backend_message = choose_vector_backend(conn, args.backend)
    where = ""
    params = []
    if args.course:
        where = "WHERE course_code = ?"
        params.append(args.course)
    sql = f"""
        SELECT id, source_path, source_type, course_code, chunk_index, chunk_text,
               embedding, model, created_at
        FROM embeddings
        {where}
        ORDER BY id
    """
    if args.limit:
        sql += " LIMIT ?"
        params.append(args.limit)
    rows = conn.execute(sql, params).fetchall()
    if args.dry_run:
        existing = conn.execute(
            "SELECT COUNT(*) FROM brain_vector_items WHERE source_table = 'embeddings'"
        ).fetchone()[0]
        conn.close()
        print(f"Would migrate {len(rows)} legacy embedding rows. Existing migrated rows: {existing}. Backend: {backend}.")
        if backend_message:
            print(f"Backend detail: {backend_message}")
        return
    migrated = 0
    skipped = 0
    for row in rows:
        if row["embedding"] is None:
            skipped += 1
            continue
        item_id, existing, digest = upsert_legacy_vector_item(conn, row, backend)
        if (
            existing
            and not args.force
            and existing["content_hash"] == digest
            and existing["embedded_at"]
            and existing["embedding_model"] == (row["model"] or EMBED_MODEL)
            and existing["embedding_dim"] == EMBED_DIM
        ):
            skipped += 1
            continue
        store_vector_blob(
            conn,
            item_id,
            row["embedding"],
            row["model"] or EMBED_MODEL,
            EMBED_DIM,
            backend,
        )
        migrated += 1
        if migrated % 500 == 0:
            conn.commit()
            print(f"Migrated {migrated} legacy embeddings...", flush=True)
    conn.commit()
    conn.close()
    print(f"Migrated {migrated} legacy embedding rows. Skipped {skipped}. Backend: {backend}.")
    if backend_message:
        print(f"Backend detail: {backend_message}")


def cmd_vector_query(args):
    conn = connect_db(args.db)
    ensure_schema(conn)
    backend, backend_message = choose_vector_backend(conn, args.backend)
    check_ollama()
    query_vec = embed_text(args.text)
    if backend == "sqlite-vec":
        results = search_sqlite_vec(conn, query_vec, args.limit)
    else:
        results = cosine_search_blob(conn, query_vec, args.limit)
    conn.close()
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=True))
        return
    if not results:
        print("No vectorized Open Brain rows matched. Run vector-index first.")
        if backend_message:
            print(f"Backend detail: {backend_message}")
        return
    print(f"Open Brain vector results via {backend}")
    for rank, item in enumerate(results, start=1):
        distance = "" if item["distance"] is None else f" distance={item['distance']:.4f}"
        print(
            f"{rank:<3} score={item['score']:.4f}{distance} "
            f"{item['source_table']}#{item['source_id']} {compact(item['content'], 120)}"
        )


def add_common(parser):
    parser.add_argument("--json", default="", help="Read structured JSON input from a path or '-' for stdin.")
    parser.add_argument("--agent", default="", help="Agent or process that created the row.")
    parser.add_argument("--source-type", default="", help="Source category, such as chat, file, email, calendar, or db.")
    parser.add_argument("--source-path", default="", help="Source file path, URL, table, or other durable locator.")
    parser.add_argument("--source-ref", default="", help="Line, row id, message id, or other source locator.")
    parser.add_argument("--provenance-json", default="", help="Extra provenance as JSON.")
    parser.add_argument("--tags", default="", help="Comma-separated tags or a JSON array.")
    parser.add_argument(
        "--no-vectorize",
        action="store_true",
        help="Save the structured row without immediately embedding it.",
    )
    parser.add_argument(
        "--vector-backend",
        choices=["auto", "sqlite-vec", "blob"],
        default="auto",
        help="Vector backend for automatic embedding after capture.",
    )


def build_parser():
    parser = argparse.ArgumentParser(description="Claudia Open Brain substrate")
    parser.add_argument("--db", default=str(DB_PATH), help="SQLite database path.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create Open Brain tables and indexes idempotently.")
    p_init.add_argument(
        "--sqlite-vec",
        action="store_true",
        help="Also try to create the optional sqlite-vec vec0 table.",
    )
    p_init.set_defaults(func=cmd_init)

    p_event = sub.add_parser("ingest-event", help="Append a structured memory event.")
    add_common(p_event)
    p_event.add_argument("--event-type", default="note")
    p_event.add_argument("--title", default="")
    p_event.add_argument("--body", default="")
    p_event.add_argument("--body-file", default="")
    p_event.add_argument("--subject", default="")
    p_event.add_argument("--event-time", default="")
    p_event.add_argument("--importance", default="0")
    p_event.add_argument("--confidence", default="")
    p_event.add_argument("--status", default="active")
    p_event.set_defaults(func=cmd_ingest_event)

    p_memory = sub.add_parser("ingest-memory", help="Append a durable memory note.")
    add_common(p_memory)
    p_memory.add_argument("--memory-type", default="note")
    p_memory.add_argument("--title", default="")
    p_memory.add_argument("--body", default="")
    p_memory.add_argument("--body-file", default="")
    p_memory.add_argument("--importance", default="0")
    p_memory.add_argument("--confidence", default="")
    p_memory.add_argument("--status", default="active")
    p_memory.add_argument("--valid-from", default="")
    p_memory.add_argument("--valid-until", default="")
    p_memory.add_argument("--review-after", default="")
    p_memory.set_defaults(func=cmd_ingest_memory)

    p_claim = sub.add_parser("ingest-claim", help="Append an atomic claim with provenance.")
    add_common(p_claim)
    p_claim.add_argument("--claim-text", default="")
    p_claim.add_argument("--subject", default="")
    p_claim.add_argument("--predicate", default="")
    p_claim.add_argument("--object", default="")
    p_claim.add_argument("--qualifier", default="")
    p_claim.add_argument("--evidence", default="")
    p_claim.add_argument("--importance", default="0")
    p_claim.add_argument("--confidence", default="")
    p_claim.add_argument("--status", default="active")
    p_claim.add_argument("--valid-from", default="")
    p_claim.add_argument("--valid-until", default="")
    p_claim.add_argument("--review-after", default="")
    p_claim.set_defaults(func=cmd_ingest_claim)

    p_link = sub.add_parser("link-concepts", help="Append a relationship between two concepts.")
    add_common(p_link)
    p_link.add_argument("--concept-a", default="")
    p_link.add_argument("--concept-b", default="")
    p_link.add_argument("--relation", default="related_to")
    p_link.add_argument("--rationale", default="")
    p_link.add_argument("--weight", default="1.0")
    p_link.add_argument("--confidence", default="")
    p_link.add_argument("--status", default="active")
    p_link.set_defaults(func=cmd_link_concepts)

    p_contra = sub.add_parser("record-contradiction", help="Append an explicit contradiction record.")
    add_common(p_contra)
    p_contra.add_argument("--claim-id-a", default="")
    p_contra.add_argument("--claim-id-b", default="")
    p_contra.add_argument("--summary", default="")
    p_contra.add_argument("--details", default="")
    p_contra.add_argument("--evidence", default="")
    p_contra.add_argument("--severity", default="")
    p_contra.add_argument("--confidence", default="")
    p_contra.add_argument("--resolution-status", default="open")
    p_contra.set_defaults(func=cmd_record_contradiction)

    p_handoff = sub.add_parser("ingest-handoff", help="Append a structured agent handoff and linked event.")
    add_common(p_handoff)
    p_handoff.add_argument("--handoff-agent", default="")
    p_handoff.add_argument("--status", default="")
    p_handoff.add_argument("--task-title", default="")
    p_handoff.add_argument("--summary", default="")
    p_handoff.add_argument("--files-checked", default="")
    p_handoff.add_argument("--files-changed", default="")
    p_handoff.add_argument("--key-findings", default="")
    p_handoff.add_argument("--blockers", default="")
    p_handoff.add_argument("--memory-updated", default="")
    p_handoff.add_argument("--recommended-next-action", default="")
    p_handoff.add_argument("--importance", default="0")
    p_handoff.add_argument("--confidence", default="")
    p_handoff.set_defaults(func=cmd_ingest_handoff)

    p_pref = sub.add_parser(
        "capture-preference",
        help="Append a durable Edgar preference to memory and Open Brain.",
    )
    add_common(p_pref)
    p_pref.add_argument("--text", default="")
    p_pref.add_argument("--body-file", default="")
    p_pref.add_argument("--title", default="")
    p_pref.add_argument("--preference-type", default="preference")
    p_pref.add_argument("--scope", choices=["global", "agent"], default="global")
    p_pref.add_argument("--target-agent", default="")
    p_pref.add_argument("--target-path", default="")
    p_pref.add_argument("--importance", default="5")
    p_pref.add_argument("--confidence", default="user_confirmed")
    p_pref.set_defaults(func=cmd_capture_preference)

    p_query = sub.add_parser("query", help="Search Open Brain rows with basic LIKE matching.")
    p_query.add_argument("term", nargs="?", default="")
    p_query.add_argument("--table", choices=["all"] + list(QUERY_TABLES), default="all")
    p_query.add_argument("--limit", type=int, default=20)
    p_query.add_argument("--json", action="store_true")
    p_query.set_defaults(func=cmd_query)

    p_audit = sub.add_parser("audit", help="Find stale claims and contradiction candidates.")
    p_audit.add_argument("--as-of", default="")
    p_audit.add_argument("--stale-days", type=int, default=90)
    p_audit.add_argument("--limit", type=int, default=20)
    p_audit.add_argument("--json", action="store_true")
    p_audit.set_defaults(func=cmd_audit)

    p_compile = sub.add_parser("compile", help="Compile a simple Markdown view from structured rows.")
    p_compile.add_argument("--query", default="")
    p_compile.add_argument("--title", default="")
    p_compile.add_argument("--out", default="")
    p_compile.add_argument("--limit", type=int, default=10)
    p_compile.add_argument("--agent", default="Hephaestus")
    p_compile.add_argument("--source-type", default="compiled_view")
    p_compile.add_argument("--source-path", default=str(DB_PATH))
    p_compile.add_argument("--source-ref", default="")
    p_compile.add_argument("--provenance-json", default="")
    p_compile.add_argument("--tags", default="")
    p_compile.add_argument("--no-vectorize", action="store_true")
    p_compile.add_argument("--vector-backend", choices=["auto", "sqlite-vec", "blob"], default="auto")
    p_compile.set_defaults(func=cmd_compile)

    p_vstatus = sub.add_parser("vector-status", help="Show local Open Brain vector index status.")
    p_vstatus.add_argument("--check-sqlite-vec", action="store_true")
    p_vstatus.add_argument("--json", action="store_true")
    p_vstatus.set_defaults(func=cmd_vector_status)

    p_vindex = sub.add_parser("vector-index", help="Embed Open Brain rows into the local vector index.")
    p_vindex.add_argument("--table", choices=["all"] + list(QUERY_TABLES), default="all")
    p_vindex.add_argument("--backend", choices=["auto", "sqlite-vec", "blob"], default="auto")
    p_vindex.add_argument("--limit", type=int, default=0)
    p_vindex.add_argument("--force", action="store_true")
    p_vindex.add_argument("--dry-run", action="store_true")
    p_vindex.set_defaults(func=cmd_vector_index)

    p_migrate = sub.add_parser(
        "migrate-legacy-embeddings",
        help="Port rows from the old embeddings table into the Open Brain vector index.",
    )
    p_migrate.add_argument("--backend", choices=["auto", "sqlite-vec", "blob"], default="auto")
    p_migrate.add_argument("--course", default="")
    p_migrate.add_argument("--limit", type=int, default=0)
    p_migrate.add_argument("--force", action="store_true")
    p_migrate.add_argument("--dry-run", action="store_true")
    p_migrate.set_defaults(func=cmd_migrate_legacy_embeddings)

    p_vquery = sub.add_parser("vector-query", help="Semantic search over vectorized Open Brain rows.")
    p_vquery.add_argument("text")
    p_vquery.add_argument("--backend", choices=["auto", "sqlite-vec", "blob"], default="auto")
    p_vquery.add_argument("--limit", type=int, default=10)
    p_vquery.add_argument("--json", action="store_true")
    p_vquery.set_defaults(func=cmd_vector_query)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
