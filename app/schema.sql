DROP TABLE IF EXISTS nyc;

CREATE TABLE nyc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    address TEXT NOT NULL,
    latitude TEXT NOT NULL,
    longitude TEXT NOT NULL,
    label TEXT NOT NULL,
    submitted_by TEXT,
    comments TEXT
);