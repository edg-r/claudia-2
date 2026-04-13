---
name: semantic-search
description: >
  Perform semantic search across course materials and Obsidian notes using
  local embeddings (Ollama + nomic-embed-text). Use when keyword search fails,
  when exploring conceptual connections, or for "what do we know about X" queries.
---

## When to Use

Use semantic search when:
- The user asks conceptual questions: "what readings discuss institutional credibility?"
- You need to find connections across courses that share ideas but not keywords
- Keyword/SQL search returns nothing useful
- The user asks "what do we know about X" or "find everything related to Y"

Use SQL/keyword search when:
- The question is structural: "what's due next week?", "how many readings for GPCO 403?"
- You need exact matches: specific file names, assignment titles, dates

## Commands

All commands run from the workspace root.

### Index files
```bash
python3 _claudia/embeddings.py index [--course "GPCO 410"] [--force]
```
- Indexes all text files (PDF, markdown) tracked in the database
- Incremental by default (skips files already embedded)
- `--force` re-embeds everything
- `--course` filters to a single course

### Semantic query
```bash
python3 _claudia/embeddings.py query "bargaining theory and credible commitments" [--course "GPCO 410"] [--top-k 10]
```
- Returns top-k results ranked by cosine similarity
- Shows source file, course, similarity score, and text preview
- `--course` narrows search to one course

### Check status
```bash
python3 _claudia/embeddings.py status
```
- Reports total chunks, files indexed, coverage, per-course breakdown

## Prerequisites

Ollama must be running: `ollama serve`
Model must be pulled: `ollama pull nomic-embed-text`

## Interpreting Results

- Scores above 0.7: strong match
- Scores 0.5-0.7: related content
- Scores below 0.5: weak/tangential
