---
name: daily-briefing
description: Daily morning briefing with calendar, both email inboxes, and UCSD weather
---

You are generating a daily morning briefing for Edgar (edgar.agunias@gmail.com / eagunias@ucsd.edu). Your goal is to produce a clear, well-organized snapshot of his day across calendar, email, and weather.

Follow these steps in order:

## 0. Time Tracker Sync
Before gathering any external data, run the time tracker sync to ensure the database reflects the latest CSV:

```
python3 _claudia/sync_timelog.py
```

Then regenerate the dashboard so stats are current:

```
python3 _claudia/dashboard.py
```

Print the sync summary line ("Rows imported: N, Total hours: X.XX") in the briefing under the header below. If either command fails, note the error and continue -- do not abort the briefing.

## 1. Weather — UCSD / La Jolla, CA
Search the web for today's weather forecast for La Jolla, CA 92037 (near UC San Diego). Include:
- Today's high and low temperatures
- Conditions (sunny, cloudy, rain, etc.)
- Any active weather advisories or alerts

## 2. Google Calendar
Search ALL five of Edgar's calendars for today's events. Use the gcal_list_events tool for each calendar ID:
- **001 Personal**: edgar.agunias@gmail.com
- **002 Learning**: dicjpk2av0g6nkujknnesgu8fs@group.calendar.google.com
- **003 Deadlines**: v92252vbd42kh2gpbomtatttu0@group.calendar.google.com
- **004 Meals**: t911bgee9nie57kkgbmbhi9eqg@group.calendar.google.com
- **005 UCSD**: prpr87jk4kd4kkrs29sa29m5c4@group.calendar.google.com

For each calendar, pull events with timeMin = today at 00:00:00 and timeMax = today at 23:59:59. Aggregate all results and organize by category (Exams, Meals, Work, Learning, etc.). List each event with its time, title, location (if any), and source calendar.

## 3. Personal Gmail (edgar.agunias@gmail.com)
Use gmail_search_messages with query `is:unread newer_than:2d` to surface recent unread emails. Summarize the most important ones, grouped by theme (finance, security, social, etc.). Flag anything that requires action.

## 4. UCSD Email (eagunias@ucsd.edu)
Use gmail_search_messages with query `to:eagunias@ucsd.edu is:unread newer_than:2d` to check the school inbox. Summarize unread messages. Flag anything academic, administrative, or time-sensitive.

## 5. Compile the Briefing
Present the briefing in this format, using APA 7 style for any citations:

---
## ☀️ Daily Briefing — [Today's Date, e.g. Monday, March 16, 2026]

### 📊 Time Tracker Sync
[One-line sync summary: rows imported, total hours, any errors]

### 🌡️ Weather — La Jolla / UCSD
[Forecast summary with any advisories]

### 🗓️ Calendar — Today
[List of events, or "No events scheduled today."]

### 📬 Personal Gmail (edgar.agunias@gmail.com)
[Grouped summary of unread emails with action flags]

### 🎓 UCSD Email (eagunias@ucsd.edu)
[Summary of unread school emails with action flags]

### ✅ Action Items
[Numbered list of concrete things Edgar should do today, drawn from all sources]

### 🔀 Delegation Suggestions
Review all briefing items (emails, calendar events, action items) for tasks that could be routed to a specialist agent. Use this mapping:

| Course / Domain | Agent |
|---|---|
| GPCO 403 — Intl Economics (Handley) | Plutus |
| GPCO 410 — Intl Pol & Security (Praether) | Athena |
| GPEC 446 — QM3 (Valasquez) | Tyche |
| GPPS 444 — History of Warfare (Thomas) | Ares |
| GPPS 463 — Politics of SEA (Ravanilla) | Poseidon |
| Cross-class research or synthesis | Atlas |
| File sorting, concept lookups, DB queries | Mnemosyne |

For each suggestion, use this format:
- **[Agent Name]** — [Task description] — Confidence: `high` or `low`

Use `high` when the match is obvious (e.g., a new GPCO 403 assignment should go to Plutus). Use `low` when the routing is ambiguous or the task could span multiple agents.

These suggestions are written for Claudia (the orchestrator), not for Edgar directly. Claudia will execute `high`-confidence delegations immediately and confirm `low`-confidence ones with Edgar before acting.

If nothing warrants delegation, write "No delegation suggestions today."
---

## Constraints & preferences
- Use APA 7 formatting for any citations or sources
- Keep the tone warm but professional
- Do not include marketing emails, spam, or routine automated digests in the action items — only surface things that genuinely need attention
- If the calendar is empty, say so clearly
- End the briefing cleanly — do not ask follow-up questions
