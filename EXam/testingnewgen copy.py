import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import pandas as pd  # Voor het exporteren naar Excel
import bcrypt  # Gebruik bcrypt voor veilige wachtwoordopslag

# Maak of verbind met een SQLite database
conn = sqlite3.connect('kledingwinkel.db')
c = conn.cursor()

# Maak de gebruikers tabel als die nog niet bestaat
c.execute('''
CREATE TABLE IF NOT EXISTS gebruikers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gebruikersnaam TEXT NOT NULL UNIQUE,
    wachtwoord_hash TEXT NOT NULL
)
''')

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

# Functie voor registratie
def registreer():
    gebruikersnaam = gebruikersnaam_entry.get().strip()
    wachtwoord = wachtwoord_entry.get().strip()

    if not gebruikersnaam or not wachtwoord:
        messagebox.showerror("Fout", "Gebruikersnaam en wachtwoord zijn verplicht!")
        return

    # Hash het wachtwoord
    wachtwoord_hash = bcrypt.hashpw(wachtwoord.encode('utf-8'), bcrypt.gensalt())

    try:
        c.execute("INSERT INTO gebruikers (gebruikersnaam, wachtwoord_hash) VALUES (?, ?)", (gebruikersnaam, wachtwoord_hash))
        conn.commit()
        messagebox.showinfo("Succes", "Registratie voltooid! Log nu in.")
        login_scherm()
    except sqlite3.IntegrityError:
        messagebox.showerror("Fout", "Gebruikersnaam bestaat al. Kies een andere.")

# Functie voor inloggen
def inloggen():
    gebruikersnaam = gebruikersnaam_entry.get().strip()
    wachtwoord = wachtwoord_entry.get().strip()

    if not gebruikersnaam or not wachtwoord:
        messagebox.showerror("Fout", "Gebruikersnaam en wachtwoord zijn verplicht!")
        return

    c.execute("SELECT wachtwoord_hash FROM gebruikers WHERE gebruikersnaam = ?", (gebruikersnaam,))
    gebruiker = c.fetchone()

    if gebruiker and bcrypt.checkpw(wachtwoord.encode('utf-8'), gebruiker[0]):
        messagebox.showinfo("Succes", "Inloggen geslaagd!")
        hoofdscherm()
    else:
        messagebox.showerror("Fout", "Onjuiste gebruikersnaam of wachtwoord.")



        def login_scherm():
    # Vernietig bestaande vensters
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Inloggen")

    tk.Label(root, text="Gebruikersnaam").grid(row=0, column=0, padx=5, pady=5)
    global gebruikersnaam_entry
    gebruikersnaam_entry = tk.Entry(root)
    gebruikersnaam_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(root, text="Wachtwoord").grid(row=1, column=0, padx=5, pady=5)
    global wachtwoord_entry
    wachtwoord_entry = tk.Entry(root, show="*")
    wachtwoord_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Button(root, text="Inloggen", command=inloggen).grid(row=2, column=0, padx=5, pady=10)
    tk.Button(root, text="Registreren", command=registreer_scherm).grid(row=2, column=1, padx=5, pady=10)


# Functie om kledingstukken toe te voegen aan de database
def voeg_kledingstuk_toe():
    merk = merk_combobox.get().strip()
    type_kleding = type_combobox.get().strip()
    maat = maat_combobox.get().strip()
    hoeveelheid = hoeveelheid_combobox.get().strip()

    if not merk or not type_kleding or not maat or not hoeveelheid:
        messagebox.showerror("Fout", "Alle velden zijn verplicht!")
        return

    try:
        c.execute("INSERT INTO kledingstukken (merk, type, maat, hoeveelheid) VALUES (?, ?, ?, ?)",
                  (merk, type_kleding, maat, int(hoeveelheid)))
        conn.commit()
        messagebox.showinfo("Succes", "Kledingstuk toegevoegd aan voorraad.")
        update_lijstbox()
    except Exception as e:
        messagebox.showerror("Fout", f"Er is een fout opgetreden: {e}")

# Functie om een kledingstuk te verwijderen
def verwijder_kledingstuk():
    try:
        geselecteerd_item = lijstbox.get(lijstbox.curselection())
        kleding_id = geselecteerd_item.split(" - ")[0]
        c.execute("DELETE FROM kledingstukken WHERE id = ?", (kleding_id,))
        conn.commit()
        messagebox.showinfo("Succes", "Kledingstuk verwijderd.")
        update_lijstbox()
    except Exception as e:
        messagebox.showerror("Fout", f"Selecteer een item om te verwijderen! Fout: {e}")

# Functie om de lijstbox te updaten
def update_lijstbox():
    lijstbox.delete(0, tk.END)
    for row in c.execute("SELECT id, merk, type, maat, hoeveelheid FROM kledingstukken"):
        lijstbox.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]}")

# Functie om merken te scrapen
def scrape_merken_van_wikipedia():
    try:
        response = requests.get("https://nl.wikipedia.org/wiki/Lijst_van_kledingmerken")
        soup = BeautifulSoup(response.content, "html.parser")
        merken = [li.text.strip() for li in soup.select("ul li a") if li.text.strip()]
        merk_combobox['values'] = merken
        messagebox.showinfo("Succes", "Merken succesvol gescraped!")
    except Exception as e:
        messagebox.showerror("Fout", f"Er is een fout opgetreden bij het scrapen: {e}")

# Functie om het hoofdscherm (voorraadbeheer) weer te geven
def hoofdscherm():
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Kledingwinkel Voorraadbeheer")
    root.geometry('800x600')

    tk.Label(root, text="Merk").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    global merk_combobox
    merk_combobox = ttk.Combobox(root)
    merk_combobox.grid(row=0, column=1, sticky="ew", padx=5)

    scrape_knop = tk.Button(root, text="Scrape Merken van Wikipedia", command=scrape_merken_van_wikipedia)
    scrape_knop.grid(row=0, column=2, sticky="ew", padx=5)

    tk.Label(root, text="Type").grid(row=1, column=0, sticky="w", padx=5)
    global type_combobox
    type_combobox = ttk.Combobox(root, values=["Shirt", "Sweater", "Jas", "Broek", "Trui", "Vest"])
    type_combobox.grid(row=1, column=1, sticky="ew", padx=5)

    tk.Label(root, text="Maat").grid(row=2, column=0, sticky="w", padx=5)
    global maat_combobox
    maat_combobox = ttk.Combobox(root, values=["XS", "S", "M", "L", "XL", "XXL"])
    maat_combobox.grid(row=2, column=1, sticky="ew", padx=5)

    tk.Label(root, text="Hoeveelheid").grid(row=3, column=0, sticky="w", padx=5)
    global hoeveelheid_combobox
    hoeveelheid_combobox = ttk.Combobox(root, values=[str(i) for i in range(1, 11)])
    hoeveelheid_combobox.grid(row=3, column=1, sticky="ew", padx=5)

    tk.Button(root, text="Voeg Kledingstuk Toe", command=voeg_kledingstuk_toe).grid(row=4, column=0, columnspan=3, pady=10, sticky="ew", padx=5)
    tk.Button(root, text="Verwijder Geselecteerd Kledingstuk", command=verwijder_kledingstuk).grid(row=5, column=0, columnspan=3, pady=10, sticky="ew", padx=5)

    global lijstbox
    lijstbox = tk.Listbox(root, width=60)
    lijstbox.grid(row=6, column=0, columnspan=3, pady=10, sticky="nsew", padx=5)

    update_lijstbox()

# Start het login scherm
root = tk.Tk()
login_scherm()
root.mainloop()
