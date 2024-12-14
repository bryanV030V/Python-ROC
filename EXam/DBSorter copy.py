import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import pandas as pd  # Voor het exporteren naar Excel

# Maak of verbind met een SQLite database
conn = sqlite3.connect('kledingwinkel.db')
c = conn.cursor()

# Maak tabellen als ze nog niet bestaan
c.execute('''
CREATE TABLE IF NOT EXISTS kledingstukken (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    merk TEXT NOT NULL,
    type TEXT NOT NULL,
    maat TEXT NOT NULL,
    hoeveelheid INTEGER NOT NULL
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS gebruikers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gebruikersnaam TEXT UNIQUE NOT NULL,
    wachtwoord TEXT NOT NULL
)
''')
conn.commit()

# Functie voor inloggen
def login():
    gebruikersnaam = gebruikersnaam_entry.get().strip()
    wachtwoord = wachtwoord_entry.get().strip()

    if not gebruikersnaam or not wachtwoord:
        messagebox.showerror("Fout", "Alle velden zijn verplicht!")
        return

    c.execute("SELECT * FROM gebruikers WHERE gebruikersnaam = ? AND wachtwoord = ?", (gebruikersnaam, wachtwoord))
    gebruiker = c.fetchone()

    if gebruiker:
        login_frame.pack_forget()
        main_frame.pack(fill="both", expand=True)
        update_lijst()
    else:
        messagebox.showerror("Fout", "Ongeldige inloggegevens!")

# Functie voor registratie
def registreer():
    gebruikersnaam = gebruikersnaam_entry.get().strip()
    wachtwoord = wachtwoord_entry.get().strip()

    if not gebruikersnaam or not wachtwoord:
        messagebox.showerror("Fout", "Alle velden zijn verplicht!")
        return

    try:
        c.execute("INSERT INTO gebruikers (gebruikersnaam, wachtwoord) VALUES (?, ?)", (gebruikersnaam, wachtwoord))
        conn.commit()
        messagebox.showinfo("Succes", "Registratie geslaagd! Log nu in.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Fout", "Gebruikersnaam bestaat al!")

# Functie om kledingstuk toe te voegen of bij te werken
def voeg_kledingstuk_toe():
    merk = merk_combobox.get().strip()
    type_ = type_combobox.get().strip()
    maat = maat_combobox.get().strip()
    hoeveelheid = hoeveelheid_combobox.get().strip()

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

    c.execute("SELECT * FROM kledingstukken WHERE merk = ? AND type = ? AND maat = ?", (merk, type_, maat))
    kledingstuk = c.fetchone()

    if kledingstuk:
        nieuwe_hoeveelheid = kledingstuk[4] + hoeveelheid
        c.execute("UPDATE kledingstukken SET hoeveelheid = ? WHERE id = ?", (nieuwe_hoeveelheid, kledingstuk[0]))
        messagebox.showinfo("Succes", "Hoeveelheid bijgewerkt!")
    else:
        c.execute("INSERT INTO kledingstukken (merk, type, maat, hoeveelheid) VALUES (?, ?, ?, ?)", (merk, type_, maat, hoeveelheid))
        messagebox.showinfo("Succes", "Nieuw kledingstuk toegevoegd!")

    conn.commit()
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

# Functie om de lijst bij te werken
def update_lijst():
    lijstbox.delete(0, tk.END)
    
    query = "SELECT * FROM kledingstukken WHERE 1=1"
    params = []

    filter_merk = filter_merk_combobox.get().strip()
    filter_type = filter_type_combobox.get().strip()
    filter_maat = filter_maat_combobox.get().strip()
    filter_hoeveelheid = filter_hoeveelheid_combobox.get().strip()

    if filter_merk:
        query += " AND merk LIKE ?"
        params.append(f"%{filter_merk}%")
    if filter_type:
        query += " AND type LIKE ?"
        params.append(f"%{filter_type}%")
    if filter_maat:
        query += " AND maat LIKE ?"
        params.append(f"%{filter_maat}%")
    if filter_hoeveelheid:
        try:
            hoeveelheid = int(filter_hoeveelheid)
            query += " AND hoeveelheid = ?"
            params.append(hoeveelheid)
        except ValueError:
            messagebox.showerror("Fout", "Hoeveelheid filter moet een positief geheel getal zijn!")
            return
    
    c.execute(query, params)
    
    for rij in c.fetchall():
        lijstbox.insert(tk.END, f"ID: {rij[0]}, Merk: {rij[1]}, Type: {rij[2]}, Maat: {rij[3]}, Hoeveelheid: {rij[4]}")

# Functie om kledingstukken naar Excel te exporteren
def exporteer_naar_excel():
    c.execute("SELECT * FROM kledingstukken")
    kledingstukken = c.fetchall()

    if not kledingstukken:
        messagebox.showerror("Fout", "Geen kledingstukken om te exporteren.")
        return
    
    df = pd.DataFrame(kledingstukken, columns=['ID', 'Merk', 'Type', 'Maat', 'Hoeveelheid'])
    try:
        df.to_excel('kledingvoorraad.xlsx', index=False, engine='openpyxl')
        messagebox.showinfo("Succes", "Data succesvol geëxporteerd naar kledingvoorraad.xlsx!")
    except Exception as e:
        messagebox.showerror("Fout", f"Er is een fout opgetreden bij het exporteren: {str(e)}")

