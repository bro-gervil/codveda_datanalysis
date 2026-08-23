import pandas as pd


def ohlc_correct(df: pd.DataFrame) -> pd.DataFrame:
    ohlc_cols = ['open', 'high', 'low', 'close']
    
    missing_values = df[ohlc_cols].isna().sum().sum()
    # --- Step 1 : We process missing values ---
    if missing_values > 0:
        print(f"Missing values : {missing_values} Empty values detected. Forward Fill...")
        
        # Cleaning the dataframe by dropping rows where all OHLC values are NaN
        df = df.dropna(subset=ohlc_cols, how='all')
        
        # Forward Fill (financial data continuity) and Backward Fill (for the first rows)
        df[ohlc_cols] = df[ohlc_cols].ffill().bfill()

    # --- Step 2 : INITIAL CONSISTENCY CHECK ---
    high_valide = df['high'] >= df[['open', 'low', 'close']].max(axis=1)
    low_valide  = df['low'] <= df[['open', 'high', 'close']].min(axis=1)
    
    # The open is incorrect if it exceeds the current high/low bounds
    open_valide = (df['open'] <= df['high']) & (df['open'] >= df['low'])
    
    lignes_valides = high_valide & low_valide & open_valide
    
    # If 100% of the rows are valid, we stop here
    if lignes_valides.all():
        print("✅ Success : All the OHLC data are structurally correct. No process.")
        return df

    # --- Step 3 : Correction of inconsistencies ---
    nb_erreurs = (~lignes_valides).sum()
    print(f"⚠️ : {nb_erreurs} wrong line(s) of data inconsistencies found out. Correction processing...")
    
    # A. Correction of the Open value if it is outside the High/Low bounds
    df['close_precedent'] = df['close'].shift(1)
    open_hors_bornes = (df['open'] > df['high']) | (df['open'] < df['low'])
    
    # If the Open is outside the High/Low bounds, we replace it with the previous Close value (if available)
    df.loc[open_hors_bornes & df['close_precedent'].notna(), 'open'] = df['close_precedent']
    
    # B. Expand the High/Low bounds when they exclude Open or Close.
    high_required = df[['open', 'close']].max(axis=1)
    low_required = df[['open', 'close']].min(axis=1)
    df['high'] = df['high'].clip(lower=high_required)
    df['low'] = df['low'].clip(upper=low_required)
    
    # C. Final security for the Open value (e.g., for the first row of the file)
    df['open'] = df['open'].clip(lower=df['low'], upper=df['high'])
    
    # Cleaning of the temporary column
    df = df.drop(columns=['close_precedent'], errors='ignore')
    
    print("🔄 Correction process ended. All data is now consistent.")
    return df
