import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# Database setup
def create_db():
    conn = sqlite3.connect('kledingwinkel.db')
    c = conn.cursor()
    # Create tables for products and users
    c.execute('''CREATE TABLE IF NOT EXISTS gebruikers (
                id INTEGER PRIMARY KEY,
                gebruikersnaam TEXT NOT NULL,
                wachtwoord TEXT NOT NULL
            )''')
    c.execute('''CREATE TABLE IF NOT EXISTS kledingstukken
                 (id INTEGER PRIMARY KEY, merk TEXT, type TEXT, maat TEXT, hoeveelheid INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS gebruikers
                 (id INTEGER PRIMARY KEY, gebruikersnaam TEXT NOT NULL, wachtwoord TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Add a new user (for testing purposes or initial setup)
def add_user(gebruikersnaam, wachtwoord):
    conn = sqlite3.connect('kledingwinkel.db')
    c = conn.cursor()
    c.execute("INSERT INTO gebruikers (gebruikersnaam, wachtwoord) VALUES (?, ?)", (gebruikersnaam, wachtwoord))
    conn.commit()
    conn.close()

# Login function
def login(gebruikersnaam, wachtwoord):
    conn = sqlite3.connect('kledingwinkel.db')
    c = conn.cursor()
    try:
        # Query the database for the user
        c.execute("SELECT * FROM gebruikers WHERE gebruikersnaam = ? AND wachtwoord = ?", (gebruikersnaam, wachtwoord))
        user = c.fetchone()
        if user:
            messagebox.showinfo("Succes", f"Welkom, {gebruikersnaam}!")
            app = Application()  # Launch the main application after successful login
            app.mainloop()
        else:
            messagebox.showerror("Fout", "Onjuiste gebruikersnaam of wachtwoord.")
    except sqlite3.OperationalError as e:
        messagebox.showerror("Database Fout", f"Er is een fout opgetreden: {e}")
    finally:
        conn.close()

# GUI setup for Login
def setup_login_gui():
    def handle_login():
        gebruikersnaam = username_entry.get()
        wachtwoord = password_entry.get()
        login(gebruikersnaam, wachtwoord)

    root = tk.Tk()
    root.title("Login Scherm")
    root.geometry("300x200")

    # Labels and entry fields for login
    tk.Label(root, text="Gebruikersnaam:").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Wachtwoord:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    # Login button
    login_button = tk.Button(root, text="Login", command=handle_login)
    login_button.pack(pady=10)

    root.mainloop()

# Add a new product to the database
def add_product(merk, type, maat, hoeveelheid):
    conn = sqlite3.connect('kledingwinkel.db')
    c = conn.cursor()
    c.execute('''INSERT INTO kledingstukken (merk, type, maat, hoeveelheid)
                 VALUES (?, ?, ?, ?)''', (merk, type, maat, hoeveelheid))
    conn.commit()
    conn.close()

# Function to filter products based on criteria
def filter_products(merk=None, type=None, maat=None):
    conn = sqlite3.connect('kledingwinkel.db')
    c = conn.cursor()
    query = "SELECT * FROM kledingstukken WHERE 1=1"
    params = []
    
    if merk:
        query += " AND merk = ?"
        params.append(merk)
    if type:
        query += " AND type = ?"
        params.append(type)
    if maat:
        query += " AND maat = ?"
        params.append(maat)
    
    c.execute(query, tuple(params))
    products = c.fetchall()
    conn.close()
    return products

# Export data to Excel
def export_to_excel():
    conn = sqlite3.connect('kledingwinkel.db')
    c = conn.cursor()
    c.execute("SELECT * FROM kledingstukken")
    data = c.fetchall()
    conn.close()
    
    df = pd.DataFrame(data, columns=["ID", "Merk", "Type", "Maat", "Hoeveelheid"])
    df.to_excel("kledingvoorraad.xlsx", index=False)
    messagebox.showinfo("Exporteren", "De voorraad is geëxporteerd naar Excel!")

# Export data to SQL backup
def export_to_sql():
    conn = sqlite3.connect('kledingwinkel.db')
    with open('kledingwinkel_dump.sql', 'w') as f:
        for line in conn.iterdump():
            f.write(f'{line}\n')
    messagebox.showinfo("Exporteren", "De database is geëxporteerd naar SQL!")

# Web scraping function to get brand names from Wikipedia
def scrape_brands():
    url = "https://en.wikipedia.org/wiki/List_of_clothing_brands"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    brands = []
    
    for item in soup.find_all('li'):
        brand = item.get_text()
        if 'brand' in brand.lower():
            brands.append(brand)
    
    return brands

# GUI using Tkinter
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Voorraadbeheer Kledingwinkel")
        self.geometry("500x400")
        
        # Widgets for adding products
        self.merk_label = tk.Label(self, text="Merk:")
        self.merk_label.grid(row=0, column=0)
        self.merk_entry = tk.Entry(self)
        self.merk_entry.grid(row=0, column=1)

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

        self.add_button = tk.Button(self, text="Voeg Product Toe", command=self.add_product)
        self.add_button.grid(row=4, column=0, columnspan=2)

        # Buttons for export
        self.export_excel_button = tk.Button(self, text="Exporteer naar Excel", command=export_to_excel)
        self.export_excel_button.grid(row=5, column=0, columnspan=2)

        self.export_sql_button = tk.Button(self, text="Exporteer naar SQL", command=export_to_sql)
        self.export_sql_button.grid(row=6, column=0, columnspan=2)
        
        # Display filtered products
        self.filter_button = tk.Button(self, text="Filter Producten", command=self.filter_products)
        self.filter_button.grid(row=7, column=0, columnspan=2)
        
        # Dropdown for brands (from Wikipedia)
        self.scrape_brands = tk.Button(self, text="Scrape van wikipedia", command=self.scrape_brands)
        self.scrape_brands.grid(row=9, column=0, columnspan=2)

        self.brand_label = tk.Label(self, text="Merk (van Wikipedia):")
        self.brand_label.grid(row=8, column=0)
        self.brand_dropdown = ttk.Combobox(self)
        self.brand_dropdown.grid(row=8, column=1)
        self.brand_dropdown['values'] = scrape_brands()  # Fetch and set brand names
        self.scrape_brands = tk.Button(self, text="Scrape van wikipedia", command=self.scrape_brands)
        self.scrape_brands.grid(row=10, column=4, columnspan=2)
        
    def add_product(self):
        merk = self.merk_entry.get()
        type = self.type_entry.get()
        maat = self.maat_entry.get()
        try:
            hoeveelheid = int(self.hoeveelheid_entry.get())
            add_product(merk, type, maat, hoeveelheid)
            messagebox.showinfo("Succes", "Product succesvol toegevoegd!")
        except ValueError:
            messagebox.showerror("Fout", "Voer een geldig aantal in voor hoeveelheid.")

    def filter_products(self):
        merk = self.merk_entry.get()
        type = self.type_entry.get()
        maat = self.maat_entry.get()
        
        filtered_products = filter_products(merk, type, maat)
        
        if filtered_products:
            result_str = "\n".join([f"{prod[1]} - {prod[2]} - {prod[3]} - {prod[4]}" for prod in filtered_products])
            messagebox.showinfo("Gefilterde Producten", result_str)
        else:
            messagebox.showinfo("Geen Resultaten", "Geen producten gevonden voor de opgegeven filters.")

# Main Program
if __name__ == "__main__":
    create_db()
    # Uncomment the line below to add a test user (run only once)
    add_user("admin", "admin123")
    setup_login_gui()
