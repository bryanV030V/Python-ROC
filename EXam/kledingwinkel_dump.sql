BEGIN TRANSACTION;
CREATE TABLE gebruikers (
                id INTEGER PRIMARY KEY,
                gebruikersnaam TEXT NOT NULL,
                wachtwoord TEXT NOT NULL
            );
INSERT INTO "gebruikers" VALUES(1,'admin','admin123');
INSERT INTO "gebruikers" VALUES(2,'admin','admin123');
INSERT INTO "gebruikers" VALUES(3,'admin','admin123');
CREATE TABLE kledingstukken (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    merk TEXT NOT NULL,
    type TEXT NOT NULL,
    maat TEXT NOT NULL,
    hoeveelheid INTEGER NOT NULL
);
INSERT INTO "kledingstukken" VALUES(1,'Abercrombie & Fitch','Vest','M',10);
INSERT INTO "kledingstukken" VALUES(2,'Abbey Dawn','Broek','L',7);
INSERT INTO "kledingstukken" VALUES(3,'Nalini','Broek','S',6);
INSERT INTO "kledingstukken" VALUES(4,'Hummel International','Sweater','XL',10);
INSERT INTO "kledingstukken" VALUES(5,'Gsus','Jas','XXL',9);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('kledingstukken',5);
COMMIT;
