# 🚨 Don't change the code below 👇
two_digit_number = int(input("Type a two digit number: "))

# 🚨 Don't change the code above 👆

####################################
#Write your code below this line 👇
def ontbind_twee_cijferig_getal(two_digit_number):
    eerste_cijfer = two_digit_number // 10
    tweede_cijfer = two_digit_number % 10
    return eerste_cijfer, tweede_cijfer

def main():
    
    if two_digit_number >= 10 and two_digit_number <= 99:
        eerste_cijfer, tweede_cijfer = ontbind_twee_cijferig_getal(two_digit_number)
        print(f"Het eerste cijfer is: {eerste_cijfer} Het Tweede cijfer is: {tweede_cijfer}")
        print(f"Getal 1 en 2 bij elkaar is {eerste_cijfer + tweede_cijfer}") 
       
    else:
        print("Het ingevoerde getal is geen 2-cijferig getal.")
     
if __name__ == "__main__":
    main()

