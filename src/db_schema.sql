-- LogLens Blue: SQLite schema for log analysis

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_type TEXT,
    hostname TEXT,
    ts TEXT,
    ip TEXT,
    user TEXT,
    status TEXT,      -- 'success' | 'failure' | 'info' | 'warning'
    message TEXT,
    additional_tags JSON,
    original_file TEXT
);

CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT,
    severity INTEGER,
    ts TEXT,
    log_type TEXT,
    ip TEXT,
    user TEXT,
    hint TEXT,
    context JSON,
    event_id INTEGER,
    FOREIGN KEY(event_id) REFERENCES events(id)
);

CREATE TABLE IF NOT EXISTS stats_hourly (
    day_hour TEXT,
    log_type TEXT,
    count INTEGER,
    PRIMARY KEY(day_hour, log_type)
);

CREATE TABLE IF NOT EXISTS stats_daily_ip (
    day TEXT,
    ip TEXT,
    count INTEGER,
    PRIMARY KEY(day, ip)
);

CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT,
    mode TEXT,
    source_file TEXT,
    notes JSON
);

CREATE TABLE IF NOT EXISTS session_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    event_id INTEGER,
    verdict_user INTEGER,
    verdict_correct INTEGER,
    penalty INTEGER,
    FOREIGN KEY(session_id) REFERENCES sessions(id),
    FOREIGN KEY(event_id) REFERENCES events(id)
);


