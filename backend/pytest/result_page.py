import os
import json
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许所有域的跨域请求


@app.route('/result/<user_id>', methods=['GET'])
def check_batches(user_id):
    user_path = os.path.join(os.getcwd(), user_id)
    if not os.path.exists(user_path):
        return jsonify({"status": "error", "message": "User ID not found"}), 404

    json_path = os.path.join(user_path, f'{user_id}_result.json')
    if not os.path.exists(json_path):
        return jsonify({"status": "error", "message": "Result JSON file not found"}), 404

    with open(json_path, 'r', encoding='utf-8') as json_file:
        image_data = json.load(json_file)

    completed_images = {f'batch{batch}': 0 for batch in range(1, 5)}
    total_images = {f'batch{batch}': 0 for batch in range(1, 5)}

    for image in image_data:
        url = image["url"]
        batch_name = os.path.basename(os.path.dirname(url))
        total_images[batch_name] += 1
        if image["rate"] != "NULL" and image["tagList"]:
            completed_images[batch_name] += 1

    result = {}
    for batch in completed_images:
        if total_images[batch] > 0:
            result[batch] = (completed_images[batch] / total_images[batch]) * 100
        else:
            result[batch] = 0

    return jsonify({"status": "success", "result": result}), 200


if __name__ == '__main__':
    app.run(port=5002)
