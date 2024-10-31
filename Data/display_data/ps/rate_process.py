import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

current_dir = os.path.dirname(os.path.abspath(__file__))


original_scores_path = os.path.join(current_dir, 'just_combined_data.json')
standardized_scores_path = os.path.join(current_dir, 'standardized_data.json')

with open(original_scores_path) as f:
    original_scores = json.load(f)
with open(standardized_scores_path) as f:
    standardized_scores = json.load(f)

df_original = pd.DataFrame(original_scores)
df_standardized = pd.DataFrame(standardized_scores)

plt.figure(figsize=(12, 12))
sns.heatmap(df_original, cmap='coolwarm', annot=False, square=True)
plt.title('Heatmap of Original Scores')
plt.xlabel('User')
plt.ylabel('Image ID')
heatmap_original_path = os.path.join(current_dir, 'heatmap_original_scores_default.png')
plt.savefig(heatmap_original_path, dpi=300, bbox_inches='tight')
plt.close()

plt.figure(figsize=(12, 12))
sns.heatmap(df_standardized, cmap='coolwarm', annot=False, square=True)
plt.title('Heatmap of Standardized Scores')
plt.xlabel('User')
plt.ylabel('Image ID')
heatmap_standardized_path = os.path.join(current_dir, 'heatmap_standardized_scores_default.png')
plt.savefig(heatmap_standardized_path, dpi=300, bbox_inches='tight')
plt.close()
