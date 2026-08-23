import pandas as pd

# Function to report the quality of the dataframe
def rep_quality(df: pd.DataFrame, name: str) -> None:
    print(f"\n--- {name} ---")
    print(f"Dimensions : {df.shape}")
    missing = df.isna().sum()
    duplicates = df.duplicated().sum()
    print(f"Duplicate rows : {duplicates}")
    if missing.any():
        print("Missing values:")
        print(missing[missing > 0])
    else:
        print("No missing values.")