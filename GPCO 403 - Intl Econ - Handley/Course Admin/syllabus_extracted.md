# GPCO 403 Syllabus Extraction

## Sources Inspected

- `GPCO 403 - Intl Econ - Handley/Course Admin/GPCO 403 Syllabus 2026_post.pdf` - canonical Spring 2026 syllabus; extracted with `pdftotext -layout`.
- `_claudia/claudia.db` - current `courses`, `assignments`, and `readings` rows for `course_id=1`.
- `GPCO 403 - Intl Econ - Handley/_agent/AGENT_CONTEXT.md` - Plutus course memory.
- `GPCO 403 - Intl Econ - Handley/_agent/ASSIGNMENTS.md` - local assignment tracker.
- `_claudia/system/deadline-data-contract.md` - deadline normalization standard.
- `_claudia/system/syllabus-extraction-template.md` - artifact structure.

## Course Basics

- Course: GPCO 403, International Economics
- Instructor: Professor Kyle Handley, `khandley@ucsd.edu`
- Term: Spring 2026
- Meeting pattern: Monday/Wednesday, 2:00-3:20 PM
- Location: Robinson Auditorium
- Instructor office hours: Monday 12:30-1:30 PM, Wednesday 3:30-4:30 PM, and by appointment
- TA: Chloe Margulis, `cmargulis@ucsd.edu`
- TA office hours: Tuesday 2:00-3:00 PM and Thursday 12:30-1:30 PM, RBC Room 3131
- Required text: Robert Feenstra and Alan Taylor, *International Economics*, 5th ed., 2021. Syllabus says older 3rd/4th editions are acceptable.

## Assignments And Deadlines

| Title | Due Date | Due Time | Timezone | Weight | Submission | Source | Confidence | Notes |
|---|---|---:|---|---:|---|---|---|---|
| Concept Check 1 | 2026-04-06 | 23:59 | America/Los_Angeles | 4% | Canvas quiz | syllabus pp. 3, 5; DB id 1 | verified | Opens 2026-04-01. Current DB status: completed; grade `14.1/17`. Lowest concept check dropped. |
| Data Brief 1 | 2026-04-17 | 23:59 | America/Los_Angeles | 5% | Canvas | syllabus pp. 3, 5; DB id 2 | verified | Opens 2026-04-08. Compare assigned country to U.S. macro indicators. Current DB status: completed. |
| Concept Check 2 | 2026-04-20 | 23:59 | America/Los_Angeles | 4% | Canvas quiz | syllabus pp. 3, 5; DB id 3 | verified | Opens 2026-04-15. Current DB status: pending, but due date has passed as of 2026-04-28; verify completion status. |
| Concept Check 3 | 2026-04-28 | 23:59 | America/Los_Angeles | 4% | Canvas quiz | syllabus pp. 3, 5; DB id 4 | verified | Opens 2026-04-22. Due today on extraction date, 2026-04-28. |
| Midterm Exam | 2026-05-04 | 14:00 | America/Los_Angeles | 30% | In class | syllabus pp. 4, 5; DB id 5 | verified | 2:00-3:20 PM; covers first 9-10 lectures, approximately first 5 weeks. |
| Concept Check 4 | 2026-05-18 | 23:59 | America/Los_Angeles | 4% | Canvas quiz | syllabus pp. 3, 5; DB id 6 | verified | Opens 2026-05-13. |
| Concept Check 5 | 2026-06-02 | 23:59 | America/Los_Angeles | 4% | Canvas quiz | syllabus pp. 3, 6; DB id 8 | ambiguous | Syllabus narrative says due Monday 2026-06-01; course grid says due Tuesday 2026-06-02. Existing DB uses 2026-06-02. Verify against Canvas. |
| Data Brief 2 | 2026-06-03 | 23:59 | America/Los_Angeles | 5% | Timed Canvas memo | syllabus pp. 3-4, 5-6; DB id 7 | verified | Opens 2026-05-20. Two-hour WTO trade-profile memo. Must begin no later than 2026-06-03 22:00 to receive full time. |
| Final Exam | 2026-06-08 | 08:00 | America/Los_Angeles | 40% | In class | syllabus p. 4; DB id 9 | verified | 8:00-11:00 AM. Cumulative, weighted toward final 5-6 weeks. |

