import pandas as pd
import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
from tqdm import tqdm
import warnings

# 禁用无关警告
warnings.filterwarnings("ignore", module="pymc")
warnings.filterwarnings("ignore", module="arviz")

def load_economic_activity_data(csv_path):
    # 手动指定各个段的位置（基于用户描述的结构）
    category_positions = {
        "Total economically active": (14, 26),
        "Total in employment": (27, 39),
        "Total unemployed": (40, 52),
        "Total economically inactive": (53, 65),
    }

    year_cols = [str(y) for y in range(2012, 2020)]

    result = {}

    for category, (start, end) in category_positions.items():
        df = pd.read_csv(csv_path, skiprows=start, nrows=end-start, encoding="utf-8")
        df = df.drop(columns=[col for col in df.columns if "rate" in col])  # 仅保留绝对数值
        df = df.rename(columns={"Area": "region"})
        df = df.set_index("region")
        df = df[year_cols]
        df = df.apply(pd.to_numeric, errors='coerce').fillna(0).astype(int)
        result[category] = df

    return result


def bayesian_forecast(series_data, forecast_year=2021):
    """贝叶斯线性回归预测"""
    y = series_data.values.astype(float)
    x = np.arange(len(y))  # 使用相对时间位置

    with pm.Model() as model:
        # 先验分布
        alpha = pm.Normal("alpha", mu=y.mean(), sigma=1e6)
        beta = pm.Normal("beta", mu=0, sigma=1e6)
        sigma = pm.HalfNormal("sigma", sigma=1e6)

        # 线性模型
        mu = alpha + beta * x
        y_obs = pm.Normal("y_obs", mu=mu, sigma=sigma, observed=y)

        # 后验采样
        trace = pm.sample(draws=2000,
                          tune=1000,
                          target_accept=0.95,
                          progressbar=False,
                          # chains= 12,
                          cores= 6)


    # 预测未来值
    x_future = len(y)  # 下一个时间点
    posterior_pred = trace.posterior["alpha"] + trace.posterior["beta"] * x_future
    posterior_pred = np.round(posterior_pred).astype(int)
    return az.summary(posterior_pred, kind="stats")


def generate_predictions(economic_data):
    """生成所有预测结果"""
    predictions = []

    for category, df in economic_data.items():
        print(f"\nProcessing category: {category}")

        # 过滤无效数据
        valid_regions = df.dropna(how='all').index

        for region in tqdm(valid_regions, desc=category):
            try:
                # 获取时间序列数据
                series = df.loc[region]

                # 跳过无效数据
                if series.isna().all() or (series == 0).all():
                    continue

                # 贝叶斯预测
                pred_summary = bayesian_forecast(series)

                # 保存结果
                predictions.append({
                    "region": region,
                    "category": category,
                    "2021_mean": pred_summary["mean"].values[0],
                    "2021_sd": pred_summary["sd"].values[0],
                    "2021_hdi_3%": pred_summary["hdi_3%"].values[0],
                    "2021_hdi_97%": pred_summary["hdi_97%"].values[0]
                })

            except Exception as e:
                print(f"\nError processing {region}: {str(e)}")
                continue

    return pd.DataFrame(predictions)


def reshape_predictions(df):
    """重构预测结果格式"""
    return df.pivot_table(
        index="region",
        columns="category",
        values=["2021_mean", "2021_sd", "2021_hdi_3%", "2021_hdi_97%"],
        aggfunc="first"
    ).droplevel(0, axis=1).reset_index()



if __name__ == "__main__":
    csv_path = "table/Economic Activity Data.csv"  # 替换为你的实际路径
    economic_data = load_economic_activity_data(csv_path)

    # 打印确认结构
    # for category, df in economic_data.items():
    #     print(f"\nCategory: {category}")
    #     print(df.head())

    # 生成预测
    predictions = generate_predictions(economic_data)

    # 重构格式并保存
    final_df = reshape_predictions(predictions)
    final_df.to_csv("table/2021_pred.csv", index=False)
    print("\n预测结果已保存至 table/2021_pred.csv")

    # 显示前5行结果
    print("\n预测结果示例：")
    print(final_df.head())
    # 不要轻易跑，运行一次40min