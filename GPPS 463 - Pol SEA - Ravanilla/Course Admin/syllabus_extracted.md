# GPPS 463 Syllabus Extraction

## Sources Inspected

- `GPPS 463 - Pol SEA - Ravanilla/Course Admin/GPPS 463 Syllabus.pdf` - canonical syllabus: course basics, grading, exams, participation rules, academic integrity, make-up exam policy, grade dispute policy, accommodations.
- `GPPS 463 - Pol SEA - Ravanilla/Course Admin/GPPS 463 - Politics of Southeast Asia - Ravanilla [SP26].pdf` - Canvas course schedule export: lecture-day sequence, required readings, optional readings, no-post days, visible LD2 discussion/attendance Canvas items.
- `_claudia/claudia.db` - current GPPS 463 course, assignment, and readings rows. Read only; no DB writes.
- `GPPS 463 - Pol SEA - Ravanilla/_agent/AGENT_CONTEXT.md`, `ASSIGNMENTS.md`, and `TASK_LOG.md` - Poseidon memory for already-created discussion posts and course arc.

## Course Basics

- Course: GPPS 463, Politics of Southeast Asia
- Instructor: Nico Ravanilla
- Term: Spring 2026
- Meeting pattern: Mondays and Wednesdays, 8:00-9:20 AM
- Location: RBC 3201
- Office: RBC 1325
- Office hours: Monday 11:00 AM-12:00 PM, or by appointment. Note: the extracted syllabus text says "11:00 PM - 12:00 PM," almost certainly an OCR/source typo for 11:00 AM.
- Course frame: graduate-level introduction to Southeast Asian history, political institutions, political actors, and economic development, organized around lecture questions and political-economy tools.

## Assignments And Deadlines

| Title | Due Date | Due Time | Timezone | Weight | Submission | Source | Confidence | Notes |
|---|---|---:|---|---:|---|---|---|---|
| Discussion Post for Lecture Day 2: What explains the rise & fall of the ancient kingdoms of SE Asia? | 2026-04-01 | 00:01 | America/Los_Angeles | participation | Canvas | Canvas schedule / DB | verified | Current DB row `assignments.id=32`, status completed. Canvas schedule lists Apr 1 due by 12:01 AM and 2 pts. |
| Discussion Post for Lecture Day 5: Are colonial institutions bad for long-run development? | 2026-04-13 | 17:00 | America/Los_Angeles | participation | Canvas | course memory / DB | verified | Current DB row `assignments.id=27`, status completed. |
| Discussion Post for Lecture Day 6: How did World War II impact Southeast Asia? | 2026-04-14 | 17:00 | America/Los_Angeles | participation | Canvas/email | course memory / DB | verified | Current DB row `assignments.id=28`, status completed. Canvas/email update moved deadline to Apr 14 at 5 PM. |
| Discussion Post for Lecture Day 8: Why did only some countries experience the Asian Miracle? | 2026-04-21 | 17:00 | America/Los_Angeles | participation | Canvas | course memory / DB | verified | Current DB row `assignments.id=33`, status completed. Required reading: Jansen (2001). |
| Discussion Post for Lecture Day 9: How did Singapore do it? | 2026-04-27 | 00:01 | America/Los_Angeles | participation | Canvas/email | DB | verified | Current DB row `assignments.id=34`, status pending. Canvas notification surfaced by Eos. Required reading: Huff (1995). |
| Discussion Post for Lecture Day 10: Why was the Asian Financial Crisis unequally felt in the region? | 2026-04-28 | 17:00 | America/Los_Angeles | participation | Canvas | DB / syllabus pattern / Edgar confirmation | inferred | Current DB row `assignments.id=35`, status pending. Required reading: Hicken (2008). Verify Canvas exact due time if possible. |
| Midterm Exam 1 | 2026-04-20 | 08:00 | America/Los_Angeles | 25% | In class / LockDown Browser | syllabus / DB | verified | Current DB row `assignments.id=22`, status completed. Covers first portion; one 3x5 index card allowed. |
| Midterm Exam 2 | 2026-05-11 | 08:00 | America/Los_Angeles | 25% | In class / LockDown Browser | syllabus / DB | verified | Current DB row `assignments.id=23`, status pending. Covers second portion; one 3x5 index card allowed. |
| Final Exam | 2026-06-10 | 08:00 | America/Los_Angeles | 25% | In class / LockDown Browser | syllabus / DB | verified | Current DB row `assignments.id=24`, status pending. 8:00-11:00 AM in RBC 3201; previous index cards also allowed. |

