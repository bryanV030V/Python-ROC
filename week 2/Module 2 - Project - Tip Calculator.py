# 1. Vraag hoe hoog de rekening was in €
# 2. Vraag vervolgens hoeveel percentage fooi jullie willen geven, kies uit 10, 12 of 15%
# 3. Vraag vervolgens met hoeveel personen de rekening betaald moet worden.
# 4. Als resultaat geef je aan hoeveel elk persoon moet betalen.


#Write your code below this line 👇

print("Welkom bij de fooi calculator!")
print("________________________________")
# Stap 1: Vraag hoe hoog de rekening was in €
rekening_bedrag = float(input("Hoe hoog was de rekening in €? "))

# Stap 2: Vraag vervolgens hoeveel percentage fooi jullie willen geven, kies uit 10, 12 of 15%
fooi_percentage = float(input("Hoeveel procent fooi willen jullie geven? (kies uit 10, 12 of 15) "))

# Stap 3: Vraag vervolgens met hoeveel personen de rekening betaald moet worden.
aantal_personen = int(input("Met hoeveel personen moet de rekening betaald worden? "))

# Bereken totale bedrag inclusief fooi
totaal_bedrag = rekening_bedrag * (1 + fooi_percentage / 100)

# Bereken bedrag per persoon
bedrag_per_persoon = totaal_bedrag / aantal_personen

# Stap 4: Als resultaat geef je aan hoeveel elk persoon moet betalen.
print(f"Elk persoon moet €{bedrag_per_persoon:.2f} betalen.")



