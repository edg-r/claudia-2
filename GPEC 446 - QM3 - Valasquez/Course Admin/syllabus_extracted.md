# GPEC 446 Syllabus Extraction

## Sources Inspected

- `GPEC 446 - QM3 - Valasquez/Course Admin/QM3_Syllabus.pdf` - canonical syllabus for GPEC 446 / Applied Data Analysis and Statistical Decision Making.
- `_claudia/claudia.db` - current `courses`, `assignments`, and `readings` rows for course_id `3` / `GPEC 446`.
- `GPEC 446 - QM3 - Valasquez/_agent/AGENT_CONTEXT.md` - Tyche memory, especially the warning that folder week labels and syllabus week labels diverge.
- `_claudia/system/deadline-data-contract.md` and `_claudia/system/syllabus-extraction-template.md` - normalization contract and extraction format.

## Course Basics

- Course: GPEC 446, Applied Data Analysis and Statistical Decision Making
- Instructor: Mateo Vasquez-Cortes
- Term: Spring 2026
- Class: Tuesday/Thursday, 9:30-11:00 AM, Auditorium
- Data lab: Friday, 11:00 AM-12:00 PM, Auditorium
- TA section: Thursday, 2:00-3:00 PM, Room 3201
- Office hours:
  - Mateo: Thursday 12:00-2:00 PM, RBC 1306
  - David Vargas: Thursday 11:00 AM-12:00 PM, 262 Malik Hall
  - Vincent Alulu: Tuesday 3:30-4:30 PM, Room 313
  - Ofri Mantell: Wednesday 12:30-1:30 PM, Room 3131
- Software: R for all data analysis exercises.

## Assignments And Deadlines

| Title | Due Date | Due Time | Timezone | Weight | Submission | Source | Confidence | Notes |
|---|---|---:|---|---:|---|---|---|---|
| Homework I | 2026-04-26 | 23:59 | America/Los_Angeles | 25% | TurnItIn | Canvas/assignment memory + DB | verified | Syllabus places HW I in Week 4 and says exact deadlines appear on the assignment. Current DB marks this completed and verified from Canvas/assignment memory. |
| Homework II | 2026-05-23 | 23:59 | America/Los_Angeles | 25% | TurnItIn | syllabus + DB inference | inferred | Syllabus places HW II in Week 8 and says exact deadlines appear on the assignment. Current DB uses 2026-05-23 23:59; verify against Canvas when posted. |
| Data Project | 2026-06-07 | 23:59 | America/Los_Angeles | 25% | TBD | syllabus + DB inference | inferred | Syllabus places project in Week 10 and says details will be provided throughout the quarter. Current DB uses 2026-06-07 23:59; verify final due date and submission channel when posted. |

## Recurring Obligations

| Obligation | Rule | Due Time | Weight | Source | Notes |
|---|---|---:|---:|---|---|
| Data labs | Fridays, 11:00 AM-12:00 PM, Auditorium | 11:00 |  | syllabus | Strongly encouraged; coding skills and hands-on homework support. |
| TA sections | Thursdays, 2:00-3:00 PM, Room 3201 | 14:00 |  | syllabus | Review lecture material, work through practice problems, and ask questions. |
| Class meetings | Tuesdays and Thursdays, 9:30-11:00 AM, Auditorium | 09:30 |  | syllabus | Regular lecture meetings. |

## Exams And In-Class Assessments

| Title | Date | Time | Location | Weight | Source | Notes |
|---|---|---:|---|---:|---|---|
| Midterm Exam | 2026-05-05 | 09:30-11:00 | Auditorium | 25% | syllabus + DB | In-class exam on Tuesday of Week 6. Current DB row is verified and `date_kind='in_class'`. |

## Readings By Week

