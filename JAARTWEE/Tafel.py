Getal = int(input("voer een getal in:"))

print(f"de tafel van het getal {Getal}:")
for i in range(1, 11):
    Resultaat = Getal * i
    print(f"{Getal} x {i} = {Resultaat}")