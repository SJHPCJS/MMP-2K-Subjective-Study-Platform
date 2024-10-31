import json
import pandas as pd


def determine_score_range(average_rating):
    levels = [0, 25, 50, 75, 100]
    closest_level = min(levels, key=lambda x: abs(x - average_rating))
    if closest_level == 0:
        lower_bound, upper_bound = 0, 25
    elif closest_level == 100:
        lower_bound, upper_bound = 75, 100
    else:
        lower_bound = max(0, closest_level - 25)
        upper_bound = min(100, closest_level + 25)
    return lower_bound, upper_bound


file_path = 'processed_rate.json'
with open(file_path) as f:
    all_users_data = json.load(f)

new_data = {}
json_data = {}

for key, value in all_users_data.items():
    average_rating = value.get("average_rating", 0)
    lower_bound, upper_bound = determine_score_range(average_rating)

    value["score_range"] = {
        "lower_bound": lower_bound,
        "upper_bound": upper_bound
    }

    new_data[key] = value
    json_data[key] = {
        "score_range": {
            "lower_bound": lower_bound,
            "upper_bound": upper_bound
        }
    }

new_json_path = 'final_image_info.json'
with open(new_json_path, 'w') as f:
    json.dump(json_data, f, indent=4)

df = pd.DataFrame.from_dict(new_data, orient='index')
output_excel_path = 'final_image_info.xlsx'
df.to_excel(output_excel_path, index_label='ID')
