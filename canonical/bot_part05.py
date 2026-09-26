                    end=(end + pd.Timedelta(days=1)).strftime('%Y-%m-%d'),
                     interval='1h', progress=False)
    if df is None or len(df) < 50:
        return None
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    df = df.rename(columns=lambda c: c.lower()).reset_index()
    time_col = next((c for c in df.columns if c.lower() in ('date', 'datetime