## Recurring Obligations

| Obligation | Rule | Due Time | Weight | Source | Notes |
|---|---|---:|---:|---|---|
| Discussion posts | Submit one question about the assigned readings the day before each lecture before 5:00 PM. Posting begins Tuesday, March 31. | 17:00 | 50% of participation grade; 12.5% of course grade | syllabus | Submission must include a clearly stated question, not a statement, plus no more than 3 sentences explaining why the question is important. Current DB has recurring row `assignments.id=25`. Canvas/email may override due time for specific posts, as with LD2 and LD9. |
| In-class attendance quizzes | Short Canvas quizzes during class, based on assigned readings and key concepts. | class time | 50% of participation grade; 12.5% of course grade | syllabus | Perfect quiz earns 1 point; one or more mistakes still earns 0.75 points. Current DB has recurring row `assignments.id=26`. Visible Canvas schedule includes `Attendance (LD2)` on Apr 1 worth 3 pts. |

## Known No-Post Days

| Lecture Day | Date | Reason | Source | DB Treatment |
|---|---|---|---|---|
| LD1 | 2026-03-30 | Course overview; no assigned reading; no discussion post. | Canvas schedule | Do not add discussion-post row. |
| LD7 | 2026-04-20 | In-class Midterm Exam 1. | Canvas schedule / syllabus | Do not add discussion-post row unless Canvas later creates one. |
| LD13 | 2026-05-11 | In-class Midterm Exam 2. | Canvas schedule / syllabus | Do not add discussion-post row unless Canvas later creates one. |
| LD17 | 2026-05-25 | Memorial Day: no class, no readings, no discussion posts. | Canvas schedule | Do not add discussion-post or attendance row. |
| LD20 | 2026-06-03 | Course wrap-up; no assigned reading; no discussion post. | Canvas schedule | Do not add discussion-post row. |

## Future Discussion-Post Rows To Add For Daily-Dispatch Safety

These should become individual `assignments` rows when Mnemosyne normalizes the course data. Use `deadline_source='syllabus/canvas schedule'`, `source_confidence='inferred'`, `date_kind='hard'`, `is_recurring=0`, and preserve the recurring row. Canvas/emails should override any inferred due date/time.

| Title | Due Date | Due Time | Timezone | Confidence | Notes |
|---|---|---:|---|---|---|
| Discussion Post for Lecture Day 11: How is Vietnam doing under communism? | 2026-05-03 | 17:00 | America/Los_Angeles | inferred | Due day before Mon May 4 lecture. Required reading: Malesky, Abrami & Zheng (2011). |
| Discussion Post for Lecture Day 12: Why are Cambodia, Laos, and Myanmar lagging behind their neighbors? | 2026-05-05 | 17:00 | America/Los_Angeles | ambiguous | Lecture exists on Canvas schedule, likely Wed May 6, but extracted schedule shows no required reading under LD12. Verify Canvas before creating or leave as ambiguity. |
| Discussion Post for Lecture Day 14: How was Duterte able to implement the brutal drug war in the Philippines? | 2026-05-12 | 17:00 | America/Los_Angeles | inferred | Due day before Wed May 13 lecture. Required reading: Ravanilla, Sexton & Haim (2022). |
| Discussion Post for Lecture Day 15: Why did UMNO dominate Malaysian politics, and why did it lose power? | 2026-05-17 | 17:00 | America/Los_Angeles | inferred | Due day before Mon May 18 lecture. Required reading: Ostwald (2013). |
| Discussion Post for Lecture Day 16: Why do some countries have high state capacity but not others? | 2026-05-19 | 17:00 | America/Los_Angeles | inferred | Due day before Wed May 20 lecture. Required reading: Slater (2010), Ch. 1. |
| Discussion Post for Lecture Day 18: Is ethnic and racial diversity bad for Southeast Asia? | 2026-05-26 | 17:00 | America/Los_Angeles | inferred | Due day before Wed May 27 lecture. Required reading: Tajima, Samphantharak & Ostwald (2018). |
| Discussion Post for Lecture Day 19: How is the U.S.-China rivalry reshaping Southeast Asia? | 2026-05-31 | 17:00 | America/Los_Angeles | inferred | Due day before Mon Jun 1 lecture. Multiple required readings/reports. |

