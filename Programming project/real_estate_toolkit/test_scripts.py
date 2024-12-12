import sys
from pathlib import Path

# Dynamically add the 'src' directory to Python's path
current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src"
sys.path.insert(0, str(src_dir))

# Import your modules
from real_estate_toolkit.data.loader import DataLoader
from real_estate_toolkit.data.cleaner import Cleaner

# Paths to CSV files
train_data_path = Path("/mnt/data/train.csv")

# Step 1: Load the data
print("Loading data...")
loader = DataLoader(data_path=train_data_path)
train_data = loader.load_data_from_csv()
print(f"Loaded {len(train_data)} rows from train.csv.")

# Step 2: Clean the data
print("\nCleaning data...")
cleaner = Cleaner(data=train_data)

# Renaming columns
cleaner.rename_with_best_practices()
print("Columns renamed to snake_case. Sample keys:")
print(list(train_data[0].keys()))

# Replacing 'NA' with None
cleaned_data = cleaner.na_to_none()
print("\nReplaced 'NA' with None. Sample row:")
print(cleaned_data[0])



