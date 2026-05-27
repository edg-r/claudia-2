#!/usr/bin/env python3
"""
Local Open Brain vector dashboard server.

Usage:
    python3 _claudia/vector_dashboard_server.py
"""

import json
import math
import subprocess
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

try:
    import pysqlite3 as sqlite3
except ImportError:
    import sqlite3

import brain

HOST = "127.0.0.1"
PORT = 8776
SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / "claudia.db"
DASHBOARD_PATH = SCRIPT_DIR / "vector_dashboard.html"


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def scalar(conn, sql, params=()):
    return conn.execute(sql, params).fetchone()[0]


def rows(conn, sql, params=()):
    return [dict(row) for row in conn.execute(sql, params).fetchall()]


def load_vec(conn):
    ok, message = brain.ensure_sqlite_vec_schema(conn)
    return ok, message


def vector_stats():
    conn = connect()
    ok, vec_message = load_vec(conn)
    legacy_chunks = scalar(conn, "SELECT COUNT(*) FROM embeddings")
    legacy_sources = scalar(conn, "SELECT COUNT(DISTINCT source_path) FROM embeddings")
    migrated_legacy = scalar(
        conn,
        "SELECT COUNT(*) FROM brain_vector_items WHERE source_table = 'embeddings'",
    )
    vector_items = scalar(conn, "SELECT COUNT(*) FROM brain_vector_items")
    blob_embeddings = scalar(conn, "SELECT COUNT(*) FROM brain_vector_embeddings")
    vec_rows = scalar(conn, f"SELECT COUNT(*) FROM {brain.VEC_TABLE}") if ok else 0
    integrity = scalar(conn, "PRAGMA integrity_check")
    by_source = rows(
        conn,
        """
        SELECT source_table, COUNT(*) AS count
        FROM brain_vector_items
        GROUP BY source_table
        ORDER BY count DESC, source_table
        """,
    )
    by_course = rows(
        conn,
        """
        SELECT COALESCE(NULLIF(json_extract(metadata_json, '$.course_code'), ''), 'N/A') AS course,
               COUNT(*) AS count
        FROM brain_vector_items
        WHERE source_table = 'embeddings'
        GROUP BY course
        ORDER BY count DESC, course
        """,
    )
    by_type = rows(
        conn,
        """
        SELECT COALESCE(NULLIF(json_extract(metadata_json, '$.source_type'), ''), 'unknown') AS type,
               COUNT(*) AS count
        FROM brain_vector_items
        WHERE source_table = 'embeddings'
        GROUP BY type
        ORDER BY count DESC, type
        """,
    )
    recent = rows(
        conn,
        """
        SELECT id, source_table, source_id, embedded_at, embedding_model, vector_backend,
               substr(content, 1, 180) AS preview, metadata_json
        FROM brain_vector_items
        ORDER BY id DESC
        LIMIT 12
        """,
    )
    topology_nodes = rows(
        conn,
        """
        SELECT id, metadata_json, substr(content, 1, 120) AS preview
        FROM brain_vector_items
        ORDER BY id DESC
        LIMIT 3000
        """,
    )
    conn.close()
    coverage = 0 if legacy_chunks == 0 else round((migrated_legacy / legacy_chunks) * 100, 2)
    return {
        "database": str(DB_PATH),
        "sqlite_vec_ready": ok,
        "sqlite_vec_message": vec_message,
        "integrity": integrity,
        "model": brain.EMBED_MODEL,
        "dimensions": brain.EMBED_DIM,
        "legacy_chunks": legacy_chunks,
        "legacy_sources": legacy_sources,
        "migrated_legacy": migrated_legacy,
        "legacy_coverage": coverage,
        "vector_items": vector_items,
        "blob_embeddings": blob_embeddings,
        "vec_rows": vec_rows,
        "by_source": by_source,
        "by_course": by_course,
        "by_type": by_type,
        "recent": recent,
        "topology_nodes": topology_nodes,
    }


