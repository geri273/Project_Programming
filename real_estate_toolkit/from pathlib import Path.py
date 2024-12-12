from pathlib import Path
from src.real_estate_toolkit.data.loader import DataLoader

# Paths to the uploaded files
train_data_path = Path("/mnt/data/train.csv")
test_data_path = Path("/mnt/data/test.csv")

# Instantiate the DataLoader for train and test files
train_loader = DataLoader(data_path=train_data_path)
test_loader = DataLoader(data_path=test_data_path)

# Load train data
print("Testing train.csv...")
train_data = train_loader.load_data_from_csv()
print(f"Loaded {len(train_data)} rows from train.csv.")

# Validate required columns in train.csv
required_columns = ["Id", "SalePrice", "LotArea", "YearBuilt", "BedroomAbvGr"]
is_train_valid = train_loader.validate_columns(required_columns)
print(f"Train.csv valid columns: {is_train_valid}")

# Load test data
print("\nTesting test.csv...")
test_data = test_loader.load_data_from_csv()
print(f"Loaded {len(test_data)} rows from test.csv.")

# Validate required columns in test.csv
required_columns_test = ["Id", "LotArea", "YearBuilt", "BedroomAbvGr"]
is_test_valid = test_loader.validate_columns(required_columns_test)
print(f"Test.csv valid columns: {is_test_valid}")
