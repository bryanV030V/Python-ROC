#1. Zorg voor een begroeting van je script.
#2. Vraag de gebruiker om de plaats waar hij/zij is opgegroeid.
#3. Vraag de gebruiker om de naam van een huisdier.
#4. Combineer de naam van de plaats en de naam van het huisdier.
#5. Geef het resultaat als volgt weer: (voorbeeld: De naam van je band is: Nieuwegein Fluffie)
#5. Zorg ervoor dat de input telkens op een nieuwe lijn start.

print("Welkom bij het programma!")
naam = input("Wat is jouw naam? ")

print(f"Hallo, {naam}!")

plaats = input("Waar kom je vandaan? ")

huisdier = input("Heb je een huisdier? (ja/nee) ").lower()
if huisdier == "ja":
    huisdier_naam = input("Wat is de naam van je huisdier? ")
    print(f"{huisdier_naam} {plaats}!\n Dat klinkt leuk!")
else:
    print(f"Geen huisdier uit {plaats}? Dat is ook prima!")

print("Bedankt voor het gebruiken van het programma!")