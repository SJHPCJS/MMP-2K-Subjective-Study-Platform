import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, t

current_dir = os.path.dirname(os.path.abspath(__file__))

standardized_data_path = os.path.join(current_dir, 'standardized_data.json')
just_combined_data_path = os.path.join(current_dir, 'just_combined_data.json')
image_stats_path = os.path.join(current_dir, 'image_stats.json')
output_excel_path = os.path.join(current_dir, 'analysis_results.xlsx')

with open(standardized_data_path) as f:
    standardized_data = json.load(f)
with open(just_combined_data_path) as f:
    just_combined_data = json.load(f)
with open(image_stats_path) as f:
    image_stats = json.load(f)

def user_correlation_analysis(all_users_data):
    correlations = {}
    for user, ratings in all_users_data.items():
        user_ratings_list = []
        avg_other_users_list = []
        for image_id, user_rating in ratings.items():
            other_users_ratings = [r[image_id] for u, r in all_users_data.items() if u != user]
            if other_users_ratings:
                avg_other_users_rating = np.mean(other_users_ratings)
                user_ratings_list.append(user_rating)
                avg_other_users_list.append(avg_other_users_rating)
        if len(user_ratings_list) >= 2 and len(avg_other_users_list) >= 2:
            correlations[user] = pearsonr(user_ratings_list, avg_other_users_list)[0]
        else:
            correlations[user] = None
    return correlations

correlations = user_correlation_analysis(just_combined_data)
standardized_correlations = user_correlation_analysis(standardized_data)

def user_correlation_analysis2(all_users_data):
    correlations = {}
    for user, ratings in all_users_data.items():
        user_ratings_list = []
        avg_all_users_list = []
        for image_id, user_rating in ratings.items():
            all_users_ratings = [r[image_id] for r in all_users_data.values()]
            if all_users_ratings:
                avg_all_users_rating = np.mean(all_users_ratings)
                user_ratings_list.append(user_rating)
                avg_all_users_list.append(avg_all_users_rating)
        if len(user_ratings_list) >= 2 and len(avg_all_users_list) >= 2:
            correlations[user] = pearsonr(user_ratings_list, avg_all_users_list)[0]
        else:
            correlations[user] = None
    return correlations
print(user_correlation_analysis2(standardized_data))

def grubbs_test(data, alpha=0.05):
    mean_data = np.mean(data)
    std_dev = np.std(data)
    N = len(data)
    G_max = max(abs(data - mean_data)) / std_dev
    G_min = min(abs(data - mean_data)) / std_dev
    t_dist = t.ppf(1 - alpha / (2 * N), N - 2)
    G_critical = ((N - 1) / np.sqrt(N)) * np.sqrt((t_dist ** 2) / (N - 2 + t_dist ** 2))
    is_outlier = G_max > G_critical or G_min > G_critical
    return G_max, G_min, G_critical, is_outlier

grubbs_results = {}
for image_id, stats in image_stats.items():
    original_rate_list = stats['original_rate_list']
    grubbs_results[image_id] = grubbs_test(original_rate_list)

correlation_df = pd.DataFrame(list(correlations.items()), columns=['User', 'Correlation'])
standardized_correlation_df = pd.DataFrame(list(standardized_correlations.items()), columns=['User', 'Correlation'])
grubbs_df = pd.DataFrame.from_dict(grubbs_results, orient='index', columns=['G_max', 'G_min', 'G_critical', 'Is_Outlier'])

plt.figure(figsize=(10, 6))
plt.bar(correlation_df['User'], correlation_df['Correlation'], color='skyblue')
plt.xlabel('User')
plt.ylabel('Correlation')
plt.title('User Correlation Analysis')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(current_dir, 'user_correlation.png'))
plt.show()

plt.figure(figsize=(10, 6))
plt.bar(standardized_correlation_df['User'], standardized_correlation_df['Correlation'], color='skyblue')
plt.xlabel('User')
plt.ylabel('Correlation')
plt.title('Standardized User Correlation Analysis')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(current_dir, 'standardized_user_correlation.png'))
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(grubbs_df.index, grubbs_df['G_max'], label='G_max values', color='blue')
plt.scatter(grubbs_df.index, grubbs_df['G_min'], label='G_min values', color='green')
plt.axhline(y=grubbs_df['G_critical'].iloc[0], color='r', linestyle='--', label='G critical value')
plt.xlabel('Image ID')
plt.ylabel('G Value')
plt.title('Grubbs Test for Outliers')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(current_dir, 'grubbs_test.png'))
plt.show()

with pd.ExcelWriter(output_excel_path) as writer:
    correlation_df.to_excel(writer, sheet_name='Correlations', index=False)
    standardized_correlation_df.to_excel(writer, sheet_name='Standardized Correlations', index=False)
    grubbs_df.to_excel(writer, sheet_name='Grubbs Test', index_label='Image ID')

print(f"Results saved to {output_excel_path}")
