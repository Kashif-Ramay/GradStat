"""
Test reading the CSV file directly
"""
import pandas as pd

file_path = r"c:\Users\kashi\CascadeProjects\quran-root-flashcards\gradstat\test-data\normal-data.csv"

# Read the CSV
df = pd.read_csv(file_path)

print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"Dtypes:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nNumeric columns: {list(df.select_dtypes(include=['float64', 'int64', 'int32', 'float32']).columns)}")
