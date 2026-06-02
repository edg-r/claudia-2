-- schema.sql
-- DDL for stores & reviews tables

CREATE TABLE IF NOT EXISTS stores (
    place_id   TEXT PRIMARY KEY,
    name       TEXT NOT NULL,
    address    TEXT NOT NULL,
    lat        NUMERIC(9,6),
    lng        NUMERIC(9,6),
    opening_hours JSONB,
    is_active  BOOLEAN DEFAULT TRUE,
    last_fetched TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reviews (
    id           BIGSERIAL PRIMARY KEY,
    place_id     TEXT REFERENCES stores(place_id) ON DELETE CASCADE,
    author_name  TEXT,
    rating       INT CHECK (rating BETWEEN 1 AND 5),
    text         TEXT,
    relative_time TEXT,
    created_at   TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_reviews_place_id ON reviews(place_id);
