from datetime import datetime

# Huidig jaar bepalen
huidig_jaar = datetime.now().year

# Lijst met primaire kleuren
primaire_kleuren = ["rood", "blauw", "geel"]

# Gegevens opvragen en opslaan in variabelen
naam = input("Wat is je naam? ")
leeftijd = int(input("Hoe oud ben je? "))
favoriete_kleur = input("Wat is je favoriete kleur? ").lower()  # Maak de invoer lowercase voor consistentie
heeft_huisdieren = input("Heb je huisdieren? (ja/nee) ").lower()

# Vragen hoeveel huisdieren, indien van toepassing
if heeft_huisdieren == "ja":
    aantal_huisdieren = int(input("Hoeveel huisdieren heb je? "))
    huisdieren_tekst = f"Je hebt {aantal_huisdieren} huisdier(en)."
else:
    aantal_huisdieren = 0
    huisdieren_tekst = "Je hebt geen huisdieren."

geboorte_maand = int(input("In welke maand ben je geboren? (nummer van de maand, 1 t/m 12) "))

# Berekenen van geboortejaar
geboortejaar = huidig_jaar - leeftijd
# Als de geboortemaand nog moet komen in het huidige jaar, dan een jaar aftrekken
if geboorte_maand > datetime.now().month:
    geboortejaar -= 1

# Checken of de opgegeven kleur een primaire kleur is
if favoriete_kleur in primaire_kleuren:
    kleur_status = f"{favoriete_kleur.capitalize()} is een primaire kleur."
else:
    kleur_status = f"{favoriete_kleur.capitalize()} is geen primaire kleur."

# Netjes de informatie weergeven in een overzichtelijke output
print("\n--- Overzicht van de ingevoerde gegevens ---")
print(f"Naam: {naam}")
print(f"Leeftijd: {leeftijd}")
print(f"Favoriete kleur: {favoriete_kleur.capitalize()} ({kleur_status})")
print(f"{huisdieren_tekst}")
print(f"Geboortemaand: {geboorte_maand}")
print(f"Je bent waarschijnlijk geboren in het jaar: {geboortejaar}")



