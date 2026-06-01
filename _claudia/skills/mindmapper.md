---
name: mindmapper
description: >
  Ingests image-only scanned handwritten mind map PDFs from inbox/, moves and renames
  them, runs native Vision OCR, decodes the spatial conceptual connections, writes
  structured notes directly to the active iCloud Obsidian vault with confidence properties,
  updates the course Map of Content (MOC), registers them in the claudia.db files index,
  and triggers vector embeddings re-indexing.
---

# Mind Map OCR & Ingestion Skill (mindmapper)

Use this skill when Edgar drops handwritten mind map PDFs (e.g., "P&S L - [Topic].pdf") in `/Users/edgar/Documents/01 Projects/Claudia/inbox/` and wants them fully integrated into his database and active Obsidian vault. 

This workflow translates visual, handwritten, and spatial concept maps into highly structured, semantically indexable academic notes.

---

## Step 1: File Sorting & Standardized Naming

Examine the PDF file in `inbox/` and consult the syllabus or the `courses` table in `claudia.db` to identify the correct course (e.g. **GPCO 410 — International Politics & Security**) and week folder.

1.  **Move the original note PDF** to its respective weekly folder in the course directory:
    *   *Path Pattern:* `[Course Folder]/W[X] - [Topic]/W[X] - [Topic] Lecture Notes.pdf`
2.  **Register the PDF** in `claudia.db` `files` table:
    *   `path`: relative path from workspace root.
    *   `filename`: `W[X] - [Topic] Lecture Notes.pdf`
    *   `course_id`: ID from the `courses` table.
    *   `file_type`: `pdf`
    *   `indexed`: `0` (scanned PDFs have no selectable text, so they are marked but not indexed directly).

---

## Step 2: High-Accuracy Neural OCR

Run the native macOS Vision-based OCR script to extract handwritten text along with horizontal and vertical coordinates to preserve spatial connections:

```bash
swift "[Course Folder]/tmp_pdf_ocr.swift" "[Path to moved PDF]" 10
```

---

## Step 3: Concept Reconstruction & Academic Decoding

Analyze the raw coordinate-based OCR output. Handwritten transcriptions will contain distortions, which you must translate into precise academic theories, actors, and mechanisms using the course syllabus and reading contexts.

*   Identify the **Core Central Concept** or question.
*   Extract the **Key Structural Branches** (e.g., Kydd & Walter's 5 strategies of terrorism, David Lake's 4 components of statehood).
*   Map the **Strategic Interactions** (e.g., actor payoffs, state builder self-interest vs. domestic legitimacy).

---

## Step 4: Calculate Ingestion Confidence (`ocr_confidence`)

Evaluate the legibility of the handwritten scan and the accuracy of the reconstruction, and assign a confidence percentage.

| Score | Label | Criteria |
| :--- | :--- | :--- |
| **95–100%** | Excellent | Pristine handwriting, standard terminology, direct coordinates. Reconstructed with virtually zero ambiguity. |
| **85–94%** | Good | Small blur or handwriting slant. Occasional uncertain characters resolved easily by contextual academic alignment. |
| **70–84%** | Fair | Heavy cursive or sketchy lines. Reconstructed by mapping incomplete coordinate terms to assigned readings (e.g. Fearon, Powell). |
| **<70%** | Poor | Highly illegible scribbles or damaged pages. Requires significant contextual guesswork. |

---

## Step 5: Save to Active iCloud Obsidian Vault with Metadata

Create a clean, well-formatted Markdown file directly inside Edgar's **active iCloud Obsidian vault** at:
`~/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObiV3/Notes/`

Name the file `W[X] - [Topic] Mindmap Decoded.md` and include Obsidian frontmatter properties at the top of the file, saving the estimated confidence score:

```yaml
---
tags:
  - GPCO410IntlPolSec/MindmapDecoded
  - GPCO410IntlPolSec/Week[X]
title: "W[X] - [Topic] Mindmap Decoded"
course: "[Full Course Name, e.g., GPCO 410 — International Politics & Security]"
week: [X]
type: "mindmap-decoded"
ocr_used: true
ocr_confidence: [Score, e.g. 85]
---
```

Use **Headings**, **Bullet Lists**, and **Mermaid Diagrams** to present the reconstructed mind map structure and conceptual connections.

---

## Step 6: Map of Content (MOC) Linkage

1.  Locate the course MOC note in Edgar's iCloud vault:
    `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/ObiV3/Notes/[Course Name MOC].md`
2.  Append a section for the new week linking both the standardized **Lecture Notes PDF** and the **Decoded Mindmap Note**:
    ```markdown
    # [[W[X] - [Topic] Lecture Notes.pdf]]
    - Mindmap Reconstructed: [[W[X] - [Topic] Mindmap Decoded]]
    ```

---

## Step 7: Database & Vector Indexing

To make the handwritten concepts semantically searchable across the entire workspace:

1.  **Register the new Markdown file** in `claudia.db` under the `files` table:
    *   `path`: relative path inside the workspace `knowledge/obsidian/Notes/W[X] - [Topic] Mindmap Decoded.md` (Note: maintain a local sync copy in the workspace folder for DB scanning).
    *   `filename`: `W[X] - [Topic] Mindmap Decoded.md`
    *   `file_type`: `markdown`
    *   `course_id`: ID from the `courses` table.
    *   `indexed`: `0`
2.  **Synchronize Workspace Copy:** Copy the new file from the iCloud vault to the workspace `knowledge/obsidian/Notes/` directory so the database indexer can access it.
3.  **Run Vector Indexer:** Trigger the embedding indexing script:
    ```bash
    python3 _claudia/embeddings.py index --course "[Course Code]"
    ```

---

## Step 8: Save Protocol Compliance

Stage and commit only your modified memory files and task logs using Git:
```bash
git add -- [Agent Task Log] [Mnemosyne Task Log]
git commit -m "docs([Course Code]): ingest and index W[X] mindmap notes"
```
Do not stage database files (`claudia.db`) or local Obsidian notes as they are ignored by your `.gitignore`.
