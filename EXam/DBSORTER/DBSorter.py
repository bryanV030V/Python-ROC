import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import pandas as pd  # Voor het exporteren naar Excel
import bcrypt  # Use bcrypt for secure password hashing



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
    merk = merk_combobox.get().strip()
    type_ = type_combobox.get().strip()
    maat = maat_combobox.get().strip()
    hoeveelheid = hoeveelheid_combobox.get().strip()

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
    merk_combobox.set('')
    type_combobox.set('')
    maat_combobox.set('')
    hoeveelheid_combobox.set('')
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

# Functie om de lijst van kledingstukken bij te werken in de UI, met filters
def update_lijst():
    lijstbox.delete(0, tk.END)
    
    query = "SELECT * FROM kledingstukken WHERE 1=1"
    params = []

    # Gebruik de filters ingevuld door de gebruiker
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

# Functie om kledingstukken naar een Excel-bestand te exporteren
def exporteer_naar_excel():
    c.execute("SELECT * FROM kledingstukken")
    kledingstukken = c.fetchall()
    
    # Controleer of er kledingstukken zijn
    if not kledingstukken:
        messagebox.showerror("Fout", "Geen kledingstukken om te exporteren.")
        return
    
    # Dataframe maken van de kledingstukken
    df = pd.DataFrame(kledingstukken, columns=['ID', 'Merk', 'Type', 'Maat', 'Hoeveelheid'])
    
    # Exporteer naar Excel-bestand
    try:
        df.to_excel('kledingvoorraad.xlsx', index=False, engine='openpyxl')
        messagebox.showinfo("Succes", "Data succesvol geëxporteerd naar kledingvoorraad.xlsx!")
    except Exception as e:
        messagebox.showerror("Fout", f"Er is een fout opgetreden bij het exporteren: {str(e)}")

# Functie om de database naar een SQL-bestand te exporteren
def exporteer_naar_sql():
    try:
        with open('kledingwinkel_dump.sql', 'w') as f:
            # Loop door alle SQL-statements om de database opnieuw te creëren
            for lijn in conn.iterdump():
                f.write(f'{lijn}\n')
        messagebox.showinfo("Succes", "Database succesvol geëxporteerd naar kledingwinkel_dump.sql!")
    except Exception as e:
        messagebox.showerror("Fout", f"Er is een fout opgetreden bij het exporteren naar SQL: {str(e)}")

# Functie om de merken van Wikipedia te scrapen
def scrape_merken_van_wikipedia():
    url = "https://nl.wikipedia.org/wiki/Categorie:Kledingmerk"  # Nederlandse versie van Wikipedia
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        merken = []
        
        # Zoek de merken op basis van de links in de categorie
        for link in soup.select(".mw-category-group ul li a"):
            merk = link.text.strip()
            merken.append(merk)
        
        if not merken:
            messagebox.showerror("Fout", "Geen merken gevonden op de Wikipedia-pagina.")
            return
        
        # Vul de dropdown (ComboBox) met de gescrapte merken
        merk_combobox['values'] = merken
        filter_merk_combobox['values'] = merken  # Update ook de filter
        messagebox.showinfo("Succes", "Merken succesvol gescraped en toegevoegd aan de dropdown!")
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Fout", f"Er is een fout opgetreden bij het scrapen van Wikipedia: {e}")

# Functie om de grootte van het venster aan te passen (schermvullend of terug naar venstergrootte)
def toggle_fullscreen(event=None):
    root.attributes('-fullscreen', not root.attributes('-fullscreen'))

# Functie om uit het volledige scherm te gaan
def end_fullscreen(event=None):
    root.attributes('-fullscreen', False)

# UI setup met tkinter
root = tk.Tk()
root.title("Kledingwinkel Voorraadbeheer")

# Zorg ervoor dat het venster kan worden aangepast
root.geometry('1920x1080')  # Startgrootte
root.resizable(True, True)  # Maak het venster resizable

# Bind de F11-toets voor het schakelen tussen volledige schermmodus
root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)

# Rest van de UI-setup blijft hetzelfde...
tk.Label(root, text="Merk").grid(row=0, column=0, sticky="w", padx=5, pady=5)
merk_combobox = ttk.Combobox(root)
merk_combobox.grid(row=0, column=1, sticky="ew", padx=5)

