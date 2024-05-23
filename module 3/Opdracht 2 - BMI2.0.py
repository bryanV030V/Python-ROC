# Get user input for height and weight
height = float(input("Enter your height in meters: "))
weight = float(input("Enter your weight in kilograms: "))

# Calculate BMI
bmi = weight / (height ** 2)

# Display the calculated BMI
print("Your BMI is:", round(bmi, 2))
