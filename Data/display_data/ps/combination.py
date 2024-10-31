import os
import json

base_dir = os.path.join(os.path.dirname(__file__))

all_data = {}

user_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

def process_user_data():
    for user in user_dirs:
        user_dir = os.path.join(base_dir, user)
        json_path = os.path.join(user_dir, 'data.json')

        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                user_data = json.load(f)

            all_data[user] = {}

            for entry in user_data:
                image_id = entry["image_id"]
                rate = entry["rate"]
                all_data[user][image_id] = rate

            all_data[user] = dict(sorted(all_data[user].items(), key=lambda x: int(x[0])))

def save_combined_data(output_file):
    output_path = os.path.join(base_dir, output_file)
    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(all_data, outfile, indent=4, ensure_ascii=False)

process_user_data()
save_combined_data('just_combined_data.json')
