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

    def generate_price_distribution_analysis(self) -> pl.DataFrame:
        """
        Analyze sale price distribution using clean data.
        
        Tasks to implement:
        1. Compute basic price statistics and generate another data frame called price_statistics:
            - Mean
            - Median
            - Standard deviation
            - Minimum and maximum prices
        2. Create an interactive histogram of sale prices using Plotly.
        
        Returns:
            - Statistical insights dataframe
            - Save Plotly figures for price distribution in src/real_estate_toolkit/analytics/outputs/ folder.
        """
        # Step 1: Compute basic price statistics
        price_column = 'SalePrice'  # Assuming the target column for sale price is "SalePrice"
        price_statistics = self.cleaned_data.select(
            pl.col(price_column).mean().alias("mean"),
            pl.col(price_column).median().alias("median"),
            pl.col(price_column).std().alias("std_dev"),
            pl.col(price_column).min().alias("min"),
            pl.col(price_column).max().alias("max")
        )
        
        # Step 2: Create an interactive histogram of sale prices using Plotly
        fig = px.histogram(self.cleaned_data.to_pandas(), x=price_column, nbins=50, title="Sale Price Distribution")
        fig.update_layout(xaxis_title='Sale Price', yaxis_title='Count')
        
        # Save Plotly figure
        output_folder = Path("src/real_estate_toolkit/analytics/outputs/")
        output_folder.mkdir(parents=True, exist_ok=True)
        fig.write_html(output_folder / "price_distribution.html")
        
        print("Price distribution analysis completed.")
        
        return price_statistics
   

    def neighborhood_price_comparison(self) -> pl.DataFrame:
        """
        Create a boxplot comparing house prices across different neighborhoods.
        
        Tasks to implement:
        1. Group data by neighborhood
        2. Calculate price statistics for each neighborhood
        3. Create Plotly boxplot with:
            - Median prices
            - Price spread
            - Outliers
        
        Returns:
            - Return neighborhood statistics dataframe
            - Save Plotly figures for neighborhood price comparison in src/real_estate_toolkit/analytics/outputs/ folder.
        """
        print("Generating neighborhood price comparison...")

        # Step 1: Group data by neighborhood
        neighborhood_stats = self.cleaned_data.groupby("Neighborhood").agg(
            [
                pl.col("SalePrice").mean().alias("mean_price"),
                pl.col("SalePrice").median().alias("median_price"),
                pl.col("SalePrice").std().alias("std_dev"),
                pl.col("SalePrice").min().alias("min_price"),
                pl.col("SalePrice").max().alias("max_price"),
            ]
        )

        # Step 2: Create Plotly boxplot
        fig = px.box(
            self.cleaned_data.to_pandas(),
            x="Neighborhood",
            y="SalePrice",
            title="Price Comparison Across Neighborhoods",
            labels={"SalePrice": "Price", "Neighborhood": "Neighborhood"},
            points="all",  # Show all data points, including outliers
        )

        # Save the Plotly figure
        output_folder = Path("src/real_estate_toolkit/analytics/outputs/")
        output_folder.mkdir(parents=True, exist_ok=True)
        fig.write_html(output_folder / "neighborhood_price_comparison.html")

        print("Neighborhood price comparison plot saved.")

        return neighborhood_stats


    def feature_correlation_heatmap(self, variables: List[str]) -> None:
        """
        Generate a correlation heatmap for variables input.
        
        Tasks to implement:
        1. Pass a list of numerical variables
        2. Compute correlation matrix and plot it
        
        Args:
            variables (List[str]): List of variables to correlate
        
        Returns:
            Save Plotly figures for correlation heatmap in src/real_estate_toolkit/analytics/outputs/ folder.
        """
        print("Generating correlation heatmap...")

        # Step 1: Filter the data to include only the specified variables
        data = self.cleaned_data.select(variables).to_pandas()

        # Step 2: Compute the correlation matrix
        correlation_matrix = data.corr()

        # Step 3: Create the heatmap using Plotly
        fig = px.imshow(
            correlation_matrix,
            text_auto=True,
            title="Feature Correlation Heatmap"
        )

        # Step 4: Save the Plotly figure
        output_folder = Path("src/real_estate_toolkit/analytics/outputs/")
        output_folder.mkdir(parents=True, exist_ok=True)
        fig.write_html(output_folder / "correlation_heatmap.html")

        print("Correlation heatmap saved.")


    def create_scatter_plots(self) -> Dict[str, go.Figure]:
        """
        Create scatter plots exploring relationships between key features.
        
        Scatter plots to create:
        1. House price vs. Total square footage
        2. Sale price vs. Year built
        3. Overall quality vs. Sale price
        
        Tasks to implement:
        - Use Plotly Express for creating scatter plots
        - Add trend lines
        - Include hover information
        - Color-code points based on a categorical variable
        - Save them in in src/real_estate_toolkit/analytics/outputs/ folder.
        
        Returns:
            Dictionary of Plotly Figure objects for different scatter plots. 
        """
        print("Creating scatter plots...")

        scatter_plots = {}

        # 1. House price vs. Total square footage
        fig1 = px.scatter(
            self.cleaned_data.to_pandas(),
            x="GrLivArea", 
            y="SalePrice",
            title="House Price vs. Total Square Footage",
            trendline="ols",  # Add a trendline
            hover_data=["OverallQual"],  # Show Overall Quality in hover data
            color="OverallQual",  # Color points by Overall Quality
            labels={"GrLivArea": "Total Square Footage", "SalePrice": "House Price"}
        )
        scatter_plots["House_Price_vs_Square_Feet"] = fig1

        # 2. Sale price vs. Year built
        fig2 = px.scatter(
            self.cleaned_data.to_pandas(),
            x="YearBuilt", 
            y="SalePrice",
            title="Sale Price vs. Year Built",
            trendline="ols",  # Add a trendline
            hover_data=["OverallQual"],  # Show Overall Quality in hover data
            color="OverallQual",  # Color points by Overall Quality
            labels={"YearBuilt": "Year Built", "SalePrice": "Sale Price"}
        )
        scatter_plots["Sale_Price_vs_Year_Built"] = fig2

        # 3. Overall quality vs. Sale price
        fig3 = px.scatter(
            self.cleaned_data.to_pandas(),
            x="OverallQual", 
            y="SalePrice",
            title="Overall Quality vs. Sale Price",
            trendline="ols",  # Add a trendline
            hover_data=["GrLivArea"],  # Show Total Square Footage in hover data
            color="OverallQual",  # Color points by Overall Quality
            labels={"OverallQual": "Overall Quality", "SalePrice": "Sale Price"}
        )
        scatter_plots["Overall_Quality_vs_Sale_Price"] = fig3

        # Step: Save the Plotly figures to HTML files
        output_folder = Path("src/real_estate_toolkit/analytics/outputs/")
        output_folder.mkdir(parents=True, exist_ok=True)

        # Save all plots
        for plot_name, fig in scatter_plots.items():
            fig.write_html(output_folder / f"{plot_name}.html")
            print(f"{plot_name} saved.")

        return scatter_plots
