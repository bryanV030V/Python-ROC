# 🚨 Don't change the code below 👇
height = float(input("Enter your height in m: "))
weight = float(input("Enter your weight in kg: "))
# 🚨 Don't change the code above 👆

# Write your code below this line 👇

# Calculate BMI (Body Mass Index)
bmi = weight / (height ** 2)

# Print the calculated BMI
print("Your BMI is:", round(bmi, 2))
