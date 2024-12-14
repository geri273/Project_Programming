from typing import List, Dict
import polars as pl
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

class MarketAnalyzer:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.real_estate_data = pl.read_csv(data_path)
        self.real_state_clean_data = None

    def clean_data(self) -> None:

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

        self.real_state_clean_data = self.real_estate_data
        print("Data cleaning completed.")

    def generate_price_distribution_analysis(self) -> pl.DataFrame:
        
        price_column = 'SalePrice'  
        price_statistics = self.real_state_clean_data.select(
            pl.col(price_column).mean().alias("mean"),
            pl.col(price_column).median().alias("median"),
            pl.col(price_column).std().alias("std_dev"),
            pl.col(price_column).min().alias("min"),
            pl.col(price_column).max().alias("max")
        )
        
       
        fig = px.histogram(self.real_state_clean_data.to_pandas(), x=price_column, nbins=50, title="Sale Price Distribution")
        fig.update_layout(xaxis_title='Sale Price', yaxis_title='Count')
        
     
        output_folder = Path("src/real_estate_toolkit/analytics/outputs/")
        output_folder.mkdir(parents=True, exist_ok=True)
        fig.write_html(output_folder / "price_distribution.html")
        
        print("Price distribution analysis completed.")
        
        return price_statistics

    def neighborhood_price_comparison(self) -> pl.DataFrame:

        neighborhood_stats = self.real_state_clean_data.group_by("Neighborhood").agg(
            [
                pl.col("SalePrice").mean().alias("mean_price"),
                pl.col("SalePrice").median().alias("median_price"),
                pl.col("SalePrice").std().alias("std_dev"),
                pl.col("SalePrice").min().alias("min_price"),
                pl.col("SalePrice").max().alias("max_price"),
            ]
        )

        fig = px.box(
            self.real_state_clean_data.to_pandas(),
            x="Neighborhood",
            y="SalePrice",
            title="Price Comparison Across Neighborhoods",
            labels={"SalePrice": "Price", "Neighborhood": "Neighborhood"},
            points="all",  
        )

        output_folder = Path("src/real_estate_toolkit/analytics/outputs/")
        output_folder.mkdir(parents=True, exist_ok=True)
        fig.write_html(output_folder / "neighborhood_price_comparison.html")

        print("Neighborhood price comparison plot saved.")

        return neighborhood_stats

    def feature_correlation_heatmap(self, variables: List[str]) -> None:

        data = self.real_state_clean_data.select(variables).to_pandas()

        correlation_matrix = data.corr()

        fig = px.imshow(
            correlation_matrix,
            text_auto=True,
            title="Feature Correlation Heatmap"
        )

        output_folder = Path("src/real_estate_toolkit/analytics/outputs/")
        output_folder.mkdir(parents=True, exist_ok=True)
        fig.write_html(output_folder / "correlation_heatmap.html")

        print("Correlation heatmap saved.")

    @staticmethod
    def save_figure_to_html(fig: go.Figure, output_path: Path) -> Path:
        fig.write_html(output_path) 
        return output_path

    def create_scatter_plots(self) -> Dict[str, go.Figure]:

        scatter_plots = {}

        fig1 = px.scatter(
            self.real_state_clean_data.to_pandas(),
            x="GrLivArea", 
            y="SalePrice",
            title="House Price vs. Total Square Footage",
            trendline="ols",  
            hover_data=["OverallQual"],  
            color="OverallQual",  
            labels={"GrLivArea": "Total Square Footage", "SalePrice": "House Price"}
        )
        scatter_plots["House_Price_vs_Square_Feet"] = fig1

        fig2 = px.scatter(
            self.real_state_clean_data.to_pandas(),
            x="YearBuilt", 
            y="SalePrice",
            title="Sale Price vs. Year Built",
            trendline="ols",  
            hover_data=["OverallQual"],  
            color="OverallQual",  
            labels={"YearBuilt": "Year Built", "SalePrice": "Sale Price"}
        )
        scatter_plots["Sale_Price_vs_Year_Built"] = fig2


        fig3 = px.scatter(
            self.real_state_clean_data.to_pandas(),
            x="OverallQual", 
            y="SalePrice",
            title="Overall Quality vs. Sale Price",
            trendline="ols",  
            hover_data=["GrLivArea"],  
            color="OverallQual",  
            labels={"OverallQual": "Overall Quality", "SalePrice": "Sale Price"}
        )
        scatter_plots["Overall_Quality_vs_Sale_Price"] = fig3

        output_folder = Path("src/real_estate_toolkit/analytics/outputs/")
        output_folder.mkdir(parents=True, exist_ok=True)

        for plot_name, fig in scatter_plots.items():
            output_file = self.save_figure_to_html(fig, output_folder / f"{plot_name}.html")
            print(f"HTML file saved at: {output_file}")

        return scatter_plots
