#!/usr/bin/env python3
"""
Discovery ETL: pull thrift-store place_ids for San Diego and upsert into Postgres.
Run with:  python etl/discovery.py
"""

import os, sys, time, logging, requests, psycopg2
from psycopg2.extras import execute_batch, Json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)

GOOGLE_KEY   = os.getenv("GOOGLE_PLACES_KEY")
LAT          = os.getenv("SD_CENTER_LAT", "32.7157")
LNG          = os.getenv("SD_CENTER_LNG", "-117.1611")
RADIUS       = os.getenv("DISCOVERY_RADIUS_M", "30000")

if not GOOGLE_KEY:
    logging.error("GOOGLE_PLACES_KEY missing in env"); sys.exit(1)

DSN = "dbname={PGDATABASE} user={PGUSER} host={PGHOST} password={PGPASSWORD}".format(**os.environ)

TEXT_SEARCH = (
    "https://maps.googleapis.com/maps/api/place/textsearch/json"
    "?query=thrift%20store&location={lat},{lng}&radius={rad}&type=store&key={key}"
)

def fetch_page(url):
    for attempt in range(5):
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        if r.status_code in {429, 500, 503}:
            delay = 2 ** attempt
            logging.warning("Rate-limited (%s). Sleep %ss", r.status_code, delay)
            time.sleep(delay)
            continue
        r.raise_for_status()
    raise RuntimeError("Gave up after 5 retries")

def run():
    logging.info("Connecting to Postgres…")
    with psycopg2.connect(DSN) as conn, conn.cursor() as cur:
        url = TEXT_SEARCH.format(lat=LAT, lng=LNG, rad=RADIUS, key=GOOGLE_KEY)
        total, inserted = 0, 0

        while url:
            data = fetch_page(url)
            rows = [
                (
                    p["place_id"],
                    p["name"],
                    p.get("formatted_address", ""),
                    p["geometry"]["location"]["lat"],
                    p["geometry"]["location"]["lng"],
                )
                for p in data.get("results", [])
            ]
            total += len(rows)

            execute_batch(
                cur,
                """
                INSERT INTO stores (place_id, name, address, lat, lng)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (place_id)
                DO UPDATE SET
                    name=EXCLUDED.name,
                    address=EXCLUDED.address,
                    lat=EXCLUDED.lat,
                    lng=EXCLUDED.lng,
                    is_active=TRUE
                """,
                rows,
            )
            inserted += cur.rowcount
            conn.commit()

            next_token = data.get("next_page_token")
            url = (
                f"{TEXT_SEARCH}&pagetoken={next_token}" if next_token else None
            )
            if next_token:
                time.sleep(2)  # Google requirement

        logging.info("Done. scanned=%s  upserts=%s", total, inserted)

if __name__ == "__main__":
    run()
