import os
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict

base_dir = os.path.join(os.path.dirname(__file__))

all_data = defaultdict(lambda: {'rate_list': [], 'average': 0, 'max': 0, 'min': 0, 'variance': 0})

user_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

for user in user_dirs:
    user_dir = os.path.join(base_dir, user)
    json_path = os.path.join(user_dir, 'data.json')

    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            try:
                user_data = json.load(f)
            except json.JSONDecodeError:
                continue

        for image_info in user_data:
            image_id = image_info['image_id']
            rate = image_info['rate']
            all_data[image_id]['rate_list'].append(rate)

for image_id, image_info in all_data.items():
    rate_list = image_info['rate_list']
    image_info['average'] = float(np.mean(rate_list))
    image_info['max'] = int(np.max(rate_list))
    image_info['min'] = int(np.min(rate_list))
    image_info['variance'] = float(np.var(rate_list))  # 计算方差

output_path = os.path.join(os.path.dirname(__file__), 'combined_data.json')
with open(output_path, 'w') as f:
    json.dump(all_data, f, indent=4)

image_ids = sorted(all_data.keys(), key=int)
average_scores = [all_data[image_id]['average'] for image_id in image_ids]
max_scores = [all_data[image_id]['max'] for image_id in image_ids]
min_scores = [all_data[image_id]['min'] for image_id in image_ids]
variances = [all_data[image_id]['variance'] for image_id in image_ids]

# 方差最小-最大归一化
min_variance = min(variances)
max_variance = max(variances)
variances_normalized = [(v - min_variance) / (max_variance - min_variance) for v in variances]

plt.figure(figsize=(10, 6), dpi=300)
plt.bar(image_ids, average_scores)
plt.xlabel('Image ID')
plt.ylabel('Average Rating')
plt.title('Average Rating per Image')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'average_rating_per_image.png'))
plt.close()

plt.figure(figsize=(10, 6), dpi=300)
plt.plot(image_ids, average_scores, label='Average Rating', marker='o')
plt.fill_between(image_ids, min_scores, max_scores, color='lightgray', label='Range (min-max)')
plt.xlabel('Image ID')
plt.ylabel('Rating')
plt.title('Rating Range and Averages per Image')
plt.legend()
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'rating_range_per_image.png'))
plt.close()

bins = [0, 12.5, 37.5, 62.5, 87.5, 100]
bin_labels = ['0-12.5', '12.5-37.5', '37.5-62.5', '62.5-87.5', '87.5-100']

plt.figure(figsize=(8, 6), dpi=300)
plt.hist(average_scores, bins=bins, edgecolor='black', rwidth=0.8)
plt.xlabel('Average Score Range')
plt.ylabel('Frequency')
plt.title('Distribution of Average Scores in Bins')
plt.xticks(bins[:-1], bin_labels, rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'average_score_distribution.png'))
plt.close()

# 绘制归一化后的方差图
plt.figure(figsize=(10, 6), dpi=300)
plt.bar(image_ids, variances_normalized)
plt.xlabel('Image ID')
plt.ylabel('Normalized Variance')
plt.title('Normalized Variance per Image (Min-Max Scaling)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(base_dir, 'normalized_variance_per_image.png'))
plt.close()

# 导出数据为Excel文件
df = pd.DataFrame({
    'Image ID': image_ids,
    'Average Score': average_scores,
    'Max Score': max_scores,
    'Min Score': min_scores,
    'Variance': variances,
    'Normalized Variance': variances_normalized
})

excel_output_path = os.path.join(base_dir, 'image_data_with_variances.xlsx')
df.index += 1  # 将索引从1开始
df.to_excel(excel_output_path, index=True, index_label="Row Number")

print("Excel file and normalized variance plot generated successfully.")
print("Image IDs with max-min difference greater than 50:")
for image_id in image_ids:
    if all_data[image_id]['max'] - all_data[image_id]['min'] > 50:
        print(image_id)
