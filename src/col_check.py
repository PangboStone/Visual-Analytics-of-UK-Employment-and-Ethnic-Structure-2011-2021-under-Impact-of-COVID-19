import pandas as pd

# 读取两个合并后的 CSV 文件
df_2011 = pd.read_csv("table/2011/merged_2011.csv")
df_2021 = pd.read_csv("table/2021/merged_2021.csv")

# 获取列名
columns_2011 = set(df_2011.columns)
columns_2021 = set(df_2021.columns)

# 输出差异
print("列名仅在 2011 中的：")
print(columns_2011 - columns_2021)

print("\n列名仅在 2021 中的：")
print(columns_2021 - columns_2011)

# 检查是否完全一致
if columns_2011 == columns_2021:
    print("\n✅ 两个文件的列名完全一致。")
else:
    print("\n⚠️ 两个文件的列名不一致，请查看上方差异。")



# # 读取 merged_2011（已初步重命名过）
# df_2011 = pd.read_csv("table/2011/merged_2011.csv")
#
# # 去除所有字段名右侧冒号
# df_2011.columns = [col.strip().rstrip(':') for col in df_2011.columns]
#
# # 构建扩展字段映射（使其与 merged_2021 一致）
# column_mapping = {
#     "All usual residents": "Total: All usual residents",
#     "All usual residents aged 16 to 74": "Total: All usual residents aged 16 years and over",
#     "Economically inactive Student (including full-time students)": "Economically inactive: Student",
#     "Economically active Employee Part-time": "Economically active (excluding full-time students): In employment: Employee: Part-time",
#     "Economically active Employee Full-time": "Economically active (excluding full-time students): In employment: Employee: Full-time",
#     "Economically active Self-employed": "Economically active (excluding full-time students): In employment: Self-employed without employees",
#     "Economically active Unemployed": "Economically active (excluding full-time students): Unemployed",
#     "Economically active In employment": "Economically active (excluding full-time students):In employment",
#     "Economically active": "Economically active (excluding full-time students)",
#     "Economically active Full-time student": "Economically active and a full-time student",
#     "Economically Inactive": "Economically inactive",
#     "Economically inactive Retired": "Economically inactive: Retired",
#     "Economically inactive Looking after home or family": "Economically inactive: Looking after home or family",
#     "Economically inactive Long-term sick or disabled": "Economically inactive: Long-term sick or disabled",
#     "Economically inactive Other": "Economically inactive: Other",
#     "Unemployed Never worked": "Economically active (excluding full-time students): Unemployed",  # 没有精确匹配，只能近似合并
#     "Unemployed Age 16 to 24": "Economically active (excluding full-time students): Unemployed",  # 合并统计类别
#     "Unemployed Age 50 to 74": "Economically active (excluding full-time students): Unemployed",  # 同上
#     "Long-term unemployed": "Economically active (excluding full-time students): Unemployed",  # 统一并入“失业”
#     "White": "White",
#     "White Irish": "White: Irish",
#     "White English/Welsh/Scottish/Northern Irish/British": "White: English, Welsh, Scottish, Northern Irish or British",
#     "White Other White": "White: Other White",
#     "White Gypsy or Irish Traveller": "White: Gypsy or Irish Traveller",
#     "Mixed/multiple ethnic groups": "Mixed or Multiple ethnic groups",
#     "Mixed/multiple ethnic groups White and Black Caribbean": "Mixed or Multiple ethnic groups: White and Black Caribbean",
#     "Mixed/multiple ethnic groups White and Black African": "Mixed or Multiple ethnic groups: White and Black African",
#     "Mixed/multiple ethnic groups White and Asian": "Mixed or Multiple ethnic groups: White and Asian",
#     "Mixed/multiple ethnic groups Other Mixed": "Mixed or Multiple ethnic groups: Other Mixed or Multiple ethnic groups",
#     "Asian/Asian British": "Asian, Asian British or Asian Welsh",
#     "Asian/Asian British Indian": "Asian, Asian British or Asian Welsh: Indian",
#     "Asian/Asian British Pakistani": "Asian, Asian British or Asian Welsh: Pakistani",
#     "Asian/Asian British Bangladeshi": "Asian, Asian British or Asian Welsh: Bangladeshi",
#     "Asian/Asian British Chinese": "Asian, Asian British or Asian Welsh: Chinese",
#     "Asian/Asian British Other Asian": "Asian, Asian British or Asian Welsh: Other Asian",
#     "Black/African/Caribbean/Black British": "Black, Black British, Black Welsh, Caribbean or African",
#     "Black/African/Caribbean/Black British African": "Black, Black British, Black Welsh, Caribbean or African: African",
#     "Black/African/Caribbean/Black British Caribbean": "Black, Black British, Black Welsh, Caribbean or African: Caribbean",
#     "Black/African/Caribbean/Black British Other Black": "Black, Black British, Black Welsh, Caribbean or African: Other Black",
#     "Other ethnic group": "Other ethnic group",
#     "Other ethnic group Arab": "Other ethnic group: Arab",
#     "Other ethnic group Any other ethnic group": "Other ethnic group: Any other ethnic group"
# }
#
# # 重命名字段
# df_2011.rename(columns=column_mapping, inplace=True)
#
# # 保存标准化后的文件
# df_2011.to_csv("table/2011/merged_2011.csv", index=False)
#
# print("✅ merged_2011 列名已完全标准化为 merged_2021 格式！")
#

