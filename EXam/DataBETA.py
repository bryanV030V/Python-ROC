import sqlite3
import tkinter as tk
from tkinter import messagebox

# Maak of verbind met een SQLite database
conn = sqlite3.connect('kledingwinkel.db')
c = conn.cursor()

# Maak de kledingstukken tabel als die nog niet bestaat
c.execute('''
CREATE TABLE IF NOT EXISTS kledingstukken (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    merk TEXT NOT NULL,
    type TEXT NOT NULL,
    maat TEXT NOT NULL,
    hoeveelheid INTEGER NOT NULL
)
''')
conn.commit()

# Functie om kledingstuk toe te voegen of bij te werken
def voeg_kledingstuk_toe():
    merk = merk_entry.get().strip()
    type_ = type_entry.get().strip()
    maat = maat_entry.get().strip()
    hoeveelheid = hoeveelheid_entry.get().strip()

    # Validatie van invoer
    if merk == "" or type_ == "" or maat == "" or hoeveelheid == "":
        messagebox.showerror("Fout", "Alle velden zijn verplicht!")
        return
    
    try:
        hoeveelheid = int(hoeveelheid)
        if hoeveelheid <= 0:
            raise ValueError("Hoeveelheid moet groter zijn dan 0.")
    except ValueError:
        messagebox.showerror("Fout", "Hoeveelheid moet een positief geheel getal zijn!")
        return

    # Controleer of er al een kledingstuk met hetzelfde merk, type en maat is
    c.execute("SELECT * FROM kledingstukken WHERE merk = ? AND type = ? AND maat = ?", (merk, type_, maat))
    kledingstuk = c.fetchone()

    if kledingstuk:
        # Update de hoeveelheid als het kledingstuk al bestaat
        nieuwe_hoeveelheid = kledingstuk[4] + hoeveelheid
        c.execute("UPDATE kledingstukken SET hoeveelheid = ? WHERE id = ?", (nieuwe_hoeveelheid, kledingstuk[0]))
        messagebox.showinfo("Succes", "Hoeveelheid bijgewerkt!")
    else:
        # Voeg een nieuw kledingstuk toe
        c.execute("INSERT INTO kledingstukken (merk, type, maat, hoeveelheid) VALUES (?, ?, ?, ?)", (merk, type_, maat, hoeveelheid))
        messagebox.showinfo("Succes", "Nieuw kledingstuk toegevoegd!")

    # Database opslaan en invoervelden leegmaken
    conn.commit()
    merk_entry.delete(0, tk.END)
    type_entry.delete(0, tk.END)
    maat_entry.delete(0, tk.END)
    hoeveelheid_entry.delete(0, tk.END)
    update_lijst()

# Functie om kledingstuk te verwijderen
def verwijder_kledingstuk():
    geselecteerd = lijstbox.curselection()
    if not geselecteerd:
        messagebox.showerror("Fout", "Selecteer een kledingstuk om te verwijderen.")
        return
    
    geselecteerd_id = lijstbox.get(geselecteerd).split(", ")[0].split(": ")[1]
    c.execute("DELETE FROM kledingstukken WHERE id = ?", (geselecteerd_id,))
    conn.commit()
    messagebox.showinfo("Succes", "Kledingstuk verwijderd.")
    update_lijst()

# Functie om de lijst van kledingstukken bij te werken in de UI
def update_lijst(filter_merk="", filter_type="", filter_maat=""):
    lijstbox.delete(0, tk.END)
    
    query = "SELECT * FROM kledingstukken WHERE 1=1"
    params = []

    if filter_merk:
        query += " AND merk LIKE ?"
        params.append(f"%{filter_merk}%")
    if filter_type:
        query += " AND type LIKE ?"
        params.append(f"%{filter_type}%")
    if filter_maat:
        query += " AND maat LIKE ?"
        params.append(f"%{filter_maat}%")
    
    c.execute(query, params)
    
    for rij in c.fetchall():
        lijstbox.insert(tk.END, f"ID: {rij[0]}, Merk: {rij[1]}, Type: {rij[2]}, Maat: {rij[3]}, Hoeveelheid: {rij[4]}")

# Functie voor filteren op basis van zoekcriteria
def zoek_kledingstukken():
    filter_merk = filter_merk_entry.get().strip()
    filter_type = filter_type_entry.get().strip()
    filter_maat = filter_maat_entry.get().strip()
    update_lijst(filter_merk, filter_type, filter_maat)

# UI setup met tkinter
root = tk.Tk()
root.title("Kledingwinkel Voorraadbeheer")

# Labels en invoervelden voor toevoegen/bijwerken van kledingstukken
tk.Label(root, text="Merk").grid(row=0, column=0)
merk_entry = tk.Entry(root)
merk_entry.grid(row=0, column=1)

tk.Label(root, text="Type (Shirt, Sweater, Jas, etc.)").grid(row=1, column=0)
type_entry = tk.Entry(root)
type_entry.grid(row=1, column=1)

tk.Label(root, text="Maat").grid(row=2, column=0)
maat_entry = tk.Entry(root)
maat_entry.grid(row=2, column=1)

tk.Label(root, text="Hoeveelheid").grid(row=3, column=0)
hoeveelheid_entry = tk.Entry(root)
hoeveelheid_entry.grid(row=3, column=1)

# Knop om kledingstuk toe te voegen of bij te werken
voeg_toe_knop = tk.Button(root, text="Voeg Kledingstuk Toe", command=voeg_kledingstuk_toe)
voeg_toe_knop.grid(row=4, column=0, columnspan=2, pady=10)

# Verwijderknop
verwijder_knop = tk.Button(root, text="Verwijder Geselecteerd Kledingstuk", command=verwijder_kledingstuk)
verwijder_knop.grid(row=5, column=0, columnspan=2, pady=10)

# Labels en invoervelden voor filteren/zoeken
tk.Label(root, text="Filter op Merk").grid(row=6, column=0)
filter_merk_entry = tk.Entry(root)
filter_merk_entry.grid(row=6, column=1)

tk.Label(root, text="Filter op Type").grid(row=7, column=0)
filter_type_entry = tk.Entry(root)
filter_type_entry.grid(row=7, column=1)

tk.Label(root, text="Filter op Maat").grid(row=8, column=0)
filter_maat_entry = tk.Entry(root)
filter_maat_entry.grid(row=8, column=1)

# Zoekknop
zoek_knop = tk.Button(root, text="Zoek Kledingstukken", command=zoek_kledingstukken)
zoek_knop.grid(row=9, column=0, columnspan=2, pady=10)

# Lijst van kledingstukken
lijstbox = tk.Listbox(root, height=10, width=50)
lijstbox.grid(row=10, column=0, columnspan=2, pady=10)

# Lijst bijwerken bij opstarten
update_lijst()

# Start de applicatie
root.mainloop()

# Sluit de databaseverbinding wanneer de applicatie wordt gesloten
conn.close()
