# 🚨 Don't change the code below 👇
year = int(input("Which year do you want to check? "))
# 🚨 Don't change the code above 👆

#Write your code below this line 👇

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def find_closest_leap_year(year):
    while True:
        year += 1
        if is_leap_year(year):
            return year

if is_leap_year(year):
    print(f"{year} is a leap year.")
else:
    closest_leap_year = find_closest_leap_year(year)
    print(f"{year} is not a leap year. The closest leap year is {closest_leap_year}.")
