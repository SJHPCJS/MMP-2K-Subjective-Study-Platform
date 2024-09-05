from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json
import logging
import re
import shutil

app = Flask(__name__)
CORS(app)  # 启用CORS

# 设置日志记录
logging.basicConfig(filename='../server/app.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# 获取当前工作目录
BASE_DIR = os.getcwd()

# 设置静态文件夹路径
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

@app.route('/static/<path:filename>')
def serve_static_file(filename):
    return send_from_directory(STATIC_FOLDER, filename)

@app.route('/get_image/<id>', methods=['GET'])
def get_image(id):
    try:
        batch = request.args.get('batch')
        logger.debug(f"Received request for ID: {id} and batch: {batch}")

        # 构建文件路径
        file_path = os.path.join(BASE_DIR, id, f'{id}_result.json')
        logger.debug(f"Constructed file path: {file_path}")

        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return jsonify({"error": "File not found"}), 404

        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        filtered_data = []

        # 处理并生成图片URL
        for item in data:
            img_path = item.get('url')
            if img_path and os.path.exists(img_path):
                img_filename = os.path.basename(img_path)
                static_img_path = os.path.join(STATIC_FOLDER, img_filename)
                if not os.path.exists(static_img_path):
                    shutil.copy(img_path, static_img_path)
                item['url'] = f"{request.host_url}static/{img_filename}"

                # 从路径中提取批次信息
                batch_match = re.search(r'batch(\d+)', img_path)
                if batch_match:
                    item['batch'] = batch_match.group(1)
                else:
                    item['batch'] = "Unknown"

                if item['batch'] == batch:
                    filtered_data.append(item)
            else:
                logger.error(f"Image file not found: {img_path}")
                item['url'] = "Image file not found"
                item['batch'] = "Unknown"

        logger.debug(f"Returning data: {filtered_data}")

        # 返回JSON数据
        return jsonify(filtered_data), 200

    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5003)
