Index):
        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    df = df.rename(columns=lambda c: c.lower()).reset_index()
    time_col = next((c for c in df.columns if c.lower() in ('date', 'datetime')), None)
    df['datetime'] = pd.to_datetime(df[time_col]).dt_tz_localize(None)
    return df[['datetime','open','high','low','close']].sort_values('datetime').reset_index(drop=True)

# ===== Position management =====
def check_position_exit(pos, df_now):
    """Check if open position hit stop/target. Returns updated pos or None.""
    pair = pos['pair']
    pip = pip_size(pair)
    df_idx = df_now.set_index('datetime')
   # Find bars from entry to now
    entry_t = pd.TiM