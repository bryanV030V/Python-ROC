import random

def toss_coin():
    # Genereer een willekeurig getal: 0 of 1
    result = random.randint(0, 1)
    
    # Als resultaat gelijk is aan 0, is het munt, anders is het kop
    if result == 0:
        return "munt"
    else:
        return "kop"

# Test de functie
print("Het resultaat van het munt opgooien is:", toss_coin())
