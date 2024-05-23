import random

# Plaatjes van de handen
rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

hands = [rock, paper, scissors]

while True:
    # Gebruiker kiest
    user_choice = int(input("Wat kies je? Type 0 voor Rock, 1 voor Paper, of 2 voor Scissors. Of typ 3 om te stoppen.\n"))

    # Controleer gebruikersinvoer
    if user_choice == 3:
        print("Bedankt voor het spelen! Tot de volgende keer.")
        break
    elif user_choice >= 3 or user_choice < 0:
        print("Ongeldige invoer. Probeer opnieuw.")
        continue

    print("Jouw keuze:")
    print(hands[user_choice])

    # Computer kiest
    computer_choice = random.randint(0, 2)
    print("Computers keuze:")
    print(hands[computer_choice])

    # Bepaal de winnaar
    if user_choice == computer_choice:
        print("Gelijkspel!")
    elif (user_choice == 0 and computer_choice == 2) or (user_choice == 1 and computer_choice == 0) or (user_choice == 2 and computer_choice == 1):
        print("Je wint!")
    else:
        print("Je verliest!")
