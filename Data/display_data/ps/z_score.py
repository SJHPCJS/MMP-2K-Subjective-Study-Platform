import os
import json
import numpy as np
from sklearn.preprocessing import StandardScaler

# 定义基础目录
base_dir = os.path.join(os.path.dirname(__file__))

# 读取just_combined_data.json文件
input_file = os.path.join(base_dir, 'just_combined_data.json')

with open(input_file, 'r', encoding='utf-8') as infile:
    combined_data = json.load(infile)

# 初始化一个新的字典来存储标准化后的数据
standardized_data = {}

# 对每个用户对象的数据进行标准化处理
for user, user_data in combined_data.items():
    image_ids = list(user_data.keys())
    rates = list(user_data.values())

    # 将 rates 转化为 numpy 数组并进行 z-score 标准化
    rates_array = np.array(rates).reshape(-1, 1)
    scaler = StandardScaler()
    standardized_rates = scaler.fit_transform(rates_array).flatten()

    # 将标准化后的数据重新保存到字典中，使用原有的 image_id
    standardized_data[user] = {image_ids[i]: standardized_rates[i] for i in range(len(image_ids))}

# 将标准化后的数据保存到新的JSON文件
output_file = os.path.join(base_dir, 'standardized_data.json')

with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(standardized_data, outfile, indent=4, ensure_ascii=False)