## Exams And In-Class Assessments

| Title | Date | Time | Location | Weight | Source | Notes |
|---|---|---:|---|---:|---|---|
| Attendance Quiz LD2 | 2026-04-01 | class time | RBC 3201 / Canvas | participation | Canvas schedule | Visible Canvas schedule item, 3 pts. |
| In-class attendance quizzes | recurring class meetings | class time | RBC 3201 / Canvas | 12.5% course | syllabus | Short low-stakes Canvas quizzes. Add individual rows only if Canvas exposes dated quiz items; otherwise recurring row is sufficient but daily dispatch must check it. |
| Midterm Exam 1 | 2026-04-20 | 08:00-09:20 | RBC 3201 | 25% | syllabus | Multiple choice and short essays. LockDown Browser. |
| Midterm Exam 2 | 2026-05-11 | 08:00-09:20 | RBC 3201 | 25% | syllabus | Multiple choice and short essays. LockDown Browser. |
| Final Exam | 2026-06-10 | 08:00-11:00 | RBC 3201 | 25% | syllabus | Multiple choice and short essays. LockDown Browser. |

## Readings By Week

| Week | Date/Session | Reading | File Path | Pages | Required? | Notes |
|---:|---|---|---|---:|---|---|
| 1 | LD1 Mar 30 | No assigned reading |  |  | No | Course overview; no discussion post. |
| 1 | LD2 Apr 1 | Hayton (2014), Ch. 1 | `GPPS 463 - Pol SEA - Ravanilla/W1 - Ancient Kingdoms/hayton2014_chap1.pdf` | 28 | Yes | DB reading row `readings.id=70`; author misspelled as Heyton in DB. Optional: Osborne Chs. 1-2; Wolters (1999) introduction. |
| 2 | LD3 Apr 6 | Dell, Lane & Querubin (2018) | `GPPS 463 - Pol SEA - Ravanilla/W2 - Sinivs Indi, Guns Germs & Steel/dai viet.pdf` | 39 | Yes | DB reading row `readings.id=71` has blank authors and week=1; should likely be week=2. Optional: Osborne Ch. 3. |
| 2 | LD4 Apr 8 | Diamond (1997), Prologue | `GPPS 463 - Pol SEA - Ravanilla/W2 - Sinivs Indi, Guns Germs & Steel/diamond_yalis.pdf` | 21 | Yes | DB reading row `readings.id=72`. Optional: Osborne Chs. 5-7; Elson (2004). |
| 3 | LD5 Apr 13 | Acemoglu & Robinson (2012), Ch. 9 | `GPPS 463 - Pol SEA - Ravanilla/W3 - Colonial Institutions and Development/The Dutch in Indonesia_Acemoglu2012.pdf` | 5 | Yes | DB reading row `readings.id=75`. Optional: Cruz (2014). |
| 3 | LD5 Apr 13 | Dell & Olken (2018) | `GPPS 463 - Pol SEA - Ravanilla/W3 - Colonial Institutions and Development/Dell-Olken - Development Effects of the Extractive Colonial Economy.pdf` | 40 | Yes | DB reading row `readings.id=73`. |
| 3 | LD6 Apr 15 | Stubbs (1999) | `GPPS 463 - Pol SEA - Ravanilla/W3 - Colonial Institutions and Development/stubbs1999.pdf` | 20 | Yes | DB reading row `readings.id=74`. Optional: Dell & Querubin (2017); Osborne Chs. 8-15. |
| 4 | LD7 Apr 20 | No reading listed; in-class Midterm Exam 1 |  |  | No | Exam day. |
| 4 | LD8 Apr 22 | Jansen (2001) | `GPPS 463 - Pol SEA - Ravanilla/W4 - Asian Miracle/Thailand- The Making of a Miracle.pdf` |  | Yes | Not currently in DB readings. Optional: Kim (2010); Doner (1991). |
| 5 | LD9 Apr 27 | Huff (1995) | `GPPS 463 - Pol SEA - Ravanilla/W5 - Singapore & Asian Financial Crisis/huff1995.pdf` |  | Yes | Not currently in DB readings. Optional: Wong (2007); Krugman (1994). |
| 5 | LD10 Apr 29 | Hicken (2008) | `GPPS 463 - Pol SEA - Ravanilla/W5 - Singapore & Asian Financial Crisis/hicken2008.pdf` |  | Yes | Not currently in DB readings. Optional: McIntyre (2001); Wade (2000). |
| 6 | LD11 May 4 | Malesky, Abrami & Zheng (2011) | `GPPS 463 - Pol SEA - Ravanilla/W6 - Vietnam Under Communism/malesky2011.pdf` |  | Yes | Not currently in DB readings. |
| 6 | LD12 likely May 6 | No required reading visible in extracted Canvas schedule |  |  | Ambiguous | Lecture topic: Cambodia, Laos, and Myanmar lagging behind neighbors. Verify Canvas. |
| 7 | LD13 May 11 | No reading listed; in-class Midterm Exam 2 |  |  | No | Exam day. |
| 7 | LD14 May 13 | Ravanilla, Sexton & Haim (2022) | `GPPS 463 - Pol SEA - Ravanilla/W7 - Duterte Drug War/Ravanilla_2022.pdf` |  | Yes | Not currently in DB readings. Optional: De Lima (2019). |
| 8 | LD15 May 18 | Ostwald (2013) | `GPPS 463 - Pol SEA - Ravanilla/W8 - Malaysian Politics & State Capacity/ostwald2013.pdf` |  | Yes | Not currently in DB readings. Optional: Slater (2003); Slater & Wong (2013). |
| 8 | LD16 May 20 | Slater (2010), Ch. 1 | `GPPS 463 - Pol SEA - Ravanilla/W8 - Malaysian Politics & State Capacity/to_extract_and_to_organize.pdf` |  | Yes | File identity should be verified/renamed. Optional: Slater (2010), Ch. 2. |
| 9 | LD17 May 25 | No class, no readings, no discussion posts |  |  | No | Memorial Day. |
| 9 | LD18 May 27 | Tajima, Samphantharak & Ostwald (2018) | `GPPS 463 - Pol SEA - Ravanilla/W9 - Ethnic Diversity in SEA/ethnic_segregation_and_public_goods_evidence_from_indonesia.pdf` |  | Yes | Not currently in DB readings. Optional: Hirschman (1986); Islam (1998). |
| 10 | LD19 Jun 1 | Hayton (2021) | `GPPS 463 - Pol SEA - Ravanilla/W10 - US-China Rivalry/China Still Stifling Efforts at South China Sea Code of Conduct After 25 Years.pdf` |  | Yes | Not currently in DB readings. |
| 10 | LD19 Jun 1 | RAND Research Report (2020), Chs. 1-4 | `GPPS 463 - Pol SEA - Ravanilla/W10 - US-China Rivalry/RAND Research Report 2020.pdf` |  | Yes | Not currently in DB readings. |
| 10 | LD19 Jun 1 | Quang (2019) | workspace file not found |  | Yes | Canvas schedule labels this as Reading 2. |
| 10 | LD19 Jun 1 | ASPI Report (2020), introduction | workspace file not found |  | Yes | Canvas schedule lists intro only. |
| 10 | LD20 Jun 3 | No assigned reading |  |  | No | Course wrap-up; no discussion post. |

