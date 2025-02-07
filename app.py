from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# In-memory storage for users
users = {}
next_user_id = 1  # Used to generate unique user IDs

def get_next_user_id():
    """Generate the next unique user ID."""
    global next_user_id
    current_id = next_user_id
    next_user_id += 1
    return str(current_id)

# -------------------------------------
# Home Endpoint
# -------------------------------------
@app.route('/')
def home():
    return "Welcome to the Banking Platform - User Management API!"

# -------------------------------------
# Endpoint: List All Users
# -------------------------------------
@app.route('/usermanagement/users', methods=['GET'])
def list_users():
    """
    Returns a list of all registered users.
    """
    return jsonify(list(users.values())), 200

# -------------------------------------
# Endpoint: Retrieve User by ID
# -------------------------------------
@app.route('/usermanagement/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieve a user's details by their user_id.
    """
    if user_id not in users:
        abort(404, description="User not found.")
    return jsonify(users[user_id]), 200

# -------------------------------------
# Endpoint: Create (Register) a New User
# -------------------------------------
@app.route('/usermanagement/users', methods=['POST'])
def create_user():
    """
    Create a new user. Expected JSON payload:
    {
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe"  # Optional
    }
    """
    if not request.is_json:
        abort(400, description="Request must be JSON.")

    data = request.get_json()
    required_fields = ['username', 'email']
    if not all(field in data for field in required_fields):
        abort(400, description=f"Missing required fields: {', '.join(required_fields)}")

    # Generate a unique user ID
    user_id = get_next_user_id()
    user = {
        "id": user_id,
        "username": data['username'],
        "email": data['email'],
        "full_name": data.get('full_name', '')
    }
    users[user_id] = user
    return jsonify(user), 201

# -------------------------------------
# Endpoint: Update an Existing User
# -------------------------------------
@app.route('/usermanagement/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update an existing user's information.
    Accepts a JSON payload with any of the following fields: 'username', 'email', 'full_name'
    """
    if user_id not in users:
        abort(404, description="User not found.")

    if not request.is_json:
        abort(400, description="Request must be JSON.")

    data = request.get_json()
    user = users[user_id]
    if 'username' in data:
        user['username'] = data['username']
    if 'email' in data:
        user['email'] = data['email']
    if 'full_name' in data:
        user['full_name'] = data['full_name']

    users[user_id] = user
    return jsonify(user), 200

# -------------------------------------
# Endpoint: Delete a User
# -------------------------------------
@app.route('/usermanagement/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Delete a user by their user_id.
    """
    if user_id not in users:
        abort(404, description="User not found.")
    deleted_user = users.pop(user_id)
    return jsonify({"message": f"User {user_id} has been deleted.", "user": deleted_user}), 200

# -------------------------------------
# Run the Flask App
# -------------------------------------
if __name__ == '__main__':
    # Make the server externally visible and run on port 5000.
    app.run(host='0.0.0.0', port=5000, debug=True)
