from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)  # 启用CORS

# 获取当前工作目录
BASE_DIR = os.getcwd()

@app.route('/submit_rate/<id>', methods=['POST'])
def submit_rate(id):
    try:
        data = request.json
        batch = data.get('batch')
        image_id = data.get('image_id')
        rate = data.get('rate')

        if batch is None or image_id is None or rate is None:
            return jsonify({"error": "Missing required fields"}), 400

        # 构建用户的结果文件路径
        result_file_path = os.path.join(BASE_DIR, id, f"{id}_result.json")

        if not os.path.exists(result_file_path):
            return jsonify({"error": "Result file not found"}), 404

        # 读取结果文件内容
        with open(result_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 找到并更新对应的图片信息
        image_updated = False
        for image in data:
            if image.get('image_id') == str(image_id) and f"batch{batch}" in image.get('url'):
                image['rate'] = rate
                image_updated = True
                break

        if not image_updated:
            return jsonify({"error": "Image not found"}), 404

        # 写回更新后的数据
        with open(result_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        return jsonify({"message": "Rate updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5003)
