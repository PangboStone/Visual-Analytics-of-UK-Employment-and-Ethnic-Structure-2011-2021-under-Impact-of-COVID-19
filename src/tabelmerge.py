import pandas as pd

ethnicity_df_2021 = pd.read_csv( "table/2021/eth_2021_new.csv")
economic_df_2021 = pd.read_csv("table/2021/eco_2021_new.csv")
# 读取数据
ethnicity_2011_df = pd.read_csv("table/2011/eth_2011_new.csv")
economic_2011_df = pd.read_csv("table/2011/eco_2011_new.csv")
# 去除多余列（如Rural Urban）
# ethnicity_2011_df = ethnicity_2011_df.drop(columns=["Rural Urban"], errors="ignore")

# 标准化列名：移除结尾的注释和前缀统一
def clean_column(col):
    col = col.replace("Ethnic Group: ", "").replace("measures: Value", "").strip()
    col = col.replace("Ethnic group: ", "").replace("measures: Value", "").strip()
    col = col.replace("Economic Activity: ", "").replace(";", ":").strip()
    col = col.replace("Economic activity status: ", "").replace(";", ":").strip()
    return col


# # 检查关键列是否一致
# assert all(ethnicity_df_2021.columns[:3] == economic_df_2021.columns[:3]), "前3列不一致"

# ethnicity_df_2021.columns = [clean_column(c) if c not in ["date", "geography", "geography code"] else c for c in ethnicity_df_2021.columns]
# economic_df_2021.columns = [clean_column(c) if c not in ["date", "geography", "geography code"] else c for c in economic_df_2021.columns]

# 合并数据（基于年份、地区名和地区代码）
merged_df = pd.merge(ethnicity_df_2021, economic_df_2021, on=["date", "geography", "geography code"], suffixes=("_eth", "_eco"))



# 保存结果
merged_df.to_csv("table/2021/merged_2021.csv", index=False)
print("✅ 合并完成，结果保存在 table/2021/merged_2021.csv")





ethnicity_2011_df.columns = [clean_column(c) if c not in ["date", "geography", "geography code"] else c for c in ethnicity_2011_df.columns]
economic_2011_df.columns = [clean_column(c) if c not in ["date", "geography", "geography code"] else c for c in economic_2011_df.columns]

# 合并
merged_df_2011 = pd.merge(ethnicity_2011_df, economic_2011_df, on=["date", "geography", "geography code"], how="inner")

# 保存结果

merged_df_2011.to_csv("table/2011/merged_2011.csv", index=False)
print("✅ 合并完成，结果保存在 table/2011/merged_2011.csv")

print(merged_df.head())

