import os
import json
import pandas as pd
from collections import defaultdict

base_dir = os.path.dirname(__file__)
just_combined_data_path = os.path.join(base_dir, 'just_combined_data.json')
standardized_data_path = os.path.join(base_dir, 'standardized_data.json')

with open(just_combined_data_path, 'r', encoding='utf-8') as f:
    original_data = json.load(f)

with open(standardized_data_path, 'r', encoding='utf-8') as f:
    standardized_data = json.load(f)

image_stats = defaultdict(lambda: {
    'original_rate_list': [], 'standardized_rate_list': []
})

for user in original_data:
    for image_id in original_data[user]:
        original_rate = original_data[user][image_id]
        standardized_rate = standardized_data[user][image_id]

        image_stats[image_id]['original_rate_list'].append((user, int(original_rate)))
        image_stats[image_id]['standardized_rate_list'].append((user, float(standardized_rate)))


image_stats_df = pd.DataFrame()

for image_id, data in image_stats.items():
    temp_data = {
        'Image_ID': image_id,
    }
    for user, original_rate in data['original_rate_list']:
        temp_data[f'{user}_Original_Rate'] = original_rate

    for user, standardized_rate in data['standardized_rate_list']:
        temp_data[f'{user}_Standardized_Rate'] = standardized_rate

    image_stats_df = pd.concat([image_stats_df, pd.DataFrame([temp_data])], ignore_index=True)

image_stats_df.to_excel(os.path.join(base_dir, 'image_stats_user_columns.xlsx'), index=False)