## Policies

- AI/tool policy: No explicit AI policy found in the syllabus text. Apply Claudia's AI disclosure SOP for graded work assisted by agents; do not assume silence equals permission.
- Academic integrity: GPS does not tolerate plagiarism, cheating, or dishonesty. Analytic work is expected to be Edgar's own; all sources/data must be recognized and cited. Suspected cases are referred to Academic Integrity.
- Late work: No general late-work policy found in the extracted syllabus. Use Canvas/instructor updates for discussion-post exceptions.
- Make-up exams: No make-up exams without an approved and documented excuse. Illness must be documented by UCSD health service; death or serious illness in immediate family is acceptable; otherwise only standing University policy excuses. Notify instructor in writing.
- Attendance/participation: Students are required to attend two lectures each week, read before class, and participate actively. Discussion posts and in-class attendance quizzes each count for half of participation.
- Submission format for discussion posts: clearly stated question plus no more than 3 sentences explaining importance.
- Grade disputes: Written memo of no more than 400 words within seven calendar days after graded work is returned.
- Accommodations: AFA letters through OSD; requests for exam accommodations should be made at least two weeks before the midterm exam.

## DB Normalization Notes

- Rows already present in `assignments`: individual discussion posts through LD10; recurring discussion-post row; recurring attendance-quiz row; Midterm 1; Midterm 2; Final Exam.
- Rows to add: individual future discussion-post rows for LD11, LD14, LD15, LD16, LD18, and LD19, with due dates listed above and confidence `inferred` until Canvas assignment rows are visible. Consider LD12 only after Canvas verifies an assigned reading and post requirement.
- Rows to update: mark LD9 and LD10 completed if Edgar submitted them; otherwise keep pending. Keep LD10 confidence `inferred` unless Canvas confirms exact due time.
- Rows to avoid: no discussion-post rows for LD1, LD7, LD13, LD17, or LD20 unless Canvas later creates one explicitly.
- Readings rows to add: Jansen (2001), Huff (1995), Hicken (2008), Malesky/Abrami/Zheng (2011), Ravanilla/Sexton/Haim (2022), Ostwald (2013), Slater (2010) Ch. 1, Tajima/Samphantharak/Ostwald (2018), Hayton (2021), RAND (2020), Quang (2019), ASPI (2020). LD12 reading remains unknown.
- Readings rows to update: `readings.id=70` author should likely be `Hayton, Bill`, not `Heyton, Bill`; `readings.id=71` should likely have authors `Dell, Melissa; Lane, Nathan; Querubin, Pablo` and week=2.
- Daily-dispatch safety: Eos should treat recurring discussion posts as a backstop, but known future posts need individual DB rows so today/tomorrow scans do not miss them. Canvas/email notifications override inferred syllabus-pattern rows and should update the row source/confidence.
- Attendance quizzes: Keep recurring attendance row active. Add individual attendance quiz rows only where Canvas exposes dated quiz items, because the syllabus does not list every quiz date separately.
- Ambiguities needing verification: LD12 date, readings, and discussion-post requirement; exact Canvas due times for future discussion posts; missing local files for Quang (2019) and ASPI (2020); identity of `to_extract_and_to_organize.pdf` as Slater Ch. 1.

---
Generated for: Edgar Agunias
Date: 2026-04-28
Model: GPT-5 Codex
Sources: GPPS 463 syllabus PDF, Canvas course schedule export PDF, current Claudia DB GPPS 463 assignments/readings rows, Poseidon course memory
Agent: Poseidon
---
