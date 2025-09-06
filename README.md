# Visual-Analytics-of-UK-Employment-and-Ethnic-Structure-2011-2021-under-Impact-of-COVID-19

This project conducts a visual analysis of socio-economic transformations across regions of England and Wales, leveraging UK Census datasets from 2011 and 2021. specifically investigating the impact of the COVID-19 pandemic on employment by comparing observed 2021 data against a counterfactual Bayesian forecast based on pre-pandemic trends.

## 📊 Dashboard Preview

An interactive Tableau dashboard was designed to explore the complex relationships between geography, ethnicity, and economic activity, presenting an intuitive visual report.

| Employment Analysis & COVID-19 Impact | Dimensionality Reduction & Geographic Projection |
| :---: | :---: |
| ![Dashboard Page 1](./report/figures/page1.png) | ![Dashboard Page 3](./report/figures/page3.png) |
| **Ethnic & Economic Composition** | **Long-term Trend Analysis** |
| ![Dashboard Page 4](./report/figures/page4.jpg) | ![Dashboard Page 2](./report/figures/page2.png) |

## 🎯 Core Research Questions

This project aims to answer several key questions through data modeling and visualization:
1.  **Socio-Economic Change:** How did the composition of the labour force and ethnic diversity change across England and Wales between 2011 and 2021?
2.  **Impact of COVID-19:** What was the structural impact of the COVID-19 pandemic on employment? How do the actual 2021 employment figures deviate from predictions based on a "no-pandemic" scenario?
3.  **Latent Patterns:** Are there hidden clusters or patterns in the relationship between regional demographics, ethnicity, and economic outcomes?

## 🔬 Methodology

The analysis follows four stage pipeline:

1.  **Data Preparation Pipeline:** Raw census data from multiple sources for 2011 and 2021 are cleaned, harmonized, and merged into unified datasets.
2.  **Bayesian Forecasting:** A Bayesian linear regression model, implemented in Python with `Pymc`, is trained on 2011-2019 regional employment data to generate a probabilistic forecast for 2021. This creates a counterfactual baseline of what employment might have looked like without the pandemic.
3.  **Dimensionality Reduction:** Two non-linear projection techniques, **UMAP** and **Neuroscale**, are applied to the high-dimensional census data to uncover and visualize latent socio-ethnic structures in a 2D space.
4.  **Visualization:** The processed data, predictions, and projections are loaded into **Tableau** to create an interactive dashboard for exploratory visual analysis.

## 📁 Repository Structure

The repository is organized to separate data, source code, the final report, and the Tableau workbook.
```
.
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── bayesian_model_prediction.py
│   ├── col_check.py
│   ├── data_projection.py
│   ├── pred_cmp_analysis.py
│   ├── prepare_data.py
│   ├── tabelmerge.py
│   └── tableconvert.py
├── tableau/
│   ├── Employment_Dashboard.twbx
│   ├── Visual_Analytics_formal_Report.pdf
│   ├── Tableau_Geocoding_Cheat_Sheet.pdf
│   └── dashboards.png
├── report/
│   ├── Visual_Analytics_formal_Report.pdf
│   └── figures/
└── README.md
```
## ⚙ Dependencies & Installation 🔧


This project requires Python 3.8+ and several scientific computing libraries. Core dependencies include:
* `pandas` & `numpy` for data manipulation.
* `pymc` & `arviz` for Bayesian modeling.
* `scikit-learn` & `umap-learn` for machine learning and dimensionality reduction.
* `torch` for the Neuroscale implementation.
* `matplotlib` & `seaborn` for static visualizations.

```bash
pip install pandas numpy pymc arviz tqdm scikit-learn umap-learn torch matplotlib seaborn
```

Alternatively, for users of the Conda package manager, it is recommended to install dependencies from the conda-forge channel for the most up-to-date versions.

```Bash
conda install -c conda-forge pandas numpy pymc arviz tqdm scikit-learn umap-learn pytorch matplotlib seaborn
```

## 🚀 Execution

The analysis is performed by running the Python scripts located in the `src/` directory in a specific order. Each script performs a step in the data processing and modeling pipeline.

1.  **Merge Raw Data:**
    Run `tabelmerge.py` to combine the separate raw files on ethnicity and economic activity for both 2011 and 2021.
    ```bash
    python src/tabelmerge.py
    ```
2.  **Prepare and Clean Data:**
    Run `prepare_data.py` to standardize columns, add features (like ratios), and create a unified dataset for analysis.
    ```bash
    python src/prepare_data.py
    ```
3.  **Generate Bayesian Forecast:**
    Execute the Bayesian model to generate the 2021 employment predictions based on pre-2020 trends. **Note: This script can be computationally intensive.**
    ```bash
    python src/bayesian_model_prediction.py
    ```
4.  **Run Dimensionality Reduction:**
    Apply UMAP and Neuroscale to the processed data to generate the 2D projections.
    ```bash
    python src/data_projection.py
    ```
5.  **Analyze Prediction vs. Actual Data:**
    Run this script to generate comparison tables (residuals, relative error) and plots (bar charts, heatmaps) of the model's predictions versus the actual 2021 census data.
    ```bash
    python src/pred_cmp_analysis.py
    ```

6.  **Visualize in Tableau:**
    After running the scripts, the `data/processed/` folder will contain the necessary datasets. Open the `tableau/Employment_Dashboard.twbx` workbook in Tableau and refresh the data sources to link them to your newly generated files.

## 📚 References

* **[1] Gelman, A., et al. (2013).** *Bayesian Data Analysis*. CRC Press.
* **[2] McInnes, L., Healy, J., & Melville, J. (2018).** UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. *arXiv preprint arXiv:1802.03426*.
* **[3] Bishop, C. M., James, G. D., & Nasrabadi, N. M. (1998).** Neuroscale: Novel topographic projection technique for multivariate data. *Neural Networks*, 11(2), 277-290.
* **[4] Munzner, T. (2014).** *Visualization Analysis and Design*. CRC Press.

