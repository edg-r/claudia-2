# My Finances Dashboard

Local dashboard for the Actual Budget SQLite export in this folder.

## Run

```bash
cd "/Users/edgar/Documents/000 Files/My-Finances-cleaned-actual-export-v3"
python3 server.py
```

Open:

```text
http://127.0.0.1:8787
```

## SimpleFIN Token Setup

Do not put SimpleFIN credentials in `dashboard.html`, JavaScript, `metadata.json`, or `db.sqlite`.

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

Put the SimpleFIN access URL here:

```env
SIMPLEFIN_ACCESS_URL="https://USER:PASSWORD@bridge.simplefin.org/simplefin"
```

`.env.local` is ignored by git. The dashboard's **Sync SimpleFIN** button calls the local Python server, and the Python server reads `.env.local`, makes a timestamped `db.sqlite` backup, fetches SimpleFIN, updates balances, and inserts new deduped transactions.

If you only have a one-time app connection/setup token, put the Base64 token in `.env.local` as:

```env
SIMPLEFIN_ACCESS_URL="paste-one-time-token-here"
```

Then use **Sync SimpleFIN** or call the local claim endpoint once:

```bash
curl -X POST http://127.0.0.1:8787/api/claim-setup-token
```

The server decodes the token, POSTs the claim URL with an empty body, and replaces the token in `.env.local` with the returned access URL. A `403` at this stage means the one-time token was already claimed or expired; generate a fresh app connection token.

---
Generated for: Edgar Agunias
Date: 2026-05-15
Model: GPT-5 Codex
Sources: Local Actual Budget SQLite export, SimpleFIN protocol documentation, Claudia Hephaestus/Mnemosyne handoffs
Agent: Hephaestus, Mnemosyne, Claudia
---
