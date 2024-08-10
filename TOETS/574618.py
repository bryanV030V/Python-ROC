import random

print("Python Perioden toets.")
print("20-06-2024 NEISD4RO21F 574618 Bryan Van 't Veld.")
print("__________________________________________________")

# Take input from the user
input_string = input("type de Prijzen in met een komma: ")
numbers = input_string.split(', ')
number_list = [int(number.strip()) for number in numbers]
print(f"Prijzen zoals opgegeven: {numbers}")

last_elem = number_list.pop()

number_list.sort(reverse=True)
print(f"{number_list} Dit is de prijs lijst van groot naar klein.")


average = sum(number_list) / len(number_list)
print(f"De gemiddelde prijs is: {average:.2f}")

print(f"{last_elem} is het laatst ingevulde getal")




