import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore

file_path = 'just_combined_data.json'
with open(file_path) as f:
    all_users_data = json.load(f)

df = pd.DataFrame(all_users_data)

def zscore_image_ratings(df):
    results_df = df.apply(zscore, axis=1)
    return results_df

zscore_df = zscore_image_ratings(df)
output_path = 'zscore_each_image.xlsx'
zscore_df.to_excel(output_path, index=True)

lower_threshold = -2.0
upper_threshold = 2.0


n_rows, n_cols = zscore_df.shape
fig_width = n_cols * 1.2
fig_height = n_rows * 0.5

fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.axis('tight')
ax.axis('off')

table_data = zscore_df.values
table = ax.table(cellText=[[f'{val:.2f}' for val in row] for row in table_data],
                 rowLabels=zscore_df.index,
                 colLabels=zscore_df.columns,
                 cellLoc='center',
                 loc='center')

for i in range(len(zscore_df)):
    for j in range(len(zscore_df.columns)):
        cell = table[i+1, j]
        value = zscore_df.iloc[i, j]
        if value > upper_threshold or value < lower_threshold:
            cell.set_facecolor('red')
        else:
            cell.set_facecolor('white')

table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.2, 1.2)

visualization_output = 'zscore_table.png'
plt.savefig(visualization_output, bbox_inches='tight')
plt.show()