'''
# --- 对 2011 表，合并失业子类字段 ---
unemployed_subfields_2011 = [
    'Unemployed: Age 16 to 24',
    'Unemployed: Never worked',
    'Unemployed: Age 50 to 74',
    'Economically active (excluding full-time students): Unemployed.1'
]
df_2011['Economically active (excluding full-time students): Unemployed'] = (
    df_2011.get('Economically active (excluding full-time students): Unemployed', 0)
)
for col in unemployed_subfields_2011:
    if col in df_2011.columns:
        df_2011['Economically active (excluding full-time students): Unemployed'] += df_2011[col]
        df_2011.drop(columns=col, inplace=True)

# --- 对 2021 表，合并 self-employed 子类字段 ---
# 1. without employees
df_2021['Economically active (excluding full-time students): In employment: Self-employed without employees'] = (
    df_2021.get('Economically active (excluding full-time students): In employment: Self-employed without employees: Full-time', 0) +
    df_2021.get('Economically active (excluding full-time students): In employment: Self-employed without employees: Part-time', 0)
)
df_2021.drop(columns=[
    'Economically active (excluding full-time students): In employment: Self-employed without employees: Full-time',
    'Economically active (excluding full-time students): In employment: Self-employed without employees: Part-time'
], inplace=True, errors='ignore')

# 2. with employees
df_2021['Economically active (excluding full-time students): In employment: Self-employed with employees'] = (
    df_2021.get('Economically active (excluding full-time students): In employment: Self-employed with employees: Full-time', 0) +
    df_2021.get('Economically active (excluding full-time students): In employment: Self-employed with employees: Part-time', 0)
)
df_2021.drop(columns=[
    'Economically active (excluding full-time students): In employment: Self-employed with employees: Full-time',
    'Economically active (excluding full-time students): In employment: Self-employed with employees: Part-time'
], inplace=True, errors='ignore')
# --- 对 2021 表，删除与全日制学生相关的字段 ---
fields_to_drop_2021 = [
    'Economically active and a full-time student:In employment:Self-employed without employees',
    'Economically active and a full-time student:In employment:Self-employed with employees',
    'Economically active and a full-time student:In employment:Self-employed without employees',
    'Economically active and a full-time student:In employment:Employee',
    'Economically active and a full-time student:In employment',
    'Economically active and a full-time student: Unemployed',
    'Economically active and a full-time student: In employment: Self-employed with employees: Full-time',
    'Economically active and a full-time student: In employment: Self-employed with employees',
    'Economically active and a full-time student: In employment: Self-employed without employees: Full-time',
    'Economically active and a full-time student: In employment: Self-employed without employees: Part-time',
    'Economically active and a full-time student: In employment: Employee: Part-time',
    'Economically active and a full-time student: In employment: Employee: Full-time',
    'Economically active and a full-time student: In employment: Self-employed with employees: Part-time',
    'White: Roma'
    'Economically active (excluding full-time students):In employment:Self-employed with employees',
    'Economically active (excluding full-time students): In employment: Self-employed with employees',
    'Economically active (excluding full-time students):In employment:Self-employed without employees',
    'Economically active (excluding full-time students):In employment:Employee',
    'Economically active (excluding full-time students):In employment:Self-employed with employees'

]

df_2021.drop(columns=fields_to_drop_2021, inplace=True, errors='ignore')


# 保存最终标准化后的表格
df_2011.to_csv("table/2011/merged_2011.csv", index=False)
df_2021.to_csv("table/2021/merged_2021.csv", index=False)
print("✅ 两个年份的数据已字段标准化并保存")


'''