# GPCO 410 Syllabus Extraction

## Sources Inspected

- `GPCO 410 - Intl Pol:Sec - Praether/Course Admin/International_Politics_and_Security_Syllabus.pdf` - canonical syllabus.
- `GPCO 410 - Intl Pol:Sec - Praether/_agent/SYLLABUS_NOTES.md` - pre-existing syllabus scaffold.
- `GPCO 410 - Intl Pol:Sec - Praether/_agent/FEEDBACK.md` - course-specific writing and grading rules.
- `_claudia/claudia.db` - existing assignment and reading rows, including Canvas-updated data memo deadline.

## Course Basics

- Course: GPCO 410, International Politics and Security
- Instructor: Lauren Prather
- Term: Spring 2026
- Meeting pattern: Monday/Wednesday, 11:00 AM-12:20 PM
- Location: GPS Auditorium
- Instructor office hours: Tuesday 10:00 AM-12:00 PM by signup, plus appointment
- TA: Ali Abdirisak, Monday 9:30-10:30 AM, RBC 3130

## Assignments And Deadlines

| Title | Due Date | Due Time | Timezone | Weight | Submission | Source | Confidence | Notes |
|---|---|---:|---|---:|---|---|---|---|
| Analytic Memo - BLUE | 2026-04-08 | 11:00 | America/Los_Angeles | 10% | Canvas | syllabus | verified | Choose one W2 option; late after start of class not graded. |
| Analytic Memo - ORANGE | 2026-04-29 | 11:00 | America/Los_Angeles | 10% | Canvas | syllabus | verified | Choose one W3-W5 option. Latest active option is Myanmar democratization on Apr 29. |
| Midterm Exam | 2026-05-04 | 11:00 | America/Los_Angeles | 30% | In class | syllabus | verified | Applies course concepts to analyze world events. |
| Data Memo - Interstate Conflict (COW) | 2026-05-15 | 17:00 | America/Los_Angeles | 10% | Canvas | Canvas/email update | verified | Updated deadline in DB/memory to May 15 at 5 PM. Original syllabus says start of class. |
| Data Memo - Civil War (PRIO) | 2026-05-15 | 17:00 | America/Los_Angeles | 10% | Canvas | Canvas/email update | verified | Choose one data memo total. |
| Data Memo - Regime Type (Polity IV) | 2026-05-15 | 17:00 | America/Los_Angeles | 10% | Canvas | Canvas/email update | verified | Choose one data memo total. |
| Analytic Memo - PURPLE | 2026-05-20 | 11:00 | America/Los_Angeles | 10% | Canvas | syllabus | verified | Choose one W6-W8 option. |
| Final Exam | 2026-06-03 | 11:00 | America/Los_Angeles | 30% | In class | syllabus | verified | In-class final exam; randomly selects one of Edgar's three analytic memos and asks expansion questions. |

## Recurring Obligations

| Obligation | Rule | Due Time | Weight | Source | Notes |
|---|---|---:|---:|---|---|
| Readings and participation | Do assigned reading, attend class, participate. |  |  | syllabus | No separate percentage listed beyond memo/exam structure. |

## Exams And In-Class Assessments

| Title | Date | Time | Location | Weight | Source | Notes |
|---|---|---:|---|---:|---|---|
| Midterm Exam | 2026-05-04 | 11:00-12:20 | GPS Auditorium | 30% | syllabus | Apply concepts to analyze world events. |
| Final Exam | 2026-06-03 | 11:00-12:20 | GPS Auditorium | 30% | syllabus | Uses one of the three analytic memos. |

## Readings By Week

| Week | Date/Session | Reading | File Path | Pages | Required? | Notes |
|---:|---|---|---|---:|---|---|
| 1 | Apr 1 | Lake & Powell; McMillan; Muthoo; optional Dixit & Nalebuff | `W1 - Game Theory/` |  | Yes | Strategic choice and bargaining. |
| 2 | Apr 6 / Apr 8 | Frieden; Schelling; Milner; Lebow; MIT signaling notes; McMillan; Russell | `W2 - Preferance Theory/` |  | Yes | Actors, preferences, strategies, information/signaling. |
| 3 | Apr 13 / Apr 15 | Fearon; Morrow; Yetiv; Powell; Saddam's Delusions | `W3 - Info & Commitment Problems/` |  | Yes | Information and commitment problems. |
| 4 | Apr 20 / Apr 22 | Bueno de Mesquita et al.; Walter; Blattman & Miguel | DB/file rows |  | Yes | Democratic peace and civil war. |
| 5 | Apr 27 / Apr 29 | Walter, Committing to Peace Ch. 2; Cederman, Hug & Krebs | `W5 - Negotiated Settlements & Democratization/` |  | Yes | Civil war settlements and democratization violence. |
| 6 | May 6 | Beardsley & Asal | DB/file rows |  | Yes | Nuclear proliferation. |
| 7 | May 11 / May 13 | Carpenter & Bandow; Pape; Ashworth et al.; Pape reply | DB/file rows |  | Yes | Nuclear credibility and terrorism. |
| 8 | May 18 / May 20 | Kydd & Walter; Stein; Gourevitch | DB/file rows |  | Yes | Terrorism strategy and collective security. |
| 9 | May 27 | Lake, Building Legitimate States Ch. 1 | DB/file rows |  | Yes | Statebuilding. |
| 10 | Jun 1 | Rogowski; Fearon; Herrmann/Tetlock/Visser | DB/file rows |  | Yes | Public opinion and international security. |

## Policies

- AI/tool policy: AI may be used for concept help, feedback, brainstorming/outlining, and grammar/spelling. AI-generated text, verbatim or edited, may not be submitted in papers or written assignments.
- Disclosure: Any assignment using AI tools must describe exactly how they were used.
- Late work: Memos submitted after 11:00 AM on due day are not graded, unless Canvas/email override applies.
- Submission format: Canvas; memos max 3 double-spaced pages, 12 pt font, one-inch margins. Only first 950 words graded if format exceeds limits.
- Citation format: Footnotes only for memos/data memos.
- Grading notes: Four memos/data memo total at 10% each; midterm 30%; final 30%; curved median B+.

## DB Normalization Notes

- Update ORANGE and PURPLE due_time to `11:00`, date_kind `window_end`, source `syllabus`.
- Keep Data Memo rows at `2026-05-15 17:00` with source `canvas/email update` rather than syllabus because DB/memory already records Prather date change.
- Update Midterm and Final due_time to `11:00`, date_kind `in_class`, source `syllabus`.
- Preserve no-AI-generated-text rule in notes for all memo rows.
