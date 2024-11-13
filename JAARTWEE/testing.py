import sqlite3

# Maak een verbinding met de SQLite database (of maak een nieuwe aan als deze niet bestaat)
conn = sqlite3.connect("studenten_database.db")
cursor = conn.cursor()

# Stap 1: Maak de tabellen voor studentinfo, open dagen, en inschrijving
cursor.execute("""
CREATE TABLE IF NOT EXISTS Studentinfo (
    student_id INTEGER PRIMARY KEY,
    naam TEXT NOT NULL,
    email TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS OpenDagen (
    opendag_id INTEGER PRIMARY KEY,
    locatie TEXT NOT NULL,
    datum TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Inschrijving (
    inschrijving_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    opendag_id INTEGER,
    aanwezigheid BOOLEAN DEFAULT 0,
    FOREIGN KEY (student_id) REFERENCES Studentinfo(student_id),
    FOREIGN KEY (opendag_id) REFERENCES OpenDagen(opendag_id)
)
""")

# Stap 2: Voeg voorbeelddata toe aan de tabellen (INSERT INTO)
# Voeg een student toe
cursor.execute("""
INSERT INTO Studentinfo (naam, email) VALUES
('Jan Jansen', 'jan.jansen@example.com')
""")
cursor.execute("""
INSERT INTO Studentinfo (naam, email) VALUES
('Piet Pietersen', 'piet.pietersen@example.com')
""")

# Voeg een open dag toe
cursor.execute("""
INSERT INTO OpenDagen (locatie, datum) VALUES
('Amsterdam', '2024-12-01')
""")
cursor.execute("""
INSERT INTO OpenDagen (locatie, datum) VALUES
('Rotterdam', '2024-12-15')
""")

# Voeg inschrijvingen toe voor de studenten
cursor.execute("""
INSERT INTO Inschrijving (student_id, opendag_id) VALUES
(1, 1)
""")
cursor.execute("""
INSERT INTO Inschrijving (student_id, opendag_id) VALUES
(2, 2)
""")

# Opslaan van wijzigingen in de database
conn.commit()

# Stap 3: Update query - Markeer dat een student aanwezig is op een open dag
# Stel aanwezigheid van student met inschrijving_id 1 in op 'aanwezig' (1)
cursor.execute("""
UPDATE Inschrijving
SET aanwezigheid = 1
WHERE inschrijving_id = 1
""")

# Markeer ook dat de tweede student aanwezig was
cursor.execute("""
UPDATE Inschrijving
SET aanwezigheid = 1
WHERE inschrijving_id = 2
""")

# Opslaan van wijzigingen in de database
conn.commit()

# Stap 4: Query om gegevens op te halen van studenten die aanwezig waren op een open dag
print("\nAanwezige studenten op open dagen:")
cursor.execute("""
SELECT Studentinfo.naam, Studentinfo.email, OpenDagen.locatie, OpenDagen.datum
FROM Inschrijving
INNER JOIN Studentinfo ON Inschrijving.student_id = Studentinfo.student_id
INNER JOIN OpenDagen ON Inschrijving.opendag_id = OpenDagen.opendag_id
WHERE Inschrijving.aanwezigheid = 1
""")

# Print de resultaten van de query
for row in cursor.fetchall():
    print(f"Naam: {row[0]}, Email: {row[1]}, Locatie: {row[2]}, Datum: {row[3]}")

# Sluit de databaseverbinding
conn.close()
