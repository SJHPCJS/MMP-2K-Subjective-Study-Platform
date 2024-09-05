import json
import pandas as pd
import matplotlib.pyplot as plt

# 读取JSON数据
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 转换为DataFrame
df = pd.DataFrame(data)

# 计算每个批次的图像数量
batch_counts = df['batch'].value_counts().sort_index()

# 计算每个批次的平均评分
batch_avg_rate = df.groupby('batch')['rate'].mean().sort_index()

# 可视化：每个批次的图像数量
plt.figure(figsize=(10, 5))
batch_counts.plot(kind='bar', color='skyblue')
plt.title('Number of Images per Batch')
plt.xlabel('Batch')
plt.ylabel('Number of Images')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.savefig('images_per_batch.png')
plt.show()

# 可视化：每个批次的平均评分
plt.figure(figsize=(10, 5))
batch_avg_rate.plot(kind='bar', color='lightgreen')
plt.title('Average Rating per Batch')
plt.xlabel('Batch')
plt.ylabel('Average Rating')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.savefig('average_rating_per_batch.png')
plt.show()

# 计算每个评分的图像数量
rating_counts = df['rate'].value_counts().sort_index()

# 可视化：每个评分的图像数量
plt.figure(figsize=(10, 5))
rating_counts.plot(kind='bar', color='coral')
plt.title('Number of Images per Rating')
plt.xlabel('Rating')
plt.ylabel('Number of Images')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.savefig('images_per_rating.png')
plt.show()

# 计算并可视化每个因子出现的次数
factor_list = [item['factor'] for sublist in df['tagList'] for item in sublist]
factor_counts = pd.Series(factor_list).value_counts()

plt.figure(figsize=(10, 5))
factor_counts.plot(kind='bar', color='orchid')
plt.title('Frequency of Factors in Tags')
plt.xlabel('Factor')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y')
plt.savefig('factor_frequency.png')
plt.show()
