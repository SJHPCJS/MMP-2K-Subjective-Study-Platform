import os
import json
import numpy as np
from sklearn.preprocessing import StandardScaler


base_dir = os.path.join(os.path.dirname(__file__))
input_file = os.path.join(base_dir, 'just_combined_data.json')

with open(input_file, 'r', encoding='utf-8') as infile:
    combined_data = json.load(infile)
standardized_data = {}

for user, user_data in combined_data.items():
    image_ids = list(user_data.keys())
    rates = list(user_data.values())

    rates_array = np.array(rates).reshape(-1, 1)
    scaler = StandardScaler()
    standardized_rates = scaler.fit_transform(rates_array).flatten()


    standardized_data[user] = {image_ids[i]: standardized_rates[i] for i in range(len(image_ids))}

output_file = os.path.join(base_dir, 'standardized_data.json')

with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(standardized_data, outfile, indent=4, ensure_ascii=False)