| Week | Date/Session | Reading | File Path | Pages | Required? | Notes |
|---:|---|---|---|---:|---|---|
| 1 | Week 1 | Angrist & Pischke, *Mastering 'Metrics*, Ch. 1 | `GPEC 446 - QM3 - Valasquez/Course Admin/Joshua D. Angrist, Jörn-Steffen Pischke - Mastering 'Metrics_ The Path from Cause to Effect (2014, Princeton University Press).pdf` | 46 | Suggested | Causality and quantitative analysis: selection, random assignment, intro regression. DB row 13 matches topic and chapter. |
| 2 | Week 2 | Angrist & Pischke, *Mastering 'Metrics*, Ch. 2 | same PDF as above | 51 | Suggested | Regression for causal inference, regression as stratification, omitted-variable bias. DB row 14 matches. |
| 3 | Week 3 | Angrist & Pischke, *Mastering 'Metrics*, Ch. 3 | same PDF as above | 49 | Suggested | Instrumental variables, 2SLS, LATE identifying conditions. DB row 15 matches. |
| 4 | Week 4 | Angrist & Pischke, *Mastering 'Metrics*, Ch. 5; Wooldridge, Ch. 13 | Mastering 'Metrics PDF + Wooldridge source TBD/Canvas |  | Suggested | Panel data basics, fixed effects, DiD. DB row 16 title currently says "Mastering Metrics Ch 4 + Wooldridge Ch 13"; update to Ch. 5. |
| 5 | Week 5 | Angrist & Pischke, *Mastering 'Metrics*, Ch. 5; Wooldridge, Ch. 14 | Mastering 'Metrics PDF + Wooldridge source TBD/Canvas |  | Suggested | DiD II, staggered treatment adoption, event study designs. DB row 17 title currently says "Mastering Metrics Ch 4 + Wooldridge Ch 14"; update to Ch. 5. |
| 6 | Week 6 | Additional readings | Canvas/TBD |  | Suggested | Matching and synthetic control methods. DB row 18 currently lists "Mastering Metrics Ch 2 review + Matching/Synthetic Control"; syllabus only says additional readings. |
| 7 | Week 7 | Angrist & Pischke, *Mastering 'Metrics*, Ch. 4 | Mastering 'Metrics PDF |  | Suggested | Regression discontinuity design. DB row 19 currently says "Mastering Metrics Ch 5"; update to Ch. 4. |
| 8 | Week 8 | Gerber & Green, Ch. 3 | Canvas/TBD |  | Suggested | Experiments I, experimental design, stratification and block randomization. DB row 20 matches topic but has no file path/pages. |
| 9 | Week 9 | Gerber & Green, Ch. 4 | Canvas/TBD |  | Suggested | Experiments II, non-compliance, factorial designs and interaction effects. DB row 21 matches topic but has no file path/pages. |
| 10 | Week 10 | Wooldridge, Ch. 10 and Ch. 11 | Canvas/TBD |  | Suggested | Time series, lagged variables, seasonality. DB row 22 matches topic but has no file path/pages. |

## Policies

- AI/tool policy: AI tools may be used to help with coding tasks and to better understand literature and key topics.
- Written-explanation policy: All written explanations must be composed by Edgar. AI-generated written homework responses are treated as academic dishonesty and referred to the UCSD Office of Academic Integrity.
- Collaboration: Students may discuss concepts behind homework questions and share code snippets to improve programming ability. The writeup must be 100% individual.
- Submission format: Homework is submitted through TurnItIn.com.
- Late work: No general late-work rule appears in the syllabus. Exact homework deadlines are assignment-specific.
- Attendance/participation: Friday data labs are strongly encouraged; TA sections are weekly review/support sessions.
- Grading notes: Homework I 25%, Homework II 25%, in-class midterm 25%, data project 25%.

## DB Normalization Notes

- Rows to add:
  - Consider adding recurring rows for Friday data labs and Thursday TA sections, with `is_recurring=1`, `date_kind='recurring'`, and no assignment weight.
- Rows to update:
  - Assignment row 12 / Homework II: keep as inferred until Canvas posts exact deadline; `deadline_source='syllabus'` is acceptable only if notes preserve that the exact date/time is inferred from Week 8 and DB memory.
  - Assignment row 13 / Data Project: keep as inferred until project instructions post; submission channel remains TBD.
  - Reading row 16: change title from `Mastering Metrics Ch 4 + Wooldridge Ch 13 (Panel Data/DiD)` to `Mastering Metrics Ch 5 + Wooldridge Ch 13 (Panel Data/DiD)`.
  - Reading row 17: change title from `Mastering Metrics Ch 4 + Wooldridge Ch 14 (DiD II / Staggered)` to `Mastering Metrics Ch 5 + Wooldridge Ch 14 (DiD II / Staggered)`.
  - Reading row 19: change title from `Mastering Metrics Ch 5 (Regression Discontinuity Design)` to `Mastering Metrics Ch 4 (Regression Discontinuity Design)`.
  - Reading rows 16-22: add file paths/page counts once Wooldridge, Gerber & Green, and additional readings are available locally or in Canvas.
- Rows to mark completed:
  - Assignment row 10 / Homework I is already marked completed in the current DB.
- Ambiguities needing verification:
  - Exact due date/time for Homework II.
  - Exact due date/time and submission channel for the Data Project.
  - Whether Week 6 matching/synthetic-control readings are Canvas papers only or include a specific textbook chapter.
  - Whether labs/sections should be represented in `assignments`, a separate calendar layer, or only in course memory/dispatch logic.

## References

Angrist, J. D., & Pischke, J.-S. (2014). *Mastering 'metrics: The path from cause to effect*. Princeton University Press.

Angrist, J. D., & Pischke, J.-S. (2009). *Mostly harmless econometrics: An empiricist's companion*. Princeton University Press.

Gerber, A. S., & Green, D. P. (2012). *Field experiments: Design, analysis, and interpretation*. W. W. Norton.

Hansen, B. E. (2022). *Econometrics*. Princeton University Press.

Wooldridge, J. M. (2020). *Introductory econometrics: A modern approach* (7th ed.). Cengage Learning.

---
Generated for: Edgar Agunias
Date: 2026-04-28
Model: GPT-5 Codex
Sources: GPEC 446 QM3 syllabus PDF, current claudia.db GPEC 446 assignment/readings rows, Tyche agent memory, deadline data contract
Agent: Tyche
---
