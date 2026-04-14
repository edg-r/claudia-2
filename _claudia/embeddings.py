#!/usr/bin/env python3
"""
Claudia Embedding Pipeline
Local semantic search using Ollama (nomic-embed-text) + SQLite.

Usage:
    python3 embeddings.py index [--course CODE] [--force]
    python3 embeddings.py query "search terms" [--course CODE] [--top-k 10]
    python3 embeddings.py status
"""

import argparse
import json
import os
import re
import sqlite3
import struct
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

import numpy as np
from datetime import datetime

# --- Configuration ---
SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / "claudia.db"
WORKSPACE_ROOT = SCRIPT_DIR.parent
OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL = "nomic-embed-text"
EMBED_DIM = 768
CHUNK_SIZE = 2000  # characters
CHUNK_OVERLAP = 500


# --- Ollama helpers ---

def check_ollama():
    """Check if Ollama is running. Exit with message if not."""
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags")
        with urllib.request.urlopen(req, timeout=5):
            pass
    except (urllib.error.URLError, ConnectionRefusedError, OSError):
        print("Error: Ollama is not running. Start it with: ollama serve")
        sys.exit(1)


def embed_text(text):
    """Embed a single text string via Ollama. Returns list of floats."""
    payload = json.dumps({"model": MODEL, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["embedding"]


# --- Serialization ---

def serialize_embedding(vec):
    """Pack a list of floats into a BLOB."""
    return struct.pack(f"<{EMBED_DIM}f", *vec)


def deserialize_embedding(blob):
    """Unpack a BLOB into a numpy array."""
    return np.array(struct.unpack(f"<{EMBED_DIM}f", blob), dtype=np.float32)


# --- Text extraction ---

def extract_text_pdf(path):
    """Extract text from a PDF using pypdf."""
    try:
        from pypdf import PdfReader
    except ImportError:
        print(f"  Warning: pypdf not installed, skipping {path}")
        return ""
    try:
        reader = PdfReader(str(path))
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"[Page {i+1}]\n{text}")
        return "\n\n".join(pages)
    except Exception as e:
        print(f"  Warning: Failed to read PDF {path}: {e}")
        return ""


def extract_text_markdown(path):
    """Read a markdown file, strip YAML frontmatter and Obsidian wikilinks."""
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  Warning: Failed to read {path}: {e}")
        return ""

    # Strip YAML frontmatter
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            text = text[end + 3:].strip()

    # Strip Obsidian wikilinks: [[Page|Display]] -> Display, [[Page]] -> Page
    text = re.sub(r'\[\[([^|\]]+)\|([^\]]+)\]\]', r'\2', text)
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)

    return text


def extract_text(path):
    """Dispatch text extraction by file extension."""
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".pdf":
        return extract_text_pdf(path)
    elif ext in (".md", ".markdown", ".txt"):
        return extract_text_markdown(path)
    else:
        return ""


# --- Chunking ---

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks, respecting paragraph boundaries."""
    text = text.strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        if end >= len(text):
            chunks.append(text[start:].strip())
            break

        # Try to break at a paragraph boundary
        candidate = text[start:end]
        para_break = candidate.rfind("\n\n")
        if para_break > chunk_size * 0.3:
            end = start + para_break + 2
        else:
            # Try sentence boundary
            sent_break = candidate.rfind(". ")
            if sent_break > chunk_size * 0.3:
                end = start + sent_break + 2
            # Otherwise hard-split at chunk_size

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - overlap
        if start < 0:
            start = 0

    return chunks


# --- Indexing ---

def needs_reindex(source_path, conn):
    """Check if a file needs (re)embedding."""
    row = conn.execute(
        "SELECT MAX(created_at) FROM embeddings WHERE source_path = ?",
        (source_path,),
    ).fetchone()
    if row[0] is None:
        return True
    try:
        file_mtime = os.path.getmtime(source_path)
        from datetime import datetime
        db_time = datetime.fromisoformat(row[0]).timestamp()
        return file_mtime > db_time
    except (OSError, ValueError):
        return True


def index_file(path, source_type, course_code, conn):
    """Extract, chunk, embed, and store a single file."""
    text = extract_text(path)
    if not text or len(text.strip()) < 20:
        return 0

    chunks = chunk_text(text)
    if not chunks:
        return 0

    # Remove old embeddings for this file
    conn.execute("DELETE FROM embeddings WHERE source_path = ?", (str(path),))

    count = 0
    for i, chunk in enumerate(chunks):
        try:
            vec = embed_text(chunk)
            blob = serialize_embedding(vec)
            conn.execute(
                """INSERT INTO embeddings
                   (source_path, source_type, course_code, chunk_index, chunk_text, embedding, model)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (str(path), source_type, course_code, i, chunk, blob, MODEL),
            )
            count += 1
        except Exception as e:
            print(f"  Warning: Failed to embed chunk {i} of {path}: {e}")

    return count


