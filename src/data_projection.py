import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import umap

import matplotlib.pyplot as plt
import seaborn as sns


import torch
import torch.nn as nn
from scipy.spatial.distance import pdist, squareform



def load_and_prepare_data(file_path):
    df = pd.read_csv(file_path)
    df_numeric = df.select_dtypes(include=[np.number])
    return StandardScaler().fit_transform(df_numeric), df['geography code']


def run_pca(data, geography_codes, out_path='output/pca_projection.csv'):
    pca = PCA(n_components=2, random_state=42)
    projected = pca.fit_transform(data)
    df_proj = pd.DataFrame(projected, columns=['x', 'y'])
    df_proj['geography code'] = geography_codes.values
    df_proj.to_csv(out_path, index=False)
    print(f'[✓] PCA projection saved to {out_path}')


def run_umap(data, geography_codes, out_path='output/umap_projection.csv'):
    reducer = umap.UMAP(n_components=2, random_state=42)
    projected = reducer.fit_transform(data)
    df_proj = pd.DataFrame(projected, columns=['x', 'y'])
    df_proj['geography code'] = geography_codes.values
    df_proj.to_csv(out_path, index=False)
    print(f'[✓] UMAP projection saved to {out_path}')




#  Neuroscale方法
class RBFMapping(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.centers = nn.Parameter(torch.randn(hidden_dim, input_dim))
        self.linear = nn.Linear(hidden_dim, output_dim)
        self.sigma = nn.Parameter(torch.tensor(1.0))

    def forward(self, x):
        diff = x.unsqueeze(1) - self.centers.unsqueeze(0)  # [N, K, D]
        dists = torch.sum(diff**2, dim=2)  # [N, K]
        activations = torch.exp(-dists / (2 * self.sigma**2))
        return self.linear(activations)

def pairwise_dist(x):
    """Compute pairwise Euclidean distance matrix."""
    return torch.cdist(x, x, p=2)

def run_neuroscale(data_np, geography_codes, out_path='output/neuroscale_projection_2011.csv', epochs=500, lr=1e-2):
    print("[•] Running Neuroscale projection...")

    # Standardize to torch tensor
    data = torch.tensor(data_np, dtype=torch.float32)
    target_dist = pairwise_dist(data).detach()

    model = RBFMapping(input_dim=data.shape[1], hidden_dim=20, output_dim=2)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        optimizer.zero_grad()
        low_dim = model(data)
        low_dist = pairwise_dist(low_dim)
        loss = torch.mean((low_dist - target_dist)**2)
        loss.backward()
        optimizer.step()
        if epoch % 50 == 0 or epoch == epochs - 1:
            print(f"[{epoch}/{epochs}] Loss: {loss.item():.4f}")

    final_proj = model(data).detach().numpy()
    df_proj = pd.DataFrame(final_proj, columns=['x', 'y'])
    df_proj['geography code'] = geography_codes.values
    df_proj.to_csv(out_path, index=False)
    print(f'[✓] Neuroscale projection saved to {out_path}')


def plot_projection(csv_path, output_path=None, color_by=None, title=None):
    """

    参数:
        csv_path (str): 投影结果CSV文件路径
        output_path (str): 图片保存路径（可选）
        color_by (str): 着色列名（可选）
        title (str): 自定义标题（可选）
    """
    # 读取数据
    df = pd.read_csv(csv_path)

    # 创建图形
    plt.figure(figsize=(10, 8))

    # 基础绘图
    if color_by and color_by in df.columns:
        sc = plt.scatter(df['x'], df['y'], c=df[color_by], cmap='viridis', alpha=0.7)
        plt.colorbar(sc, label=color_by)
    else:
        plt.scatter(df['x'], df['y'], alpha=0.7)

    # 标题和标签
    if not title:
        title = "Data Projection"
    plt.title(title)
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")
    plt.grid(alpha=0.3)

    # 保存或显示
    if output_path:
        # plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {output_path}")
    else:
        plt.show()
    plt.close()

def main():
    os.makedirs('output', exist_ok=True)

    # 使用 2011 数据
    # data_2011, codes_2011 = load_and_prepare_data('table/2011/merged_2011.csv')
    # run_pca(data_2011, codes_2011, out_path='output/pca_projection_2011.csv')
    # run_umap(data_2011, codes_2011, out_path='output/umap_projection_2011.csv')
    # run_neuroscale(data_2011, codes_2011, out_path='output/neuroscale_projection_2011.csv')

    # 使用 2021 数据（如需要）
    # data_2021, codes_2021 = load_and_prepare_data('table/2021/merged_2021.csv')
    # run_pca(data_2021, codes_2021, out_path='output/pca_projection_2021.csv')
    # run_umap(data_2021, codes_2021, out_path='output/umap_projection_2021.csv')
    # run_neuroscale(data_2021, codes_2021, out_path='output/neuroscale_projection_2021.csv')

    # 可视化
    plot_projection("output/umap_projection_2021.csv", color_by="Economically active",title="Umap_projection_2021")
    plot_projection("output/neuroscale_projection_2021.csv",color_by="Economically active", title="Neuroscale_projection_2021")

if __name__ == '__main__':
    main()
