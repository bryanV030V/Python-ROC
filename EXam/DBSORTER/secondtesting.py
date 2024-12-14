import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import requests
from bs4 import BeautifulSoup
import pandas as pd  # Voor het exporteren naar Excel
import threading
import bcrypt  # Secure password hashing

# Thread lock for SQLite
db_lock = threading.Lock()

# Singleton connection
def get_db_connection():
    if not hasattr(get_db_connection, "connection"):
        get_db_connection.connection = sqlite3.connect('kledingwinkel.db', check_same_thread=False)
    return get_db_connection.connection

# Initialize Database
def create_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS gebruikers (
                id INTEGER PRIMARY KEY,
                gebruikersnaam TEXT NOT NULL,
                wachtwoord TEXT NOT NULL
            )''')
    c.execute('''CREATE TABLE IF NOT EXISTS kledingstukken (
                id INTEGER PRIMARY KEY,
                merk TEXT,
                type TEXT,
                maat TEXT,
                hoeveelheid INTEGER)''')
    conn.commit()

# Add a user
# Add a user without encryption
def add_user(gebruikersnaam, wachtwoord):
    conn = get_db_connection()
    with db_lock:
        c = conn.cursor()
        c.execute("INSERT INTO gebruikers (gebruikersnaam, wachtwoord) VALUES (?, ?)", (gebruikersnaam, wachtwoord))
        conn.commit()

# Login function
# Login function without encryption
def login(gebruikersnaam, wachtwoord):
    conn = get_db_connection()
    with db_lock:
        c = conn.cursor()
        c.execute("SELECT wachtwoord FROM gebruikers WHERE gebruikersnaam = ?", (gebruikersnaam,))
        user = c.fetchone()
        if user and wachtwoord == user[0]:  # Plaintext password comparison
            messagebox.showinfo("Succes", f"Welkom, {gebruikersnaam}!")
        else:
            messagebox.showerror("Fout", "Onjuiste gebruikersnaam of wachtwoord.")

# Functions from DBSorter
conn = sqlite3.connect('kledingwinkel.db')
c = conn.cursor()

# Create the clothing table if it doesn't exist
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

# Function to add or update clothing item
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
    merk_combobox.set('')
    type_combobox.set('')
    maat_combobox.set('')
    hoeveelheid_combobox.set('')
    update_lijst()

# Function to delete clothing item
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

# Function to update the clothing list in the UI
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

# Function to export to Excel
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

# Function to scrape brands from Wikipedia
def scrape_merken_van_wikipedia():
    url = "https://nl.wikipedia.org/wiki/Categorie:Kledingmerk"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        merken = [link.text.strip() for link in soup.select(".mw-category-group ul li a")]
        
        if merken:
            merk_combobox['values'] = merken
            filter_merk_combobox['values'] = merken
            messagebox.showinfo("Succes", "Merken succesvol gescraped en toegevoegd aan de dropdown!")
        else:
            messagebox.showerror("Fout", "Geen merken gevonden op de Wikipedia-pagina.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Fout", f"Er is een fout opgetreden bij het scrapen van Wikipedia: {e}")

# UI Setup
def setup_ui():
    global root, merk_combobox, type_combobox, maat_combobox, hoeveelheid_combobox, lijstbox
    global filter_merk_combobox, filter_type_combobox, filter_maat_combobox, filter_hoeveelheid_combobox

    root = tk.Tk()
    root.title("Kledingwinkel Voorraadbeheer")
    root.geometry('800x600')
    root.resizable(True, True)

    tk.Label(root, text="Merk").grid(row=0, column=0, padx=5, pady=5)
    merk_combobox = ttk.Combobox(root)
    merk_combobox.grid (row=0, column=1, padx=5)

    tk.Label(root, text="Type").grid(row=1, column=0, padx=5, pady=5)
    type_combobox = ttk.Combobox(root, values=["Shirt", "Sweater", "Jas", "Broek", "Trui", "Vest"])
    type_combobox.grid(row=1, column=1, padx=5)

    tk.Label(root, text="Maat").grid(row=2, column=0, padx=5, pady=5)
    maat_combobox = ttk.Combobox(root, values=["XS", "S", "M", "L", "XL", "XXL"])
    maat_combobox.grid(row=2, column=1, padx=5)

    tk.Label(root, text="Hoeveelheid").grid(row=3, column=0, padx=5, pady=5)
    hoeveelheid_combobox = ttk.Combobox(root, values=[str(i) for i in range(1, 11)])
    hoeveelheid_combobox.grid(row=3, column=1, padx=5)

    voeg_toe_knop = tk.Button(root, text="Voeg Kledingstuk Toe", command=voeg_kledingstuk_toe)
    voeg_toe_knop.grid(row=4, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

    verwijder_knop = tk.Button(root, text="Verwijder Geselecteerd Kledingstuk", command=verwijder_kledingstuk)
    verwijder_knop.grid(row=5, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

    lijstbox = tk.Listbox(root, width=60)
    lijstbox.grid(row=6, column=0, columnspan=3, pady=10, padx=5, sticky="nsew")

    filter_label = tk.Label(root, text="Filters")
    filter_label.grid(row=7, column=0, padx=5, pady=5)

    tk.Label(root, text="Filter op Merk").grid(row=8, column=0, padx=5, pady=5)
    filter_merk_combobox = ttk.Combobox(root)
    filter_merk_combobox.grid(row=8, column=1, padx=5)

    tk.Label(root, text="Filter op Type").grid(row=9, column=0, padx=5, pady=5)
    filter_type_combobox = ttk.Combobox(root, values=["Shirt", "Sweater", "Jas", "Broek", "Trui", "Vest"])
    filter_type_combobox.grid(row=9, column=1, padx=5)

    tk.Label(root, text="Filter op Maat").grid(row=10, column=0, padx=5, pady=5)
    filter_maat_combobox = ttk.Combobox(root, values=["XS", "S", "M", "L", "XL", "XXL"])
    filter_maat_combobox.grid(row=10, column=1, padx=5)

    tk.Label(root, text="Filter op Hoeveelheid").grid(row=11, column=0, padx=5, pady=5)
    filter_hoeveelheid_combobox = ttk.Combobox(root, values=[str(i) for i in range(1, 11)])
    filter_hoeveelheid_combobox.grid(row=11, column=1, padx=5)

    filter_knop = tk.Button(root, text="Pas Filter Toe", command=update_lijst)
    filter_knop.grid(row=12, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

    exporteer_knop = tk.Button(root, text="Exporteer naar Excel", command=exporteer_naar_excel)
    exporteer_knop.grid(row=13, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

    scrape_knop = tk.Button(root, text="Scrape Merken van Wikipedia", command=scrape_merken_van_wikipedia)
    scrape_knop.grid(row=14, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

    root.mainloop()

# Setup Login GUI
def setup_login_gui():
    def handle_login():
        gebruikersnaam = username_entry.get()
        wachtwoord = password_entry.get()
        login(gebruikersnaam, wachtwoord)

    login_root = tk.Tk()
    login_root.title("Login Scherm")
    login_root.geometry("300x200")

    tk.Label(login_root, text="Gebruikersnaam:").pack(pady=5)
    username_entry = tk.Entry(login_root)
    username_entry.pack(pady=5)

    tk.Label(login_root, text="Wachtwoord:").pack(pady=5)
    password_entry = tk.Entry(login_root, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(login_root, text="Login", command=handle_login)
    login_button.pack(pady=10)

    login_root.mainloop()

# Main entry point
if __name__ == "__main__":
    create_db()  # Ensure database and tables exist
    add_user("admin", "admin123")  # Add a default admin user
    setup_login_gui()  # Launch login screen
