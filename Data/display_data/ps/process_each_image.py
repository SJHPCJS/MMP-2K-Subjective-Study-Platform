import json
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import zscore, pearsonr

file_path = 'just_combined_data.json'
with open(file_path) as f:
    all_users_data = json.load(f)

df = pd.DataFrame(all_users_data)

def process_image_ratings(df, lower_threshold=-2.0, upper_threshold=2.0):
    zscore_df = df.apply(zscore, axis=1)
    processed_df = df.copy()

    for col in zscore_df.columns:
        for index in zscore_df.index:
            if zscore_df.loc[index, col] < lower_threshold or zscore_df.loc[index, col] > upper_threshold:
                valid_values = df.loc[index][(zscore_df.loc[index] >= lower_threshold) & (zscore_df.loc[index] <= upper_threshold)]
                if not valid_values.empty:
                    valid_mean = valid_values.mean()
                else:
                    valid_mean = df.loc[index].mean()
                processed_df.loc[index, col] = valid_mean

    return processed_df

processed_df = process_image_ratings(df)

image_avg_ratings = processed_df.mean(axis=1).to_dict()
processed_data = processed_df.to_dict(orient='index')

for image_id, data in processed_data.items():
    data['average_rating'] = image_avg_ratings[image_id]

processed_output_path = 'processed_rate.json'
with open(processed_output_path, 'w') as f:
    json.dump(processed_data, f, indent=4)

user_correlations = {}
user_avg_scores = {}

for user in df.columns:
    user_avg = processed_df[user].mean()
    user_avg_scores[user] = user_avg

    other_users_avg = processed_df.drop(columns=[user]).mean(axis=1)
    correlation, _ = pearsonr(processed_df[user], other_users_avg)
    user_correlations[user] = correlation

output_excel_path = 'processed_user_corr.xlsx'
result_df = pd.DataFrame({
    'User': user_correlations.keys(),
    'Average_Score': user_avg_scores.values(),
    'Correlation_with_Others': user_correlations.values()
})
result_df.to_excel(output_excel_path, index=False)

print(f'Processed data saved to {processed_output_path}')
print(f'Correlation data saved to {output_excel_path}')

correlation_bar_chart_path = 'user_correlation_with_others.png'
plt.figure(figsize=(14, 8))
plt.bar(result_df['User'], result_df['Correlation_with_Others'], color='lightgreen', edgecolor='black')
plt.title('Correlation of Users with Others', fontsize=16)
plt.xlabel('User', fontsize=14)
plt.ylabel('Correlation', fontsize=14)
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(correlation_bar_chart_path, format='png', dpi=300)
plt.close()


bar_chart_path = 'user_average_scores.png'
plt.figure(figsize=(14, 8))
plt.bar(result_df['User'], result_df['Average_Score'], color='skyblue', edgecolor='black')
plt.title('Average Scores of Users', fontsize=16)
plt.xlabel('User', fontsize=14)
plt.ylabel('Average Score', fontsize=14)
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig(bar_chart_path, format='png', dpi=300)
plt.close()

