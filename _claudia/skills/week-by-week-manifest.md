#Resource #AI/ChatGPT5 
# Week-by-Week Course Manifest — Spec & Templates (Canvas→Zip Pipeline)

A single source of truth that lets humans and scripts know **what exists, where it lives, how to access it, and current status** — organized by week.

---
## 1) What this manifest enables
- **Zip builder:** Produce `/dist/weekXX.zip` with consistent structure.
- **Summary pipeline:** Auto-run memo-style summaries for all readings with `summary.status: pending` and write to `output_path`.
- **Access checker:** Re-try SSO/EZProxy/paywalled links where `access.status != downloaded`.
- **Calendar export:** Emit `.ics` from `assignments[].due`.
- **QA & reproducibility:** Verify file hashes, page counts, and link availability on re-runs.

---
## 2) Directory & naming conventions
```
/manifest/course.yaml            # the master manifest (YAML)
/readings/weekXX/*.pdf
/assignments/weekXX/*
/practice/weekXX/*
/summaries/*.md                  # memo-style reading overviews
/logs/*.json
/dist/weekXX.zip
```
**IDs**
- Pattern: `W{week}-{Type}{seq}` where Type ∈ {R (reading), A (assignment), P (practice)}.
  - Examples: `W3-R1`, `W5-A2`, `W2-P1`.

**Filenames**
- Kebab-case; prefix with `weekXX-` when helpful. Example: `week03-alliances-credibility.pdf`.

---
## 3) Enumerations (allowed values)
```yaml
access:
  method: ["direct", "UCSD SSO via EZProxy", "VPN", "instructor-upload"]
  status: ["pending", "sso_required", "downloaded", "failed", "unreachable"]
summary:
  status: ["pending", "done", "failed", "skipped"]
qc:
  status: ["unchecked", "passed", "flagged"]
```

---
## 4) Course-level manifest (YAML skeleton)
```yaml
course:
  institution: "UC San Diego (UCSD)"
  canvas_domain: "https://canvas.ucsd.edu"
  course_name: "<Course Name>"
  course_code: "<CODE>"
  term: "<Term Year>"
  course_url: "<Canvas course URL>"
  timezone: "America/Los_Angeles"
  library_mode: "UCSD SSO via EZProxy" # or "direct"/"VPN"
  operator: "<name or bot>"
  created_at: "<ISO>"
  updated_at: "<ISO>"
  notes: "<free text>"

weeks:
  - week: 1
    dates: "YYYY-MM-DD..YYYY-MM-DD"
    topic: "<weekly topic>"
    readings: []
    assignments: []
    practice_materials: []
    notes: "<optional>"
```

---
## 5) Week block template
```yaml
- week: <n>
  dates: "YYYY-MM-DD..YYYY-MM-DD"
  topic: "<topic>"
  readings:
    - id: "W<n>-R<m>"
      title: "<title>"
      authors: ["<Author Surname, Given>"]
      year: <YYYY>
      citation: "<complete citation string>"
      source_type: "journal|book chapter|report|handout|web"
      source_url: "<url or NA>"
      access:
        method: "UCSD SSO via EZProxy|direct|VPN|instructor-upload"
        status: "pending|sso_required|downloaded|failed|unreachable"
        last_checked: "<ISO>"
        credentials_scope: "ucsd.edu" # if relevant
      file:
        path: "readings/weekXX/<file>.pdf"
        pages: <int or null>
        sha256: "<hash or null>"
        size_bytes: <int or null>
      summary:
        status: "pending|done|failed|skipped"
        output_path: "summaries/W<n>-R<m>.md"
        last_run: "<ISO or null>"
      qc:
        status: "unchecked|passed|flagged"
        notes: "<issues discovered>"

  assignments:
    - id: "W<n>-A<m>"
      name: "<assignment title>"
      due: "YYYY-MM-DDTHH:MM"
      points: <int or null>
      rubric_url: "<url or NA>"
      file: { path: "assignments/weekXX/<file>", sha256: "<hash or null>" }

  practice_materials:
    - id: "W<n>-P<m>"
      type: "past midterm|quiz bank|sample quiz|review sheet|solutions"
      file: { path: "practice/weekXX/<file>", sha256: "<hash or null>" }

  notes: "<free text>"
```

---
## 6) Operator checklist (Canvas→Manifest)
**Goal:** Populate `course.yaml`, download materials, and set statuses so automations can run.

1) **Gather course meta**: domain, course URL, term, timezone.
2) **Enumerate weeks** from syllabus schedule; create empty week blocks.
3) **Collect readings**
   - Check **Modules**, **Files**, and **Syllabus** (including inline links).
   - For links behind paywalls, attempt **UCSD SSO via EZProxy**; if not accessible, set `access.status: sso_required` or `failed` with reason in `notes`.
   - Save PDFs to `readings/weekXX/` and capture `pages`, `sha256`, `size_bytes`.
4) **Assignments & due dates**: add to `assignments[]` with ISO datetime; attach rubric URL or file if provided.
5) **Practice materials**: past exams, question banks, sample quizzes, review sheets.
6) **QC**: Spot-check 10% of files: openability, correct pages, clean text layer.
7) **Update timestamps**: `updated_at` at top-level.

