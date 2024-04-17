# # Importing necessary modules for HTML generation
# from flask import Flask, render_template, request

# app = Flask(__name__)

# # Initialize game variables
# arr = [[0 for _ in range(10)] for _ in range(10)]

# # Function to check if placing a ship is possible
# def Putable(row, col, dir, length):
#     if dir == "竖":
#         if row + length > 10:
#             return False
#         for i in range(row, row + length):
#             if arr[i][col] != 0:
#                 return False
#         return True

#     if dir == "横":
#         if col + length > 10:
#             return False
#         for i in range(col, col + length):
#             if arr[row][i] != 0:
#                 return False
#         return True

# # Function to place a ship on the board
# def place_ship(row, col, dir, length):
#     if Putable(row, col, dir, length):
#         if dir == "竖":
#             for i in range(row, row + length):
#                 arr[i][col] = "H"
#         if dir == "横":
#             for i in range(col, col + length):
#                 arr[row][i] = "H"

# # Function to place a miss on the board
# def place_miss(row, col):
#     arr[row][col] = "M"

# # Function to generate a probability map
# def prob_map(length):
#     map1 = [[0 for _ in range(10)] for _ in range(10)]
#     for i in range(10):
#         for j in range(10):
#             if Putable(i, j, "横", length):
#                 for k in range(length):
#                     map1[i][j + k] += 1
#             if Putable(i, j, "竖", length):
#                 for k in range(length):
#                     map1[i + k][j] += 1
#     return map1

# # Function to find the maximum number in the probability map
# def max_num(map):
#     max_num = 0
#     x, y = 0, 0
#     for i in range(10):
#         for j in range(10):
#             if map[i][j] > max_num:
#                 max_num = map[i][j]
#                 x, y = j + 1, i + 1
#     return x, y

# # Route for the main page
# @app.route('/', methods=['GET', 'POST'])
# def game():
#     if request.method == 'POST':
#         if 'comp_length' in request.form:
#             # Special case: Find provable hit
#             length = int(request.form['comp_length'])
#             prob_map1 = prob_map(length)
#             x, y = max_num(prob_map1)
#             return render_template('index.html', arr=arr, max_x=x, max_y=y)
#         else:
#             # Regular case: Player's turn
#             userx = int(request.form['x'])
#             usery = int(request.form['y'])
#             direction = request.form['direction']
#             length = int(request.form['length'])

#             # Place ship or miss based on user input
#             if direction == "横":
#                 place_ship(usery - 1, userx - 1, direction, length)
#             elif direction == "竖":
#                 place_ship(usery - 1, userx - 1, direction, length)
#             else:
#                 place_miss(usery - 1, userx - 1)

#     return render_template('index.html', arr=arr, max_x=None, max_y=None)

# # Route to stop the game
# @app.route('/stop', methods=['POST'])
# def stop_game():
#     # Perform any necessary cleanup or actions to stop the game
#     return "Game stopped."

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request

app = Flask(__name__)

# Initialize game variables
arr = [[0 for _ in range(10)] for _ in range(10)]

# Function to check if placing a ship is possible
def Putable(row, col, dir, length):
    if dir == "竖":
        if row + length > 10:
            return False
        for i in range(row, row + length):
            if arr[i][col] != 0:
                return False
        return True

    if dir == "横":
        if col + length > 10:
            return False
        for i in range(col, col + length):
            if arr[row][i] != 0:
                return False
        return True

# Function to place a ship on the board
def place_ship(row, col, dir, length):
    if Putable(row, col, dir, length):
        if dir == "竖":
            for i in range(row, row + length):
                arr[i][col] = "H"
        if dir == "横":
            for i in range(col, col + length):
                arr[row][i] = "H"

# Function to place a miss on the board
def place_miss(row, col):
    arr[row][col] = "M"

# Function to generate a probability map
def prob_map(length):
    map1 = [[0 for _ in range(10)] for _ in range(10)]
    for i in range(10):
        for j in range(10):
            if Putable(i, j, "横", length):
                for k in range(length):
                    map1[i][j + k] += 1
            if Putable(i, j, "竖", length):
                for k in range(length):
                    map1[i + k][j] += 1
    return map1

# Function to find the maximum number in the probability map
def max_num(map):
    max_num = 0
    x, y = 0, 0
    for i in range(10):
        for j in range(10):
            if map[i][j] > max_num:
                max_num = map[i][j]
                x, y = j + 1, i + 1
    return x, y

@app.route('/', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        if 'comp_length' in request.form:
            # Special case: Find provable hit
            length = int(request.form['comp_length'])
            prob_map1 = prob_map(length)
            x, y = max_num(prob_map1)
            return render_template('index.html', arr=arr, max_x=x, max_y=y,prob_map1=prob_map1)
        else:
            # Regular case: Player's turn
            userx = int(request.form['x'])
            usery = int(request.form['y'])
            direction = request.form['direction']
            length = int(request.form['length'])

            # Place ship or miss based on user input
            if direction == "横":
                place_ship(usery - 1, userx - 1, direction, length)
            elif direction == "竖":
                place_ship(usery - 1, userx - 1, direction, length)
            else:
                place_miss(usery - 1, userx - 1)

    return render_template('index.html', arr=arr, max_x=None, max_y=None)

# Route to stop the game
@app.route('/stop', methods=['POST'])
def stop_game():
    # Perform any necessary cleanup or actions to stop the game
    return "Game stopped."

if __name__ == '__main__':
    app.run(debug=True)

