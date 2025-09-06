import pandas as pd

# --- 1. 读取数据 ---
df_2011 = pd.read_csv("table/2011/merged_2011.csv")
df_2021 = pd.read_csv("table/2021/merged_2021.csv")

# --- 2. 重命名以统一结构 ---
df_2011.rename(columns={
    "geography": "Area Name",
    "geography code": "Area Code"
}, inplace=True)

df_2021.rename(columns={
    "geography": "Area Name",
    "geography code": "Area Code"
}, inplace=True)

# --- 3. 添加年份信息 ---
df_2011["Year"] = 2011
df_2021["Year"] = 2021

# --- 4. 定义辅助函数计算比例 ---
def compute_ratios(df, total_col, fields):
    for f in fields:
        ratio_col = f + " (%)"
        df[ratio_col] = df[f] / df[total_col]
    return df

# --- 5. 选取分析字段 ---
ethnicity_fields = [
    "White",
    "Black, Black British, Black Welsh, Caribbean or African",
    "Asian, Asian British or Asian Welsh",
    "Mixed or Multiple ethnic groups",
    "Other ethnic group"
]

employment_fields = [
    "Economically active (excluding full-time students):In employment",
    "Economically active (excluding full-time students): Unemployed",
    "Economically inactive"
]

# --- 6. 计算比例 ---
df_2011 = compute_ratios(df_2011, "Total: All usual residents", ethnicity_fields)
df_2021 = compute_ratios(df_2021, "Total: All usual residents", ethnicity_fields)

df_2011 = compute_ratios(df_2011, "Total: All usual residents aged 16 years and over", employment_fields)
df_2021 = compute_ratios(df_2021, "Total: All usual residents aged 16 years and over", employment_fields)

# --- 7. 选取统一列名 ---
common_cols = [
    "Area Code", "Area Name", "Year",
    "White (%)",
    "Black, Black British, Black Welsh, Caribbean or African (%)",
    "Asian, Asian British or Asian Welsh (%)",
    "Mixed or Multiple ethnic groups (%)",
    "Other ethnic group (%)",
    "Economically active (excluding full-time students):In employment (%)",
    "Economically active (excluding full-time students): Unemployed (%)",
    "Economically inactive (%)"
]

# --- 8. 合并两年数据 ---
df_all = pd.concat([
    df_2011[common_cols],
    df_2021[common_cols]
], ignore_index=True)

# --- 9. 保存清洗结果 ---
df_all.to_csv("data1.csv", index=False)
print("✅ 数据预处理完成")
