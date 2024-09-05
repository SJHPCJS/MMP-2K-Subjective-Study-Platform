from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def read_ids_from_file(file_path):
    with open(file_path, 'r') as file:
        ids = file.read().splitlines()
    return ids

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if 'id' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    user_id = data['id']
    ids = read_ids_from_file('../server/id.txt')  # 确保id.txt在同一个目录下

    if user_id in ids:
        return jsonify({'message': 'Record found'}), 200
    else:
        return jsonify({'message': 'Record not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
