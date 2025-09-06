import pandas as pd
import os

# 创建输出文件夹
output_dir = "TableauDataSource"
os.makedirs(output_dir, exist_ok=True)
# 定义区域名称到代码的映射字典
region_code_mapping = {
    "country:England and Wales": "K04000001",
    "gor:North East": "E12000001",
    "gor:North West": "E12000002",
    "gor:Yorkshire and The Humber": "E12000003",
    "gor:East Midlands": "E12000004",
    "gor:West Midlands": "E12000005",
    "gor:East": "E12000006",
    "gor:London": "E12000007",
    "gor:South East": "E12000008",
    "gor:South West": "E12000009",
    "gor:Wales": "W92000004"
}

# 添加geography code
def add_geography_code(df):

    # 添加geography code列
    df['geography code'] = df['region'].map(region_code_mapping)

    # 检查是否有未匹配的区域
    unmatched = df[df['geography code'].isna()]['region'].unique()
    if len(unmatched) > 0:
        print(f"警告: 以下区域未找到匹配的代码: {unmatched}")



# 1. 转换 merged_2011.csv 和 merged_2021.csv 为 long format
def convert_merged_csv(filename):
    df = pd.read_csv(filename)
    id_vars = ['date', 'geography', 'geography code']
    df_long = df.melt(id_vars=id_vars, var_name='category', value_name='value')
    basename = os.path.basename(filename)
    output_path = os.path.join(output_dir, basename.replace('.csv', '_long.csv'))
    df_long.to_csv(output_path, index=False)


# convert_merged_csv("table/2011/merged_2011.csv")
# convert_merged_csv("table/2021/merged_2021.csv")

# df2011 = pd.read_csv('TableauDataSource/merged_2011_long.csv')
# df2021 = pd.read_csv('TableauDataSource/merged_2021_long.csv')
#
#
# # 合并两个 DataFrame
# df_combined = pd.concat([df2011, df2021], ignore_index=True)
#
# # 输出合并后的 CSV 文件
# df_combined.to_csv("TableauDataSource/merged_2021_2011_long.csv", index=False)
#

# 2. 合并 2021_real.csv 和 2021_pred.csv 为 long format
def convert_pred_real(real_file, pred_file):
    real_df = pd.read_csv(real_file)
    pred_df = pd.read_csv(pred_file)

    real_long = real_df.melt(id_vars=['region'], var_name='category', value_name='value')
    real_long['source'] = 'real'

    pred_long = pred_df.melt(id_vars=['region'], var_name='category', value_name='value')
    pred_long['source'] = 'predicted'

    combined_df = pd.concat([real_long, pred_long], ignore_index=True)
    add_geography_code(combined_df)
    combined_df.to_csv(os.path.join(output_dir, 'pred_vs_real_long.csv'), index=False)


# convert_pred_real("table/2021_real.csv", "table/2021_pred.csv")


# 3. 转换 pred_comparison.csv 为 long format（metric-value）
def convert_comparison(filename):
    df = pd.read_csv(filename)
    df_long = df.melt(id_vars=['region', 'category'], var_name='metric', value_name='value')
    add_geography_code(df_long)
    df_long.to_csv(os.path.join(output_dir, 'comparison_long.csv'), index=False)


# convert_comparison("table/pred_comparison.csv")

# 输出已完成的转换文件列表
os.listdir(output_dir)