## Recurring Obligations

| Obligation | Rule | Due Time | Weight | Source | Notes |
|---|---|---:|---:|---|---|
| Attendance and class engagement | Attend regularly, stay actively engaged, and minimize distractions. |  | Participation/engagement not separately weighted in syllabus grade table | syllabus p. 4 | Visible off-task device use may affect classroom participation and engagement assessment. |
| Canvas monitoring | Check Canvas for announcements, handouts, notes, links, and added readings. |  |  | syllabus p. 2 | Additional readings may be added later and marked required or background. |
| Newspaper/current-events reading | Read and analyze international/domestic economic news to check understanding. |  |  | syllabus p. 2 | Suggested outlets include Financial Times, The Economist, Bloomberg, NYT, WSJ, Washington Post, and BusinessWeek. |

## Exams And In-Class Assessments

| Title | Date | Time | Location | Weight | Source | Notes |
|---|---|---:|---|---:|---|---|
| Midterm Exam | 2026-05-04 | 14:00-15:20 | Robinson Auditorium | 30% | syllabus pp. 4, 5; DB id 5 | In class; short answer and multiple choice; first 9-10 lectures / roughly weeks 1-5. |
| Final Exam | 2026-06-08 | 08:00-11:00 | Not specified in syllabus | 40% | syllabus p. 4; DB id 9 | Short answer and multiple choice; cumulative, weighted toward final 5-6 weeks. |

## Readings By Week

| Week | Date/Session | Reading | File Path | Pages | Required? | Notes |
|---:|---|---|---|---:|---|---|
| 1 | Mar 30 / Apr 1 | Feenstra and Taylor Ch. 1; Ch. 16.1-16.2 | textbook; DB readings id 1, 2 |  | Yes | Introduction; GDP and national income accounting. DB status: completed for both. |
| 2 | Apr 6 / Apr 8 | Feenstra and Taylor Ch. 12.2, 16.3-16.5 | textbook; DB reading id 3 |  | Yes | Balance of payments/current account. DB status: completed. |
| 3 | Apr 13 / Apr 15 | Feenstra and Taylor Ch. 12.1, 13.1-13.4, 14.1; The Economist Big Mac Index | textbook / Canvas; DB readings id 4, 6 |  | Yes | Exchange rates, law of one price, PPP, Big Mac application. DB status: pending. |
| 4 | Apr 20 / Apr 22 | Feenstra and Taylor Ch. 12.3, 15.5, 19.1-19.4 | textbook; DB reading id 5 |  | Yes | External wealth, valuation effects, consumption smoothing, crises. DB status: pending. |
| 5 | Apr 27 / Apr 29 | No new reading separately listed in reading section |  |  |  | Course grid: PPP/LOOP/Big Mac application, midterm roadmap, optional recorded evening review after class-week. Week labeling may differ from current Canvas folders. |
| 6 | May 4 / May 6 | Feenstra and Taylor Ch. 2; The Economist, "The miracle of trade" | textbook / Canvas; DB readings id 7, 8 |  | Yes | Midterm Monday; start trade and Ricardian model Wednesday. DB status: pending. |
| 7 | May 11 / May 13 | Feenstra and Taylor Ch. 4 and 17.1 if time permits | textbook; DB reading id 9 |  | Yes | Heckscher-Ohlin and factor endowments. DB status: pending. |
| 8 | May 18 / May 20 | Feenstra and Taylor Ch. 6 | textbook; DB reading id 10 |  | Yes | Firms, increasing returns, and trade. DB status: pending. |
| 9 | May 25 / May 27 | Feenstra and Taylor Ch. 8, 11.1-11.2; Amiti, Redding, and Weinstein (2019) | textbook / Canvas; DB readings id 11, 12 | 24 for Amiti et al. row | Yes | Trade and commercial policy. Monday 2026-05-25 is Memorial Day, no class. DB status: pending. |
| 10 | Jun 1 / Jun 3 | No new reading separately listed in reading section |  |  |  | Trade policy II and final roadmap. Data Brief 2 active window ends 2026-06-03 23:59. |

