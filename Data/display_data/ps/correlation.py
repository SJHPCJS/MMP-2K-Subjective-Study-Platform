import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 文件路径
base_dir = os.path.dirname(__file__)
standardized_data_path = os.path.join(base_dir, 'standardized_data.json')

# 新建一个目录存放图表
output_dir = os.path.join(base_dir, 'correlation_analysis')
os.makedirs(output_dir, exist_ok=True)

# 读取 JSON 数据
with open(standardized_data_path, 'r', encoding='utf-8') as f:
    standardized_data = json.load(f)

# 转换为DataFrame，行是image_id，列是用户
df = pd.DataFrame(standardized_data).T  # 使用.T转置，确保图像ID为行，用户为列
df.index = range(1, 73)  # 设置图像ID为1到72


# 函数：计算每个用户与其他用户的相关性
def calculate_user_correlation(df):
    results = {}

    for user in df.columns:
        # 排除当前用户，计算其他用户的平均评分
        other_users_mean = df.drop(columns=[user]).mean(axis=1)

        # 计算当前用户与其他用户平均评分的相关系数（逐张图计算）
        image_correlations = df.apply(lambda x: x.corr(other_users_mean), axis=0)

        # 计算每个用户的整体相关性（所有图的相关系数的平均值）
        overall_correlation = df[user].corr(other_users_mean)

        # 保存结果
        results[user] = {
            'image_correlations': image_correlations.tolist(),
            'overall_correlation': overall_correlation
        }

    return results


# 评估每个用户与其他用户的相关性
correlation_results = calculate_user_correlation(df)

# 转换结果为DataFrame
image_corr_df = pd.DataFrame({
    user: result['image_correlations'] for user, result in correlation_results.items()
}, index=df.index)  # 保持图像ID作为索引

# 保存每张图片的相关性结果到Excel文件
overall_corr_df = pd.DataFrame({
    user: [result['overall_correlation']] for user, result in correlation_results.items()
}).T
overall_corr_df.columns = ['Overall Correlation']

# 合并结果并保存到同一个Excel文件
with pd.ExcelWriter(os.path.join(base_dir, 'user_correlations.xlsx')) as writer:
    image_corr_df.to_excel(writer, sheet_name='Image Correlations')
    overall_corr_df.to_excel(writer, sheet_name='Overall Correlations')


# 绘制总体相关性的柱状图
plt.figure(figsize=(10, 6))
overall_corr_df['Overall Correlation'].plot(kind='bar', color='skyblue')
plt.title('Overall Correlation for Each User with Others')
plt.xlabel('User')
plt.ylabel('Correlation')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'overall_correlation_bar.png'))
plt.close()

# 绘制用户之间的图像评分相关性热图
plt.figure(figsize=(12, 8))
sns.heatmap(image_corr_df, annot=False, cmap='coolwarm', cbar=True)
plt.title('Correlation Heatmap between Users on Images')
plt.xlabel('Users')
plt.ylabel('Images')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'correlation_heatmap.png'))
plt.close()

# 为每个用户生成散点图：用户评分 vs 其他用户平均评分
for user in df.columns:
    other_users_mean = df.drop(columns=[user]).mean(axis=1)
    plt.figure(figsize=(8, 6))
    plt.scatter(df[user], other_users_mean, alpha=0.5, color='purple')
    plt.title(f'User {user} Ratings vs Other Users Mean Ratings')
    plt.xlabel(f'User {user} Ratings')
    plt.ylabel('Other Users Mean Ratings')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'user_{user}_scatter.png'))
    plt.close()
