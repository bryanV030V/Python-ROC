# List of student heights
student_heights = []

# Number of students
num_students = int(input("Hoeveel studenten zijn er? "))

# Input student heights
for i in range(num_students):
    height = int(input(f"Voer de lengte in van student {i+1}: "))
    student_heights.append(height)

# Calculate the total height
total_height = 0
for height in student_heights:
    total_height += height

# Calculate the average height
average_height = total_height / num_students

# Round the average height to the nearest whole number
rounded_average_height = round(average_height)

print(f"De gemiddelde lengte van de studenten is: {rounded_average_height} cm.")
