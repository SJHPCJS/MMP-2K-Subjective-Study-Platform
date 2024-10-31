from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import re

app = Flask(__name__)
CORS(app)  # 启用CORS

# 获取当前工作目录
BASE_DIR = os.getcwd()

# 设置静态文件夹路径
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
IMAGE_BASE_FOLDER = os.path.join(BASE_DIR, 'image_base')

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
    ids = read_ids_from_file('id.txt')

    if user_id in ids:
        return jsonify({'message': 'Record found'}), 200
    else:
        return jsonify({'message': 'Record not found'}), 404

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

    completed_images = {str(batch): 0 for batch in range(1, 5)}
    total_images = {str(batch): 0 for batch in range(1, 5)}

    for image in image_data:
        batch_name = image["batch"]
        total_images[batch_name] += 1
        if image["rate"] != "NULL":
            completed_images[batch_name] += 1

    result = {}
    for batch in completed_images:
        if total_images[batch] > 0:
            result[batch] = round((completed_images[batch] / total_images[batch]) * 100,2)
        else:
            result[batch] = 0

    return jsonify({"status": "success", "result": result}), 200

@app.route('/get_image/<id>', methods=['GET'])
def get_image(id):
    try:
        batch = request.args.get('batch')
        print(f"Received request for ID: {id} and batch: {batch}")


        file_path = os.path.join(BASE_DIR, id, f'{id}_result.json')
        print(f"Constructed file path: {file_path}")


        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return jsonify({"error": "File not found"}), 404


        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        filtered_data = []


        for item in data:
            img_path = item.get('url')
            if img_path and os.path.exists(img_path):
                item['url'] = f"{request.host_url}serve_image/{os.path.basename(img_path)}"

                if item['batch'] == batch:
                    filtered_data.append(item)
            else:
                print(f"Image file not found: {img_path}")
                item['url'] = "Image file not found"
                item['batch'] = "Unknown"

        print(f"Returning data: {filtered_data}")


        return jsonify(filtered_data), 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/serve_image/<filename>', methods=['GET'])
def serve_image(filename):
    image_path = os.path.join(IMAGE_BASE_FOLDER, filename)
    if os.path.exists(image_path):
        return send_file(image_path)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/submit_rate/<id>', methods=['POST'])
def submit_rate(id):
    try:
        data = request.json
        batch = str(data.get('batch'))
        image_id = str(data.get('image_id'))
        rate = data.get('rate')

        print(f"Received data: batch={batch}, image_id={image_id}, rate={rate}")

        if batch is None or image_id is None or rate is None:
            return jsonify({"error": "Missing required fields"}), 400

        # 构建用户的结果文件路径
        result_file_path = os.path.join(BASE_DIR, id, f"{id}_result.json")
        print(f"Result file path: {result_file_path}")

        if not os.path.exists(result_file_path):
            print(f"Result file not found: {result_file_path}")
            return jsonify({"error": "Result file not found"}), 404


        with open(result_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)


        image_updated = False
        for image in data:
            print(f"Checking image: {image}")
            if image.get('image_id') == image_id and image.get('batch') == batch:
                image['rate'] = rate
                image_updated = True
                break

        if not image_updated:
            print(f"Image not found: image_id={image_id}, batch={batch}")
            return jsonify({"error": "Image not found"}), 404


        with open(result_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return jsonify({"message": "Rate updated successfully"}), 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/update_data/<id>', methods=['POST'])
def update_data(id):
    try:
        data = request.json
        image_id = str(data.get('image_id'))
        tag_list = data.get('tagList')
        description = data.get('description')

        print(f"Received data: image_id={image_id}, tagList={tag_list}, description={description}")

        if image_id is None or tag_list is None or description is None:
            return jsonify({"error": "Missing required fields"}), 400


        result_file_path = os.path.join(BASE_DIR, id, f"{id}_result.json")
        print(f"Result file path: {result_file_path}")

        if not os.path.exists(result_file_path):
            print(f"Result file not found: {result_file_path}")
            return jsonify({"error": "Result file not found"}), 404


        with open(result_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)


        image_updated = False
        for image in data:
            print(f"Checking image: {image}")
            if image.get('image_id') == image_id:
                image['tagList'] = tag_list
                image['description'] = description
                image_updated = True
                break

        if not image_updated:
            print(f"Image not found: image_id={image_id}")
            return jsonify({"error": "Image not found"}), 404


        with open(result_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return jsonify({"message": "Data updated successfully"}), 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
