from typing import List, Dict, Any
from pathlib import Path
import polars as pl
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error

class HousePricePredictor:
    def __init__(self, train_data_path: str, test_data_path: str):
        self.train_data = pl.read_csv(train_data_path)
        self.test_data = pl.read_csv(test_data_path)
        self.model: Pipeline = None  
        self.preprocessor = None
        self.target = None
        self.features = None

    def clean_data(self) -> None:
        self.train_data = self.train_data.fill_nan(None).fill_null(0)
        self.test_data = self.test_data.fill_nan(None).fill_null(0)

    def prepare_features(self, target_column: str = 'SalePrice') -> None:
        self.target = target_column
        self.features = [col for col in self.train_data.columns if col != target_column]
        
        sample_df = self.train_data.to_pandas()  
        self.numeric_features = sample_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        self.categorical_features = [col for col in self.features if col not in self.numeric_features]
        
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])
        
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.numeric_features),
                ('cat', categorical_transformer, self.categorical_features)
            ]
        )

    def train_baseline_models(self) -> Dict[str, Dict[str, Any]]:
        full_train_data = self.train_data.to_pandas()
        X = full_train_data.drop(columns=[self.target])
        y = full_train_data[self.target]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        models = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42)
        }
        
        results = {}
        for name, model in models.items():
            pipeline = Pipeline(steps=[
                ('preprocessor', self.preprocessor),
                ('model', model)
            ])
            
            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_test)
            
            results[name] = {
                "MSE": mean_squared_error(y_test, y_pred),
                "MAE": mean_absolute_error(y_test, y_pred),
                "R2": r2_score(y_test, y_pred),
                "MAPE": mean_absolute_percentage_error(y_test, y_pred),
                "model": pipeline  
            }
        
        self.model = results["Random Forest"]["model"]
        return results

    def forecast_sales_price(self, output_path: str) -> None:
        if not self.model:
            raise ValueError("Model has not been trained. Please call train_models() first.")

        X_test = self.test_data.to_pandas()
        
        predictions = self.model.predict(X_test)
        
        submission = pl.DataFrame({
            "Id": self.test_data["Id"].to_list(),
            "SalePrice": predictions
        })
        submission.write_csv(output_path)
        print(f"Predictions saved to {output_path}")

