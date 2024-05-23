print("Welcome to Python Pizza Deliveries!")

# Get user input
size = input("What size pizza do you want? S, M, or L ").lower()
add_pepperoni = input("Do you want pepperoni? Y or N ").lower()
extra_cheese = input("Do you want extra cheese? Y or N ").lower()

# Set prices
small_pizza_price = 15
medium_pizza_price = 20
large_pizza_price = 25
pepperoni_price = 2
extra_cheese_price = 1

# Calculate base price
if size == 's':
    total_price = small_pizza_price
elif size == 'm':
    total_price = medium_pizza_price
elif size == 'l':
    total_price = large_pizza_price
else:
    print("Invalid pizza size.")
    exit()

# Add pepperoni price
if add_pepperoni == 'y':
    if size == 's':
        total_price += pepperoni_price
    else:
        total_price += 3

# Add extra cheese price
if extra_cheese == 'y':
    total_price += extra_cheese_price

# Display final bill
print(f"Your final bill is: ${total_price}")