def get_indexable_files(conn, course_filter=None):
    """Get files to index from the database, joined with course codes."""
    query = """
        SELECT f.path, f.file_type, c.code
        FROM files f
        LEFT JOIN courses c ON f.course_id = c.id
        WHERE f.file_type IN ('pdf', 'md', 'markdown', 'txt')
    """
    params = []
    if course_filter:
        query += " AND c.code = ?"
        params.append(course_filter)
    query += " ORDER BY f.path"
    return conn.execute(query, params).fetchall()


def get_reading_summary_paths(conn):
    """Get readings that have markdown summaries (prefer these over raw PDFs)."""
    rows = conn.execute(
        "SELECT file_path, summary_path FROM readings WHERE summary_path IS NOT NULL AND summary_path != ''"
    ).fetchall()
    return {row[0]: row[1] for row in rows if row[0] and row[1]}


def cmd_index(args):
    """Index files into the embeddings table."""
    check_ollama()
    conn = sqlite3.connect(str(DB_PATH))

    files = get_indexable_files(conn, args.course)
    summary_map = get_reading_summary_paths(conn)

    if not files:
        print("No indexable files found.")
        conn.close()
        return

    total_chunks = 0
    indexed_files = 0
    skipped = 0

    print(f"Found {len(files)} indexable files.")
    if args.course:
        print(f"Filtering to course: {args.course}")

    for i, (path, file_type, course_code) in enumerate(files):
        # Resolve path relative to workspace if needed
        full_path = Path(path)
        if not full_path.is_absolute():
            full_path = WORKSPACE_ROOT / path

        if not full_path.exists():
            continue

        # Prefer summary markdown over raw PDF if available
        if str(path) in summary_map:
            summary_path = Path(summary_map[str(path)])
            if not summary_path.is_absolute():
                summary_path = WORKSPACE_ROOT / summary_path
            if summary_path.exists():
                full_path = summary_path
                file_type = "md"

        # Check if reindex needed
        if not args.force and not needs_reindex(str(full_path), conn):
            skipped += 1
            continue

        print(f"  [{i+1}/{len(files)}] Indexing: {full_path.name}...", end=" ", flush=True)
        chunks = index_file(full_path, file_type or "unknown", course_code or "", conn)
        total_chunks += chunks
        if chunks > 0:
            indexed_files += 1
            print(f"({chunks} chunks)")
        else:
            print("(skipped - no text)")

        # Commit every 10 files
        if indexed_files % 10 == 0:
            conn.commit()

    conn.commit()
    conn.close()

    print(f"\nDone. Indexed {indexed_files} files ({total_chunks} chunks). Skipped {skipped} (already current).")


# --- Querying ---

