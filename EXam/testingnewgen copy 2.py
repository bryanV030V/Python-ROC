import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import threading

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
def add_user(gebruikersnaam, wachtwoord):
    conn = get_db_connection()
    with db_lock:
        c = conn.cursor()
        c.execute("INSERT INTO gebruikers (gebruikersnaam, wachtwoord) VALUES (?, ?)", (gebruikersnaam, wachtwoord))
        conn.commit()

# Login function
def login(gebruikersnaam, wachtwoord):
    conn = get_db_connection()
    with db_lock:
        c = conn.cursor()
        c.execute("SELECT * FROM gebruikers WHERE gebruikersnaam = ? AND wachtwoord = ?", (gebruikersnaam, wachtwoord))
        user = c.fetchone()
        if user:
            messagebox.showinfo("Succes", f"Welkom, {gebruikersnaam}!")
            app = Application()
            app.mainloop()
        else:
            messagebox.showerror("Fout", "Onjuiste gebruikersnaam of wachtwoord.")

# Add a product
def add_product(merk, type, maat, hoeveelheid):
    conn = get_db_connection()
    with db_lock:
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO kledingstukken (merk, type, maat, hoeveelheid)
                        VALUES (?, ?, ?, ?)''', (merk, type, maat, hoeveelheid))
            conn.commit()
            messagebox.showinfo("Succes", "Product succesvol toegevoegd!")
        except sqlite3.OperationalError as e:
            messagebox.showerror("Fout", f"Database-fout: {e}")

# Scrape brands from Wikipedia
def scrape_brands(brand_combobox):
    url = "https://nl.wikipedia.org/wiki/Categorie:Kledingmerk"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        brands = [link.text.strip() for link in soup.select(".mw-category-group ul li a")]
        if brands:
            brand_combobox['values'] = brands
            messagebox.showinfo("Succes", "Merken succesvol gescraped en toegevoegd aan de dropdown!")
        else:
            messagebox.showerror("Fout", "Geen merken gevonden op de Wikipedia-pagina.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Fout", f"Er is een fout opgetreden bij het scrapen van Wikipedia: {e}")

# Main Application Class
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Voorraadbeheer Kledingwinkel")
        self.geometry("500x400")

        # Merk Dropdown
        self.merk_label = tk.Label(self, text="Merk:")
        self.merk_label.grid(row=0, column=0)
        self.merk_combobox = ttk.Combobox(self)
        self.merk_combobox.grid(row=0, column=1)

        # Scrape Button
        self.scrape_button = tk.Button(self, text="Scrape Merken",
                                        command=lambda: threading.Thread(target=scrape_brands, args=(self.merk_combobox,)).start())
        self.scrape_button.grid(row=0, column=2)

        # Other Fields
        self.type_label = tk.Label(self, text="Type:")
        self.type_label.grid(row=1, column=0)
        self.type_entry = tk.Entry(self)
        self.type_entry.grid(row=1, column=1)

        self.maat_label = tk.Label(self, text="Maat:")
        self.maat_label.grid(row=2, column=0)
        self.maat_entry = tk.Entry(self)
        self.maat_entry.grid(row=2, column=1)

        self.hoeveelheid_label = tk.Label(self, text="Hoeveelheid:")
        self.hoeveelheid_label.grid(row=3, column=0)
        self.hoeveelheid_entry = tk.Entry(self)
        self.hoeveelheid_entry.grid(row=3, column=1)

        # Add Product Button
        self.add_button = tk.Button(self, text="Voeg Product Toe", command=self.add_product)
        self.add_button.grid(row=4, column=0, columnspan=2)

    def add_product(self):
        merk = self.merk_combobox.get()
        type = self.type_entry.get()
        maat = self.maat_entry.get()
        try:
            hoeveelheid = int(self.hoeveelheid_entry.get())
            add_product(merk, type, maat, hoeveelheid)
        except ValueError:
            messagebox.showerror("Fout", "Voer een geldig aantal in voor hoeveelheid.")

# Login GUI
def setup_login_gui():
    def handle_login():
        gebruikersnaam = username_entry.get()
        wachtwoord = password_entry.get()
        login(gebruikersnaam, wachtwoord)

    root = tk.Tk()
    root.title("Login Scherm")
    root.geometry("300x200")

    tk.Label(root, text="Gebruikersnaam:").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Wachtwoord:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    login_button = tk.Button(root, text="Login", command=handle_login)
    login_button.pack(pady=10)

    root.mainloop()

# Run Application
if __name__ == "__main__":
    create_db()
    add_user("admin", "admin123")  # Add a default admin user
    setup_login_gui()
