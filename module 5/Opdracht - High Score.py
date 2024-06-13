# 🚨 Don't change the code below 👇
student_scores = [78, 65, 89, 86, 55, 91, 64, 89]
# 🚨 Don't change the code above 👆

# Write your code below this row 👇

def get_highest_score(scores):
    highest_score = scores[0]
    for score in scores:
        if score > highest_score:
            highest_score = score
    return highest_score

def get_average_score(scores):
    total_score = 0
    for score in scores:
        total_score += score
    average_score = total_score / len(scores)
    return average_score

highest_score = get_highest_score(student_scores)
average_score = get_average_score(student_scores)

print(f"The highest score in the class is: {highest_score}")
print(f"The average score in the class is: {average_score}")
