import random

# Genereer een random nummer tussen 0 en 100
random_number = random.randint(0, 100)
print("Ik heb een nummer tussen 0 en 100 gekozen. Probeer het te raden!")

# Start een while loop die blijft draaien totdat het juiste nummer is geraden
while True:
    # Vraag de gebruiker om een nummer in te voeren
    try:
        geraden_nummer = int(input("Voer je geraden nummer in: "))
        
        # Controleer of het geraden nummer correct is
        if geraden_nummer < random_number:
            print("Het getal is te laag. Probeer het opnieuw.")
        elif geraden_nummer > random_number:
            print("Het getal is te hoog. Probeer het opnieuw.")
        else:
            print("Gefeliciteerd! Je hebt het nummer geraden:", random_number)
            break  # Verlaat de loop als het juiste nummer is geraden
    except ValueError:
        print("Voer alstublieft een geldig nummer in.")
