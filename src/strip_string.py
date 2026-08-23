import pandas as pd
import numpy as np

# Function to strip string columns of whitespace
def strip_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove whitespace from all text columns."""
    out = df.copy()
    for col in out.select_dtypes(include="object").columns:
        out[col] = out[col].astype(str).str.strip().replace({"nan": np.nan, "None": np.nan})
    return out
