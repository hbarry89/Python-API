from flask import Flask, request, jsonify
import json
import logging

app = Flask(__name__)

# Read the JSON file
with open('data.json', 'r') as f:
    users = json.load(f)

# GET All
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# GET One by ID
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = users.get(id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

# POST
@app.route('/create-user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = str(data.get('id'))
    
    if user_id in users:
        return jsonify({"error": "User already exists"}), 400
    
    users[user_id] = data

    # Save to the JSON file
    save_to_file()

    return jsonify(data), 201

# PUT
@app.route('/update-user/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = users.get(id)

    if user:
        user.update(data)
        # Save to the JSON file
        save_to_file()
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404
    
# DELETE
@app.route('/delete-user/<id>', methods=['DELETE'])
def delete_user(id):
    user = users.get(id)
    if user:
        users.pop(id)
        # Save to the JSON file
        save_to_file()
        return jsonify({"message": "User deleted"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

def save_to_file():
    try:
        with open('data.json', 'w') as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        logging.error("Failed to save data to file: %s", str(e))
        return jsonify({"error": "Failed to save data to file. Please check the server logs for more details."}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)
