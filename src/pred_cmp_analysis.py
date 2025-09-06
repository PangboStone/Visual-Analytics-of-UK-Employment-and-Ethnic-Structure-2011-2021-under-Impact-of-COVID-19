# compare_forecast_actual.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 加载预测值和真实值
pred_df = pd.read_csv('table/2021_pred.csv')
pred_df = pred_df.iloc[:, :5]
real_df = pd.read_csv('table/2021_real.csv')

# 输出所有列名; 检查列名是否正确
# print(pred_df.columns.tolist())
# print(real_df.columns.tolist())

# 指定四个比较的指标列
categories = [
    'Total economically active',
    'Total in employment',
    'Total unemployed',
    'Total economically inactive'
]

# 确保两个表格按地区对齐
pred_df = pred_df.set_index('region').loc[real_df['region']].reset_index()
real_df = real_df.set_index('region').reset_index()

# 计算残差与相对误差并保存
error_records = []
for category in categories:
    for i in range(len(real_df)):
        region = real_df.loc[i, 'region']
        real = real_df.loc[i, category]
        pred = pred_df.loc[i, category]
        residual = pred - real
        relative_error = residual / real if real != 0 else 0
        error_records.append({
            'region': region,
            'category': category,
            'residual': residual,
            'relative_error': relative_error
        })

error_df = pd.DataFrame(error_records)
error_df.to_csv('pred_comparison.csv', index=False)

# 创建输出图像目录
os.makedirs('figures', exist_ok=True)


#  # 绘制条形图：每个类别一个图，创建一个2x2子图画布
fig, axs = plt.subplots(2, 2, figsize=(16, 12))
axs = axs.flatten()

for idx, category in enumerate(categories):
    ax = axs[idx]
    regions = real_df['region']
    real_values = real_df[category]
    pred_values = pred_df[category]

    x = range(len(regions))
    bar_width = 0.35

    ax.bar([i - bar_width / 2 for i in x], real_values, width=bar_width, label='Real', color='red')
    ax.bar([i + bar_width / 2 for i in x], pred_values, width=bar_width, label='Predicted', color='blue')

    ax.set_xticks(x)
    ax.set_xticklabels(regions, rotation=45, ha='right')
    ax.set_ylabel('Population Count')
    ax.set_title(f'{category}')

# 添加图例（只添加一次）
handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right', ncol=2, fontsize=12)

plt.tight_layout(rect=[0, 0, 1, 0.95])  # 留出上方空间给总标题和图例
fig.suptitle('Actual vs Predicted Values by Region (2021)', fontsize=16)
plt.savefig('figures/barplot_combined.png')
plt.show()
plt.close()

# 绘制热力图（相对误差）
heatmap_data = error_df.pivot(index='region', columns='category', values='relative_error')
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, annot=True, cmap='RdBu_r', center=0, fmt=".2%",linewidths=0.2, linecolor='black')
plt.title('Relative Error Heatmap (2021 Prediction vs Real)')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('figures/error_heatmap.png')
plt.show()
plt.close()