# Functie om database te exporteren naar SQL
def exporteer_naar_sql():
    try:
        with open('kledingwinkel_dump.sql', 'w') as f:
            for lijn in conn.iterdump():
                f.write(f'{lijn}\n')
        messagebox.showinfo("Succes", "Database succesvol geëxporteerd naar kledingwinkel_dump.sql!")
    except Exception as e:
        messagebox.showerror("Fout", f"Er is een fout opgetreden bij het exporteren naar SQL: {str(e)}")

# UI setup voor inloggen
root = tk.Tk()
root.title("Kledingwinkel Voorraadbeheer")
root.geometry('800x600')

login_frame = tk.Frame(root)
login_frame.pack(fill="both", expand=True)

tk.Label(login_frame, text="Gebruikersnaam").pack(pady=5)
gebruikersnaam_entry = tk.Entry(login_frame)
gebruikersnaam_entry.pack(pady=5)

tk.Label(login_frame, text="Wachtwoord").pack(pady=5)
wachtwoord_entry = tk.Entry(login_frame, show="*")
wachtwoord_entry.pack(pady=5)

tk.Button(login_frame, text="Inloggen", command=login).pack(pady=10)
tk.Button(login_frame, text="Registreer", command=registreer).pack(pady=5)

main_frame = tk.Frame(root)
# Main frame UI
tk.Label(main_frame, text="Merk").grid(row=0, column=0, sticky="w", padx=5, pady=5)
merk_combobox = ttk.Combobox(main_frame)
merk_combobox.grid(row=0, column=1, sticky="ew", padx=5)

#scrape_knop = tk.Button(main_frame, text="Scrape Merken van Wikipedia", command=scrape_merken_van_wikipedia)
#scrape_knop.grid(row=0, column=2, sticky="ew", padx=5)

tk.Label(main_frame, text="Type").grid(row=1, column=0, sticky="w", padx=5)
type_combobox = ttk.Combobox(main_frame, values=["Shirt", "Sweater", "Jas", "Broek", "Trui", "Vest"])
type_combobox.grid(row=1, column=1, sticky="ew", padx=5)

tk.Label(main_frame, text="Maat").grid(row=2, column=0, sticky="w", padx=5)
maat_combobox = ttk.Combobox(main_frame, values=["XS", "S", "M", "L", "XL", "XXL"])
maat_combobox.grid(row=2, column=1, sticky="ew", padx=5)

tk.Label(main_frame, text="Hoeveelheid").grid(row=3, column=0, sticky="w", padx=5)
hoeveelheid_combobox = ttk.Combobox(main_frame, values=[str(i) for i in range(1, 11)])
hoeveelheid_combobox.grid(row=3, column=1, sticky="ew", padx=5)

voeg_toe_knop = tk.Button(main_frame, text="Voeg Kledingstuk Toe", command=voeg_kledingstuk_toe)
voeg_toe_knop.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew", padx=5)

verwijder_knop = tk.Button(main_frame, text="Verwijder Geselecteerd Kledingstuk", command=verwijder_kledingstuk)
verwijder_knop.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew", padx=5)

lijstbox = tk.Listbox(main_frame, width=60)
lijstbox.grid(row=6, column=0, columnspan=3, pady=10, sticky="nsew", padx=5)

# Zorg dat de listbox resizable is
main_frame.grid_rowconfigure(6, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

tk.Label(main_frame, text="Filter op Merk").grid(row=7, column=0, sticky="w", padx=5)
filter_merk_combobox = ttk.Combobox(main_frame)
filter_merk_combobox.grid(row=7, column=1, sticky="ew", padx=5)

tk.Label(main_frame, text="Filter op Type").grid(row=8, column=0, sticky="w", padx=5)
filter_type_combobox = ttk.Combobox(main_frame, values=["Shirt", "Sweater", "Jas", "Broek", "Trui", "Vest"])
filter_type_combobox.grid(row=8, column=1, sticky="ew", padx=5)

tk.Label(main_frame, text="Filter op Maat").grid(row=9, column=0, sticky="w", padx=5)
filter_maat_combobox = ttk.Combobox(main_frame, values=["XS", "S", "M", "L", "XL", "XXL"])
filter_maat_combobox.grid(row=9, column=1, sticky="ew", padx=5)

tk.Label(main_frame, text="Filter op Hoeveelheid").grid(row=10, column=0, sticky="w", padx=5)
filter_hoeveelheid_combobox = ttk.Combobox(main_frame, values=[str(i) for i in range(1, 11)])
filter_hoeveelheid_combobox.grid(row=10, column=1, sticky="ew", padx=5)

filter_knop = tk.Button(main_frame, text="Pas Filter Toe", command=update_lijst)
filter_knop.grid(row=11, column=0, columnspan=3, pady=10, sticky="ew", padx=5)

exporteer_excel_knop = tk.Button(main_frame, text="Exporteer naar Excel", command=exporteer_naar_excel)
exporteer_excel_knop.grid(row=12, column=0, columnspan=3, pady=10, sticky="ew", padx=5)

exporteer_sql_knop = tk.Button(main_frame, text="Exporteer naar SQL", command=exporteer_naar_sql)
exporteer_sql_knop.grid(row=13, column=0, columnspan=3, pady=10, sticky="ew", padx=5)

# Start de Tkinter-applicatie
root.mainloop()

# Sluit de databaseverbinding
conn.close()

