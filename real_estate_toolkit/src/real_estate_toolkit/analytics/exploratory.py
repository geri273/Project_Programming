from typing import List, Dict
import polars as pl
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

class MarketAnalyzer:
    def __init__(self, data_path: str):
        """
        Initialize the analyzer with data from a CSV file.
        
        Args:
            data_path (str): Path to the Ames Housing dataset
        """
        self.data_path = data_path
        self.real_estate_data = pl.read_csv(data_path)
        self.cleaned_data = None

    def clean_data(self) -> None:
       
        print("Cleaning data...")

        numeric_columns = self.real_estate_data.select(pl.col(pl.Float64) | pl.col(pl.Int64)).columns
        categorical_columns = [col for col in self.real_estate_data.columns if col not in numeric_columns]

        for col in numeric_columns:
            median_value = self.real_estate_data[col].median()
            self.real_estate_data = self.real_estate_data.with_columns(
                self.real_estate_data[col].fill_null(median_value)
            )

        for col in categorical_columns:
            self.real_estate_data = self.real_estate_data.with_columns(
                self.real_estate_data[col].fill_null("Unknown")
            )

        for col in numeric_columns:
            self.real_estate_data = self.real_estate_data.with_columns(
                self.real_estate_data[col].cast(pl.Float64)
            )

        for col in categorical_columns:
            self.real_estate_data = self.real_estate_data.with_columns(
                self.real_estate_data[col].cast(pl.Utf8)
            )

        self.cleaned_data = self.real_estate_data
        print("Data cleaning completed.")


    def generate_price_distribution_analysis(self, output_path: str) -> None:
        """
        Analyze sale price distribution and create an interactive histogram.
        """
        fig = px.histogram(self.cleaned_data.to_pandas(), x="SalePrice", nbins=50, title="Sale Price Distribution")
        fig.write_html(output_path)

    def neighborhood_price_comparison(self, output_path: str) -> None:
        """
        Create a boxplot comparing house prices across different neighborhoods.
        """
        fig = px.box(self.cleaned_data.to_pandas(), x="Neighborhood", y="SalePrice", title="Neighborhood Price Comparison")
        fig.update_layout(xaxis={'categoryorder':'total ascending'})
        fig.write_html(output_path)

    def feature_correlation_heatmap(self, variables: List[str], output_path: str) -> None:
        """
        Generate a heatmap of feature correlations.
        Args:
            variables (List[str]): List of numeric variables to correlate.
        """
        data = self.cleaned_data.select(variables).to_pandas()
        correlation_matrix = data.corr()
        fig = px.imshow(correlation_matrix, text_auto=True, title="Feature Correlation Heatmap")
        fig.write_html(output_path)

    def create_scatter_plots(self, output_folder: str) -> None:
        """
        Create scatter plots to explore relationships between key features.
        """
        data = self.cleaned_data.to_pandas()
        
        plots = {
            "price_vs_area": px.scatter(data, x="GrLivArea", y="SalePrice", title="Price vs. Living Area", trendline="ols"),
            "price_vs_year_built": px.scatter(data, x="YearBuilt", y="SalePrice", title="Price vs. Year Built", trendline="ols"),
            "quality_vs_price": px.scatter(data, x="OverallQual", y="SalePrice", title="Overall Quality vs. Price", trendline="ols"),
        }

        for name, fig in plots.items():
            fig.write_html(Path(output_folder) / f"{name}.html")
