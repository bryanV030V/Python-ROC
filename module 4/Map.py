# Initial map
map = [['⬜️', '⬜️', '⬜️'],
       ['⬜️', '⬜️', '⬜️'],
       ['⬜️', '⬜️', '⬜️']]

# Function to print the map
def print_map():
    for row in map:
        print(" ".join(row))

# Function to mark a spot on the map
def mark_spot(position):
    column = int(position[0]) - 1
    row = int(position[1]) - 1
    map[row][column] = 'X'

# User input for position
position = input("Enter the column and row number (e.g., 23 for column 2, row 3): ")

# Mark the spot on the map
mark_spot(position)

# Print the updated map
print_map()
