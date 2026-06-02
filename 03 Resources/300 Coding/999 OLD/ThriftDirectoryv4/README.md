# Thrift SD Scraper

Populate a Postgres DB with thrift stores in San Diego using the Google Places API.

## Quickstart

```sh
docker-compose up --build
```

## Environment Variables

See `.env.example` for required variables.

## Project Structure

- `etl/` — ETL scripts for discovery and details
- `db/` — Database schema
- `tests/` — Unit tests

## Scheduler

Add cron jobs in the scraper container for regular ETL runs.

## CI

GitHub Actions workflow in `.github/workflows/ci.yml`.