# Knop om merken te scrapen van Wikipedia
scrape_knop = tk.Button(root, text="Scrape Merken van Wikipedia", command=scrape_merken_van_wikipedia)
scrape_knop.grid(row=0, column=2, sticky="ew", padx=5)

# Combobox voor Type (Shirt, Sweater, Jas, etc.)
tk.Label(root, text="Type").grid(row=1, column=0, sticky="w", padx=5)
type_combobox = ttk.Combobox(root, values=["Shirt", "Sweater", "Jas", "Broek", "Trui", "Vest"])
type_combobox.grid(row=1, column=1, sticky="ew", padx=5)

# Combobox voor Maat (XS, S, M, L, XL)
tk.Label(root, text="Maat").grid(row=2, column=0, sticky="w", padx=5)
maat_combobox = ttk.Combobox(root, values=["XS", "S", "M", "L", "XL", "XXL"])
maat_combobox.grid(row=2, column=1, sticky="ew", padx=5)

# Combobox voor Hoeveelheid (1-10)
tk.Label(root, text="Hoeveelheid").grid(row=3, column=0, sticky="w", padx=5)
hoeveelheid_combobox = ttk.Combobox(root, values=[str(i) for i in range(1, 11)])
hoeveelheid_combobox.grid(row=3, column=1, sticky="ew", padx=5)

# Knop om kledingstuk toe te voegen of bij te werken
voeg_toe_knop = tk.Button(root, text="Voeg Kledingstuk Toe", command=voeg_kledingstuk_toe)
voeg_toe_knop.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew", padx=5)

# Verwijderknop
verwijder_knop = tk.Button(root, text="Verwijder Geselecteerd Kledingstuk", command=verwijder_kledingstuk)
verwijder_knop.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew", padx=5)

# Listbox voor het tonen van de kledingstukken
lijstbox = tk.Listbox(root, width=60)
lijstbox.grid(row=6, column=0, columnspan=3, pady=10, sticky="nsew", padx=5)

# Zorg ervoor dat de listbox mee resizes met het venster
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(1, weight=1)

# Filtersectie
tk.Label(root, text="Filter op Merk").grid(row=7, column=0, sticky="w", padx=5)
filter_merk_combobox = ttk.Combobox(root)
filter_merk_combobox.grid(row=7, column=1, sticky="ew", padx=5)

tk.Label(root, text="Filter op Type").grid(row=8, column=0, sticky="w", padx=5)
filter_type_combobox = ttk.Combobox(root, values=["Shirt", "Sweater", "Jas", "Broek", "Trui", "Vest"])
filter_type_combobox.grid(row=8, column=1, sticky="ew", padx=5)

tk.Label(root, text="Filter op Maat").grid(row=9, column=0, sticky="w", padx=5)
filter_maat_combobox = ttk.Combobox(root, values=["XS", "S", "M", "L", "XL", "XXL"])
filter_maat_combobox.grid(row=9, column=1, sticky="ew", padx=5)

tk.Label(root, text="Filter op Hoeveelheid").grid(row=10, column=0, sticky="w", padx=5)
filter_hoeveelheid_combobox = ttk.Combobox(root, values=[str(i) for i in range(1, 11)])
filter_hoeveelheid_combobox.grid(row=10, column=1, sticky="ew", padx=5)

# Knop om filters toe te passen
filter_knop = tk.Button(root, text="Pas Filter Toe", command=update_lijst)
filter_knop.grid(row=11, column=0, columnspan=3, pady=10, sticky="ew", padx=5)

# Knop om de data te exporteren naar een Excel-bestand
exporteer_knop = tk.Button(root, text="Exporteer naar Excel", command=exporteer_naar_excel)
exporteer_knop.grid(row=12, column=0, columnspan=3, pady=10, sticky="ew", padx=5)

# Knop om de data te exporteren naar een SQL-bestand
exporteer_sql_knop = tk.Button(root, text="Exporteer naar SQL", command=exporteer_naar_sql)
exporteer_sql_knop.grid(row=13, column=0, columnspan=3, pady=10, sticky="ew", padx=5)

# Start de lijst updaten
update_lijst()

# Start de Tkinter-applicatie
root.mainloop()

# Sluit de databaseverbinding wanneer de app wordt gesloten
conn.close()