def cmd_query(args):
    """Semantic search across embeddings."""
    check_ollama()
    conn = sqlite3.connect(str(DB_PATH))

    # Build query
    sql = "SELECT source_path, course_code, chunk_index, chunk_text, embedding FROM embeddings"
    params = []
    if args.course:
        sql += " WHERE course_code = ?"
        params.append(args.course)

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    if not rows:
        print("No embeddings found. Run 'index' first.")
        return

    # Embed the query
    print(f"Searching {len(rows)} chunks...\n")
    query_vec = np.array(embed_text(args.text), dtype=np.float32)

    # Build matrix and compute cosine similarity
    paths = []
    courses = []
    chunk_indices = []
    chunk_texts = []
    matrix = np.zeros((len(rows), EMBED_DIM), dtype=np.float32)

    for i, (path, course, ci, ct, blob) in enumerate(rows):
        paths.append(path)
        courses.append(course or "")
        chunk_indices.append(ci)
        chunk_texts.append(ct)
        matrix[i] = deserialize_embedding(blob)

    # Vectorized cosine similarity
    query_norm = np.linalg.norm(query_vec)
    row_norms = np.linalg.norm(matrix, axis=1)
    # Avoid division by zero
    row_norms = np.maximum(row_norms, 1e-10)
    similarities = (matrix @ query_vec) / (row_norms * query_norm)

    # Get top-k
    top_k = min(args.top_k, len(rows))
    top_indices = np.argsort(similarities)[::-1][:top_k]

    # Display results
    print(f"{'#':<4} {'Score':<8} {'Course':<12} {'Source':<50} {'Text Preview'}")
    print("-" * 120)

    for rank, idx in enumerate(top_indices):
        score = similarities[idx]
        source = Path(paths[idx]).name
        course = courses[idx]
        preview = chunk_texts[idx][:100].replace("\n", " ")
        print(f"{rank+1:<4} {score:<8.4f} {course:<12} {source:<50} {preview}")


# --- Status ---

def cmd_status(args):
    """Report embedding index status."""
    conn = sqlite3.connect(str(DB_PATH))

    total_chunks = conn.execute("SELECT COUNT(*) FROM embeddings").fetchone()[0]
    unique_files = conn.execute("SELECT COUNT(DISTINCT source_path) FROM embeddings").fetchone()[0]
    total_db_files = conn.execute(
        "SELECT COUNT(*) FROM files WHERE file_type IN ('pdf', 'md', 'markdown', 'txt')"
    ).fetchone()[0]

    last_indexed = conn.execute("SELECT MAX(created_at) FROM embeddings").fetchone()[0]

    print("=== Claudia Embedding Index Status ===\n")
    print(f"Total chunks embedded:  {total_chunks}")
    print(f"Unique files indexed:   {unique_files}")
    print(f"Indexable files in DB:  {total_db_files}")
    print(f"Coverage:               {unique_files}/{total_db_files} files")
    print(f"Last indexed:           {last_indexed or 'never'}")

    # Per-course breakdown
    print(f"\n{'Course':<12} {'Chunks':<10} {'Files':<10}")
    print("-" * 32)
    rows = conn.execute(
        """SELECT course_code, COUNT(*) as chunks, COUNT(DISTINCT source_path) as files
           FROM embeddings
           GROUP BY course_code
           ORDER BY course_code"""
    ).fetchall()

    if rows:
        for code, chunks, files in rows:
            print(f"{code or 'N/A':<12} {chunks:<10} {files:<10}")
    else:
        print("(no embeddings yet)")

    conn.close()


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(description="Claudia Embedding Pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    # index
    p_index = sub.add_parser("index", help="Index files into embedding store")
    p_index.add_argument("--course", type=str, help="Filter to a specific course code (e.g. 'GPCO 410')")
    p_index.add_argument("--force", action="store_true", help="Re-embed all files regardless of timestamps")
    p_index.set_defaults(func=cmd_index)

    # query
    p_query = sub.add_parser("query", help="Semantic search across embeddings")
    p_query.add_argument("text", type=str, help="Search query text")
    p_query.add_argument("--course", type=str, help="Filter to a specific course code")
    p_query.add_argument("--top-k", type=int, default=10, help="Number of results (default: 10)")
    p_query.set_defaults(func=cmd_query)

    # status
    p_status = sub.add_parser("status", help="Show embedding index status")
    p_status.set_defaults(func=cmd_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
