# Stel een correct wachtwoord in
correct_password = "kaas"

# Start een while loop
while True:
    # Vraag de gebruiker om een wachtwoord in te voeren
    ingevoerd_wachtwoord = input("Voer het wachtwoord in: ")

    # Controleer of het wachtwoord correct is
    if ingevoerd_wachtwoord == correct_password:
        print("Correct wachtwoord ingevoerd. Toegang verleend.")
        break  # Verlaat de loop als het wachtwoord correct is
    else:
        print("Onjuist wachtwoord. Probeer opnieuw.")
