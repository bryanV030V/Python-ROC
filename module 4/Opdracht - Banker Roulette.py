import random

# Input the names separated by comma and space
names_string = input("Enter the names separated by comma and space: ")

# Split the input string into individual names
names = names_string.split(", ")

# Count the number of names
num_names = len(names)

# Generate a random index within the range of number of names
random_index = random.randint(0, num_names - 1)

# Select the random name using the random index
selected_name = names[random_index]

print("The person selected to pay for everybody's food bill is:", selected_name)
