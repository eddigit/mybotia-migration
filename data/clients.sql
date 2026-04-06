PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            company_name TEXT NOT NULL,
            contact_name TEXT DEFAULT '',
            plan TEXT DEFAULT 'pro',
            max_tokens_month INTEGER DEFAULT 500000,
            is_admin INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_login DATETIME
        , photo_url TEXT DEFAULT '');
INSERT INTO clients VALUES(2,'coachdigitalparis@gmail.com','$2y$10$J5CYDUislRG4cYBuihNdJeYyKBrdM3.0VUnqVBrpdZXZW/h9rSt7G','Coach Digital','Gilles KORZEC','enterprise',2000000,1,'2026-02-25 12:36:03','2026-03-01 05:16:01','');
INSERT INTO clients VALUES(3,'lea@collaborateur.pro','$2y$10$1Tmmc9stBWVo0dU9qp3Se.x7Wu6o8fLctznDxoLpRngYP0p5OGKRa','Coach Digital','Léa','enterprise',2000000,1,'2026-02-25 16:58:17','2026-04-06 09:02:15','/uploads/profile/client_3_1772342713.jpg');
INSERT INTO clients VALUES(4,'julian@collaborateur.pro','$2y$10$.KOfxor8ZiXDGPDNZyEDdOU0N6Htnst8cVMTfMUAXQCvJ8l0X2Ayi','Coach Digital','Julian','enterprise',2000000,1,'2026-02-25 16:58:17','2026-02-27 11:31:46','');
INSERT INTO clients VALUES(5,'nina@collaborateur.pro','$2y$10$hSIU33XBYU/xiEGNUfPUnOga.3H6C1Tp.eizVAo5i6s8CIt0o3JN6','Coach Digital','Nina','enterprise',2000000,1,'2026-02-25 16:58:17','2026-02-27 11:31:46','');
INSERT INTO clients VALUES(6,'oscar@collaborateur.pro','$2y$10$VxescWynyAR.swrmYYI4XeH6ggyX6GvTPI58nM51YAMGXtZLJnHXW','Coach Digital','Oscar','enterprise',2000000,1,'2026-02-25 16:58:17','2026-02-27 11:31:46','');
INSERT INTO clients VALUES(7,'max.vlmedical@collaborateur.pro','$2y$10$mkNZHcmMAoqhzXATJOOEk.qm5ZULp6ScYQx1PBnhTibFuo11ucvJG','VL Medical','Max','pro',500000,0,'2026-02-27 11:21:33','2026-04-02 11:56:30','');
INSERT INTO clients VALUES(8,'eva.vlmedical@collaborateur.pro','$2y$10$mkNZHcmMAoqhzXATJOOEk.qm5ZULp6ScYQx1PBnhTibFuo11ucvJG','VL Medical','Eva','pro',500000,0,'2026-02-27 11:21:33','2026-02-27 11:31:46','');
INSERT INTO clients VALUES(9,'lucy@collaborateur.pro','$2y$10$J4ZYJ0djfnTCxfZZTIksw.ajjQdpoS9kMAUrWhlvS2WGlMmAiVUxK','IGH','Lucy','pro',500000,0,'2026-03-22 23:12:31',NULL,'');
COMMIT;
