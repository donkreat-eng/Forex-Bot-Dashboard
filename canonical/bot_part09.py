Index):
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    df = df.rename(columns=lambda c: c.lower()).reset_index()
    time_col = next((c for c in df.columns if c.lower() in ('date', 'datetime')), None)
    df['datetime'] = pd.to_datetime(df[time_col]).dt.tz_localize(None)
    return df[['datetime','open','high','low','close']].sort_values('datetime').reset_index(drop=True)

def pip_value_per_lot_usd(pair, pr