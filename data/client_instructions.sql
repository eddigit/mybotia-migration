PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE client_instructions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            collaborateur TEXT DEFAULT '_global',
            instructions TEXT DEFAULT '',
            synced_at DATETIME DEFAULT NULL,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id),
            UNIQUE(client_id, collaborateur)
        );
INSERT INTO client_instructions VALUES(11,7,'_global','Vouvoyez-moi. VL Medical materiel medical.',NULL,'2026-02-27 11:21:33');
INSERT INTO client_instructions VALUES(12,7,'max','Droit medical, dispositifs medicaux.',NULL,'2026-02-27 11:21:33');
INSERT INTO client_instructions VALUES(13,3,'_global','',NULL,'2026-03-01 05:25:19');
INSERT INTO client_instructions VALUES(14,3,'lea','',NULL,'2026-03-01 05:25:19');
COMMIT;