## Policies

- AI/tool policy: The syllabus does not state a course-specific AI policy beyond UCSD academic integrity. Use UCSD academic integrity as the controlling baseline and apply Claudia's AI disclosure SOP for any graded work where agents materially assist.
- Academic integrity: Students must honor normal academic integrity standards; failures are reported to the Office of Academic Integrity.
- Late work: Concept checks are due electronically on Canvas by 11:59 PM on the due date. Canvas remains open until 11:59 PM the following day, but late submissions are penalized. Other late-work rules are not specified in the syllabus.
- Attendance/participation: Regular attendance and active attention are expected. Laptops/tablets may be used for course purposes; phones should be put away unless needed for class.
- Submission format: Concept checks and data briefs are through Canvas. Data Brief 2 is a two-hour timed Canvas memo.
- Grading notes: Concept Checks 20% total with five checks at 4% each and the lowest score dropped; Data Briefs 10%; Midterm 30%; Final 40%. The syllabus grade table does not separately list participation despite the engagement policy.
- Accommodations: Formal disability accommodation requests should be presented within the first two weeks of class; GPS Student Services can help with documentation.
- Non-discrimination and harassment: GPS/UCSD policies apply.

## DB Normalization Notes

- Current DB assignment rows already include normalized deadline fields for all nine major rows: `due_time`, `timezone=America/Los_Angeles`, `deadline_source=syllabus`, `source_confidence`, `date_kind`, and `last_verified_at=2026-04-28`.
- Recommended assignment row update: row 3, `Concept Check 2`, is still `status=pending` despite due date 2026-04-20. Verify on Canvas or with Edgar and mark completed if submitted.
- Recommended assignment row update: row 4, `Concept Check 3`, is due today, 2026-04-28, at 23:59. Confirm submission after deadline.
- Recommended assignment row update: row 8, `Concept Check 5`, should remain `source_confidence=ambiguous` until Canvas resolves the conflict between 2026-06-01 and 2026-06-02.
- Recommended assignment row cleanup: row 7, `Data Brief 2`, notes currently duplicate the open/start constraint. Mnemosyne may simplify notes while preserving `opens_at=2026-05-20` and "must begin by 2026-06-03 22:00."
- Recommended source metadata update: assignment `source_path` currently points to this Markdown artifact. For auditability, Mnemosyne may prefer `source_path=GPCO 403 - Intl Econ - Handley/Course Admin/GPCO 403 Syllabus 2026_post.pdf` plus notes that the normalized interpretation lives here.
- Reading rows to add: none from the posted syllabus; current DB readings 1-12 cover the syllabus reading list.
- Reading rows to update: add local file paths when Canvas PDFs/textbook excerpts exist in the course folder, especially The Economist Big Mac Index, "The miracle of trade," and Amiti et al. (2019).
- Reading ambiguities: syllabus says additional Canvas readings may be added later and marked required/background. Re-check Canvas before weekly study-guide or daily-briefing use.
- Course-grid ambiguity: the narrative due-date list says Concept Check 5 is due Monday, June 1; the course grid says Tuesday, June 2. The current DB follows the grid.

## References

Amiti, M., Redding, S. J., & Weinstein, D. E. (2019). The impact of the 2018 tariffs on prices and welfare. *Journal of Economic Perspectives, 33*(4), 187-210.

Feenstra, R. C., & Taylor, A. M. (2021). *International economics* (5th ed.). Worth Publishers.

---
Generated for: Edgar Agunias
Date: 2026-04-28
Model: GPT-5 Codex (reasoning effort not exposed)
Sources: GPCO 403 Spring 2026 syllabus PDF; current `_claudia/claudia.db` assignment and reading rows; Plutus memory files; Claudia deadline contract and extraction template
Agent: Plutus
---