def keyword_search(term, limit):
    conn = connect()
    pattern = f"%{term}%"
    result = rows(
        conn,
        """
        SELECT id, source_table, source_id, embedded_at, vector_backend,
               substr(content, 1, 360) AS preview, metadata_json
        FROM brain_vector_items
        WHERE content LIKE ?
           OR metadata_json LIKE ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (pattern, pattern, limit),
    )
    conn.close()
    return result


def vector_search(term, limit):
    conn = brain.connect_db(DB_PATH)
    brain.ensure_schema(conn)
    backend, detail = brain.choose_vector_backend(conn, "sqlite-vec")
    brain.check_ollama()
    query_vec = brain.embed_text(term)
    result = brain.search_sqlite_vec(conn, query_vec, limit)
    conn.close()
    return {"backend": backend, "detail": detail, "results": result}


def vector_preview(item_id, bins=96):
    conn = connect()
    row = conn.execute(
        """
        SELECT i.id, i.source_table, i.source_id, i.content, i.metadata_json,
               i.vector_backend, e.embedding, e.embedding_model, e.embedding_dim
        FROM brain_vector_items i
        JOIN brain_vector_embeddings e ON e.item_id = i.id
        WHERE i.id = ?
        """,
        (item_id,),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    vec = list(brain.deserialize_embedding(row["embedding"]))
    bin_count = max(12, min(int(bins), len(vec)))
    stride = max(1, math.ceil(len(vec) / bin_count))
    compact = []
    for start in range(0, len(vec), stride):
        window = vec[start : start + stride]
        compact.append(sum(window) / len(window))
    if len(compact) > bin_count:
        compact = compact[:bin_count]
    norm = math.sqrt(sum(value * value for value in vec))
    return {
        "id": row["id"],
        "source_table": row["source_table"],
        "source_id": row["source_id"],
        "vector_backend": row["vector_backend"],
        "embedding_model": row["embedding_model"],
        "embedding_dim": row["embedding_dim"],
        "norm": norm,
        "min": min(vec),
        "max": max(vec),
        "mean": sum(vec) / len(vec),
        "preview": row["content"][:900],
        "metadata": json.loads(row["metadata_json"] or "{}"),
        "bins": compact,
        "first_dims": vec[:24],
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "ClaudiaVectorDashboard/1.0"

    def log_message(self, fmt, *args):
        return

    def send_json(self, payload, status=HTTPStatus.OK):
        body = json.dumps(payload, indent=2, ensure_ascii=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_html(self):
        body = DASHBOARD_PATH.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        try:
            if path in ("/", "/vector-dashboard.html"):
                self.serve_html()
            elif path == "/api/stats":
                self.send_json(vector_stats())
            elif path == "/api/search":
                term = query.get("q", [""])[0].strip()
                mode = query.get("mode", ["keyword"])[0]
                limit = max(1, min(int(query.get("limit", ["12"])[0]), 50))
                if not term:
                    self.send_json({"results": []})
                elif mode == "vector":
                    self.send_json(vector_search(term, limit))
                else:
                    self.send_json({"results": keyword_search(term, limit)})
            elif path == "/api/vector":
                item_id = int(query.get("id", ["0"])[0])
                payload = vector_preview(item_id)
                if payload is None:
                    self.send_json({"ok": False, "error": "Vector item not found"}, HTTPStatus.NOT_FOUND)
                else:
                    self.send_json(payload)
            elif path == "/api/health":
                self.send_json({"ok": True, "host": HOST, "port": PORT})
            else:
                self.send_error(HTTPStatus.NOT_FOUND, "Not found")
        except SystemExit as exc:
            self.send_json({"ok": False, "error": str(exc), "results": []}, HTTPStatus.SERVICE_UNAVAILABLE)
        except Exception as exc:
            self.send_json({"ok": False, "error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/migrate":
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        try:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_DIR / "brain.py"),
                    "migrate-legacy-embeddings",
                    "--backend",
                    "sqlite-vec",
                ],
                cwd=str(SCRIPT_DIR.parent),
                text=True,
                capture_output=True,
                check=False,
            )
            self.send_json(
                {
                    "ok": proc.returncode == 0,
                    "returncode": proc.returncode,
                    "stdout": proc.stdout,
                    "stderr": proc.stderr,
                    "stats": vector_stats(),
                },
                HTTPStatus.OK if proc.returncode == 0 else HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        except Exception as exc:
            self.send_json({"ok": False, "error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)


def main():
    if not DASHBOARD_PATH.exists():
        raise SystemExit(f"Missing dashboard HTML: {DASHBOARD_PATH}")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Claudia vector dashboard running at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
