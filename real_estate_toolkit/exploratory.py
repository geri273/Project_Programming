import polars as pl
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

class EDA:
    def __init__(self, data_path: str):
        """
        Initialize with the path to the dataset and load the data.
        
        Args:
            data_path (str): Path to the CSV file.
        """
        self.data_path = data_path
        self.df = pl.read_csv(data_path)
        self.df_cleaned = None

    def clean_data(self) -> None:
        """
        Clean the dataset:
        - Handle missing values.
        - Convert data types to appropriate formats.
        - Drop rows with missing target variable (SalePrice).
        """
        # Fill missing values (example for numeric columns with median, categorical with mode)
        self.df_cleaned = self.df.fill_nan({
            "LotFrontage": self.df["LotFrontage"].median(),
            "GarageYrBlt": self.df["GarageYrBlt"].median(),
            "BsmtQual": self.df["BsmtQual"].mode(),
            "MasVnrArea": self.df["MasVnrArea"].median(),
            "Electrical": self.df["Electrical"].mode(),
        })
        
        # Convert columns to correct data types
        self.df_cleaned = self.df_cleaned.with_columns([
            pl.col("YrSold").cast(pl.Int64),
            pl.col("OverallQual").cast(pl.Int32),
            pl.col("LotArea").cast(pl.Int64),
            pl.col("GrLivArea").cast(pl.Int64)
        ])
        
        # Drop rows with missing target variable (SalePrice)
        self.df_cleaned = self.df_cleaned.filter(pl.col("SalePrice").is_not_null())

    def descriptive_statistics(self) -> pd.DataFrame:
        """
        Get descriptive statistics for the cleaned data.
        
        Returns:
            pd.DataFrame: Summary statistics (mean, median, std, etc.).
        """
        df_pandas = self.df_cleaned.to_pandas()
        return df_pandas.describe()

    def generate_price_distribution_analysis(self, output_path: str) -> None:
        """
        Generate a histogram of SalePrice distribution.
        
        Args:
            output_path (str): Path to save the plot.
        """
        df_pandas = self.df_cleaned.to_pandas()
        fig = px.histogram(df_pandas, x="SalePrice", nbins=50, title="Sale Price Distribution")
        fig.write_html(output_path)

    def neighborhood_price_comparison(self, output_path: str) -> None:
        """
        Generate a boxplot comparing SalePrice across different neighborhoods.
        
        Args:
            output_path (str): Path to save the plot.
        """
        df_pandas = self.df_cleaned.to_pandas()
        fig = px.box(df_pandas, x="Neighborhood", y="SalePrice", title="Neighborhood Price Comparison")
        fig.update_layout(xaxis={'categoryorder':'total ascending'})
        fig.write_html(output_path)

    def feature_correlation_heatmap(self, variables: list, output_path: str) -> None:
        """
        Generate a heatmap for feature correlations between selected numeric variables.
        
        Args:
            variables (list): List of column names to analyze.
            output_path (str): Path to save the heatmap plot.
        """
        df_pandas = self.df_cleaned.select(variables).to_pandas()
        correlation_matrix = df_pandas.corr()
        fig = px.imshow(correlation_matrix, text_auto=True, title="Feature Correlation Heatmap")
        fig.write_html(output_path)

    def create_scatter_plots(self, output_folder: str) -> None:
        """
        Create scatter plots to explore relationships between key features.
        
        Args:
            output_folder (str): Folder path to save scatter plots.
        """
        df_pandas = self.df_cleaned.to_pandas()
        
        plots = {
            "price_vs_area": px.scatter(df_pandas, x="GrLivArea", y="SalePrice", title="Price vs. Living Area", trendline="ols"),
            "price_vs_year_built": px.scatter(df_pandas, x="YearBuilt", y="SalePrice", title="Price vs. Year Built", trendline="ols"),
            "quality_vs_price": px.scatter(df_pandas, x="OverallQual", y="SalePrice", title="Overall Quality vs. Price", trendline="ols"),
        }

        for name, fig in plots.items():
            fig.write_html(f"{output_folder}/{name}.html")
