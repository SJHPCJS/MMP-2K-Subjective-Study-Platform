import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

base_dir = os.path.dirname(__file__)
just_combined_data_path = os.path.join(base_dir, 'just_combined_data.json')
standardized_data_path = os.path.join(base_dir, 'standardized_data.json')

output_dir = os.path.join(base_dir, 'comparison_charts')
os.makedirs(output_dir, exist_ok=True)

with open(just_combined_data_path, 'r', encoding='utf-8') as f:
    original_data = json.load(f)

with open(standardized_data_path, 'r', encoding='utf-8') as f:
    standardized_data = json.load(f)

image_stats = defaultdict(lambda: {
    'original_rate_list': [], 'standardized_rate_list': [],
    'original_max': 0, 'original_min': 0, 'original_mean': 0,
    'standardized_max': 0, 'standardized_min': 0, 'standardized_mean': 0,
    'standardized_variance': 0
})

for user in original_data:
    for image_id in original_data[user]:
        original_rate = original_data[user][image_id]
        standardized_rate = standardized_data[user][image_id]

        image_stats[image_id]['original_rate_list'].append(int(original_rate))
        image_stats[image_id]['standardized_rate_list'].append(float(standardized_rate))

for image_id, data in image_stats.items():
    original_rates = data['original_rate_list']
    standardized_rates = data['standardized_rate_list']

    data['original_max'] = int(np.max(original_rates))
    data['original_min'] = int(np.min(original_rates))
    data['original_mean'] = float(np.mean(original_rates))

    data['standardized_max'] = float(np.max(standardized_rates))
    data['standardized_min'] = float(np.min(standardized_rates))
    data['standardized_mean'] = float(np.mean(standardized_rates))
    data['standardized_variance'] = float(np.var(standardized_rates))

image_stats_df = pd.DataFrame([
    {
        'Image_ID': image_id,
        'Original_Max': data['original_max'],
        'Original_Min': data['original_min'],
        'Original_Mean': data['original_mean'],
        'Standardized_Max': data['standardized_max'],
        'Standardized_Min': data['standardized_min'],
        'Standardized_Mean': data['standardized_mean'],
        'Standardized_Variance': data['standardized_variance'],
        'Original_Rate_List': data['original_rate_list'],
        'Standardized_Rate_List': data['standardized_rate_list']
    }
    for image_id, data in image_stats.items()
])
image_stats_df.to_excel(os.path.join(base_dir, 'image_stats.xlsx'), index=False)

with open(os.path.join(base_dir, 'image_stats.json'), 'w', encoding='utf-8') as outfile:
    json.dump(image_stats, outfile, indent=4, ensure_ascii=False)

original_means = [data['original_mean'] for data in image_stats.values()]
standardized_means = [data['standardized_mean'] for data in image_stats.values()]
standardized_variances = [data['standardized_variance'] for data in image_stats.values()]
image_ids = list(image_stats.keys())

plt.figure(figsize=(12, 6))
index = np.arange(len(image_ids))
bar_width = 0.35

plt.bar(index, original_means, bar_width, label='Original Mean', color='blue')
plt.bar(index + bar_width, standardized_means, bar_width, label='Standardized Mean', color='green')

plt.xlabel('Image ID')
plt.ylabel('Mean Rate')
plt.title('Original Mean vs Standardized Mean Rates for Images')
plt.xticks(index + bar_width / 2, image_ids, rotation=90)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'mean_comparison.png'))
plt.close()

original_all_rates = [rate for data in image_stats.values() for rate in data['original_rate_list']]
plt.figure(figsize=(10, 6))
plt.hist(original_all_rates, bins=20, color='blue', alpha=0.7, label='Original Rates')
plt.title('Histogram of Original Rates for All Images')
plt.xlabel('Rate')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'original_histogram.png'))
plt.close()

plt.figure(figsize=(12, 6))
plt.bar(index, standardized_variances, bar_width, label='Standardized Variance', color='purple')
plt.xlabel('Image ID')
plt.ylabel('Variance')
plt.title('Standardized Variances for Images')
plt.xticks(index, image_ids, rotation=90)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'variance_comparison.png'))
plt.close()

plt.figure(figsize=(12, 6))
plt.scatter(standardized_means, standardized_variances, color='purple', alpha=0.7)
plt.title('Scatter Plot of Standardized Means vs Variances')
plt.xlabel('Standardized Mean')
plt.ylabel('Standardized Variance')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'mean_vs_variance_scatter.png'))
plt.close()