---
## 7) Prompt — Canvas Course Extractor → Manifest (copy/paste)
```
ROLE
You are a READ-ONLY Canvas Course Extractor for UCSD. Do not modify or post anything. Your job: traverse Syllabus, Modules, and Files to compile a week-by-week manifest and download artifacts.

INPUTS
- canvas_domain: https://canvas.ucsd.edu
- course_url: <paste>
- institution: UC San Diego (UCSD)
- term: <term>
- timezone: America/Los_Angeles
- library_mode: UCSD SSO via EZProxy

REQUIREMENTS
- Capture readings that appear only as links on the Syllabus (including paywalled academic journals via UCSD SSO).
- For each item, fill all fields defined in the Week block template. If a field is unknown, write `null` or `NA` (not blank).
- Download files to the standard directories and compute `pages`, `sha256`, `size_bytes`.
- Set accurate statuses for `access.status`, `summary.status`, and `qc.status`.

OUTPUTS
- Write a single YAML file at `/manifest/course.yaml` matching the schema in this document.
- Save all files under the directory scheme. Produce a console summary: counts by week and a list of missing/failed items.

FAIL-SAFES
- If SSO is required, attempt once. If blocked, set `access.status: sso_required` and record the exact URL.
- Never invent metadata. Use `NA` or `null` and note the gap.
```

---
## 8) Prompt — Memo Summarizer Integration (reads manifest)
```
ROLE
You are a Policy Memo Summarizer. For each reading in the provided manifest with `summary.status: pending`, produce a concise BLUF-first memo summary and save it to `summary.output_path`.

INPUTS
- manifest_yaml: <contents of /manifest/course.yaml>

INSTRUCTIONS
- For each `weeks[*].readings[*]` where `summary.status == "pending"` and `file.path` exists, load the PDF and generate an output using the memo template (≤300 words, BLUF-first, evidence-cited).
- Use `context_for_use` as: `<course_name> — Week <week>: <topic>`.
- Include page/section cites where possible.
- After writing the summary, set `summary.status: done` and `summary.last_run` to now.

OUTPUT
- Updated `/manifest/course.yaml` and new Markdown summaries at each `output_path`.
```

---
## 9) Validation rules (lightweight)
- **IDs** unique across entire manifest.
- **Paths** must exist for any item with `access.status: downloaded`.
- **pages** is an integer ≥ 1 for PDFs; null allowed only when file unavailable.
- **sha256** is 64 hex chars when present.
- **due** uses ISO `YYYY-MM-DDTHH:MM` (local time).

---
## 10) JSON Schema (abridged) — optional validator
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["course", "weeks"],
  "properties": {
    "course": {
      "type": "object",
      "required": ["institution", "canvas_domain", "course_name", "course_code", "term", "course_url", "timezone"],
      "properties": {
        "institution": {"type": "string"},
        "canvas_domain": {"type": "string"},
        "course_name": {"type": "string"},
        "course_code": {"type": "string"},
        "term": {"type": "string"},
        "course_url": {"type": "string"},
        "timezone": {"type": "string"},
        "updated_at": {"type": "string"}
      }
    },
    "weeks": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["week", "readings", "assignments", "practice_materials"],
        "properties": {
          "week": {"type": "integer", "minimum": 0},
          "dates": {"type": "string"},
          "topic": {"type": "string"},
          "readings": {"type": "array"},
          "assignments": {"type": "array"},
          "practice_materials": {"type": "array"}
        }
      }
    }
  }
}
```

---
## 11) Example — Week 3 (filled)
```yaml
- week: 3
  dates: "2025-10-13..2025-10-19"
  topic: "Nuclear deterrence"
  readings:
    - id: "W3-R1"
      title: "Alliance Commitments and Credibility"
      authors: ["Doe, Jane"]
      year: 2019
      citation: "Doe, J. (2019). Alliance Commitments... Journal of Security Studies, 28(4), 455–480."
      source_type: "journal"
      source_url: "https://doi.org/..."
      access: { method: "UCSD SSO via EZProxy", status: "downloaded", last_checked: "2025-10-12", credentials_scope: "ucsd.edu" }
      file: { path: "readings/week03/alliances-credibility.pdf", pages: 27, sha256: "<hash>", size_bytes: 1532088 }
      summary: { status: "pending", output_path: "summaries/W3-R1.md", last_run: null }
      qc: { status: "unchecked", notes: "" }
  assignments:
    - id: "W3-A1"
      name: "Policy memo 1"
      due: "2025-10-17T23:59"
      points: 15
      rubric_url: "https://canvas.ucsd.edu/courses/xxxx/assignments/yyyy"
      file: { path: "assignments/week03/policy-memo-1.pdf", sha256: null }
  practice_materials:
    - id: "W3-P1"
      type: "past midterm"
      file: { path: "practice/week03/midterm_2023.pdf", sha256: "<hash>" }
  notes: "Prof added an extra reading via syllabus on 10/11."
```

---
## 12) CLI-style automation hooks (pseudocode)
**zip-week**
```
for item in weeks[W].(readings+assignments+practice_materials):
  assert exists(item.file.path) if item.access.status == 'downloaded'
zip files → /dist/week{W}.zip
include /manifest/course.yaml excerpt in zip
```

**summarize-pending**
```
for r in all readings where r.summary.status == 'pending' and exists(r.file.path):
  memo = summarize_pdf(r.file.path, context=course.course_name + ' — Week ' + week.topic)
  write memo → r.summary.output_path
  r.summary.status = 'done'; r.summary.last_run = now()
```

**check-access**
```
for item in all readings:
  if item.access.status in ['pending','sso_required','failed','unreachable']:
    try_access(item.source_url, mode=course.library_mode)
    update status + last_checked
```

---
## 13) Notes & extensions
- Add `est_reading_time_min` if you want weekly workload estimates.
- Add `tags: ["deterrence", "alliances"]` for cross-week queries.
- Add `ocr: { needed: bool, done: bool }` for scanned PDFs.

