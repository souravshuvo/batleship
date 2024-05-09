from flask import Flask, render_template, request, redirect,jsonify,send_file
from datetime import datetime
import os
import requests

app = Flask(__name__)

# Get the directory of the current Python script
current_dir = os.path.dirname(__file__)

# Construct the full path to the PDF file
pdf_path = os.path.join(current_dir, 'static', 'instruction.pdf')

LIKE_API_URL = "https://grozziieget.zjweiting.com:3091/Review-0.0.1-SNAPSHOT/like"
COMMENT_API_URL = "https://grozziieget.zjweiting.com:3091/Review-0.0.1-SNAPSHOT/details"
visitor_API_URL = "https://grozziieget.zjweiting.com:3091/Review-0.0.1-SNAPSHOT/like/visitors"

# Initialize game variables
arr = [[0 for _ in range(10)] for _ in range(10)]
# Initialize comment, like, and dislike dictionaries
comments = []
likes = 0
dislikes = 0
access=0


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
    if request.method == 'GET':
        global likes
        global dislikes
        global comments
        global access
        # Fetch initial like and dislike counts from API
        initial_likes = fetch_likes_from_api()
        likes = initial_likes
        initial_dislikes = fetch_dislikes_from_api()
        dislikes=initial_dislikes
        access= increse_visitor_from_api()
        # Fetch initial comments from API
        initial_comments = fetch_comments_from_api()
        comments=initial_comments

        # Reset game state when first accessing the page
        reset_game()  
        return render_template('index.html', arr=arr, max_x=None, max_y=None, likes=initial_likes, dislikes=initial_dislikes, comments=initial_comments,access=access)
    
    if request.method == 'POST':
        if 'comp_length' in request.form:
            # Special case: Find provable hit
            length = int(request.form['comp_length'])
            prob_map1 = prob_map(length)
            x, y = max_num(prob_map1)
            return render_template('index.html', arr=arr, max_x=x, max_y=y, prob_map1=prob_map1, comments=comments, likes=likes, dislikes=dislikes,access=access)
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

    return render_template('index.html', arr=arr, max_x=None, max_y=None, comments=comments, likes=likes, dislikes=dislikes,access=access)

# Function to add a comment with timestamp
def add_comment(comment):
    global comments
    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")  # Get current timestamp
    comments.append((comment, timestamp))  # Append comment with timestamp tuple to comments list


@app.route('/comment', methods=['POST'])
def add_comment_route():
    try:
        data = request.json
        comment = data['comment']
        timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        data = {
            "review": comment,
            "localDateTime": timestamp,
        }
        response = requests.post(COMMENT_API_URL, json=data)
        if response.status_code == 200:
            # Update the global comments variable
            add_comment(comment)
            # Fetch updated comments from the API
            updated_comments = fetch_comments_from_api()
            # Return updated comments along with success message and timestamp
            return jsonify({'success': True, 'comments': updated_comments, 'timestamp': timestamp})
        else:
            return jsonify({'success': False, 'message': 'Failed to add comment'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
# Helper function to fetch initial like count from API
def fetch_likes_from_api():
    # Make GET request to API endpoint to fetch like count
    response = requests.get(LIKE_API_URL)
    if response.status_code == 200:
        # Parse response and return like count
        return response.json().get('alike', 0)
    else:
        # Handle error, return default value
        return 0

# Helper function to fetch initial dislike count from API
def fetch_dislikes_from_api():
    # Make GET request to API endpoint to fetch dislike count
    response = requests.get(LIKE_API_URL)
    if response.status_code == 200:
        # Parse response and return dislike count
        return response.json().get('aunlike', 0)
    else:
        # Handle error, return default value
        return 0

# Helper function to fetch initial comments from API
def fetch_comments_from_api():
    # Make GET request to API endpoint to fetch comments
    response = requests.get(COMMENT_API_URL)
    if response.status_code == 200:
        # Parse response and return comments
        data = response.json()
        return data  # Assuming comments are directly returned as a list
    else:
        # Handle error, return empty list
        return []
    
    
def increse_visitor_from_api():
    # Make GET request to API endpoint to fetch like count
    response = requests.put(visitor_API_URL)
    if response.status_code == 200:
        # Parse response and return like count
        return response.json().get('visitors', 0)
    else:
        # Handle error, return default value
        return 0

@app.route('/like', methods=['POST'])
def like():
    try:
        global likes
        data = {
            "alike": likes + 1,
        }
        response = requests.post(LIKE_API_URL, json=data)
        if response.status_code == 200:
            likes += 1
            return jsonify({"success": True, "message": "Like successful"})
        else:
            return jsonify({"success": False, "message": "Failed to like"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/dislike', methods=['POST'])
def dislike():
    try:
        global dislikes
        data = {
            "aunlike": dislikes + 1,
        }
        response = requests.post(LIKE_API_URL, json=data)
        if response.status_code == 200:
            dislikes += 1
            return jsonify({"success": True, "message": " successful"})
        else:
            return jsonify({"success": False, "message": "Failed"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    



# Function to reset game state
def reset_game():
    global arr
    arr = [[0 for _ in range(10)] for _ in range(10)]
    return redirect('/')


@app.route('/show', methods=['POST'])
def show_instructions():
    # Construct the full path to the PDF file
    current_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(current_dir, 'static', 'instruction.pdf')

    # Return the PDF file as an attachment
    return send_file(pdf_path, as_attachment=False)

@app.route('/stop', methods=['POST'])
def stop_game():
    return reset_game()

if __name__ == '__main__':
    app.run(debug=True)



