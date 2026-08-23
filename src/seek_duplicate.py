import pandas as pd

# Function to seek duplicate rows in the dataframe and return a message with the number of duplicate rows found
def seek_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    duplicate_rows = df[df.duplicated()]
    print(f"Number of duplicate rows: {len(duplicate_rows)}")
    return duplicate_rows
