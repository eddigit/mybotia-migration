PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE client_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        session_key TEXT NOT NULL DEFAULT 'main',
        content TEXT DEFAULT '',
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(client_id, session_key)
    );
COMMIT;
